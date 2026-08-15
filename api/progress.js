import crypto from "crypto";

/* ------------------------------------------------------------------
   Find the Redis credentials, whatever prefix the Vercel integration
   decided to use.
   ------------------------------------------------------------------ */
function findStore() {
  const env = process.env;

  const known = [
    ["KV_REST_API_URL", "KV_REST_API_TOKEN"],
    ["UPSTASH_REDIS_REST_URL", "UPSTASH_REDIS_REST_TOKEN"],
    ["REDIS_REST_URL", "REDIS_REST_TOKEN"],
    ["STORAGE_REST_API_URL", "STORAGE_REST_API_TOKEN"],
    ["STORAGE_KV_REST_API_URL", "STORAGE_KV_REST_API_TOKEN"]
  ];
  for (const [u, t] of known) {
    if (env[u] && env[t]) return { base: env[u], token: env[t] };
  }

  for (const key of Object.keys(env)) {
    if (!/REST_(API_)?URL$/.test(key)) continue;
    const val = env[key];
    if (!val || !/^https?:\/\//.test(val)) continue;
    const tokenKey = key.replace(/URL$/, "TOKEN");
    if (env[tokenKey]) return { base: val, token: env[tokenKey] };
  }

  return null;
}

function storeHints() {
  return Object.keys(process.env)
    .filter(k => /(KV|REDIS|UPSTASH|STORAGE)/i.test(k))
    .sort();
}

const SALT = process.env.AZULEJO_SALT || "azulejo-default-salt";
const ADMIN_TOKEN = process.env.AZULEJO_ADMIN_TOKEN || "";
const USERS_KEY = "azulejo:users";

const sha = s => crypto.createHash("sha256").update(s).digest("hex");
const cleanEmail = e => String(e || "").trim().toLowerCase();

const dataKey = (email, pass) =>
  "azulejo:d:" + sha(cleanEmail(email) + "\u0000" + String(pass || "") + "\u0000" + SALT).slice(0, 40);

const userField = email => sha(cleanEmail(email) + "\u0000" + SALT).slice(0, 32);

/* Vercel puts the visitor's address in x-forwarded-for. The first entry is
   the client; the rest are proxies. */
function clientIp(req) {
  const h = req.headers || {};
  const fwd = h["x-forwarded-for"] || h["X-Forwarded-For"] || "";
  const first = String(fwd).split(",")[0].trim();
  return first || String(h["x-real-ip"] || "") || "";
}
function geo(req) {
  const h = req.headers || {};
  const country = h["x-vercel-ip-country"] || "";
  const city = h["x-vercel-ip-city"] || "";
  return [decodeURIComponent(String(city)), String(country)].filter(Boolean).join(", ");
}

async function redis(store, cmd) {
  const res = await fetch(store.base.replace(/\/$/, ""), {
    method: "POST",
    headers: { Authorization: "Bearer " + store.token, "Content-Type": "application/json" },
    body: JSON.stringify(cmd)
  });
  if (!res.ok) throw new Error("store responded " + res.status);
  const j = await res.json();
  return j.result;
}

const parse = v => {
  if (v == null) return null;
  if (typeof v !== "string") return v;
  try { return JSON.parse(v); } catch (e) { return null; }
};

function safeEqual(a, b) {
  const x = Buffer.from(String(a));
  const y = Buffer.from(String(b));
  if (x.length !== y.length) return false;
  return crypto.timingSafeEqual(x, y);
}

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST" && req.method !== "GET") {
    return res.status(405).json({ error: "method_not_allowed" });
  }

  const store = findStore();
  if (!store) {
    return res.status(500).json({
      error: "no_store",
      hint: "No Redis credentials found. Connect an Upstash for Redis database to this project and redeploy.",
      found: storeHints()
    });
  }

  let body = req.method === "GET" ? Object.assign({ action: "load" }, req.query) : req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  body = body || {};

  const action = String(body.action || "load");

  try {
    /* ---------------- admin ---------------- */
    if (action === "admin") {
      if (!ADMIN_TOKEN) {
        return res.status(503).json({ error: "admin_disabled", hint: "Set AZULEJO_ADMIN_TOKEN in Vercel and redeploy." });
      }
      if (!safeEqual(body.token || "", ADMIN_TOKEN)) {
        return res.status(403).json({ error: "bad_token" });
      }

      const op = String(body.op || "list");

      if (op === "list") {
        const flat = (await redis(store, ["HGETALL", USERS_KEY])) || [];
        const users = [];
        for (let i = 0; i < flat.length; i += 2) {
          const rec = parse(flat[i + 1]);
          if (rec) users.push(Object.assign({ field: flat[i] }, rec));
        }
        users.sort((a, b) => (b.savedAt || 0) - (a.savedAt || 0));
        return res.status(200).json({ users: users });
      }

      if (op === "delete") {
        const field = body.field || userField(body.email);
        await redis(store, ["HDEL", USERS_KEY, field]);
        return res.status(200).json({ ok: true });
      }

      return res.status(400).json({ error: "bad_op" });
    }

    /* ---------------- load ---------------- */
    if (action === "load") {
      if (!body.code && !cleanEmail(body.email)) return res.status(400).json({ error: "no_email" });
      const key = body.code
        ? "azulejo:" + sha("azulejo:" + body.code).slice(0, 32)
        : dataKey(body.email, body.pass);
      const raw = await redis(store, ["GET", key]);
      return res.status(200).json({ data: parse(raw) });
    }

    /* ---------------- save ---------------- */
    if (action === "save") {
      const email = cleanEmail(body.email);
      if (!email && !body.code) return res.status(400).json({ error: "no_email" });
      if (!body.data || typeof body.data !== "object") return res.status(400).json({ error: "bad_data" });

      const value = JSON.stringify(body.data);
      if (value.length > 400000) return res.status(413).json({ error: "too_big" });

      const key = body.code
        ? "azulejo:" + sha("azulejo:" + body.code).slice(0, 32)
        : dataKey(email, body.pass);

      await redis(store, ["SET", key, value, "EX", 63072000]);

      if (email) {
        const m = body.meta || {};
        const field = userField(email);

        /* keep whatever we already knew about this account */
        const prev = parse(await redis(store, ["HGET", USERS_KEY, field])) || {};

        const ip = clientIp(req);
        const where = geo(req);
        const now = Date.now();

        const rec = {
          email: email,
          xp: m.xp || 0,
          answered: m.answered || 0,
          correct: m.correct || 0,
          seconds: m.seconds || 0,
          savedAt: now,
          createdAt: prev.createdAt || now,
          firstIp: prev.firstIp || ip,
          ip: ip,
          where: where || prev.where || "",
          sessions: (prev.sessions || 0) + (body.newSession ? 1 : 0),
          lang: body.lang || prev.lang || ""
        };
        await redis(store, ["HSET", USERS_KEY, field, JSON.stringify(rec)]);
      }

      return res.status(200).json({ ok: true, bytes: value.length });
    }

    return res.status(400).json({ error: "bad_action" });
  } catch (err) {
    return res.status(502).json({ error: "store_failed", detail: String(err.message || err) });
  }
}
