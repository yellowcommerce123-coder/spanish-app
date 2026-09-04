#!/usr/bin/env python3
"""
De werkwoordenlijst uitbreiden met de ontbrekende woorden uit de lesstof.

De app kende 41 werkwoorden; in de lesnotities over verbos regulares stonden er
twaalf die er nog niet in zaten. Alle twaalf zijn regelmatig in de tegenwoordige
tijd, dus ze passen zonder meer in het bestaande vervoegingssysteem.

Ze worden op drie plekken toegevoegd, zoals de app dat zelf ook doet:
  VERBS    de werkwoorden zelf, met uitspraak in dezelfde notatie
  NLSTEM   de Nederlandse stam, gebruikt om zinnen mee te bouwen
  EN_VERB  de Engelse betekenis

De Nederlandse vertalingen zijn bewust allemaal verschillend van de bestaande
41, want twee werkwoorden met dezelfde vertaling zouden betekenen dat een goed
antwoord fout gerekend kan worden.

Idempotent: al toegepast -> doet niets. Past de code niet -> harde fout.

Gebruik: 09-werkwoorden-uitbreiden.py <repo-map>
"""
import sys, pathlib

MARK = "/* PATCH: extra werkwoorden uit de lesstof */"

OUD_VERBS = '''  {es:"recibir",nl:"ontvangen",g:"ir",pron:"re-thee-BEER"},{es:"decidir",nl:"beslissen",g:"ir",pron:"de-thee-DEER"}
];'''
NIEUW_VERBS = '''  {es:"recibir",nl:"ontvangen",g:"ir",pron:"re-thee-BEER"},{es:"decidir",nl:"beslissen",g:"ir",pron:"de-thee-DEER"},
  ''' + MARK + '''
  {es:"bajar",nl:"dalen",g:"ar",pron:"ba-CHAR"},{es:"contestar",nl:"beantwoorden",g:"ar",pron:"kon-tes-TAR"},
  {es:"entrar",nl:"binnenkomen",g:"ar",pron:"en-TRAR"},{es:"practicar",nl:"oefenen",g:"ar",pron:"prak-tee-KAR"},
  {es:"regresar",nl:"terugkeren",g:"ar",pron:"re-gre-SAR"},
  {es:"meter",nl:"instoppen",g:"er",pron:"me-TER"},{es:"romper",nl:"breken",g:"er",pron:"rom-PER"},
  {es:"prender",nl:"aanzetten",g:"er",pron:"pren-DER"},
  {es:"compartir",nl:"delen",g:"ir",pron:"kom-par-TEER"},{es:"describir",nl:"beschrijven",g:"ir",pron:"des-kree-BEER"},
  {es:"discutir",nl:"bespreken",g:"ir",pron:"dees-koe-TEER"},{es:"sufrir",nl:"lijden",g:"ir",pron:"soe-FREER"}
];'''

OUD_NLSTEM = '''  vivir:"woon", escribir:"schrijf", abrir:"open", subir:"ga omhoog", recibir:"ontvang", decidir:"beslis"
};'''
NIEUW_NLSTEM = '''  vivir:"woon", escribir:"schrijf", abrir:"open", subir:"ga omhoog", recibir:"ontvang", decidir:"beslis",
  ''' + MARK + '''
  bajar:"daal", contestar:"beantwoord", entrar:"kom binnen", practicar:"oefen", regresar:"keer terug",
  meter:"stop in", romper:"breek", prender:"zet aan",
  compartir:"deel", describir:"beschrijf", discutir:"bespreek", sufrir:"lijd"
};'''

OUD_EN = '''decidir:"to decide"
};'''
NIEUW_EN = '''decidir:"to decide",
bajar:"to go down", contestar:"to answer", entrar:"to enter", practicar:"to practise",
regresar:"to return", meter:"to put in", romper:"to break", prender:"to turn on",
compartir:"to share", describir:"to describe", discutir:"to discuss", sufrir:"to suffer"
};'''


def sub1(s, oud, nieuw, wat):
    n = s.count(oud)
    if n != 1:
        raise SystemExit("FOUT: %s %d keer gevonden -- de code is van vorm veranderd" % (wat, n))
    return s.replace(oud, nieuw, 1)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("gebruik: 09-werkwoorden-uitbreiden.py <repo-map>")
    f = pathlib.Path(sys.argv[1]) / "index.html"
    if not f.is_file():
        raise SystemExit("FOUT: index.html ontbreekt")
    s = f.read_text(encoding="utf-8")
    if MARK in s:
        print("   index.html  al gepatcht")
        return
    s = sub1(s, OUD_VERBS, NIEUW_VERBS, "de werkwoordenlijst")
    s = sub1(s, OUD_NLSTEM, NIEUW_NLSTEM, "de Nederlandse stammen")
    s = sub1(s, OUD_EN, NIEUW_EN, "de Engelse betekenissen")
    f.write_text(s, encoding="utf-8")
    print("   index.html  gepatcht (12 werkwoorden toegevoegd)")


main()
