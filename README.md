# spanish-app (Azulejo)

Statische app met één serverless functie, gehost op Vercel.

**Live:** https://spanishapp-eta.vercel.app
**Vercel-project:** `spanish_app`

## Structuur

| Pad | Wat |
|---|---|
| `index.html` | de hele app, één bestand |
| `api/progress.js` | serverless functie, slaat voortgang op in Redis/KV |
| `vercel.json` | cache-headers (geen caching op `/` en `/api/*`) |

Framework preset: **Other**. Er is geen build-stap.

## Environment variables

Staan in Vercel onder Settings → Environment Variables, niet in deze repo:

- Redis/KV-koppeling — `KV_REST_API_URL` + `KV_REST_API_TOKEN` (of de Upstash-varianten)
- `AZULEJO_SALT` — salt voor het hashen van gebruikers
- `AZULEJO_ADMIN_TOKEN` — beheerderswachtwoord; zonder deze weigert de admin-API

## Deployen

Elke push naar `main` deployt automatisch naar productie.

Nieuwe versie als zip binnengekregen? Dan:

```bash
~/Projects/deploy-spanish-app.sh
```

Dat pakt de nieuwste zip uit `~/Downloads`, controleert de inhoud, scant op
per ongeluk meegekomen sleutels of tokens (deze repo is publiek), vervangt de
bestanden, commit en pusht. Vercel doet de rest.
