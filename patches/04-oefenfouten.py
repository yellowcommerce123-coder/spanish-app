#!/usr/bin/env python3
"""
Twee oefeningen die zichzelf beantwoordden.

Allebei bouwen ze een fout antwoord door een letter aan het woord te plakken, en
allebei komt daar soms precies het goede antwoord uit. ex() gooit dubbele opties
weg, dus bleef er een enkele knop over met het juiste antwoord erop: een gratis
punt en een scherm dat er kapot uitziet.

  adjectives/onveranderlijk  bij woorden op -e: fuerte + s = fuertes
  plural/keuze               de klinkertest /[aeiou]$/ kende geen accenten,
                             dus bebe, sofa, cafe en te belandden in de
                             medeklinker-tak en kregen -s -- het goede meervoud

Bij allebei ligt er nu een vangnet onder: is de afleider gelijk aan het
antwoord, dan wordt er een andere gekozen.

Gebruik: 04-oefenfouten.py <repo-map>
"""
import _lib

MERK_ADJ = '/* PATCH: afleider mag niet gelijk zijn aan het antwoord */'

ADJ = [
    ('  const bad = plural ? a.es+"s" : (w.g==="f" ? a.es.replace(/.$/,"a") : a.es+"o");',
     '  /* PATCH: afleider mag niet gelijk zijn aan het antwoord */\n  let bad = plural ? a.es+"s" : (w.g==="f" ? a.es.replace(/.$/,"a") : a.es+"o");\n  let badWhy = L("Die vorm bestaat niet.","That form does not exist. Only -o adjectives have four forms.");\n  if(bad === right){\n    bad = a.es;\n    badWhy = L("Dat is de enkelvoudsvorm. Het onderwerp is meervoud, dus er hoort een -s achter: "+right+".",\n               "That is the singular form. The subject is plural, so it needs an -s: "+right+".");\n  }',
     'de afleider in adjectives/onveranderlijk'),
    ('    wrongWhy:{[bad]:L("Die vorm bestaat niet.","That form does not exist. Only -o adjectives have four forms.")},',
     '    wrongWhy:{[bad]:badWhy},',
     'de uitleg bij die afleider'),
]

MERK_MEERVOUD = '/* PATCH: meervoud-afleider mag niet het antwoord zijn */'

MEERVOUD = [
    ('  const bad = w.es.endsWith("z") ? w.es+"es" : (/[aeiou]$/.test(w.es) ? w.es+"es" : w.es+"s");',
     '  /* PATCH: meervoud-afleider mag niet het antwoord zijn */\n  const klinker = /[aeiouáéíóú]$/.test(w.es);\n  let bad = w.es.endsWith("z") ? w.es+"es" : (klinker ? w.es+"es" : w.es+"s");\n  if(bad === w.pl) bad = klinker ? w.es+"s" : w.es+"es";\n  if(bad === w.pl) bad = w.es;',
     'de afleider in plural/keuze'),
]

def wijzig_adj(t):
    for oud, nieuw, wat in ADJ:
        t = _lib.eenmalig(t, oud, nieuw, wat)
    return t


def wijzig_meervoud(t):
    for oud, nieuw, wat in MEERVOUD:
        t = _lib.eenmalig(t, oud, nieuw, wat)
    return t


_lib.draai(MERK_ADJ, "index.html", wijzig_adj)
_lib.draai(MERK_MEERVOUD, "index.html", wijzig_meervoud)
