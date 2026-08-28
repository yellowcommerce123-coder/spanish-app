#!/usr/bin/env python3
"""
De tegel "Hay en está" makkelijker maken voor beginners.

Drie van de vier oefeningen op die tegel zijn meerkeuze, maar de vierde
(hay/nl2es) laat je een complete Spaanse zin intypen. Dat is een flinke sprong:
je moet de zin niet alleen begrijpen maar ook spellen en uit het niets opbouwen.

Deze patch maakt er een bouwoefening van: de woorden staan klaar en je tikt ze
aan in de goede volgorde. Als extra keuze ligt ook de andere vorm in de bak --
staat er hay in de zin, dan ligt está erbij en omgekeerd. Je moet dus nog steeds
kiezen tussen hay en está, alleen hoef je niet meer te typen.

Idempotent: al toegepast -> doet niets. Past de code niet -> harde fout.

Gebruik: 03-hay-zin-bouwen.py <repo-map>
"""
import sys, pathlib

MARK = "/* PATCH: hay als bouwoefening */"

OUD = '''  return {type:"input", prompt:L("Vertaal naar het Spaans.","Translate into Spanish."),
    sentence:nl, showEs:es, answer:es, accept:[es, es.replace(".","")], word:w.key,
    why:nieuw
      ? L("Je zegt er is een, dus het ding is nieuw. Nieuw plus onbepaald betekent hay plus un of una.",'''

NIEUW = '''  ''' + MARK + '''
  const woorden = es.replace(".","").split(" ");
  const andere  = nieuw ? "está" : "hay";
  return {type:"build",
    prompt:L("Bouw de Spaanse zin. Tik de woorden aan in de goede volgorde.",
             "Build the Spanish sentence. Tap the words in the right order."),
    sentence:nl, showEs:es, pool:R.shuffle(woorden.concat([andere])),
    answer:woorden.join(" "), accept:[woorden.join(" "), es], word:w.key,
    why:nieuw
      ? L("Je zegt er is een, dus het ding is nieuw. Nieuw plus onbepaald betekent hay plus un of una.",'''


def patch_html(p):
    s = p.read_text(encoding="utf-8")
    if MARK in s:
        return "index.html  al gepatcht"
    n = s.count(OUD)
    if n == 0:
        raise SystemExit("FOUT: hay/nl2es niet gevonden -- de code is van vorm veranderd")
    if n > 1:
        raise SystemExit("FOUT: hay/nl2es %d keer gevonden, te onduidelijk om te patchen" % n)
    p.write_text(s.replace(OUD, NIEUW, 1), encoding="utf-8")
    return "index.html  gepatcht"


def main():
    if len(sys.argv) < 2:
        raise SystemExit("gebruik: 03-hay-zin-bouwen.py <repo-map>")
    f = pathlib.Path(sys.argv[1]) / "index.html"
    if not f.is_file():
        raise SystemExit("FOUT: index.html ontbreekt")
    print("   " + patch_html(f))


main()
