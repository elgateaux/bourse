#!/usr/bin/env python3
"""Génère BILAN.html : le bilan complet du portefeuille PEG, sous forme d'article de journal.
Les chiffres viennent des sorties de portefeuille.py (CSV du dossier du screen) ; les prix
d'entrée sont recalculés avec le même moteur (portefeuille.rendements)."""
import csv
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

D = sys.argv[1]          # dossier du screen
OUT = sys.argv[2]        # fichier HTML de sortie
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import portefeuille as M  # noqa: E402


def lire(nom, dossier=D):
    with open(os.path.join(dossier, nom), encoding="utf-8") as f:
        return list(csv.DictReader(f))


res = {r["ticker"]: r for r in lire("resultats_univers.csv")}
univ = {r["ticker"]: r for r in lire("zacks_univers.csv", os.path.join(D, "data"))}
hyp = {r["ticker"]: r for r in lire("hypotheses.csv", os.path.join(D, "data"))}
cmp_ = {r["indicateur"]: r for r in lire("comparaison.csv")}
stress = {r["scenario"]: r for r in lire("stress_tests.csv")}
sens = {r["variante_scenario_base"]: r for r in lire("sensibilites.csv")}
var = {r["variante"]: r for r in lire("variantes.csv")}
poche = lire("poche_etf.csv")
mem = lire("memoire.csv")
nvd = {r["cas"]: r for r in lire("nvidia.csv")}
monzo = {r["cas"]: r for r in lire("monzo.csv")}


# ------------------------------------------------------------------ formats
def q(x, d):
    """Arrondi à d décimales, demi vers le haut (évite 6,35 -> 6,3)."""
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
    return fr(100 * x, d, signe) + " %"


def px_calc(x):
    """Cours calculé (2030, zone d'achat) : précision adaptée à l'ordre de grandeur."""
    return fr(x, 2 if x < 10 else (1 if x < 100 else 0)) + " $"


def px_cote(x):
    return fr(x, 2) + " $"


def f(r, k):
    return float(r[k])


P, N, NH, V4 = "portefeuille", "nasdaq100_reconstitue", "nasdaq100_hors_memoire", "version_4_lignes"


def c(col, k):
    return float(cmp_[k][col])


RET = "Retenu : Nu 30 %, Rheinmetall 30 %, TSMC 15 %, Uber 15 %, NVIDIA 10 %"
MATIN = "Version du matin : Nu, Rheinmetall 1/3 ; NVIDIA, TSMC 1/6"
TRIO = "Trio du 30/09 : Nu, Broadcom, Rheinmetall"
HUIT = "Première version à 8 lignes"
assert abs(f(var[RET], "tcam_esperance") - c(P, "tcam_esperance")) < 1e-4
assert abs(sum(M.PORTEFEUILLE.values()) - 1) < 1e-9

NOMS = {"NU": "Nu", "RNMBY": "Rheinmetall", "TSM": "TSMC", "UBER": "Uber", "NVDA": "NVIDIA",
        "CRDO": "Credo", "AVGO": "Broadcom", "RDDT": "Reddit", "ORCL": "Oracle", "GRAB": "Grab",
        "SE": "Sea", "ADYEY": "Adyen", "MELI": "Mercado Libre", "ATEYY": "Advantest", "AMZN": "Amazon",
        "GOOGL": "Alphabet", "MSFT": "Microsoft", "SKHY": "SK Hynix", "ASML": "ASML", "MU": "Micron"}


def tc(t, k):
    return f(res[t], f"tcam_{k}")


def cours2030(t, scen="base"):
    return f(res[t], "prix") * (1 + f(res[t], scen))


# ------------------------------------------------------------------ infographie 1 : fourchettes
LO, HI = -20.0, 50.0


def xpos(v):
    return (100 * v - LO) / (HI - LO) * 100


lignes = ["NU", "RNMBY", "TSM", "UBER", "NVDA"]
ranges = [(NOMS[t], tc(t, "bear"), tc(t, "base"), tc(t, "bull"), tc(t, "esperance"), "") for t in lignes]
ranges += [("Portefeuille", c(P, "tcam_bear"), c(P, "tcam_base"), c(P, "tcam_bull"), c(P, "tcam_esperance"), " is-key"),
           ("Nasdaq 100", c(N, "tcam_bear"), c(N, "tcam_base"), c(N, "tcam_bull"), c(N, "tcam_esperance"), " is-ref")]
f1 = []
for lab, b, m, u, e, cls in ranges:
    f1.append(f'''<div class="rg-row{cls}">
  <div class="rg-label">{lab}</div>
  <div class="rg-track" title="{lab} : pessimiste {pct(b)}, central {pct(m)}, optimiste {pct(u)}, espéré {pct(e)} par an">
    <span class="rg-zero" style="left:{xpos(0):.1f}%"></span>
    <span class="rg-span" style="left:{xpos(b):.1f}%;width:{xpos(u) - xpos(b):.1f}%"></span>
    <span class="rg-end" style="left:{xpos(b):.1f}%"></span><span class="rg-end" style="left:{xpos(u):.1f}%"></span>
    <span class="rg-base" style="left:{xpos(m):.1f}%"></span>
    <span class="rg-exp" style="left:{xpos(e):.1f}%"></span>
  </div>
  <div class="rg-val"><b>{pct(e)}</b><span>{pct(b)} à {pct(u)}</span></div>
</div>''')
fig_ranges = "\n".join(f1)
ticks = "".join(f'<span style="left:{xpos(v / 100):.1f}%">{fr(v, 0, signe=v > 0)} %</span>'
                for v in (-20, -10, 0, 10, 20, 30, 40, 50))

# ------------------------------------------------------------------ infographie 2 : versions
ndx_dbl = f(stress["Double choc : NU et RNMBY en bear"], "tcam_nasdaq100")
versions = [("Première version", "30/09 · huit valeurs, de NVIDIA à Credo", var[HUIT], False),
            ("Trio", "30/09 · Nu, Broadcom, Rheinmetall", var[TRIO], False),
            ("Version du matin", "01/10 · Nu, Rheinmetall, NVIDIA, TSMC", var[MATIN], False),
            ("Version retenue", "01/10 · avec Uber à 15 %", var[RET], True)]
MAXV = 0.30
f2 = []
for lab, sous, r, fort in versions + [("Nasdaq 100 reconstitué", "31 valeurs, 74 % de l'indice", None, False)]:
    esp = f(r, "tcam_esperance") if r else c(N, "tcam_esperance")
    dbl = f(r, "tcam_double_choc") if r else ndx_dbl
    f2.append(f'''<div class="gb-row{' is-key' if fort else ''}">
  <div class="gb-label"><b>{lab}</b><span>{sous}</span></div>
  <div class="gb-bars">
    <div class="gb-line"><div class="gb-track"><div class="gb-bar s1" style="width:{100 * esp / MAXV:.1f}%" title="{lab} : rendement espéré {pct(esp)} par an"></div></div><span class="gb-val">{pct(esp)}</span></div>
    <div class="gb-line"><div class="gb-track"><div class="gb-bar s2" style="width:{100 * dbl / MAXV:.1f}%" title="{lab} : {pct(dbl)} par an si Nu et Rheinmetall déçoivent ensemble"></div></div><span class="gb-val">{pct(dbl)}</span></div>
  </div>
</div>''')
fig_versions = "\n".join(f2)

t_versions = ""
for lab, sous, r, fort in versions:
    cls = ' class="ptf"' if fort else ""
    t_versions += (f'<tr{cls}><td>{lab} <span style="color:var(--muted)">({sous.split(" · ")[0]})</span></td>'
                   f'<td>{pct(f(r, "tcam_esperance"))}</td><td>{pct(f(r, "tcam_bear"))}</td>'
                   f'<td>{pct(f(r, "tcam_krach_ia"))}</td><td>{pct(f(r, "tcam_double_choc"))}</td>'
                   f'<td>{pct(f(r, "p_sous_indice"))}</td><td>{pct(f(r, "p_perte"))}</td></tr>')
krach_ndx = f(stress["Krach du capex IA (valeurs IA en bear, le reste en base)"], "tcam_nasdaq100")
t_versions += (f'<tr class="ref"><td>Nasdaq 100 reconstitué</td><td>{pct(c(N, "tcam_esperance"))}</td>'
               f'<td>{pct(c(N, "tcam_bear"))}</td><td>{pct(krach_ndx)}</td><td>{pct(ndx_dbl)}</td><td>—</td><td>—</td></tr>')

# ------------------------------------------------------------------ tableau du portefeuille
t_ptf = ""
for t in lignes:
    r = res[t]
    w = M.PORTEFEUILLE[t]
    nom = NOMS[t] + (" (ADR)" if t == "RNMBY" else "")
    t_ptf += (f'<tr><td>{nom}</td><td>{fr(100 * w, 0)} %</td><td>{px_cote(f(r, "prix"))}</td>'
              f'<td>{fr(f(r, "pe_ntm"))}</td><td>{fr(f(r, "g27"), 0, True)} %</td><td>{fr(f(r, "peg_lt"), 2)}</td>'
              f'<td class="hl">{pct(tc(t, "esperance"))}</td><td>{px_calc(cours2030(t))}</td>'
              f'<td>≤ {px_calc(f(r, "prix_peg1"))}</td></tr>')
t_ptf += (f'<tr class="tot"><td>Portefeuille</td><td>100 %</td><td></td><td>{fr(c(P, "pe_ntm"))}</td>'
          f'<td>{fr(c(P, "g27"), 0, True)} %</td><td>{fr(c(P, "peg_lt"), 2)}</td><td class="hl">{pct(c(P, "tcam_esperance"))}</td>'
          f'<td></td><td></td></tr>')
t_ptf += (f'<tr class="ref"><td>Nasdaq 100 reconstitué</td><td></td><td></td><td>{fr(c(N, "pe_ntm"))}</td>'
          f'<td>{fr(c(N, "g27"), 0, True)} %</td><td>{fr(c(N, "peg_lt"), 2)}*</td><td>{pct(c(N, "tcam_esperance"))}</td>'
          f'<td></td><td></td></tr>')

# ------------------------------------------------------------------ NVIDIA face au sur-mesure
nv_lab = [("Bull du modèle", "Optimiste du modèle : BPA +25 %/an"),
          ("Base du modèle", "Central du modèle : BPA +15 %/an"),
          ("Marges comprimées", "Marges comprimées : BPA +7 %/an, P/E 14"),
          ("Disruption", "Disruption : BPA stable, P/E 10"),
          ("Bear du modèle", f"Pessimiste du modèle : BPA stable, P/E {fr(f(res['NVDA'], 'pe_bear'))}")]
t_nv = ""
for k, lab in nv_lab:
    r = nvd[k]
    cls = ' class="negv"' if f(r, "nvda_tcam") < 0 else ""
    t_nv += (f'<tr><td>{lab}</td><td{cls}>{pct(f(r, "nvda_tcam"))}</td><td>{px_calc(f(r, "nvda_cours_2030"))}</td>'
             f'<td class="hl">{pct(f(r, "ptf_tsm_base"))}</td><td>{pct(f(r, "ptf_tsm_bull"))}</td><td>{pct(f(r, "ndx"))}</td></tr>')

# ------------------------------------------------------------------ infographie 3 : puces d'Anthropic
sur_mesure, gpu, amd = 161.2 + 111.1 + 110.0, 84.5 + 31.4, 20.0
tot = sur_mesure + gpu + amd

# ------------------------------------------------------------------ mémoire
mem_ix = {(r["ticker"], r["cas"]): r for r in mem}
mem_rows = [("Cycle sévère", "−65 %"), ("Cycle normal", "−50 %"), ("Cycle doux", "−35 %"),
            ("Le cycle disparaît, P/E 12", "Stables, au sommet"), ("Croissance de 10 %/an, P/E 12", "+46 % (+10 % par an)")]
t_mem = ""
for cas, lab in mem_rows:
    a, b = mem_ix[("SKHY", cas)], mem_ix[("MU", cas)]
    na = ' class="negv"' if f(a, "tcam") < 0 else ""
    nb = ' class="negv"' if f(b, "tcam") < 0 else ""
    t_mem += (f'<tr><td>{lab}</td><td>{fr(f(a, "pe_sortie"), 0)}</td>'
              f'<td{na}>{pct(f(a, "tcam"))}</td><td{nb}>{pct(f(b, "tcam"))}</td></tr>')

# ------------------------------------------------------------------ poches ETF et fonds
t_etf, t_fonds = "", ""
for r in poche:
    w = f(r, "part")
    if r["poche"] == "ETF Nasdaq 100":
        lab = "Aucune (portefeuille seul)" if w == 0 else fr(100 * w, 0) + " %"
        cls = ' class="ptf"' if w == 0 else ""
        t_etf += (f'<tr{cls}><td>{lab}</td><td>{pct(f(r, "tcam_esperance"))}</td><td>{pct(f(r, "tcam_double_choc"))}</td>'
                  f'<td>{pct(f(r, "tcam_krach_ia"))}</td><td>{pct(f(r, "tcam_bear"))}</td></tr>')
    else:
        t_fonds += (f'<tr><td>{fr(100 * w, 0)} %</td><td>{fr(100 * f(r, "rendement_fonds_hyp"), 0)} % par an</td>'
                    f'<td>{pct(f(r, "tcam_esperance"))}</td><td>{pct(f(r, "tcam_double_choc"))}</td></tr>')
t_fonds += (f'<tr class="ptf"><td>Aucune</td><td>—</td><td>{pct(c(P, "tcam_esperance"))}</td>'
            f'<td>{pct(f(var[RET], "tcam_double_choc"))}</td></tr>')

# ------------------------------------------------------------------ infographie 4 : le screen
ecran = ["NU", "RNMBY", "CRDO", "AVGO", "UBER", "RDDT", "ORCL", "GRAB", "SE", "ADYEY", "MELI", "NVDA", "TSM",
         "ATEYY", "AMZN", "GOOGL", "MSFT", "SKHY", "ASML", "MU"]
pts = [(t, NOMS[t], tc(t, "esperance")) for t in ecran] + [("NDX", "Nasdaq 100", c(N, "tcam_esperance"))]
pts.sort(key=lambda x: -x[2])
REF = tc("TSM", "esperance")
f4 = []
for t, lab, e in pts:
    cls = " is-ptf" if t in M.PORTEFEUILLE else (" is-ndx" if t == "NDX" else "")
    statut = "dans le portefeuille" if t in M.PORTEFEUILLE else ("indice" if t == "NDX" else "hors portefeuille")
    f4.append(f'<div class="sb-row{cls}"><span class="sb-lab">{lab}</span>'
              f'<div class="sb-track"><span class="sb-ref" style="left:{100 * REF / MAXV:.2f}%"></span>'
              f'<div class="sb-bar" style="width:{100 * e / MAXV:.1f}%" title="{lab} ({statut}) : {pct(e)} par an espérés"></div></div>'
              f'<span class="sb-val">{pct(e)}</span></div>')
fig_screen = "\n".join(f4)

# ------------------------------------------------------------------ candidats
VERDICTS = {
    "CRDO": f"La meilleure idée IA du screen hors portefeuille, mais une petite valeur très volatile (pessimiste {pct(tc('CRDO', 'bear'))} par an).",
    "AVGO": "Sortie le 01/10 : dépendance à Anthropic. Revient si l'introduction d'Anthropic réduit ce risque.",
    "RDDT": "Dépend du trafic venu de Google. Rendez-vous le 29/10.",
    "ORCL": "Pari à effet de levier sur OpenAI : trésorerie négative, dilution. À la place de NVIDIA, pas en plus.",
    "GRAB": "Correcte, mais moins bien qu'Uber, qui en détient 13,5 %. Grèves au Vietnam, fusion avec GoTo incertaine.",
    "SE": "Les analystes baissent leurs prévisions (Zacks Rank 5).",
    "ADYEY": "Moins bien que Nu. Entrée sous 685 € environ.",
    "MELI": "Même région que Nu, trois fois plus chère. Prévisions en baisse (Zacks Rank 4).",
    "ATEYY": "Le bon thème, la complexité des puces, mais un prix qui l'a intégré (+122 % en un an).",
    "AMZN": "Belle entreprise à prix plein, même en retirant sa participation dans Anthropic.",
    "GOOGL": "Prix plein. Participation de 10 à 15 % dans Anthropic.",
    "MSFT": "Azure +43 %, mais 25 fois les bénéfices pour 15 % de croissance.",
    "SKHY": "Cyclique au sommet : un pari binaire sur la fin du cycle.",
    "ASML": "33 fois les bénéfices pour environ 14 % de croissance annuelle.",
    "MU": "Cyclique au sommet, déjà 5 % du Nasdaq 100.",
}
t_cand = ""
for t in sorted(VERDICTS, key=lambda t: -tc(t, "esperance")):
    r = res[t]
    adr = " (ADR)" if t in ("ATEYY", "SKHY", "ADYEY") else ""
    cyc = r["peg_lt"] == ""
    croiss = "cyclique" if cyc else fr(f(r, "g_lt_base"), 0) + " %"
    peg = "—" if cyc else fr(f(r, "peg_lt"), 2)
    zone = "—" if cyc else "≤ " + px_calc(f(r, "prix_peg1"))
    pe_note = "*" if t in ("GRAB", "AMZN", "GOOGL") else ""
    t_cand += (f'<tr><td>{NOMS[t]}{adr}</td><td>{px_cote(f(r, "prix"))}</td><td>{fr(f(r, "pe_ntm"))}{pe_note}</td>'
               f'<td>{croiss}</td><td>{peg}</td><td>{pct(tc(t, "esperance"))}</td><td>{zone}</td>'
               f'<td class="verdict">{VERDICTS[t]}</td></tr>')


# ------------------------------------------------------------------ prix d'entrée d'Oracle (même moteur)
def prix_pour(t, cible):
    u, h = univ[t], hyp[t]
    eps = f(res[t], "eps_ntm")
    lo, hi = 0.2 * f(u, "prix"), 1.5 * f(u, "prix")
    for _ in range(80):
        mid = (lo + hi) / 2
        e = M.rendements({"div_yield": u["div_yield"], "pe_ntm": mid / eps}, h)["tcam_esperance"]
        lo, hi = (mid, hi) if e > cible else (lo, mid)
    return lo


orcl_seuil = prix_pour("ORCL", c(P, "tcam_esperance"))

# ------------------------------------------------------------------ stress tests
stress_rows = [
    ("Tout en central", "Tout en base"),
    ("Krach de l'IA", "Krach du capex IA (valeurs IA en bear, le reste en base)"),
    ("Les puces sur mesure gagnent (NVIDIA pessimiste, TSMC optimiste)", "Les puces sur mesure gagnent (NVDA en bear, TSM en bull)"),
    ("Choc dur sur Taïwan (TSMC et NVIDIA pessimistes)", "Choc dur sur Taïwan (TSM et NVDA en bear)"),
    ("NVIDIA tient ses promesses (optimiste)", "NVIDIA tient ses promesses (NVDA en bull)"),
    ("Les robotaxis contournent Uber", "Les robotaxis contournent Uber (UBER en bear)"),
    ("Crédit ou politique au Brésil (Nu)", "Choc de crédit ou politique au Brésil (NU en bear)"),
    ("Paix durable en Ukraine (Rheinmetall)", "Paix durable en Ukraine (RNMBY en bear)"),
    ("Nu rachète Monzo tout en actions", "Nu rachète Monzo 10 Md£ tout en actions (NU en base, BPA dilué)"),
    ("Le supercycle de la mémoire se prolonge", "Supercycle mémoire prolongé (MU/SNDK en bull, le reste en base)"),
    ("Nu et Rheinmetall déçoivent ensemble", "Double choc : NU et RNMBY en bear"),
    ("Tout en pessimiste", "Tout en bear"),
    ("Tout en optimiste", "Tout en bull"),
]
t_stress = ""
for lab, k in stress_rows:
    r = stress[k]
    a, a4, b = f(r, "tcam_portefeuille"), f(r, "tcam_version_4_lignes"), f(r, "tcam_nasdaq100")
    ecart = float(q(100 * a, 1) - q(100 * b, 1))
    cls = ' class="neg"' if ecart < 0 else ""
    t_stress += (f'<tr{cls}><td>{lab}</td><td class="hl">{pct(a)}</td><td>{pct(a4)}</td><td>{pct(b)}</td>'
                 f'<td>{fr(ecart, 1, signe=True)} pts</td></tr>')


def ecart_sens(nom):
    return fr(f(sens[nom], "ecart_pts"), 1)


esp8 = f(var[HUIT], "tcam_esperance")
vals = {
    "pe": fr(c(P, "pe_ntm")), "pe_ndx": fr(c(N, "pe_ntm")),
    "esp": pct(c(P, "tcam_esperance")), "esp_ndx": pct(c(N, "tcam_esperance")),
    "esp4": pct(c(V4, "tcam_esperance")), "esp_trio": pct(f(var[TRIO], "tcam_esperance")),
    "bear": pct(c(P, "tcam_bear")), "bear_ndx": pct(c(N, "tcam_bear")),
    "bear_abs": pct(-c(P, "tcam_bear")), "bear_ndx_abs": pct(-c(N, "tcam_bear")),
    "dbl": pct(f(var[RET], "tcam_double_choc")), "dbl4": pct(f(var[MATIN], "tcam_double_choc")),
    "dbl_ndx": pct(ndx_dbl), "ndx_base": pct(c(N, "tcam_base")),
    "peg": fr(c(P, "peg_lt"), 2), "peg_ndx_hm": fr(c(NH, "peg_lt"), 2),
    "peg_ratio": fr(c(NH, "peg_lt") / c(P, "peg_lt"), 1),
    "ia": fr(100 * c(P, "part_ia"), 0) + " %", "ia_ndx": fr(100 * c(N, "part_ia"), 0) + " %",
    "p5": pct(f(var[RET], "p_sous_indice")), "p8": pct(f(var[HUIT], "p_sous_indice")),
    "ecart8": fr(float(q(100 * c(P, "tcam_esperance"), 1) - q(100 * esp8, 1)), 1),
    "nu_bear": pct(tc("NU", "bear")), "nv_bear": pct(tc("NVDA", "bear")), "nv_bull": pct(tc("NVDA", "bull")),
    "uber_pe": fr(f(res["UBER"], "pe_ntm")), "uber_pe27": fr(f(res["UBER"], "pe_27")),
    "uber_g27": fr(f(res["UBER"], "g27"), 0, True) + " %", "uber_esp": pct(tc("UBER", "esperance")),
    "uber_bear": pct(tc("UBER", "bear")), "uber_bear_abs": pct(-tc("UBER", "bear")), "uber_c30_bear": fr(cours2030("UBER", "bear"), 0) + " $",
    "uber_peg1": px_calc(f(res["UBER"], "prix_peg1")),
    "uber_marge": fr(100 * (1 - f(res["UBER"], "prix") / f(res["UBER"], "prix_peg1")), 0) + " %",
    "nu_pe": fr(f(res["NU"], "pe_ntm")), "nu_peg": fr(f(res["NU"], "peg_lt"), 2), "nu_esp": pct(tc("NU", "esperance")),
    "nu_c30": px_calc(cours2030("NU")), "nu_peg1": px_calc(f(res["NU"], "prix_peg1")),
    "monzo_ptf": pct(f(monzo["Rachat à 10 Md£, tout en actions"], "ptf_tcam_esperance")),
    "rh_esp": pct(tc("RNMBY", "esperance")), "rh_c30": px_calc(cours2030("RNMBY")),
    "tsm_peg": fr(f(res["TSM"], "peg_lt"), 2), "tsm_esp": pct(tc("TSM", "esperance")), "tsm_pe": fr(f(res["TSM"], "pe_ntm")),
    "tsm_c30": px_calc(cours2030("TSM")), "tsm_peg1": px_calc(f(res["TSM"], "prix_peg1")),
    "nv_esp": pct(tc("NVDA", "esperance")), "nv_c30": px_calc(cours2030("NVDA")), "nv_peg1": px_calc(f(res["NVDA"], "prix_peg1")),
    "skhy_pe": fr(f(res["SKHY"], "pe_ntm")), "mu_pe": fr(f(res["MU"], "pe_ntm")),
    "ndx_mem": pct(f(stress["Supercycle mémoire prolongé (MU/SNDK en bull, le reste en base)"], "tcam_nasdaq100")),
    "at_pe": fr(f(res["ATEYY"], "pe_ntm")), "at_esp": pct(tc("ATEYY", "esperance")),
    "at_peg1": px_calc(f(res["ATEYY"], "prix_peg1")),
    "grab_esp": pct(tc("GRAB", "esperance")), "se_esp": pct(tc("SE", "esperance")),
    "orcl_pe": fr(f(res["ORCL"], "pe_ntm")), "orcl_bear": pct(tc("ORCL", "bear")),
    "orcl_var": pct(f(var["Retenu, Oracle à la place de NVIDIA"], "tcam_esperance")),
    "orcl_seuil": px_calc(orcl_seuil), "googl_esp": pct(tc("GOOGL", "esperance")),
    "sens_base": ecart_sens("Base du modèle (convergence des PEG à mi-chemin)"),
    "sens_const": ecart_sens("Multiples constants pour tous (croissance pure)"),
    "sens_const5": ecart_sens("Croissance du portefeuille -5 pts + multiples constants"),
    "sens_pire": ecart_sens("Pire combinaison : -5 pts, multiples constants, mémoire au pic"),
    "SM_W": f"{100 * sur_mesure / tot:.1f}", "GPU_W": f"{100 * gpu / tot:.1f}",
    "SM_V": fr(sur_mesure, 0), "GPU_V": fr(gpu, 0), "SM_P": fr(100 * sur_mesure / tot, 0),
    "GPU_P": fr(100 * gpu / tot, 0), "AMD_P": fr(100 * amd / tot, 0),
}
blocs = {"FIG_RANGES": fig_ranges, "TICKS": ticks, "FIG_VERSIONS": fig_versions, "T_VERSIONS": t_versions,
         "T_PTF": t_ptf, "T_NVIDIA": t_nv, "T_MEM": t_mem, "T_ETF": t_etf, "T_FONDS": t_fonds,
         "FIG_SCREEN": fig_screen, "T_CAND": t_cand, "T_STRESS": t_stress}

# ------------------------------------------------------------------ assemblage
ancien = open(os.path.join(ICI, "..", "article", "template.html"), encoding="utf-8").read().split("\n")
i_style = ancien.index("<style>")
i_motion = next(i for i, l in enumerate(ancien) if l.startswith("@media (prefers-reduced-motion"))
i_fin = ancien.index("</style>")
css_base = "\n".join(ancien[i_style + 1:i_motion])
css_fin = "\n".join(ancien[i_motion:i_fin]).replace(
    ".fig, .fiche, .encadre, table, .quote { break-inside: avoid; }",
    ".fig, .fiche, .encadre, table, .quote, .card, .lecture, .zone { break-inside: avoid; }")
assert "break-inside: avoid; }" in css_fin and ".card" in css_fin
polices = "\n".join(ancien[1:i_style])
extra = open(os.path.join(ICI, "css_extra.css"), encoding="utf-8").read()
corps = open(os.path.join(ICI, "body.html"), encoding="utf-8").read()

for k, v in blocs.items():
    assert "{{" + k + "}}" in corps, k
    corps = corps.replace("{{" + k + "}}", v)
for k, v in vals.items():
    corps = corps.replace("{{" + k + "}}", v)
assert "{{" not in corps, corps[corps.index("{{"):corps.index("{{") + 40]
for a, b in ((" %", " %"), (" $", " $"), (" €", " €"), (" :", " :"), (" ;", " ;"),
             (" ?", " ?"), ("« ", "« "), (" »", " »"), (" Md", " Md"), (" M$", " M$"),
             (" pts", " pts")):
    corps = corps.replace(a, b)
html = ("<title>Bilan du portefeuille PEG</title>\n" + polices + "\n<style>\n" + css_base + extra + "\n" + css_fin +
        "\n</style>\n\n" + corps)
open(OUT, "w", encoding="utf-8").write(html)
print("ok", len(html), "octets ; Oracle rejoint l'espérance du portefeuille sous", px_calc(orcl_seuil))
