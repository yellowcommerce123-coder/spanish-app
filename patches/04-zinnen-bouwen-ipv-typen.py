#!/usr/bin/env python3
"""
Hele zinnen intypen wordt hele zinnen bouwen.

Een beginner die een Spaanse zin uit het niets moet opschrijven doet drie dingen
tegelijk: de zin bedenken, de woorden kennen en ze goed spellen. Dat is te veel
ineens. Deze patch haakt in op ex(), de fabriek waar elke oefening doorheen komt,
en zet elke typ-oefening met een antwoord van drie woorden of meer om naar een
bouwoefening: de woorden liggen klaar, jij bepaalt de volgorde.

Blijft wel typen, want dat is geen zin schrijven maar een vorm invullen:
  - antwoorden van een of twee woorden (stam, meervoudsvorm, "es, está")
  - antwoorden met een + erin (verbstem/splits: "habl + ar")
  - getallen als cijfer

Werkt zonder de nakijklogica aan te raken: grade() behandelt input en build al
identiek, en sameLoose() negeert leestekens, hoofdletters en accenten.

Idempotent: al toegepast -> doet niets. Past de code niet -> harde fout.

Gebruik: 04-zinnen-bouwen-ipv-typen.py <repo-map>
"""
import sys, pathlib

MARK = "/* PATCH: zinnen bouwen in plaats van typen */"

OUD = '''function ex(o){
  if(!o.kind) o.kind = ({mc:"Meerkeuze",input:"Vul in",build:"Zin bouwen",order:"Zet in de juiste orde",'''

NIEUW = '''function ex(o){
  ''' + MARK + '''
  if(o.type==="input" && typeof o.answer==="string" && o.answer.indexOf("+") < 0){
    const woorden = o.answer.replace(/[.,;:\\u00bf?\\u00a1!]/g, " ").split(/\\s+/).filter(Boolean);
    if(woorden.length >= 3){
      o.accept = (o.accept || [o.answer]).concat([woorden.join(" "), o.answer]);
      o.pool = R.shuffle(woorden.slice());
      o.type = "build";
    }
  }
  if(!o.kind) o.kind = ({mc:"Meerkeuze",input:"Vul in",build:"Zin bouwen",order:"Zet in de juiste orde",'''


def patch_html(p):
    s = p.read_text(encoding="utf-8")
    if MARK in s:
        return "index.html  al gepatcht"
    n = s.count(OUD)
    if n != 1:
        raise SystemExit("FOUT: ex() %d keer gevonden -- de code is van vorm veranderd" % n)
    p.write_text(s.replace(OUD, NIEUW, 1), encoding="utf-8")
    return "index.html  gepatcht"


def main():
    if len(sys.argv) < 2:
        raise SystemExit("gebruik: 04-zinnen-bouwen-ipv-typen.py <repo-map>")
    f = pathlib.Path(sys.argv[1]) / "index.html"
    if not f.is_file():
        raise SystemExit("FOUT: index.html ontbreekt")
    print("   " + patch_html(f))


main()
