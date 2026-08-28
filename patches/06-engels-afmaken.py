#!/usr/bin/env python3
"""
De Engelse versie afmaken.

Zet je de app op Engels, dan blijven er brokken Nederlands staan: het soortlabel
boven de vraag (MEERKEUZE), de onderwerpnaam, de kopjes in de terugkoppeling en
alle cijfers op het voortgangsscherm.

Bijna alle vertalingen bestonden al in de UI-lijst -- ze werden alleen niet via
T() aangeroepen. Deze patch voegt de paar ontbrekende vertalingen toe en laat de
schermopbouw wel door T() gaan. De onderwerpnaam wordt in een keer opgelost door
.nl op elk onderwerp taalgevoelig te maken, zodat alle ~10 plekken die die naam
tonen vanzelf goed gaan.

Idempotent: al toegepast -> doet niets. Past de code niet -> harde fout.

Gebruik: 06-engels-afmaken.py <repo-map>
"""
import sys, pathlib

MARK = "/* PATCH: Engels afmaken */"

VERVANG = [
    # --- ontbrekende vertalingen toevoegen ---
    ('const UI = {\n',
     'const UI = {\n  ' + MARK + '''
  "Meerkeuze":"Multiple choice", "Vul in":"Fill in", "Zin bouwen":"Build the sentence",
  "Zet in de juiste orde":"Put in the right order", "Luisteren":"Listen",
  "Wat zie je?":"What do you see?", "Woorden koppelen":"Match the words", "Oefening":"Exercise",
  "Waarom jouw antwoord niet kan":"Why your answer does not work",
''', "de UI-lijst"),

    # --- elk cijferblokje op het voortgangsscherm ---
    ('''function stat(n,l){ return '<div class="stat"><div class="stat-n">'+n+'</div><div class="stat-l">'+l+'</div></div>'; }''',
     '''function stat(n,l){ return '<div class="stat"><div class="stat-n">'+n+'</div><div class="stat-l">'+T(l)+'</div></div>'; }''',
     "stat()"),

    # --- het soortlabel boven de vraag ---
    ('''  if(!o.kind) o.kind = ({mc:"Meerkeuze",input:"Vul in",build:"Zin bouwen",order:"Zet in de juiste orde",
    listen:"Luisteren",picture:"Wat zie je?",match:"Woorden koppelen"})[o.type] || "Oefening";''',
     '''  if(!o.kind) o.kind = T(({mc:"Meerkeuze",input:"Vul in",build:"Zin bouwen",order:"Zet in de juiste orde",
    listen:"Luisteren",picture:"Wat zie je?",match:"Woorden koppelen"})[o.type] || "Oefening");''',
     "het soortlabel in ex()"),

    # --- onderwerpnamen: .nl volgt nu de gekozen taal ---
    ('const TOPIC = {}; TOPICS.forEach((t,i)=>{ TOPIC[t.id]=t; t.n=i; });',
     'const TOPIC = {}; TOPICS.forEach((t,i)=>{ TOPIC[t.id]=t; t.n=i; });\n' + MARK + '''
TOPICS.forEach(t => { let vast = t.nl; Object.defineProperty(t, "nl", {
  get(){ return (LANG === "en" && typeof EN_TOPIC !== "undefined" && EN_TOPIC[t.id]) ? EN_TOPIC[t.id] : vast; },
  set(v){ vast = v; }, configurable: true }); });''',
     "de onderwerpenlijst"),

    # --- kopjes in de terugkoppeling ---
    ('''<div class="fb-lab">Het juiste antwoord</div>''',
     '''<div class="fb-lab">'+T("Het juiste antwoord")+'</div>''', "kopje juiste antwoord"),
    ('''<div class="fb-lab">Waarom jouw antwoord niet kan</div>''',
     '''<div class="fb-lab">'+T("Waarom jouw antwoord niet kan")+'</div>''', "kopje foute antwoord"),
    ('''<div class="fb-lab">Onthoud</div>''',
     '''<div class="fb-lab">'+T("Onthoud")+'</div>''', "kopje Onthoud"),

    # --- losse zinnen die nog Nederlands bleven ---
    ('''<div class="fb-blk"><div class="fb-txt tiny">Je krijgt nu '+res.extra+' extra oefeningen over precies deze regel. '
      + 'Drie keer goed op rij en we gaan verder.</div></div>';''',
     '''<div class="fb-blk"><div class="fb-txt tiny">'
      + L("Je krijgt nu "+res.extra+" extra oefeningen over precies deze regel. Drie keer goed op rij en we gaan verder.",
          "You now get "+res.extra+" extra exercises on this exact rule. Three in a row correct and we move on.")
      + '</div></div>';''', "extra-oefeningen-zin"),
    ('''<div class="fb-blk"><div class="fb-txt tiny">Goed op rij: '+res.streakOnRule+' van 3.</div></div>';''',
     '''<div class="fb-blk"><div class="fb-txt tiny">'
      + L("Goed op rij: "+res.streakOnRule+" van 3.", "Correct in a row: "+res.streakOnRule+" of 3.")
      + '</div></div>';''', "goed-op-rij-zin"),
    ('''<p class="tiny dim">Zoek de paren: Spaans woord bij Nederlandse betekenis.</p>''',
     '''<p class="tiny dim">'+T("Zoek de paren: Spaans woord bij Nederlandse betekenis.")+'</p>''', "uitleg bij het paarspel"),
    ('''<p class="tiny dim" style="margin-bottom:14px">Deze onderwerpen komen extra vaak terug in de herhaling.</p>''',
     '''<p class="tiny dim" style="margin-bottom:14px">'+T("Deze onderwerpen komen extra vaak terug in de herhaling.")+'</p>''',
     "uitleg bij zwakke onderwerpen"),
    ('''<h3 class="h-lg">Voortgang bewaren</h3>''',
     '''<h3 class="h-lg">'+T("Voortgang bewaren")+'</h3>''', "kopje voortgang bewaren"),
    (''': "Oefen eerst wat, dan verschijnen ze hier")''',
     ''': T("Oefen eerst wat, dan verschijnen ze hier"))''', "tekst bij nog geen zwakke onderwerpen"),
    ('''let title = "Klaar", sub = "";''',
     '''let title = T("Klaar"), sub = "";''', "resultaattitel"),
    ('''title = pct>=80 ? "Geslaagd!" : "Nog niet";''',
     '''title = pct>=80 ? T("Geslaagd!") : T("Nog niet");''', "toetsuitslag"),
]


def main():
    if len(sys.argv) < 2:
        raise SystemExit("gebruik: 06-engels-afmaken.py <repo-map>")
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
    # aria-label komt twee keer voor, allebei vervangen
    s = s.replace('aria-label="Stoppen"', '''aria-label="'+T("Stoppen")+'"''')
    f.write_text(s, encoding="utf-8")
    print("   index.html  gepatcht (%d plekken + aria-labels)" % len(VERVANG))


main()
