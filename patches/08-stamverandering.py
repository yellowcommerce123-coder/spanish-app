#!/usr/bin/env python3
"""
Stamveranderende werkwoorden afmaken.

De app kende er negen en gebruikte ze in precies een oefening, die alleen vroeg
of de stam veranderd was. Ze werden nooit vervoegd, en de belangrijkste regel
stond er nergens: de stam verandert in elke vorm behalve bij nosotros en
vosotros -- die houden de oorspronkelijke stam.

Deze patch:
  1. zes e->ie werkwoorden erbij (cerrar, comenzar, preferir, perder, sentir,
     despertar), waarmee de tien uit de lesstof compleet zijn
  2. stamVormen(), dat de zes vormen afleidt uit de yo-vorm en de oude stam
  3. twee oefeningen: welke vorm houdt de stam, en vervoeg er een -- met de
     andere stam als valstrik, want dat is precies de fout die je wilt maken

Gebruik: 08-stamverandering.py <repo-map>
"""
import _lib

MERK = '/* PATCH: stamveranderende werkwoorden compleet */'

VERVANGINGEN = [
    ('  {es:"entender",nl:"begrijpen",en:"to understand",yo:"entiendo",st:"entend",ch:"e wordt ie",chEn:"e becomes ie"}\n];',
     '  {es:"entender",nl:"begrijpen",en:"to understand",yo:"entiendo",st:"entend",ch:"e wordt ie",chEn:"e becomes ie"},\n  /* PATCH: stamveranderende werkwoorden compleet */\n  {es:"cerrar",nl:"sluiten",en:"to close",yo:"cierro",st:"cerr",ch:"e wordt ie",chEn:"e becomes ie"},\n  {es:"comenzar",nl:"starten",en:"to start",yo:"comienzo",st:"comenz",ch:"e wordt ie",chEn:"e becomes ie"},\n  {es:"preferir",nl:"liever hebben",en:"to prefer",yo:"prefiero",st:"prefer",ch:"e wordt ie",chEn:"e becomes ie"},\n  {es:"perder",nl:"verliezen",en:"to lose",yo:"pierdo",st:"perd",ch:"e wordt ie",chEn:"e becomes ie"},\n  {es:"sentir",nl:"voelen",en:"to feel",yo:"siento",st:"sent",ch:"e wordt ie",chEn:"e becomes ie"},\n  {es:"despertar",nl:"wakker maken",en:"to wake up",yo:"despierto",st:"despert",ch:"e wordt ie",chEn:"e becomes ie"}\n];\n\n/* De zes vormen van een stamveranderend werkwoord. De stam verandert overal,\n   behalve bij nosotros en vosotros -- die houden de oorspronkelijke stam. */\nfunction stamVormen(v){\n  const g = v.es.slice(-2), nieuw = v.yo.slice(0,-1);\n  return [0,1,2,3,4,5].map(i => ((i===3 || i===4) ? v.st : nieuw) + ENDINGS[g][i]);\n}\n\nreg("verbstem","uitzondering",()=>{\n  const v = R.pick(STEMCH), vormen = stamVormen(v);\n  const goed = R.chance(.5) ? vormen[3] : vormen[4];\n  const fout = R.pickN([vormen[0], vormen[1], vormen[2], vormen[5]], 3);\n  return {type:"mc",\n    prompt:L("Bij welke vorm blijft de stam ongewijzigd?","Which form keeps the stem unchanged?"),\n    sentence:v.es+" ("+L(v.nl, v.en)+")", showEs:goed,\n    options:[goed].concat(fout), answer:goed,\n    why:L("Bij "+v.es+" verandert de stam in bijna elke vorm: "+v.ch+". Behalve bij <b>nosotros</b> en <b>vosotros</b>. Die houden de oude stam "+v.st+". Dus wel "+vormen[0]+" en "+vormen[5]+", maar niet "+vormen[3]+" en "+vormen[4]+".",\n            "In "+v.es+" the stem changes in nearly every form: "+v.chEn+". Except for <b>nosotros</b> and <b>vosotros</b>, which keep the old stem "+v.st+". So yes to "+vormen[0]+" and "+vormen[5]+", but not "+vormen[3]+" and "+vormen[4]+"."),\n    wrongWhy:{},\n    ruleName:L("Nosotros en vosotros houden de oude stam","Nosotros and vosotros keep the old stem"),\n    mistake:L("De verandering overal doorvoeren, ook bij wij en jullie.",\n              "Applying the change everywhere, including we and you-plural."),\n    trick:L("Teken een schoen om het rijtje. Alles binnen de schoen verandert; wij en jullie vallen erbuiten.",\n            "Draw a boot around the list. Everything inside the boot changes; we and you-plural fall outside it.")};\n});\n\nreg("verbstem","stamvervoegen",()=>{\n  const v = R.pick(STEMCH), vormen = stamVormen(v), i = R.int(6), pr = P6[i];\n  const g = v.es.slice(-2), nieuw = v.yo.slice(0,-1);\n  const houdt = (i === 3 || i === 4);\n  const val = (houdt ? nieuw : v.st) + ENDINGS[g][i];\n  const wrongs = [val, vormen[(i+1)%6], vormen[(i+3)%6]]\n    .filter((x,ix,a) => x !== vormen[i] && a.indexOf(x) === ix);\n  return {type:"mc",\n    prompt:L("Vervoeg "+v.es+" ("+v.nl+") voor "+pr.p+".",\n             "Conjugate "+v.es+" ("+v.en+") for "+pr.p+"."),\n    sentence:cap(pr.p)+" ___ .", showEs:cap(pr.p)+" "+vormen[i]+".",\n    options:[vormen[i]].concat(wrongs.slice(0,3)), answer:vormen[i],\n    why: houdt\n      ? L(pr.p+" is een van de twee uitzonderingen. De stam blijft gewoon "+v.st+", dus "+vormen[i]+".",\n          pr.p+" is one of the two exceptions. The stem simply stays "+v.st+", so "+vormen[i]+".")\n      : L("Bij "+pr.p+" verandert de stam: "+v.ch+". Dat geeft "+vormen[i]+".",\n          "For "+pr.p+" the stem changes: "+v.chEn+". That gives "+vormen[i]+"."),\n    wrongWhy:{[val]: houdt\n      ? L("Dat is de veranderde stam. Juist bij nosotros en vosotros verandert hij niet.",\n          "That is the changed stem. For nosotros and vosotros it is precisely the one that does not change.")\n      : L("Dat is de oude stam. Die blijft alleen staan bij nosotros en vosotros.",\n          "That is the old stem. It only stays for nosotros and vosotros.")},\n    ruleName:L("Stamverandering: overal behalve nosotros en vosotros",\n               "Stem change: everywhere except nosotros and vosotros"),\n    mistake:L("De stam ook bij wij en jullie veranderen.",\n              "Changing the stem for we and you-plural as well."),\n    trick:L("Het staartje is altijd gewoon. Alleen het midden wisselt.",\n            "The ending is always normal. Only the middle shifts.")};\n});',
     'de STEMCH-lijst'),
]


def wijzig(t):
    for oud, nieuw, wat in VERVANGINGEN:
        t = _lib.eenmalig(t, oud, nieuw, wat)
    return t


_lib.draai(MERK, "index.html", wijzig)
