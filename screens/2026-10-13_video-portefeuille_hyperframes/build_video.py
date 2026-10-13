#!/usr/bin/env python3
"""Génère la composition HyperFrames de la vidéo (video/index.html) à partir des données du modèle.

Stdlib uniquement : `python3 calcul.py && python3 build_video.py`.

Tous les nombres affichés viennent de video/donnees_video.json, écrit par calcul.py à partir des
CSV de data/. Le HTML ne contient aucun chiffre saisi à la main, sauf l'exemple pédagogique du PEG
(P/E de 20, croissance de 20 % puis 40 %), signalé comme tel à l'écran.

Rendu : voir RAPPORT.md (npx hyperframes lint / check / snapshot / render).
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.join(HERE, "video")
D = json.load(open(os.path.join(VIDEO, "donnees_video.json"), encoding="utf-8"))
NB = " "

W, H = 1920, 1080
TOTAL = 194.0
# Début de chaque scène (secondes) : la transition d'entrée commence à cet instant.
SCENES = [
    ("s1", 0.0, None), ("s2", 8.6, "blur"), ("s3", 15.6, "push"), ("s4", 26.6, "blocks"),
    ("c1", 30.6, "push"), ("c2", 39.2, "push"), ("c3", 47.8, "push"), ("c4", 56.4, "push"),
    ("c5", 65.0, "push"), ("s5", 73.6, "blocks"), ("s6", 83.6, "push"), ("s7", 95.6, "vpush"),
    ("s8", 107.6, "blur"), ("s9", 113.6, "blocks"), ("s10", 139.6, "blocks"), ("s11", 150.6, "blur"),
    ("s12", 156.6, "blocks"), ("s13", 171.6, "push"), ("s14", 181.6, "blur"), ("s15", 187.6, "blur"),
]
MEGA_T = [0.0, 5.5, 11.0, 16.5, 22.0]  # sous-panneaux de s9 (relatifs à son début)
SECTIONS = [  # (instant, libellé du bandeau)
    (0.0, "01 · Le pari"), (8.6, "02 · La méthode"), (26.6, "03 · Les cinq valeurs"),
    (73.6, "04 · Les bénéfices"), (83.6, "05 · Face à l'indice"), (113.6, "06 · Les méga-tendances"),
    (139.6, "07 · Le rétroviseur"), (156.6, "08 · Les scénarios"), (171.6, "09 · Les risques"),
    (181.6, "10 · À retenir"),
]

E = html.escape
V = D["valeurs"]
P, N, NH = D["portefeuille"], D["nasdaq"], D["nasdaq_hm"]
CIT = D["citations"]
COUL = {v["ticker"]: v["couleur"] for v in V}
GOLD, NDX, SPY = "#ffc94a", "#8da2c8", "#c9ced8"


def words(texte, cls="w"):
    return " ".join(f'<span class="{cls}">{E(m)}</span>' for m in texte.split())


def date_fr(iso):
    if len(iso) == 10 and iso[4] == "-":
        a, m, j = iso.split("-")
        return f"{j}/{m}/{a}"
    return iso


def chip(v, extra=""):
    return (f'<span class="chip {extra}" style="--c:{v["couleur"]}"><i></i>{E(v["symbole"])}</span>')


# --------------------------------------------------------------------------
# Scènes
# --------------------------------------------------------------------------
def scene_intro():
    tape = "".join(
        f'<span class="tk"><b style="color:{v["couleur"]}">{E(v["symbole"])}</b> {E(v["prix"])} '
        f'<em class="{"neg" if v["chg_52s_v"] < 0 else "pos"}">{E(v["chg_52s"])}</em> <s>12 mois</s></span>'
        for v in V)
    return f"""
<div class="scene" id="s1">
  <div class="kicker mono" id="s1-kick">Enquête · méthode PEG de Peter Lynch · horizon {D['horizon']} ans</div>
  <h1 class="s1-title cond">
    <span class="l" id="s1l1">Cinq valeurs</span>
    <span class="l" id="s1l2">pour battre</span>
    <span class="l" id="s1l3">le <em>Nasdaq 100</em></span>
  </h1>
  <div class="s1-chips">{''.join(chip(v) for v in V)}</div>
  <div class="s1-hook" id="s1-hook">
    <div class="mono lab">Rendement espéré modélisé, par an</div>
    <div class="cond big gold"><span class="num" id="s1-num" data-final="{E(P['esperance'])}">+0,0{NB}%</span></div>
    <div class="vs">contre <b style="color:{NDX}">{E(N['esperance'])}</b> pour le Nasdaq 100 reconstitué</div>
    <div class="mono sub">Moyenne de trois scénarios (25/50/25), du {D['date_analyse']} au même jour de 2030. Ce n'est pas une prévision.</div>
  </div>
  <div class="tape" id="s1-tape"><div class="tape-in" id="s1-tape-in">{tape}{tape}{tape}</div></div>
</div>"""


def scene_quote(sid, cid, contexte, bg_word):
    c = CIT[cid]
    date = date_fr(c["date"])
    return f"""
<div class="scene quote" id="{sid}">
  <div class="ghost cond" aria-hidden="true" data-layout-allow-overflow data-layout-allow-overlap>{E(bg_word)}</div>
  <div class="bigq serif" id="{sid}-q">“</div>
  <div class="qwrap">
    <blockquote class="q-en serif" id="{sid}-en">{words(c['texte_original'])}</blockquote>
    <p class="q-fr" id="{sid}-fr">« {E(c['traduction'])} »</p>
    <div class="q-attr" id="{sid}-attr"><span class="rule" id="{sid}-rule"></span>
      <span class="mono"><b>{E(c['auteur'])}</b> · {E(c['fonction'])} · {E(c['occasion'])}, {E(date)}</span></div>
    <div class="mono q-ctx" id="{sid}-ctx">{E(contexte)}</div>
  </div>
</div>"""


def scene_peg():
    ticks = "".join(f'<span class="gt" style="left:{x / 3 * 100:.4f}%">{lab}</span>'
                    for x, lab in ((0, "0"), (0.5, "0,5"), (1, "1"), (1.5, "1,5"), (2, "2"), (3, "3")))
    return f"""
<div class="scene" id="s3">
  <h2 class="title cond" id="s3-t">Le PEG : la croissance au juste prix</h2>
  <p class="lede" id="s3-l">Peter Lynch divise le P/E par la croissance annuelle du bénéfice par action. Sous 1, la croissance est bon marché.</p>
  <div class="eq">
    <div class="tile" id="s3-a"><div class="mono">P/E 12 mois</div><div class="cond tv" id="s3-pe">20</div></div>
    <div class="op cond" id="s3-o1">÷</div>
    <div class="tile" id="s3-b"><div class="mono">Croissance du BPA, par an</div><div class="cond tv"><span id="s3-g">20</span>{NB}%</div></div>
    <div class="op cond" id="s3-o2">=</div>
    <div class="tile gold-b" id="s3-c"><div class="mono">PEG</div><div class="cond tv gold" id="s3-peg">1,0</div></div>
  </div>
  <div class="gauge" id="s3-gauge">
    <div class="gz z1"><span>Aubaine</span></div><div class="gz z2"><span>Juste prix</span></div><div class="gz z3"><span>Cher</span></div>
    <div class="gticks">{ticks}</div>
    <div class="gmark" id="s3-mark"><i></i><span class="mono" id="s3-mark-l">Exemple</span></div>
  </div>
  <div class="defs mono" id="s3-defs">
    <div><b>P/E 12 mois</b> : cours ÷ bénéfice par action (BPA) attendu sur les 12 prochains mois.</div>
    <div><b>BPA non-GAAP</b> : BPA ajusté des éléments exceptionnels, consensus Zacks du {D['date_analyse']}. Exemple chiffré pédagogique.</div>
  </div>
</div>"""


def scene_roster():
    rows = "".join(f"""
    <div class="rrow" id="s4-r{i}" style="--c:{v['couleur']}">
      <i class="rbar"></i><span class="rsym cond">{E(v['symbole'])}</span>
      <span class="rname">{E(v['nom'])}<small>{E(v['theme'])}</small></span>
      <span class="rw mono">{E(v['poids'])}</span>
    </div>""" for i, v in enumerate(V))
    return f"""
<div class="scene" id="s4">
  <h2 class="title cond" id="s4-t">Cinq valeurs, cinq moteurs</h2>
  <div class="roster">{rows}</div>
  <div class="foot mono" id="s4-f">Poids égaux (hyp.) : aucune pondération n'a été fixée. Cours du {D['date_cours']}, consensus Zacks du {D['date_analyse']}.</div>
</div>"""


BASE_Y, BAR_MAX = 430, 270


def scene_card(i, v):
    c = v["citation"]
    h26 = BAR_MAX * v["bpa26_v"] / max(v["bpa26_v"], v["bpa27_v"])
    h27 = BAR_MAX * v["bpa27_v"] / max(v["bpa26_v"], v["bpa27_v"])
    pea = "Éligible au PEA" if v["pea"].startswith("oui") else "Compte-titres"
    adr = " · calculs sur l'ADR ADYEY (1/100 d'action)" if v["ticker"] == "ADYEY" else ""
    cit = c["texte"]
    ouvre = "« … " if cit[:1].islower() else "« "
    ferme = " … »" if cit[:1].islower() else " »"
    return f"""
<div class="scene card" id="c{i}" style="--c:{v['couleur']}">
  <div class="halo" id="c{i}-halo"></div>
  <div class="csym cond" id="c{i}-sym">{''.join(f'<span class="ch">{E(x)}</span>' for x in v['symbole'])}</div>
  <div class="cname" id="c{i}-name">{E(v['nom'])}<small>{E(v['theme'])}</small></div>
  <div class="cmeta mono" id="c{i}-meta">Cours {E(v['prix'])} · 12 mois {E(v['chg_52s'])} · Zacks Rank {E(v['zacks_rank'])}{E(adr)}</div>
  <div class="ctags" id="c{i}-tags"><span class="tag">Poids {E(v['poids'])}</span><span class="tag">{pea}</span></div>
  <div class="cquote" id="c{i}-q">
    <div class="serif cq-en">{E(ouvre)}{E(cit)}{E(ferme)}</div>
    <div class="cq-fr">{E(c['traduction'])}</div>
    <div class="mono cq-a">{E(c['auteur'])}, {E(c['fonction'])} · {E(date_fr(c['date']))}</div>
  </div>
  <div class="panel" id="c{i}-panel">
    <div class="mono ph">BPA non-GAAP · consensus Zacks · années civiles</div>
    <div class="bar b1" id="c{i}-b1" style="height:{h26:.1f}px"></div>
    <div class="bar b2" id="c{i}-b2" style="height:{h27:.1f}px"></div>
    <div class="bv mono" id="c{i}-v1" style="top:{BASE_Y - h26 - 52:.1f}px;left:40px" data-final="{E(v['bpa26'])}{NB}$">0,00{NB}$</div>
    <div class="bv mono" id="c{i}-v2" style="top:{BASE_Y - h27 - 52:.1f}px;left:240px" data-final="{E(v['bpa27'])}{NB}$">0,00{NB}$</div>
    <div class="by mono" style="left:70px">2026</div><div class="by mono" style="left:270px">2027</div>
    <div class="growth" id="c{i}-g"><div class="cond gv">{E(v['g27'])}</div><div class="mono">croissance du BPA en 2027</div></div>
    <div class="tiles">
      <div class="st" id="c{i}-t1"><div class="mono">P/E 12 mois</div><div class="cond">{E(v['pe'])}</div></div>
      <div class="st" id="c{i}-t2"><div class="mono">PEG long terme</div><div class="cond">{E(v['peg_lt'])}</div></div>
      <div class="st" id="c{i}-t3"><div class="mono">Croissance retenue (hyp.)</div><div class="cond">{E(v['g_lt'])}<small>/an</small></div></div>
    </div>
    <div class="mini" id="c{i}-mini"><div class="mz"></div><span class="mono m0">0</span><span class="mono m1">PEG 1</span><span class="mono m2">2</span>
      <div class="mm" id="c{i}-mm"><i></i></div></div>
    <div class="pfoot mono" id="c{i}-pf">Rendement espéré {E(v['esperance'])}/an · pessimiste {E(v['bear'])} · optimiste {E(v['bull'])}<br>Zone d'achat de Lynch (PEG 1) : {E(v['zone'])}, cours {E(v['ecart_zone'])} par rapport à la zone</div>
  </div>
</div>"""


def scene_growth():
    rows = [(v["nom"], v["g27_v"], v["g27"], v["couleur"], "") for v in sorted(V, key=lambda v: -v["g27_v"])]
    rows += [("Portefeuille", P["g27_v"], P["g27"], GOLD, "agg"),
             ("Nasdaq 100 reconstitué", N["g27_v"], N["g27"], NDX, "agg"),
             ("Nasdaq 100 hors mémoire", NH["g27_v"], NH["g27"], SPY, "agg")]
    gmax = max(r[1] for r in rows)
    html_rows = "".join(f"""
    <div class="grow {cls}" id="s5-r{i}" style="--c:{col}">
      <span class="gl">{E(nom)}</span><span class="gtrack"><i class="gb" id="s5-b{i}" style="width:{g / gmax * 100:.2f}%"></i></span>
      <span class="gvv mono" id="s5-v{i}" data-final="{E(txt)}" data-v="{g:.4f}">+0{NB}%</span>
    </div>""" for i, (nom, g, txt, col, cls) in enumerate(rows))
    return f"""
<div class="scene" id="s5">
  <h2 class="title cond" id="s5-t">Des bénéfices qui accélèrent</h2>
  <p class="lede" id="s5-l">Croissance du BPA non-GAAP attendue en 2027 par le consensus (années civiles). Celle de l'indice est gonflée par deux cycliques au sommet.</p>
  <div class="growth-list">{html_rows}</div>
  <div class="callout mono" id="s5-call">Micron et Sandisk, mémoire au pic du cycle : sans eux, la croissance du Nasdaq 100 tombe à {E(NH['g27'])}.</div>
  <div class="foot mono" id="s5-f">Moyennes pondérées par les bénéfices. Nasdaq 100 reconstitué : {D['ndx_lignes']} valeurs, {E(D['ndx_couverture'])} du poids du QQQ (composition du 30/09/2026).</div>
</div>"""


def scene_duel():
    lignes = [
        ("P/E 12 mois", P["pe"], N["pe"], P["pe_v"] < N["pe_v"], "pe"),
        ("Croissance du BPA 2027 (consensus)", P["g27"], N["g27"], P["g27_v"] > N["g27_v"], "g27"),
        ("Croissance retenue 2027-2030 (hyp.)", P["g_lt"], N["g_lt"], P["g_lt_v"] > N["g_lt_v"], "glt"),
        ("PEG long terme", P["peg_lt"], N["peg_lt"], P["peg_lt_v"] < N["peg_lt_v"], "peg"),
        ("Bêta (volatilité relative)", P["beta"], N["beta"], False, "beta"),
    ]
    rows = "".join(f"""
    <div class="drow" id="s6-r{i}">
      <span class="dl cond {'win' if w else ''}" id="s6-l{i}">{E(a)}</span>
      <span class="dc mono">{E(lab)}</span>
      <span class="dr cond {'' if w else 'win'}" id="s6-x{i}">{E(b)}</span>
    </div>""" for i, (lab, a, b, w, k) in enumerate(lignes))
    return f"""
<div class="scene" id="s6">
  <div class="dhead">
    <div class="dh l" id="s6-hl"><span class="cond gold">Portefeuille</span><span class="mono">5 valeurs × 20 %</span></div>
    <div class="dvs cond" id="s6-vs">vs</div>
    <div class="dh r" id="s6-hr"><span class="cond" style="color:{NDX}">Nasdaq 100</span><span class="mono">reconstitué : {D['ndx_lignes']} valeurs, {E(D['ndx_couverture'])} du poids</span></div>
  </div>
  <i class="dsplit" id="s6-split"></i>
  <div class="drows">{rows}</div>
  <div class="foot mono" id="s6-f">Hors mémoire, le Nasdaq 100 cote {E(NH['pe'])} fois ses bénéfices, pour un PEG long terme de {E(NH['peg_lt'])}. Le portefeuille est plus volatil : bêta de {E(P['beta'])} contre {E(N['beta'])}.</div>
</div>"""


# Nuage P/E contre croissance retenue
SX0, SY0, SPW, SPH, XMAX, YMAX = 120, 630, 1000, 560, 30.0, 30.0


def sx(g):
    return SX0 + g / XMAX * SPW


def sy(pe):
    return SY0 - pe / YMAX * SPH


def scene_scatter():
    pts = [(v["symbole"], v["g_lt_v"], v["pe_v"], v["couleur"], "dot") for v in V]
    pts += [("Portefeuille", P["g_lt_v"], P["pe_v"], GOLD, "star"),
            ("Nasdaq 100", N["g_lt_v"], N["pe_v"], NDX, "idx"),
            ("Nasdaq 100 hors mémoire", NH["g_lt_v"], NH["pe_v"], SPY, "idx")]
    off = {"NVDA": (-22, 8, "end"), "TSM": (-22, 4, "end"), "NU": (22, 8, "start"),
           "RDDT": (22, 8, "start"), "ADYEN": (24, -10, "start"), "Portefeuille": (26, 34, "start"),
           "Nasdaq 100": (-26, 8, "end"), "Nasdaq 100 hors mémoire": (-26, 8, "end")}
    els = []
    for i, (nom, g, pe, col, kind) in enumerate(pts):
        x, y = sx(g), sy(pe)
        dx, dy, anc = off[nom]
        if kind == "star":
            forme = f'<path d="M0,-22 L6,-7 L22,-7 L9,3 L14,19 L0,9 L-14,19 L-9,3 L-22,-7 L-6,-7 Z" fill="{col}"/>'
        elif kind == "idx":
            forme = f'<path d="M0,-16 L16,0 L0,16 L-16,0 Z" fill="none" stroke="{col}" stroke-width="4"/>'
        else:
            forme = f'<circle cx="0" cy="0" r="13" fill="{col}"/>'
        shape = f'<g transform="translate({x:.1f},{y:.1f})"><g class="pt" id="s7-p{i}">{forme}</g></g>'
        els.append(shape + f'<text class="plab" id="s7-t{i}" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anc}" fill="{col}">{E(nom)}</text>')
    gx = "".join(f'<text class="ax" x="{sx(g):.1f}" y="{SY0 + 36}" text-anchor="middle">{g} %</text>'
                 f'<line class="gridl" x1="{sx(g):.1f}" y1="{SY0}" x2="{sx(g):.1f}" y2="{SY0 - SPH}"/>'
                 for g in (0, 5, 10, 15, 20, 25, 30))
    gy = "".join(f'<text class="ax" x="{SX0 - 18}" y="{sy(p) + 8:.1f}" text-anchor="end">{p}</text>'
                 f'<line class="gridl" x1="{SX0}" y1="{sy(p):.1f}" x2="{SX0 + SPW}" y2="{sy(p):.1f}"/>'
                 for p in (0, 10, 20, 30))
    zone = f"M{sx(0)},{sy(0)} L{sx(30)},{sy(30)} L{sx(30)},{sy(0)} Z"
    return f"""
<div class="scene" id="s7">
  <h2 class="title cond" id="s7-t">Le nuage de Lynch</h2>
  <svg class="scatter" id="s7-svg" viewBox="0 0 1180 730" width="1180" height="730">
    {gy}{gx}
    <path id="s7-zone" d="{zone}" fill="{GOLD}" fill-opacity="0.07"/>
    <line class="pegl" id="s7-l1" x1="{sx(0)}" y1="{sy(0)}" x2="{sx(30):.1f}" y2="{sy(30):.1f}"/>
    <line class="pegl dash" id="s7-l15" x1="{sx(0)}" y1="{sy(0)}" x2="{sx(20):.1f}" y2="{sy(30):.1f}"/>
    <text class="pegt" id="s7-tl1" x="{sx(27.5):.1f}" y="{sy(27.5) + 34:.1f}" text-anchor="middle">PEG = 1</text>
    <text class="pegt" id="s7-tl15" x="{sx(11) - 14:.1f}" y="{sy(16.5) - 6:.1f}" text-anchor="end">PEG = 1,5</text>
    <text class="axt" x="{SX0 + SPW / 2}" y="{SY0 + 74}" text-anchor="middle">Croissance retenue du BPA, par an</text>
    <text class="axt" x="{SX0 - 70}" y="{SY0 - SPH / 2}" text-anchor="middle" transform="rotate(-90 {SX0 - 70} {SY0 - SPH / 2})">P/E 12 mois</text>
    {''.join(els)}
  </svg>
  <div class="side" id="s7-side">
    <div class="mono" id="s7-l">P/E 12 mois contre croissance annuelle du BPA retenue pour 2027-2030 (hyp.). Sous la droite PEG = 1, la croissance est payée moins d'une fois son taux.</div>
    <div class="sv" id="s7-s1"><span class="mono">PEG long terme · portefeuille</span><b class="cond gold">{E(P['peg_lt'])}</b></div>
    <div class="sv" id="s7-s2"><span class="mono">Nasdaq 100 reconstitué</span><b class="cond" style="color:{NDX}">{E(N['peg_lt'])}</b></div>
    <div class="sv" id="s7-s3"><span class="mono">Nasdaq 100 hors mémoire</span><b class="cond" style="color:{SPY}">{E(NH['peg_lt'])}</b></div>
    <div class="mono note">Micron et Sandisk, cycliques, sont modélisés à part : leurs bénéfices de 2030 retombent, ce qui écrase la croissance de l'indice.</div>
  </div>
</div>"""


def scene_mega():
    panels = []
    for i, m in enumerate(D["megatendances"], 1):
        cols = [x for x in V if x["nom"] in m["valeurs"]]
        col = cols[0]["couleur"]
        chips = "".join(chip(x) for x in cols)
        panels.append(f"""
  <div class="mp" id="m{i}" style="--c:{col}">
    <div class="mghost cond" aria-hidden="true" data-layout-allow-overlap>0{i}</div>
    <div class="mono mk" id="m{i}-k">Méga-tendance {i:02d} / 04</div>
    <div class="mt cond" id="m{i}-t">{E(m['titre'])}</div>
    <div class="ma serif" id="m{i}-a">{E(m['accroche'])}</div>
    <div class="mn cond" id="m{i}-n" data-final="{E(m['chiffre_txt'])}" data-v="{m['chiffre_v']}" data-u="{E(m['unite'])}">0</div>
    <div class="ml" id="m{i}-l">{E(m['libelle'])}</div>
    <div class="mc" id="m{i}-c"><span class="mono">Qui capte la valeur</span>{chips}</div>
    <div class="ms mono" id="m{i}-s">Sources : {E(m['source_titre'])} · {E(m['source2_titre'])}</div>
  </div>""")
    # constellation
    lefts = [m["titre"] for m in D["megatendances"]]
    ly = [330, 470, 610, 750]
    ordre = ["NVDA", "TSM", "NU", "ADYEY", "RDDT"]
    ry = dict(zip(ordre, [290, 410, 530, 650, 770]))
    liens = []
    for j, m in enumerate(D["megatendances"]):
        for x in V:
            if x["nom"] in m["valeurs"]:
                y1, y2 = ly[j], ry[x["ticker"]]
                liens.append(f'<path class="link" id="m5-p{len(liens)}" d="M640,{y1} C900,{y1} 1060,{y2} 1320,{y2}" stroke="{x["couleur"]}"/>')
    nodes_l = "".join(f'<div class="nl" id="m5-l{j}" style="top:{y - 34}px">{E(t)}</div>' for j, (t, y) in enumerate(zip(lefts, ly)))
    nodes_r = "".join(f'<div class="nr" id="m5-r{k}" style="top:{ry[t] - 34}px;--c:{COUL[t]}"><i></i>{E(next(x["nom"] for x in V if x["ticker"] == t))}</div>'
                      for k, t in enumerate(ordre))
    panels.append(f"""
  <div class="mp" id="m5">
    <div class="mt cond small" id="m5-t">Quatre tendances, cinq moteurs</div>
    <svg class="links" viewBox="0 0 1920 1080" width="1920" height="1080">{''.join(liens)}</svg>
    {nodes_l}{nodes_r}
    <div class="m5-call" id="m5-call"><b class="cond gold">{E(D['part_ia_ptf'])}</b><span>du portefeuille (NVIDIA et TSMC) dépend du même moteur : les investissements dans l'IA. Les trois autres lignes ont des moteurs indépendants.</span></div>
  </div>""")
    return f'<div class="scene" id="s9">{"".join(panels)}</div>'


def scene_retro():
    r1, ry_ = D["retro"]["1an"], D["retro"]["ytd"]
    scale = 10.0  # px par point de %
    zero = 640
    bars = []
    groups = [("12 mois", r1, 200), ("Depuis janvier", ry_, 700)]
    k = 0
    for lab, r, x0 in groups:
        for j, (nom, cle, col) in enumerate((("Portefeuille", "ptf", GOLD), ("Nasdaq 100", "qqq", NDX), ("S&P 500", "spy", SPY))):
            v = r[cle + "_v"]
            h = abs(v) * scale
            top = zero - h if v >= 0 else zero
            lab_top = top - 52 if v >= 0 else zero + h + 10
            x = x0 + j * 135
            bars.append(f'<i class="rb {"neg" if v < 0 else ""}" id="s10-b{k}" style="left:{x}px;top:{top:.1f}px;height:{max(h, 3):.1f}px;background:{col}"></i>'
                        f'<span class="rv mono" id="s10-v{k}" style="left:{x - 20}px;top:{lab_top:.1f}px;color:{col}">{E(r[cle])}</span>'
                        f'<span class="rn mono" style="left:{x - 20}px;top:{zero + 62}px">{E(nom)}</span>')
            k += 1
        bars.append(f'<span class="rg cond" style="left:{x0}px;top:{zero + 104}px">{E(lab)}</span>')
    lst = "".join(f"""
    <div class="srow" id="s10-s{i}" style="--c:{v['couleur']}"><span class="sn">{E(v['nom'])}</span>
      <span class="strack"><i class="sb {'neg' if v['chg_52s_v'] < 0 else ''}" id="s10-sb{i}" style="width:{abs(v['chg_52s_v']) * 3:.1f}px;{'right:50%' if v['chg_52s_v'] < 0 else 'left:50%'}"></i></span>
      <span class="sv2 mono {'neg' if v['chg_52s_v'] < 0 else 'pos'}">{E(v['chg_52s'])}</span></div>"""
                  for i, v in enumerate(sorted(V, key=lambda v: -v["chg_52s_v"])))
    return f"""
<div class="scene" id="s10">
  <h2 class="title cond" id="s10-t">Le rétroviseur : l'indice a gagné</h2>
  <p class="lede wide" id="s10-l">Performances en dollars, poids égaux sans rééquilibrage : les cinq valeurs n'ont pas suivi le Nasdaq 100.</p>
  <i class="zero" id="s10-z"></i>
  {''.join(bars)}
  <div class="slist" id="s10-list"><div class="mono sh">Sur 12 mois, valeur par valeur</div>{lst}</div>
  <div class="msg serif" id="s10-m">Le prix d'aujourd'hui intègre ces chutes. C'est là que naît l'écart de PEG.</div>
  <div class="foot mono" id="s10-f">Sources : Zacks Investment Research, variations au {D['date_analyse']} (QQQ et SPY : performance sur un an et depuis le 1er janvier).</div>
</div>"""


RX0, RX1, RMIN, RMAX = 330, 1730, -15.0, 40.0


def rx(p):
    return RX0 + (p * 100 - RMIN) / (RMAX - RMIN) * (RX1 - RX0)


def scene_scen():
    rows = []
    for i, (nom, a, col) in enumerate((("Portefeuille", P, GOLD), ("Nasdaq 100", N, NDX))):
        y = 410 + i * 130
        rows.append(f"""
    <div class="rlab cond" style="top:{y - 24}px;color:{col}">{E(nom)}</div>
    <i class="rng" id="s12-r{i}" style="left:{rx(a['bear_v']):.1f}px;width:{rx(a['bull_v']) - rx(a['bear_v']):.1f}px;top:{y - 13}px;background:{col}"></i>
    <i class="rdot" id="s12-d{i}" style="left:{rx(a['base_v']) - 15:.1f}px;top:{y - 15}px;border-color:{col}"></i>
    <i class="rdia" id="s12-e{i}" style="left:{rx(a['esperance_v']) - 13:.1f}px;top:{y - 13}px;background:{col}"></i>
    <span class="rtx mono" id="s12-x{i}a" style="left:{rx(a['bear_v']) - 60:.1f}px;top:{y + 26}px">{E(a['bear'])}</span>
    <span class="rtx mono" id="s12-x{i}b" style="left:{rx(a['base_v']) - 60:.1f}px;top:{y + 26}px">{E(a['base'])}</span>
    <span class="rtx mono" id="s12-x{i}c" style="left:{rx(a['bull_v']) - 60:.1f}px;top:{y + 26}px">{E(a['bull'])}</span>
    <span class="resp mono" id="s12-y{i}" style="left:{rx(a['esperance_v']) - 140:.1f}px;top:{y - 64}px;color:{col}">espéré {E(a['esperance'])}/an</span>""")
    ticks = "".join(f'<span class="at mono" style="left:{rx(p / 100) - 40:.1f}px">{"+" if p > 0 else ("−" if p < 0 else "")}{abs(p)}{NB}%</span>'
                    for p in (-10, 0, 10, 20, 30, 40))
    stress = {s["nom"]: s for s in D["stress"]}
    krach = stress["Krach du capex IA (valeurs IA en bear, le reste en base)"]
    return f"""
<div class="scene" id="s12">
  <h2 class="title cond" id="s12-t">Quatre ans, trois scénarios</h2>
  <p class="lede wide" id="s12-l">Rendement annuel jusqu'en 2030 : pessimiste, central, optimiste (25/50/25), dividendes réinvestis, mêmes règles pour l'indice.</p>
  <i class="zline" id="s12-z" style="left:{rx(0):.1f}px"></i>
  <div class="aticks" id="s12-ax">{ticks}</div>
  {''.join(rows)}
  <div class="cent" id="s12-cent">
    <div class="mono">100 € investis deviennent, en espérance</div>
    <div class="cv"><b class="cond gold" id="s12-c1" data-final="{E(P['cent'])}{NB}€" data-v="{P['cent_v']:.4f}">100{NB}€</b><span class="mono">portefeuille</span></div>
    <div class="cv"><b class="cond" id="s12-c2" style="color:{NDX}" data-final="{E(N['cent'])}{NB}€" data-v="{N['cent_v']:.4f}">100{NB}€</b><span class="mono">Nasdaq 100</span></div>
  </div>
  <div class="schips">
    <div class="sc" id="s12-k1"><b class="cond">{E(D['p_sous_indice'])}</b><span>de probabilité de finir sous l'indice central</span></div>
    <div class="sc" id="s12-k2"><b class="cond">{E(D['p_perte'])}</b><span>de probabilité de perdre de l'argent</span></div>
    <div class="sc" id="s12-k3"><b class="cond">{E(krach['ptf'])}</b><span>par an si l'IA s'effondre, contre {E(krach['ndx'])} pour l'indice</span></div>
  </div>
  <div class="foot mono" id="s12-f">Scénarios du modèle, pas des prévisions. Les probabilités supposent des scénarios indépendants : les crises corrélées n'y sont pas.</div>
</div>"""


def scene_risks():
    nu = next(v for v in V if v["ticker"] == "NU")
    items = [
        ("Taïwan", "Une crise autour de l'île frapperait TSMC et NVIDIA en même temps."),
        ("Le dollar", f"{D['part_usd']} du portefeuille est coté en dollars : une baisse de 10 % du dollar coûte environ {D['effet_dollar_10'].replace('−', '')} en euros."),
        ("La volatilité", f"Bêta pondéré de {P['beta']} contre {N['beta']} pour l'indice : des baisses de 30 à 50 % sont possibles sur une ligne."),
        ("Reddit", "Trafic venu de la recherche Google et licences de données d'IA à renégocier en 2027."),
        ("Nu", f"Crédit au Brésil et élections : un choc ramène sa ligne à {nu['bear']}/an dans le scénario pessimiste."),
        ("Adyen", "Commissions sous pression face à Stripe, nouveau directeur financier en 2027."),
    ]
    cards = "".join(f"""
    <div class="rk" id="s13-k{i}"><i class="rkl" id="s13-kl{i}"></i><span class="mono">{i + 1:02d}</span><b>{E(t)}</b><p>{E(x)}</p></div>"""
                    for i, (t, x) in enumerate(items))
    return f"""
<div class="scene" id="s13">
  <h2 class="title cond" id="s13-t">Ce que le modèle ne voit pas</h2>
  <div class="rgrid">{cards}</div>
</div>"""


def scene_final():
    r1 = D["retro"]["1an"]
    return f"""
<div class="scene" id="s15">
  <h2 class="title cond fin" id="s15-t">Cinq valeurs, un critère : la croissance au juste prix</h2>
  <div class="recap">
    <div class="rc" id="s15-c1"><span class="mono">PEG long terme</span><b class="cond gold">{E(P['peg_lt'])}</b><small>contre {E(N['peg_lt'])} pour le Nasdaq 100</small></div>
    <div class="rc" id="s15-c2"><span class="mono">Rendement espéré, par an</span><b class="cond gold">{E(P['esperance'])}</b><small>contre {E(N['esperance'])} pour le Nasdaq 100</small></div>
    <div class="rc" id="s15-c3"><span class="mono">12 derniers mois</span><b class="cond gold">{E(r1['ptf'])}</b><small>contre {E(r1['qqq'])} pour le Nasdaq 100</small></div>
  </div>
  <div class="disc" id="s15-d">
    <p><b>Analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé.</b></p>
    <p>« La Gazette du PEG » est un titre fictif : il ne correspond à aucune publication existante.</p>
    <p class="mono">Sources : consensus et cours Zacks Investment Research ({D['date_analyse']}, cours du {D['date_cours']}) · communiqués des sociétés · presse citée dans le dossier. Calculs : calcul.py, dépôt elgateaux/bourse, screens/2026-10-13_video-portefeuille_hyperframes.</p>
  </div>
</div>"""


# --------------------------------------------------------------------------
# Feuille de style
# --------------------------------------------------------------------------
CSS = r"""
@font-face { font-family: "GZ Archivo"; src: url("fonts/archivo-latin-wdth-normal.woff2") format("woff2");
  font-weight: 100 900; font-stretch: 62% 125%; font-style: normal; }
@font-face { font-family: "GZ Newsreader"; src: url("fonts/newsreader-latin-opsz-normal.woff2") format("woff2");
  font-weight: 200 800; font-style: normal; }
@font-face { font-family: "GZ Newsreader"; src: url("fonts/newsreader-latin-opsz-italic.woff2") format("woff2");
  font-weight: 200 800; font-style: italic; }
@font-face { font-family: "GZ Plex Mono"; src: url("fonts/ibm-plex-mono-latin-400-normal.woff2") format("woff2"); font-weight: 400; }
@font-face { font-family: "GZ Plex Mono"; src: url("fonts/ibm-plex-mono-latin-500-normal.woff2") format("woff2"); font-weight: 500; }
@font-face { font-family: "GZ Plex Mono"; src: url("fonts/ibm-plex-mono-latin-600-normal.woff2") format("woff2"); font-weight: 600; }
:root { --ink:#07090d; --paper:#f2ede2; --muted:#a3abbb; --dim:#8d96a8; --line:rgba(242,237,226,.14);
  --gold:#ffc94a; --ndx:#8da2c8; --spy:#c9ced8; --neg:#ff5a4f; --pos:#5be38f; }
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1920px; height:1080px; overflow:hidden; background:var(--ink); }
body { color:var(--paper); font-family:"GZ Archivo", sans-serif; font-stretch:100%; -webkit-font-smoothing:antialiased; }
#root { position:relative; width:100%; height:100%; overflow:hidden; background:var(--ink); }
.cond { font-family:"GZ Archivo", sans-serif; font-stretch:62%; font-weight:900; text-transform:uppercase; letter-spacing:-.005em; }
.mono { font-family:"GZ Plex Mono", monospace; font-weight:500; letter-spacing:.02em; }
.serif { font-family:"GZ Newsreader", serif; font-style:italic; font-weight:400; }
.gold { color:var(--gold); }
.neg { color:var(--neg); } .pos { color:var(--pos); }
#bg, #grid, #grain, #fade, #hud { position:absolute; inset:0; }
#bg { overflow:hidden; }
.glow { position:absolute; border-radius:50%; filter:blur(120px); opacity:.20; }
.glow.a { width:900px; height:900px; left:-250px; top:-300px; background:#3a5bd9; }
.glow.b { width:800px; height:800px; left:1300px; top:500px; background:#ffb020; opacity:.13; }
#grid { background-image:linear-gradient(rgba(242,237,226,.045) 1px, transparent 1px), linear-gradient(90deg, rgba(242,237,226,.045) 1px, transparent 1px);
  background-size:80px 80px; }
#grain { opacity:.07; pointer-events:none; z-index:60;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' seed='7' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>"); }
.vign { position:absolute; inset:0; background:radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,.55) 100%); }
#hud { z-index:50; pointer-events:none; }
.band { position:absolute; left:0; width:1920px; z-index:45; pointer-events:none; }
.band.t { top:0; height:118px; background:linear-gradient(#07090d 72%, rgba(7,9,13,0)); }
.band.b { bottom:0; height:96px; background:linear-gradient(rgba(7,9,13,0), #07090d 55%); }
.hud-top { position:absolute; left:120px; right:120px; top:44px; height:40px; display:flex; align-items:center; justify-content:space-between;
  font-family:"GZ Plex Mono", monospace; font-size:18px; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); }
.hud-top .mast { color:var(--paper); font-weight:600; }
.hud-top .secs { position:relative; width:560px; height:26px; }
.hud-top .sec { position:absolute; left:0; top:0; width:560px; text-align:center; color:var(--gold); opacity:0; }
.hud-rule { position:absolute; left:120px; right:120px; top:96px; height:1px; background:var(--line); transform-origin:left center; }
.hud-bot { position:absolute; left:120px; right:120px; bottom:30px; display:flex; justify-content:space-between;
  font-family:"GZ Plex Mono", monospace; font-size:15px; color:var(--dim); letter-spacing:.04em; }
#progress { position:absolute; left:0; bottom:0; height:5px; width:1920px; background:var(--gold); transform-origin:left center; }
.scene { position:absolute; left:0; top:0; width:1920px; height:1080px; overflow:hidden; opacity:0; z-index:10; }
#s1 { opacity:1; }
.wipe { position:absolute; left:0; top:0; width:1920px; height:1080px; z-index:40; }
#fade { background:#000; opacity:0; z-index:70; }
.kicker { position:absolute; left:120px; top:150px; font-size:22px; text-transform:uppercase; letter-spacing:.18em; color:var(--muted); }
.title { position:absolute; left:120px; top:136px; width:1680px; font-size:104px; line-height:.92; }
.lede { position:absolute; left:120px; top:262px; width:1300px; font-size:31px; line-height:1.3; color:var(--muted); }
.lede.short { width:900px; } .lede.wide { width:1680px; font-size:29px; }
.foot { position:absolute; left:120px; top:960px; width:1680px; font-size:17px; color:var(--dim); letter-spacing:.02em; }
/* s1 */
.s1-title { position:absolute; left:112px; top:208px; width:1100px; font-size:178px; line-height:.86; }
.s1-title .l { display:block; }
.s1-title em { font-style:normal; color:var(--gold); }
.s1-chips { position:absolute; left:120px; top:760px; display:flex; gap:18px; }
.chip { display:inline-flex; align-items:center; gap:12px; padding:12px 22px 12px 18px; border:2px solid var(--c); border-radius:999px;
  font-family:"GZ Plex Mono", monospace; font-weight:600; font-size:28px; letter-spacing:.06em; color:var(--paper); background:rgba(7,9,13,.6); }
.chip i { display:block; width:14px; height:14px; border-radius:50%; background:var(--c); }
.s1-hook { position:absolute; left:1240px; top:250px; width:560px; }
.s1-hook .lab { font-size:20px; text-transform:uppercase; letter-spacing:.12em; color:var(--muted); }
.s1-hook .big { font-size:210px; line-height:.95; margin-top:8px; font-variant-numeric:tabular-nums; }
.s1-hook .vs { font-size:30px; line-height:1.3; margin-top:14px; }
.s1-hook .sub { font-size:17px; color:var(--dim); margin-top:22px; line-height:1.5; }
.tape { position:absolute; left:0; top:880px; width:1920px; height:60px; border-top:1px solid var(--line); border-bottom:1px solid var(--line); overflow:hidden; }
.tape-in { position:absolute; left:0; top:0; height:60px; display:flex; white-space:nowrap; }
.tk { display:inline-block; padding:0 46px; line-height:58px; font-family:"GZ Plex Mono", monospace; font-size:24px; color:var(--muted); }
.tk b { font-weight:600; } .tk em { font-style:normal; } .tk s { text-decoration:none; color:var(--dim); font-size:18px; }
/* citations */
.quote .ghost { position:absolute; right:-40px; top:120px; font-size:820px; line-height:.8; color:#12161e; white-space:nowrap; }
.bigq { position:absolute; left:130px; top:150px; font-size:420px; line-height:1; color:var(--gold); font-style:normal; }
.qwrap { position:absolute; left:250px; top:290px; width:1420px; display:flex; flex-direction:column; gap:34px; }
.q-en { font-size:74px; line-height:1.1; color:var(--paper); }
.q-en .w { display:inline-block; }
.q-fr { font-size:34px; line-height:1.35; color:var(--muted); }
.q-attr { display:flex; align-items:center; gap:22px; font-size:20px; color:var(--muted); }
.q-attr b { color:var(--paper); font-weight:600; }
.q-attr .rule { display:block; width:90px; height:3px; background:var(--gold); transform-origin:left center; }
.q-ctx { font-size:17px; color:var(--dim); }
/* s3 */
.eq { position:absolute; left:120px; top:390px; width:1680px; display:flex; align-items:center; justify-content:center; gap:34px; }
.tile { width:420px; height:240px; border:2px solid var(--line); border-radius:22px; padding:28px 32px; background:rgba(255,255,255,.025); }
.tile .mono { font-size:19px; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); }
.tile .tv { font-size:150px; line-height:1; margin-top:10px; font-variant-numeric:tabular-nums; }
.tile.gold-b { border-color:var(--gold); }
.op { font-size:120px; color:var(--dim); }
.gauge { position:absolute; left:240px; top:730px; width:1440px; height:46px; display:flex; }
.gz { position:relative; height:46px; display:flex; align-items:center; padding-left:16px; font-family:"GZ Plex Mono", monospace; font-size:17px; text-transform:uppercase; letter-spacing:.1em; }
.gz.z1 { width:33.3333%; background:rgba(255,201,74,.22); color:var(--gold); border-radius:23px 0 0 23px; }
.gz.z2 { width:16.6667%; background:rgba(242,237,226,.08); color:var(--muted); }
.gz.z3 { width:50%; background:rgba(255,90,79,.14); color:#ff8a80; border-radius:0 23px 23px 0; }
.gticks { position:absolute; left:0; top:58px; width:1440px; height:30px; }
.gt { position:absolute; top:0; width:80px; margin-left:-40px; text-align:center; font-family:"GZ Plex Mono", monospace; font-size:18px; color:var(--dim); }
.gmark { position:absolute; left:0; top:-74px; width:200px; margin-left:-100px; height:130px; display:flex; flex-direction:column; align-items:center; }
.gmark span { font-size:18px; color:var(--gold); white-space:nowrap; }
.gmark i { order:2; display:block; width:4px; height:96px; background:var(--gold); margin-top:6px; }
.defs { position:absolute; left:240px; top:860px; width:1440px; font-size:19px; line-height:1.6; color:var(--muted); }
.defs b { color:var(--paper); font-weight:600; }
/* s4 */
.roster { position:absolute; left:120px; top:290px; width:1680px; }
.rrow { position:relative; height:116px; border-bottom:1px solid var(--line); display:flex; align-items:center; }
.rbar { position:absolute; left:0; top:22px; width:10px; height:72px; background:var(--c); border-radius:5px; }
.rsym { width:420px; padding-left:40px; font-size:104px; line-height:1; color:var(--c); }
.rname { flex:1; font-size:44px; font-weight:700; }
.rname small { display:block; font-size:26px; font-weight:400; color:var(--muted); margin-top:4px; }
.rw { font-size:44px; color:var(--paper); }
/* cartes */
.card .halo { position:absolute; left:-200px; top:-160px; width:1100px; height:900px; border-radius:50%; background:var(--c); opacity:.10; filter:blur(140px); }
.csym { position:absolute; left:112px; top:128px; width:820px; font-size:250px; line-height:.88; color:var(--c); white-space:nowrap; overflow:hidden; }
.csym .ch { display:inline-block; }
.cname { position:absolute; left:120px; top:372px; width:820px; font-size:58px; font-weight:800; line-height:1.05; }
.cname small { display:block; font-size:34px; font-weight:400; color:var(--muted); margin-top:8px; }
.cmeta { position:absolute; left:120px; top:500px; width:820px; font-size:20px; color:var(--muted); line-height:1.5; }
.ctags { position:absolute; left:120px; top:560px; display:flex; gap:12px; }
.tag { font-family:"GZ Plex Mono", monospace; font-size:19px; text-transform:uppercase; letter-spacing:.08em; padding:8px 16px; border:1px solid var(--c); border-radius:999px; color:var(--paper); }
.cquote { position:absolute; left:120px; top:640px; width:790px; border-left:4px solid var(--c); padding-left:26px; }
.cq-en { font-size:33px; line-height:1.22; color:var(--paper); }
.cq-fr { font-size:22px; line-height:1.4; color:var(--muted); margin-top:12px; }
.cq-a { font-size:16px; color:var(--dim); margin-top:12px; line-height:1.45; }
.panel { position:absolute; left:980px; top:140px; width:820px; height:790px; border:1px solid var(--line); border-radius:22px; background:rgba(255,255,255,.03); }
.ph { position:absolute; left:40px; top:30px; font-size:17px; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); }
.bar { position:absolute; bottom:360px; width:150px; border-radius:10px 10px 0 0; transform-origin:bottom center; }
.bar.b1 { left:70px; background:rgba(242,237,226,.22); }
.bar.b2 { left:270px; background:var(--c); }
.bv { position:absolute; width:230px; text-align:center; font-size:34px; font-weight:600; font-variant-numeric:tabular-nums; }
.by { position:absolute; top:442px; width:150px; text-align:center; font-size:20px; color:var(--muted); }
.growth { position:absolute; left:470px; top:150px; width:320px; }
.growth .gv { font-size:132px; line-height:.9; color:var(--c); }
.growth .mono { font-size:17px; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; margin-top:10px; }
.tiles { position:absolute; left:40px; top:500px; width:740px; display:flex; gap:16px; }
.st { flex:1; height:128px; border:1px solid var(--line); border-radius:16px; padding:16px 18px; }
.st .mono { font-size:14px; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); }
.st .cond { font-size:66px; line-height:1; margin-top:10px; }
.st small { font-size:26px; color:var(--muted); }
.mini { position:absolute; left:40px; top:668px; width:740px; height:14px; border-radius:7px; background:rgba(242,237,226,.08); }
.mini .mz { position:absolute; left:0; top:0; width:50%; height:14px; border-radius:7px 0 0 7px; background:rgba(255,201,74,.30); }
.mini .mono { position:absolute; top:22px; font-size:15px; color:var(--dim); }
.mini .m0 { left:0; } .mini .m1 { left:50%; margin-left:-24px; } .mini .m2 { right:0; }
.mm { position:absolute; left:0; top:-14px; width:0; height:42px; }
.mm i { position:absolute; left:-4px; top:0; width:8px; height:42px; border-radius:4px; background:var(--c); box-shadow:0 0 18px var(--c); }
.pfoot { position:absolute; left:40px; top:716px; width:740px; font-size:16px; line-height:1.55; color:var(--muted); }
/* s5 */
.growth-list { position:absolute; left:120px; top:380px; width:1680px; }
.grow { display:flex; align-items:center; height:62px; }
.grow.agg:first-of-type { }
.grow .gl { width:420px; font-size:30px; font-weight:600; }
.grow.agg .gl { color:var(--c); }
.gtrack { position:relative; width:1060px; height:34px; }
.gb { position:absolute; left:0; top:0; height:34px; border-radius:0 8px 8px 0; background:var(--c); transform-origin:left center; display:block; }
.grow.agg .gb { opacity:.9; }
.gvv { width:180px; padding-left:22px; font-size:30px; font-weight:600; font-variant-numeric:tabular-nums; }
#s5-r5 { margin-top:26px; border-top:1px solid var(--line); padding-top:0; }
.callout { position:absolute; left:120px; top:900px; width:1680px; font-size:20px; color:var(--paper); }
#s5 .foot { top:944px; }
/* s6 */
.dhead { position:absolute; left:120px; top:150px; width:1680px; height:130px; }
.dh { position:absolute; top:0; width:700px; display:flex; flex-direction:column; gap:8px; }
.dh .cond { font-size:96px; line-height:.9; }
.dh .mono { font-size:18px; color:var(--muted); }
.dh.l { left:0; } .dh.r { right:0; text-align:right; align-items:flex-end; }
.dvs { position:absolute; left:790px; top:14px; width:100px; text-align:center; font-size:70px; color:var(--dim); }
.dsplit { position:absolute; left:959px; top:300px; width:2px; height:600px; background:var(--line); transform-origin:top center; display:block; }
.drows { position:absolute; left:120px; top:310px; width:1680px; }
.drow { position:relative; height:116px; }
.dl, .dr { position:absolute; top:6px; width:560px; font-size:100px; line-height:1; color:var(--muted); font-variant-numeric:tabular-nums; }
.dl { left:0; text-align:right; } .dr { right:0; text-align:left; }
.dl.win { color:var(--gold); } .dr.win { color:var(--ndx); }
.dc { position:absolute; left:640px; top:40px; width:400px; text-align:center; font-size:17px; text-transform:uppercase; letter-spacing:.06em; color:var(--paper);
  background:var(--ink); padding:6px 0; }
/* s7 */
.scatter { position:absolute; left:110px; top:262px; }
.scatter .gridl { stroke:rgba(242,237,226,.07); stroke-width:1; }
.scatter .ax { font-family:"GZ Plex Mono", monospace; font-size:19px; fill:#8f98aa; }
.scatter .axt { font-family:"GZ Plex Mono", monospace; font-size:18px; fill:#9aa3b4; text-transform:uppercase; letter-spacing:.08em; }
.pegl { stroke:#ffc94a; stroke-width:3; fill:none; }
.pegl.dash { stroke:#9aa3b4; stroke-dasharray:10 10; stroke-width:2; }
.pegt { font-family:"GZ Plex Mono", monospace; font-size:19px; fill:#ffc94a; }
#s7-tl15 { fill:#9aa3b4; }
.plab { font-family:"GZ Plex Mono", monospace; font-size:21px; font-weight:600; }
.side { position:absolute; left:1380px; top:290px; width:420px; display:flex; flex-direction:column; gap:26px; }
.side > .mono { font-size:19px; line-height:1.5; color:var(--muted); }
.side .note { font-size:16px; color:var(--dim); }
.sv { border-top:1px solid var(--line); padding-top:14px; display:flex; flex-direction:column; gap:4px; }
.sv .mono { font-size:16px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); }
.sv b { font-size:92px; line-height:1; }
/* s9 */
.mp { position:absolute; left:0; top:0; width:1920px; height:1080px; opacity:0; }
#m1 { opacity:1; }
.mghost { position:absolute; right:60px; top:150px; font-size:700px; line-height:.8; color:#12161e; }
.mk { position:absolute; left:120px; top:150px; font-size:20px; text-transform:uppercase; letter-spacing:.16em; color:var(--c); }
.mt { position:absolute; left:120px; top:186px; width:1680px; font-size:128px; line-height:.92; }
.mt.small { top:136px; font-size:96px; }
.ma { position:absolute; left:120px; top:318px; width:1400px; font-size:44px; color:var(--muted); }
.mn { position:absolute; left:112px; top:400px; width:1300px; font-size:290px; line-height:1; color:var(--c); font-variant-numeric:tabular-nums; text-transform:none; }
.ml { position:absolute; left:120px; top:700px; width:1300px; font-size:36px; line-height:1.3; }
.mc { position:absolute; left:120px; top:812px; display:flex; align-items:center; gap:16px; }
.mc > .mono { font-size:17px; text-transform:uppercase; letter-spacing:.12em; color:var(--muted); margin-right:8px; }
.ms { position:absolute; left:120px; top:906px; width:1680px; font-size:15px; color:var(--dim); }
.links path { fill:none; stroke-width:4; stroke-linecap:round; opacity:.9; }
.nl { position:absolute; left:160px; width:480px; height:68px; display:flex; align-items:center; padding:0 26px; border:1px solid var(--line); border-radius:14px;
  background:rgba(7,9,13,.85); font-size:30px; font-weight:700; }
.nr { position:absolute; left:1320px; width:440px; height:68px; display:flex; align-items:center; gap:16px; padding:0 24px; border:2px solid var(--c); border-radius:999px;
  background:rgba(7,9,13,.85); font-size:32px; font-weight:700; }
.nr i { display:block; width:16px; height:16px; border-radius:50%; background:var(--c); }
.m5-call { position:absolute; left:160px; top:880px; width:1600px; display:flex; align-items:center; gap:28px; }
.m5-call b { font-size:96px; line-height:1; }
.m5-call span { font-size:28px; line-height:1.35; }
/* s10 */
.zero { position:absolute; left:160px; top:640px; width:980px; height:2px; background:rgba(242,237,226,.35); transform-origin:left center; display:block; }
.rb { position:absolute; width:110px; border-radius:6px 6px 0 0; transform-origin:bottom center; display:block; }
.rb.neg { border-radius:0 0 6px 6px; transform-origin:top center; }
.rv { position:absolute; width:150px; text-align:center; font-size:30px; font-weight:600; }
.rn { position:absolute; width:150px; text-align:center; font-size:16px; color:var(--muted); }
.rg { position:absolute; width:400px; font-size:44px; color:var(--paper); }
.slist { position:absolute; left:1220px; top:390px; width:580px; }
.slist .sh { font-size:17px; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); margin-bottom:18px; }
.srow { display:flex; align-items:center; height:70px; border-bottom:1px solid var(--line); }
.sn { width:150px; font-size:28px; font-weight:700; color:var(--c); }
.strack { position:relative; width:300px; height:22px; }
.strack::before { content:""; position:absolute; left:50%; top:-8px; width:1px; height:38px; background:rgba(242,237,226,.3); }
.sb { position:absolute; top:0; height:22px; background:var(--c); display:block; }
.sb.neg { transform-origin:right center; } .sb { transform-origin:left center; }
.sv2 { width:130px; text-align:right; font-size:26px; font-weight:600; }
.msg { position:absolute; left:120px; top:880px; width:1680px; font-size:38px; color:var(--paper); }
#s10 .foot { top:950px; }
/* s12 */
.zline { position:absolute; top:340px; width:2px; height:250px; background:rgba(242,237,226,.25); display:block; }
.aticks { position:absolute; left:0; top:596px; width:1920px; height:30px; }
.at { position:absolute; width:80px; text-align:center; font-size:17px; color:var(--dim); }
.rlab { position:absolute; left:120px; width:200px; font-size:42px; line-height:1; }
.rng { position:absolute; height:26px; border-radius:13px; opacity:.85; transform-origin:left center; display:block; }
.rdot { position:absolute; width:30px; height:30px; border-radius:50%; border:5px solid; background:var(--ink); display:block; }
.rdia { position:absolute; width:26px; height:26px; transform:rotate(45deg); box-shadow:0 0 0 4px var(--ink); display:block; }
.rtx { position:absolute; width:120px; text-align:center; font-size:20px; color:var(--muted); }
.resp { position:absolute; width:280px; text-align:center; font-size:21px; font-weight:600; }
.cent { position:absolute; left:120px; top:660px; width:1080px; display:flex; flex-wrap:wrap; column-gap:70px; }
.cent > .mono { width:100%; font-size:20px; text-transform:uppercase; letter-spacing:.12em; color:var(--muted); margin-bottom:6px; }
.cv { display:flex; flex-direction:column; }
.cv b { font-size:200px; line-height:.95; font-variant-numeric:tabular-nums; }
.cv .mono { font-size:18px; color:var(--muted); text-transform:uppercase; letter-spacing:.1em; }
.schips { position:absolute; left:1240px; top:660px; width:560px; display:flex; flex-direction:column; gap:14px; }
.sc { display:flex; align-items:center; gap:22px; border:1px solid var(--line); border-radius:16px; padding:10px 22px; }
.sc b { font-size:52px; line-height:1; color:var(--gold); min-width:150px; }
.sc span { font-size:21px; line-height:1.3; color:var(--paper); }
#s12 .foot { top:960px; }
/* s13 */
.rgrid { position:absolute; left:120px; top:300px; width:1680px; display:grid; grid-template-columns:repeat(3, 1fr); gap:30px; }
.rk { position:relative; height:290px; border:1px solid var(--line); border-radius:20px; padding:34px 32px; background:rgba(255,255,255,.025); overflow:hidden; }
.rkl { position:absolute; left:0; top:0; width:100%; height:5px; background:var(--neg); transform-origin:left center; display:block; }
.rk .mono { font-size:18px; color:var(--neg); }
.rk b { display:block; font-size:42px; margin-top:10px; }
.rk p { font-size:24px; line-height:1.35; color:var(--muted); margin-top:14px; }
/* s15 */
.title.fin { font-size:112px; width:1500px; }
.recap { position:absolute; left:120px; top:420px; width:1680px; display:flex; gap:28px; }
.rc { flex:1; border:1px solid var(--line); border-radius:20px; padding:26px 30px; }
.rc .mono { font-size:17px; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); }
.rc b { display:block; font-size:96px; line-height:1; margin-top:12px; }
.rc small { display:block; font-size:26px; color:var(--ndx); margin-top:10px; }
.disc { position:absolute; left:120px; top:690px; width:1680px; display:flex; flex-direction:column; gap:14px; font-size:27px; line-height:1.35; }
.disc .mono { font-size:17px; color:var(--dim); }
"""


# --------------------------------------------------------------------------
# Timeline GSAP
# --------------------------------------------------------------------------
JS = r"""
const D = __DATA__;
const SC = __SCENES__;
const TOTAL = __TOTAL__;
const MEGA_T = __MEGA__;
const SECTIONS = __SECTIONS__;
const tl = gsap.timeline({ paused: true });
const $ = (s) => document.querySelector(s);
const $$ = (s) => Array.from(document.querySelectorAll(s));
const NB = " ";
const start = Object.fromEntries(SC.map((s) => [s[0], s[1]]));

function fr(v, d, signe) {
  let s = Math.abs(v).toFixed(d);
  let [i, f] = s.split(".");
  i = i.replace(/\B(?=(\d{3})+(?!\d))/g, NB);
  s = f ? i + "," + f : i;
  if (v < 0 && Number(Math.abs(v).toFixed(d)) !== 0) return "−" + s;
  return signe ? "+" + s : s;
}
// Compteur : le texte final est celui écrit par Python (data-final), à l'identique.
function count(sel, from, to, dec, t, dur, opt) {
  opt = opt || {};
  const el = $(sel);
  const fin = el.getAttribute("data-final");
  const o = { v: from };
  tl.to(o, { v: to, duration: dur, ease: opt.ease || "power3.out",
    onUpdate: function () {
      el.textContent = this.progress() >= 1 ? fin : (opt.pre || "") + fr(o.v, dec, opt.signe) + (opt.suf || "");
    } }, t);
}
const IN = (sel, from, t, dur, ease, extra) =>
  tl.fromTo(sel, Object.assign({ opacity: 0 }, from), Object.assign({ opacity: 1, x: 0, y: 0, duration: dur, ease: ease }, extra || {}), t);

// ---------------- fond, bandeau, progression ----------------
tl.fromTo("#bg", { opacity: 0 }, { opacity: 1, duration: 1.2, ease: "sine.out" }, 0);
tl.fromTo("#grid", { backgroundPosition: "0px 0px" }, { backgroundPosition: "-160px -320px", duration: TOTAL, ease: "none" }, 0);
tl.to(".glow.a", { x: 520, y: 260, duration: TOTAL / 2, ease: "sine.inOut", yoyo: true, repeat: 1 }, 0);
tl.to(".glow.b", { x: -640, y: -380, duration: TOTAL / 2, ease: "sine.inOut", yoyo: true, repeat: 1 }, 0);
tl.fromTo("#progress", { scaleX: 0 }, { scaleX: 1, duration: TOTAL, ease: "none" }, 0);
tl.fromTo(".hud-top", { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, 0.25);
tl.fromTo(".hud-rule", { scaleX: 0 }, { scaleX: 1, duration: 1.1, ease: "expo.inOut" }, 0.3);
tl.fromTo(".hud-bot", { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.out" }, 0.9);
SECTIONS.forEach((s, i) => {
  const el = "#sec" + i;
  tl.fromTo(el, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.45, ease: "power2.out" }, s[0] + (i ? 0.35 : 0.5));
  if (i + 1 < SECTIONS.length) tl.to(el, { opacity: 0, y: -12, duration: 0.3, ease: "power2.in" }, SECTIONS[i + 1][0]);
});
tl.set("#fade", { opacity: 0 }, 0);
tl.to("#fade", { opacity: 1, duration: 1.0, ease: "power1.in" }, TOTAL - 1.0);

// ---------------- transitions ----------------
const WIPES = ["#w0", "#w1", "#w2", "#w3", "#w4"];
tl.set(WIPES, { x: -1920 }, 0);
function trans(type, oldS, newS, T) {
  const o = "#" + oldS, n = "#" + newS;
  if (type === "push") {
    tl.to(o, { x: -1920, duration: 0.75, ease: "power3.inOut" }, T);
    tl.fromTo(n, { x: 1920, opacity: 1 }, { x: 0, opacity: 1, duration: 0.75, ease: "power3.inOut" }, T);
    tl.set(o, { opacity: 0 }, T + 0.76);
  } else if (type === "vpush") {
    tl.to(o, { y: -1080, duration: 0.75, ease: "power3.inOut" }, T);
    tl.fromTo(n, { y: 1080, opacity: 1 }, { y: 0, opacity: 1, duration: 0.75, ease: "power3.inOut" }, T);
    tl.set(o, { opacity: 0 }, T + 0.76);
  } else if (type === "blocks") {
    WIPES.forEach((w, i) => {
      tl.set(w, { x: -1920 }, T - 0.01);
      tl.to(w, { x: 0, duration: 0.32, ease: "power3.inOut" }, T + i * 0.045);
      tl.to(w, { x: 1920, duration: 0.32, ease: "power3.inOut" }, T + 0.42 + i * 0.045);
    });
    tl.set(o, { opacity: 0 }, T + 0.38);
    tl.set(n, { opacity: 1 }, T + 0.38);
  } else if (type === "blur") {
    tl.to(o, { filter: "blur(16px)", scale: 1.05, opacity: 0, duration: 0.7, ease: "power2.inOut" }, T);
    tl.fromTo(n, { filter: "blur(16px)", scale: 0.96, opacity: 0 },
      { filter: "blur(0px)", scale: 1, opacity: 1, duration: 0.85, ease: "power2.out" }, T + 0.2);
  }
}
for (let i = 1; i < SC.length; i++) trans(SC[i][2], SC[i - 1][0], SC[i][0], SC[i][1]);

// ---------------- scènes ----------------
function quote(id, t) {
  tl.fromTo("#" + id + "-q", { opacity: 0, scale: 0.6, rotation: -8 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.7, ease: "back.out(1.8)" }, t + 0.25);
  tl.fromTo("#" + id + " .q-en .w", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out", stagger: 0.07 }, t + 0.5);
  const n = $$("#" + id + " .q-en .w").length;
  const t2 = t + 0.6 + n * 0.07;
  IN("#" + id + "-fr", { y: 18 }, t2 + 0.25, 0.7, "power2.out");
  tl.fromTo("#" + id + "-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "expo.out" }, t2 + 0.6);
  IN("#" + id + "-attr", { x: -30 }, t2 + 0.65, 0.6, "power3.out");
  IN("#" + id + "-ctx", {}, t2 + 1.0, 0.6, "sine.out");
  tl.fromTo("#" + id + " .ghost", { x: 60 }, { x: -60, duration: 6.5, ease: "none" }, t);
}

// S1 — intro
(function () {
  IN("#s1-kick", { x: -40 }, 0.6, 0.6, "power3.out");
  tl.fromTo("#s1l1", { opacity: 0, scale: 1.35, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.55, ease: "expo.out", transformOrigin: "left center" }, 0.9);
  IN("#s1l2", { x: -160 }, 1.45, 0.45, "power4.out");
  tl.fromTo("#s1l3", { opacity: 0, y: 90, rotation: -3 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "back.out(1.6)", transformOrigin: "left bottom" }, 2.0);
  tl.fromTo(".s1-chips .chip", { opacity: 0, y: 40, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "back.out(2.2)", stagger: 0.09 }, 2.9);
  IN("#s1-hook .lab", { y: 14 }, 3.6, 0.5, "power2.out");
  tl.fromTo("#s1-hook .big", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "none" }, 3.8);
  count("#s1-num", 0, D.portefeuille.esperance_v * 100, 1, 3.8, 1.6, { suf: NB + "%", signe: true, ease: "power2.out" });
  tl.fromTo("#s1-num", { scale: 0.55 }, { scale: 1, duration: 1.6, ease: "power2.out", transformOrigin: "left bottom" }, 3.8);
  IN("#s1-hook .vs", { y: 16 }, 5.2, 0.6, "power3.out");
  IN("#s1-hook .sub", {}, 5.8, 0.8, "sine.out");
  tl.fromTo("#s1-tape", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.out" }, 3.2);
  const w = $("#s1-tape-in").scrollWidth / 3;
  tl.fromTo("#s1-tape-in", { x: 0 }, { x: -w, duration: 9, ease: "none" }, 0);
})();

// S2, S8, S11, S14 — citations
quote("s2", start.s2); quote("s8", start.s8); quote("s11", start.s11); quote("s14", start.s14);

// S3 — le PEG
(function () {
  const t = start.s3;
  IN("#s3-t", { y: 40 }, t + 0.5, 0.6, "expo.out");
  IN("#s3-l", { y: 20 }, t + 0.9, 0.6, "power2.out");
  tl.fromTo(["#s3-a", "#s3-b", "#s3-c"], { opacity: 0, y: 60, rotationX: -40 }, { opacity: 1, y: 0, rotationX: 0, duration: 0.7, ease: "power3.out", stagger: 0.18, transformPerspective: 900 }, t + 1.4);
  tl.fromTo(["#s3-o1", "#s3-o2"], { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.5)", stagger: 0.18 }, t + 1.7);
  tl.fromTo("#s3-gauge", { opacity: 0, scaleX: 0.6 }, { opacity: 1, scaleX: 1, duration: 0.8, ease: "expo.out", transformOrigin: "left center" }, t + 2.6);
  tl.fromTo("#s3-mark", { opacity: 0, x: 0 }, { opacity: 1, x: 1440 / 3, duration: 1.2, ease: "power3.out" }, t + 3.1);
  // la croissance double : 20 % -> 40 %, le PEG tombe de 1,0 à 0,5
  const g = { v: 20 };
  tl.to(g, { v: 40, duration: 1.4, ease: "power2.inOut", onUpdate: function () {
    $("#s3-g").textContent = fr(g.v, 0);
    $("#s3-peg").textContent = fr(20 / g.v, 1);
  } }, t + 5.3);
  tl.to("#s3-b", { borderColor: "#ffc94a", duration: 0.4, ease: "sine.out" }, t + 5.3);
  tl.to("#s3-mark", { x: 1440 * 0.5 / 3, duration: 1.4, ease: "power2.inOut" }, t + 5.3);
  tl.fromTo("#s3-c", { boxShadow: "0 0 0px rgba(255,201,74,0)" }, { boxShadow: "0 0 60px rgba(255,201,74,.45)", duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 1 }, t + 6.6);
  IN("#s3-defs", { y: 16 }, t + 7.4, 0.7, "power2.out");
})();

// S4 — les cinq
(function () {
  const t = start.s4;
  IN("#s4-t", { x: -60 }, t + 0.5, 0.6, "expo.out");
  tl.fromTo(".rrow", { opacity: 0, x: 260 }, { opacity: 1, x: 0, duration: 0.6, ease: "power4.out", stagger: 0.12 }, t + 0.8);
  tl.fromTo(".rbar", { scaleY: 0 }, { scaleY: 1, duration: 0.5, ease: "back.out(2)", stagger: 0.12, transformOrigin: "center bottom" }, t + 1.1);
  IN("#s4-f", {}, t + 2.2, 0.6, "sine.out");
})();

// Cartes valeur par valeur
D.valeurs.forEach((v, k) => {
  const id = "c" + (k + 1), t = start[id];
  tl.fromTo("#" + id + " .ch", { opacity: 0, y: 140 }, { opacity: 1, y: 0, duration: 0.7, ease: "expo.out", stagger: 0.06 }, t + 0.45);
  IN("#" + id + "-name", { x: -40 }, t + 0.8, 0.55, "power3.out");
  IN("#" + id + "-meta", {}, t + 1.1, 0.5, "sine.out");
  tl.fromTo("#" + id + " .tag", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)", stagger: 0.08 }, t + 1.3);
  tl.fromTo("#" + id + "-panel", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, t + 0.7);
  tl.fromTo("#" + id + "-b1", { scaleY: 0 }, { scaleY: 1, duration: 0.8, ease: "power3.out" }, t + 1.2);
  tl.fromTo("#" + id + "-b2", { scaleY: 0 }, { scaleY: 1, duration: 1.0, ease: "power4.out" }, t + 1.5);
  IN("#" + id + "-v1", {}, t + 1.2, 0.3, "none");
  IN("#" + id + "-v2", {}, t + 1.5, 0.3, "none");
  count("#" + id + "-v1", 0, v.bpa26_v, 2, t + 1.2, 0.8, { suf: NB + "$" });
  count("#" + id + "-v2", 0, v.bpa27_v, 2, t + 1.5, 1.0, { suf: NB + "$" });
  tl.fromTo("#" + id + "-g", { opacity: 0, scale: 0.4, rotation: -6 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.6, ease: "back.out(2.4)", transformOrigin: "left center" }, t + 2.4);
  tl.fromTo("#" + id + " .st", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out", stagger: 0.12 }, t + 2.8);
  IN("#" + id + "-mini", {}, t + 3.3, 0.4, "sine.out");
  tl.fromTo("#" + id + "-mm", { x: 0 }, { x: Math.min(v.peg_lt_v, 2) / 2 * 740, duration: 1.0, ease: "power3.out" }, t + 3.4);
  IN("#" + id + "-pf", {}, t + 4.0, 0.6, "sine.out");
  tl.fromTo("#" + id + "-q", { opacity: 0, clipPath: "inset(0 100% 0 0)" }, { opacity: 1, clipPath: "inset(0 0% 0 0)", duration: 1.0, ease: "power2.inOut" }, t + 3.0);
  tl.fromTo("#" + id + "-halo", { scale: 0.8, opacity: 0.04 }, { scale: 1.1, opacity: 0.14, duration: 7.5, ease: "sine.inOut" }, t);
});

// S5 — croissance des bénéfices
(function () {
  const t = start.s5;
  IN("#s5-t", { y: 40 }, t + 0.5, 0.6, "expo.out");
  IN("#s5-l", { y: 16 }, t + 0.8, 0.6, "power2.out");
  $$(".grow").forEach((r, i) => {
    const ti = t + 1.3 + i * 0.22 + (i >= 5 ? 0.5 : 0);
    IN("#s5-r" + i, { x: -30 }, ti, 0.4, "power3.out");
    tl.fromTo("#s5-b" + i, { scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: i >= 5 ? "power4.out" : "power3.out" }, ti + 0.1);
    const el = $("#s5-v" + i);
    count("#s5-v" + i, 0, parseFloat(el.getAttribute("data-v")), 0, ti + 0.1, 0.9, { suf: NB + "%", signe: true });
  });
  tl.fromTo("#s5-call", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, t + 5.3);
  IN("#s5-f", {}, t + 5.9, 0.6, "sine.out");
})();

// S6 — duel
(function () {
  const t = start.s6;
  IN("#s6-hl", { x: -80 }, t + 0.5, 0.6, "expo.out");
  IN("#s6-hr", { x: 80 }, t + 0.6, 0.6, "expo.out");
  tl.fromTo("#s6-vs", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power4.out" }, t + 0.9);
  tl.fromTo("#s6-split", { scaleY: 0 }, { scaleY: 1, duration: 1.0, ease: "expo.inOut" }, t + 1.0);
  $$(".drow").forEach((r, i) => {
    const ti = t + 1.6 + i * 1.5;
    IN("#s6-r" + i + " .dc", {}, ti, 0.4, "sine.out");
    IN("#s6-l" + i, { x: -60 }, ti + 0.15, 0.55, "power4.out");
    IN("#s6-x" + i, { x: 60 }, ti + 0.25, 0.55, "power4.out");
    tl.fromTo("#s6-r" + i + " .win", { textShadow: "0 0 0px rgba(255,201,74,0)" }, { textShadow: "0 0 34px rgba(255,201,74,.55)", duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 1 }, ti + 0.8);
  });
  IN("#s6-f", { y: 14 }, t + 9.4, 0.7, "power2.out");
})();

// S7 — nuage de Lynch
(function () {
  const t = start.s7;
  IN("#s7-t", { y: 40 }, t + 0.5, 0.6, "expo.out");
  tl.fromTo("#s7-svg .gridl", { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.out", stagger: 0.03 }, t + 0.9);
  tl.fromTo("#s7-svg .ax, #s7-svg .axt", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.out" }, t + 1.0);
  ["#s7-l1", "#s7-l15"].forEach((s, i) => {
    const len = $(s).getTotalLength();
    tl.fromTo(s, { strokeDasharray: i ? "10 10" : len + " " + len, strokeDashoffset: i ? 0 : len, opacity: i ? 0 : 1 },
      { strokeDashoffset: 0, opacity: 1, duration: 1.2, ease: "power2.inOut" }, t + 1.4 + i * 0.4);
  });
  IN("#s7-zone", {}, t + 2.2, 0.8, "sine.out");
  IN("#s7-tl1", {}, t + 2.4, 0.5, "sine.out");
  IN("#s7-tl15", {}, t + 2.6, 0.5, "sine.out");
  for (let i = 0; i < 8; i++) {
    const ti = t + (i < 5 ? 3.0 + i * 0.25 : 4.8 + (i - 5) * 0.7);
    tl.fromTo("#s7-p" + i, { opacity: 0, scale: 0, svgOrigin: "0 0" },
      { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(3)", svgOrigin: "0 0" }, ti);
    IN("#s7-t" + i, {}, ti + 0.2, 0.4, "sine.out");
  }
  tl.fromTo("#s7-p5", { filter: "drop-shadow(0 0 0px #ffc94a)" }, { filter: "drop-shadow(0 0 18px #ffc94a)", duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut" }, t + 5.4);
  IN("#s7-l", { x: 30 }, t + 1.0, 0.6, "power2.out");
  tl.fromTo(["#s7-s1", "#s7-s2", "#s7-s3"], { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out", stagger: 0.35 }, t + 6.4);
  IN("#s7-side .note", {}, t + 8.0, 0.6, "sine.out");
})();

// S9 — méga-tendances
(function () {
  const t0 = start.s9;
  for (let i = 1; i <= 4; i++) {
    const t = t0 + MEGA_T[i - 1];
    if (i > 1) {
      tl.to("#m" + (i - 1), { y: -1080, duration: 0.7, ease: "power3.inOut" }, t);
      tl.fromTo("#m" + i, { y: 1080, opacity: 1 }, { y: 0, opacity: 1, duration: 0.7, ease: "power3.inOut" }, t);
      tl.set("#m" + (i - 1), { opacity: 0 }, t + 0.71);
    }
    IN("#m" + i + "-k", { x: -30 }, t + 0.45, 0.5, "power3.out");
    tl.fromTo("#m" + i + "-t", { opacity: 0, y: 70, skewY: 4 }, { opacity: 1, y: 0, skewY: 0, duration: 0.65, ease: "expo.out" }, t + 0.55);
    IN("#m" + i + "-a", { y: 20 }, t + 0.9, 0.6, "power2.out");
    const el = $("#m" + i + "-n");
    const val = parseFloat(el.getAttribute("data-v"));
    const dec = Math.round(val) === val ? 0 : 1;
    IN("#m" + i + "-n", {}, t + 1.2, 0.3, "none");
    count("#m" + i + "-n", 0, val, dec, t + 1.2, 1.5, { suf: NB + el.getAttribute("data-u"), ease: "power2.out" });
    tl.fromTo("#m" + i + "-n", { scale: 0.7 }, { scale: 1, duration: 1.5, ease: "power2.out", transformOrigin: "left center" }, t + 1.2);
    IN("#m" + i + "-l", { y: 16 }, t + 2.4, 0.6, "power2.out");
    tl.fromTo("#m" + i + "-c .chip", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.5)", stagger: 0.12 }, t + 2.9);
    IN("#m" + i + "-c > .mono", {}, t + 2.8, 0.4, "sine.out");
    IN("#m" + i + "-s", {}, t + 3.2, 0.6, "sine.out");
    tl.fromTo("#m" + i + " .mghost", { y: 60 }, { y: -40, duration: 5.5, ease: "none" }, t);
  }
  const t = t0 + MEGA_T[4];
  tl.to("#m4", { y: -1080, duration: 0.7, ease: "power3.inOut" }, t);
  tl.fromTo("#m5", { y: 1080, opacity: 1 }, { y: 0, opacity: 1, duration: 0.7, ease: "power3.inOut" }, t);
  tl.set("#m4", { opacity: 0 }, t + 0.71);
  IN("#m5-t", { y: 30 }, t + 0.5, 0.5, "expo.out");
  tl.fromTo(".nl", { opacity: 0, x: -50 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out", stagger: 0.1 }, t + 0.7);
  tl.fromTo(".nr", { opacity: 0, x: 50 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out", stagger: 0.1 }, t + 0.8);
  $$(".links path").forEach((p, i) => {
    const len = p.getTotalLength();
    tl.fromTo(p, { strokeDasharray: len + " " + len, strokeDashoffset: len }, { strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }, t + 1.3 + i * 0.12);
  });
  tl.fromTo("#m5-call", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "back.out(1.6)" }, t + 2.4);
  tl.fromTo("#m5-p0, #m5-p1", { strokeWidth: 4 }, { strokeWidth: 9, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 1 }, t + 2.6);
})();

// S10 — rétroviseur
(function () {
  const t = start.s10;
  IN("#s10-t", { y: 40 }, t + 0.5, 0.6, "expo.out");
  IN("#s10-l", { y: 16 }, t + 0.8, 0.6, "power2.out");
  tl.fromTo("#s10-z", { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "expo.inOut" }, t + 1.0);
  $$(".rb").forEach((b, i) => {
    const ti = t + 1.4 + (i % 3) * 0.18 + Math.floor(i / 3) * 1.2;
    tl.fromTo(b, { scaleY: 0 }, { scaleY: 1, duration: 0.8, ease: "power4.out" }, ti);
    IN("#s10-v" + i, { y: 10 }, ti + 0.5, 0.4, "power2.out");
  });
  tl.fromTo(".rn, .rg", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.out", stagger: 0.05 }, t + 1.5);
  IN("#s10-list .sh", {}, t + 4.0, 0.5, "sine.out");
  $$(".srow").forEach((r, i) => {
    IN("#s10-s" + i, { x: 30 }, t + 4.2 + i * 0.2, 0.45, "power3.out");
    tl.fromTo("#s10-sb" + i, { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.out" }, t + 4.35 + i * 0.2);
  });
  IN("#s10-m", { y: 20 }, t + 6.6, 0.8, "power2.out");
  IN("#s10-f", {}, t + 7.4, 0.6, "sine.out");
})();

// S12 — scénarios
(function () {
  const t = start.s12;
  IN("#s12-t", { y: 40 }, t + 0.5, 0.6, "expo.out");
  IN("#s12-l", { y: 16 }, t + 0.8, 0.6, "power2.out");
  tl.fromTo("#s12-z", { scaleY: 0 }, { scaleY: 1, duration: 0.6, ease: "expo.out", transformOrigin: "top center" }, t + 1.2);
  IN("#s12-ax", {}, t + 1.3, 0.6, "sine.out");
  tl.fromTo(".rlab", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out", stagger: 0.3 }, t + 1.4);
  [0, 1].forEach((i) => {
    const ti = t + 1.8 + i * 1.2;
    tl.fromTo("#s12-r" + i, { scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: "power3.inOut" }, ti);
    tl.fromTo("#s12-d" + i, { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(3)" }, ti + 0.7);
    tl.fromTo("#s12-e" + i, { opacity: 0, scale: 0, rotation: 45 }, { opacity: 1, scale: 1, rotation: 45, duration: 0.45, ease: "back.out(3)" }, ti + 0.9);
    tl.fromTo(["#s12-x" + i + "a", "#s12-x" + i + "b", "#s12-x" + i + "c"], { opacity: 0, y: -8 }, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out", stagger: 0.08 }, ti + 0.8);
    IN("#s12-y" + i, { y: 12 }, ti + 1.0, 0.45, "power3.out");
  });
  IN("#s12-cent > .mono", {}, t + 4.6, 0.5, "sine.out");
  tl.fromTo("#s12-cent .cv", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out", stagger: 0.25 }, t + 4.8);
  count("#s12-c1", 100, parseFloat($("#s12-c1").getAttribute("data-v")), 0, t + 5.0, 2.2, { suf: NB + "€", ease: "power2.inOut" });
  count("#s12-c2", 100, parseFloat($("#s12-c2").getAttribute("data-v")), 0, t + 5.25, 2.2, { suf: NB + "€", ease: "power2.inOut" });
  tl.fromTo(".sc", { opacity: 0, x: 50 }, { opacity: 1, x: 0, duration: 0.55, ease: "power4.out", stagger: 0.45 }, t + 7.6);
  IN("#s12-f", {}, t + 9.4, 0.6, "sine.out");
})();

// S13 — risques
(function () {
  const t = start.s13;
  IN("#s13-t", { y: 40 }, t + 0.5, 0.6, "expo.out");
  for (let i = 0; i < 6; i++) {
    const ti = t + 1.0 + i * 0.55;
    tl.fromTo("#s13-k" + i, { opacity: 0, y: 50, rotationX: -25 }, { opacity: 1, y: 0, rotationX: 0, duration: 0.6, ease: "power3.out", transformPerspective: 1000 }, ti);
    tl.fromTo("#s13-kl" + i, { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "expo.inOut" }, ti + 0.2);
  }
})();

// S15 — fin
(function () {
  const t = start.s15;
  IN("#s15-t", { y: 40 }, t + 0.5, 0.7, "expo.out");
  tl.fromTo(".rc", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.55, ease: "back.out(1.6)", stagger: 0.2 }, t + 1.1);
  IN("#s15-d", { y: 20 }, t + 2.2, 0.8, "power2.out");
})();

window.__timelines["main"] = tl;
"""


def build():
    secs = "".join(f'<span class="sec" id="sec{i}">{E(lab)}</span>' for i, (t, lab) in enumerate(SECTIONS))
    scenes = [
        scene_intro(),
        scene_quote("s2", "lynch_peg", "Le critère de ce portefeuille : un PEG proche ou inférieur à 1.", "PEG"),
        scene_peg(), scene_roster(),
        *[scene_card(i + 1, v) for i, v in enumerate(V)],
        scene_growth(), scene_duel(), scene_scatter(),
        scene_quote("s8", "buffett_wonderful", "Cinq entreprises de qualité, achetées à un prix correct plutôt qu'au rabais.", "PRIX"),
        scene_mega(), scene_retro(),
        scene_quote("s11", "lynch_corrections", "Le portefeuille peut rester derrière l'indice un ou deux ans : c'est le prix de la méthode.", "TEMPS"),
        scene_scen(), scene_risks(),
        scene_quote("s14", "lynch_know", "Chaque ligne a sa raison d'être et sa règle de vente.", "SAVOIR"),
        scene_final(),
    ]
    js = (JS.replace("__DATA__", json.dumps(D, ensure_ascii=False))
          .replace("__SCENES__", json.dumps(SCENES)).replace("__TOTAL__", str(TOTAL))
          .replace("__MEGA__", json.dumps(MEGA_T)).replace("__SECTIONS__", json.dumps(SECTIONS, ensure_ascii=False)))
    page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}">
<title>Cinq valeurs pour battre le Nasdaq 100 — {D['date_analyse']}</title>
<script src="vendor/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="{W}" data-height="{H}" data-duration="{TOTAL:g}">
  <div id="bg"><div class="glow a"></div><div class="glow b"></div><div id="grid"></div><div class="vign"></div></div>
  {''.join(scenes)}
  <div class="wipe" id="w0" style="background:{V[0]['couleur']}"></div>
  <div class="wipe" id="w1" style="background:{V[1]['couleur']}"></div>
  <div class="wipe" id="w2" style="background:{V[2]['couleur']}"></div>
  <div class="wipe" id="w3" style="background:{V[3]['couleur']}"></div>
  <div class="wipe" id="w4" style="background:#07090d"></div>
  <div class="band t"></div><div class="band b"></div>
  <div id="hud">
    <div class="hud-top"><span class="mast">La Gazette du PEG*</span><span class="secs">{secs}</span><span>{D['date_analyse']} · cours du {D['date_cours']}</span></div>
    <i class="hud-rule"></i>
    <div class="hud-bot"><span>* Titre fictif : il ne correspond à aucune publication existante.</span><span>Analyse quantitative et datée, pas un conseil en investissement personnalisé.</span></div>
    <i id="progress"></i>
  </div>
  <div id="grain"></div>
  <div id="fade"></div>
  <audio id="bgm" src="audio/bande_son.mp3" data-start="0" data-duration="{TOTAL:g}" data-track-index="10" data-volume="0.9"></audio>
</div>
<script>{js}</script>
</body>
</html>
"""
    with open(os.path.join(VIDEO, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("video/index.html écrit :", len(page), "caractères ;", len(SCENES), "scènes ;", TOTAL, "s")


if __name__ == "__main__":
    build()
