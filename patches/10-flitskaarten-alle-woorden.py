#!/usr/bin/env python3
"""
Flitskaarten met alle woorden, als echte oefening.

Wat er was: een enkele willekeurige kaart uit VOCAB met een knop "Nieuw woord".
Geen stapel, geen voortgang, geen idee wat je al gehad hebt -- en de 53
werkwoorden zaten er niet in.

Wat het wordt: een geschudde stapel van alle 278 kaarten (225 woorden + 53
werkwoorden). Teller erboven, kaart omdraaien door erop te tikken, en daarna
zeg je zelf of je het wist. Wat je niet wist komt aan het eind terug, zodat je
een ronde kunt afsluiten met precies de kaarten die je nog niet beheerst.

Meteen meegenomen: de achterkant toonde altijd de Nederlandse betekenis, ook in
de Engelse versie, en "Tik om om te draaien" liep niet door T().

Idempotent: al toegepast -> doet niets. Past de code niet -> harde fout.

Gebruik: 10-flitskaarten-alle-woorden.py <repo-map>
"""
import sys, pathlib

MARK = "/* PATCH: flitskaarten met alle woorden */"

OUD_VAR = "let FLASH = null, MEM = null;"
NIEUW_VAR = "let FLASH = null, MEM = null, FDECK = null;"

OUD_KNOP = '''  h += '<div class="card pad stack-14"><div class="row"><div class="h-lg">Flashkaarten</div><div class="spacer"></div>'
    + '<button class="btn btn-sm" data-flash="new">Nieuw woord</button></div><div id="flashbox"></div></div>';'''
NIEUW_KNOP = '''  h += '<div class="card pad stack-14"><div class="row"><div class="h-lg">'+L("Flitskaarten","Flashcards")+'</div><div class="spacer"></div>'
    + '<button class="btn btn-sm" data-flash="new">'+L("Nieuwe ronde","New round")+'</button></div><div id="flashbox"></div></div>';'''

OUD_FN = '''function newFlash(){
  const w = R.pick(VOCAB);
  FLASH = w;
  $("#flashbox").innerHTML = '<div class="flash" id="flash"><div class="flash-in">'
    + '<div class="flash-face"><div><div class="ves" style="font-size:30px">'+(w.art?'<span class="art">'+w.art+'</span> ':'')+w.es+'</div>'
    + '<div class="vpron" style="margin-top:6px">'+w.pron+'</div>'
    + '<div class="tiny dim" style="margin-top:14px">Tik om om te draaien</div></div></div>'
    + '<div class="flash-face flash-back"><div>'+(w.emoji?'<div style="font-size:40px">'+w.emoji+'</div>':'')
    + '<div class="vnl" style="font-size:24px">'+w.nl+'</div>'
    + '<div class="tiny dim" style="margin-top:10px">'+T("meervoud")+': '+w.pl+'</div></div></div>'
    + '</div></div>';
}'''

NIEUW_FN = MARK + '''
/* de hele woordenschat als stapel: zelfstandige naamwoorden, bijvoeglijke
   naamwoorden en werkwoorden, geschud */
function flashStapel(){
  const uitWoorden = VOCAB.map(w => ({
    voor: (w.art ? '<span class="art">'+w.art+'</span> ' : '') + w.es,
    pron: w.pron || pronOf(w.es),
    emoji: w.emoji || "",
    achter: betekenis(w),
    extra: w.isAdj ? L("beschrijvend woord","describing word") : T("meervoud")+": "+w.pl
  }));
  const uitWerkwoorden = VERBS.map(v => ({
    voor: v.es,
    pron: v.pron || pronOf(v.es),
    emoji: "",
    achter: verbBetekenis(v),
    extra: L("werkwoord op -"+v.g, "verb ending in -"+v.g)
  }));
  return R.shuffle(uitWoorden.concat(uitWerkwoorden));
}

function newFlash(){
  FDECK = {kaarten: flashStapel(), i: 0, nogeens: [], goed: 0};
  paintFlash();
}

function paintFlash(){
  const box = $("#flashbox"); if(!box || !FDECK) return;
  const d = FDECK;

  if(d.i >= d.kaarten.length){
    const totaal = d.goed + d.nogeens.length;
    box.innerHTML = '<div class="note"><p class="prose">'
      + L("Ronde klaar. Je kende "+d.goed+" van de "+totaal+" kaarten.",
          "Round finished. You knew "+d.goed+" out of "+totaal+" cards.")
      + '</p></div><div class="row" style="gap:8px;flex-wrap:wrap;margin-top:12px">'
      + (d.nogeens.length
          ? '<button class="btn btn-primary btn-sm" data-flash="herhaal">'
            + L("De "+d.nogeens.length+" moeilijke nog eens", "Redo the "+d.nogeens.length+" hard ones")+'</button>'
          : '')
      + '<button class="btn btn-ghost btn-sm" data-flash="new">'+L("Opnieuw met alles","Start over with all")+'</button></div>';
    return;
  }

  const k = d.kaarten[d.i];
  box.innerHTML = '<div class="tiny dim" style="margin-bottom:8px">'+(d.i+1)+' / '+d.kaarten.length+'</div>'
    + '<div class="flash" id="flash"><div class="flash-in">'
    + '<div class="flash-face"><div><div class="ves" style="font-size:30px">'+k.voor+'</div>'
    + '<div class="vpron" style="margin-top:6px">'+k.pron+'</div>'
    + '<div class="tiny dim" style="margin-top:14px">'+T("Tik om om te draaien")+'</div></div></div>'
    + '<div class="flash-face flash-back"><div>'+(k.emoji?'<div style="font-size:40px">'+k.emoji+'</div>':'')
    + '<div class="vnl" style="font-size:24px">'+k.achter+'</div>'
    + '<div class="tiny dim" style="margin-top:10px">'+k.extra+'</div></div></div>'
    + '</div>'
    + '<div class="row" style="gap:8px;margin-top:12px">'
    + '<button class="btn btn-primary btn-sm" data-flash="ken">'+L("Ken ik","I knew it")+'</button>'
    + '<button class="btn btn-ghost btn-sm" data-flash="nog">'+L("Nog niet","Not yet")+'</button></div>';
}'''

OUD_KLIK = '''  if(d.flash==="new"){ newFlash(); return; }
  if(t.id==="flash"){ t.classList.toggle("flipped"); return; }'''
NIEUW_KLIK = '''  if(d.flash==="new"){ newFlash(); return; }
  ''' + MARK + '''
  if(d.flash==="ken" && FDECK){ FDECK.goed++; FDECK.i++; paintFlash(); return; }
  if(d.flash==="nog" && FDECK){ FDECK.nogeens.push(FDECK.kaarten[FDECK.i]); FDECK.i++; paintFlash(); return; }
  if(d.flash==="herhaal" && FDECK){ FDECK = {kaarten:R.shuffle(FDECK.nogeens), i:0, nogeens:[], goed:0}; paintFlash(); return; }
  if(t.id==="flash"){ t.classList.toggle("flipped"); return; }'''


def sub1(s, oud, nieuw, wat):
    n = s.count(oud)
    if n != 1:
        raise SystemExit("FOUT: %s %d keer gevonden -- de code is van vorm veranderd" % (wat, n))
    return s.replace(oud, nieuw, 1)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("gebruik: 10-flitskaarten-alle-woorden.py <repo-map>")
    f = pathlib.Path(sys.argv[1]) / "index.html"
    if not f.is_file():
        raise SystemExit("FOUT: index.html ontbreekt")
    s = f.read_text(encoding="utf-8")
    if MARK in s:
        print("   index.html  al gepatcht")
        return
    s = sub1(s, OUD_VAR,  NIEUW_VAR,  "de variabelen van het spelscherm")
    s = sub1(s, OUD_KNOP, NIEUW_KNOP, "de kop boven de flitskaarten")
    s = sub1(s, OUD_FN,   NIEUW_FN,   "newFlash()")
    s = sub1(s, OUD_KLIK, NIEUW_KLIK, "de klikafhandeling")
    f.write_text(s, encoding="utf-8")
    print("   index.html  gepatcht")


main()
