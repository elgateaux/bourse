#!/usr/bin/env python3
"""Vidéo HyperFrames du bilan du portefeuille PEG (1er octobre 2026).

Deux étapes, appelées par fabriquer.sh :
  textes S T : écrit le texte lu par la voix de synthèse, une scène par fichier (T/voix/NN.txt) ;
  html   S T : lit la durée de chaque voix (T/voix/NN.wav) et écrit la composition T/index.html.

Tous les chiffres viennent des CSV du screen S (sorties de portefeuille.py et data/video_*.csv).
La voix lit les nombres en toutes lettres, écrits par ce script à partir des mêmes valeurs.
Bibliothèque standard uniquement.
"""
import csv
import html
import json
import os
import re
import sys
import wave
from decimal import Decimal, ROUND_HALF_UP

ETAPE, D, T = sys.argv[1], sys.argv[2], sys.argv[3]


def lire(nom, dossier=None):
    with open(os.path.join(dossier or D, nom), encoding="utf-8") as f:
        return list(csv.DictReader(f))


DATA = os.path.join(D, "data")
pf = {r["ticker"]: r for r in lire("portefeuille.csv")}
cmp_ = {r["indicateur"]: r for r in lire("comparaison.csv")}
stress = lire("stress_tests.csv")
calendrier = [r for r in lire("video_calendrier.csv", DATA) if r["dans_la_video"] == "1"]
vente = {r["ticker"]: r for r in lire("video_signaux_vente.csv", DATA)}
mode = {r["ticker"]: r for r in lire("video_mode_emploi.csv", DATA)}
LIGNES = ["NU", "RNMBY", "TSM", "UBER", "NVDA"]
assert list(pf) == LIGNES, list(pf)


# ------------------------------------------------------------------ formats écrits
def q(x, d):
    return Decimal(repr(round(x, 10))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)


def fr(x, d=1, signe=False):
    v = q(x, d)
    s = f"{v:+}" if signe else f"{v}"
    if v == 0:
        s = s.replace("+", "").replace("-", "")
    ent, _, dec = s.partition(".")
    neg = ent.startswith("-")
    ent = ent.lstrip("+-")
    if len(ent) > 3:
        ent = f"{int(ent):,}".replace(",", " ")
    pre = "−" if neg else ("+" if signe and v > 0 else "")
    return pre + ent + ("," + dec if dec else "")


def pct(x, d=1, signe=False):
    return fr(100 * x, d, signe) + " %"


def usd(x):
    """Cours calculé (zone d'achat) : mêmes arrondis que l'article (build_bilan.px_calc)."""
    return fr(x, 2 if x < 10 else (1 if x < 100 else 0)) + " $"


def cours(x):
    return fr(x, 2) + " $"


def f(r, k):
    return float(r[k])


def c(col, k):
    return float(cmp_[k][col])


# ------------------------------------------------------------------ nombres dits en lettres
UNITES = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix",
          "onze", "douze", "treize", "quatorze", "quinze", "seize"]
DIZAINES = {20: "vingt", 30: "trente", 40: "quarante", 50: "cinquante", 60: "soixante"}


def _99(n):
    if n < 17:
        return UNITES[n]
    if n < 20:
        return "dix-" + UNITES[n - 10]
    if n < 70:
        d, u = n // 10 * 10, n % 10
        return DIZAINES[d] + ("" if u == 0 else "-et-un" if u == 1 else "-" + UNITES[u])
    if n < 80:
        return "soixante-et-onze" if n == 71 else "soixante-" + _99(n - 60)
    return "quatre-vingts" if n == 80 else "quatre-vingt-" + _99(n - 80)


def _999(n):
    cent, r = divmod(n, 100)
    if cent == 0:
        return _99(r)
    tete = "cent" if cent == 1 else UNITES[cent] + " cent" + ("s" if r == 0 else "")
    return tete + (" " + _99(r) if r else "")


def lettres(n):
    m, r = divmod(n, 1000)
    if m == 0:
        return _999(r)
    tete = "mille" if m == 1 else _999(m) + " mille"
    return tete + (" " + _999(r) if r else "")


def dire(x, d=1):
    """Nombre lu à voix haute, arrondi comme à l'écran : 24,2 -> « vingt-quatre virgule deux »."""
    s = f"{q(x, d)}"
    neg = s.startswith("-")
    ent, _, dec = s.lstrip("-").partition(".")
    mots = ("moins " if neg else "") + lettres(int(ent))
    if dec.strip("0"):
        dec = dec.rstrip("0")
        zeros = len(dec) - len(dec.lstrip("0"))
        mots += " virgule " + "zéro " * zeros + lettres(int(dec))
    return mots


def dire_pct(x, d=1):
    return dire(100 * x, d) + " pour cent"


# Noms écrits pour que la voix française les prononce comme un lecteur francophone.
VOIX = {"NU": "Nou", "RNMBY": "Rhine-métal", "TSM": "TSMC", "UBER": "Oubeur", "NVDA": "Ènvidia"}
NOMS = {"NU": "Nu Holdings", "RNMBY": "Rheinmetall", "TSM": "TSMC", "UBER": "Uber", "NVDA": "NVIDIA"}
THEMES = {"NU": "Banque numérique, Brésil et Mexique", "RNMBY": "Réarmement européen",
          "TSM": "Fabrication des puces d'IA", "UBER": "Mobilité et livraison", "NVDA": "Accélérateurs d'IA"}
LECTURES = {
    "NU": "Le PEG le plus bas de l'univers étudié. Risque du moment : un rachat de Monzo payé en actions.",
    "RNMBY": "Un titre puni pour des erreurs d'exécution, pas pour la demande. Son PDG achète des actions.",
    "TSM": "Grave les puces de tous les concepteurs : gagne quel que soit le vainqueur. Risque numéro un : Taïwan.",
    "UBER": "Le marché craint les robotaxis de Waymo et Tesla. Uber répond par le nombre de partenaires.",
    "NVDA": "Hypothèse prudente : la part des puces sur mesure monte, d'où un poids limité à 10 %.",
}

# ------------------------------------------------------------------ chiffres du bilan
P, N, NH = "portefeuille", "nasdaq100_reconstitue", "nasdaq100_hors_memoire"
pe_p, pe_n = c(P, "pe_ntm"), c(N, "pe_ntm")
g_p, g_n = c(P, "g27"), c(N, "g27")
peg_p, peg_nh = c(P, "peg_lt"), c(NH, "peg_lt")
esp_p, esp_n = c(P, "tcam_esperance"), c(N, "tcam_esperance")
bear_p, bear_n = c(P, "tcam_bear"), c(N, "tcam_bear")
DOUBLE = next(r for r in stress if r["scenario"].startswith("Double choc"))
gagnes = sum(1 for r in stress if float(r["ecart_pts"]) > 0)
poids = {t: f(pf[t], "poids") for t in LIGNES}
part_usd = sum(poids[t] for t in LIGNES if t != "RNMBY")   # Rheinmetall s'achète en euros sur Xetra
part_nu_rnm = poids["NU"] + poids["RNMBY"]
sous_zone = [t for t in LIGNES if f(pf[t], "prix") <= f(pf[t], "prix_peg1")]
au_dessus = [t for t in LIGNES if t not in sous_zone]
assert au_dessus == ["TSM", "NVDA"], au_dessus  # le texte de la scène « pratique » le suppose
assert poids["NU"] == poids["RNMBY"] and poids["TSM"] == poids["UBER"]  # « chacun » dans la scène « composition »

STRESS_VUS = [  # (libellé à l'écran, début du nom du scénario dans stress_tests.csv)
    ("Tout en scénario central", "Tout en base"),
    ("Krach de l'IA", "Krach du capex IA"),
    ("Les puces sur mesure gagnent", "Les puces sur mesure gagnent"),
    ("Choc sur Taïwan (TSMC seul)", "Choc géopolitique sur Taïwan"),
    ("Choc de crédit au Brésil", "Choc de crédit ou politique au Brésil"),
    ("Paix durable en Ukraine", "Paix durable en Ukraine"),
    ("Nu et Rheinmetall déçoivent ensemble", "Double choc"),
]


def scen(debut):
    return next(r for r in stress if r["scenario"].startswith(debut))


def jj_mois(iso):
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
            "octobre", "novembre", "décembre"]
    a, m, j = (int(x) for x in iso.split("-"))
    return ("premier" if j == 1 else lettres(j)) + " " + mois[m - 1]


def jj_mm(iso):
    a, m, j = iso.split("-")
    return f"{j}/{m}"


# ------------------------------------------------------------------ scènes
def e(s):
    return html.escape(s, quote=False)


def kicker(s):
    return f'<p class="kicker">{e(s)}</p>'


scenes = []


def scene(sid, voix, corps, anims):
    voix = re.sub(r"([.?:] )([a-zé])", lambda m: m.group(1) + m.group(2).upper(), " ".join(voix.split()))
    scenes.append({"id": sid, "voix": voix, "corps": corps, "anims": anims})


# 1. Titre
scene("titre", f"""
Le Cahier PEG. Cinq valeurs pour battre le Nasdaque cent : l'essentiel à savoir, en trois minutes.
Chiffres au vingt-neuf septembre.
""", f"""
{kicker("Le Cahier PEG · le bilan en vidéo")}
<h1 class="titre">Cinq valeurs pour battre le Nasdaq&nbsp;100</h1>
<p class="chapo">Tout ce qu'un investisseur doit savoir, en trois minutes.</p>
<p class="meta">Bilan du 01/10/2026 · cours et consensus Zacks du 29/09/2026 · horizon 2026-2030</p>
""", [(".kicker", "up", 0.2), (".titre", "up", 0.5), (".chapo", "up", 1.2), (".meta", "fade", 1.8)])

# 2. Méthode
scene("methode", f"""
La méthode de Piteur Linch : payer la croissance le moins cher possible. On la mesure avec le PEG,
le prix divisé par la croissance des bénéfices. Sous un, c'est bon marché.
Le portefeuille est à {dire(peg_p, 2)}, le Nasdaque, hors mémoire, à {dire(peg_nh, 2)}.
""", f"""
{kicker("La méthode")}
<h2>Peter Lynch : la croissance au juste prix</h2>
<div class="formule"><span>PEG</span> = <span>P/E</span> ÷ <span>croissance annuelle du BPA</span></div>
<div class="echelle">
  <div class="echelle-barre"><div class="zone-bon"></div></div>
  <div class="repere seuil" style="left:{100 / 3:.3f}%"><i>seuil de Lynch</i><b>1</b></div>
  <div class="repere pf" style="left:{peg_p / 3 * 100:.3f}%"><b>{fr(peg_p, 2)}</b><i>Portefeuille</i></div>
  <div class="repere ndx" style="left:{peg_nh / 3 * 100:.3f}%"><b>{fr(peg_nh, 2)}</b><i>Nasdaq 100 hors mémoire</i></div>
</div>
<p class="note">PEG long terme : P/E des 12 prochains mois divisé par la croissance annuelle retenue 2027-2031.</p>
""", [(".kicker", "up", 0.1), ("h2", "up", 0.3), (".formule", "up", 1.2), (".echelle-barre", "grow", 4.0),
      (".repere.seuil", "up", 4.5), (".repere.pf", "up", 7.5), (".repere.ndx", "up", 9.0), (".note", "fade", 9.5)])

# 3. Composition
rangs = "".join(f"""
<div class="ligne l{i}">
  <div class="nom"><b>{e(NOMS[t])}</b><span>{e(THEMES[t])}</span></div>
  <div class="barre"><div class="rempli" style="width:{poids[t] / 0.3 * 100:.1f}%"></div></div>
  <div class="val">{pct(poids[t], 0)}</div>
</div>""" for i, t in enumerate(LIGNES))
scene("composition", f"""
Cinq lignes, cinq moteurs indépendants. {VOIX["NU"]}, la banque numérique d'Amérique latine, et {VOIX["RNMBY"]},
le réarmement européen : {dire_pct(poids["NU"], 0)} chacun. TSMC, qui grave les puces d'IA, et {VOIX["UBER"]} :
{dire_pct(poids["TSM"], 0)} chacun. {VOIX["NVDA"]} : {dire_pct(poids["NVDA"], 0)}.
""", f"""
{kicker("La composition")}
<h2>Cinq lignes, cinq moteurs indépendants</h2>
<div class="lignes">{rangs}</div>
<p class="note">Rééquilibrage une fois par an, ou dès qu'une ligne dépasse 40 % du portefeuille.</p>
""", [(".kicker", "up", 0.1), ("h2", "up", 0.3)]
    + [(f".l{i}", "row", 1.5 + 1.8 * i) for i in range(5)] + [(".note", "fade", 10.0)])

# 4. Valorisation
def duo(label, a, b, lb, cls):
    return f"""<div class="duo {cls}"><p class="lab">{e(label)}</p>
<p class="gros"><span class="pfv">{a}</span></p><p class="vs">Portefeuille</p>
<p class="moyen">{b}</p><p class="vs">{e(lb)}</p></div>"""


scene("valorisation", f"""
Le portefeuille coûte {dire(pe_p)} fois ses bénéfices des douze prochains mois, contre {dire(pe_n)} pour
l'indice, pour une croissance comparable en deux mille vingt-sept : plus {dire(g_p, 0)} pour cent, contre
plus {dire(g_n, 0)}.
""", f"""
{kicker("La valorisation")}
<h2>Moins cher que l'indice, pour la même croissance</h2>
<div class="duos">
{duo("P/E des 12 prochains mois", fr(pe_p), fr(pe_n), "Nasdaq 100", "d1")}
{duo("Croissance du BPA en 2027", fr(g_p, 0, True) + " %", fr(g_n, 0, True) + " %", "Nasdaq 100", "d2")}
{duo("PEG long terme", fr(peg_p, 2), fr(peg_nh, 2), "Nasdaq 100 hors mémoire", "d3")}
</div>
<p class="note">Nasdaq 100 reconstitué avec 31 valeurs, {fr(float(cmp_["couverture_ndx_pct"][N]), 0)} % de son poids. BPA non-GAAP, consensus Zacks.</p>
""", [(".kicker", "up", 0.1), ("h2", "up", 0.3), (".d1", "up", 1.0), (".d2", "up", 5.5), (".d3", "up", 8.0),
      (".note", "fade", 8.5)])

# 5. Rendement espéré : fourchettes
LO, HI = -0.20, 0.50


def x(v):
    return (v - LO) / (HI - LO) * 100


lignes_f = [(NOMS[t], f(pf[t], "tcam_bear"), f(pf[t], "tcam_base"), f(pf[t], "tcam_bull"), f(pf[t], "tcam_esperance"), "")
            for t in LIGNES]
lignes_f += [("Portefeuille", bear_p, c(P, "tcam_base"), c(P, "tcam_bull"), esp_p, " cle"),
             ("Nasdaq 100", bear_n, c(N, "tcam_base"), c(N, "tcam_bull"), esp_n, " ndx")]
fourchettes = "".join(f"""
<div class="fr{cls} f{i}"><div class="nom">{e(n)}</div>
 <div class="piste"><div class="plage" style="left:{x(b):.2f}%;width:{x(h) - x(b):.2f}%"></div>
 <div class="esp" style="left:{x(es):.2f}%"></div></div>
 <div class="val">{pct(es)}</div></div>""" for i, (n, b, m, h, es, cls) in enumerate(lignes_f))
graduations = "".join(f'<span style="left:{x(v / 100):.2f}%">{fr(v, 0, True) if v else "0"} %</span>'
                      for v in range(-20, 51, 10))
scene("rendement", f"""
Notre modèle en attend {dire_pct(esp_p)} par an sur quatre ans, contre {dire_pct(esp_n)} pour l'indice.
Une sortie de modèle, pas une promesse : dans le pire scénario, il perdrait {dire(-100 * bear_p)} pour cent
par an, l'indice {dire(-100 * bear_n)}.
""", f"""
{kicker("Le rendement espéré")}
<h2>{pct(esp_p)} par an espérés, contre {pct(esp_n)}</h2>
<div class="fourchettes">{fourchettes}
 <div class="graduations">{graduations}</div></div>
<p class="note">Du scénario pessimiste à l'optimiste, point : espérance pondérée 25/50/25. Rendement annuel 2026-2030 en dollars.</p>
""", [(".kicker", "up", 0.1), ("h2", "up", 0.3)] + [(f".f{i}", "row", 1.5 + 0.35 * i) for i in range(7)]
    + [(".graduations", "fade", 2.0), (".note", "fade", 3.0), (".fr.cle", "pulse", 6.0)])


# 6-10. Une fiche par valeur
def fiche_voix(t):
    r = pf[t]
    pe, g27, es = f(r, "pe_ntm"), f(r, "g27"), f(r, "tcam_esperance")
    n, fin = VOIX[t], f"Espérance : {dire_pct(es)} par an."
    if t == "NU":
        return f"{n} est la moins chère : {dire(pe, 0)} fois ses bénéfices, et le PEG le plus bas de notre univers. {fin}"
    if t == "RNMBY":
        return (f"{n}, punie pour des erreurs d'exécution, cote {dire(pe, 0)} fois ses bénéfices, pour "
                f"{dire(g27, 0)} pour cent de croissance attendue l'an prochain. {fin}")
    if t == "TSM":
        return f"TSMC grave les puces de tous les concepteurs. C'est la plus chère des cinq, et son grand risque reste Taïwan. {fin}"
    if t == "UBER":
        return (f"{n} cote {dire(pe, 0)} fois ses bénéfices. Le marché craint les robotaxis ; nous pensons qu'ils "
                f"auront besoin de sa plateforme. {fin}")
    return (f"{n} ne pèse que {dire_pct(poids[t], 0)} : face aux puces sur mesure, nous retenons "
            f"{dire(f(r, 'g_lt_base'), 0)} pour cent de croissance par an après deux mille vingt-sept. {fin}")


for i, t in enumerate(LIGNES):
    r = pf[t]
    prix, zone = f(r, "prix"), f(r, "prix_peg1")
    dans = t in sous_zone
    puce = ('<span class="puce bon">Sous sa zone d\'achat</span>' if dans
            else '<span class="puce mal">Au-dessus de sa zone d\'achat</span>')
    stats = [("Poids", pct(poids[t], 0)), ("P/E 12 mois", fr(f(r, "pe_ntm"))),
             ("BPA 2027", fr(f(r, "g27"), 0, True) + " %"), ("PEG long terme", fr(f(r, "peg_lt"), 2)),
             ("Cours au 29/09", cours(prix)), ("Zone d'achat jusqu'à", usd(zone))]
    grille = "".join(f'<div class="stat s{j}"><p>{e(a)}</p><b>{b}</b></div>' for j, (a, b) in enumerate(stats))
    scene(f"fiche-{t.lower()}", fiche_voix(t), f"""
{kicker(f"Les cinq lignes · {i + 1} sur 5")}
<div class="fiche">
 <div class="gauche"><h2 class="nomv">{e(NOMS[t])}</h2><p class="theme">{e(THEMES[t])}</p>
  <p class="espv"><b>{pct(f(r, "tcam_esperance"))}</b><span>par an espérés</span></p>{puce}</div>
 <div class="grille">{grille}</div>
</div>
<p class="lecture">{e(LECTURES[t])}</p>
""", [(".kicker", "up", 0.1), (".nomv", "up", 0.3), (".theme", "up", 0.6), (".espv", "up", 1.0), (".puce", "up", 1.4)]
        + [(f".s{j}", "up", 1.6 + 0.15 * j) for j in range(6)] + [(".lecture", "fade", 3.0)])

# 11. Stress tests
MAXS = 0.30
paires = "".join(f"""
<div class="paire p{i}{' alerte' if float(scen(k)['ecart_pts']) < 0 else ''}"><div class="nom">{e(lab)}</div>
 <div class="barres"><div class="b pfb" style="width:{max(float(scen(k)['tcam_portefeuille']), 0) / MAXS * 100:.1f}%"><span>{pct(float(scen(k)['tcam_portefeuille']))}</span></div>
 <div class="b ndb" style="width:{max(float(scen(k)['tcam_nasdaq100']), 0) / MAXS * 100:.1f}%"><span>{pct(float(scen(k)['tcam_nasdaq100']))}</span></div></div></div>"""
                 for i, (lab, k) in enumerate(STRESS_VUS))
scene("stress", f"""
Sur {lettres(len(stress))} scénarios de crise, le portefeuille bat l'indice {lettres(gagnes)} fois. L'exception :
si {VOIX["NU"]} et {VOIX["RNMBY"]} déçoivent ensemble, il tombe à {dire_pct(float(DOUBLE["tcam_portefeuille"]))} par an,
contre {dire_pct(float(DOUBLE["tcam_nasdaq100"]))} pour l'indice.
""", f"""
{kicker("Les stress tests")}
<h2>Il bat l'indice dans {gagnes} scénarios sur {len(stress)}, sauf un</h2>
<div class="legende"><span class="lp">Portefeuille</span><span class="ln">Nasdaq 100</span></div>
<div class="paires">{paires}</div>
<p class="note">Rendement annuel 2026-2030 : valeurs visées en scénario pessimiste (optimiste pour TSMC face aux puces sur mesure), le reste en central.</p>
""", [(".kicker", "up", 0.1), ("h2", "up", 0.3), (".legende", "fade", 0.8)]
    + [(f".p{i}", "row", 1.2 + 0.4 * i) for i in range(len(STRESS_VUS))] + [(".note", "fade", 4.0),
                                                                              (".paire.alerte", "pulse", 7.0)])

# 12. Critique
critiques = [
    (pct(part_nu_rnm, 0), "du portefeuille repose sur deux valeurs : Nu et Rheinmetall."),
    ("2 sur 5", f"TSMC et NVIDIA cotent au-dessus de leur zone d'achat ({usd(f(pf['TSM'], 'prix_peg1'))} et {usd(f(pf['NVDA'], 'prix_peg1'))})."),
    (pct(part_usd, 0), "des montants sont cotés en dollars : risque de change pour un investisseur en euros."),
    (pct(bear_p), f"par an si tout tourne mal en même temps, contre {pct(bear_n)} pour l'indice : une récession frappe tout le monde."),
]
items = "".join(f'<div class="crit c{i}"><b>{a}</b><p>{e(b)}</p></div>' for i, (a, b) in enumerate(critiques))
scene("critique", f"""
Les points faibles. {dire(100 * part_nu_rnm, 0)} pour cent du portefeuille reposent sur deux valeurs.
TSMC et {VOIX["NVDA"]} sont achetés au-dessus de leur zone d'achat. {dire(100 * part_usd, 0)} pour cent sont cotés
en dollars. Et une récession ferait tout baisser ensemble.
""", f"""
{kicker("La critique")}
<h2>Les questions qui fâchent</h2>
<div class="crits">{items}</div>
""", [(".kicker", "up", 0.1), ("h2", "up", 0.3)] + [(f".c{i}", "up", 1.5 + 2.6 * i) for i in range(4)])

# 13. Mode d'emploi
actions = "".join(f"""<div class="act a{i}"><div class="env {'pea' if mode[t]['enveloppe'] == 'PEA' else 'cto'}">{e(mode[t]['enveloppe'])}</div>
<div class="nom"><b>{e(NOMS[t])}</b> · {pct(poids[t], 0)}</div><p>{e(mode[t]['action'])}</p></div>"""
                  for i, t in enumerate(LIGNES))
scene("pratique", f"""
En pratique, {VOIX["RNMBY"]} va dans le plan d'épargne en actions, achetée en euros. Les quatre autres vont en
compte-titres. TSMC et {VOIX["NVDA"]} s'achètent en deux fois. Consignes du premier octobre : les cours ont bougé depuis.
""", f"""
{kicker("Le mode d'emploi au 01/10/2026")}
<h2>PEA ou compte-titres : qui va où</h2>
<div class="acts">{actions}</div>
<p class="note">Consignes du bilan du 01/10/2026, sur les cours du 29/09. Les cours ont évolué depuis.</p>
""", [(".kicker", "up", 0.1), ("h2", "up", 0.3)] + [(f".a{i}", "row", 1.0 + 0.5 * i) for i in range(5)]
    + [(".note", "fade", 3.5)])

# 14. Quand vendre et calendrier
signaux = "".join(f'<li class="v{i}"><b>{e(NOMS[t])}</b><span>{e(vente[t]["signal"])}</span></li>' for i, t in enumerate(LIGNES))
dates = "".join(f'<li class="k{i}"><b>{jj_mm(r["date"])}</b><span>{e(r["evenement"])}</span></li>' for i, r in enumerate(calendrier))
resultats = [r for r in calendrier if r["evenement"].startswith("Résultats")]
cal_voix = ", ".join(f"{VOIX[t]} le {jj_mois(r['date']) if k == 0 else jj_mois(r['date']).split()[0]}"
                     for k, r in enumerate(resultats) for t in LIGNES if NOMS[t].split()[0] in r["evenement"])
scene("vendre", f"""
On vend sur des signaux fixés à l'avance, comme une marge brute de TSMC sous soixante pour cent.
Prochains résultats : {cal_voix}.
""", f"""
{kicker("Quand vendre, et quand regarder")}
<div class="deux">
 <div><h3>Les signaux de vente</h3><ul class="signaux">{signaux}</ul></div>
 <div><h3>Le calendrier</h3><ul class="cal">{dates}</ul></div>
</div>
""", [(".kicker", "up", 0.1), ("h3", "up", 0.3)] + [(f".v{i}", "row", 1.0 + 0.4 * i) for i in range(5)]
    + [(f".k{i}", "row", 4.0 + 0.4 * i) for i in range(len(calendrier))])

# 15. Fin
scene("fin", """
Analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé.
""", f"""
{kicker("À retenir")}
<h2 class="fin-t">{pct(esp_p)} espérés par an, contre {pct(esp_n)}, avec un point faible : Nu et Rheinmetall ensemble.</h2>
<p class="avert">Analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé.
Les rendements sont des sorties de modèle fondées sur des hypothèses, pas des prévisions.</p>
<p class="sources">Sources : modèle du Cahier PEG (dépôt elgateaux/bourse, screens/2026-09-30_portefeuille-peg_nasdaq100),
consensus Zacks au 29/09/2026. Les résultats de TSMC du 15/10/2026 ne sont pas intégrés.
Voix de synthèse Kokoro ; musique générée par script. « Le Cahier PEG » est un titre fictif,
sans lien avec une publication existante.</p>
""", [(".kicker", "up", 0.1), (".fin-t", "up", 0.4), (".avert", "fade", 1.5), (".sources", "fade", 2.5)])


# ------------------------------------------------------------------ étape 1 : textes
if ETAPE == "textes":
    os.makedirs(os.path.join(T, "voix"), exist_ok=True)
    mots = 0
    for i, s in enumerate(scenes):
        chemin = os.path.join(T, "voix", f"{i:02d}.txt")
        avant = open(chemin, encoding="utf-8").read() if os.path.exists(chemin) else None
        if avant != s["voix"] + "\n":  # un texte inchangé garde sa voix déjà synthétisée
            with open(chemin, "w", encoding="utf-8") as fh:
                fh.write(s["voix"] + "\n")
        mots += len(s["voix"].split())
    print(f"{len(scenes)} scènes, {mots} mots lus")
    sys.exit(0)

assert ETAPE == "html", ETAPE

# ------------------------------------------------------------------ étape 2 : composition
MARGE_AVANT, MARGE_APRES = 0.45, 0.75
t0 = 0.0
for i, s in enumerate(scenes):
    with wave.open(os.path.join(T, "voix", f"{i:02d}.wav")) as w:
        s["voix_duree"] = w.getnframes() / w.getframerate()
    s["debut"] = round(t0, 3)
    s["duree"] = round(MARGE_AVANT + s["voix_duree"] + MARGE_APRES, 3)
    t0 += s["duree"]
TOTAL = round(t0 + 1.0, 3)
scenes[-1]["duree"] = round(TOTAL - scenes[-1]["debut"], 3)
assert TOTAL <= 180, f"vidéo de {TOTAL:.1f} s : plus de 3 minutes"

js = ["const tl = gsap.timeline({ paused: true });"]
for i, s in enumerate(scenes):
    sel = f"#sc-{s['id']}"
    d0 = s["debut"]
    for cible, kind, off in s["anims"]:
        if off > s["duree"] - 0.6:  # une animation tardive serait coupée : on la ramène dans la scène
            off = max(0.2, s["duree"] - 1.5)
        cs = json.dumps(f"{sel} {cible}")
        t = round(d0 + off, 3)
        if kind == "up":
            js.append(f"tl.from({cs}, {{opacity: 0, y: 40, duration: 0.7, ease: 'power3.out'}}, {t});")
        elif kind == "fade":
            js.append(f"tl.from({cs}, {{opacity: 0, duration: 0.8, ease: 'power1.out'}}, {t});")
        elif kind == "row":
            js.append(f"tl.from({cs}, {{opacity: 0, x: -60, duration: 0.6, ease: 'power3.out'}}, {t});")
        elif kind == "grow":
            js.append(f"tl.from({cs}, {{scaleX: 0, transformOrigin: 'left center', duration: 1.0, ease: 'power2.inOut'}}, {t});")
        elif kind == "pulse":
            js.append(f"tl.to({cs}, {{scale: 1.03, duration: 0.35, yoyo: true, repeat: 1, ease: 'sine.inOut'}}, {t});")
    if i:
        js.append(f"tl.from({json.dumps(sel)}, {{opacity: 0, duration: 0.45, ease: 'power1.out'}}, {d0});")
    js.append(f"tl.to({json.dumps(sel)}, {{opacity: 0, duration: 0.4, ease: 'power1.in'}}, {round(d0 + s['duree'] - 0.4, 3)});")
# barres qui poussent : composition, fourchettes, stress tests
js.append("document.querySelectorAll('.rempli, .plage, .b').forEach((el) => {"
          " const sc = el.closest('.clip'); const t0 = parseFloat(sc.dataset.start);"
          " const row = el.closest('.ligne, .fr, .paire');"
          " const k = row ? [...row.parentNode.children].indexOf(row) : 0;"
          " tl.from(el, {scaleX: 0, transformOrigin: 'left center', duration: 0.9, ease: 'power2.out'},"
          " t0 + (el.classList.contains('rempli') ? 1.6 + 1.8 * k : el.classList.contains('plage') ? 1.7 + 0.35 * k : 1.4 + 0.4 * k)); });")
js.append(f"tl.fromTo('#progression', {{scaleX: 0}}, {{scaleX: 1, duration: {TOTAL}, ease: 'none'}}, 0);")
js.append("window.__timelines = window.__timelines || {};")
js.append("window.__timelines['main'] = tl;")

clips = []
for i, s in enumerate(scenes):
    clips.append(f'<section id="sc-{s["id"]}" class="clip scene" data-start="{s["debut"]}" data-duration="{s["duree"]}" '
                 f'data-track-index="1">{s["corps"]}</section>')
    clips.append(f'<audio id="voix-{i:02d}" src="voix/{i:02d}.wav" data-start="{round(s["debut"] + MARGE_AVANT, 3)}" '
                 f'data-duration="{round(s["voix_duree"], 3)}" data-track-index="3" data-volume="1"></audio>')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "video.css"), encoding="utf-8") as fh:
    css = fh.read()

page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>Cinq valeurs pour battre le Nasdaq 100 · la vidéo</title>
<link rel="stylesheet" href="polices/polices.css" />
<script src="vendor/gsap.min.js"></script>
<style>
{css}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
<div id="cadre" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="0">
 <div class="marque">Le Cahier PEG</div>
 <div class="pied">Titre fictif · analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé · données au 29/09/2026</div>
 <div id="progression"></div>
</div>
{chr(10).join(clips)}
<audio id="musique" src="musique.wav" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-volume="1"></audio>
</div>
<script>
{chr(10).join(js)}
</script>
</body>
</html>
"""
with open(os.path.join(T, "index.html"), "w", encoding="utf-8") as fh:
    fh.write(page)
with open(os.path.join(T, "duree.txt"), "w") as fh:
    fh.write(f"{TOTAL}\n")
with open(os.path.join(T, "minutage.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["scene", "debut_s", "duree_s", "voix_s", "texte_lu"])
    for s in scenes:
        w.writerow([s["id"], s["debut"], s["duree"], round(s["voix_duree"], 2), s["voix"]])
print(f"{len(scenes)} scènes, durée totale {TOTAL:.1f} s")
