#!/usr/bin/env python3
"""
Waarschuwen voordat iemand zonder account verdergaat.

Zonder account blijft de voortgang in localStorage van dat ene apparaat. Wist
iemand zijn browsergegevens of pakt hij een andere telefoon, dan is alles weg.
Die keuze moet je bewust maken, dus "Verder zonder account" vraagt nu eerst om
een bevestiging in plaats van meteen door te gaan.

Idempotent: al toegepast -> doet niets. Past de code niet -> harde fout.

Gebruik: 02-waarschuwing-zonder-account.py <repo-map>
"""
import sys, pathlib

MARK = "/* PATCH: waarschuwing zonder account */"


def sub(s, old, new, what):
    if old not in s:
        raise SystemExit("FOUT: %s niet gevonden -- de code is van vorm veranderd" % what)
    return s.replace(old, new, 1)


def patch_html(p):
    s = p.read_text(encoding="utf-8")
    if MARK in s:
        return "index.html  al gepatcht"

    # 1. de knop wordt een tweetrapsraket: eerst uitleg, dan pas verder
    s = sub(s,
        """    + '<div class="center"><button class="btn btn-ghost btn-sm" data-skiplogin="1">'+T("Verder zonder account")+'</button>'
    + '<div class="tiny dim" style="margin-top:8px">'+T("Dan blijft je voortgang alleen in deze browser.")+'</div></div>'""",
        """    + '<div class="center">' """ + MARK + """
    + (AUTH.warn
        ? '<div class="note note-granada" style="text-align:left"><p class="prose" style="font-size:15px">'
          + L("Zonder account bewaart de app je voortgang <b>alleen in deze browser, op dit apparaat</b>. "
            + "Wis je je browsergegevens, gebruik je een prive-venster of pak je een andere telefoon of laptop, "
            + "dan is alles weg en begin je opnieuw bij nul. Er is dan geen manier om het terug te halen.",
              "Without an account the app keeps your progress <b>only in this browser, on this device</b>. "
            + "Clear your browsing data, use a private window or switch to another phone or laptop, "
            + "and everything is gone and you start over from zero. There is no way to get it back.")
          + '</p></div>'
          + '<div class="row" style="justify-content:center;gap:8px;flex-wrap:wrap">'
          + '<button class="btn btn-primary btn-sm" data-showlogin="1">'
          + L("Toch een account maken","Create an account after all")+'</button>'
          + '<button class="btn btn-ghost btn-sm" data-skiplogin="ja">'
          + L("Ik begrijp het, ga verder","I understand, continue")+'</button></div>'
        : '<button class="btn btn-ghost btn-sm" data-skiplogin="1">'+T("Verder zonder account")+'</button>'
          + '<div class="tiny dim" style="margin-top:8px">'+T("Dan blijft je voortgang alleen in deze browser.")+'</div>')
    + '</div>'""",
        "skip-knop in renderGate()")

    # 2. eerste klik toont de waarschuwing, tweede klik gaat pas door
    s = sub(s,
        """  if(d.skiplogin){ try{ localStorage.setItem("azulejo:skiplogin","1"); }catch(e){} const g=$("#gate"); if(g) g.remove(); return; }
  if(d.showlogin){ try{ localStorage.removeItem("azulejo:skiplogin"); }catch(e){} renderGate(); return; }""",
        """  if(d.skiplogin){ """ + MARK + """
    if(d.skiplogin !== "ja"){ AUTH.warn = true; renderGate(); return; }
    try{ localStorage.setItem("azulejo:skiplogin","1"); }catch(e){}
    AUTH.warn = false;
    const g=$("#gate"); if(g) g.remove(); return;
  }
  if(d.showlogin){ AUTH.warn = false; try{ localStorage.removeItem("azulejo:skiplogin"); }catch(e){} renderGate(); return; }""",
        "skiplogin-afhandeling")

    p.write_text(s, encoding="utf-8")
    return "index.html  gepatcht"


def main():
    if len(sys.argv) < 2:
        raise SystemExit("gebruik: 02-waarschuwing-zonder-account.py <repo-map>")
    root = pathlib.Path(sys.argv[1])
    f = root / "index.html"
    if not f.is_file():
        raise SystemExit("FOUT: index.html ontbreekt in %s" % root)
    print("   " + patch_html(f))


main()
