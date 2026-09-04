#!/usr/bin/env python3
"""
Hele zinnen intypen wordt hele zinnen bouwen.

Een beginner die een Spaanse zin uit het niets moet opschrijven doet drie dingen
tegelijk: de zin bedenken, de woorden kennen en ze goed spellen. Te veel ineens.

Twee ingrepen, samen een verhaal:

  1. De tegel "Hay en esta" had een typ-oefening waar de andere drie meerkeuze
     waren. Die wordt een bouwoefening, met de andere vorm (hay tegenover esta)
     als extra keuze in de bak, zodat je nog steeds moet kiezen.
  2. Een haak in ex(), de fabriek waar elke oefening doorheen komt: elke
     typ-oefening met een antwoord van drie woorden of meer wordt een
     bouwoefening. Antwoorden van een of twee woorden blijven typen -- dat is
     een vorm invullen, geen zin schrijven.

De nakijklogica blijft ongemoeid: grade() behandelt input en build al identiek,
en sameLoose() negeert leestekens, hoofdletters en accenten.

Gebruik: 03-zinnen-bouwen.py <repo-map>
"""
import _lib

MERK_HAY = '/* PATCH: hay als bouwoefening */'

HAY = [
    ('  return {type:"input", prompt:L("Vertaal naar het Spaans.","Translate into Spanish."),\n    sentence:nl, showEs:es, answer:es, accept:[es, es.replace(".","")], word:w.key,\n    why:nieuw\n      ? L("Je zegt er is een, dus het ding is nieuw. Nieuw plus onbepaald betekent hay plus un of una.",',
     '  /* PATCH: hay als bouwoefening */\n  const woorden = es.replace(".","").split(" ");\n  const andere  = nieuw ? "está" : "hay";\n  return {type:"build",\n    prompt:L("Bouw de Spaanse zin. Tik de woorden aan in de goede volgorde.",\n             "Build the Spanish sentence. Tap the words in the right order."),\n    sentence:nl, showEs:es, pool:R.shuffle(woorden.concat([andere])),\n    answer:woorden.join(" "), accept:[woorden.join(" "), es], word:w.key,\n    why:nieuw\n      ? L("Je zegt er is een, dus het ding is nieuw. Nieuw plus onbepaald betekent hay plus un of una.",',
     'hay/nl2es'),
]

MERK_ALGEMEEN = '/* PATCH: zinnen bouwen in plaats van typen */'

ALGEMEEN = [
    ('function ex(o){\n  if(!o.kind) o.kind = ({mc:"Meerkeuze",input:"Vul in",build:"Zin bouwen",order:"Zet in de juiste orde",',
     'function ex(o){\n  /* PATCH: zinnen bouwen in plaats van typen */\n  if(o.type==="input" && typeof o.answer==="string" && o.answer.indexOf("+") < 0){\n    const woorden = o.answer.replace(/[.,;:\\u00bf?\\u00a1!]/g, " ").split(/\\s+/).filter(Boolean);\n    if(woorden.length >= 3){\n      o.accept = (o.accept || [o.answer]).concat([woorden.join(" "), o.answer]);\n      o.pool = R.shuffle(woorden.slice());\n      o.type = "build";\n    }\n  }\n  if(!o.kind) o.kind = ({mc:"Meerkeuze",input:"Vul in",build:"Zin bouwen",order:"Zet in de juiste orde",',
     'ex()'),
]

def wijzig_hay(t):
    for oud, nieuw, wat in HAY:
        t = _lib.eenmalig(t, oud, nieuw, wat)
    return t


def wijzig_algemeen(t):
    for oud, nieuw, wat in ALGEMEEN:
        t = _lib.eenmalig(t, oud, nieuw, wat)
    return t


_lib.draai(MERK_HAY, "index.html", wijzig_hay)
_lib.draai(MERK_ALGEMEEN, "index.html", wijzig_algemeen)
