#!/usr/bin/env python3
"""
Fout in plural/keuze: bij woorden met een accent beantwoordt de vraag zichzelf.

De oefening maakt een fout meervoud door de verkeerde regel toe te passen. De
klinkertest daarvoor is /[aeiou]$/ en kent dus geen accenten. Woorden als bebé,
sofá, café en té belanden daardoor in de medeklinker-tak, waar er -s achter komt
-- precies het goede meervoud. Twee identieke opties, ex() gooit de dubbele weg,
en er blijft een enkele knop over met het juiste antwoord erop.

De app zelf doet het elders wel goed: pluralReason() gebruikt /[aeiouaeiou]$/
mét accenten. Deze patch trekt de test gelijk en legt er een vangnet onder, zodat
de foute optie nooit meer gelijk kan zijn aan het antwoord.

Idempotent: al toegepast -> doet niets. Past de code niet -> harde fout.

Gebruik: 07-meervoud-afleider.py <repo-map>
"""
import sys, pathlib

MARK = "/* PATCH: meervoud-afleider mag niet het antwoord zijn */"

OUD = '''  const bad = w.es.endsWith("z") ? w.es+"es" : (/[aeiou]$/.test(w.es) ? w.es+"es" : w.es+"s");'''

NIEUW = '''  ''' + MARK + '''
  const klinker = /[aeiouáéíóú]$/.test(w.es);
  let bad = w.es.endsWith("z") ? w.es+"es" : (klinker ? w.es+"es" : w.es+"s");
  if(bad === w.pl) bad = klinker ? w.es+"s" : w.es+"es";
  if(bad === w.pl) bad = w.es;'''


def main():
    if len(sys.argv) < 2:
        raise SystemExit("gebruik: 07-meervoud-afleider.py <repo-map>")
    f = pathlib.Path(sys.argv[1]) / "index.html"
    if not f.is_file():
        raise SystemExit("FOUT: index.html ontbreekt")
    s = f.read_text(encoding="utf-8")
    if MARK in s:
        print("   index.html  al gepatcht")
        return
    n = s.count(OUD)
    if n != 1:
        raise SystemExit("FOUT: plural/keuze %d keer gevonden -- de code is van vorm veranderd" % n)
    f.write_text(s.replace(OUD, NIEUW, 1), encoding="utf-8")
    print("   index.html  gepatcht")


main()
