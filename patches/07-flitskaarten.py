#!/usr/bin/env python3
"""
Flitskaarten met alle woorden, als echte oefening.

Wat er was: een enkele willekeurige kaart uit VOCAB met een knop "Nieuw woord".
Geen stapel, geen voortgang, geen idee wat je al gehad hebt -- en de werkwoorden
zaten er niet in.

Wat het wordt: een geschudde stapel van alle kaarten (woorden + werkwoorden),
met daarboven je score, een voortgangsbalk en het percentage dat je goed had.
Kaart omdraaien door erop te tikken of met Enter, daarna zeg je zelf of je het
wist -- met de muis of met 1 en 2. Wat je niet wist komt aan het eind terug in
een herhaalronde.

Met een knop draai je de richting om: Spaans voor en betekenis achter, of
andersom. Beide kanten oefenen is niet hetzelfde: herkennen kun je al lang
voordat je het zelf kunt oproepen.

Geen klok, bewust. Bij zelf-beoordelen jaagt tijdsdruk je door je eigen twijfel
heen, en dat is net het moment waarop je leert. Voor tijdsdruk is er de tijdrit.

Meteen meegenomen: de achterkant toonde altijd de Nederlandse betekenis, ook in
de Engelse versie, en "Tik om om te draaien" liep niet door T().

Gebruik: 07-flitskaarten.py <repo-map>
"""
import _lib

MERK = '/* PATCH: flitskaarten met alle woorden */'

VERVANGINGEN = [
    ('let FLASH = null, MEM = null;',
     'let FLASH = null, MEM = null, FDECK = null;',
     'de variabelen van het spelscherm'),
    ('  h += \'<div class="card pad stack-14"><div class="row"><div class="h-lg">Flashkaarten</div><div class="spacer"></div>\'\n    + \'<button class="btn btn-sm" data-flash="new">Nieuw woord</button></div><div id="flashbox"></div></div>\';',
     '  h += \'<div class="card pad stack-14"><div class="row"><div class="h-lg">\'+L("Flitskaarten","Flashcards")+\'</div><div class="spacer"></div>\'\n    + \'<button class="btn btn-sm" data-flash="new">\'+L("Nieuwe ronde","New round")+\'</button></div><div id="flashbox"></div></div>\';',
     'de kop boven de flitskaarten'),
    ('function newFlash(){\n  const w = R.pick(VOCAB);\n  FLASH = w;\n  $("#flashbox").innerHTML = \'<div class="flash" id="flash"><div class="flash-in">\'\n    + \'<div class="flash-face"><div><div class="ves" style="font-size:30px">\'+(w.art?\'<span class="art">\'+w.art+\'</span> \':\'\')+w.es+\'</div>\'\n    + \'<div class="vpron" style="margin-top:6px">\'+w.pron+\'</div>\'\n    + \'<div class="tiny dim" style="margin-top:14px">Tik om om te draaien</div></div></div>\'\n    + \'<div class="flash-face flash-back"><div>\'+(w.emoji?\'<div style="font-size:40px">\'+w.emoji+\'</div>\':\'\')\n    + \'<div class="vnl" style="font-size:24px">\'+w.nl+\'</div>\'\n    + \'<div class="tiny dim" style="margin-top:10px">\'+T("meervoud")+\': \'+w.pl+\'</div></div></div>\'\n    + \'</div></div>\';\n}',
     '/* PATCH: flitskaarten met alle woorden */\n/* de hele woordenschat als stapel: zelfstandige naamwoorden, bijvoeglijke\n   naamwoorden en werkwoorden, geschud */\nfunction flashStapel(){\n  const uitWoorden = VOCAB.map(w => ({\n    es: (w.art ? \'<span class="art">\'+w.art+\'</span> \' : \'\') + w.es,\n    pron: w.pron || pronOf(w.es),\n    emoji: w.emoji || "",\n    nl: betekenis(w),\n    extra: w.isAdj ? L("beschrijvend woord","describing word") : T("meervoud")+": "+w.pl\n  }));\n  const uitWerkwoorden = VERBS.map(v => ({\n    es: v.es,\n    pron: v.pron || pronOf(v.es),\n    emoji: "",\n    nl: verbBetekenis(v),\n    extra: L("werkwoord op -"+v.g, "verb ending in -"+v.g)\n  }));\n  return R.shuffle(uitWoorden.concat(uitWerkwoorden));\n}\n\nfunction newFlash(){\n  FDECK = {kaarten: flashStapel(), i:0, nogeens:[], goed:0,\n           richting: (FDECK && FDECK.richting) || "es"};\n  paintFlash();\n}\n\nfunction flashSlot(){\n  const d = FDECK, totaal = d.goed + d.nogeens.length;\n  return \'<div class="note"><p class="prose">\'\n    + L("Ronde klaar. Je kende "+d.goed+" van de "+totaal+" kaarten.",\n        "Round finished. You knew "+d.goed+" out of "+totaal+" cards.")\n    + \'</p></div><div class="row" style="gap:8px;flex-wrap:wrap;margin-top:12px">\'\n    + (d.nogeens.length\n        ? \'<button class="btn btn-primary btn-sm" data-flash="herhaal">\'\n          + L("De "+d.nogeens.length+" moeilijke nog eens",\n              "Redo the "+d.nogeens.length+" hard ones")+\'</button>\'\n        : \'\')\n    + \'<button class="btn btn-ghost btn-sm" data-flash="new">\'\n    + L("Opnieuw met alles","Start over with all")+\'</button></div>\';\n}\n\nfunction paintFlash(){\n  const box = $("#flashbox"); if(!box || !FDECK) return;\n  const d = FDECK;\n  if(d.i >= d.kaarten.length){ box.innerHTML = flashSlot(); return; }\n\n  const k = d.kaarten[d.i];\n  const gehad = d.goed + d.nogeens.length;\n  const pct = gehad ? Math.round(d.goed / gehad * 100) : 0;\n  const naarEs = d.richting === "nl";\n\n  const esKant = \'<div class="ves" style="font-size:30px">\'+k.es+\'</div>\'\n    + \'<div class="vpron" style="margin-top:6px">\'+k.pron+\'</div>\';\n  const nlKant = (k.emoji ? \'<div style="font-size:40px">\'+k.emoji+\'</div>\' : \'\')\n    + \'<div class="vnl" style="font-size:24px">\'+k.nl+\'</div>\';\n\n  box.innerHTML =\n      \'<div class="row" style="gap:10px;align-items:center;margin-bottom:12px">\'\n    +   \'<span class="tag tag-saffron mono">\'+d.goed+\' / \'+gehad+\'</span>\'\n    +   \'<div style="flex:1" class="bar"><div class="bar-fill" style="width:\'\n    +   Math.round(d.i / d.kaarten.length * 100)+\'%"></div></div>\'\n    +   \'<span class="tag tag-saffron mono">\'+pct+\'%</span>\'\n    + \'</div>\'\n    + \'<div class="row" style="margin-bottom:10px">\'\n    +   \'<button class="btn btn-ghost btn-sm" data-flash="richting">\'\n    +   (naarEs ? L("NL → ES","EN → ES") : L("ES → NL","ES → EN"))+\'</button>\'\n    +   \'<div class="spacer"></div>\'\n    +   \'<div class="tiny dim">\'+(d.i+1)+\' / \'+d.kaarten.length+\'</div>\'\n    + \'</div>\'\n    + \'<div class="flash" id="flash"><div class="flash-in">\'\n    +   \'<div class="flash-face"><div>\'+(naarEs ? nlKant : esKant)\n    +     \'<div class="tiny dim" style="margin-top:14px">\'+T("Tik om om te draaien")\n    +     L(" (of Enter)"," (or Enter)")+\'</div></div></div>\'\n    +   \'<div class="flash-face flash-back"><div>\'+(naarEs ? esKant : nlKant)\n    +     \'<div class="tiny dim" style="margin-top:10px">\'+k.extra+\'</div></div></div>\'\n    + \'</div>\'\n    + \'<div class="row" style="gap:8px;margin-top:12px">\'\n    +   \'<button class="btn btn-sm" data-flash="nog" style="background:var(--granada);border-color:var(--granada);color:#fff">\'\n    +   L("Nog niet","Not yet")+\' <span class="tiny" style="opacity:.7">1</span></button>\'\n    +   \'<button class="btn btn-sm" data-flash="ken" style="background:var(--verde);border-color:var(--verde);color:#fff">\'\n    +   L("Ken ik","I knew it")+\' <span class="tiny" style="opacity:.7">2</span></button>\'\n    + \'</div>\';\n}',
     'newFlash()'),
    ('  if(d.flash==="new"){ newFlash(); return; }\n  if(t.id==="flash"){ t.classList.toggle("flipped"); return; }',
     '  if(d.flash==="new"){ newFlash(); return; }\n  /* PATCH: flitskaarten met alle woorden */\n  if(d.flash==="ken" && FDECK){ FDECK.goed++; FDECK.i++; paintFlash(); return; }\n  if(d.flash==="nog" && FDECK){ FDECK.nogeens.push(FDECK.kaarten[FDECK.i]); FDECK.i++; paintFlash(); return; }\n  if(d.flash==="herhaal" && FDECK){ FDECK = {kaarten:R.shuffle(FDECK.nogeens), i:0, nogeens:[], goed:0, richting:FDECK.richting}; paintFlash(); return; }\n  if(d.flash==="richting" && FDECK){ FDECK.richting = FDECK.richting==="es" ? "nl" : "es"; paintFlash(); return; }\n  if(t.id==="flash"){ t.classList.toggle("flipped"); return; }',
     'de klikafhandeling'),
    ('document.addEventListener("keydown", ev => {\n  if(ev.key==="Enter" && DRILL.stage==="run"){',
     'document.addEventListener("keydown", ev => {\n  /* PATCH: flitskaarten met alle woorden */\n  if(CUR==="play" && FDECK && document.getElementById("flash")){\n    if(ev.key==="Enter"){ ev.preventDefault(); document.getElementById("flash").classList.toggle("flipped"); return; }\n    if(ev.key==="1" || ev.key==="2"){\n      ev.preventDefault();\n      const b = document.querySelector(\'[data-flash="\'+(ev.key==="1"?"nog":"ken")+\'"]\');\n      if(b) b.click();\n      return;\n    }\n  }\n  if(ev.key==="Enter" && DRILL.stage==="run"){',
     'de toetsenbordluisteraar'),
]

def wijzig(t):
    for oud, nieuw, wat in VERVANGINGEN:
        t = _lib.eenmalig(t, oud, nieuw, wat)
    return t


_lib.draai(MERK, "index.html", wijzig)
