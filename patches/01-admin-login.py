#!/usr/bin/env python3
"""
Beheerpagina afschermen op de inlog van het beheerdersaccount.

Zonder deze patch geeft de server toegang aan iedereen die het
AZULEJO_ADMIN_TOKEN kent, en is de e-mailcheck in de app puur cosmetisch.
Met deze patch geldt: staat AZULEJO_ADMIN_PASS in Vercel, dan komt er alleen
iemand binnen die inlogt als AZULEJO_ADMIN_EMAIL met het juiste wachtwoord.
Staat die variabele er nog niet, dan blijft het oude token werken en biedt de
app dat veld vanzelf aan, zodat je jezelf niet buitensluit.

Idempotent: al toegepast -> doet niets. Past de code niet -> harde fout,
zodat een deploy afbreekt in plaats van de afscherming stilletjes te lossen.

Gebruik: 01-admin-login.py <repo-map>
"""
import sys, pathlib

import _lib

MARK = "/* PATCH: admin via accountlogin */"



def patch_api(p):
    s = p.read_text(encoding="utf-8")
    if MARK in s:
        return "api/progress.js  al gepatcht"

    s = _lib.eenmalig(s,
        'const ADMIN_TOKEN = process.env.AZULEJO_ADMIN_TOKEN || "";',
        'const ADMIN_TOKEN = process.env.AZULEJO_ADMIN_TOKEN || "";\n' + MARK + '''
const ADMIN_EMAIL = String(process.env.AZULEJO_ADMIN_EMAIL || "jurreb@live.nl").trim().toLowerCase();
const ADMIN_PASS  = process.env.AZULEJO_ADMIN_PASS || "";''',
        "ADMIN_TOKEN-regel")

    s = _lib.eenmalig(s,
        '''      if (!ADMIN_TOKEN) {
        return res.status(503).json({ error: "admin_disabled", hint: "Set AZULEJO_ADMIN_TOKEN in Vercel and redeploy." });
      }
      if (!safeEqual(body.token || "", ADMIN_TOKEN)) {
        return res.status(403).json({ error: "bad_token" });
      }''',
        '''      /* Staat AZULEJO_ADMIN_PASS ingesteld, dan is de accountlogin de enige weg
         naar binnen en telt het losse token niet meer mee. */
      if (ADMIN_PASS) {
        const okEmail = cleanEmail(body.email) === ADMIN_EMAIL;
        const okPass  = safeEqual(body.pass || "", ADMIN_PASS);
        if (!okEmail || !okPass) {
          return res.status(403).json({ error: "not_admin" });
        }
      } else if (ADMIN_TOKEN) {
        if (!safeEqual(body.token || "", ADMIN_TOKEN)) {
          return res.status(403).json({ error: "bad_token" });
        }
      } else {
        return res.status(503).json({
          error: "admin_disabled",
          hint: "Set AZULEJO_ADMIN_PASS (or AZULEJO_ADMIN_TOKEN) in Vercel and redeploy."
        });
      }''',
        "admin-gate")

    p.write_text(s, encoding="utf-8")
    return "api/progress.js  gepatcht"


def patch_html(p):
    s = p.read_text(encoding="utf-8")
    if MARK in s:
        return "index.html       al gepatcht"

    # 1. accountgegevens meesturen; niet blokkeren op een leeg tokenveld
    s = _lib.eenmalig(s,
        '''  if(!ADM.token){ ADM.msg = "Vul eerst het beheerderswachtwoord in."; return renderAdmin(); }
  ADM.msg = "Bezig..."; renderAdmin();
  try{
    const j = await api(Object.assign({action:"admin", token:ADM.token, op:op}, extra||{}));
    if(op==="list"){ ADM.users = j.users || []; ADM.msg = ADM.users.length+" account(s) opgehaald."; }
    if(op==="delete"){ ADM.msg = "Account verwijderd."; return admCall("list"); }
  }catch(err){ ADM.msg = apiUitleg(err); }''',
        '''  ''' + MARK + '''
  if(!isAdmin()){ ADM.msg = "Deze pagina hoort bij een ander account."; return renderAdmin(); }
  ADM.msg = "Bezig..."; renderAdmin();
  try{
    const j = await api(Object.assign({action:"admin", op:op,
      email:AUTH.email||"", pass:AUTH.pass||"", token:ADM.token||""}, extra||{}));
    ADM.needToken = false;
    if(op==="list"){ ADM.users = j.users || []; ADM.msg = ADM.users.length+" account(s) opgehaald."; }
    if(op==="delete"){ ADM.msg = "Account verwijderd."; return admCall("list"); }
  }catch(err){
    const code = String(err && err.message || err);
    if(code==="bad_token" || code==="admin_disabled") ADM.needToken = true;
    if(code==="not_admin") ADM.needToken = false;
    ADM.msg = apiUitleg(err);
  }''',
        "admCall()")

    # 2. tokenveld vervangen door uitleg; veld alleen tonen als het echt nodig is
    s = _lib.eenmalig(s,
        """  h += '<div class="card pad stack-14"><div><div class="h-md">Beheerderswachtwoord</div>'
    + '<p class="prose" style="font-size:15px">Dit is niet je gewone wachtwoord. Het is de waarde die je in Vercel hebt gezet als '
    + '<span class="mono">AZULEJO_ADMIN_TOKEN</span>. Zonder dat wachtwoord weigert de server elke beheeractie, ook al zie je deze pagina.</p></div>'
    + '<input class="inp" id="adm-token" type="password" placeholder="Beheerderswachtwoord" value="'+(ADM.token||"")+'">'
    + '<div class="row"><button class="btn btn-primary btn-sm" data-adm="list">Accounts ophalen</button>'
    + '<button class="btn btn-ghost btn-sm" data-adm="forget">Wachtwoord vergeten op dit apparaat</button></div>'
    + '<div class="tiny dim" id="adm-msg">'+(ADM.msg||"")+'</div></div>';""",
        """  h += '<div class="card pad stack-14"><div><div class="h-md">Ingelogd als beheerder</div>'
    + '<p class="prose" style="font-size:15px">Je bent binnen op je eigen account '
    + '(<span class="mono">'+(AUTH.email||"")+'</span>). De server controleert bij elke beheeractie '
    + 'je e-mailadres en je wachtwoord. Wie een ander wachtwoord gebruikt, krijgt niets te zien.</p></div>'
    + (ADM.needToken
        ? '<div class="note note-granada"><p class="prose" style="font-size:15px">De server accepteert je accountlogin nog niet. '
          + 'Zet in Vercel de variabele <span class="mono">AZULEJO_ADMIN_PASS</span> op het wachtwoord van dit account '
          + 'en deploy opnieuw. Tot die tijd kun je hieronder het oude beheerderswachtwoord gebruiken.</p></div>'
          + '<input class="inp" id="adm-token" type="password" placeholder="Beheerderswachtwoord (AZULEJO_ADMIN_TOKEN)" value="'+(ADM.token||"")+'">'
        : '')
    + '<div class="row"><button class="btn btn-primary btn-sm" data-adm="list">Accounts ophalen</button>'
    + '<button class="btn btn-ghost btn-sm" data-adm="forget">Beheerderswachtwoord vergeten op dit apparaat</button></div>'
    + '<div class="tiny dim" id="adm-msg">'+(ADM.msg||"")+'</div></div>';""",
        "beheer-invoerblok")

    # 3. nette foutmelding voor een afgewezen accountlogin
    s = _lib.eenmalig(s,
        '''  if(m==="bad_token") return "Dat beheerderswachtwoord klopt niet.";''',
        '''  if(m==="bad_token") return "Dat beheerderswachtwoord klopt niet.";
  if(m==="not_admin") return "Dit account heeft geen beheerrechten, of het wachtwoord klopt niet.";''',
        "apiUitleg()")

    p.write_text(s, encoding="utf-8")
    return "index.html       gepatcht"


def main():
    if len(sys.argv) < 2:
        raise SystemExit("gebruik: 01-admin-login.py <repo-map>")
    root = pathlib.Path(sys.argv[1])
    for f in ("api/progress.js", "index.html"):
        if not (root / f).is_file():
            raise SystemExit("FOUT: %s ontbreekt in %s" % (f, root))
    print("   " + patch_api(root / "api/progress.js"))
    print("   " + patch_html(root / "index.html"))


main()
