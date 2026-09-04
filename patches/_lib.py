"""
Gedeelde hulp voor de patches.

Elke patch is een script dat de app-bestanden uit de zip aanpast. Ze delen
allemaal dezelfde drie eisen:

  idempotent   twee keer draaien mag niets kapotmaken
  eenduidig    een anker dat vaker of helemaal niet voorkomt is geen anker
  luidruchtig  past iets niet, dan stoppen -- de deploy breekt liever af dan
               dat er stilletjes een aanpassing verdwijnt

Die drie zitten hier, zodat een patch alleen nog hoeft te beschrijven wát hij
verandert.
"""
import sys
import pathlib


class PatchFout(SystemExit):
    pass


def eenmalig(tekst, oud, nieuw, wat):
    """Vervang oud door nieuw, en eis dat oud precies een keer voorkomt."""
    n = tekst.count(oud)
    if n != 1:
        raise PatchFout(
            "FOUT: %s %d keer gevonden in plaats van 1 -- de code is van vorm veranderd" % (wat, n)
        )
    return tekst.replace(oud, nieuw, 1)


def overal(tekst, oud, nieuw, wat):
    """Vervang alle voorkomens, maar eis dat het er minstens een is."""
    n = tekst.count(oud)
    if n == 0:
        raise PatchFout("FOUT: %s helemaal niet gevonden -- de code is van vorm veranderd" % wat)
    return tekst.replace(oud, nieuw)


def draai(merk, bestand, wijzig, naam=None):
    """
    Voer een patch uit op <repo-map>/<bestand>.

    merk    tekst die na afloop in het bestand staat; is die er al, dan doet
            de patch niets meer
    wijzig  functie die de inhoud krijgt en de nieuwe inhoud teruggeeft
    """
    if len(sys.argv) < 2:
        raise PatchFout("gebruik: %s <repo-map>" % (naam or sys.argv[0]))
    pad = pathlib.Path(sys.argv[1]) / bestand
    if not pad.is_file():
        raise PatchFout("FOUT: %s ontbreekt in %s" % (bestand, sys.argv[1]))

    inhoud = pad.read_text(encoding="utf-8")
    if merk in inhoud:
        print("   %-18s al gepatcht" % bestand)
        return

    nieuw = wijzig(inhoud)
    if merk not in nieuw:
        raise PatchFout("FOUT: %s zette zijn eigen merkteken niet -- patch klopt niet" % bestand)

    pad.write_text(nieuw, encoding="utf-8")
    print("   %-18s gepatcht" % bestand)
