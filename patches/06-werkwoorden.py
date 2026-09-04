#!/usr/bin/env python3
"""
De werkwoordenlijst uitbreiden met de woorden uit de lesstof.

De app kende 41 werkwoorden; in de lesnotities over verbos regulares stonden er
twaalf die er nog niet in zaten. Alle twaalf zijn regelmatig in de tegenwoordige
tijd, dus ze passen zonder uitzonderingen in het bestaande vervoegingssysteem.

Ze worden op drie plekken toegevoegd, zoals de app dat zelf ook doet:
  VERBS    de werkwoorden zelf, met uitspraak in dezelfde notatie
  NLSTEM   de Nederlandse stam, waarmee zinnen gebouwd worden
  EN_VERB  de Engelse betekenis

De Nederlandse vertalingen zijn bewust allemaal verschillend van de bestaande
41. Twee werkwoorden met dezelfde vertaling zou betekenen dat een goed antwoord
fout gerekend kan worden.

Gebruik: 06-werkwoorden.py <repo-map>
"""
import _lib

MERK = '/* PATCH: extra werkwoorden uit de lesstof */'

VERVANGINGEN = [
    ('  {es:"recibir",nl:"ontvangen",g:"ir",pron:"re-thee-BEER"},{es:"decidir",nl:"beslissen",g:"ir",pron:"de-thee-DEER"}\n];',
     '  {es:"recibir",nl:"ontvangen",g:"ir",pron:"re-thee-BEER"},{es:"decidir",nl:"beslissen",g:"ir",pron:"de-thee-DEER"},\n  /* PATCH: extra werkwoorden uit de lesstof */\n  {es:"bajar",nl:"dalen",g:"ar",pron:"ba-CHAR"},{es:"contestar",nl:"beantwoorden",g:"ar",pron:"kon-tes-TAR"},\n  {es:"entrar",nl:"binnenkomen",g:"ar",pron:"en-TRAR"},{es:"practicar",nl:"oefenen",g:"ar",pron:"prak-tee-KAR"},\n  {es:"regresar",nl:"terugkeren",g:"ar",pron:"re-gre-SAR"},\n  {es:"meter",nl:"instoppen",g:"er",pron:"me-TER"},{es:"romper",nl:"breken",g:"er",pron:"rom-PER"},\n  {es:"prender",nl:"aanzetten",g:"er",pron:"pren-DER"},\n  {es:"compartir",nl:"delen",g:"ir",pron:"kom-par-TEER"},{es:"describir",nl:"beschrijven",g:"ir",pron:"des-kree-BEER"},\n  {es:"discutir",nl:"bespreken",g:"ir",pron:"dees-koe-TEER"},{es:"sufrir",nl:"lijden",g:"ir",pron:"soe-FREER"}\n];',
     'de werkwoordenlijst'),
    ('  vivir:"woon", escribir:"schrijf", abrir:"open", subir:"ga omhoog", recibir:"ontvang", decidir:"beslis"\n};',
     '  vivir:"woon", escribir:"schrijf", abrir:"open", subir:"ga omhoog", recibir:"ontvang", decidir:"beslis",\n  /* PATCH: extra werkwoorden uit de lesstof */\n  bajar:"daal", contestar:"beantwoord", entrar:"kom binnen", practicar:"oefen", regresar:"keer terug",\n  meter:"stop in", romper:"breek", prender:"zet aan",\n  compartir:"deel", describir:"beschrijf", discutir:"bespreek", sufrir:"lijd"\n};',
     'de Nederlandse stammen'),
    ('decidir:"to decide"\n};',
     'decidir:"to decide",\nbajar:"to go down", contestar:"to answer", entrar:"to enter", practicar:"to practise",\nregresar:"to return", meter:"to put in", romper:"to break", prender:"to turn on",\ncompartir:"to share", describir:"to describe", discutir:"to discuss", sufrir:"to suffer"\n};',
     'de Engelse betekenissen'),
]

def wijzig(t):
    for oud, nieuw, wat in VERVANGINGEN:
        t = _lib.eenmalig(t, oud, nieuw, wat)
    return t


_lib.draai(MERK, "index.html", wijzig)
