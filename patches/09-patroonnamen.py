#!/usr/bin/env python3
"""
Patroonnamen die als [object Object] in beeld kwamen.

In de BUILD-gegevens is een patroonnaam tweetalig opgeslagen: {nl:..., en:...}.
Er bestaat een helper patName() die daar de juiste taal uit haalt, en vier
plekken gebruiken die netjes. Twee plekken niet, en die zetten het object
rechtstreeks in de HTML:

  - de sectiekoppen op de vijf bouwlessen -- twintig koppen die allemaal
    letterlijk "[object Object]" toonden
  - de regelnaam in de luisteroefening van diezelfde vijf tegels, die
    bovendien het Nederlandse "Patroon: " ook in de Engelse versie liet staan

Meegenomen: het kopje "Kies een blokje" liep niet door de vertaling, en
entender had dezelfde Nederlandse vertaling als comprender.

Gebruik: 09-patroonnamen.py <repo-map>
"""
import _lib

MERK = '/* PATCH: patroonnamen en losse Nederlandse resten */'

VERVANGINGEN = [
    ('      ruleName:"Patroon: "+pat.name,',
     '      /* PATCH: patroonnamen en losse Nederlandse resten */\n      ruleName:L("Patroon: ","Pattern: ")+patName(pat),',
     'de regelnaam in de luisteroefening'),
    ('<h3 class="h-lg">\'+pat.name+\'</h3>',
     '<h3 class="h-lg">\'+patName(pat)+\'</h3>',
     'de sectiekop op de bouwlessen'),
    ('>Kies een blokje</div>',
     '>\'+L("Kies een blokje","Pick a block")+\'</div>',
     'het kopje boven de blokjes'),
    ('{es:"entender",nl:"begrijpen",en:"to understand"',
     '{es:"entender",nl:"snappen",en:"to understand"',
     'de vertaling van entender'),
]


def wijzig(t):
    for oud, nieuw, wat in VERVANGINGEN:
        t = _lib.eenmalig(t, oud, nieuw, wat)
    return t


_lib.draai(MERK, "index.html", wijzig)
