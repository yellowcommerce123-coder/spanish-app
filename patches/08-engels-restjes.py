#!/usr/bin/env python3
"""
De laatste Nederlandse restjes in de Engelse versie.

Na patch 06 bleven er drie plekken over die niet door T() liepen: het kopje
"Voortgang / Niveau" boven het voortgangsscherm, en het label "meervoud:" op de
woordkaart en in de flitskaarten. De vertalingen bestonden al, op
"beschrijvend woord" na; die wordt hier toegevoegd.

Idempotent: al toegepast -> doet niets. Past de code niet -> harde fout.

Gebruik: 08-engels-restjes.py <repo-map>
"""
import sys, pathlib

MARK = "/* PATCH: laatste Engelse restjes */"

VERVANG = [
    ('"Waarom jouw antwoord niet kan":"Why your answer does not work",',
     '"Waarom jouw antwoord niet kan":"Why your answer does not work",\n  '
     + MARK + ' "beschrijvend woord":"describing word",',
     "de UI-lijst"),
    ('''<div class="eyebrow">Voortgang</div><h1 class="h-xl">Niveau '+levelOf(S.xp)+'</h1>''',
     '''<div class="eyebrow">'+T("Voortgang")+'</div><h1 class="h-xl">'+T("Niveau")+' '+levelOf(S.xp)+'</h1>''',
     "kopje op het voortgangsscherm"),
    ('''      note:w.art ? "meervoud: "+w.pl : "beschrijvend woord"''',
     '''      note:w.art ? T("meervoud")+": "+w.pl : T("beschrijvend woord")''',
     "notitie op de woordkaart"),
    ('''<div class="tiny dim" style="margin-top:10px">meervoud: '+w.pl+'</div>''',
     '''<div class="tiny dim" style="margin-top:10px">'+T("meervoud")+': '+w.pl+'</div>''',
     "meervoud op de flitskaart"),
]


def main():
    if len(sys.argv) < 2:
        raise SystemExit("gebruik: 08-engels-restjes.py <repo-map>")
    f = pathlib.Path(sys.argv[1]) / "index.html"
    if not f.is_file():
        raise SystemExit("FOUT: index.html ontbreekt")
    s = f.read_text(encoding="utf-8")
    if MARK in s:
        print("   index.html  al gepatcht")
        return
    for oud, nieuw, wat in VERVANG:
        n = s.count(oud)
        if n != 1:
            raise SystemExit("FOUT: %s %d keer gevonden -- de code is van vorm veranderd" % (wat, n))
        s = s.replace(oud, nieuw, 1)
    f.write_text(s, encoding="utf-8")
    print("   index.html  gepatcht (%d plekken)" % len(VERVANG))


main()
