#!/usr/bin/env python3
"""
Fout in adjectives/onveranderlijk: de vraag beantwoordt zichzelf.

De oefening bouwt een fout antwoord door -s achter het bijvoeglijk naamwoord te
plakken. Bij woorden die op -e eindigen (verde, grande, fuerte, caliente) is dat
precies de goede meervoudsvorm: fuerte + s = fuertes. ex() gooit dubbele opties
weg, dus blijft er een enkele knop over -- met het juiste antwoord erop. Ongeveer
een op de vijf keer een gratis punt en een scherm met een losse knop.

Oplossing: valt de foute vorm samen met de goede, gebruik dan de enkelvoudsvorm
als afleider (fuerte tegenover fuertes). Dat is een echte keuze en leert precies
wat hier telt: onveranderlijk voor geslacht, maar niet voor meervoud.

Idempotent: al toegepast -> doet niets. Past de code niet -> harde fout.

Gebruik: 05-onveranderlijk-afleider.py <repo-map>
"""
import sys, pathlib

MARK = "/* PATCH: afleider mag niet gelijk zijn aan het antwoord */"

OUD_BAD = '''  const bad = plural ? a.es+"s" : (w.g==="f" ? a.es.replace(/.$/,"a") : a.es+"o");'''

NIEUW_BAD = '''  ''' + MARK + '''
  let bad = plural ? a.es+"s" : (w.g==="f" ? a.es.replace(/.$/,"a") : a.es+"o");
  let badWhy = L("Die vorm bestaat niet.","That form does not exist. Only -o adjectives have four forms.");
  if(bad === right){
    bad = a.es;
    badWhy = L("Dat is de enkelvoudsvorm. Het onderwerp is meervoud, dus er hoort een -s achter: "+right+".",
               "That is the singular form. The subject is plural, so it needs an -s: "+right+".");
  }'''

OUD_WHY = '''    wrongWhy:{[bad]:L("Die vorm bestaat niet.","That form does not exist. Only -o adjectives have four forms.")},'''
NIEUW_WHY = '''    wrongWhy:{[bad]:badWhy},'''


def sub1(s, old, new, wat):
    n = s.count(old)
    if n != 1:
        raise SystemExit("FOUT: %s %d keer gevonden -- de code is van vorm veranderd" % (wat, n))
    return s.replace(old, new, 1)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("gebruik: 05-onveranderlijk-afleider.py <repo-map>")
    f = pathlib.Path(sys.argv[1]) / "index.html"
    if not f.is_file():
        raise SystemExit("FOUT: index.html ontbreekt")
    s = f.read_text(encoding="utf-8")
    if MARK in s:
        print("   index.html  al gepatcht")
        return
    s = sub1(s, OUD_BAD, NIEUW_BAD, "de bad-regel")
    s = sub1(s, OUD_WHY, NIEUW_WHY, "de wrongWhy-regel")
    f.write_text(s, encoding="utf-8")
    print("   index.html  gepatcht")


main()
