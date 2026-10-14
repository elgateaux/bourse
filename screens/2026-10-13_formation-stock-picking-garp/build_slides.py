#!/usr/bin/env python3
"""Diaporama « Le stock picking GARP, de zéro à autonome » (13/10/2026), généré depuis les données.

`python3 calcul.py && python3 build_slides.py [--fragment CHEMIN]`

- diaporama/index.html : document complet, autonome (polices embarquées), lisible hors ligne ;
- --fragment CHEMIN : la même page sans <!doctype>, <html>, <head> ni <body>, pour la publication en Artifact.

Deux modes d'affichage : « présentation » (une diapositive 16:9 à la fois, navigation au clavier, animations)
et « lecture » (diapositives empilées, mise en page fluide pour téléphone). Le mode « impression » sert au PDF A4.
Tous les chiffres viennent de diaporama/donnees_formation.json, écrit par calcul.py.
"""
import base64
import html
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diaporama")
FONTS = os.path.join(HERE, "..", "2026-10-13_video-portefeuille_hyperframes", "video", "fonts")
REPO = "https://github.com/elgateaux/bourse/blob/claude/upbeat-shannon-psaybb/"
with open(os.path.join(OUT, "donnees_formation.json"), encoding="utf-8") as f:
    D = json.load(f)
R, V, H, P = D["ratios"], D["val"], D["hyp"], D["params"]
FI = D["fisc"]
INV = {r["id"]: r for r in D["investisseurs"]}
NBSP = " "
COUL = {"NVDA": "#76d672", "TSM": "#ff6b5b", "NU": "#b07cff", "RDDT": "#ff8a3d", "ADYEY": "#3ddc97", "MU": "#5ab4ff",
        "INTC": "#8da2c8", "AAPL": "#c9ced8", "GOOGL": "#ffd166", "NDX": "#8da2c8"}
NOM = {"NVDA": "NVIDIA", "TSM": "TSMC", "NU": "Nu", "RDDT": "Reddit", "ADYEY": "Adyen", "MU": "Micron", "INTC": "Intel",
       "AAPL": "Apple", "GOOGL": "Alphabet"}
CINQ = ["NVDA", "TSM", "NU", "RDDT", "ADYEY"]


# ============================================================ formats
def fr(x, d=1, signe=False):
    if x is None:
        return "n.d."
    s = f"{abs(x):,.{d}f}".replace(",", " ").replace(".", ",").replace(" ", NBSP)
    if x < 0 and float(s.replace(",", ".").replace(NBSP, "")) != 0:
        return "−" + s
    return ("+" + s) if signe else s


def pc(x, d=1, signe=False):
    """x est un ratio (0,25 → 25 %)."""
    return "n.d." if x is None else fr(x * 100, d, signe) + NBSP + "%"


def eur(x, d=0):
    return fr(x, d) + NBSP + "€"


def md(x_m, d=1, u="Md$"):
    return fr(x_m / 1000, d) + NBSP + u


def usd(x, d=2):
    return fr(x, d) + NBSP + "$"


def e(s):
    return html.escape(str(s), quote=True)


def fv(i):
    return float(FI[i]["valeur"])


def cnt(v, d=0, suf="", pre="", signe=False, cls=""):
    """Nombre animé (compte à rebours vers la valeur) ; le texte statique est déjà la valeur finale."""
    return (f'<span class="cnt {cls}" data-v="{v}" data-d="{d}" data-suf="{e(suf)}" data-pre="{e(pre)}" data-s="{1 if signe else 0}">'
            f'{pre}{fr(v, d, signe)}{suf}</span>')


# ============================================================ sources numérotées
class Sources:
    def __init__(self):
        self.liste, self.index = [], {}

    def ref(self, titre, url):
        cle = url or titre
        if cle not in self.index:
            self.liste.append((titre, url))
            self.index[cle] = len(self.liste)
        return self.index[cle]

    def refs(self, paires):
        nums = []
        for t, u in paires:
            n = self.ref(t, u)
            if n not in nums:
                nums.append(n)
        return "".join(f"[{n}]" for n in nums)


S = Sources()


def Z(*tickers):
    return "Zacks " + S.refs([(f"Zacks Investment Research : fiche {t} (cours du 12/10/2026, consensus et comptes au 13/10/2026)",
                               f"https://www.zacks.com/stock/quote/{t}") for t in tickers])


def F(*ids):
    paires = []
    for i in ids:
        r = FI[i]
        paires += [(r["s1"][0], r["s1"][1]), (r["s2"][0], r["s2"][1])]
    return S.refs(paires)


def I(*ids):
    paires = []
    for i in ids:
        r = INV[i]
        paires += [(r["source_titre"], r["source_url"]), (r["source2_titre"], r["source2_url"])]
    return S.refs(paires)


def SOC(soc):
    paires = []
    for r in D["sources_societes"][soc]:
        paires += [(r["source_titre"], r["source_url"]), (r["source2_titre"], r["source2_url"])]
    return S.refs(paires)


def VID():
    return "calculs du 13/10/2026 " + S.refs([("La Gazette du PEG* : modèle PEG et vidéo du portefeuille, 13/10/2026 (valeurs.csv, comparaison.csv, stress_tests.csv)",
                                                REPO + "screens/2026-10-13_video-portefeuille_hyperframes/RAPPORT.md")])


def METH():
    return "méthode " + S.refs([("Prompt de la méthode PEG (règles de calcul, de zone d'achat et de rééquilibrage)", REPO + "prompts/portefeuille-peg-3-valeurs.md")])


def HYPS():
    return "hypothèses " + S.refs([("Hypothèses de la formation, justifiées ligne par ligne (data/hypotheses.csv)",
                                    REPO + "screens/2026-10-13_formation-stock-picking-garp/data/hypotheses.csv")])


def LYN():
    paires = []
    for r in D["lynch"].values():
        paires += [(r["source_titre"], r["source_url"]), (r["source2_titre"], r["source2_url"])]
    return S.refs(paires)


# ============================================================ briques HTML
def kv(lab, val, sub="", c=None, cls=""):
    st = f' style="--c:{c}"' if c else ""
    return (f'<div class="kv a {cls}"{st}><span class="lab">{lab}</span><span class="v">{val}</span>'
            + (f'<span class="sub">{sub}</span>' if sub else "") + "</div>")


def table(head, rows, num=(), cls="", col_cls=None):
    th = "".join(f'<th class="{"n" if i in num else ""}">{h}</th>' for i, h in enumerate(head))
    trs = []
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            k = ("n " if i in num else "") + (col_cls[i] if col_cls and col_cls[i] else "")
            tds.append(f'<td class="{k.strip()}">{c}</td>')
        trs.append("<tr class=\"a\">" + "".join(tds) + "</tr>")
    return f'<div class="tw"><table class="t {cls}"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'


def hbar(lab, frac, val, c="var(--gold)", sub="", neg=False):
    frac = max(0.0, min(1.0, frac))
    return (f'<div class="hb a{" neg" if neg else ""}" style="--c:{c}"><span class="hb-l">{lab}'
            + (f'<small>{sub}</small>' if sub else "") +
            f'</span><span class="hb-t"><i style="width:{frac * 100:.2f}%"></i></span><span class="hb-v">{val}</span></div>')


def quote(i, cls="", fr_only=False, avec_lecon=False):
    q = INV[i]
    en = "" if fr_only else f'<p class="en">« {e(q["texte_original"])} »</p>'
    fr_ = f'<p class="fr">{e(q["traduction"])}</p>'
    by = f'<p class="by">{e(q["auteur"])} · {e(q["occasion"])} · {e(q["date"])} {I(i)}</p>'
    lecon = f'<p class="lecon"><b>Leçon GARP.</b> {e(q["lecon_garp"])}</p>' if avec_lecon else ""
    return f'<blockquote class="q a {cls}">{en}{fr_}{by}{lecon}</blockquote>'


def chip(t):
    return f'<span class="chip" style="--c:{COUL[t]}"><i></i>{NOM[t]}</span>'


def hd(kick, titre, lede=""):
    return (f'<div class="hd"><p class="kick a">{kick}</p><h2 class="h1 a">{titre}</h2>'
            + (f'<p class="lede a">{lede}</p>' if lede else "") + "</div>")


def ul(items, cls=""):
    return f'<ul class="ul {cls}">' + "".join(f'<li class="a">{x}</li>' for x in items) + "</ul>"


# ============================================================ graphiques SVG
def svg_waterfall():
    n = R["NVDA"]
    ca, mb, ro, rai, imp, rn = n["chiffre_affaires"], n["marge_brute_m"], n["resultat_operationnel"], n["resultat_avant_impot"], n["impot"], n["resultat_net"]
    steps = [("Chiffre|d'affaires", ca, "tot"), ("Coût des|ventes", mb - ca, "d"), ("Marge|brute", mb, "tot"),
             ("Charges|d'exploitation", ro - mb, "d"), ("Résultat|opérationnel", ro, "tot"), ("Autres|produits", rai - ro, "d"),
             ("Résultat|avant impôt", rai, "tot"), ("Impôt|", -imp, "d"), ("Résultat|net", rn, "tot")]
    W, Hh, top, base = 1120, 600, 70, 470
    k = (base - top) / ca
    bw, gap, x0 = 96, 25, 20
    out, run = [], 0
    for i, (lab, v, kind) in enumerate(steps):
        x = x0 + i * (bw + gap)
        if kind == "tot":
            y0, y1, run = 0, v, v
            col = "#ffc94a" if i in (0, 8) else "#f2ede2"
        else:
            y0, y1 = run, run + v
            run = y1
            col = "#5be38f" if v > 0 else "#ff5a4f"
        ya, yb = base - max(y0, y1) * k, base - min(y0, y1) * k
        out.append(f'<rect class="gy" style="--i:{i}" x="{x}" y="{ya:.1f}" width="{bw}" height="{max(2, yb - ya):.1f}" fill="{col}" rx="4"/>')
        txt = md(v, 1, "") if kind == "tot" else ("+" if v > 0 else "−") + md(abs(v), 1, "")
        out.append(f'<text class="gt" style="--i:{i}" x="{x + bw / 2}" y="{ya - 14:.1f}" text-anchor="middle" font-size="25" fill="{col}" font-family="GZ Plex Mono" font-weight="600">{txt}</text>')
        l1, l2 = lab.split("|")
        out.append(f'<text class="lbl" x="{x + bw / 2}" y="{base + 34}" text-anchor="middle" font-size="23" fill="#c9ced8">{e(l1)}</text>')
        if l2:
            out.append(f'<text class="lbl" x="{x + bw / 2}" y="{base + 61}" text-anchor="middle" font-size="23" fill="#c9ced8">{e(l2)}</text>')
        if i < len(steps) - 1:
            yl = base - run * k
            out.append(f'<line x1="{x + bw}" x2="{x + bw + gap}" y1="{yl:.1f}" y2="{yl:.1f}" stroke="#8d96a8" stroke-dasharray="4 4"/>')
    out.append(f'<line x1="10" x2="{W - 10}" y1="{base}" y2="{base}" stroke="rgba(242,237,226,.3)"/>')
    out.append(f'<text x="{W - 10}" y="{Hh - 6}" text-anchor="end" font-size="19" fill="#8d96a8" font-family="GZ Plex Mono">en milliards de dollars, exercice clos fin janvier 2026</text>')
    return f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="Cascade du compte de résultat de NVIDIA">{"".join(out)}</svg>'


def svg_cycle():
    h = D["hist"]["MU"]
    pts = []
    for x in h:
        if x["nature"] == "publié":
            pts.append((x["exercice"], x["bpa"], "pub", x["taux_mb"]))
        else:
            pts.append((x["exercice"], x["bpa_ng"], "cons", None))
    W, Hh, base_top, base_bot = 1000, 520, 60, 400
    vmax = max(p[1] for p in pts)
    vmin = min(p[1] for p in pts)
    k = (base_bot - base_top) / (vmax - vmin)
    y0 = base_top + vmax * k
    bw, gap, x0 = 100, 34, 40
    out = [f'<line x1="20" x2="{W - 20}" y1="{y0:.1f}" y2="{y0:.1f}" stroke="rgba(242,237,226,.35)"/>']
    for i, (ex, v, kind, mb) in enumerate(pts):
        x = x0 + i * (bw + gap)
        ya, yb = (y0 - v * k, y0) if v >= 0 else (y0, y0 - v * k)
        if kind == "pub":
            col = "#5ab4ff" if v >= 0 else "#ff5a4f"
            out.append(f'<rect class="gy" style="--i:{i}" x="{x}" y="{ya:.1f}" width="{bw}" height="{max(2, yb - ya):.1f}" fill="{col}" rx="4"/>')
        else:
            out.append(f'<rect class="gy" style="--i:{i}" x="{x}" y="{ya:.1f}" width="{bw}" height="{max(2, yb - ya):.1f}" fill="rgba(90,180,255,.12)" stroke="#5ab4ff" stroke-width="3" stroke-dasharray="8 6" rx="4"/>')
        ty = ya - 12 if v >= 0 else yb + 30
        out.append(f'<text class="gt" style="--i:{i}" x="{x + bw / 2}" y="{ty:.1f}" text-anchor="middle" font-size="26" font-weight="600" fill="#f2ede2" font-family="GZ Plex Mono">{fr(v, 2)}</text>')
        out.append(f'<text x="{x + bw / 2}" y="{base_bot + 64}" text-anchor="middle" font-size="22" fill="#a3abbb" font-family="GZ Plex Mono">{ex}</text>')
        out.append(f'<text x="{x + bw / 2}" y="{base_bot + 96}" text-anchor="middle" font-size="19" fill="{"#8d96a8" if mb is None else "#ffc94a"}" font-family="GZ Plex Mono">{pc(mb, 0) if mb is not None else "consensus"}</text>')
    return f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="Bénéfice par action de Micron, exercices 2022 à 2028">{"".join(out)}</svg>'


def svg_temps():
    t1, t2 = D["temps"]["temps_age_tot"], D["temps"]["temps_age_tard"]
    fin = H["temps_age_fin"]
    W, Hh, l, r, t, b = 1000, 470, 110, 30, 30, 410
    vmax = max(t1["serie"][-1], t2["serie"][-1])
    step = 100000
    ymax = math.ceil(vmax / step) * step
    a0 = t1["age"]

    def X(age):
        return l + (age - a0) / (fin - a0) * (W - l - r)

    def Y(v):
        return b - v / ymax * (b - t)

    out = []
    for yv in range(0, int(ymax) + 1, step):
        out.append(f'<line x1="{l}" x2="{W - r}" y1="{Y(yv):.1f}" y2="{Y(yv):.1f}" stroke="rgba(242,237,226,.08)"/>')
        out.append(f'<text x="{l - 12}" y="{Y(yv) + 7:.1f}" text-anchor="end" font-size="20" fill="#8d96a8" font-family="GZ Plex Mono">{fr(yv / 1000, 0)}{NBSP}k€</text>')
    for age in range(int(a0), int(fin) + 1, 10):
        out.append(f'<text x="{X(age):.1f}" y="{b + 34}" text-anchor="middle" font-size="20" fill="#8d96a8" font-family="GZ Plex Mono">{age} ans</text>')
    for tt, col in ((t1, "#ffc94a"), (t2, "#8da2c8")):
        pts = " ".join(f"{X(tt['age'] + i):.1f},{Y(v):.1f}" for i, v in enumerate(tt["serie"]))
        out.append(f'<polyline class="ln" pathLength="1" points="{pts}" fill="none" stroke="{col}" stroke-width="5" stroke-linejoin="round"/>')
        out.append(f'<circle cx="{X(fin):.1f}" cy="{Y(tt["serie"][-1]):.1f}" r="8" fill="{col}"/>')
    return f'<svg viewBox="0 0 {W} {Hh + 10}" role="img" aria-label="Capital accumulé selon l\'âge de départ">{"".join(out)}</svg>'


# ============================================================ diapositives
SL = []  # (section, titre, fonction)
SECTIONS = [
    ("Ouverture", "", ""),
    ("Objectifs et horizon", "01", "Pourquoi, pour quand, combien : les questions à régler avant d'acheter une seule action."),
    ("Les bases", "02", "Ce qu'on achète vraiment quand on achète une action."),
    ("Lire les comptes", "03", "Compte de résultat, bilan, flux de trésorerie : où se cache la qualité."),
    ("Valoriser", "04", "Capitalisation, P/E, PEG : combien payer pour la croissance."),
    ("La méthode GARP", "05", "La croissance à un prix raisonnable, en règles mesurables."),
    ("Enveloppes, frais et impôts", "06", "PEA, compte-titres, assurance-vie : ce que l'État et les intermédiaires prélèvent."),
    ("Les ETF", "07", "Le socle du portefeuille : comment fonctionne un fonds indiciel coté, et lesquels choisir."),
    ("Intérêts composés", "08", "Le temps, le rendement et les frais : la calculatrice."),
    ("Grands investisseurs", "09", "Lynch, Buffett, Munger, Graham, Fisher, Smith, Bogle, Marks."),
    ("Passer à l'action", "10", "Routine, check-list, quiz, glossaire et sources."),
]


def add(sec, titre, fn, cls=""):
    SL.append({"sec": sec, "titre": titre, "fn": fn, "cls": cls})


def opener(sec):
    num = next(s[1] for s in SECTIONS if s[0] == sec)
    sous = next(s[2] for s in SECTIONS if s[0] == sec)

    def fn(ctx):
        items = [(i, s) for i, s in enumerate(ctx["slides"]) if s["sec"] == sec and "op" not in s["cls"]]
        liste = "".join(f'<li class="a"><a href="#s{i + 1}"><span class="num">{i + 1:02d}</span>{e(s["titre"])}</a></li>' for i, s in items)
        teaser = ctx["teasers"].get(sec, "")
        return (f'<div class="wipe"></div><div class="opn" aria-hidden="true">{num}</div>'
                f'<div class="op-in"><p class="kick a">Chapitre {num}</p><h2 class="xl a">{e(sec)}</h2>'
                f'<p class="lede a">{e(sous)}</p><ol class="op-list">{liste}</ol>{teaser}</div>'), ""
    add(sec, sec, fn, "op")


# ---------------------------------------------------------------- 0. ouverture
def s_cover(ctx):
    lyn = D["lynch"]
    tape = []
    for t in CINQ:
        v = V[t]
        tape.append(f'<span class="tk" style="--c:{COUL[t]}"><b>{t}</b> {usd(v["prix"])} <s>P/E NTM</s> {fr(v["pe_ntm"], 1)} '
                    f'<s>PEG</s> {fr(v["peg_lt"], 2)} <s>espéré</s> {pc(v["tcam_esperance"], 1, True)}/an</span>')
    tape_html = "".join(tape) * 2
    body = f'''
<div class="cv">
  <div class="cv-l">
    <p class="kick a">Hors-série · formation · {D["date"]}</p>
    <h1 class="cv-t a"><span>Le stock picking</span> <em>GARP</em><span>, de zéro à autonome</span></h1>
    <p class="lede a">Lire des comptes. Valoriser une action. Choisir son enveloppe. Laisser composer. Avec cinq cas d'école : NVIDIA, TSMC, Nu, Reddit et Adyen.</p>
    <div class="chips a">{"".join(chip(t) for t in CINQ)}</div>
  </div>
  <div class="cv-r a">
    <span class="lab">Le palmarès qui a lancé la méthode</span>
    <span class="cv-big">{cnt(float(lyn["rendement_annuel"]["valeur"]), 1, NBSP + "%")}</span>
    <span class="cv-sub">par an pour Peter Lynch au fonds Magellan, de {lyn["annee_debut"]["valeur"]} à {lyn["annee_fin"]["valeur"]}. Sa méthode : la croissance à un prix raisonnable, ou GARP (<i>growth at a reasonable price</i>). {LYN()}</span>
  </div>
</div>
<div class="tape a" aria-hidden="true"><div class="tape-in">{tape_html}</div></div>
<p class="cv-disc a">* Titre fictif : il ne correspond à aucune publication existante. Analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé. Cours du {D["date_cours"]}.</p>'''
    return body, "Données : " + Z(*CINQ) + " ; " + VID()


def s_sommaire(ctx):
    cards = []
    for sec, num, sous in SECTIONS[1:]:
        idx = [i for i, s in enumerate(ctx["slides"]) if s["sec"] == sec]
        cards.append(f'<a class="card toc-card a" href="#s{idx[0] + 1}"><span class="tc-n">{num}</span><span class="tc-t">{e(sec)}</span>'
                     f'<span class="tc-s">{e(sous)}</span><span class="tc-r">diapos {idx[0] + 1} à {idx[-1] + 1}</span></a>')
    return hd("Le parcours", "Dix chapitres pour tout maîtriser",
              "Chaque notion est illustrée par une société réelle et des chiffres datés. Cliquez sur un chapitre ; les flèches du clavier font avancer.") + \
        f'<div class="g c5 lc2 main">{"".join(cards)}</div>', ""


def s_objectifs(ctx):
    sp = float(FI["spiva_2025"]["valeur"])
    fx = D["frais"][2]
    items = ["Fixer un objectif, un horizon, et choisir entre investir d'un coup ou progressivement.",
             "Lire un compte de résultat, un bilan et un tableau de flux de trésorerie.",
             "Calculer un BPA, une marge, un FCF, un ROE et un ROIC.",
             "Distinguer le BPA publié (GAAP) du BPA ajusté (non-GAAP).",
             "Juger un P/E et calculer un PEG, puis une zone d'achat.",
             "Classer une société dans les six catégories de Peter Lynch.",
             "Appliquer une grille GARP et fixer des règles de vente.",
             "Choisir entre PEA, compte-titres et assurance-vie, et le bon ETF.",
             "Mesurer l'effet du temps, des frais et des impôts."]
    stats = (f'<div class="card stat a" style="--c:var(--neg)"><span class="v">{cnt(sp, 0, NBSP + "%")}</span><span class="l">des fonds actifs de grandes valeurs américaines ont fait moins bien que le S&amp;P 500 en 2025. Battre l\'indice est difficile. {F("spiva_2025")}</span></div>'
             f'<div class="card stat a" style="--c:var(--gold)"><span class="v">{cnt(fv("pfu_total"), 1, NBSP + "%")}</span><span class="l">de flat tax sur les gains d\'un compte-titres en 2026, contre {fr(fv("ps_2026"), 1)}{NBSP}% dans un PEA de plus de {fr(fv("pea_duree"), 0)}{NBSP}ans. L\'enveloppe compte. {F("pfu_total", "ps_2026")}</span></div>'
             f'<div class="card stat a" style="--c:var(--ndx)"><span class="v">{cnt(fx["part_perdue"] * 100, 1, NBSP + "%")}</span><span class="l">du capital final perdu en {fr(H["frais_duree"], 0)}{NBSP}ans avec {fr(fx["frais"] * 100, 0)}{NBSP}% de frais par an. Les frais aussi. ({HYPS()})</span></div>')
    return hd("Objectifs", "À la fin, vous saurez…") + \
        f'<div class="g c32 main"><div>{ul(items, "ck")}</div><div class="g stats3">{stats}</div></div>', ""


# ---------------------------------------------------------------- 1. les bases
def s_action(ctx):
    n, v = R["NVDA"], V["NVDA"]
    par = lambda x: x / n["actions_moyennes"]
    rdt = n["bpa_gaap"] / v["prix"]
    body = hd("Les bases · une action", "Une action, c'est une part d'entreprise",
              f"NVIDIA compte {fr(n['actions_moyennes'] / 1000, 1)} milliards d'actions en moyenne sur son exercice 2026. En achetant une action à {usd(v['prix'])}, vous possédez une fraction de ses ventes, de ses bénéfices et de sa trésorerie.")
    body += f'''<div class="g c2 main">
  <div class="card a">
    <span class="lab">L'entreprise entière (exercice clos fin janvier 2026)</span>
    <div class="g c2 lc2">
      {kv("Chiffre d'affaires", md(n["chiffre_affaires"]))}
      {kv("Résultat net", md(n["resultat_net"]))}
      {kv("Trésorerie", md(n["tresorerie"]))}
      {kv("Capitalisation boursière", md(v["capitalisation"], 0), "cours × nombre d'actions")}
    </div>
    <p class="p m a">Le <b>BPA</b> (bénéfice par action) divise le résultat net par le nombre moyen d'actions : {md(n["resultat_net"])} ÷ {fr(n["actions_moyennes"] / 1000, 2)} milliards = <b class="gold">{usd(n["bpa_recalcule"])}</b>.</p>
  </div>
  <div class="card hl a">
    <span class="lab">Votre part, pour une action à {usd(v["prix"])}</span>
    <div class="g c2 lc2">
      {kv("Ventes", usd(par(n["chiffre_affaires"])), "par action et par an")}
      {kv("Bénéfice (BPA)", usd(n["bpa_gaap"]), "par action et par an", "var(--gold)")}
      {kv("Trésorerie", usd(par(n["tresorerie"])), "par action")}
      {kv("Dividende versé", usd(par(n["dividendes"])), "par action et par an")}
    </div>
    <p class="p m a">Rapporté au prix payé, le bénéfice donne un <b>rendement bénéficiaire</b> de <b class="gold">{pc(rdt)}</b>. C'est l'inverse du P/E. Vous payez donc surtout la croissance future de ce bénéfice.</p>
  </div>
</div>'''
    return body, "Comptes annuels FY2026 et cours du 12/10/2026 : " + Z("NVDA")


def s_formule(ctx):
    x = D["exemple_pe"]
    body = hd("Les bases · la formule", "Cours = BPA × P/E",
              "Toute la Bourse tient dans cette formule. Le BPA mesure ce que l'entreprise gagne par action. Le P/E (price-to-earnings, ou PER) mesure combien le marché paie chaque dollar de ce bénéfice.")
    body += f'''<div class="g c2 main">
  <div class="g">
    <div class="eq a"><span class="lab">Aujourd'hui</span><span class="eqv">{usd(x["bpa0"], 0)} <i>×</i> {fr(x["pe0"], 0)} <i>=</i> <b>{usd(x["cours0"], 0)}</b></span></div>
    <div class="eq a"><span class="lab">Dans {fr(x["n"], 0)} ans</span><span class="eqv">{usd(x["bpa1"], 0)} <i>×</i> {fr(x["pe1"], 0)} <i>=</i> <b>{usd(x["cours1"], 0)}</b></span></div>
    <div class="card hl a"><p class="p">Le BPA a doublé (<b>{pc(x["tcam_bpa"], 1, True)}</b> par an). Mais le P/E s'est dégonflé (<b class="neg">{pc(x["tcam_pe"], 1, True)}</b> par an). L'action ne gagne que <b class="gold">{pc(x["perf"], 0, True)}</b> en {fr(x["n"], 0)} ans, soit <b class="gold">{pc(x["tcam"], 1, True)}</b> par an.</p></div>
  </div>
  <div class="card a">
    <span class="lab">Les trois moteurs du rendement d'une action</span>
    <ol class="steps">
      <li class="a"><b>La croissance du BPA.</b> Le moteur principal sur trois à cinq ans : à long terme, le cours suit le bénéfice.</li>
      <li class="a"><b>La variation du P/E.</b> L'humeur du marché. Elle peut doper ou annuler la croissance.</li>
      <li class="a"><b>Le dividende.</b> Faible chez les sociétés de croissance : de 0 à 1 % pour nos cinq valeurs.</li>
    </ol>
    <p class="p a"><b class="gold">Le GARP</b> consiste à acheter un BPA qui croît vite, sans payer un P/E qui risque de se dégonfler.</p>
  </div>
</div>'''
    return body, f"Exemple pédagogique ({HYPS()})"


def s_etf(ctx):
    ro = D["retro"]["1an"]
    s1, s15 = float(FI["spiva_2025"]["valeur"]), float(FI["spiva_15ans"]["valeur"])
    rows = [["Frais", "faibles et prévisibles", "courtage et change à l'achat, puis quasi nuls"],
            ["Temps", "quelques minutes par an", "plusieurs heures par trimestre"],
            ["Diversification", "des centaines de lignes", "5 à 15 lignes"],
            ["Potentiel", "le marché, moins les frais", "au-dessus… ou en dessous"],
            ["Risque principal", "le marché lui-même", "vos erreurs de jugement"]]
    body = hd("Les bases · le choix", "ETF ou stock picking : la question honnête",
              "Un ETF (fonds indiciel coté) achète tout l'indice pour quelques frais. Le stock picking choisit quelques actions pour faire mieux. La plupart des professionnels n'y arrivent pas.")
    body += f'''<div class="g c23 main">
  <div class="g">
    <div class="card stat a" style="--c:var(--neg)"><span class="v">{cnt(s1, 0, NBSP + "%")}</span><span class="l">des fonds actifs de grandes valeurs américaines battus par le S&amp;P 500 en 2025 {F("spiva_2025")}</span></div>
    <div class="card stat a" style="--c:var(--neg)"><span class="v">{cnt(s15, 1, NBSP + "%")}</span><span class="l">sur 15 ans, au 31/12/2024 {F("spiva_15ans")}</span></div>
  </div>
  <div class="g">
    {table(["", "ETF indiciel", "Stock picking"], rows, cls="cmp")}
    <div class="card a" style="border-color:var(--neg)"><p class="p"><b>Notre propre rétroviseur.</b> Sur 12 mois, le portefeuille de cinq valeurs a fait <b class="neg">{fr(float(ro["portefeuille_poids_egaux"]), 1, True)}{NBSP}%</b>, contre <b>{fr(float(ro["QQQ"]), 1, True)}{NBSP}%</b> pour le Nasdaq 100 (QQQ). Le stock picking peut sous-performer longtemps. Il n'a de sens qu'avec une méthode, un horizon de trois à cinq ans et de la discipline.</p></div>
  </div>
</div>'''
    body += quote("bogle_haystack", "sm")
    return body, "SPIVA " + F("spiva_2025") + " ; rétroviseur : " + VID()


def s_risque(ctx):
    rows = sorted(CINQ, key=lambda t: V[t]["ecart_plus_haut"])
    pire = rows[0]
    bars = "".join(hbar(NOM[t], -V[t]["ecart_plus_haut"] / 0.5, pc(V[t]["ecart_plus_haut"], 1), COUL[t], f"bêta {fr(V[t]['beta'], 2)}") for t in rows)
    body = hd("Les bases · le risque", f"Une action peut perdre {pc(-V[pire]['ecart_plus_haut'], 0)} sans que l'entreprise aille mal",
              f"Adyen a vu son chiffre d'affaires net croître de {pc(D['adyen']['croissance'], 0)} au premier semestre 2026. Son cours (ADR) est pourtant {pc(-V['ADYEY']['ecart_plus_haut'], 0)} sous son plus haut de 52 semaines.")
    body += f'''<div class="g c2 main">
  <div class="card a"><span class="lab">Écart entre le cours du {D["date_cours"]} et le plus haut de 52 semaines</span>{bars}
  <p class="p m a">Le <b>bêta</b> mesure la sensibilité au marché : un bêta de 2 signifie que l'action bouge en moyenne deux fois plus que l'indice.</p></div>
  <div class="g">
    {ul(["<b>Volatilité</b> : l'ampleur des variations.",
         "<b>Perte maximale</b> (drawdown) : la baisse depuis un plus haut. C'est elle qui pousse à vendre au pire moment.",
         "<b>Risque réel</b> : la perte définitive, quand la thèse d'investissement était fausse.",
         "<b>Règle</b> : n'investir en actions que l'argent dont on n'a pas besoin avant cinq ans."])}
    {quote("lynch_corrections", "sm")}
  </div>
</div>'''
    return body, "Cours, plus hauts de 52 semaines et bêtas : " + Z(*CINQ) + " ; Adyen S1 2026 " + SOC("adyen")


# ---------------------------------------------------------------- 2. lire les comptes
def s_etats(ctx):
    n = R["NVDA"]
    cards = [("Compte de résultat", "Combien l'entreprise gagne-t-elle ?", [("Chiffre d'affaires", md(n["chiffre_affaires"])), ("Résultat opérationnel", md(n["resultat_operationnel"])), ("Résultat net", md(n["resultat_net"]))], "Sur une période : un trimestre ou un exercice."),
             ("Bilan", "Que possède-t-elle ? Que doit-elle ?", [("Trésorerie", md(n["tresorerie"])), ("Dette financière", md(n["dette"])), ("Capitaux propres", md(n["capitaux_propres"]))], "Une photo à une date : la fin de l'exercice."),
             ("Tableau des flux de trésorerie", "Combien d'argent entre vraiment ?", [("Flux opérationnel", md(n["flux_operationnel"])), ("Capex", "−" + md(n["capex"])), ("FCF", md(n["fcf"]))], "Le juge de paix : le cash ne se maquille pas facilement.")]
    html_ = "".join(f'''<div class="card a"><span class="lab">{i + 1} · {t}</span><p class="cq">{q}</p>
      <div class="lines">{"".join(f'<div class="ln-r"><span>{a}</span><b>{b}</b></div>' for a, b in l)}</div><p class="p m">{x}</p></div>''' for i, (t, q, l, x) in enumerate(cards))
    body = hd("Lire les comptes · les documents", "Trois documents, trois questions",
              "Toutes les sociétés cotées publient les mêmes trois tableaux. Exemple avec NVIDIA, exercice clos fin janvier 2026.")
    body += f'<div class="g c3 main">{html_}</div>'
    body += '<p class="p m a">Où les trouver : le rapport annuel (10-K ou 20-F à la SEC pour les sociétés cotées aux États-Unis), les rapports trimestriels, le site « investisseurs » de chaque société, et des bases comme Zacks.</p>'
    return body, "Comptes FY2026 : " + Z("NVDA")


def s_cascade(ctx):
    n = R["NVDA"]
    defs = [("Chiffre d'affaires", "les ventes de la période.", None),
            ("Marge brute", "ventes moins coût direct des produits.", n["marge_brute"]),
            ("Résultat opérationnel (EBIT)", "après la recherche, le marketing et les frais généraux.", n["marge_operationnelle"]),
            ("Résultat net", "après les produits financiers et l'impôt.", n["marge_nette"])]
    d_html = "".join(f'<div class="def a"><b>{a}</b> : {b}' + (f' <span class="gold num">{pc(c)} du CA</span>' if c is not None else "") + "</div>" for a, b, c in defs)
    body = hd("Lire les comptes · le compte de résultat", "Du chiffre d'affaires au BPA : la cascade de NVIDIA",
              f"Sur {md(n['chiffre_affaires'])} de ventes, NVIDIA garde {md(n['resultat_net'])} de bénéfice net. Divisé par {fr(n['actions_moyennes'] / 1000, 2)} milliards d'actions, cela donne un BPA de {usd(n['bpa_gaap'])}.")
    body += f'''<div class="g c31 main"><figure class="ch a">{svg_waterfall()}</figure><div class="g defs">{d_html}
    <div class="def a"><b>Taux d'impôt effectif</b> : <span class="num">{pc(n["taux_impot"])}</span> du résultat avant impôt.</div></div></div>'''
    return body, "Comptes FY2026 : " + Z("NVDA")


def s_marges(ctx):
    rows = []
    for t in ["NVDA", "TSM", "NU", "RDDT"]:
        r = R[t]
        rows.append([f'<span class="dot" style="--c:{COUL[t]}"></span>{NOM[t]} <small>{r["exercice"]}</small>',
                     f'<div class="mini-b" style="--c:{COUL[t]};--w:{r["marge_brute"] * 100:.1f}%"><i></i><span>{pc(r["marge_brute"])}</span></div>',
                     f'<div class="mini-b" style="--c:{COUL[t]};--w:{r["marge_operationnelle"] * 100:.1f}%"><i></i><span>{pc(r["marge_operationnelle"])}</span></div>',
                     f'<div class="mini-b" style="--c:{COUL[t]};--w:{r["marge_nette"] * 100:.1f}%"><i></i><span>{pc(r["marge_nette"])}</span></div>'])
    a = D["adyen"]
    rows.append([f'<span class="dot" style="--c:{COUL["ADYEY"]}"></span>Adyen <small>S1 2026</small>', '<span class="na">non publiée</span>',
                 f'<div class="mini-b" style="--c:{COUL["ADYEY"]};--w:{a["marge_ebitda"] * 100:.1f}%"><i></i><span>{pc(a["marge_ebitda"])} <small>EBITDA</small></span></div>',
                 f'<div class="mini-b" style="--c:{COUL["ADYEY"]};--w:{a["marge_nette"] * 100:.1f}%"><i></i><span>{pc(a["marge_nette"])}</span></div>'])
    body = hd("Lire les comptes · les marges", "Les marges : ce qui reste de chaque dollar vendu",
              "Une marge élevée et stable signale un pouvoir de fixation des prix. Une marge qui monte avec la taille signale un effet d'échelle.")
    body += table(["Société", "Marge brute", "Marge opérationnelle", "Marge nette"], rows, cls="marg")
    body += f'''<div class="g c3 main">
  <div class="card a" style="--c:{COUL["NVDA"]}"><p class="p"><b class="col">NVIDIA</b> garde {pc(R["NVDA"]["marge_operationnelle"], 0)} de résultat opérationnel sur chaque dollar vendu. Rare pour un fabricant de matériel.</p></div>
  <div class="card a" style="--c:{COUL["RDDT"]}"><p class="p"><b class="col">Reddit</b> : {pc(R["RDDT"]["marge_brute"], 0)} de marge brute, car un service en ligne coûte peu à servir. Mais {pc(R["RDDT"]["marge_operationnelle"], 0)} seulement de marge opérationnelle : la croissance coûte cher.</p></div>
  <div class="card a" style="--c:{COUL["NU"]}"><p class="p"><b class="col">Nu</b> est une banque : sa « marge brute » est nette du coût de ses ressources et du risque de crédit. Elle ne se compare pas à celle d'un industriel.</p></div>
</div>'''
    return body, "Comptes annuels : " + Z("NVDA", "TSM", "NU", "RDDT") + " ; Adyen S1 2026 " + SOC("adyen")


def s_croissance(ctx):
    rows = sorted(["NVDA", "TSM", "NU", "RDDT"], key=lambda t: -R[t]["tcam_ca"])
    vmax = max(R[t]["tcam_ca"] for t in rows)
    bars = "".join(hbar(NOM[t], R[t]["tcam_ca"] / vmax, pc(R[t]["tcam_ca"]), COUL[t], f"{R[t]['annee_depart']} → {R[t]['exercice']}") for t in rows)
    rn = "".join(f'<div class="ln-r a"><span><i class="dot" style="--c:{COUL[t]}"></i>{NOM[t]}</span><b>{fr(R[t]["rn_depart"], 0)} → {fr(R[t]["resultat_net"], 0)}{NBSP}M$</b></div>' for t in rows)
    body = hd("Lire les comptes · la croissance", "La croissance se mesure en TCAM",
              "Le taux de croissance annuel moyen (TCAM) lisse les à-coups : c'est le taux constant qui mène du point de départ au point d'arrivée.")
    body += f'''<div class="g c2 main">
  <div class="card a"><span class="lab">TCAM du chiffre d'affaires sur les quatre derniers exercices (trois pour Reddit)</span>{bars}
    <div class="formula a">TCAM = (valeur finale ÷ valeur initiale)<sup>1/n</sup> − 1</div></div>
  <div class="g">
    <div class="card a"><span class="lab">Résultat net, du point de départ au dernier exercice</span>{rn}</div>
    <div class="card hl a"><p class="p"><b>Pourquoi pas la moyenne simple ?</b> Une action qui fait +100 % puis −50 % revient à son point de départ. La moyenne simple affiche +25 % par an ; le TCAM, 0 %.</p></div>
    <p class="p m a">Attention : la croissance passée n'est pas la croissance future. Peter Lynch raisonne sur les trois à cinq prochaines années.</p>
  </div>
</div>'''
    return body, "Comptes annuels : " + Z("NVDA", "TSM", "NU", "RDDT")


def s_gaap(ctx):
    rows = []
    for t in ["NVDA", "TSM", "NU", "RDDT"]:
        r = R[t]
        rows.append([f'<span class="dot" style="--c:{COUL[t]}"></span>{NOM[t]}', r["exercice"], usd(r["bpa_gaap"]), usd(r["bpa_non_gaap"]), pc(r["ecart_non_gaap"], 1, True)])
    ih = {x["exercice"]: x for x in D["hist"]["INTC"]}["2025"]
    rows.append([f'<span class="dot" style="--c:{COUL["INTC"]}"></span>Intel', "2025", usd(ih["bpa"]), usd(ih["bpa_ng"]), "perte → bénéfice"])
    g = V["GOOGL"]
    body = hd("Lire les comptes · le BPA", "BPA publié (GAAP) contre BPA ajusté (non-GAAP)",
              "Le BPA GAAP suit les normes comptables américaines. Le BPA non-GAAP, ou « ajusté », retire des éléments jugés exceptionnels. Analystes et consensus raisonnent en non-GAAP : vérifiez toujours ce qui est retiré.")
    body += f'''<div class="g c32 main">
  {table(["Société", "Exercice", "BPA GAAP", "BPA non-GAAP", "Écart"], rows, num=(2, 3, 4))}
  <div class="g">
    {ul(["<b>Souvent retirés</b> : la rémunération en actions, l'amortissement des acquisitions, les restructurations, les gains ou pertes sur participations.",
         "<b>La rémunération en actions est une vraie charge</b> : elle dilue l'actionnaire (diapositive suivante).",
         f"<b>Alphabet</b> : le consensus 2026 ({usd(g['bpa_f1'])}) dépasse celui de 2027 ({usd(g['bpa_f2'])}). 2026 est gonflé par la réévaluation de participations : notre méthode retient 2027 comme base."])}
  </div>
</div>'''
    return body, "BPA GAAP et non-GAAP : " + Z("NVDA", "TSM", "NU", "RDDT", "INTC", "GOOGL") + " ; " + VID()


def s_dilution(ctx):
    rows = ["NVDA", "TSM", "NU", "RDDT"]
    bars = "".join(hbar(NOM[t], abs(R[t]["dilution"]) / 0.06, pc(R[t]["dilution"], 1, True), COUL[t]) for t in rows)
    n, ts, rd = R["NVDA"], R["TSM"], R["RDDT"]
    body = hd("Lire les comptes · le capital", "Dilution, rachats, dividendes : où va le cash ?",
              "Chaque action nouvelle partage le bénéfice en plus de parts. Chaque action rachetée et annulée le partage en moins de parts.")
    body += f'''<div class="g c2 main">
  <div class="card a"><span class="lab">Variation du nombre d'actions sur le dernier exercice</span>{bars}
    <p class="p m a">Si le nombre d'actions augmente de 5 % par an, le BPA croît environ 5 points moins vite que le résultat net.</p></div>
  <div class="g">
    <div class="card a" style="--c:{COUL["NVDA"]}"><p class="p"><b class="col">NVIDIA</b> a racheté {md(n["rachats"])} d'actions et versé {md(n["dividendes"])} de dividendes, soit {pc(n["retour_actionnaire_fcf"], 0)} de son FCF.</p></div>
    <div class="card a" style="--c:{COUL["TSM"]}"><p class="p"><b class="col">TSMC</b> ne rachète pas ses actions. Il verse {md(ts["dividendes"])} de dividendes, {pc(ts["retour_actionnaire_fcf"], 0)} de son FCF.</p></div>
    <div class="card a" style="--c:{COUL["RDDT"]}"><p class="p"><b class="col">Reddit</b> : {pc(rd["dilution"], 1, True)} d'actions en un an, malgré {fr(rd["rachats"], 0)}{NBSP}M$ consacrés aux rachats et aux retenues fiscales sur actions gratuites. La rémunération en actions dilue.</p></div>
  </div>
</div>'''
    return body, "Comptes annuels : " + Z("NVDA", "TSM", "NU", "RDDT")


def s_fcf(ctx):
    def col(t):
        r = R[t]
        h = lambda x: x / R["NVDA"]["flux_operationnel"] * 100
        return f'''<div class="fcf-col a" style="--c:{COUL[t]}"><span class="lab">{NOM[t]} · {r["exercice"]}</span>
      <div class="fcf-bars"><div class="fb"><i style="height:{h(r["flux_operationnel"]):.1f}%"></i><span>{md(r["flux_operationnel"])}</span><small>flux opérationnel</small></div>
      <div class="fb cx"><i style="height:{h(r["capex"]):.1f}%"></i><span>−{md(r["capex"])}</span><small>capex</small></div>
      <div class="fb fc"><i style="height:{h(r["fcf"]):.1f}%"></i><span>{md(r["fcf"])}</span><small>FCF</small></div></div>
      <div class="ln-r"><span>Capex / chiffre d'affaires</span><b>{pc(r["capex_ca"])}</b></div>
      <div class="ln-r"><span>FCF / résultat net</span><b>{pc(r["conversion_fcf"], 0)}</b></div></div>'''
    body = hd("Lire les comptes · le cash", "Le FCF : l'argent qui reste vraiment",
              "Le flux de trésorerie disponible (free cash flow, FCF) est le cash généré par l'activité, moins le capex : les investissements dans les usines, les machines et les serveurs.")
    body += f'''<div class="g c32 main"><div class="g c2 lc2">{col("NVDA")}{col("TSM")}</div>
  <div class="g">
    <div class="formula a">FCF = flux opérationnel − capex</div>
    {ul([f"<b>NVIDIA conçoit, TSMC fabrique.</b> NVIDIA est « fabless » : capex de {pc(R['NVDA']['capex_ca'])} du chiffre d'affaires. TSMC construit les usines : {pc(R['TSM']['capex_ca'])}.",
         f"<b>Reddit</b> convertit {pc(R['RDDT']['conversion_fcf'], 0)} de son résultat en FCF : la rémunération en actions, sans sortie de cash, gonfle le flux. Elle coûte pourtant en dilution.",
         "<b>Banques</b> : le FCF de Nu n'a pas de sens. Les flux de prêts et de dépôts dominent le tableau de trésorerie."])}
  </div></div>'''
    return body, "Comptes annuels : " + Z("NVDA", "TSM", "RDDT", "NU")


def s_bilan(ctx):
    rows = ["NVDA", "TSM", "RDDT"]
    vmax = max(R[t]["tresorerie"] for t in rows)
    blocs = "".join(f'''<div class="bil a" style="--c:{COUL[t]}"><span class="lab">{NOM[t]}</span>
      {hbar("Trésorerie", R[t]["tresorerie"] / vmax, md(R[t]["tresorerie"]), COUL[t])}
      {hbar("Dette", R[t]["dette"] / vmax, md(R[t]["dette"]), "var(--neg)")}
      <div class="ln-r"><span>Trésorerie nette</span><b class="pos">{md(R[t]["tresorerie_nette"])}</b></div></div>''' for t in rows)
    body = hd("Lire les comptes · le bilan", "Le bilan : la trésorerie nette protège",
              "Actif = ce que l'entreprise possède. Passif = ce qu'elle doit, plus les capitaux propres, c'est-à-dire ce qui revient aux actionnaires.")
    body += f'''<div class="g c32 main"><div class="g c3 lc1">{blocs}</div>
  <div class="g">
    <div class="formula a">Trésorerie nette = trésorerie − dette financière</div>
    {ul(["Une entreprise en trésorerie nette n'a besoin ni des banques ni des marchés pour traverser une crise.",
         "Une dette nette élevée transforme une mauvaise année en problème de survie.",
         "Pour une banque comme Nu, la dette fait partie du métier : on regarde la solvabilité et la qualité des prêts, pas la trésorerie nette."])}
  </div></div>'''
    return body, "Bilans de fin d'exercice : " + Z("NVDA", "TSM", "RDDT")


def s_roic(ctx):
    n = R["NVDA"]
    rows = []
    for t in ["NVDA", "TSM", "NU", "RDDT"]:
        r = R[t]
        roic = "banque : n.a." if r["roic"] is None else (pc(r["roic"], 0) + ("" if r["roic_significatif"] else " <small>(non significatif)</small>"))
        rows.append([f'<span class="dot" style="--c:{COUL[t]}"></span>{NOM[t]}', pc(r["roe"]), roic])
    body = hd("Lire les comptes · la rentabilité", "ROE et ROIC : la rentabilité du capital",
              f"Une entreprise de qualité gagne beaucoup sur l'argent qu'on lui confie. La grille GARP exige au moins {fr(H['garp_rentabilite_min'], 0)}{NBSP}% (hyp.).")
    body += f'''<div class="g c2 main">
  <div class="g">
    <div class="formula a">ROE = résultat net ÷ capitaux propres moyens</div>
    <div class="formula a">ROIC = résultat opérationnel après impôt ÷ capital investi moyen<br><small>capital investi = capitaux propres + dette − trésorerie</small></div>
    <div class="card a"><span class="lab">Le calcul pour NVIDIA</span>
      <div class="ln-r"><span>Résultat opérationnel × (1 − {pc(n["taux_impot"])})</span><b>{md(n["nopat"])}</b></div>
      <div class="ln-r"><span>Capital investi moyen</span><b>{md(n["capital_investi_moyen"])}</b></div>
      <div class="ln-r"><span>ROIC</span><b class="gold">{pc(n["roic"])}</b></div></div>
  </div>
  <div class="g">
    {table(["Société", "ROE", "ROIC"], rows, num=(1, 2))}
    <p class="p m a">Le ROIC de Reddit n'a pas de sens : sa trésorerie couvre presque tous ses capitaux propres, le capital investi est minuscule. On retient alors le ROE. Pour une banque, seul le ROE compte.</p>
  </div>
</div>'''
    return body, "Comptes annuels : " + Z("NVDA", "TSM", "NU", "RDDT") + " ; " + HYPS()


def s_banque(ctx):
    nu, r = D["nu"], R["NU"]
    body = hd("Lire les comptes · les banques", "Lire une banque : l'exemple de Nu",
              "Une banque vend de l'argent : elle emprunte (dépôts) et prête plus cher. Ses indicateurs ne sont pas ceux d'un industriel.")
    body += f'''<div class="g c4 lc2 main">
  {kv("Clients", cnt(nu["clients"], 0, NBSP + "M"), "au 30/06/2026", COUL["NU"])}
  {kv("Résultat net du T2 2026", cnt(nu["resultat_net_trimestre"], 0, NBSP + "M$"), "premier trimestre au-delà du milliard", COUL["NU"])}
  {kv("Marge d'intérêts ajustée du risque", cnt(nu["marge_interets_ajustee_risque"], 1, NBSP + "%"), "ce que rapportent les prêts, après le coût des impayés", COUL["NU"])}
  {kv("Ratio d'efficacité", cnt(nu["ratio_efficacite"], 1, NBSP + "%"), "coûts ÷ revenus : plus il est bas, mieux c'est", COUL["NU"])}
  {kv("ROE 2025", pc(r["roe"]), "la mesure reine pour une banque", "var(--gold)")}
  {kv("Cours ÷ fonds propres (P/B)", fr(V["NU"]["p_b"], 1) + NBSP + "×", "le multiple adapté aux banques", "var(--gold)")}
  {kv("P/E NTM", fr(V["NU"]["pe_ntm"], 1), "12 prochains mois", "var(--gold)")}
  {kv("PEG de long terme", fr(V["NU"]["peg_lt"], 2), "le plus bas des cinq valeurs", "var(--gold)")}
</div>'''
    body += '<p class="p m a">À surveiller à chaque trimestre : le coût du risque (les impayés), la croissance des dépôts, le ROE et le ratio d\'efficacité. Un ROE élevé justifie un P/B élevé, tant qu\'il dure.</p>'
    return body, "Nu T2 2026 " + SOC("nu") + " ; comptes 2025 et cours : " + Z("NU") + " ; " + VID()


def s_plateformes(ctx):
    rd, a = D["reddit"], D["adyen"]
    produit = rd["utilisateurs_actifs_jour"] * rd["revenu_par_utilisateur"]
    body = hd("Lire les comptes · les modèles", "Lire une plateforme : Reddit et Adyen",
              "Pour chaque société, trouvez l'équation de son chiffre d'affaires : un volume multiplié par un prix. Puis suivez chaque terme, trimestre après trimestre.")
    body += f'''<div class="g c2 main">
  <div class="card a" style="--c:{COUL["RDDT"]}"><span class="lab col">Reddit · deuxième trimestre 2026</span>
    <div class="formula">CA ≈ utilisateurs × revenu par utilisateur</div>
    <div class="g c2 lc2">{kv("Utilisateurs actifs quotidiens", cnt(rd["utilisateurs_actifs_jour"], 1, NBSP + "M"), "« DAUq »", COUL["RDDT"])}{kv("Revenu par utilisateur (ARPU)", usd(rd["revenu_par_utilisateur"]), "sur le trimestre", COUL["RDDT"])}
    {kv("Chiffre d'affaires", cnt(rd["chiffre_affaires_trimestre"], 0, NBSP + "M$"), f"{fr(rd['croissance_ca'], 0, True)}{NBSP}% sur un an", COUL["RDDT"])}{kv("Marge d'EBITDA ajusté", cnt(rd["marge_ebitda_ajuste"], 0, NBSP + "%"), "non-GAAP", COUL["RDDT"])}</div>
    <p class="p m">Vérification : {fr(rd["utilisateurs_actifs_jour"], 1)} M × {usd(rd["revenu_par_utilisateur"])} = {fr(produit, 0)}{NBSP}M$.</p></div>
  <div class="card a" style="--c:{COUL["ADYEY"]}"><span class="lab col">Adyen · premier semestre 2026</span>
    <div class="formula">CA net = volume traité × taux de commission</div>
    <div class="g c2 lc2">{kv("Volume de paiements traité", cnt(a["volume_md"], 1, NBSP + "Md€"), "", COUL["ADYEY"])}{kv("Taux de commission (take rate)", pc(a["take_rate"], 3), "CA net ÷ volume", COUL["ADYEY"])}
    {kv("Chiffre d'affaires net", cnt(a["ca"], 1, NBSP + "M€"), pc(a["croissance"], 0, True) + " sur un an", COUL["ADYEY"])}{kv("Marge d'EBITDA", pc(a["marge_ebitda"]), "", COUL["ADYEY"])}</div>
    <p class="p m">Sur 100 € payés chez un marchand, Adyen garde environ {fr(a["take_rate"] * 100 * 100 / 100, 2)} centimes… sur des centaines de milliards d'euros.</p></div>
</div>'''
    return body, "Reddit " + SOC("reddit") + " ; Adyen " + SOC("adyen")


def s_cycliques(ctx):
    mu, it = V["MU"], V["INTC"]
    ih = {x["exercice"]: x for x in D["hist"]["INTC"]}
    body = hd("Lire les comptes · les cycliques", "Les cycliques : le piège du P/E bas",
              f"Micron fabrique de la mémoire. Ses prix suivent l'offre et la demande : son BPA est passé d'une perte à {usd(mu['bpa_fy0'])} (non-GAAP) en trois ans. Il cote {fr(mu['pe_f1'], 1)} fois le BPA attendu pour l'exercice 2027.")
    body += f'''<div class="g c32 main"><figure class="ch a"><span class="lab">Micron : BPA GAAP publié, puis consensus non-GAAP (pointillés), en dollars ; marge brute en or</span>{svg_cycle()}</figure>
  <div class="g">
    <div class="card hl a"><p class="p"><b>La règle de Lynch.</b> Sur une cyclique, un P/E bas signale souvent le sommet du cycle : les bénéfices sont au plus haut et vont baisser. Notre méthode n'applique donc pas de PEG aux cycliques.</p></div>
    <div class="card a" style="--c:{COUL["INTC"]}"><span class="lab col">Intel, un redressement</span>
      <p class="p">BPA GAAP de {usd(ih["2024"]["bpa"])} en 2024, consensus de {usd(ih["2026"]["bpa_ng"])} pour 2026. Le cours a pris {pc(it["chg_52s"], 0, True)} en un an : à {fr(it["pe_f1"], 1)} fois le BPA 2026, le marché paie déjà la guérison.</p></div>
    <p class="p m a">Repérer une cyclique : marges qui font le yo-yo, produit standardisé, prix fixé par le marché (mémoire, acier, pétrole, transport).</p>
  </div></div>'''
    return body, "Comptes annuels et consensus : " + Z("MU", "INTC") + " ; " + METH()


# ---------------------------------------------------------------- 3. valoriser
def s_cap(ctx):
    rows = []
    for t in ["NVDA", "TSM", "RDDT"]:
        v, r = V[t], R[t]
        rows.append([f'<span class="dot" style="--c:{COUL[t]}"></span>{NOM[t]}', md(v["capitalisation"]), md(r["dette"]), md(r["tresorerie"]), f'<b>{md(v["valeur_entreprise"])}</b>'])
    rows.append([f'<span class="dot" style="--c:{COUL["NU"]}"></span>Nu', md(V["NU"]["capitalisation"]), "—", "—", "<i>non pertinente</i>"])
    body = hd("Valoriser · la taille", "Capitalisation et valeur d'entreprise",
              "La capitalisation est le prix de toutes les actions. La valeur d'entreprise (VE) est le prix de l'entreprise entière : on ajoute la dette qu'on reprendrait et on retire la trésorerie qu'on encaisserait.")
    body += f'''<div class="g main">
  <div class="g c2"><div class="formula a">Capitalisation = cours × nombre d'actions</div><div class="formula a">VE = capitalisation + dette − trésorerie</div></div>
  {table(["Société", "Capitalisation", "+ dette", "− trésorerie", "= valeur d'entreprise"], rows, num=(1, 2, 3, 4))}
  <p class="p m a">On rapporte la VE au résultat opérationnel (VE/EBIT) ou à l'EBITDA pour comparer des sociétés plus ou moins endettées. Pour une banque, la VE n'a pas de sens : la dette est sa matière première. Capitalisations du {D["date_cours"]}, bilans du dernier exercice publié ; TSMC en dollars, par ADR.</p>
</div>'''
    return body, "Capitalisations et bilans : " + Z("NVDA", "TSM", "RDDT", "NU")


def s_pe5(ctx):
    pe5 = D["pe5"]
    vmax = max(p for _, _, p in pe5)
    bars = "".join(hbar(l, p / vmax, fr(p, 1), "var(--gold)" if "NTM" in l else COUL["NVDA"], f"BPA {usd(b)}") for l, b, p in pe5)
    nv = D["nvda_zacks"]
    body = hd("Valoriser · le P/E", f"Un seul cours, cinq P/E : NVIDIA de {fr(min(p for *_, p in pe5), 1)} à {fr(vmax, 1)}",
              f"Même cours ({usd(V['NVDA']['prix'])}), cinq bénéfices différents au dénominateur. Quand la croissance est forte, le choix du BPA change tout.")
    body += f'''<div class="g c32 main"><div class="card a"><span class="lab">P/E de NVIDIA selon le BPA retenu (BPA non-GAAP)</span>{bars}</div>
  <div class="g">{ul(["<b>Dernier exercice</b> (trailing) : le passé publié.",
                    "<b>12 derniers mois</b> : les quatre derniers trimestres publiés.",
                    "<b>Exercice en cours</b> (forward) : le consensus de l'année.",
                    "<b>12 prochains mois (NTM)</b> : notre référence. Il mêle l'exercice en cours et le suivant au prorata des mois restants.",
                    "<b>Toujours dire quel P/E on cite.</b> Comparer un P/E passé à un P/E futur n'a aucun sens."])}</div></div>'''
    return body, "Cours, BPA publiés et consensus : " + Z("NVDA") + f" (P/E 12 mois : fiche du {D['date_cours']}) ; NTM : " + VID()


def s_multiples(ctx):
    rows = []
    for t in ["NVDA", "TSM", "RDDT"]:
        v = V[t]
        rows.append([f'<span class="dot" style="--c:{COUL[t]}"></span>{NOM[t]}', fr(v["pe_ntm"], 1), fr(v["p_s"], 1), fr(v["ve_ebit"], 1), pc(v["rendement_fcf"])])
    rows.append([f'<span class="dot" style="--c:{COUL["NU"]}"></span>Nu', fr(V["NU"]["pe_ntm"], 1), "—", "—", f'P/B {fr(V["NU"]["p_b"], 1)}']
                )
    guide = [["P/E", "sociétés bénéficiaires et régulières", "le bénéfice peut être ajusté, ou cyclique"],
             ["P/S (cours ÷ ventes)", "croissance encore peu rentable", "ignore les marges"],
             ["VE/EBIT ou VE/EBITDA", "comparer des sociétés plus ou moins endettées", "l'EBITDA ignore le capex"],
             ["Rendement FCF (FCF ÷ capitalisation)", "la vraie rémunération en cash", "faible pour une société qui investit"],
             ["P/B (cours ÷ fonds propres)", "banques et assureurs", "inutile pour les actifs immatériels"]]
    body = hd("Valoriser · les multiples", "Un multiple pour chaque type de société",
              "Le P/E ne suffit pas. Chaque multiple éclaire un angle : les ventes, le résultat avant dette, le cash, les fonds propres.")
    body += f'''<div class="g c2 main">
  <div class="g">{table(["Société", "P/E NTM", "P/S", "VE/EBIT", "Rdt FCF"], rows, num=(1, 2, 3, 4))}
    <p class="p m a">P/S, VE/EBIT et rendement FCF : dernier exercice publié, cours du {D["date_cours"]}. Des multiples passés élevés se justifient seulement si la croissance future suit.</p></div>
  {table(["Multiple", "Utile pour", "Son angle mort"], guide)}
</div>'''
    return body, "Données : " + Z("NVDA", "TSM", "RDDT", "NU") + " ; P/E NTM : " + VID()


def s_peg(ctx):
    rows = []
    for t in CINQ:
        v = V[t]
        rows.append([f'<span class="dot" style="--c:{COUL[t]}"></span>{NOM[t]}', fr(v["pe_ntm"], 1), pc(v["croissance_retenue"], 0), f'<b>{fr(v["peg_lt"], 2)}</b>'])
    nv = V["NVDA"]
    seuils = {"forte": H["zone_peg_forte"], "zone": H["zone_peg"], "elig": H["garp_peg_max"], "vente": H["vente_peg"]}
    body = hd("Valoriser · le PEG", "Le PEG : le prix de la croissance",
              "Peter Lynch divise le P/E par le taux de croissance annuel du BPA, exprimé en points. Une société qui croît de 15 % par an vaut, selon lui, environ 15 fois ses bénéfices : un PEG de 1.")
    body += f'''<div class="g c2 main">
  <div class="g">
    <div class="formula a">PEG = P/E ÷ croissance annuelle du BPA (en %)</div>
    <div class="card a pegcalc" data-forte="{seuils['forte']}" data-zone="{seuils['zone']}" data-elig="{seuils['elig']}" data-vente="{seuils['vente']}">
      <span class="lab">À vous : calculez un PEG</span>
      <div class="g c2 lc2"><label class="fld"><span>P/E</span><input type="number" id="peg-pe" value="{nv['pe_ntm']:.1f}" min="1" max="200" step="0.1" inputmode="decimal"></label>
      <label class="fld"><span>Croissance du BPA (% par an)</span><input type="number" id="peg-g" value="{nv['croissance_retenue'] * 100:.0f}" min="1" max="100" step="0.5" inputmode="decimal"></label></div>
      <div class="peg-out"><span class="peg-v" id="peg-v">{fr(nv['pe_ntm'] / (nv['croissance_retenue'] * 100), 2)}</span><span class="peg-txt" id="peg-txt">éligible à la méthode</span></div>
      <div class="gauge"><i class="gz z1"></i><i class="gz z2"></i><i class="gz z3"></i><i class="gz z4"></i><i class="gz z5"></i><b class="gm" id="peg-m"></b></div>
      <div class="gauge-l"><span>0</span><span>{fr(seuils['forte'], 1)}</span><span>{fr(seuils['zone'], 0)}</span><span>{fr(seuils['elig'], 1)}</span><span>{fr(seuils['vente'], 0)}</span><span>3</span></div>
    </div>
  </div>
  <div class="g">{table(["Valeur", "P/E NTM", "Croissance retenue (hyp.)", "PEG long terme"], rows, num=(1, 2, 3))}
    {quote("lynch_peg", "sm")}</div>
</div>'''
    return body, "Données et croissances retenues : " + VID() + " ; " + METH()


def s_piege(ctx):
    rows = []
    for t in CINQ:
        v = V[t]
        rows.append([f'<span class="dot" style="--c:{COUL[t]}"></span>{NOM[t]}', pc(v["croissance_2027"], 0, True), fr(v["peg_2027"], 2), pc(v["croissance_retenue"], 0), f'<b>{fr(v["peg_lt"], 2)}</b>'])
    c = D["comparaison"]
    rows.append(['<span class="dot" style="--c:var(--ndx)"></span>Nasdaq 100 reconstitué', pc(c["g27"]["ndx"] / 100, 0, True), fr(c["peg27"]["ndx"], 2), pc(c["g_lt"]["ndx"] / 100, 1), f'<b>{fr(c["peg_lt"]["ndx"], 2)}</b>'])
    body = hd("Valoriser · le piège", "Le piège : un PEG flatté par une croissance de pic",
              f"Le consensus prévoit {pc(V['NVDA']['croissance_2027'], 0, True)} de BPA pour NVIDIA en 2027. Avec ce chiffre, le PEG tombe à {fr(V['NVDA']['peg_2027'], 2)}. Mais une croissance pareille ne dure pas.")
    body += f'''<div class="g c32 main">{table(["Valeur", "BPA 2027 (consensus)", "PEG 2027", "Croissance retenue", "PEG long terme"], rows, num=(1, 2, 3, 4))}
  <div class="g">{ul(["<b>Plafond.</b> Dans le PEG N+1, la méthode plafonne la croissance à 50 % pour neutraliser les effets de base.",
                    "<b>Prudence.</b> Le PEG de long terme utilise une croissance durable, plus prudente que le consensus quand celui-ci extrapole un pic (hyp.).",
                    f"<b>L'indice aussi.</b> Le Nasdaq 100 affiche un PEG 2027 de {fr(c['peg27']['ndx'], 2)}, mais {fr(c['peg_lt']['ndx'], 2)} sur la durée : la mémoire, au sommet de son cycle, fausse la photo ({fr(c['peg_lt']['ndx_hm'], 2)} hors mémoire)."])}</div></div>'''
    return body, "Données : " + VID() + " ; " + METH()


def s_consensus(ctx):
    nv, v = D["nvda_zacks"], V["NVDA"]
    rows = [[f'<span class="dot" style="--c:{COUL[t]}"></span>{NOM[t]}', str(V[t]["zacks_rank"])] for t in CINQ]
    body = hd("Valoriser · les attentes", "Consensus, surprises et rang Zacks",
              "Le consensus est la moyenne des prévisions des analystes. À court terme, les cours réagissent surtout à ses révisions et aux surprises des publications.")
    body += f'''<div class="g c3 main">
  <div class="card a" style="--c:{COUL["NVDA"]}"><span class="lab col">NVIDIA vu par Zacks, le {D["date_cours"]}</span>
    <div class="ln-r"><span>BPA FY2027 attendu</span><b>{usd(v["bpa_f1"])}</b></div>
    <div class="ln-r"><span>BPA FY2028 attendu</span><b>{usd(v["bpa_f2"])} <small>ou {usd(float(nv["bpa_fy2028_fiche"]))}</small></b></div>
    <div class="ln-r"><span>Surprise du dernier trimestre</span><b class="pos">{fr(float(nv["surprise_bpa_dernier_trimestre"]), 2, True)}{NBSP}%</b></div>
    <div class="ln-r"><span>Rang Zacks (court terme)</span><b>{nv["zacks_rank"]} · achat fort</b></div>
    <div class="ln-r"><span>Recommandation (long terme)</span><b>{nv["recommandation"]}</b></div>
    <div class="ln-r"><span>Objectif de cours</span><b>{usd(float(nv["objectif_zacks"]), 0)}</b></div>
    <div class="ln-r"><span>Scores valeur · croissance · momentum</span><b>{nv["score_value"]} · {nv["score_growth"]} · {nv["score_momentum"]}</b></div></div>
  <div class="g">{table(["Valeur", "Rang Zacks"], rows, num=(1,))}<p class="p m a">De 1 (achat fort) à 5 (vente forte), selon les révisions de bénéfices. Un outil de court terme, pas une thèse.</p></div>
  <div class="g">{ul([f"<b>Deux pages, deux chiffres.</b> Le même jour, Zacks affiche {usd(v['bpa_f2'])} et {usd(float(nv['bpa_fy2028_fiche']))} pour le BPA 2028 de NVIDIA. Le consensus est une moyenne mouvante, pas une vérité.",
                    "<b>Les révisions comptent plus que le niveau.</b> Un BPA attendu relevé trimestre après trimestre porte le cours.",
                    "<b>Les objectifs de cours sont des opinions datées.</b> On les cite comme telles."])}</div>
</div>'''
    return body, "Consensus et métriques : " + Z("NVDA", *CINQ[1:])


def s_suppose(ctx):
    c = D["comparaison"]
    rows = []
    for t in CINQ:
        v = V[t]
        rows.append([f'<span class="dot" style="--c:{COUL[t]}"></span>{NOM[t]}', usd(v["prix"]), usd(v["prix_peg1"]), pc(v["ecart_zone"], 1, True)])
    body = hd("Valoriser · le second niveau", "Ce que le prix suppose déjà",
              "« Bonne société, donc j'achète » ne suffit pas. La vraie question : quelle croissance le cours suppose-t-il, et en quoi pensez-vous différemment du marché ?")
    body += f'''<div class="g c2 main">
  <div class="g">
    <div class="g c3 lc1">
      {kv("P/E NTM", f'{fr(c["pe_ntm"]["ptf"], 1)} <small>contre {fr(c["pe_ntm"]["ndx"], 1)}</small>', "portefeuille contre Nasdaq 100", "var(--gold)")}
      {kv("Croissance durable retenue", f'{fr(c["g_lt"]["ptf"], 1)}{NBSP}% <small>contre {fr(c["g_lt"]["ndx"], 1)}{NBSP}%</small>', "hyp.", "var(--gold)")}
      {kv("PEG long terme", f'{fr(c["peg_lt"]["ptf"], 2)} <small>contre {fr(c["peg_lt"]["ndx"], 2)}</small>', "", "var(--gold)")}
    </div>
    <p class="p a">À {fr(c["pe_ntm"]["ndx"], 1)} fois les bénéfices, le Nasdaq 100 suppose une croissance d'environ {fr(c["pe_ntm"]["ndx"], 0)}{NBSP}% par an pour un PEG de 1. Nous retenons {fr(c["g_lt"]["ndx"], 1)}{NBSP}%. Le portefeuille, lui, est payé à peu près sa croissance.</p>
    {quote("marks_second", "sm")}
  </div>
  <div class="g">{table(["Valeur", "Cours", "Cours pour un PEG de 1", "Écart"], rows, num=(1, 2, 3))}
  <p class="p m a">Toutes les valeurs cotent au-dessus de leur prix « PEG = 1 ». Acheter quand même, c'est parier sur une croissance au moins égale à l'hypothèse centrale.</p></div>
</div>'''
    return body, "Données : " + VID()


# ---------------------------------------------------------------- 4. méthode GARP
def s_categories(ctx):
    cats = {c["ticker"]: c for c in D["categories"]}
    defs = [("Croissance lente", "Grandes sociétés mûres, au rythme de l'économie. On les achète pour le dividende.", "Rares au Nasdaq 100.", []),
            ("Valeurs solides", "Grandes sociétés qui croissent de 10 à 12 % par an. Un amortisseur en cas de crise.", "Le piège : les payer trop cher.", ["AAPL"]),
            ("Croissance rapide", "Petites et moyennes sociétés qui croissent de 20 à 25 % par an. La catégorie préférée de Lynch.", "Le piège : la fin de la croissance.", ["NU", "ADYEY", "TSM", "NVDA"]),
            ("Cycliques", "Profits au rythme du cycle : semi-conducteurs de mémoire, automobile, acier.", "Le piège : le P/E bas au sommet.", ["MU"]),
            ("Redressements", "Sociétés en difficulté qui peuvent se relever.", "Le piège : la rechute.", ["INTC", "RDDT"]),
            ("Valeurs d'actifs", "Sociétés assises sur des actifs que le marché ignore : immobilier, brevets, trésorerie.", "Rares au Nasdaq 100.", [])]
    cards = []
    for nom, d, piege, ts in defs:
        ex = "".join(f'<div class="ex"><span class="dot" style="--c:{COUL[t]}"></span><b>{NOM[t]}</b> <span>{e(cats[t]["indicateur"])} : <b class="num">{cats[t]["valeur"]}</b></span></div>' for t in ts)
        cards.append(f'<div class="card cat a"><span class="lab">{nom}</span><p class="p">{d}</p><p class="p m"><i>{piege}</i></p>{ex}</div>')
    body = hd("La méthode GARP · classer", "Les six catégories de Peter Lynch",
              "Avant de valoriser une société, Lynch la classe. On ne juge pas une cyclique comme une croissance rapide, ni un redressement comme une valeur solide.")
    body += f'<div class="g c3 lc1 main cats">{"".join(cards)}</div>'
    return body, "Catégories : " + I("lynch_categories") + " ; classement des exemples (hyp.) et données : " + Z("AAPL", "NU", "TSM", "NVDA", "MU", "INTC", "RDDT") + " ; Adyen " + SOC("adyen")


def s_grille(ctx):
    rows = [["Croissance durable du BPA", f"≥ {fr(H['garp_croissance_min'], 0)}{NBSP}% par an", "Le moteur du cours à long terme", "Lynch"],
            ["PEG de long terme", f"≤ {fr(H['garp_peg_max'], 1)}", "Ne pas surpayer la croissance", "Lynch"],
            ["ROIC (ROE pour une banque)", f"≥ {fr(H['garp_rentabilite_min'], 0)}{NBSP}%", "Une entreprise de qualité", "Buffett, Smith"],
            ["Marge nette", f"≥ {fr(H['garp_marge_nette_min'], 0)}{NBSP}%", "Un pouvoir de fixation des prix", "Fisher"],
            ["Dilution", f"≤ {fr(H['garp_dilution_max'], 0)}{NBSP}% par an", "Le BPA suit le résultat net", "Buffett"],
            ["Trésorerie nette", "≥ 0", "Survivre à une crise", "Graham"],
            ["Rang Zacks", f"≤ {fr(H['garp_rank_max'], 0)}", "Des révisions qui ne baissent pas", "consensus"]]
    body = hd("La méthode GARP · la grille", "La grille GARP en sept critères",
              "Sept critères chiffrés, les mêmes pour chaque société. Ils ne remplacent pas le jugement : ils forcent à regarder les mêmes choses à chaque fois.")
    body += f'''<div class="g c31 main">{table(["Critère", "Seuil (hyp.)", "Pourquoi", "Inspiration"], rows)}
  <div class="g"><div class="card hl a"><span class="lab">Le huitième critère, qualitatif</span><p class="p">Un avantage concurrentiel que l'on sait expliquer en une phrase : un écosystème logiciel (NVIDIA), une avance de fabrication (TSMC), un coût d'acquisition client très bas (Nu), un réseau de communautés (Reddit), une plateforme unique de paiement (Adyen).</p></div>
  <p class="p m a">Seuils : {HYPS()}. Le PEG maximal de {fr(H['garp_peg_max'], 1)} est la règle d'éligibilité de la méthode.</p></div></div>'''
    return body, HYPS() + " ; " + METH()


def s_grille_app(ctx):
    G = {g["ticker"]: g for g in D["grille"]}
    crit = [c[0] for c in G["NVDA"]["criteres"]]
    rows = []
    for i, cname in enumerate(crit):
        r = [cname]
        for t in CINQ:
            _, val, ok = G[t]["criteres"][i]
            mark = "ok" if ok is True else ("ko" if ok is False else "na")
            sym = {"ok": "✓", "ko": "✗", "na": "–"}[mark]
            r.append(f'<span class="mk {mark}">{sym}</span> {val}')
        rows.append(r)
    rows.append(["<b>Score</b>"] + [f'<b>{G[t]["score"]} / {G[t]["evalues"]}</b>' for t in CINQ])
    head = ["Critère"] + [f'<span class="dot" style="--c:{COUL[t]}"></span>{NOM[t]}' for t in CINQ]
    body = hd("La méthode GARP · l'application", "La grille appliquée aux cinq valeurs",
              "Les cinq valeurs ont été choisies avec cette méthode : elles passent presque tous les critères. Les écarts sont plus instructifs que les succès.")
    body += table(head, rows, cls="grille w")
    body += f'''<div class="g c3 main">
  <div class="card a" style="--c:{COUL["RDDT"]}"><p class="p"><b class="col">Reddit</b> échoue sur la dilution ({pc(R["RDDT"]["dilution"], 1, True)} d'actions en un an). À surveiller à chaque trimestre.</p></div>
  <div class="card a" style="--c:{COUL["ADYEY"]}"><p class="p"><b class="col">Adyen</b> : comptes annuels complets non collectés pour cette formation. Trois critères restent « n.d. » : un trou à combler avant d'acheter.</p></div>
  <div class="card a" style="--c:{COUL["NU"]}"><p class="p"><b class="col">Nu</b> : le critère de trésorerie nette ne s'applique pas à une banque. Le ROE le remplace.</p></div>
</div>'''
    return body, "Calculs : grille_garp.csv ; données " + Z(*CINQ) + " ; " + VID() + " ; " + HYPS()


def s_scenarios(ctx):
    lo, hi = -0.25, 0.45

    def pos(x):
        return (x - lo) / (hi - lo) * 100

    rows = []
    items = [(t, NOM[t], COUL[t], V[t]["tcam_bear"], V[t]["tcam_base"], V[t]["tcam_bull"], V[t]["tcam_esperance"]) for t in CINQ]
    c = D["comparaison"]
    items.append(("PTF", "Portefeuille", "var(--gold)", c["tcam_bear"]["ptf"], c["tcam_base"]["ptf"], c["tcam_bull"]["ptf"], c["tcam_esperance"]["ptf"]))
    items.append(("NDX", "Nasdaq 100", "var(--ndx)", c["tcam_bear"]["ndx"], c["tcam_base"]["ndx"], c["tcam_bull"]["ndx"], c["tcam_esperance"]["ndx"]))
    for t, nom, col, b, m, u, esp in items:
        rows.append(f'''<div class="rg a" style="--c:{col}"><span class="rg-l">{nom}</span><span class="rg-t"><i class="rg-band" style="left:{pos(b):.2f}%;width:{pos(u) - pos(b):.2f}%"></i>
      <i class="rg-m" style="left:{pos(m):.2f}%"></i><i class="rg-e" style="left:{pos(esp):.2f}%"></i>
      <span class="rg-v b" style="left:{pos(b):.2f}%">{pc(b, 0, True)}</span><span class="rg-v u" style="left:{pos(u):.2f}%">{pc(u, 0, True)}</span></span><span class="rg-x">{pc(esp, 1, True)}</span></div>''')
    ticks = "".join(f'<span style="left:{pos(x / 100):.2f}%">{fr(x, 0, x > 0)}{NBSP}%</span>' for x in range(-20, 41, 10))
    body = hd("La méthode GARP · l'incertitude", "Penser en fourchettes : trois scénarios par valeur",
              "Pessimiste, central, optimiste, pondérés 25 / 50 / 25 : on en tire un rendement annuel espéré sur quatre ans.")
    body += f'''<div class="g c31 main"><div class="card tight a"><div class="rg-head"><span class="lab">Rendement annuel sur 4 ans : pessimiste · central (trait) · optimiste ; losange = espérance</span><span class="lab">Espéré</span></div>
    {"".join(rows)}<div class="rg-ticks">{ticks}</div></div>
  <div class="g">{ul(["<b>L'espérance se calcule sur les valeurs finales</b>, pas sur les taux : le scénario optimiste pèse plus qu'il n'y paraît.",
                    "<b>Le pessimiste n'est pas le pire</b> : c'est un scénario plausible et défavorable, avec un P/E de sortie comprimé."])}</div></div>'''
    return body, "Scénarios et espérances : " + VID() + " ; " + METH()


def s_zone(ctx):
    rows = []
    for t in CINQ:
        v = V[t]
        lo = v["prix_peg08"] * 0.9
        hi = max(v["prix"], v["prix_peg1"]) * 1.08
        p = lambda x: (x - lo) / (hi - lo) * 100
        rows.append(f'''<div class="zn a" style="--c:{COUL[t]}"><span class="zn-l">{NOM[t]}</span><span class="zn-t">
      <i class="zn-safe" style="left:0;width:{p(v["prix_peg08"]):.2f}%"></i><i class="zn-buy" style="left:{p(v["prix_peg08"]):.2f}%;width:{p(v["prix_peg1"]) - p(v["prix_peg08"]):.2f}%"></i>
      <i class="zn-px" style="left:{p(v["prix"]):.2f}%"></i><span class="zn-pl" style="left:{p(v["prix"]):.2f}%">{usd(v["prix"])}</span>
      <span class="zn-a" style="left:{p(v["prix_peg08"]):.2f}%">{usd(v["prix_peg08"])}</span><span class="zn-a" style="left:{p(v["prix_peg1"]):.2f}%">{usd(v["prix_peg1"])}</span></span>
      <span class="zn-x">{pc(v["ecart_zone"], 1, True)}</span></div>''')
    body = hd("La méthode GARP · acheter", "La zone d'achat, ou la marge de sécurité",
              f"La zone d'achat est le cours pour lequel le PEG de long terme vaut {fr(H['zone_peg'], 0)} : croissance retenue × BPA NTM. Sous un PEG de {fr(H['zone_peg_forte'], 1)}, c'est la zone de forte sécurité.")
    body += f'''<div class="g c31 main"><div class="card a"><div class="rg-head"><span class="lab">Cours du {D["date_cours"]} face à la zone d'achat (vert foncé : PEG ≤ {fr(H['zone_peg_forte'], 1)} ; vert : PEG ≤ {fr(H['zone_peg'], 0)})</span><span class="lab">Au-dessus de la zone</span></div>{"".join(rows)}</div>
  <div class="g">{ul(["<b>Dans la zone</b> : achat en une fois.",
                    "<b>Au-dessus</b> : en deux fois, la moitié maintenant, la moitié sur repli ou après la publication suivante.",
                    "<b>Toujours dire</b> que l'on achète au-dessus de la zone, et pourquoi."])}
    {quote("graham_margin", "sm")}</div></div>'''
    return body, "Zones d'achat : " + VID() + " ; " + METH() + " ; citation " + I("graham_margin")


def s_vendre(ctx):
    body = hd("La méthode GARP · vendre", "Quand vendre : presque jamais, mais pas jamais",
              "Vendre est la décision la plus difficile. La règle : décider avant d'acheter ce qui ferait vendre, avec un indicateur, un seuil et une durée.")
    body += f'''<div class="g c3 main">
  <div class="card a"><span class="lab">Les trois raisons de Philip Fisher</span>{ul(["Une erreur d'analyse à l'achat.", "L'entreprise ne remplit plus les critères qui avaient justifié l'achat.", "Une bien meilleure occasion, rare, qui exige de l'argent."])}</div>
  <div class="card hl a"><span class="lab">Les règles mécaniques de la méthode</span>{ul([f"PEG de long terme au-dessus de {fr(H['vente_peg'], 0)} : vendre la moitié de la ligne.",
                                                                                                f"PEG repassé sous {fr(H['renfort_peg'], 1)} sans règle de vente déclenchée : renforcer.",
                                                                                                "Thèse cassée, par exemple « marge brute sous X % deux trimestres de suite » : tout vendre."])}</div>
  <div class="g">{quote("fisher_never", "sm")}{quote("buffett_forever", "sm", fr_only=True)}</div>
</div>'''
    return body, "Règles : " + METH() + " ; citations " + I("fisher_never", "buffett_forever")


def s_portefeuille(ctx):
    c = D["comparaison"]
    st = D["stress"]
    moteurs = "".join(f'<div class="ln-r a"><span><i class="dot" style="--c:{COUL[t]}"></i>{NOM[t]} · <small>{e(V[t]["theme"])}</small></span><b>20{NBSP}%</b></div>' for t in CINQ)
    chocs = [s for s in st if not s["scenario"].startswith("Tout en")]
    srows = table(["Choc (une ou plusieurs valeurs en scénario pessimiste)", "Portefeuille", "Nasdaq 100"],
                  [[e(s["scenario"]), pc(float(s["tcam_portefeuille"]), 1, True), pc(float(s["tcam_nasdaq100"]), 1, True)] for s in chocs], num=(1, 2), cls="stress")
    body = hd("La méthode GARP · assembler", "Des moteurs de croissance indépendants",
              "Le but n'est pas la diversification pour elle-même. C'est l'indépendance des moteurs de croissance : que la panne de l'un n'arrête pas les autres.")
    body += f'''<div class="g c23 main">
  <div class="g">
    <div class="card a"><span class="lab">Cinq lignes, cinq moteurs, poids égaux (hyp.)</span>{moteurs}</div>
    <div class="card stat a" style="--c:var(--gold)"><span class="v">{cnt(c["part_ia"]["ptf"] * 100, 0, NBSP + "%")}</span><span class="l">du portefeuille dépend de l'intelligence artificielle, contre {pc(c["part_ia"]["ndx"], 0)} pour le Nasdaq 100 : le principal risque de concentration.</span></div>
  </div>
  <div class="g"><span class="lab a">Tests de résistance : rendement annuel sur 4 ans</span>{srows}
    <p class="p m a">5 à 10 lignes, pas plus de deux par moteur. Si les scénarios des valeurs étaient indépendants, le portefeuille aurait {pc(c['p_sous_indice_central']['ptf'], 0)} de chances de finir sous l'indice et {pc(c['p_perte']['ptf'], 1)} de perdre de l'argent. Ils ne le sont pas tout à fait : ces chiffres flattent la diversification.</p></div>
</div>'''
    return body, "Données et tests : " + VID()


def s_biais(ctx):
    a, rd, mu = V["ADYEY"], V["RDDT"], V["MU"]
    bs = [("Ancrage", f"Adyen a coté {usd(a['plus_haut_52s'])} (ADR) il y a moins d'un an. Ce plus haut ne dit rien de la valeur d'aujourd'hui."),
          ("Peur de rater", f"Micron a pris {pc(mu['chg_52s'], 0, True)} en un an. Acheter parce que « ça monte », c'est acheter le cycle au sommet."),
          ("Récence", f"Reddit perd {pc(-rd['chg_ytd'], 0)} depuis janvier. Le dernier mouvement n'est pas une tendance."),
          ("Confirmation", "On lit ce qui conforte sa thèse. Remède : écrire la thèse adverse avant d'acheter."),
          ("Aversion à la perte", "On garde les perdants pour « se refaire » et on vend les gagnants trop tôt."),
          ("Excès de confiance", f"{fr(float(FI['spiva_2025']['valeur']), 0)}{NBSP}% des gérants professionnels ont fait moins bien que l'indice en 2025. Et vous ?")]
    cards = "".join(f'<div class="card a"><span class="lab">{n}</span><p class="p">{t}</p></div>' for n, t in bs)
    body = hd("La méthode GARP · se méfier de soi", "Les biais qui coûtent cher",
              "Le premier ennemi de l'investisseur est dans le miroir. Chaque biais a un exemple chiffré dans nos cinq valeurs.")
    body += f'<div class="g c32 main"><div class="g c3 lc1">{cards}</div><div class="g">{quote("munger_invert", "sm", avec_lecon=True)}</div></div>'
    return body, "Cours et variations : " + Z("ADYEY", "MU", "RDDT") + " ; SPIVA " + F("spiva_2025") + " ; citation " + I("munger_invert")


# ---------------------------------------------------------------- 5. enveloppes
def s_enveloppes(ctx):
    rows = [["Plafond de versements", f"{eur(fv('pea_plafond'))} ({e(FI['pea_plafond']['precision'].split(';')[0])})", "aucun", "aucun"],
            ["Ce qu'on peut y mettre", "actions de l'UE et de l'EEE, ETF éligibles", "tout : États-Unis, Asie, Amérique latine…", "fonds et ETF (unités de compte) proposés par le contrat"],
            ["Durée clé", f"{fr(fv('pea_duree'), 0)} ans", "aucune", f"{fr(fv('av_duree'), 0)} ans"],
            ["Impôt sur les gains, après la durée clé", f"{fr(fv('ps_2026'), 1)}{NBSP}% (prélèvements sociaux seuls)", f"{fr(fv('pfu_total'), 1)}{NBSP}% chaque année de cession", f"{fr(fv('av_taux_reduit'), 1)}{NBSP}% + {fr(fv('ps_av'), 1)}{NBSP}%, après abattement de {eur(fv('av_abattement_seul'))} ({eur(fv('av_abattement_couple'))} pour un couple)"],
            ["Avant la durée clé", f"retrait = clôture, gains au PFU de {fr(fv('pfu_total'), 1)}{NBSP}%", "—", f"{fr(fv('pfu_ir') + fv('ps_av'), 1)}{NBSP}%"],
            ["Frais typiques", "plafonnés par décret", "courtage et change", f"gestion de {e(FI['av_frais_gestion']['precision'].split(';')[0])} par an"],
            ["Transmission", "succession classique", "succession classique", f"{eur(fv('av_transmission'))} par bénéficiaire (versements avant 70 ans)"]]
    body = hd("Enveloppes · le tableau", "PEA, compte-titres, assurance-vie : le tableau",
              "Trois enveloppes, trois fiscalités. Le même placement ne rapporte pas la même somme selon l'endroit où on le loge.")
    body += table(["", "PEA", "Compte-titres", "Assurance-vie"], rows, cls="env w")
    body += '<p class="p m a">Barème 2026 : la CSG passe de 9,2 % à 10,6 %, ce qui porte la flat tax à 31,4 % ; l\'assurance-vie est exclue de la hausse.</p>'
    return body, "Fiscalité 2026 : " + F("pea_plafond", "pea_duree", "ps_2026", "pfu_total", "av_duree", "av_taux_reduit", "ps_av", "av_abattement_seul", "av_transmission", "av_frais_gestion")


def s_pea(ctx):
    elig = "".join(f'<div class="ln-r a"><span><i class="dot" style="--c:{COUL[t]}"></i>{NOM[t]}</span><b class="{"pos" if t == "ADYEY" else "neg"}">{"éligible (Pays-Bas)" if t == "ADYEY" else "non éligible"}</b></div>' for t in CINQ)
    fr_ = [("Ordre en ligne", f"{fr(fv('pea_frais_ordre'), 1)}{NBSP}% au maximum", FI["pea_frais_ordre"]["precision"]),
           ("Droits de garde", f"{fr(fv('pea_garde'), 1)}{NBSP}% par an au maximum", FI["pea_garde"]["precision"]),
           ("Ouverture", f"{eur(fv('pea_ouverture'))} au maximum", FI["pea_ouverture"]["precision"])]
    body = hd("Enveloppes · le PEA", "Le PEA : doux, mais européen",
              f"Après {fr(fv('pea_duree'), 0)} ans, les gains ne paient que {fr(fv('ps_2026'), 1)}{NBSP}% de prélèvements sociaux. Avant, un retrait clôture le plan et les gains paient la flat tax.")
    body += f'''<div class="g c3 main">
  <div class="g">{kv("Plafond de versements", cnt(fv("pea_plafond"), 0, NBSP + "€"), e(FI["pea_plafond"]["precision"].split(";")[0]), "var(--gold)")}
    {kv("Impôt après " + fr(fv("pea_duree"), 0) + " ans", cnt(fv("ps_2026"), 1, NBSP + "%"), "prélèvements sociaux seulement", "var(--gold)")}</div>
  <div class="g"><div class="card a"><span class="lab">Nos cinq valeurs dans un PEA ?</span>{elig}</div>
    <div class="card hl a"><p class="p"><b>L'astuce des ETF synthétiques.</b> Des ETF répliquent le Nasdaq 100 ou le S&amp;P 500 par un contrat d'échange tout en restant éligibles. {e(FI["etf_synthetiques"]["precision"].split(";")[-1].strip()).capitalize()}.</p></div></div>
  <div class="card a"><span class="lab">Frais plafonnés (décret n° 2020-95)</span>{"".join(f'<div class="ln-r"><span>{a}</span><b>{b}</b></div><p class="p m sm">{e(c)}</p>' for a, b, c in fr_)}
</div>
</div>'''
    return body, "PEA : " + F("pea_plafond", "pea_duree", "ps_2026", "pea_eligibilite", "pea_frais_ordre", "pea_garde", "pea_ouverture", "etf_synthetiques")


def s_cto(ctx):
    body = hd("Enveloppes · le compte-titres", f"Le compte-titres : le monde entier, à {fr(fv('pfu_total'), 1)}{NBSP}%",
              "Aucun plafond, aucune restriction : c'est là que vont NVIDIA, TSMC, Nu et Reddit. En contrepartie, chaque plus-value et chaque dividende paient la flat tax.")
    body += f'''<div class="g c3 main">
  <div class="g">{kv("Flat tax (PFU) 2026", cnt(fv("pfu_total"), 1, NBSP + "%"), e(FI["pfu_total"]["precision"]), "var(--gold)")}
    {kv("Option pour le barème", cnt(fv("cto_bareme"), 0, NBSP + "%"), "d'abattement sur les dividendes ; " + e(FI["cto_bareme"]["precision"].split(";")[0]), "var(--gold)")}</div>
  <div class="card a"><span class="lab">Les règles utiles</span>{ul([f"<b>Moins-values</b> : reportables {fr(fv('cto_moins_values'), 0)} ans, {e(FI['cto_moins_values']['precision'])}.",
                                                                  f"<b>Taxe sur les transactions financières</b> : {fr(fv('ttf'), 1)}{NBSP}% sur les achats d'actions françaises de plus d'1 Md€ de capitalisation ; {e(FI['ttf']['precision'].split(';')[1].strip())}.",
                                                                  f"<b>Change</b> : {e(FI['change_frais']['precision'])}."])}</div>
  <div class="card a"><span class="lab">Dividendes étrangers</span>{ul([f"<b>États-Unis</b> : retenue de {fr(fv('us_retenue'), 0)}{NBSP}% avec le formulaire W-8BEN ; {e(FI['us_retenue']['precision'])}.",
                                                                   "<b>TSMC (Taïwan)</b> : taux de retenue à vérifier auprès du courtier. Nos sources se contredisent.",
                                                                   "<b>Nu, Reddit, Adyen</b> : pas de dividende aujourd'hui."])}</div>
</div>'''
    return body, "Compte-titres : " + F("pfu_total", "cto_bareme", "cto_moins_values", "ttf", "change_frais", "us_retenue")


def s_av(ctx):
    body = hd("Enveloppes · l'assurance-vie", "L'assurance-vie : la championne de la durée et de la transmission",
              f"Après {fr(fv('av_duree'), 0)} ans, les gains bénéficient d'un abattement annuel et d'un taux réduit. Au décès, chaque bénéficiaire reçoit jusqu'à {eur(fv('av_transmission'))} hors succession.")
    body += f'''<div class="g c3 main">
  <div class="g">{kv("Avant " + fr(fv("av_duree"), 0) + " ans", cnt(fv("pfu_ir") + fv("ps_av"), 1, NBSP + "%"), e(FI["av_duree"]["precision"]), "var(--gold)")}
    {kv("Après " + fr(fv("av_duree"), 0) + " ans", f'{fr(fv("av_taux_reduit"), 1)}{NBSP}% + {fr(fv("ps_av"), 1)}{NBSP}%', f"impôt après abattement de {eur(fv('av_abattement_seul'))} ({eur(fv('av_abattement_couple'))} pour un couple) + prélèvements sociaux", "var(--gold)")}</div>
  <div class="card a"><span class="lab">Les règles utiles</span>{ul([f"<b>Taux réduit</b> : {fr(fv('av_taux_reduit'), 1)}{NBSP}% jusqu'à {eur(fv('av_seuil_primes'))} de versements, {e(FI['av_seuil_primes']['precision'])} ; {e(FI['av_taux_reduit']['precision'])}.",
                                                                  f"<b>Prélèvements sociaux</b> : {fr(fv('ps_av'), 1)}{NBSP}%, car {e(FI['ps_av']['precision'])}.",
                                                                  f"<b>Frais de gestion</b> : {e(FI['av_frais_gestion']['precision'])}."])}</div>
  <div class="card a"><span class="lab">Transmission</span><p class="p">{eur(fv("av_transmission"))} par bénéficiaire pour les versements faits avant 70 ans, {e(FI["av_transmission"]["precision"])}.</p>
    <p class="p m">Limite pour le stock picker : un contrat propose surtout des fonds et des ETF. Vérifiez la liste des supports avant de signer.</p></div>
</div>'''
    return body, "Assurance-vie : " + F("av_duree", "av_taux_reduit", "ps_av", "av_abattement_seul", "av_abattement_couple", "av_seuil_primes", "av_frais_gestion", "av_transmission")


def s_frais(ctx):
    ex = 2000
    rows = [["Courtage sur un PEA", f"{fr(fv('pea_frais_ordre'), 1)}{NBSP}% maximum par ordre en ligne", eur(ex * fv("pea_frais_ordre") / 100), F("pea_frais_ordre")],
            ["Change euro → dollar (compte-titres)", f"environ {fr(fv('change_frais'), 2)}{NBSP}%", eur(ex * fv("change_frais") / 100), F("change_frais")],
            ["Taxe sur les transactions financières", f"{fr(fv('ttf'), 1)}{NBSP}% (actions françaises > 1 Md€)", eur(ex * fv("ttf") / 100), F("ttf")],
            ["Droits de garde sur un PEA", f"{fr(fv('pea_garde'), 1)}{NBSP}% par an maximum", eur(ex * fv("pea_garde") / 100) + " par an", F("pea_garde")],
            ["Gestion d'une assurance-vie", e(FI["av_frais_gestion"]["precision"].split(";")[0]) + " par an", eur(ex * fv("av_frais_gestion") / 100) + " par an", F("av_frais_gestion")],
            ["Retenue sur dividende américain", f"{fr(fv('us_retenue'), 0)}{NBSP}% avec W-8BEN", "imputable", F("us_retenue")]]
    body = hd("Enveloppes · les frais", "Les frais qui comptent, ligne par ligne",
              f"Chaque frais semble petit. Pour un achat de {eur(ex)}, voici ce qu'ils coûtent. Les frais annuels, eux, se composent pendant des décennies.")
    body += table(["Frais", "Montant", f"Sur {eur(ex)}", "Sources"], rows, num=(2,), cls="w")
    body += f'<div class="g c2 main"><div class="card hl a"><p class="p"><b>La règle.</b> Peu d\'ordres, des lignes gardées longtemps, des frais annuels bas. Un frais ponctuel se paie une fois ; un frais annuel de 1 % se paie chaque année sur tout le capital.</p></div>{quote("munger_waiting", "sm")}</div>'
    return body, "Plafonds et barèmes : sources numérotées ci-dessus ; citation " + I("munger_waiting")


def s_ou(ctx):
    pv = H["plus_value_exemple"]
    fp = D["fisc_pv"]
    vmax = max(fp.values())
    bars = "".join(hbar(k, v / vmax, eur(v), "var(--pos)" if v == min(fp.values()) else ("var(--neg)" if v == vmax else "var(--gold)")) for k, v in sorted(fp.items(), key=lambda x: x[1]))
    rows = [[f'<span class="dot" style="--c:{COUL[t]}"></span>{NOM[t]}', "PEA" if t == "ADYEY" else "Compte-titres", "société néerlandaise" if t == "ADYEY" else "société hors Union européenne"] for t in CINQ]
    rows.append(['<span class="dot" style="--c:var(--ndx)"></span>ETF Nasdaq 100 synthétique', "PEA", "éligible par contrat d'échange"])
    rows.append(['<span class="dot" style="--c:var(--paper)"></span>ETF monde, horizon long', "Assurance-vie", "abattement après 8 ans et transmission"])
    body = hd("Enveloppes · le choix", "Quelle enveloppe pour quelle valeur ?",
              f"Sur {eur(pv)} de plus-value, l'écart entre la meilleure et la pire enveloppe atteint {eur(vmax - min(fp.values()))}.")
    body += f'''<div class="g c2 main">
  <div class="g">{table(["Valeur", "Enveloppe", "Pourquoi"], rows)}
    <p class="p m sm a">Ordre de remplissage proposé (hyp.) : le PEA d'abord, pour tout ce qui y est éligible ; le compte-titres pour les actions hors d'Europe ; l'assurance-vie pour le socle d'ETF de long terme et la transmission.</p></div>
  <div class="card a"><span class="lab">Impôts et prélèvements sur {eur(pv)} de plus-value, retrait total</span>{bars}</div>
</div>'''
    return body, "Calculs : " + F("ps_2026", "pfu_total", "av_taux_reduit", "ps_av", "av_abattement_seul", "av_abattement_couple") + " ; éligibilité " + F("pea_eligibilite", "etf_synthetiques")


# ---------------------------------------------------------------- 6. intérêts composés
def s_composes(ctx):
    ic = D["interets"]
    rows = []
    for l in ic:
        rows.append([f'<b>{pc(l["taux"], 0)}</b>', eur(l["valeur_10ans"]), eur(l["valeur_20ans"]), f'<b>{eur(l["valeur_30ans"])}</b>',
                     f'{fr(l["doublement_72"], 1)} <small>({fr(l["doublement_exact"], 1)})</small>'])
    huit = next(l for l in ic if abs(l["taux"] - 0.07) < 1e-9)
    body = hd("Intérêts composés · la mécanique", "Les intérêts composés : des gains sur les gains",
              f"Placés à 7 % par an, {eur(H['calc_capital'])} deviennent {eur(huit['valeur_30ans'])} en 30 ans. Les gains de l'année 30 dépassent à eux seuls la mise de départ.")
    body += f'''<div class="g c32 main"><div class="g">{table(["Rendement annuel", "10 ans", "20 ans", "30 ans", "Règle de 72 (exact)"], rows, num=(1, 2, 3, 4))}
    <div class="formula a">Règle de 72 : années pour doubler ≈ 72 ÷ rendement annuel (en %)</div></div>
  <div class="g">{quote("buffett_snowball", "sm")}
    <div class="card a" style="border-color:var(--neg)"><p class="p"><b>Une fausse citation.</b> « Les intérêts composés sont la huitième merveille du monde » n'est pas d'Einstein. Princeton University Press la classe parmi les citations « probablement pas d'Einstein ». {I("einstein_mythe")}</p></div></div></div>'''
    return body, f"Capital de {eur(H['calc_capital'])}, sans frais ni impôt (interets_composes.csv) ; " + I("buffett_snowball")


def s_calc(ctx):
    d = D["defauts"]
    fld = lambda id_, lab, val, mn, mx, st, unit: f'''<div class="fld a"><label for="c-{id_}-n">{lab}</label>
      <input type="range" id="c-{id_}" value="{val}" min="{mn}" max="{mx}" step="{st}" aria-label="{lab}"><span class="nb"><input type="number" id="c-{id_}-n" value="{val}" min="{mn}" max="{mx}" step="{st}" inputmode="decimal"><em>{unit}</em></span></div>'''
    body = hd("Intérêts composés · à vous", "À vous : la calculatrice")
    body += f'''<div class="calc main" id="calc">
  <div class="ctl card a">
    {fld("cap", "Capital de départ", int(d["capital"]), 0, 500000, 500, "€")}
    {fld("men", "Versement mensuel", int(d["mensuel"]), 0, 5000, 25, "€")}
    {fld("dur", "Durée", int(d["annees"]), 1, 40, 1, "ans")}
    {fld("ren", "Rendement brut annuel", d["rendement"] * 100, 0, 20, 0.5, "%")}
    {fld("fra", "Frais annuels", d["frais"] * 100, 0, 3, 0.05, "%")}
    {fld("inf", "Inflation annuelle", d["inflation"] * 100, 0, 6, 0.1, "%")}
    <div class="fld fw a"><label>Enveloppe</label><div class="seg" id="c-env" role="group" aria-label="Enveloppe"><button type="button" data-v="PEA" aria-pressed="true">PEA</button><button type="button" data-v="AV" aria-pressed="false">Assurance-vie</button><button type="button" data-v="CTO" aria-pressed="false">Compte-titres</button></div></div>
    <div class="fld fw a"><label>Foyer (assurance-vie)</label><div class="seg" id="c-foy" role="group" aria-label="Foyer"><button type="button" data-v="0" aria-pressed="true">Seul</button><button type="button" data-v="1" aria-pressed="false">Couple</button></div></div>
  </div>
  <div class="res">
    <div class="res-top a"><div><span class="lab">Valeur nette après impôts</span><span class="res-big" id="r-net">—</span></div>
      <div class="res-k"><span class="lab">En euros d'aujourd'hui</span><span id="r-reel">—</span></div></div>
    <div class="res-grid a">
      <div><span class="lab">Versé</span><b id="r-verse">—</b></div><div><span class="lab">Valeur brute</span><b id="r-brut">—</b></div>
      <div><span class="lab">Gains</span><b id="r-gain" class="pos">—</b></div><div><span class="lab">Coût des frais</span><b id="r-frais" class="neg">—</b></div>
      <div><span class="lab">Impôts</span><b id="r-imp" class="neg">—</b></div><div><span class="lab">Net ÷ versé</span><b id="r-mult">—</b></div>
    </div>
    <p class="warn" id="r-warn" hidden></p>
    <figure class="ch calc-ch a"><svg id="r-svg" viewBox="0 0 1000 250" role="img" aria-label="Évolution du capital"></svg>
      <figcaption class="leg"><span><i style="background:rgba(242,237,226,.28)"></i>Versements</span><span><i style="background:var(--gold)"></i>Valeur brute</span><span><i class="dash"></i>Sans frais</span></figcaption></figure>
    <div class="cmp-env a" id="r-cmp"></div>
  </div>
</div>'''
    return body, "Capitalisation mensuelle, frais prélevés sur l'encours, impôt d'un retrait total en fin de période ; dividendes non modélisés. Défauts : " + HYPS() + " ; fiscalité " + F("ps_2026", "pfu_total", "av_taux_reduit", "ps_av", "av_abattement_seul", "av_seuil_primes")


def s_tyrannie(ctx):
    fx = D["frais"]
    sans = fx[0]["sans_frais"]
    bars = hbar("Sans frais", 1.0, eur(sans), "var(--paper)")
    bars += "".join(hbar(f"{fr(x['frais'] * 100, 1)}{NBSP}% par an", x["valeur"] / sans, eur(x["valeur"]), ["var(--pos)", "var(--gold)", "var(--neg)"][i], f"−{pc(x['part_perdue'], 1)}") for i, x in enumerate(fx))
    b = D["bogle"]
    body = hd("Intérêts composés · les frais", "La tyrannie des frais composés",
              f"{eur(H['frais_capital'])} puis {eur(H['frais_versement'])} par mois pendant {fr(H['frais_duree'], 0)} ans, à {fr(H['frais_rendement'], 0)}{NBSP}% brut par an. Seule différence : les frais annuels.")
    body += f'''<div class="g c32 main"><div class="card a"><span class="lab">Capital final selon les frais annuels</span>{bars}
    <p class="p m a">Les frais se composent comme les gains, mais contre vous : {fr(fx[2]["frais"] * 100, 0)}{NBSP}% par an coûtent {eur(fx[2]["cout"])}, soit {pc(fx[2]["part_perdue"], 0)} du capital final.</p></div>
  <div class="g">{quote("bogle_costs", "sm")}
    <div class="card a"><p class="p">L'exemple de Bogle : {fr(b["r"] * 100, 0)}{NBSP}% brut, {fr(b["f"] * 100, 0)}{NBSP}% de frais, {fr(b["n"], 0)} ans. L'épargnant perd entre <b class="neg">{pc(b["part_perdue_soustraction"], 0)}</b> et <b class="neg">{pc(b["part_perdue"], 0)}</b> de son capital final selon la convention de calcul : « près des deux tiers ».</p></div></div></div>'''
    return body, "Calculs : frais.csv, " + HYPS() + " ; " + I("bogle_costs")


def s_impact_env(ctx):
    env = D["enveloppes"]
    d = D["defauts"]
    vmax = max(x["net"] for x in env)
    cols = {"PEA": "var(--pos)", "AV": "var(--gold)", "AV (couple)": "var(--gold)", "CTO": "var(--neg)"}
    noms = {"PEA": "PEA", "AV": "Assurance-vie (seul)", "AV (couple)": "Assurance-vie (couple)", "CTO": "Compte-titres"}
    bars = "".join(hbar(noms[x["enveloppe"]], x["net"] / vmax, eur(x["net"]), cols[x["enveloppe"]], f"impôts {eur(x['impot'])} · {pc(x['taux_effectif'], 1)} des gains") for x in env)
    ecart = env[0]["net"] - env[-1]["net"]
    body = hd("Intérêts composés · l'enveloppe", f"Même placement, trois enveloppes : {eur(ecart)} d'écart",
              f"Les paramètres par défaut de la calculatrice : {eur(d['capital'])} puis {eur(d['mensuel'])} par mois, {fr(d['annees'], 0)} ans, {fr(d['rendement'] * 100, 0)}{NBSP}% brut, {fr(d['frais'] * 100, 1)}{NBSP}% de frais. Seule change l'enveloppe.")
    body += f'''<div class="g c32 main"><div class="card a"><span class="lab">Valeur nette après impôts, retrait total au bout de {fr(d["annees"], 0)} ans · versé : {eur(env[0]["verse"])} · valeur brute : {eur(env[0]["valeur"])}</span>{bars}</div>
  <div class="g">{ul(["<b>À frais égaux.</b> En pratique, l'assurance-vie ajoute souvent des frais sur les supports, ce qui réduit son avantage.",
                    "<b>Dividendes non modélisés.</b> Sur un compte-titres, ils sont taxés chaque année, ce qui freine la capitalisation.",
                    "<b>Le PEA gagne</b>… mais n'accepte ni NVIDIA, ni TSMC, ni Nu, ni Reddit."])}</div></div>'''
    return body, "Calculs : enveloppes.csv ; " + HYPS() + " ; fiscalité " + F("ps_2026", "pfu_total", "av_taux_reduit", "ps_av", "av_abattement_seul", "av_abattement_couple")


def s_temps(ctx):
    t1, t2 = D["temps"]["temps_age_tot"], D["temps"]["temps_age_tard"]
    body = hd("Intérêts composés · le temps", "Le temps plutôt que le timing",
              f"Deux épargnants placent {eur(H['temps_versement'])} par mois à {fr(D['defauts']['rendement'] * 100, 0)}{NBSP}% brut ({fr(D['defauts']['frais'] * 100, 1)}{NBSP}% de frais). L'un commence à {fr(t1['age'], 0)} ans, l'autre à {fr(t2['age'], 0)} ans. Les deux s'arrêtent à {fr(H['temps_age_fin'], 0)} ans.")
    body += f'''<div class="g c32 main"><figure class="ch a">{svg_temps()}</figure>
  <div class="g">
    {kv(f"Départ à {fr(t1['age'], 0)} ans", cnt(t1["valeur"], 0, NBSP + "€"), f"pour {eur(t1['verse'])} versés", "var(--gold)")}
    {kv(f"Départ à {fr(t2['age'], 0)} ans", cnt(t2["valeur"], 0, NBSP + "€"), f"pour {eur(t2['verse'])} versés", "var(--ndx)")}
    <div class="card hl a"><p class="p">Dix ans d'avance et {eur(t1["verse"] - t2["verse"])} de versements en plus multiplient le capital final par <b class="gold">{fr(t1["valeur"] / t2["valeur"], 1)}</b>. Le meilleur moment pour commencer était hier ; le second, aujourd'hui.</p></div>
  </div></div>'''
    return body, "Calcul : " + HYPS() + " ; avant impôts"


# ---------------------------------------------------------------- 7. grands investisseurs
def s_lynch(ctx):
    L = D["lynch"]
    body = hd("Grands investisseurs · Peter Lynch", "Peter Lynch : la croissance au juste prix",
              f"De {L['annee_debut']['valeur']} à {L['annee_fin']['valeur']}, il fait passer le fonds Magellan de Fidelity de {fr(float(L['encours_debut']['valeur']), 0)}{NBSP}M$ à {md(float(L['encours_fin']['valeur']), 0)}. L'inventeur du PEG et des six catégories.")
    body += f'''<div class="g c3 main">
  <div class="g">{kv("Rendement annuel moyen", cnt(float(L["rendement_annuel"]["valeur"]), 1, NBSP + "%"), f"{L['annee_debut']['valeur']}-{L['annee_fin']['valeur']}", "var(--gold)")}
    <div class="card a"><span class="lab">Ses idées</span>{ul(["Investir dans ce que l'on comprend.", "Classer avant de valoriser : six catégories.", "Payer la croissance à son prix : le PEG.", "Rester investi : le temps fait le travail."])}</div></div>
  {quote("lynch_know", "", avec_lecon=True)}
  {quote("lynch_corrections", "", avec_lecon=True)}
</div>'''
    return body, "Palmarès " + LYN()


def s_buffett(ctx):
    body = hd("Grands investisseurs · Warren Buffett", "Warren Buffett : la qualité d'abord",
              "Élève de Graham, Buffett a appris de Munger à préférer une entreprise exceptionnelle à une affaire bon marché. Le GARP lui doit son critère de qualité.")
    body += f'''<div class="g c2 main q-grid">
  {quote("buffett_wonderful", "sm", avec_lecon=True)}{quote("buffett_price", "sm", avec_lecon=True)}
  {quote("buffett_fearful", "sm", avec_lecon=True)}{quote("buffett_forever", "sm", avec_lecon=True)}
</div>'''
    return body, "Citations : sources numérotées sous chaque citation"


def s_munger(ctx):
    body = hd("Grands investisseurs · Charlie Munger", "Charlie Munger : inverser, puis attendre",
              "Associé de Buffett pendant 45 ans, Munger raisonnait à l'envers : chercher d'abord comment échouer, pour l'éviter. Et laisser le temps faire le reste.")
    body += f'''<div class="g c2 main">{quote("munger_invert", "", avec_lecon=True)}{quote("munger_waiting", "", avec_lecon=True)}</div>'''
    return body, "Citations : sources numérotées sous chaque citation"


def s_graham(ctx):
    body = hd("Grands investisseurs · Benjamin Graham", "Benjamin Graham : M. Marché et la marge de sécurité")
    body += f'''<div class="g c3 main">{quote("graham_mrmarket", "sm", avec_lecon=True)}{quote("graham_margin", "sm", avec_lecon=True)}{quote("graham_voting", "sm", avec_lecon=True)}</div>'''
    return body, "Attribution corrigée : la formule de la machine à voter et à peser est de Buffett, qui résumait les idées de Graham et Dodd ; elle est souvent prêtée à Graham. Sources sous chaque citation"


def s_fisher(ctx):
    body = hd("Grands investisseurs · Fisher et Smith", "Philip Fisher et Terry Smith : acheter la qualité, puis attendre",
              "Fisher a appris à Buffett l'enquête de terrain sur la croissance. Terry Smith, fondateur de Fundsmith, a résumé la méthode en trois verbes.")
    body += f'''<div class="g c2 main">{quote("fisher_never", "", avec_lecon=True)}{quote("smith_3steps", "", avec_lecon=True)}</div>'''
    return body, "Citations : sources numérotées sous chaque citation"


def s_bogle(ctx):
    body = hd("Grands investisseurs · les contradicteurs", "John Bogle et Howard Marks : les contradicteurs utiles",
              "Bogle, fondateur de Vanguard, a démocratisé le fonds indiciel. Marks, cofondateur d'Oaktree, rappelle qu'avoir raison ne suffit pas : il faut avoir raison contre le consensus.")
    body += f'''<div class="g c3 main">{quote("bogle_haystack", "", avec_lecon=True)}{quote("bogle_costs", "", avec_lecon=True)}{quote("marks_second", "", avec_lecon=True)}</div>'''
    return body, "Citations : sources numérotées sous chaque citation"


def s_synthese(ctx):
    rows = [["Peter Lynch", "PEG, six catégories, connaître ce que l'on possède", "PEG ≤ " + fr(H["garp_peg_max"], 1) + ", classement avant valorisation, thèse écrite"],
            ["Warren Buffett", "Qualité à prix correct, prix ≠ valeur", "ROIC ≥ " + fr(H["garp_rentabilite_min"], 0) + NBSP + "%, dilution ≤ " + fr(H["garp_dilution_max"], 0) + NBSP + "%"],
            ["Charlie Munger", "Inverser, attendre", "Liste des risques avant achat, peu d'ordres"],
            ["Benjamin Graham", "M. Marché, marge de sécurité", "Zone d'achat à PEG " + fr(H["zone_peg"], 0) + " et " + fr(H["zone_peg_forte"], 1) + ", trésorerie nette"],
            ["Philip Fisher", "Croissance de qualité, vendre presque jamais", "Trois raisons de vendre, marge nette ≥ " + fr(H["garp_marge_nette_min"], 0) + NBSP + "%"],
            ["Terry Smith", "Bonnes entreprises, pas trop cher, ne rien faire", "Grille de qualité, rééquilibrage seulement à PEG " + fr(H["vente_peg"], 0)],
            ["John Bogle", "Les frais et l'indice", "Comparer chaque année au Nasdaq 100 ; frais bas"],
            ["Howard Marks", "Pensée de second niveau", "Ce que le prix suppose ; croissance retenue plus prudente que le consensus"]]
    body = hd("Grands investisseurs · la synthèse", "Ce que chacun apporte à la grille",
              "La méthode de cette formation n'invente rien. Elle assemble les leçons des plus grands en règles chiffrées.")
    body += table(["Investisseur", "Idée maîtresse", "Traduction dans la méthode"], rows, cls="w")
    return body, HYPS() + " ; " + METH()


# ---------------------------------------------------------------- 8. passer à l'action
def s_routine(ctx):
    check = ["Puis-je expliquer l'activité en deux phrases ?", "Dans quelle catégorie de Lynch ?", "Quelle croissance durable du BPA, plus prudente que le consensus ?",
             "Que retire le BPA non-GAAP ?", "Quel FCF, quel capex ?", f"ROIC (ou ROE) au-dessus de {fr(H['garp_rentabilite_min'], 0)}{NBSP}% ?",
             "Trésorerie nette ? Dilution ?", "PEG de long terme et zone d'achat ?", "Quelle enveloppe ?", "Quelle règle de vente, écrite avant d'acheter ?"]
    ol = "".join(f'<li class="a"><span class="num">{i + 1:02d}</span>{x}</li>' for i, x in enumerate(check))
    body = hd("Passer à l'action · la routine", "La check-list et la routine",
              "Dix questions avant chaque achat. Puis une routine légère : l'essentiel se joue quatre fois par an, aux publications.")
    body += f'''<div class="g c2 main"><div class="card a"><span class="lab">Avant d'acheter : dix questions</span><ol class="chk">{ol}</ol></div>
  <div class="g">
    <div class="card a"><span class="lab">Chaque mois</span><p class="p">Un versement programmé. Ne pas regarder les cours chaque jour : M. Marché n'a rien d'utile à dire.</p></div>
    <div class="card a"><span class="lab">À chaque publication trimestrielle</span><p class="p">Résultats face au consensus, révisions, KPI de l'équation du chiffre d'affaires, thèse intacte ? Règles de vente déclenchées ?</p></div>
    <div class="card a"><span class="lab">Une fois par an</span><p class="p">Recalculer les PEG ; rééquilibrer (au-dessus de {fr(H["vente_peg"], 0)}, alléger ; sous {fr(H["renfort_peg"], 1)}, renforcer) ; comparer au Nasdaq 100 ; vérifier les dates des {fr(fv("pea_duree"), 0)} et {fr(fv("av_duree"), 0)} ans ; imputer les moins-values.</p></div>
  </div></div>'''
    return body, METH() + " ; " + HYPS()


def s_quiz(ctx):
    n, ts = R["NVDA"], R["TSM"]
    c = D["comparaison"]
    peg = c["pe_ntm"]["ptf"] / c["g_lt"]["ptf"]
    fx2 = D["frais"][2]
    qs = [(f"NVIDIA : {md(n['resultat_net'])} de résultat net, {fr(n['actions_moyennes'] / 1000, 2)} milliards d'actions. Son BPA ?",
           [usd(n["bpa_recalcule"]), usd(n["bpa_recalcule"] * 10, 1), usd(n["bpa_recalcule"] / 10)], 0, "BPA = résultat net ÷ nombre moyen d'actions."),
          (f"P/E de {fr(c['pe_ntm']['ptf'], 1)}, croissance du BPA de {fr(c['g_lt']['ptf'], 1)} % par an. Le PEG ?",
           [fr(1 / peg, 2), fr(peg, 2), fr(c["peg_lt"]["ndx"], 2)], 1, "PEG = P/E ÷ croissance en points."),
          (f"TSMC : flux opérationnel {md(ts['flux_operationnel'])}, capex {md(ts['capex'])}. Son FCF ?",
           [md(ts["flux_operationnel"] + ts["capex"]), md(ts["fcf"]), md(ts["flux_operationnel"])], 1, "FCF = flux opérationnel − capex."),
          ("Laquelle de ces actions peut entrer dans un PEA ?", ["NVIDIA", "Nu", "Adyen"], 2, "Adyen est une société néerlandaise : Union européenne."),
          (f"Plus-value de {eur(H['plus_value_exemple'])} dans un PEA de plus de {fr(fv('pea_duree'), 0)} ans : combien d'impôts et prélèvements ?",
           [eur(D["fisc_pv"]["Compte-titres"]), eur(0), eur(D["fisc_pv"]["PEA (après 5 ans)"])], 2, f"Seulement les prélèvements sociaux : {fr(fv('ps_2026'), 1)} %."),
          ("À 8 % par an, en combien de temps un capital double-t-il ?", [f"{fr(72 / 8, 0)} ans", f"{fr(100 / 8, 1)} ans", "6 ans"], 0, "Règle de 72 : 72 ÷ 8 = 9."),
          (f"Une cyclique affiche un P/E de {fr(V['MU']['pe_f1'], 1)} au sommet de son cycle. Pour Lynch, c'est…", ["une aubaine", "un possible signal de vente", "un PEG de 0,1"], 1, "Au sommet, les bénéfices sont au plus haut et vont baisser."),
          (f"{fr(fx2['frais'] * 100, 0)} % de frais par an pendant {fr(H['frais_duree'], 0)} ans : quelle part du capital final disparaît ?",
           [pc(fx2["frais"], 0), pc(fx2["part_perdue"], 0), pc(0.6, 0)], 1, "Les frais se composent, comme les gains."),
          ("Un ETF qui suit le Nasdaq 100 peut-il entrer dans un PEA ?", ["Jamais", "Oui, en synthétique", "S'il est américain"], 1, "Le swap échange la performance d'un panier européen contre celle du Nasdaq 100."),
          ("Selon Vanguard (2023), investir en une fois a battu un DCA de trois mois dans quelle part des cas ?",
           [pc(1 - float(D["horizon"]["dca_vanguard_2023"]["valeur"]) / 100, 0), "50 %", pc(float(D["horizon"]["dca_vanguard_2023"]["valeur"]) / 100, 0)], 2, "Le marché monte plus souvent qu'il ne baisse : l'argent investi tôt travaille plus longtemps.")]
    cards = []
    for i, (q, opts, ok, why) in enumerate(qs):
        bt = "".join(f'<button type="button" class="opt{" good" if j == ok else ""}" data-ok="{1 if j == ok else 0}">{o}</button>' for j, o in enumerate(opts))
        cards.append(f'<div class="card qz-q a"><p class="p"><span class="num gold">{i + 1:02d}</span> {q}</p><div class="opts">{bt}</div><p class="why">{why}</p></div>')
    body = hd("Passer à l'action · testez-vous", "Testez-vous : dix questions",
              'Cliquez sur une réponse. <span class="score" id="qz-score"></span>')
    body += f'<div class="g c5 lc1 main qz">{"".join(cards)}</div>'
    return body, "Données des diapositives précédentes"


GLOSS = [("Action", "Part du capital d'une société : droit aux bénéfices, aux dividendes et au vote."),
         ("ADR", "Certificat coté aux États-Unis qui représente des actions étrangères (TSMC ; Adyen, 1 ADR = 1/100 d'action)."),
         ("Assurance-vie", "Enveloppe d'épargne : fonds en euros et unités de compte ; fiscalité douce après 8 ans."),
         ("Bêta", "Sensibilité d'une action aux mouvements du marché (1 = comme l'indice)."),
         ("Capitalisant", "ETF ou fonds qui réinvestit les dividendes au lieu de les verser."),
         ("BPA", "Bénéfice par action : résultat net ÷ nombre moyen d'actions."),
         ("BPA non-GAAP", "BPA « ajusté », hors éléments jugés exceptionnels par la société."),
         ("Capex", "Investissements dans les actifs physiques : usines, machines, serveurs."),
         ("Capitalisation", "Cours × nombre d'actions : la valeur boursière des fonds propres."),
         ("Capitaux propres", "Ce qui revient aux actionnaires au bilan : actifs moins dettes."),
         ("Consensus", "Moyenne des prévisions des analystes (BPA, chiffre d'affaires)."),
         ("Cyclique", "Société dont les profits suivent le cycle économique ou un cycle de prix."),
         ("DCA", "Dollar-cost averaging : investir une somme fixe à intervalles réguliers, quel que soit le cours."),
         ("Dilution", "Hausse du nombre d'actions, qui partage le bénéfice en plus de parts."),
         ("Distribuant", "ETF ou fonds qui verse les dividendes reçus, en général une à quatre fois par an."),
         ("Dividende", "Part du bénéfice versée aux actionnaires."),
         ("EBIT", "Résultat opérationnel : avant intérêts et impôt."),
         ("EBITDA", "EBIT avant dotations aux amortissements ; ignore le coût du capex."),
         ("Écart de suivi", "Différence de performance entre un ETF et son indice, frais compris."),
         ("Épargne de précaution", "Réserve disponible immédiatement pour les imprévus, avant tout placement risqué."),
         ("ETF", "Fonds coté qui réplique un indice, pour des frais faibles."),
         ("FCF", "Flux de trésorerie disponible : flux opérationnel − capex."),
         ("Flat tax (PFU)", "Prélèvement forfaitaire unique : 31,4 % en 2026 (12,8 % + 18,6 %)."),
         ("Frais courants (TER)", "Frais annuels d'un fonds, prélevés sur son actif : on ne les voit pas, on les subit."),
         ("GARP", "Growth at a reasonable price : la croissance à un prix raisonnable."),
         ("Horizon", "Durée pendant laquelle l'argent peut rester investi sans en avoir besoin."),
         ("Investissement en une fois", "Lump sum : placer toute la somme disponible d'un coup."),
         ("Marge brute", "Ventes moins coût direct des produits, en % des ventes."),
         ("Marge opérationnelle", "Résultat opérationnel en % des ventes."),
         ("Marge nette", "Résultat net en % des ventes."),
         ("NTM", "Next twelve months : les 12 prochains mois."),
         ("P/B", "Cours ÷ fonds propres par action ; multiple des banques."),
         ("P/E (PER)", "Cours ÷ BPA : combien on paie un dollar de bénéfice."),
         ("P/S", "Capitalisation ÷ chiffre d'affaires."),
         ("PEA", "Plan d'épargne en actions : actions européennes, 18,6 % de prélèvements après 5 ans."),
         ("PEG", "P/E ÷ croissance annuelle du BPA en points ; 1 = croissance payée à son prix."),
         ("PRIIPs", "Règlement européen qui impose un document d'informations clés (DIC) : sans lui, pas de vente aux particuliers."),
         ("Prélèvements sociaux", "CSG, CRDS et prélèvement de solidarité : 18,6 % en 2026 (17,2 % en assurance-vie)."),
         ("Rachat d'actions", "La société rachète et annule ses actions : le BPA monte."),
         ("Rang Zacks", "Note de 1 (achat fort) à 5 (vente forte) fondée sur les révisions de BPA."),
         ("Réplication physique", "L'ETF détient les actions de l'indice, toutes ou un échantillon."),
         ("Réplication synthétique", "L'ETF détient un autre panier et échange sa performance contre celle de l'indice (swap)."),
         ("ROE", "Résultat net ÷ capitaux propres moyens."),
         ("ROIC", "Résultat opérationnel après impôt ÷ capital investi moyen."),
         ("Take rate", "Commission prélevée sur le volume traité (Adyen : CA net ÷ volume)."),
         ("TCAM", "Taux de croissance annuel moyen : (fin ÷ début)^(1/n) − 1."),
         ("Trésorerie nette", "Trésorerie moins dette financière."),
         ("TTF", "Taxe sur les transactions financières : 0,4 % sur les achats d'actions françaises de plus d'1 Md€."),
         ("UCITS (OPCVM)", "Cadre européen des fonds : diversification, dépositaire, limites sur les contreparties."),
         ("Unités de compte", "Supports d'une assurance-vie investis en fonds, ETF ou actions, sans garantie du capital."),
         ("Valeur d'entreprise", "Capitalisation + dette − trésorerie."),
         ("Valeur liquidative", "Valeur des actifs d'un fonds par part, calculée chaque jour."),
         ("W-8BEN", "Formulaire américain qui ramène la retenue sur dividendes de 30 % à 15 % pour un résident français.")]


def s_glossaire(part, nparts=3):
    def fn(ctx):
        per = math.ceil(len(GLOSS) / nparts)
        items = GLOSS[(part - 1) * per:part * per]
        dl = "".join(f'<div class="gl a"><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a, b in items)
        rng = f"{items[0][0][0]} à {items[-1][0][0]}"
        body = hd("Passer à l'action · le glossaire", f"Glossaire ({part}/{nparts}) : de {rng}", "")
        body += f'<dl class="gloss main">{dl}</dl>'
        return body, "Taux du glossaire : " + F("pfu_total", "ps_2026", "ps_av", "ttf", "us_retenue")
    return fn


def s_sources(part, nparts):
    def fn(ctx):
        lst = S.liste
        per = math.ceil(len(lst) / nparts)
        chunk = list(enumerate(lst))[part * per:(part + 1) * per]
        li = "".join(f'<li><span class="num">[{i + 1}]</span> <a href="{e(u.replace(" ", "%20"))}" target="_blank" rel="noopener">{e(t)}</a></li>' if u else f'<li><span class="num">[{i + 1}]</span> {e(t)}</li>' for i, (t, u) in chunk)
        body = hd("Passer à l'action · les sources", f"Sources ({part + 1}/{nparts})",
                  "Chaque chiffre clé renvoie à ces sources numérotées. Les pages Zacks sont datées du 13/10/2026 ; les opinions y sont des opinions datées." if part == 0 else "")
        body += f'<ol class="srcs main">{li}</ol>'
        return body, "Liens consultés le 13/10/2026 ; certaines pages de première main étaient inaccessibles depuis l'environnement de calcul et ont été vérifiées par la recherche web"
    return fn


def s_fin(ctx):
    pts = ["Une action est une part d'entreprise : son cours suit le BPA, à un P/E près.",
           "Les comptes disent la qualité : marges, FCF, ROIC, trésorerie, dilution.",
           "Le PEG mesure le prix de la croissance ; méfiez-vous des croissances de pic.",
           "Une grille écrite, une zone d'achat, des règles de vente décidées à l'avance.",
           "PEA d'abord quand c'est possible ; les impôts et les frais se composent aussi.",
           "Le temps est le premier moteur. Commencez tôt, restez investi, comparez-vous à l'indice."]
    corr = [f"BPA 2028 de NVIDIA : {usd(V['NVDA']['bpa_f2'])} (comparateur Zacks) contre {usd(float(D['nvda_zacks']['bpa_fy2028_fiche']))} (fiche Zacks) le même jour. La formation retient le premier, comme le modèle.",
            f"Plus haut de 52 semaines de NVIDIA : {usd(V['NVDA']['plus_haut_52s'])} (comparateur Zacks) ; la fiche affiche un autre chiffre. La diapositive sur le risque utilise le comparateur pour les cinq valeurs.",
            "La formule « machine à voter, machine à peser » est attribuée à Buffett, d'après Graham ; la « huitième merveille » n'est pas d'Einstein.",
            "Retenue à la source de Taïwan sur les dividendes de TSMC : sources contradictoires, à vérifier."]
    body = hd("Fin", "Ce qu'il faut retenir", "")
    body += f'''<div class="g c2 main"><div>{ul(pts, "ck")}</div>
  <div class="g"><div class="card a"><span class="lab">Données signalées et corrigées</span>{ul(corr, "sm")}</div>
  <div class="card hl a"><p class="p"><b>* La Gazette du PEG</b> est un titre fictif : il ne correspond à aucune publication existante. Ce diaporama est une analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé. Les performances passées ne préjugent pas des performances futures ; investir en actions expose à une perte en capital.</p></div></div></div>'''
    return body, f"Formation du {D['date']}, cours du {D['date_cours']}"



# ---------------------------------------------------------------- 1. objectifs et horizon (suite) et 7. ETF : diapositives sans données externes
def s_noyau(ctx):
    nmin, nmax = H["noyau_min"], H["noyau_max"]
    ex = 10000
    body = hd("Objectifs et horizon · l'allocation", "Le noyau et les satellites",
              "Un débutant n'a pas d'historique qui prouve qu'il bat l'indice. Le noyau du portefeuille suit donc l'indice ; le stock picking occupe les satellites, une part qu'on accepte de voir sous-performer.")
    body += f'''<div class="g c2 main">
  <div class="card a"><span class="lab">Exemple pour {eur(ex)} (hyp.)</span>
    <div class="ns"><div class="ns-n" style="flex:{nmax - 10:.0f}"><b>{eur(ex * (nmax - 10) / 100)}</b><span>noyau : un ou deux ETF larges (monde, Nasdaq 100)</span></div>
    <div class="ns-s" style="flex:{110 - nmax:.0f}"><b>{eur(ex * (110 - nmax) / 100)}</b><span>satellites : 5 actions GARP de {eur(ex * (110 - nmax) / 100 / 5)}</span></div></div>
    {ul([f"<b>Noyau</b> : de {fr(nmin, 0)} à {fr(nmax, 0)} % du portefeuille (hyp.). Il garantit de faire à peu près comme le marché.",
         "<b>Satellites</b> : le reste, en actions choisies avec la grille GARP. C'est là que se joue la surperformance… ou la sous-performance.",
         "<b>Une fois par an</b>, comparer les satellites à l'indice. Trois ans de retard ? Réduire leur part."])}</div>
  <div class="g">
    <div class="card hl a"><p class="p"><b>Le portefeuille de cette formation est 100 % satellites.</b> Cinq valeurs, aucun ETF : c'est le choix d'un investisseur qui accepte l'écart à l'indice. Sur 12 mois, il a fait {fr(float(D["retro"]["1an"]["portefeuille_poids_egaux"]), 1, True)}{NBSP}%, contre {fr(float(D["retro"]["1an"]["QQQ"]), 1, True)}{NBSP}% pour le Nasdaq 100.</p></div>
    {quote("bogle_haystack", "sm")}
  </div>
</div>'''
    return body, HYPS() + " ; rétroviseur " + VID()


def s_dca_ex(ctx):
    dc = D["dca"]
    noms = {"baisse_puis_rebond": "Le marché baisse, puis rebondit", "hausse_reguliere": "Le marché monte régulièrement"}
    cards = []
    for sc in ("baisse_puis_rebond", "hausse_reguliere"):
        d = dc[sc]
        pmax = max(d["prix"])
        barres = "".join(f'<div class="px-b"><i style="height:{x / pmax * 100:.1f}%"></i><span>{fr(x, 0)}</span><small>m{i + 1}</small></div>' for i, x in enumerate(d["prix"]))
        gagnant = "DCA" if d["valeur_dca"] > d["valeur_lump"] else "En une fois"
        cards.append(f'''<div class="card a"><span class="lab">{noms[sc]}</span><div class="px">{barres}</div>
      <div class="ln-r"><span>Parts achetées en une fois (mois 1)</span><b>{fr(d["parts_lump"], 1)}</b></div>
      <div class="ln-r"><span>Parts achetées en DCA ({eur(d["tranche"])} par mois)</span><b>{fr(d["parts_dca"], 1)}</b></div>
      <div class="ln-r"><span>Coût moyen DCA · prix moyen</span><b>{fr(d["cout_moyen_dca"], 2)} · {fr(d["prix_moyen"], 2)}</b></div>
      <div class="ln-r"><span>Valeur finale : en une fois · DCA</span><b>{eur(d["valeur_lump"])} · {eur(d["valeur_dca"])}</b></div>
      <p class="p"><b class="{"pos" if gagnant == "DCA" else "gold"}">{gagnant} gagne</b> : {eur(abs(d["valeur_dca"] - d["valeur_lump"]))} d'écart.</p></div>''')
    body = hd("Objectifs et horizon · le DCA en pratique", "Le DCA en pratique : deux scénarios",
              f"{eur(H['dca_montant'])} à investir : tout au premier mois, ou {eur(H['dca_montant'] / H['dca_mois'])} par mois pendant {fr(H['dca_mois'], 0)} mois. Le DCA achète plus de parts quand le prix baisse : son coût moyen est toujours inférieur ou égal au prix moyen.")
    body += f'<div class="g c2 main">{"".join(cards)}</div>'
    body += '<p class="p m a">Conclusion : le DCA protège du mauvais moment, au prix d\'un rendement moyen plus faible quand le marché monte. Pour une épargne prélevée chaque mois sur le salaire, la question ne se pose pas : le versement programmé est du DCA naturel.</p>'
    return body, "Exemple pédagogique (data/dca_exemple.csv) ; " + HYPS()


def s_etf_contenu(ctx):
    q = D["etf_us"]["QQQ"]
    pos = D["qqq"][:10]
    vmax = float(pos[0]["poids_pct"])
    mien = {"NVDA", "TSM", "NU", "RDDT", "ADYEY"}
    bars = "".join(hbar(f'{x["nom"]}', float(x["poids_pct"]) / vmax, f'{fr(float(x["poids_pct"]), 2)}{NBSP}%',
                        COUL.get(x["ticker"], "var(--ndx)") if x["ticker"] in mien or x["ticker"] in ("MU",) else "var(--ndx)") for x in pos)
    top10 = sum(float(x["poids_pct"]) for x in pos)
    body = hd("Les ETF · le contenu", "Ce que contient un ETF Nasdaq 100",
              f"L'ETF américain QQQ réplique le Nasdaq 100 : {q['nombre_lignes']} lignes pour {fr(float(q['frais_pct']), 2)}{NBSP}% de frais par an. Ses dix premières lignes pèsent {fr(float(q['poids_10_premieres_pct']), 1)}{NBSP}% du fonds.")
    body += f'''<div class="g c32 main"><div class="card tight a"><span class="lab">Les dix premières lignes de QQQ, positions au 04/09/2026</span>{bars}
    <p class="p m">Total des dix premières : {fr(top10, 1)}{NBSP}% (Alphabet compte deux fois : actions A et C).</p></div>
  <div class="g">{ul([f"<b>Une seule de nos cinq valeurs</b> est dans le Nasdaq 100 : NVIDIA, première ligne à {fr(float(pos[0]['poids_pct']), 2)}{NBSP}%. TSMC, Nu et Reddit sont cotées au NYSE ; Adyen à Amsterdam.",
                    f"<b>Un indice achète aussi les cycliques au sommet</b> : Micron pèse {fr(float(D['qqq'][3]['poids_pct']), 2)}{NBSP}% après {pc(V['MU']['chg_52s'], 0, True)} en un an.",
                    "<b>Pondération par la capitalisation</b> : plus une action monte, plus elle pèse. L'indice renforce ses gagnants, sans jamais regarder le prix.",
                    f"<b>Encours de QQQ</b> : {md(float(q['encours_musd']), 0)}."])}</div></div>'''
    return body, "Positions et métriques de QQQ : " + S.refs([("Zacks Investment Research : fiche QQQ, positions au 04/09/2026 (servi le 13/10/2026)", "https://www.zacks.com/stock/quote/QQQ")]) + " ; Micron : " + Z("MU")



# ---------------------------------------------------------------- 1. objectifs et horizon et 7. ETF : diapositives sourcées
def HZ(i):
    return D["horizon"][i]


def HZv(i):
    return float(D["horizon"][i]["valeur"])


def HZS(*ids):
    paires = []
    for i in ids:
        r = D["horizon"][i]
        paires += [(r["source_titre"], r["source_url"]), (r["source2_titre"], r["source2_url"])]
    return S.refs([x for x in paires if x[0]])


def ER(i):
    return D["etf_regles"][i]


def ERS(*ids):
    paires = []
    for i in ids:
        r = D["etf_regles"][i]
        paires += [(r["source_titre"], r["source_url"]), (r["source2_titre"], r["source2_url"])]
    return S.refs([x for x in paires if x[0]])


def ETFS(rows):
    paires = []
    for r in rows:
        paires += [(r["source_titre"], r["source_url"]), (r["source2_titre"], r["source2_url"])]
    return S.refs([x for x in paires if x[0]])



def s_precaution(ctx):
    la = HZ("livret_a_taux")
    body = hd("Objectifs et horizon · d'abord", "Avant d'investir : l'épargne de précaution",
              "L'argent placé en actions doit pouvoir rester investi plusieurs années. Avant d'acheter une seule action, on met de côté de quoi faire face aux imprévus, sans jamais devoir vendre au pire moment.")
    etapes = [("1", "Épargne de précaution", e(HZ("precaution_regle")["fait"]), "Livret A, LDDS : disponibles, garantis, sans impôt"),
              ("2", "Dettes chères", "Rembourser un crédit à la consommation rapporte son taux, sans risque.", "aucun placement ne rapporte 15 % sans risque"),
              ("3", "Projets datés", "Voiture, apport immobilier : l'argent nécessaire avant 5 ans ne va pas en actions.", "livrets, fonds en euros"),
              ("4", "Long terme", "Retraite, liberté financière, transmission : là commence l'investissement en actions.", "PEA, assurance-vie, compte-titres")]
    cards = "".join(f'<div class="card st-c a"><span class="tc-n">{n}</span><span class="tc-t">{t}</span><p class="p sm">{d}</p><span class="tc-r">{x}</span></div>' for n, t, d, x in etapes)
    body += f'''<div class="g main"><div class="g c4 lc1">{cards}</div>
  <div class="g c3 lc1">
    {kv("Livret A, depuis le " + e(HZ("livret_a_taux")["periode"]), cnt(HZv("livret_a_taux"), 1, NBSP + "%"), "net d'impôt ; " + e(la["precision"]), "var(--gold)")}
    {kv("Plafonds", eur(HZv("livret_a_plafond")) + " <small>+ " + eur(HZv("ldds_plafond")) + " (LDDS)</small>", "par personne", "var(--gold)")}
    {kv("Inflation en France", cnt(HZv("inflation_2026"), 1, NBSP + "%"), e(HZ("inflation_2026")["periode"]) + " ; " + e(HZ("inflation_2026")["precision"]), "var(--ndx)")}
  </div></div>'''
    return body, "Sources : " + HZS("precaution_regle", "livret_a_taux", "livret_a_plafond", "ldds_plafond", "inflation_2026")


def s_horizon_table(ctx):
    rows = [["Imprévus", "immédiat", "Livret A, LDDS", "aucune"],
            ["Projet à moins de 2 ans", "0 à 2 ans", "livrets, compte à terme", "aucune"],
            ["Projet à 2 à 5 ans", "2 à 5 ans", "fonds en euros d'assurance-vie, livrets", "faible"],
            ["Projet à 5 à 8 ans", "5 à 8 ans", "PEA, assurance-vie : ETF et actions en partie", "moyenne"],
            ["Retraite, liberté financière", "8 ans et plus", "PEA, assurance-vie, compte-titres : ETF et actions", "élevée"],
            ["Transmission", "long", "assurance-vie", "selon l'horizon des bénéficiaires"]]
    body = hd("Objectifs et horizon · planifier", "Un objectif, un horizon, un support",
              "Chaque euro a une mission et une date. C'est la date qui décide du support : plus elle est lointaine, plus on peut accepter les variations des actions.")
    body += f'''<div class="g c32 main">{table(["Objectif", "Horizon", "Supports adaptés (hyp.)", "Part d'actions"], rows)}
  <div class="g">{ul([f"<b>Les horizons de l'AMF</b> : {e(HZ('amf_horizon')['fait'])}",
                    "<b>Un objectif chiffré</b> : « 300 € par mois pendant 20 ans pour compléter ma retraite » vaut mieux que « gagner de l'argent ».",
                    "<b>La tolérance au risque</b> : pourrez-vous voir votre portefeuille perdre 40 % sans vendre ? Si la réponse est non, réduisez la part d'actions."])}</div></div>'''
    return body, "Tableau : proposition pédagogique (hyp.) ; horizon " + HZS("amf_horizon")


def s_horizon_risque(ctx):
    per = [(k, lab) for k, lab in (("sp500_neg_1an", "1 an"), ("sp500_neg_5ans", "5 ans"), ("sp500_neg_10ans", "10 ans"), ("sp500_neg_15ans", "15 ans"), ("sp500_neg_20ans", "20 ans")) if k in D["horizon"]]
    vmax = max(HZv(k) for k, _ in per) or 1
    bars = "".join(hbar(f"Détention de {lab}", HZv(k) / vmax, f"{fr(HZv(k), 1)}{NBSP}%", "var(--neg)" if HZv(k) > 0 else "var(--pos)", e(HZ(k)["periode"])) for k, lab in per)
    kr = [k for k in ("krach_2000", "krach_2008", "krach_2020", "krach_2022", "pire_annee") if k in D["horizon"]]
    krows = "".join(f'<div class="ln-r a"><span>{e(HZ(k)["fait"].split(" : ")[0])} <small>{e(HZ(k)["periode"])}</small></span><b class="neg">{fr(-abs(HZv(k)), 1)}{NBSP}%</b></div>' for k in kr)
    body = hd("Objectifs et horizon · le temps", "Le temps réduit le risque de perte",
              "Sur un an, les actions perdent souvent. Sur vingt ans, l'histoire américaine n'a jamais montré de perte. Le risque ne disparaît pas : il change de nature.")
    body += f'''<div class="g c32 main"><div class="card a"><span class="lab">Part des périodes de détention en perte, {e(HZ(per[0][0])["precision"])}</span>{bars}</div>
  <div class="g"><div class="card a"><span class="lab">Les grandes chutes du S&amp;P 500</span>{krows}</div>
    <p class="p m a">Le passé ne garantit rien : ces chiffres décrivent un marché, les États-Unis, sur une période favorable. Un indice mondial ou européen a connu des décennies plus longues sans gain.</p></div></div>'''
    return body, "Sources : " + HZS(*[k for k, _ in per], *kr)


def s_dca(ctx):
    v12, v23 = HZ("dca_vanguard_2012"), HZ("dca_vanguard_2023")
    rows = [["Rendement moyen", "plus élevé, car le marché monte plus souvent qu'il ne baisse", "plus faible : l'argent attend"],
            ["Pire scénario", "tout investir juste avant un krach", "le krach n'atteint qu'une partie de la somme"],
            ["Regret", "fort si le marché chute juste après", "réduit"],
            ["Discipline", "une décision unique", "une routine, automatisable"],
            ["Pour qui", "une somme disponible et des nerfs solides", "un salaire épargné chaque mois, ou un héritage qu'on n'ose pas placer"]]
    body = hd("Objectifs et horizon · entrer sur le marché", "En une fois ou progressivement ?",
              "Le DCA (dollar-cost averaging) investit la même somme à intervalles réguliers. L'investissement en une fois (lump sum) place tout tout de suite. Les études tranchent sur le rendement ; la psychologie, parfois, autrement.")
    body += f'''<div class="g c23 main">
  <div class="g">
    <div class="card stat a" style="--c:var(--gold)"><span class="v">{cnt(float(v23["valeur"] or v12["valeur"]), 0, NBSP + "%")}</span><span class="l">{e(v23["fait"])}</span></div>
    <p class="p m a">{e(v12["fait"])}</p>
    <p class="p m a">{e(HZ("dca_comportement")["fait"])}</p>
  </div>
  {table(["", "En une fois", "Progressivement (DCA)"], rows)}
</div>'''
    return body, "Sources : " + HZS("dca_vanguard_2012", "dca_vanguard_2023", "dca_comportement")



def etf_frais_txt(r):
    return f'{fr(float(r["frais_courants_pct"]), 2)}{NBSP}%' if r["frais_courants_pct"] else "à vérifier"


def s_etf_fonctionne(ctx):
    fx = [float(r["frais_courants_pct"]) for r in D["etf"] if r["frais_courants_pct"]]
    etapes = [("L'indice", "Une liste d'actions et leurs poids : Nasdaq 100, S&P 500, MSCI World. Personne ne choisit : la règle décide."),
              ("Le fonds", "Un émetteur (Amundi, iShares, Vanguard…) gère un fonds qui reproduit l'indice. Vous en détenez des parts."),
              ("La Bourse", "La part se négocie comme une action, toute la journée, au prix du marché."),
              ("L'arbitrage", e(ER("creation_rachat")["regle"]))]
    fl = "".join(f'<div class="card fl a"><span class="tc-n">{i + 1}</span><span class="tc-t">{t}</span><p class="p sm">{d}</p></div>' + ('<span class="fl-ar" aria-hidden="true">→</span>' if i < 3 else "") for i, (t, d) in enumerate(etapes))
    body = hd("Les ETF · le principe", "Comment fonctionne un ETF",
              "Un ETF (exchange-traded fund, ou tracker) est un fonds coté en Bourse qui reproduit un indice. Une seule part donne accès à des centaines d'actions.")
    body += f'''<div class="g main"><div class="flow">{fl}</div>
  <div class="g c3 lc1">
    {kv("Frais courants des ETF du tableau", f"{fr(min(fx), 2)} à {fr(max(fx), 2)}{NBSP}%", "par an, prélevés chaque jour sur l'actif du fonds : on ne les voit pas, on les subit", "var(--gold)")}
    {kv("Écart de suivi", "le vrai coût", e(ER("ecart_suivi")["regle"]), "var(--ndx)")}
    {kv("Valeur liquidative", "la référence", "la valeur des actifs du fonds par part, calculée chaque jour ; le cours de Bourse s'en écarte très peu", "var(--ndx)")}
  </div></div>'''
    return body, "Sources : " + ERS("creation_rachat", "ecart_suivi") + " ; frais : " + ETFS(D["etf"])


def s_etf_replication(ctx):
    phys = [r for r in D["etf"] if r["replication"].startswith("physique")]
    synt = [r for r in D["etf"] if r["replication"].startswith("synth")]
    lst = lambda rows: ", ".join(r["ticker"].split(" ")[0] for r in rows)
    body = hd("Les ETF · la réplication", "Physique ou synthétique ?",
              "Deux façons de suivre un indice. Les deux sont encadrées par la directive européenne UCITS ; seule la seconde ouvre le PEA aux indices américains et mondiaux.")
    body += f'''<div class="g c2 main">
  <div class="card a"><span class="lab">Réplication physique</span><p class="cq">Le fonds achète les actions de l'indice.</p>
    {ul(["<b>Complète</b> : toutes les actions, aux mêmes poids.", "<b>Par échantillonnage</b> : un sous-ensemble représentatif, pour les indices de milliers de lignes.",
         "<b>Atout</b> : on sait ce qu'on détient. <b>Limite</b> : pas d'actions américaines dans un PEA.", f"Exemples : {lst(phys)}."])}</div>
  <div class="card hl a"><span class="lab">Réplication synthétique (swap)</span><p class="cq">Le fonds détient un autre panier et échange sa performance contre celle de l'indice.</p>
    {ul([e(ER("pea_swap")["regle"]),
         f"<b>Risque de contrepartie</b> : si la banque fait défaut, le fonds garde son panier ; l'exposition est plafonnée à {fr(float(ER('ucits_contrepartie')['valeur']), 0)}{NBSP}% de l'actif par banque.",
         f"<b>2026</b> : {e(ER('pea_swap_2026')['regle'])}", f"Exemples : {lst(synt)}."])}</div>
</div>'''
    return body, "Sources : " + ERS("pea_swap", "ucits_contrepartie", "pea_swap_2026") + " ; exemples " + ETFS(D["etf"])


def s_etf_capi(ctx):
    fb, fh = D["etf_frais"]["etf_frais_bas"], D["etf_frais"]["etf_frais_haut"]
    d = D["defauts"]
    rows = [["Compte-titres", "dividendes taxés chaque année à la flat tax", "impôt reporté à la vente"],
            ["PEA", "pas d'impôt tant que l'argent reste dans le plan", "idem"],
            ["Assurance-vie", "pas d'impôt avant un rachat", "idem ; offre surtout capitalisante"]]
    body = hd("Les ETF · les coûts", "Capitalisant ou distribuant, et le vrai prix des frais", e(ER("capi_distri")["regle"]))
    body += f'''<div class="g c2 main">
  {table(["Enveloppe", "ETF distribuant", "ETF capitalisant"], rows)}
  <div class="card a"><span class="lab">{eur(d["capital"])} puis {eur(d["mensuel"])} par mois, {fr(d["annees"], 0)} ans, {fr(d["rendement"] * 100, 0)}{NBSP}% brut</span>
    {hbar(f"Frais de {fr(fb['frais'] * 100, 2)}{NBSP}%", 1.0, eur(fb["valeur"]), "var(--pos)")}
    {hbar(f"Frais de {fr(fh['frais'] * 100, 2)}{NBSP}%", fh["valeur"] / fb["valeur"], eur(fh["valeur"]), "var(--neg)")}
    <p class="p">Écart : <b class="gold">{eur(fb["valeur"] - fh["valeur"])}</b> pour {eur(fb["verse"])} versés, avant impôts. À indice égal, les frais courants sont le premier critère de choix.</p></div>
</div>'''
    return body, "Sources : " + ERS("capi_distri") + " ; calcul : " + HYPS()


def s_etf_table(ctx):
    rows = []
    for r in sorted(D["etf"], key=lambda r: (r["pea"] != "oui", r["indice"])):
        rows.append([f'<b>{e(r["nom"])}</b> <small>{e(r["ticker"])} · {e(r["isin"])}</small>', e(r["indice"]), e(r["replication"]), etf_frais_txt(r),
                     f'<span class="{"pos" if r["pea"] == "oui" else "na"}">{e(r["pea"])}</span>', e(r["domicile"])])
    body = hd("Les ETF · la sélection", "Les principaux ETF pour un investisseur français",
              "Les synthétiques ouvrent le PEA aux indices américains et mondiaux ; les physiques irlandais sont souvent moins chers, mais réservés au compte-titres et à l'assurance-vie.")
    body += table(["ETF", "Indice", "Réplication", "Frais courants", "PEA", "Domicile"], rows, num=(3,), cls="etf w")
    body += "<p class=\"p m sm a\">Frais « à vérifier » : sources contradictoires (Vanguard FTSE All-World : 0,14 % à 0,22 % ; Amundi PEA Emergent : 0,20 % à 0,30 %). Tous ces ETF sont capitalisants. Avant d'acheter, lisez le document d'informations clés (DIC) de l'émetteur. Liste indicative, pas une recommandation.</p>"
    return body, "Sources : " + ETFS(D["etf"])


def s_etf_choisir(ctx):
    us = D["etf_us"]
    q = ["<b>Quel indice ?</b> Monde pour le socle ; États-Unis ou Nasdaq 100 pour plus de croissance et plus de concentration.",
         "<b>Quelle enveloppe ?</b> PEA : un synthétique éligible. Compte-titres ou assurance-vie : un physique, souvent moins cher.",
         "<b>Quels frais courants ?</b> À indice égal, le moins cher gagne presque toujours sur la durée.",
         "<b>Quel écart de suivi ?</b> Il mesure le coût réel, au-delà des frais affichés.",
         "<b>Capitalisant ou distribuant ?</b> Capitalisant sur un compte-titres, pour reporter l'impôt.",
         "<b>Quel encours et quel émetteur ?</b> Un fonds important et un émetteur solide limitent le risque de fermeture."]
    body = hd("Les ETF · choisir", "Choisir son ETF en six questions", "")
    body += f'''<div class="g c32 main"><div class="card a">{ul(q)}</div>
  <div class="card a" style="border-color:var(--neg)"><span class="lab">Pourquoi pas QQQ ou SPY ?</span><p class="p">{e(ER("priips")["regle"])}</p>
    <div class="ln-r"><span>QQQ (Nasdaq 100)</span><b>{fr(float(us["QQQ"]["frais_pct"]), 2)}{NBSP}%</b></div>
    <div class="ln-r"><span>SPY (S&amp;P 500)</span><b>{fr(float(us["SPY"]["frais_pct"]), 2)}{NBSP}%</b></div>
    <div class="ln-r"><span>VOO (S&amp;P 500)</span><b>{fr(float(us["VOO"]["frais_pct"]), 2)}{NBSP}%</b></div>
    <p class="p m sm">Frais annuels selon Zacks. Leurs équivalents européens (CNDX, CSPX, PUST, PSP5) jouent le même rôle, avec un document d'informations clés.</p></div></div>'''
    return body, "Sources : " + ERS("priips") + " ; frais américains " + S.refs([("Zacks Investment Research : fiches QQQ, SPY, VOO (12/10/2026)", "https://www.zacks.com/stock/quote/QQQ")])


# ============================================================ assemblage du plan
def plan(n_sources):
    SL.clear()
    add("Ouverture", "Couverture", s_cover, "cover")
    add("Ouverture", "Le parcours", s_sommaire)
    add("Ouverture", "À la fin, vous saurez…", s_objectifs)
    opener("Objectifs et horizon")
    add("Objectifs et horizon", "L'épargne de précaution", s_precaution)
    add("Objectifs et horizon", "Un objectif, un horizon, un support", s_horizon_table)
    add("Objectifs et horizon", "Le temps réduit le risque", s_horizon_risque)
    add("Objectifs et horizon", "Le noyau et les satellites", s_noyau)
    add("Objectifs et horizon", "En une fois ou progressivement ?", s_dca)
    add("Objectifs et horizon", "Le DCA en pratique", s_dca_ex)
    opener("Les bases")
    add("Les bases", "Une action, c'est une part d'entreprise", s_action)
    add("Les bases", "Cours = BPA × P/E", s_formule)
    add("Les bases", "ETF ou stock picking", s_etf)
    add("Les bases", "Le risque", s_risque)
    opener("Lire les comptes")
    add("Lire les comptes", "Trois documents, trois questions", s_etats)
    add("Lire les comptes", "La cascade du compte de résultat", s_cascade)
    add("Lire les comptes", "Les marges", s_marges)
    add("Lire les comptes", "La croissance (TCAM)", s_croissance)
    add("Lire les comptes", "BPA GAAP et non-GAAP", s_gaap)
    add("Lire les comptes", "Dilution, rachats, dividendes", s_dilution)
    add("Lire les comptes", "Le FCF et le capex", s_fcf)
    add("Lire les comptes", "Le bilan", s_bilan)
    add("Lire les comptes", "ROE et ROIC", s_roic)
    add("Lire les comptes", "Lire une banque : Nu", s_banque)
    add("Lire les comptes", "Lire une plateforme : Reddit et Adyen", s_plateformes)
    add("Lire les comptes", "Les cycliques : Micron et Intel", s_cycliques)
    opener("Valoriser")
    add("Valoriser", "Capitalisation et valeur d'entreprise", s_cap)
    add("Valoriser", "Cinq P/E pour une action", s_pe5)
    add("Valoriser", "Les autres multiples", s_multiples)
    add("Valoriser", "Le PEG", s_peg)
    add("Valoriser", "Le piège du PEG de court terme", s_piege)
    add("Valoriser", "Consensus et rang Zacks", s_consensus)
    add("Valoriser", "Ce que le prix suppose", s_suppose)
    opener("La méthode GARP")
    add("La méthode GARP", "Les six catégories de Lynch", s_categories)
    add("La méthode GARP", "La grille en sept critères", s_grille)
    add("La méthode GARP", "La grille appliquée", s_grille_app)
    add("La méthode GARP", "Trois scénarios", s_scenarios)
    add("La méthode GARP", "La zone d'achat", s_zone)
    add("La méthode GARP", "Quand vendre", s_vendre)
    add("La méthode GARP", "Construire le portefeuille", s_portefeuille)
    add("La méthode GARP", "Les biais", s_biais)
    opener("Enveloppes, frais et impôts")
    add("Enveloppes, frais et impôts", "Le tableau des enveloppes", s_enveloppes)
    add("Enveloppes, frais et impôts", "Le PEA", s_pea)
    add("Enveloppes, frais et impôts", "Le compte-titres", s_cto)
    add("Enveloppes, frais et impôts", "L'assurance-vie", s_av)
    add("Enveloppes, frais et impôts", "Les frais", s_frais)
    add("Enveloppes, frais et impôts", "Quelle enveloppe pour quelle valeur", s_ou)
    opener("Les ETF")
    add("Les ETF", "Comment fonctionne un ETF", s_etf_fonctionne)
    add("Les ETF", "Ce que contient un ETF Nasdaq 100", s_etf_contenu)
    add("Les ETF", "Physique ou synthétique", s_etf_replication)
    add("Les ETF", "Capitalisant, distribuant et frais", s_etf_capi)
    add("Les ETF", "Les principaux ETF", s_etf_table)
    add("Les ETF", "Choisir son ETF", s_etf_choisir)
    opener("Intérêts composés")
    add("Intérêts composés", "La mécanique", s_composes)
    add("Intérêts composés", "La calculatrice", s_calc, "calc-sl")
    add("Intérêts composés", "La tyrannie des frais", s_tyrannie)
    add("Intérêts composés", "L'effet de l'enveloppe", s_impact_env)
    add("Intérêts composés", "Le temps plutôt que le timing", s_temps)
    opener("Grands investisseurs")
    add("Grands investisseurs", "Peter Lynch", s_lynch)
    add("Grands investisseurs", "Warren Buffett", s_buffett)
    add("Grands investisseurs", "Charlie Munger", s_munger)
    add("Grands investisseurs", "Benjamin Graham", s_graham)
    add("Grands investisseurs", "Fisher et Smith", s_fisher)
    add("Grands investisseurs", "Bogle et Marks", s_bogle)
    add("Grands investisseurs", "La synthèse", s_synthese)
    opener("Passer à l'action")
    add("Passer à l'action", "Check-list et routine", s_routine)
    add("Passer à l'action", "Testez-vous", s_quiz, "quiz-sl")
    for k in (1, 2, 3):
        add("Passer à l'action", f"Glossaire ({k}/3)", s_glossaire(k))
    for k in range(n_sources):
        add("Passer à l'action", f"Sources ({k + 1}/{n_sources})", s_sources(k, n_sources), "src-sl")
    add("Passer à l'action", "Ce qu'il faut retenir", s_fin)


def teasers():
    n = R["NVDA"]
    pe5 = D["pe5"]
    c = D["comparaison"]
    t = lambda big, txt: f'<div class="op-tz a"><span class="op-big">{big}</span><span class="op-txt">{txt}</span></div>'
    fx = [float(r["frais_courants_pct"]) for r in D["etf"] if r["frais_courants_pct"]]
    return {
        "Objectifs et horizon": t(cnt(float(D["horizon"]["dca_vanguard_2023"]["valeur"]), 0, NBSP + "%"), "des cas où investir en une fois a battu un DCA de trois mois (Vanguard, MSCI World, 1976-2022)"),
        "Les ETF": t(f"{fr(min(fx), 2)} → {fr(max(fx), 2)}{NBSP}%", "les frais courants annuels des principaux ETF : des centaines d'actions pour presque rien"),
        "Les bases": t(cnt(n["bpa_gaap"], 2, NBSP + "$"), "de bénéfice par action pour NVIDIA sur l'exercice 2026"),
        "Lire les comptes": t(cnt(n["marge_operationnelle"] * 100, 1, NBSP + "%"), "de marge opérationnelle chez NVIDIA : 60 cents gardés sur chaque dollar vendu"),
        "Valoriser": t(f'{fr(min(p for *_, p in pe5), 1)} → {fr(max(p for *_, p in pe5), 1)}', "les cinq P/E de NVIDIA, pour un seul et même cours"),
        "La méthode GARP": t(cnt(c["peg_lt"]["ptf"], 2), f"le PEG de long terme du portefeuille, contre {fr(c['peg_lt']['ndx'], 2)} pour le Nasdaq 100"),
        "Enveloppes, frais et impôts": t(f'{fr(fv("ps_2026"), 1)} <small>contre</small> {fr(fv("pfu_total"), 1)}{NBSP}%', "l'impôt sur les gains d'un PEA de plus de 5 ans, contre celui d'un compte-titres"),
        "Intérêts composés": t("×" + fr(D["interets"][1]["valeur_30ans"] / H["calc_capital"], 1), "votre capital en 30 ans à 7 % par an, sans rien ajouter"),
        "Grands investisseurs": t(cnt(float(D["lynch"]["rendement_annuel"]["valeur"]), 1, NBSP + "%"), "par an pour Peter Lynch au fonds Magellan, de 1977 à 1990"),
        "Passer à l'action": t("10", "questions à se poser avant chaque achat"),
    }


def rendre(n_sources):
    global S
    S = Sources()
    plan(n_sources)
    ctx = {"slides": SL, "teasers": teasers()}
    N = len(SL)
    out = []
    for i, s in enumerate(SL):
        body, src = s["fn"](ctx)
        cls = s["cls"]
        hud = (f'<header class="hud"><span class="mast">La Gazette du PEG*</span><span class="hsec">{e(s["sec"])}</span>'
               f'<span class="hnum">{i + 1:02d} / {N}</span></header>')
        foot = f'<footer class="foot"><span class="src">{src}</span><span class="ed">Hors-série formation · {D["date"]}</span></footer>'
        inner = body if "op" in cls else f'<div class="body">{body}</div>'
        out.append(f'<section class="slide {cls}" id="s{i + 1}" data-sec="{e(s["sec"])}" data-titre="{e(s["titre"])}" aria-label="{i + 1}. {e(s["titre"])}">'
                   f'<div class="sl-in"><div class="bg" aria-hidden="true"></div>{hud}{inner}{foot}</div></section>')
    return out


# ============================================================ CSS et JS
CSS_SRC = r"""
:root { color-scheme: dark; --ink:#07090d; --ink2:#0b0e14; --card:rgba(242,237,226,.035); --paper:#f2ede2; --muted:#a3abbb; --dim:#8d96a8;
  --line:rgba(242,237,226,.15); --line2:rgba(242,237,226,.08); --gold:#ffc94a; --ndx:#8da2c8; --neg:#ff6a5f; --pos:#5be38f; background:#07090d; }
html, body { background:#07090d; color:#f2ede2; }
body { margin:0; }
#gz { font-family:"GZ Archivo", "Archivo", "Arial Narrow", Arial, sans-serif; color:var(--paper); background:var(--ink); -webkit-font-smoothing:antialiased; }
#gz *, #gz *::before, #gz *::after { box-sizing:border-box; }
:where(#gz) :where(h1,h2,h3,p,ul,ol,dl,dd,figure,blockquote) { margin:0; padding:0; }
:where(#gz) :where(ul, ol) { list-style:none; }
:where(#gz) a { color:inherit; }
:where(#gz) button { font:inherit; color:inherit; }
.gold { color:var(--gold); } .neg { color:var(--neg); } .pos { color:var(--pos); } .col { color:var(--c); }
.num { font-family:"GZ Plex Mono", "IBM Plex Mono", ui-monospace, monospace; font-variant-numeric:tabular-nums; }

/* ---------- jetons : lecture (défaut) puis présentation et impression ---------- */
.sl-in { --u:.55px; --fs-hud:11px; --fs-foot:11px; --fs-kick:11.5px; --fs-h1:clamp(25px, 7vw, 40px); --fs-xl:clamp(44px, 13vw, 84px);
  --fs-lede:16.5px; --fs-b:15px; --fs-s:13.5px; --fs-xs:12px; --fs-t:13.5px; --fs-th:11px; --fs-lab:11px;
  --fs-n1:clamp(46px, 13vw, 80px); --fs-n2:clamp(36px, 10vw, 56px); --fs-n3:30px; --fs-n4:21px; --fs-q:clamp(19px, 5vw, 26px);
  --gap:16px; --pad-x:16px; --r:12px; }
%P .sl-in { --u:calc(100cqw / 1920); --fs-hud:17u; --fs-foot:16u; --fs-kick:21u; --fs-h1:84u; --fs-xl:220u;
  --fs-lede:31u; --fs-b:27.5u; --fs-s:22.5u; --fs-xs:18.5u; --fs-t:25.5u; --fs-th:17u; --fs-lab:17.5u;
  --fs-n1:180u; --fs-n2:108u; --fs-n3:68u; --fs-n4:41u; --fs-q:46u; --gap:30u; --pad-x:104u; --r:18u; }
%P .g.main { align-content:safe center; }

/* ---------- diapositive ---------- */
.slide { position:relative; container-type:inline-size; background:var(--ink); overflow:hidden; isolation:isolate; }
.sl-in { position:relative; display:flex; flex-direction:column; padding:14px var(--pad-x) 14px; min-height:100%; }
%P .sl-in { height:100%; padding:28u var(--pad-x) 22u; }
.bg { position:absolute; inset:0; z-index:-1; pointer-events:none;
  background:
    radial-gradient(60% 70% at 0% 0%, rgba(58,91,217,.16), transparent 70%),
    radial-gradient(50% 60% at 100% 100%, rgba(255,176,32,.09), transparent 70%),
    linear-gradient(rgba(242,237,226,.035) 1px, transparent 1px) 0 0 / 80u 80u,
    linear-gradient(90deg, rgba(242,237,226,.035) 1px, transparent 1px) 0 0 / 80u 80u; }
.bg::after { content:""; position:absolute; inset:0; opacity:.06;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' seed='7' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>"); }
.hud { display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:6px 16px; font:500 var(--fs-hud)/1.2 "GZ Plex Mono", monospace;
  letter-spacing:.14em; text-transform:uppercase; color:var(--muted); padding-bottom:12u; border-bottom:1px solid var(--line); }
.hud .mast { color:var(--paper); font-weight:600; } .hud .hsec { color:var(--gold); }
.body { flex:1 1 auto; min-height:0; display:flex; flex-direction:column; gap:var(--gap); padding-top:24u; }
.hd { display:flex; flex-direction:column; gap:12u; }
.kick { font:500 var(--fs-kick)/1.25 "GZ Plex Mono", monospace; letter-spacing:.16em; text-transform:uppercase; color:var(--gold); }
.h1 { font-family:"GZ Archivo", sans-serif; font-weight:900; font-stretch:62%; text-transform:uppercase; font-size:var(--fs-h1); line-height:.95;
  letter-spacing:-.002em; text-wrap:balance; max-width:1720u; }
.lede { font-family:"GZ Newsreader", Georgia, serif; font-size:var(--fs-lede); line-height:1.36; color:var(--muted); max-width:1400u; text-wrap:pretty; }
.main { flex:1 1 auto; min-height:0; }
.foot { display:flex; gap:6px 24u; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; font:400 var(--fs-foot)/1.4 "GZ Plex Mono", monospace;
  color:var(--dim); padding-top:10u; border-top:1px solid var(--line2); margin-top:14u; }
.foot .src { min-width:0; flex:1 1 300px; } .foot .ed { white-space:nowrap; }
.p { font-size:var(--fs-b); line-height:1.42; text-wrap:pretty; } .p.m { color:var(--muted); }
.p b, .ul b { font-weight:700; } .p.sm { font-size:var(--fs-s); line-height:1.35; }
.lab { display:block; font:500 var(--fs-lab)/1.3 "GZ Plex Mono", monospace; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); }
small { font-size:max(.78em, 11px); color:var(--muted); }

/* ---------- grilles ---------- */
.g { display:grid; gap:var(--gap); grid-template-columns:minmax(0,1fr); align-content:start; }
.g > * { min-width:0; }
.lc2 { grid-template-columns:repeat(2, minmax(0,1fr)); }
%P .c2 { grid-template-columns:repeat(2, minmax(0,1fr)); } %P .c3 { grid-template-columns:repeat(3, minmax(0,1fr)); }
%P .c4 { grid-template-columns:repeat(4, minmax(0,1fr)); } %P .c5 { grid-template-columns:repeat(5, minmax(0,1fr)); } %P .c32 { grid-template-columns:minmax(0,3fr) minmax(0,2fr); }
%P .c23 { grid-template-columns:minmax(0,2fr) minmax(0,3fr); } %P .c31 { grid-template-columns:minmax(0,3fr) minmax(0,1.25fr); }
%P .lc1.c3 { grid-template-columns:repeat(3, minmax(0,1fr)); }
.stats3 { grid-template-rows:auto; }

/* ---------- briques ---------- */
.card { background:var(--card); border:1px solid var(--line); border-radius:var(--r); padding:18u 22u; display:flex; flex-direction:column; gap:10u; min-width:0; }
.lecture .card, .card { padding:12px 14px; }
%P .card { padding:20u 24u; }
.card.hl { border-color:var(--gold); background:rgba(255,201,74,.05); }
.card[style*="--c"] { border-top:3px solid var(--c); }
.kv { display:flex; flex-direction:column; gap:4u; background:var(--card); border:1px solid var(--line); border-radius:var(--r); padding:12px 14px; border-top:3px solid var(--c, var(--line)); }
%P .kv { padding:18u 22u; }
.kv .v { font:900 var(--fs-n3)/1 "GZ Archivo", sans-serif; font-stretch:62%; color:var(--c, var(--paper)); font-variant-numeric:tabular-nums; }
.kv .v small { font-size:.5em; font-stretch:100%; font-weight:500; }
.kv .sub { font-size:var(--fs-s); color:var(--muted); line-height:1.3; }
.stat { justify-content:center; }
.stat .v { font:900 var(--fs-n2)/.95 "GZ Archivo", sans-serif; font-stretch:62%; color:var(--c, var(--paper)); }
.stat .l { font-size:var(--fs-s); color:var(--muted); line-height:1.38; }
.ul { display:flex; flex-direction:column; gap:10u; }
.ul li { position:relative; padding-left:24u; font-size:var(--fs-b); line-height:1.4; }
.lecture .ul li, .ul li { padding-left:18px; }
%P .ul li { padding-left:30u; }
.ul li::before { content:""; position:absolute; left:2px; top:.5em; width:7px; height:7px; background:var(--gold); transform:rotate(45deg); }
%P .ul li::before { width:11u; height:11u; }
.ul.sm li { font-size:var(--fs-s); line-height:1.35; }
.ul.ck li::before { content:"✓"; background:none; transform:none; top:0; color:var(--pos); font-weight:700; width:auto; height:auto; }
.steps { counter-reset:st; display:flex; flex-direction:column; gap:12u; }
.steps li { counter-increment:st; position:relative; padding-left:44u; font-size:var(--fs-b); line-height:1.4; }
.lecture .steps li, .steps li { padding-left:30px; } %P .steps li { padding-left:52u; }
.steps li::before { content:counter(st); position:absolute; left:0; top:0; font:900 1.5em/1 "GZ Archivo"; font-stretch:62%; color:var(--gold); }
.formula { font:500 var(--fs-b)/1.4 "GZ Plex Mono", monospace; color:var(--paper); background:rgba(255,201,74,.07); border-left:3px solid var(--gold); padding:10px 14px; border-radius:0 8px 8px 0; }
%P .formula { padding:14u 20u; }
.formula small { display:block; font-size:.8em; }
.ln-r { display:flex; justify-content:space-between; align-items:baseline; gap:12px; padding:7u 0; border-bottom:1px solid var(--line2); font-size:var(--fs-b); }
.ln-r b { font-family:"GZ Plex Mono", monospace; font-weight:600; font-variant-numeric:tabular-nums; text-align:right; white-space:nowrap; }
.ln-r small { font-weight:400; }
.dot { display:inline-block; width:.62em; height:.62em; border-radius:50%; background:var(--c); margin-right:.45em; vertical-align:.05em; }
i.dot { font-style:normal; }
.chips { display:flex; flex-wrap:wrap; gap:10px; }
.chip { display:inline-flex; align-items:center; gap:8px; padding:6px 12px; border:2px solid var(--c); border-radius:999px; font:600 var(--fs-s) "GZ Plex Mono", monospace; letter-spacing:.04em; }
%P .chip { padding:10u 20u; gap:12u; }
.chip i { width:10px; height:10px; border-radius:50%; background:var(--c); }
.def { font-size:var(--fs-b); line-height:1.4; padding-bottom:10u; border-bottom:1px solid var(--line2); }
.na { color:var(--dim); font-style:italic; }
.cq { font:italic 400 var(--fs-n4)/1.15 "GZ Newsreader", Georgia, serif; }
.lines { display:flex; flex-direction:column; }

/* barres horizontales */
.hb { display:grid; grid-template-columns:minmax(0, 9em) minmax(0,1fr) auto; align-items:center; gap:10px; padding:5u 0; }
%P .hb { grid-template-columns:300u minmax(0,1fr) 210u; gap:18u; padding:7u 0; }
.hb-l { font-size:var(--fs-b); line-height:1.15; } .hb-l small { display:block; font:400 var(--fs-xs) "GZ Plex Mono", monospace; color:var(--dim); }
.hb-t { position:relative; height:12px; background:var(--line2); border-radius:99px; overflow:hidden; }
%P .hb-t { height:24u; }
.hb-t i { display:block; height:100%; background:var(--c); border-radius:99px; transform-origin:left center; }
.hb-v { font:600 var(--fs-b) "GZ Plex Mono", monospace; text-align:right; white-space:nowrap; font-variant-numeric:tabular-nums; }
.hb.neg .hb-t i { background:var(--c); }

/* tableaux */
.tw { overflow-x:auto; min-width:0; }
.t { width:100%; border-collapse:collapse; font-size:var(--fs-t); line-height:1.3; font-variant-numeric:tabular-nums; }
.t th { font:500 var(--fs-th)/1.25 "GZ Plex Mono", monospace; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); text-align:left; padding:8u 12u; border-bottom:1px solid var(--line); vertical-align:bottom; }
.t td { padding:9u 12u; border-bottom:1px solid var(--line2); vertical-align:middle; }
.t .n { text-align:right; font-family:"GZ Plex Mono", monospace; white-space:nowrap; }
.t td:first-child { font-weight:600; }
.t.w { min-width:640px; } %P .t.w { min-width:0; }
.t.env td { vertical-align:top; } .t.env td:not(:first-child) { color:var(--paper); }
.t.grille td { font-size:calc(var(--fs-t) * .92); white-space:nowrap; } .t.grille td:first-child { white-space:normal; }
.mk { display:inline-block; width:1.4em; text-align:center; font-weight:700; } .mk.ok { color:var(--pos); } .mk.ko { color:var(--neg); } .mk.na { color:var(--dim); }
.mini-b { position:relative; height:1.6em; display:flex; align-items:center; min-width:120px; }
.mini-b i { position:absolute; left:0; top:15%; height:70%; width:var(--w); background:var(--c); opacity:.35; border-radius:4px; transform-origin:left; }
.mini-b span { position:relative; padding-left:8px; font-family:"GZ Plex Mono", monospace; font-weight:600; }
.t.marg td { padding-top:6u; padding-bottom:6u; }
.t.stress td { padding-top:7u; padding-bottom:7u; } .t.stress td:first-child { font-weight:400; }

/* citations */
.q { display:flex; flex-direction:column; gap:10u; border-left:3px solid var(--gold); padding-left:16px; min-width:0; }
%P .q { padding-left:24u; border-left-width:4u; }
.q .en { font:italic 400 var(--fs-q)/1.14 "GZ Newsreader", Georgia, serif; color:var(--paper); }
.q .fr { font:400 var(--fs-lede)/1.35 "GZ Newsreader", Georgia, serif; color:var(--muted); }
.q .by { font:500 var(--fs-xs)/1.45 "GZ Plex Mono", monospace; color:var(--dim); text-transform:uppercase; letter-spacing:.05em; }
.q .lecon { font-size:var(--fs-s); line-height:1.4; color:var(--paper); background:rgba(255,201,74,.06); padding:8u 12u; border-radius:6px; }
.q.sm .en { font-size:var(--fs-n4); } .q.sm .fr { font-size:var(--fs-s); }
.q-grid .q .en { font-size:calc(var(--fs-n4) * .9); }

/* couverture */
.cover .body { justify-content:space-between; }
.cv { display:grid; gap:var(--gap); grid-template-columns:minmax(0,1fr); flex:1; align-content:center; }
%P .cv { grid-template-columns:minmax(0,1.55fr) minmax(0,1fr); align-items:center; gap:70u; }
.cv-l { display:flex; flex-direction:column; gap:22u; }
.cv-t { font-family:"GZ Archivo", sans-serif; font-weight:900; font-stretch:62%; text-transform:uppercase; font-size:var(--fs-xl); line-height:.97; letter-spacing:-.005em; }
%P .cv-t { font-size:150u; }
.cv-t em { font-style:normal; color:var(--gold); } .cv-t span { display:inline; }
.cv-r { display:flex; flex-direction:column; gap:8u; border-left:3px solid var(--gold); padding-left:22u; }
.cv-big { font:900 var(--fs-n1)/.9 "GZ Archivo", sans-serif; font-stretch:62%; color:var(--gold); }
.cv-sub { font:400 var(--fs-lede)/1.35 "GZ Newsreader", Georgia, serif; color:var(--muted); }
.cv-disc { font:400 var(--fs-xs)/1.45 "GZ Plex Mono", monospace; color:var(--dim); }
.tape { position:relative; overflow:hidden; border-top:1px solid var(--line); border-bottom:1px solid var(--line); height:2.6em; font-size:var(--fs-s); }
.tape-in { position:absolute; left:0; top:0; display:flex; white-space:nowrap; height:100%; align-items:center; }
.tk { padding:0 2.2em; font-family:"GZ Plex Mono", monospace; color:var(--muted); } .tk b { color:var(--c); } .tk s { text-decoration:none; color:var(--dim); font-size:.85em; }

/* sommaire */
.toc-card { text-decoration:none; transition:border-color .2s, transform .2s; }
.toc-card:hover, .toc-card:focus-visible { border-color:var(--gold); transform:translateY(-2px); }
.tc-n { font:900 var(--fs-n3)/1 "GZ Archivo"; font-stretch:62%; color:var(--gold); }
.tc-t { font:800 var(--fs-n4)/1.05 "GZ Archivo"; font-stretch:75%; text-transform:uppercase; }
%P .toc-card { gap:6u; } %P .toc-card .tc-t { font-size:calc(var(--fs-n4) * .85); } %P .toc-card .tc-s { font-size:var(--fs-xs); }
.tc-s { font-size:var(--fs-s); color:var(--muted); line-height:1.35; }
.tc-r { font:500 var(--fs-xs) "GZ Plex Mono"; color:var(--dim); text-transform:uppercase; letter-spacing:.06em; margin-top:auto; }

/* ouvertures de chapitre */
.op .op-in { position:relative; z-index:2; flex:1; display:flex; flex-direction:column; justify-content:center; gap:16u; padding:20px 0; }
%P .op .op-in { padding:30u 0 10u; max-width:1180u; }
.op .xl { font-family:"GZ Archivo", sans-serif; font-weight:900; font-stretch:62%; text-transform:uppercase; font-size:var(--fs-xl); line-height:.95; text-wrap:balance; }
%P .op .xl { font-size:150u; }
.opn { position:absolute; right:-10px; bottom:-20px; z-index:1; font:900 46vw/.8 "GZ Archivo"; font-stretch:62%; color:transparent; -webkit-text-stroke:1.5px rgba(255,201,74,.55); pointer-events:none; }
%P .opn { font-size:700u; right:60u; bottom:30u; -webkit-text-stroke:3u rgba(255,201,74,.6); }
.op-list { display:grid; gap:4u 30u; grid-template-columns:minmax(0,1fr); margin-top:10u; }
%P .op-list { grid-template-columns:repeat(2, minmax(0,1fr)); }
.op-list a { display:flex; gap:12px; align-items:baseline; text-decoration:none; font-size:var(--fs-b); padding:5u 0; border-bottom:1px solid var(--line2); }
.op-list a:hover { color:var(--gold); }
.op-list .num { color:var(--gold); font-size:.8em; }
.op-tz { display:flex; align-items:baseline; gap:20u; flex-wrap:wrap; margin-top:12u; }
.op-big { font:900 var(--fs-n2)/1 "GZ Archivo"; font-stretch:62%; color:var(--gold); } .op-big small { font-size:.4em; color:var(--muted); font-stretch:100%; }
.op-txt { font:400 var(--fs-lede)/1.3 "GZ Newsreader", Georgia, serif; color:var(--muted); max-width:640u; }
.wipe { position:absolute; inset:0; z-index:8; background:var(--gold); transform:scaleX(0); pointer-events:none; }

/* graphiques */
.ch { min-width:0; display:flex; flex-direction:column; gap:8u; }
.ch svg { display:block; width:100%; height:auto; }
.lecture .ch, .ch { overflow-x:auto; } .ch svg { min-width:520px; } %P .ch svg { min-width:0; }
%P .ch { overflow:visible; }
.ch text { font-family:"GZ Plex Mono", monospace; }
.ch text.lbl { font-family:"GZ Archivo", sans-serif; font-stretch:75%; font-weight:500; }

/* FCF */
.fcf-col { display:flex; flex-direction:column; gap:8u; background:var(--card); border:1px solid var(--line); border-top:3px solid var(--c); border-radius:var(--r); padding:12px 14px; }
%P .fcf-col { padding:18u 22u; }
.fcf-bars { display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:10px; align-items:end; height:180px; margin:6px 0 4px; }
%P .fcf-bars { height:330u; gap:16u; }
.fb { position:relative; height:100%; display:flex; flex-direction:column; justify-content:flex-end; align-items:center; gap:4px; }
.fb i { display:block; width:100%; background:var(--c); border-radius:6px 6px 0 0; transform-origin:bottom; }
.fb.cx i { background:var(--neg); } .fb.fc i { background:var(--gold); }
.fb span { order:-1; font:600 var(--fs-s) "GZ Plex Mono"; white-space:nowrap; } .fb small { font:400 var(--fs-xs) "GZ Plex Mono"; color:var(--dim); }
.bil { display:flex; flex-direction:column; gap:6u; background:var(--card); border:1px solid var(--line); border-top:3px solid var(--c); border-radius:var(--r); padding:12px 14px; }
%P .bil { padding:18u 20u; }
%P .bil .hb { grid-template-columns:130u minmax(0,1fr) 150u; }

/* fourchettes et zones */
.rg, .zn { display:grid; grid-template-columns:7em minmax(0,1fr) 4.6em; align-items:center; gap:10px; padding:14u 0 22u; border-bottom:1px solid var(--line2); }
%P .rg, %P .zn { grid-template-columns:230u minmax(0,1fr) 150u; gap:20u; padding:5u 0 22u; }
%P .tight .hb { padding:2u 0; } %P .tight .rg { padding:3u 0 20u; }
.rg-head { display:flex; justify-content:space-between; gap:12px; }
.rg-l, .zn-l { font-size:var(--fs-b); font-weight:600; color:var(--c); }
.rg-x, .zn-x { font:600 var(--fs-b) "GZ Plex Mono"; text-align:right; color:var(--paper); }
.rg-t, .zn-t { position:relative; height:14px; background:var(--line2); border-radius:99px; }
%P .rg-t, %P .zn-t { height:20u; }
.rg-band { position:absolute; top:0; height:100%; background:var(--c); opacity:.45; border-radius:99px; transform-origin:left; }
.rg-m { position:absolute; top:-30%; height:160%; width:3px; margin-left:-1.5px; background:var(--paper); }
.rg-e { position:absolute; top:50%; width:12px; height:12px; margin:-6px 0 0 -6px; background:var(--c); border:2px solid var(--ink); transform:rotate(45deg); }
%P .rg-e { width:20u; height:20u; margin:-10u 0 0 -10u; }
.rg-v, .zn-a { position:absolute; top:100%; margin-top:4px; transform:translateX(-50%); font:500 var(--fs-xs) "GZ Plex Mono"; color:var(--dim); white-space:nowrap; }
.rg-ticks { position:relative; height:1.6em; margin:6u 0 0; margin-left:calc(7em + 10px); margin-right:calc(4.6em + 10px); font:400 var(--fs-xs) "GZ Plex Mono"; color:var(--dim); }
%P .rg-ticks { margin-left:250u; margin-right:170u; }
.rg-ticks span { position:absolute; transform:translateX(-50%); }
.zn-safe { position:absolute; top:0; height:100%; background:rgba(91,227,143,.55); border-radius:99px 0 0 99px; }
.zn-buy { position:absolute; top:0; height:100%; background:rgba(91,227,143,.25); }
.zn-px { position:absolute; top:-45%; height:190%; width:4px; margin-left:-2px; background:var(--c); }
.zn-pl { position:absolute; bottom:100%; transform:translateX(-50%); font:600 var(--fs-xs) "GZ Plex Mono"; color:var(--c); white-space:nowrap; margin-bottom:6px; }

/* catégories */
.cats .card { gap:5u; } .cat .p { font-size:var(--fs-s); line-height:1.35; } .cat .ex { font-size:var(--fs-s); line-height:1.3; }

/* PEG */
.fld { display:flex; flex-direction:column; gap:6px; font:500 var(--fs-lab) "GZ Plex Mono"; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); }
.pegcalc input { width:100%; }
input[type=number] { background:rgba(0,0,0,.25); border:1px solid var(--line); color:var(--paper); border-radius:8px; padding:8px 10px; font:600 16px "GZ Plex Mono", monospace; text-align:right; min-height:40px; }
%P input[type=number] { font-size:var(--fs-b); padding:8u 12u; min-height:0; border-radius:8u; }
input[type=number]:focus-visible, input[type=range]:focus-visible, button:focus-visible { outline:2px solid var(--gold); outline-offset:2px; }
.peg-out { display:flex; align-items:baseline; gap:16u; flex-wrap:wrap; }
.peg-v { font:900 var(--fs-n2)/1 "GZ Archivo"; font-stretch:62%; color:var(--gold); } .peg-txt { font-size:var(--fs-b); color:var(--paper); }
.gauge { position:relative; display:flex; height:14px; border-radius:99px; overflow:visible; }
%P .gauge { height:22u; }
.gauge .gz { display:block; height:100%; }
.gz.z1 { width:26.667%; background:rgba(91,227,143,.55); border-radius:99px 0 0 99px; } .gz.z2 { width:6.667%; background:rgba(91,227,143,.28); }
.gz.z3 { width:16.667%; background:rgba(255,201,74,.35); } .gz.z4 { width:16.667%; background:rgba(255,106,95,.25); } .gz.z5 { width:33.333%; background:rgba(255,106,95,.5); border-radius:0 99px 99px 0; }
.gm { position:absolute; top:-35%; height:170%; width:4px; margin-left:-2px; background:var(--paper); left:0; transition:left .4s cubic-bezier(.2,.8,.2,1); }
.gauge-l { position:relative; height:1.3em; font:400 var(--fs-xs) "GZ Plex Mono"; color:var(--dim); }
.gauge-l span { position:absolute; transform:translateX(-50%); }
.gauge-l span:nth-child(1) { left:0; transform:none; } .gauge-l span:nth-child(2) { left:26.667%; } .gauge-l span:nth-child(3) { left:33.333%; }
.gauge-l span:nth-child(4) { left:50%; } .gauge-l span:nth-child(5) { left:66.667%; } .gauge-l span:nth-child(6) { right:0; left:auto; transform:none; }

/* calculatrice */
.calc { display:grid; gap:var(--gap); grid-template-columns:minmax(0,1fr); align-items:start; }
%P .calc { grid-template-columns:700u minmax(0,1fr); gap:40u; }
%P .ctl { display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:12u 26u; align-content:start; }
%P .ctl .fw { grid-column:1 / -1; }
.ctl { gap:12px; } %P .ctl { gap:12u; }
.ctl .fld { display:grid; grid-template-columns:minmax(0,1fr) auto; align-items:center; gap:4px 10px; }
.ctl .fld > label { grid-column:1 / -1; }
.ctl .fld label { font:500 var(--fs-lab) "GZ Plex Mono"; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); }
.ctl .nb { display:flex; align-items:center; gap:6px; } .ctl .nb em { font-style:normal; color:var(--muted); font-size:var(--fs-s); min-width:1.6em; }
.ctl .nb input { width:7.5em; } %P .ctl .nb input { width:150u; }
.ctl input[type=range] { width:100%; accent-color:var(--gold); height:26px; margin:0; min-width:0; }
%P .ctl input[type=range] { height:22u; }
.seg { grid-column:1 / -1; display:flex; border:1px solid var(--line); border-radius:99px; overflow:hidden; }
.seg button { flex:1; padding:9px 8px; background:transparent; border:0; cursor:pointer; font:600 var(--fs-s) "GZ Plex Mono"; color:var(--muted); min-height:40px; }
%P .seg button { padding:9u 10u; min-height:0; }
.seg button[aria-pressed="true"] { background:var(--gold); color:var(--ink); }
.seg button:disabled { opacity:.4; cursor:not-allowed; }
.ctl .fld:has(.seg) { grid-template-columns:minmax(0,1fr); }
.res { display:flex; flex-direction:column; gap:12u; min-width:0; }
%P .res-grid div { display:flex; flex-direction:column; gap:2u; }
.res-top { display:flex; justify-content:space-between; align-items:flex-end; gap:12px; flex-wrap:wrap; }
.res-big { display:block; font:900 var(--fs-n2)/1 "GZ Archivo"; font-stretch:62%; color:var(--gold); font-variant-numeric:tabular-nums; }
.res-k { text-align:right; } .res-k span:last-child { font:600 var(--fs-n4) "GZ Plex Mono"; }
.res-grid { display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:8px 16px; }
%P .res-grid { grid-template-columns:repeat(6, minmax(0,1fr)); gap:14u; }
.res-grid b { font:600 var(--fs-b) "GZ Plex Mono"; font-variant-numeric:tabular-nums; white-space:nowrap; }
.warn { font-size:var(--fs-s); color:var(--neg); }
.calc-ch svg { min-width:0 !important; }
.leg { display:flex; gap:18px; flex-wrap:wrap; font:400 var(--fs-xs) "GZ Plex Mono"; color:var(--muted); }
.leg i { display:inline-block; width:22px; height:10px; border-radius:2px; margin-right:6px; vertical-align:middle; }
.leg i.dash { background:none; border-top:2px dashed var(--paper); height:0; }
.cmp-env { display:grid; gap:6u; }
.cmp-env .hb { padding:2u 0; } %P .cmp-env .hb-l small { display:inline; margin-left:.7em; }
.cmp-env .hb.sel .hb-l { color:var(--gold); font-weight:700; }

/* quiz */
.qz-q { gap:8u; } %P .qz-q .p { font-size:var(--fs-s); line-height:1.32; } %P .qz .card { padding:14u 18u; }
.opts { display:flex; flex-direction:column; gap:6u; }
%P .opts { flex-direction:row; flex-wrap:wrap; }
.opt { text-align:left; background:rgba(0,0,0,.2); border:1px solid var(--line); border-radius:8px; padding:8px 10px; cursor:pointer; font:600 var(--fs-s) "GZ Archivo", sans-serif; font-variant-numeric:tabular-nums; min-height:40px; }
%P .opt { padding:6u 10u; min-height:0; }
.opt:hover { border-color:var(--gold); }
.opt.ok { border-color:var(--pos); background:rgba(91,227,143,.15); } .opt.ko { border-color:var(--neg); background:rgba(255,106,95,.12); }
.why { font-size:var(--fs-xs); line-height:1.3; color:var(--muted); visibility:hidden; }
%P .qz-q .opt { font-size:var(--fs-xs); } .qz-q.done .why { visibility:visible; }
.score { color:var(--gold); font-family:"GZ Plex Mono"; }
.impression .opt.good { border-color:var(--pos); background:rgba(91,227,143,.15); } .impression .why { visibility:visible; }

/* glossaire, sources, check-list */
.gloss { display:grid; grid-template-columns:minmax(0,1fr); gap:6px 30u; align-content:start; }
%P .gloss { grid-template-columns:repeat(2, minmax(0,1fr)); gap:10u 50u; }
.gl { display:grid; grid-template-columns:8.5em minmax(0,1fr); gap:10px; padding:5u 0; border-bottom:1px solid var(--line2); font-size:var(--fs-s); line-height:1.3; }
%P .gl { font-size:calc(var(--fs-s) * .92); }
%P .gl { grid-template-columns:290u minmax(0,1fr); }
.gl dt { font-weight:800; color:var(--gold); } .gl dd { color:var(--paper); }
.srcs { columns:1; column-gap:40u; font-size:var(--fs-xs); line-height:1.35; }
%P .srcs { columns:3; }
.srcs li { break-inside:avoid; padding:3u 0 5u; color:var(--muted); overflow-wrap:anywhere; }
.srcs a { text-decoration:none; color:var(--paper); } .srcs a:hover { color:var(--gold); text-decoration:underline; }
.srcs .num { color:var(--gold); }
.chk { display:flex; flex-direction:column; gap:7u; }
.chk li { display:flex; gap:14px; align-items:baseline; font-size:var(--fs-b); line-height:1.35; padding-bottom:7u; border-bottom:1px solid var(--line2); }
.chk .num { color:var(--gold); font-size:.85em; }
.eq { display:flex; flex-direction:column; gap:6u; background:var(--card); border:1px solid var(--line); border-radius:var(--r); padding:12px 14px; }
%P .eq { padding:16u 24u; }
.eqv { font:900 var(--fs-n3)/1 "GZ Archivo"; font-stretch:62%; } .eqv i { font-style:normal; color:var(--dim); margin:0 .2em; } .eqv b { color:var(--gold); }


.st-c { gap:6u; } .st-c .tc-t { font-size:var(--fs-n4); }
/* flux ETF */
.flow { display:grid; grid-template-columns:minmax(0,1fr); gap:10px; }
%P .flow { grid-template-columns:minmax(0,1fr) auto minmax(0,1fr) auto minmax(0,1fr) auto minmax(0,1fr); align-items:stretch; gap:14u; }
.fl { gap:6u; } .fl .tc-t { font-size:var(--fs-n4); }
.fl-ar { display:none; } %P .fl-ar { display:flex; align-items:center; font:900 var(--fs-n3) "GZ Archivo"; color:var(--gold); }
.t.etf td { font-size:calc(var(--fs-t) * .9); } .t.etf td small { display:block; font-family:"GZ Plex Mono"; }
/* noyau et satellites, DCA */
.ns { display:flex; gap:8px; min-height:90px; }
%P .ns { min-height:170u; gap:12u; }
.ns > div { display:flex; flex-direction:column; justify-content:flex-end; gap:4u; padding:12px; border-radius:var(--r); }
%P .ns > div { padding:18u 20u; }
.ns-n { background:rgba(141,162,200,.25); border:1px solid var(--ndx); } .ns-s { background:rgba(255,201,74,.16); border:1px solid var(--gold); }
.ns b { font:900 var(--fs-n4)/1 "GZ Archivo"; font-stretch:62%; } .ns span { font-size:var(--fs-s); color:var(--muted); line-height:1.3; }
.px { display:grid; grid-template-columns:repeat(6, minmax(0,1fr)); gap:8px; align-items:end; height:120px; margin:4px 0 8px; }
%P .px { height:200u; gap:14u; }
.px-b { height:100%; display:flex; flex-direction:column; justify-content:flex-end; align-items:center; gap:3px; }
.px-b i { display:block; width:100%; background:var(--gold); opacity:.75; border-radius:4px 4px 0 0; transform-origin:bottom; }
.px-b span { order:-1; font:600 var(--fs-xs) "GZ Plex Mono"; } .px-b small { font:400 var(--fs-xs) "GZ Plex Mono"; color:var(--muted); }
.js .px-b i { transform:scaleY(0); } .js .on .px-b i { animation:growy .9s cubic-bezier(.2,.8,.2,1) both; animation-delay:calc(400ms + var(--i, 0) * 60ms); }
.impression .px-b i { animation:none !important; transform:none !important; }

/* ---------- mode présentation ---------- */
.pres { position:fixed; inset:0; overflow:hidden; background:#05070a; --W:min(100vw, calc((100vh - 46px) * 16 / 9)); }
.pres .stage { position:absolute; left:0; right:0; top:0; bottom:46px; }
.pres .slide { position:absolute; left:50%; top:50%; width:var(--W); height:calc(var(--W) * 9 / 16); margin:calc(var(--W) * -9 / 32) 0 0 calc(var(--W) / -2);
  opacity:0; visibility:hidden; transition:opacity .55s ease, visibility 0s linear .55s, transform .7s cubic-bezier(.2,.8,.2,1); transform:translateX(2.5%); }
.pres .slide.past { transform:translateX(-2.5%); }
.pres .slide.on { opacity:1; visibility:visible; transform:none; transition:opacity .55s ease, transform .7s cubic-bezier(.2,.8,.2,1); z-index:2; }
.ctrl { display:none; position:fixed; left:0; right:0; bottom:0; height:46px; align-items:center; gap:10px; padding:0 14px; background:#0b0e14; border-top:1px solid var(--line);
  font:500 12px "GZ Plex Mono", monospace; color:var(--muted); z-index:30; }
.pres .ctrl { display:flex; }
.ctrl button { background:transparent; border:1px solid var(--line); border-radius:6px; color:var(--paper); padding:5px 10px; cursor:pointer; font:600 12px "GZ Plex Mono", monospace; }
.ctrl button:hover { border-color:var(--gold); color:var(--gold); }
.ctrl .cn { min-width:5.5em; text-align:center; color:var(--paper); }
.ctrl .csec { color:var(--gold); text-transform:uppercase; letter-spacing:.1em; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:22em; }
.ctrl .prog { flex:1; height:4px; background:var(--line2); border-radius:2px; overflow:hidden; min-width:40px; }
.ctrl .prog i { display:block; height:100%; width:0; background:var(--gold); transition:width .45s ease; }
.ctrl .disc { color:var(--dim); font-size:10.5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:30em; }
@media (max-width:1300px) { .ctrl .disc { display:none; } }

/* ---------- mode lecture ---------- */
.lhead { display:none; }
.lecture .lhead, #gz:not(.pres):not(.impression) .lhead { display:flex; position:sticky; top:env(safe-area-inset-top, 0px); z-index:20; justify-content:space-between; align-items:center; gap:10px;
  padding:10px 16px; background:rgba(7,9,13,.94); border-bottom:1px solid var(--line); font:600 12px "GZ Plex Mono", monospace; letter-spacing:.1em; text-transform:uppercase; }
.lhead .btns { display:flex; gap:8px; }
.lhead button { background:transparent; border:1px solid var(--line); border-radius:6px; color:var(--paper); padding:7px 10px; font:600 11px "GZ Plex Mono"; cursor:pointer; min-height:36px; }
#gz:not(.pres):not(.impression) .stage { display:flex; flex-direction:column; gap:16px; padding:14px 16px 60px; max-width:1060px; margin:0 auto; }
#gz:not(.pres):not(.impression) .slide { border:1px solid var(--line); border-radius:14px; }
#gz:not(.pres):not(.impression) .op .op-in { min-height:260px; }

/* ---------- sommaire en surimpression ---------- */
.toc { position:fixed; inset:0; z-index:50; background:rgba(5,7,10,.96); overflow:auto; padding:24px 16px 40px; display:none; }
.toc.open { display:block; }
.toc-in { max-width:1200px; margin:0 auto; display:grid; gap:18px; grid-template-columns:repeat(auto-fill, minmax(260px, 1fr)); }
.toc h3 { font:900 22px/1 "GZ Archivo"; font-stretch:62%; text-transform:uppercase; color:var(--gold); margin:0 0 8px; }
.toc a { display:flex; gap:10px; padding:5px 0; text-decoration:none; font-size:14px; border-bottom:1px solid var(--line2); }
.toc a span { font-family:"GZ Plex Mono"; color:var(--dim); font-size:12px; min-width:2em; }
.toc a:hover { color:var(--gold); }
.toc .close { position:sticky; top:0; float:right; background:var(--gold); color:var(--ink); border:0; border-radius:6px; padding:8px 14px; font:700 12px "GZ Plex Mono"; cursor:pointer; }

/* ---------- animations (seulement avec JavaScript) ---------- */
.js .a { opacity:0; }
.js .on .a { animation:rise .8s cubic-bezier(.16,.84,.24,1) both; animation-delay:calc(140ms + var(--i, 0) * 60ms); }
@keyframes rise { from { opacity:0; transform:translateY(22px); } to { opacity:1; transform:none; } }
.js .hb-t i, .js .mini-b i, .js .rg-band { transform:scaleX(0); }
.js .on .hb-t i, .js .on .mini-b i, .js .on .rg-band { animation:growx 1.1s cubic-bezier(.2,.8,.2,1) both; animation-delay:calc(380ms + var(--i, 0) * 60ms); }
@keyframes growx { from { transform:scaleX(0); } to { transform:scaleX(1); } }
.js .fb i { transform:scaleY(0); }
.js .on .fb i { animation:growy 1s cubic-bezier(.2,.8,.2,1) both; animation-delay:calc(450ms + var(--i, 0) * 60ms); }
.js .gy { transform:scaleY(0); transform-box:fill-box; transform-origin:50% 100%; }
.js .on .gy { animation:growy .9s cubic-bezier(.2,.8,.2,1) both; animation-delay:calc(400ms + var(--i, 0) * 110ms); }
.js .gt { opacity:0; } .js .on .gt { animation:fade .5s ease both; animation-delay:calc(800ms + var(--i, 0) * 110ms); }
@keyframes growy { from { transform:scaleY(0); } to { transform:scaleY(1); } }
@keyframes fade { from { opacity:0; } to { opacity:1; } }
.js .ln { stroke-dasharray:1; stroke-dashoffset:1; } .js .on .ln { animation:draw 1.8s cubic-bezier(.4,0,.2,1) .5s both; }
@keyframes draw { to { stroke-dashoffset:0; } }
.js .on .wipe { animation:wipe 1.15s cubic-bezier(.7,0,.3,1) both; }
@keyframes wipe { 0% { transform:scaleX(0); transform-origin:left; } 48% { transform:scaleX(1); transform-origin:left; } 52% { transform:scaleX(1); transform-origin:right; } 100% { transform:scaleX(0); transform-origin:right; } }
.js .opn { opacity:0; } .js .on .opn { animation:opn 1.4s cubic-bezier(.16,.84,.24,1) .45s both; }
@keyframes opn { from { opacity:0; transform:translateY(8%) scale(.92); } to { opacity:1; transform:none; } }
.js .on .tape-in { animation:tape 40s linear infinite; }
@keyframes tape { from { transform:translateX(0); } to { transform:translateX(-50%); } }
.js .on .cv-t em { animation:glow 3.2s ease-in-out 1.2s infinite alternate; }
@keyframes glow { from { text-shadow:0 0 0 rgba(255,201,74,0); } to { text-shadow:0 0 40u rgba(255,201,74,.45); } }
.js .on .bg { animation:drift 18s ease-in-out infinite alternate; }
@keyframes drift { from { background-position:0 0, 0 0, 0 0, 0 0; } to { background-position:0 0, 0 0, 40u 40u, 40u 40u; } }
@media (prefers-reduced-motion: reduce) {
  .js .a, .js .hb-t i, .js .mini-b i, .js .rg-band, .js .fb i, .js .gy, .js .gt, .js .opn { animation:none !important; opacity:1; transform:none; }
  .js .ln { stroke-dashoffset:0; animation:none !important; } .js .wipe, .js .on .tape-in, .js .on .bg { animation:none !important; }
  .pres .slide { transition:none; }
}

/* ---------- impression (PDF A4 paysage) ---------- */
@page { size:A4 landscape; margin:0; }
.impression { background:var(--ink); }
.impression .stage { display:block; }
.impression .pg { width:297mm; height:210mm; display:flex; flex-direction:column; justify-content:center; align-items:center; gap:4mm; background:var(--ink);
  break-after:page; page-break-after:always; overflow:hidden; }
.impression .slide { width:277mm; height:155.8125mm; border:0.3mm solid rgba(242,237,226,.12); }
.impression .pgf { width:277mm; display:flex; justify-content:space-between; font:400 7.5pt "GZ Plex Mono", monospace; color:#8d96a8; }
.impression .a, .impression .hb-t i, .impression .mini-b i, .impression .rg-band, .impression .fb i, .impression .gy, .impression .gt, .impression .opn { animation:none !important; opacity:1 !important; transform:none !important; }
.impression .ln { stroke-dashoffset:0 !important; animation:none !important; } .impression .wipe { display:none; }
.impression .tape-in { animation:none !important; }
.impression .ctrl, .impression .lhead, .impression .toc { display:none !important; }
"""


def css():
    s = CSS_SRC.replace("%P ", ":is(.pres, .impression) ")
    s = re.sub(r"(?<![\w#.\-])(-?\d+(?:\.\d+)?)u(?![\w\-])", lambda m: f"calc({m.group(1)} * var(--u))", s)
    return s


JS = r"""
(function () {
  "use strict";
  var D = JSON.parse(document.getElementById("gz-data").textContent);
  var root = document.getElementById("gz");
  root.classList.add("js");
  var slides = Array.prototype.slice.call(root.querySelectorAll(".slide"));
  var N = slides.length, cur = 0, mode = null;
  slides.forEach(function (s) { s.querySelectorAll(".a").forEach(function (el, i) { el.style.setProperty("--i", i); }); });

  // ---------- formats (identiques à fr() et pct() de calcul.py)
  function fr(x, d, signe) {
    if (x === null || x === undefined || isNaN(x)) return "n.d.";
    var s = Math.abs(x).toFixed(d), parts = s.split("."), ent = parts[0], out = "";
    while (ent.length > 3) { out = " " + ent.slice(-3) + out; ent = ent.slice(0, -3); }
    out = ent + out + (parts[1] ? "," + parts[1] : "");
    var zero = parseFloat(s) === 0;
    if (x < 0 && !zero) return "−" + out;
    return (signe ? "+" : "") + out;
  }
  function eur(x) { return fr(x, 0) + " €"; }

  // ---------- compteurs animés
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function compter(sl) {
    if (reduce || root.classList.contains("impression")) return;
    sl.querySelectorAll(".cnt").forEach(function (el, k) {
      var v = parseFloat(el.dataset.v), d = parseInt(el.dataset.d, 10), suf = el.dataset.suf || "", pre = el.dataset.pre || "", sg = el.dataset.s === "1";
      var t0 = null, dur = 1300, delai = 250 + k * 90;
      function pas(t) {
        if (t0 === null) t0 = t;
        var p = Math.min(1, Math.max(0, (t - t0 - delai) / dur)), e = 1 - Math.pow(1 - p, 3);
        el.textContent = pre + fr(v * e, d, sg) + suf;
        if (p < 1) requestAnimationFrame(pas);
      }
      el.textContent = pre + fr(0, d, sg) + suf;
      requestAnimationFrame(pas);
    });
  }

  // ---------- navigation
  var cn = root.querySelector(".ctrl .cn"), csec = root.querySelector(".ctrl .csec"), prog = root.querySelector(".ctrl .prog i");
  function aller(i, sansHash) {
    i = Math.max(0, Math.min(N - 1, i));
    slides.forEach(function (s, k) { s.classList.toggle("on", k === i); s.classList.toggle("past", k < i); });
    cur = i;
    if (cn) cn.textContent = (i + 1) + " / " + N;
    if (csec) csec.textContent = slides[i].dataset.sec;
    if (prog) prog.style.width = ((i + 1) / N * 100) + "%";
    compter(slides[i]);
    if (!sansHash) { try { history.replaceState(null, "", "#s" + (i + 1)); } catch (e) {} }
  }
  function cible() { var m = /^#s(\d+)$/.exec(location.hash || ""); return m ? parseInt(m[1], 10) - 1 : null; }

  var io = null;
  function setMode(m) {
    mode = m;
    root.classList.toggle("pres", m === "pres");
    root.classList.toggle("lecture", m === "lecture");
    var b = root.querySelectorAll("[data-mode]");
    b.forEach(function (x) { x.textContent = m === "pres" ? "Mode lecture" : "Mode présentation"; });
    if (m === "pres") {
      if (io) { io.disconnect(); io = null; }
      slides.forEach(function (s) { s.classList.remove("on", "past"); });
      var c = cible(); aller(c === null ? cur : c, true);
    } else {
      slides.forEach(function (s) { s.classList.remove("on", "past"); });
      if ("IntersectionObserver" in window && !reduce) {
        io = new IntersectionObserver(function (es) {
          es.forEach(function (en) { if (en.isIntersecting && !en.target.classList.contains("on")) { en.target.classList.add("on"); compter(en.target); } });
        }, { threshold: 0.18 });
        slides.forEach(function (s) { io.observe(s); });
      } else { slides.forEach(function (s) { s.classList.add("on"); }); }
      var c2 = cible();
      if (c2 !== null && slides[c2]) setTimeout(function () { slides[c2].scrollIntoView(); }, 30);
    }
  }
  var mq = window.matchMedia("(min-width: 900px) and (min-height: 520px)");
  var force = null;
  try { force = localStorage.getItem("gz-mode"); } catch (e) {}
  function auto() { return force || (mq.matches ? "pres" : "lecture"); }
  if (mq.addEventListener) mq.addEventListener("change", function () { if (!force && !root.classList.contains("impression")) setMode(auto()); });
  root.querySelectorAll("[data-mode]").forEach(function (b) {
    b.addEventListener("click", function () {
      force = mode === "pres" ? "lecture" : "pres";
      try { localStorage.setItem("gz-mode", force); } catch (e) {}
      setMode(force);
    });
  });

  function champ(t) { return t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.tagName === "SELECT" || t.isContentEditable); }
  document.addEventListener("keydown", function (ev) {
    if (champ(ev.target)) return;
    var toc = root.querySelector(".toc");
    if (ev.key === "Escape" && toc.classList.contains("open")) { toc.classList.remove("open"); return; }
    if (ev.key === "t" || ev.key === "T") { toc.classList.toggle("open"); return; }
    if (mode !== "pres") return;
    if (["ArrowRight", "PageDown", " ", "Enter"].indexOf(ev.key) >= 0) { if (ev.target.tagName === "BUTTON" && ev.key !== "ArrowRight" && ev.key !== "PageDown") return; ev.preventDefault(); aller(cur + 1); }
    else if (["ArrowLeft", "PageUp", "Backspace"].indexOf(ev.key) >= 0) { ev.preventDefault(); aller(cur - 1); }
    else if (ev.key === "Home") { ev.preventDefault(); aller(0); }
    else if (ev.key === "End") { ev.preventDefault(); aller(N - 1); }
  });
  var tx = null, ty = null;
  root.addEventListener("touchstart", function (ev) { if (mode !== "pres" || champ(ev.target) || ev.target.closest("button")) { tx = null; return; } tx = ev.touches[0].clientX; ty = ev.touches[0].clientY; }, { passive: true });
  root.addEventListener("touchend", function (ev) {
    if (tx === null) return;
    var dx = ev.changedTouches[0].clientX - tx, dy = ev.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) aller(cur + (dx < 0 ? 1 : -1));
    tx = null;
  }, { passive: true });
  root.querySelector(".ctrl .prev").addEventListener("click", function () { aller(cur - 1); });
  root.querySelector(".ctrl .next").addEventListener("click", function () { aller(cur + 1); });
  root.querySelectorAll("[data-toc]").forEach(function (b) { b.addEventListener("click", function () { root.querySelector(".toc").classList.toggle("open"); }); });
  var fs = root.querySelector(".ctrl .fs");
  if (fs) fs.addEventListener("click", function () {
    try { if (document.fullscreenElement) document.exitFullscreen(); else { var p = document.documentElement.requestFullscreen && document.documentElement.requestFullscreen(); if (p && p.catch) p.catch(function () {}); } } catch (e) {}
  });
  root.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href^="#s"]');
    if (!a) return;
    var i = parseInt(a.getAttribute("href").slice(2), 10) - 1;
    if (isNaN(i)) return;
    ev.preventDefault();
    root.querySelector(".toc").classList.remove("open");
    if (mode === "pres") aller(i); else { slides[i].scrollIntoView({ behavior: reduce ? "auto" : "smooth" }); try { history.replaceState(null, "", "#s" + (i + 1)); } catch (e) {} }
  });
  window.addEventListener("hashchange", function () { var c = cible(); if (c !== null && mode === "pres") aller(c, true); });

  // ---------- calcul (traduction ligne à ligne de simuler() dans calcul.py)
  var P = D.params;
  function impotSortie(env, annees, gains, verse, couple) {
    if (gains <= 0) return 0;
    if (env === "PEA") return gains * (annees >= P.pea_duree ? P.ps : P.pfu);
    if (env === "CTO") return gains * P.pfu;
    if (annees < P.av_duree) return gains * (P.ir_pfu + P.ps_av);
    var abat = couple ? P.av_abat_couple : P.av_abat_seul;
    var partHaute = verse > 0 ? Math.max(0, verse - P.av_seuil) / verse : 0;
    var tauxIr = P.av_taux_reduit * (1 - partHaute) + P.ir_pfu * partHaute;
    return gains * P.ps_av + Math.max(0, gains - abat) * tauxIr;
  }
  function simuler(capital, mensuel, annees, rendement, frais, env, couple, inflation) {
    var g = Math.pow(1 + rendement, 1 / 12), k = Math.pow(1 - frais, 1 / 12);
    var v = capital, v0 = capital, verse = capital, serie = [{ annee: 0, verse: verse, valeur: v, sans_frais: v0 }];
    var mois = Math.round(annees * 12);
    for (var m = 1; m <= mois; m++) {
      v = v * g * k + mensuel; v0 = v0 * g + mensuel; verse += mensuel;
      if (m % 12 === 0) serie.push({ annee: m / 12, verse: verse, valeur: v, sans_frais: v0 });
    }
    var gains = v - verse, impot = impotSortie(env, annees, gains, verse, couple), net = v - impot;
    return { verse: verse, valeur: v, sans_frais: v0, cout_frais: v0 - v, gains: gains, impot: impot, net: net, reel: net / Math.pow(1 + (inflation || 0), annees), serie: serie };
  }
  window.GZ = { simuler: simuler, aller: function (i) { aller(i); }, fr: fr };

  var calc = document.getElementById("calc");
  if (calc) {
    var ids = ["cap", "men", "dur", "ren", "fra", "inf"], env = "PEA", couple = false;
    function val(id) { var x = parseFloat(document.getElementById("c-" + id + "-n").value); return isNaN(x) ? 0 : x; }
    ids.forEach(function (id) {
      var r = document.getElementById("c-" + id), n = document.getElementById("c-" + id + "-n");
      r.addEventListener("input", function () { n.value = r.value; maj(); });
      n.addEventListener("input", function () { var x = parseFloat(n.value); if (!isNaN(x)) { r.value = Math.min(parseFloat(r.max), Math.max(parseFloat(r.min), x)); } maj(); });
    });
    function seg(id, cb) {
      var bs = document.querySelectorAll("#" + id + " button");
      bs.forEach(function (b) { b.addEventListener("click", function () { bs.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); cb(b.dataset.v); maj(); }); });
    }
    seg("c-env", function (v) { env = v; });
    seg("c-foy", function (v) { couple = v === "1"; });
    var foy = document.querySelectorAll("#c-foy button");
    function svg(s) {
      var W = 1000, H = 250, l = 92, r = 40, t = 12, b = 214, se = s.serie, n = se.length - 1;
      var ymax = 0; se.forEach(function (p) { ymax = Math.max(ymax, p.sans_frais, p.valeur, p.verse); });
      var mag = Math.pow(10, Math.floor(Math.log10(Math.max(ymax, 1)))), st = mag;
      [1, 2, 2.5, 5, 10].some(function (m) { st = m * mag; return ymax / st <= 5; });
      var top = Math.ceil(ymax / st) * st || 1;
      function X(i) { return l + (n ? i / n : 0) * (W - l - r); }
      function Y(v) { return b - v / top * (b - t); }
      var o = "";
      for (var y = 0; y <= top + 1e-9; y += st) {
        o += '<line x1="' + l + '" x2="' + (W - r) + '" y1="' + Y(y).toFixed(1) + '" y2="' + Y(y).toFixed(1) + '" stroke="rgba(242,237,226,.08)"/>';
        o += '<text x="' + (l - 10) + '" y="' + (Y(y) + 7).toFixed(1) + '" text-anchor="end" font-size="20" fill="#8d96a8">' + (y >= 1e6 ? fr(y / 1e6, y % 1e6 ? 1 : 0) + " M€" : fr(y / 1000, 0) + " k€") + "</text>";
      }
      var pas = n <= 10 ? 1 : n <= 20 ? 5 : 10;
      for (var i = 0; i <= n; i += pas) o += '<text x="' + X(i).toFixed(1) + '" y="' + (b + 30) + '" text-anchor="' + (i === n ? "end" : i === 0 ? "start" : "middle") + '" font-size="20" fill="#8d96a8">' + i + " an" + (i > 1 ? "s" : "") + "</text>";
      function pts(f) { return se.map(function (p, i) { return X(i).toFixed(1) + "," + Y(f(p)).toFixed(1); }).join(" "); }
      o += '<polygon points="' + X(0).toFixed(1) + "," + b + " " + pts(function (p) { return p.valeur; }) + " " + X(n).toFixed(1) + "," + b + '" fill="rgba(255,201,74,.16)"/>';
      o += '<polygon points="' + X(0).toFixed(1) + "," + b + " " + pts(function (p) { return p.verse; }) + " " + X(n).toFixed(1) + "," + b + '" fill="rgba(242,237,226,.22)"/>';
      o += '<polyline points="' + pts(function (p) { return p.sans_frais; }) + '" fill="none" stroke="#f2ede2" stroke-width="2.5" stroke-dasharray="8 7"/>';
      o += '<polyline points="' + pts(function (p) { return p.valeur; }) + '" fill="none" stroke="#ffc94a" stroke-width="4.5" stroke-linejoin="round"/>';
      return o;
    }
    function maj() {
      var c = val("cap"), m = val("men"), n = Math.max(1, Math.round(val("dur"))), r = val("ren") / 100, f = val("fra") / 100, inf = val("inf") / 100;
      foy.forEach(function (b) { b.disabled = env !== "AV"; });
      var s = simuler(c, m, n, r, f, env, couple, inf);
      document.getElementById("r-net").textContent = eur(s.net);
      document.getElementById("r-reel").textContent = eur(s.reel);
      document.getElementById("r-verse").textContent = eur(s.verse);
      document.getElementById("r-brut").textContent = eur(s.valeur);
      document.getElementById("r-gain").textContent = eur(s.gains);
      document.getElementById("r-frais").textContent = eur(s.cout_frais);
      document.getElementById("r-imp").textContent = eur(s.impot);
      document.getElementById("r-mult").textContent = s.verse > 0 ? "×" + fr(s.net / s.verse, 2) : "—";
      var w = document.getElementById("r-warn"), msg = [];
      if (env === "PEA" && s.verse > P.pea_plafond) msg.push("Plafond de versements du PEA dépassé : " + eur(P.pea_plafond) + ".");
      if (env === "PEA" && n < P.pea_duree) msg.push("Retrait avant " + P.pea_duree + " ans : le plan est clos et les gains paient la flat tax.");
      if (env === "AV" && n < P.av_duree) msg.push("Avant " + P.av_duree + " ans, l'assurance-vie taxe les gains à " + fr((P.ir_pfu + P.ps_av) * 100, 1) + " %.");
      w.textContent = msg.join(" "); w.hidden = msg.length === 0;
      document.getElementById("r-svg").innerHTML = svg(s);
      var envs = [["PEA", false, "PEA"], ["AV", couple, "Assurance-vie" + (couple ? " (couple)" : "")], ["CTO", false, "Compte-titres"]], res = [], mx = 0;
      envs.forEach(function (x) { var z = simuler(c, m, n, r, f, x[0], x[1], inf); res.push([x, z]); mx = Math.max(mx, z.net); });
      document.getElementById("r-cmp").innerHTML = '<span class="lab">Même calcul dans les trois enveloppes, après impôts</span>' + res.map(function (q) {
        var fr_ = mx > 0 ? Math.max(0, q[1].net) / mx * 100 : 0, sel = q[0][0] === env;
        return '<div class="hb' + (sel ? " sel" : "") + '" style="--c:' + (sel ? "var(--gold)" : "rgba(242,237,226,.45)") + '"><span class="hb-l">' + q[0][2] + '<small>impôts ' + eur(q[1].impot) + '</small></span><span class="hb-t"><i style="width:' + fr_.toFixed(2) + '%;transform:none;animation:none"></i></span><span class="hb-v">' + eur(q[1].net) + "</span></div>";
      }).join("");
    }
    maj();
    window.GZ.majCalc = maj;
  }

  // ---------- PEG
  var pc = root.querySelector(".pegcalc");
  if (pc) {
    var s = { forte: +pc.dataset.forte, zone: +pc.dataset.zone, elig: +pc.dataset.elig, vente: +pc.dataset.vente };
    function majPeg() {
      var pe = parseFloat(document.getElementById("peg-pe").value), g = parseFloat(document.getElementById("peg-g").value);
      if (!(pe > 0) || !(g > 0)) return;
      var peg = pe / g, txt;
      if (peg <= s.forte) txt = "zone de forte sécurité";
      else if (peg <= s.zone) txt = "dans la zone d'achat";
      else if (peg <= s.elig) txt = "éligible à la méthode, au-dessus de la zone d'achat";
      else if (peg <= s.vente) txt = "trop cher pour la méthode";
      else txt = "au-dessus de " + fr(s.vente, 0) + " : vendre la moitié d'une ligne détenue";
      document.getElementById("peg-v").textContent = fr(peg, 2);
      document.getElementById("peg-txt").textContent = txt;
      document.getElementById("peg-m").style.left = Math.min(100, peg / 3 * 100) + "%";
    }
    ["peg-pe", "peg-g"].forEach(function (id) { document.getElementById(id).addEventListener("input", majPeg); });
    majPeg();
  }

  // ---------- quiz
  var score = 0, rep = 0, total = root.querySelectorAll(".qz-q").length, sc = document.getElementById("qz-score");
  root.querySelectorAll(".qz-q").forEach(function (q) {
    q.querySelectorAll(".opt").forEach(function (b) {
      b.addEventListener("click", function () {
        if (q.classList.contains("done")) return;
        q.classList.add("done"); rep++;
        var ok = b.dataset.ok === "1"; if (ok) score++;
        b.classList.add(ok ? "ok" : "ko");
        q.querySelector('.opt[data-ok="1"]').classList.add("ok");
        if (sc) sc.textContent = " Score : " + score + " / " + rep + (rep === total ? " — terminé." : "");
      });
    });
  });

  // ---------- impression (appelée par pdf.js)
  window.GZ.impression = function () {
    if (io) { io.disconnect(); io = null; }
    root.classList.remove("pres", "lecture"); root.classList.add("impression");
    var stage = root.querySelector(".stage");
    slides.forEach(function (s, i) {
      s.classList.add("on"); s.classList.remove("past");
      var pg = document.createElement("div"); pg.className = "pg";
      stage.insertBefore(pg, s); pg.appendChild(s);
      var f = document.createElement("div"); f.className = "pgf";
      f.innerHTML = "<span>* La Gazette du PEG est un titre fictif, sans lien avec une publication existante. Analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé.</span><span>" + (i + 1) + " / " + N + "</span>";
      pg.appendChild(f);
    });
  };

  if (/^#impression$/.test(location.hash)) window.GZ.impression();
  else setMode(auto());
})();
"""


def fonts_css():
    def b64(nom):
        with open(os.path.join(FONTS, nom), "rb") as f:
            return base64.b64encode(f.read()).decode()
    faces = [("GZ Archivo", "archivo-latin-wdth-normal.woff2", "100 900", "normal", "font-stretch:62% 125%;"),
             ("GZ Newsreader", "newsreader-latin-opsz-normal.woff2", "200 800", "normal", ""),
             ("GZ Newsreader", "newsreader-latin-opsz-italic.woff2", "200 800", "italic", ""),
             ("GZ Plex Mono", "ibm-plex-mono-latin-400-normal.woff2", "400", "normal", ""),
             ("GZ Plex Mono", "ibm-plex-mono-latin-500-normal.woff2", "500", "normal", ""),
             ("GZ Plex Mono", "ibm-plex-mono-latin-600-normal.woff2", "600", "normal", "")]
    return "".join(f'@font-face{{font-family:"{fam}";src:url(data:font/woff2;base64,{b64(fn)}) format("woff2");font-weight:{w};font-style:{st};{ex}font-display:block;}}\n'
                   for fam, fn, w, st, ex in faces)


def build(fragment=None):
    # première passe pour compter les sources, seconde pour le rendu définitif
    rendre(2)
    n_src = max(1, math.ceil(len(S.liste) / 42))
    slides = rendre(n_src)
    N = len(slides)
    toc = []
    for sec, num, _ in SECTIONS:
        items = "".join(f'<a href="#s{i + 1}"><span>{i + 1:02d}</span>{e(s["titre"])}</a>' for i, s in enumerate(SL) if s["sec"] == sec)
        toc.append(f'<div><h3>{(num + " · ") if num else ""}{e(sec)}</h3>{items}</div>')
    data = {"params": D["params"]}
    titre = "Formation GARP"
    corps = f'''<div id="gz" lang="fr">
<div class="lhead"><span>La Gazette du PEG* · Formation GARP</span><span class="btns"><button type="button" data-toc>Sommaire</button><button type="button" data-mode>Mode présentation</button></span></div>
<main class="stage">
{chr(10).join(slides)}
</main>
<nav class="ctrl" aria-label="Navigation">
  <button type="button" class="prev" aria-label="Diapositive précédente">◀</button><span class="cn">1 / {N}</span><button type="button" class="next" aria-label="Diapositive suivante">▶</button>
  <span class="csec"></span><span class="prog"><i></i></span><span class="disc">* Titre fictif · analyse datée, pas un conseil personnalisé · ← → pour naviguer, T pour le sommaire</span>
  <button type="button" data-toc>Sommaire</button><button type="button" data-mode>Mode lecture</button><button type="button" class="fs" aria-label="Plein écran">⛶</button>
</nav>
<div class="toc" role="dialog" aria-label="Sommaire"><button type="button" class="close" data-toc>Fermer</button><div class="toc-in">{"".join(toc)}</div></div>
</div>
<script type="application/json" id="gz-data">{json.dumps(data, ensure_ascii=False)}</script>
<script>{JS}</script>'''
    style = f"<style>\n{fonts_css()}{css()}</style>"
    desc = "Diaporama de formation au stock picking GARP pour un investisseur français débutant, avec calculatrice d'intérêts composés."
    complet = (f'<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
               f'<title>{titre}</title>\n<meta name="description" content="{e(desc)}">\n{style}\n</head>\n<body>\n{corps}\n</body>\n</html>\n')
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(complet)
    if fragment:
        with open(fragment, "w", encoding="utf-8") as f:
            f.write(f'<title>{titre}</title>\n<meta name="description" content="{e(desc)}">\n{style}\n{corps}\n')
    with open(os.path.join(OUT, "plan.json"), "w", encoding="utf-8") as f:
        json.dump([{"n": i + 1, "section": s["sec"], "titre": s["titre"]} for i, s in enumerate(SL)], f, ensure_ascii=False, indent=1)
    print(f"diaporama/index.html : {N} diapositives, {len(S.liste)} sources, {len(complet) / 1e6:.2f} Mo")


if __name__ == "__main__":
    frag = None
    if "--fragment" in sys.argv:
        frag = sys.argv[sys.argv.index("--fragment") + 1]
    build(frag)
