#!/usr/bin/env python3
"""
De Engelse versie afmaken.

Zet je de app op Engels, dan bleven er brokken Nederlands staan: het soortlabel
boven de vraag (MEERKEUZE), de onderwerpnaam, de kopjes in de terugkoppeling en
alle cijfers op het voortgangsscherm.

De diagnose was aardiger dan het probleem: bijna alle vertalingen bestonden al in
de UI-lijst van de app -- ze werden alleen niet via T() aangeroepen. Iemand heeft
het woordenboek gevuld en de aanroepen vergeten. Deze patch voegt de paar
ontbrekende vertalingen toe en zet de aanroepen recht.

Een ingreep lost er in een keer tien op: .nl op elk onderwerp wordt taalgevoelig,
waardoor alle plekken die zo'n naam tonen vanzelf goed gaan.

Gebruik: 05-engels.py <repo-map>
"""
import _lib

MERK_HOOFD = '/* PATCH: Engels afmaken */'

HOOFD = [
    ('const UI = {\n',
     'const UI = {\n  /* PATCH: Engels afmaken */\n  "Meerkeuze":"Multiple choice", "Vul in":"Fill in", "Zin bouwen":"Build the sentence",\n  "Zet in de juiste orde":"Put in the right order", "Luisteren":"Listen",\n  "Wat zie je?":"What do you see?", "Woorden koppelen":"Match the words", "Oefening":"Exercise",\n  "Waarom jouw antwoord niet kan":"Why your answer does not work",\n',
     'de UI-lijst'),
    ('function stat(n,l){ return \'<div class="stat"><div class="stat-n">\'+n+\'</div><div class="stat-l">\'+l+\'</div></div>\'; }',
     'function stat(n,l){ return \'<div class="stat"><div class="stat-n">\'+n+\'</div><div class="stat-l">\'+T(l)+\'</div></div>\'; }',
     'stat()'),
    ('  if(!o.kind) o.kind = ({mc:"Meerkeuze",input:"Vul in",build:"Zin bouwen",order:"Zet in de juiste orde",\n    listen:"Luisteren",picture:"Wat zie je?",match:"Woorden koppelen"})[o.type] || "Oefening";',
     '  if(!o.kind) o.kind = T(({mc:"Meerkeuze",input:"Vul in",build:"Zin bouwen",order:"Zet in de juiste orde",\n    listen:"Luisteren",picture:"Wat zie je?",match:"Woorden koppelen"})[o.type] || "Oefening");',
     'het soortlabel in ex()'),
    ('const TOPIC = {}; TOPICS.forEach((t,i)=>{ TOPIC[t.id]=t; t.n=i; });',
     'const TOPIC = {}; TOPICS.forEach((t,i)=>{ TOPIC[t.id]=t; t.n=i; });\n/* PATCH: Engels afmaken */\nTOPICS.forEach(t => { let vast = t.nl; Object.defineProperty(t, "nl", {\n  get(){ return (LANG === "en" && typeof EN_TOPIC !== "undefined" && EN_TOPIC[t.id]) ? EN_TOPIC[t.id] : vast; },\n  set(v){ vast = v; }, configurable: true }); });',
     'de onderwerpenlijst'),
    ('<div class="fb-lab">Het juiste antwoord</div>',
     '<div class="fb-lab">\'+T("Het juiste antwoord")+\'</div>',
     'kopje juiste antwoord'),
    ('<div class="fb-lab">Waarom jouw antwoord niet kan</div>',
     '<div class="fb-lab">\'+T("Waarom jouw antwoord niet kan")+\'</div>',
     'kopje foute antwoord'),
    ('<div class="fb-lab">Onthoud</div>',
     '<div class="fb-lab">\'+T("Onthoud")+\'</div>',
     'kopje Onthoud'),
    ('<div class="fb-blk"><div class="fb-txt tiny">Je krijgt nu \'+res.extra+\' extra oefeningen over precies deze regel. \'\n      + \'Drie keer goed op rij en we gaan verder.</div></div>\';',
     '<div class="fb-blk"><div class="fb-txt tiny">\'\n      + L("Je krijgt nu "+res.extra+" extra oefeningen over precies deze regel. Drie keer goed op rij en we gaan verder.",\n          "You now get "+res.extra+" extra exercises on this exact rule. Three in a row correct and we move on.")\n      + \'</div></div>\';',
     'extra-oefeningen-zin'),
    ('<div class="fb-blk"><div class="fb-txt tiny">Goed op rij: \'+res.streakOnRule+\' van 3.</div></div>\';',
     '<div class="fb-blk"><div class="fb-txt tiny">\'\n      + L("Goed op rij: "+res.streakOnRule+" van 3.", "Correct in a row: "+res.streakOnRule+" of 3.")\n      + \'</div></div>\';',
     'goed-op-rij-zin'),
    ('<p class="tiny dim">Zoek de paren: Spaans woord bij Nederlandse betekenis.</p>',
     '<p class="tiny dim">\'+T("Zoek de paren: Spaans woord bij Nederlandse betekenis.")+\'</p>',
     'uitleg bij het paarspel'),
    ('<p class="tiny dim" style="margin-bottom:14px">Deze onderwerpen komen extra vaak terug in de herhaling.</p>',
     '<p class="tiny dim" style="margin-bottom:14px">\'+T("Deze onderwerpen komen extra vaak terug in de herhaling.")+\'</p>',
     'uitleg bij zwakke onderwerpen'),
    ('<h3 class="h-lg">Voortgang bewaren</h3>',
     '<h3 class="h-lg">\'+T("Voortgang bewaren")+\'</h3>',
     'kopje voortgang bewaren'),
    (': "Oefen eerst wat, dan verschijnen ze hier")',
     ': T("Oefen eerst wat, dan verschijnen ze hier"))',
     'tekst bij nog geen zwakke onderwerpen'),
    ('let title = "Klaar", sub = "";',
     'let title = T("Klaar"), sub = "";',
     'resultaattitel'),
    ('title = pct>=80 ? "Geslaagd!" : "Nog niet";',
     'title = pct>=80 ? T("Geslaagd!") : T("Nog niet");',
     'toetsuitslag'),
]

MERK_REST = '/* PATCH: laatste Engelse restjes */'

REST = [
    ('"Waarom jouw antwoord niet kan":"Why your answer does not work",',
     '"Waarom jouw antwoord niet kan":"Why your answer does not work",\n  /* PATCH: laatste Engelse restjes */ "beschrijvend woord":"describing word",',
     'de UI-lijst'),
    ('<div class="eyebrow">Voortgang</div><h1 class="h-xl">Niveau \'+levelOf(S.xp)+\'</h1>',
     '<div class="eyebrow">\'+T("Voortgang")+\'</div><h1 class="h-xl">\'+T("Niveau")+\' \'+levelOf(S.xp)+\'</h1>',
     'kopje op het voortgangsscherm'),
    ('      note:w.art ? "meervoud: "+w.pl : "beschrijvend woord"',
     '      note:w.art ? T("meervoud")+": "+w.pl : T("beschrijvend woord")',
     'notitie op de woordkaart'),
    ('<div class="tiny dim" style="margin-top:10px">meervoud: \'+w.pl+\'</div>',
     '<div class="tiny dim" style="margin-top:10px">\'+T("meervoud")+\': \'+w.pl+\'</div>',
     'meervoud op de flitskaart'),
]

def wijzig_hoofd(t):
    for oud, nieuw, wat in HOOFD:
        t = _lib.eenmalig(t, oud, nieuw, wat)
    # dit label staat op twee plekken
    return _lib.overal(t, 'aria-label="Stoppen"', '''aria-label="'+T("Stoppen")+'"''', "de stopknop")


def wijzig_rest(t):
    for oud, nieuw, wat in REST:
        t = _lib.eenmalig(t, oud, nieuw, wat)
    return t


_lib.draai(MERK_HOOFD, "index.html", wijzig_hoofd)
_lib.draai(MERK_REST, "index.html", wijzig_rest)
