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
- `AZULEJO_ADMIN_TOKEN` — oud beheerderswachtwoord; alleen nog gebruikt als terugval
- `AZULEJO_ADMIN_PASS` — **het wachtwoord van het beheerdersaccount**. Staat deze
  ingesteld, dan komt alleen `AZULEJO_ADMIN_EMAIL` met dit wachtwoord bij de
  beheerpagina, en telt het losse token niet meer mee
- `AZULEJO_ADMIN_EMAIL` — beheerdersaccount (standaard `jurreb@live.nl`)

## Deployen

Elke push naar `main` deployt automatisch naar productie.

Nieuwe versie als zip binnengekregen? Zet hem in `~/Downloads` en draai:

```bash
~/Projects/deploy-spanish-app.sh
```

Dat pakt de nieuwste zip uit `~/Downloads` (ook als de app in een zip ín die zip
zit), controleert de inhoud, scant op per ongeluk meegekomen sleutels of tokens
(deze repo is publiek), vervangt de bestanden, commit en pusht. Vercel doet de rest.

`README.md`, `.gitignore`, `LICENSE` en `patches/` blijven bij een update staan —
die horen bij de repo, niet bij de zip.

## Eigen aanpassingen: `patches/`

De zip overschrijft `index.html` en `api/progress.js` volledig. Alles wat wij zelf
aan die bestanden veranderen staat daarom als script in `patches/`, en het
deploy-script past die na elke update opnieuw toe.

- `01-admin-login.py` — schermt de beheerpagina af op de inlog van het
  beheerdersaccount in plaats van op een los token
- `02-waarschuwing-zonder-account.py` — laat "Verder zonder account" eerst
  waarschuwen dat de voortgang alleen in die browser blijft
- `03-hay-zin-bouwen.py` — maakt van de typ-oefening op de tegel "Hay en está"
  een bouwoefening, met de andere vorm (hay/está) als extra keuze in de bak
- `04-zinnen-bouwen-ipv-typen.py` — haakt in op `ex()` en zet elke typ-oefening
  met een antwoord van drie woorden of meer om naar een bouwoefening. Antwoorden
  van een of twee woorden (werkwoordsvorm, lidwoord + zelfstandig naamwoord,
  getal) blijven typen: dat is een vorm invullen, geen zin schrijven
- `05-onveranderlijk-afleider.py` — in adjectives/onveranderlijk viel de foute
  optie samen met het antwoord bij woorden op -e (fuerte + s = fuertes)
- `06-engels-afmaken.py` — brokken Nederlands in de Engelse versie; de meeste
  vertalingen bestonden al maar liepen niet door `T()`
- `07-meervoud-afleider.py` — in plural/keuze miste de klinkertest de accenten,
  waardoor bebé, sofá, café en té zichzelf beantwoordden
- `08-engels-restjes.py` — de laatste labels die niet door `T()` liepen

Een patch is idempotent en stopt met een harde fout als de code van vorm is
veranderd. In dat geval breekt de deploy af en wordt er niets gepusht — liever
geen update dan een update zonder afscherming.
