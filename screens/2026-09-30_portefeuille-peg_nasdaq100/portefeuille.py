#!/usr/bin/env python3
"""Portefeuille concentré « PEG à la Peter Lynch » face au Nasdaq 100.

Stdlib uniquement : `python3 portefeuille.py`.

Entrées (dossier data/) :
  zacks_univers.csv    consensus Zacks (BPA non-GAAP), cours au 29/09/2026
  hypotheses.csv       hypothèses de croissance 2027-2031 par scénario (éditoriales)
  qqq_holdings.csv     composition du Nasdaq 100 (QQQ) au 30/09/2026

Sorties :
  resultats_univers.csv   métriques PEG + rendements par scénario, titre par titre
  portefeuille.csv        lignes du portefeuille retenu
  comparaison.csv         portefeuille vs Nasdaq 100 reconstitué
  stress_tests.csv        scénarios de rupture
  sensibilites.csv        variantes du scénario de base
  trios.csv               tous les trios à poids égaux parmi les meilleurs candidats
  monzo.csv               effet d'un accord Nu-Monzo selon le montage
"""
import csv
import itertools
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

HORIZON = 4  # années : 30/09/2026 -> 30/09/2030
PROBAS = {"bear": 0.25, "base": 0.50, "bull": 0.25}
G27_CAP = 50.0  # plafond de croissance pour le PEG 2027 (effets de base)
EXTRAP_CAP = 0.15  # extrapolation d'une année fiscale manquante

# Dernier exercice publié (libellé Zacks) pour les exercices non calendaires.
FY0_ANNEE = {
    "NVDA": 2026, "MRVL": 2026, "WMT": 2026,
    "AVGO": 2025, "AMAT": 2025,
    "LRCX": 2026, "KLAC": 2026, "SNDK": 2026, "LITE": 2026, "COHR": 2026, "MSFT": 2026,
    "MU": 2025, "COST": 2026, "AAPL": 2025, "CRDO": 2026, "CSCO": 2026, "PANW": 2026,
}

# Portefeuille retenu (pondérations éditoriales, voir RAPPORT.md).
PORTEFEUILLE = {"NU": 1 / 3, "AVGO": 1 / 3, "RNMBY": 1 / 3}

# Première version à 8 lignes, conservée pour comparaison.
PORTEFEUILLE_8 = {
    "NVDA": 0.17, "AVGO": 0.16, "NU": 0.14, "UBER": 0.12,
    "TSM": 0.11, "RNMBY": 0.11, "RDDT": 0.11, "CRDO": 0.08,
}

THEMES_IA = ("IA calcul", "IA fonderie et equipement", "IA memoire et stockage",
             "IA reseau et optique", "IA energie et refroidissement")

# Candidats examinés à la demande, ajoutés aux trios même hors du top 8.
CANDIDATS_EN_PLUS = ("ADYEY",)

# Accord Nu-Monzo (presse du 26 au 29/09/2026 : 8 à 10 Md£, numéraire et actions).
MONZO_GBPUSD = 1.33          # 10 Md£ ≈ 13,3 Md$
MONZO_RN_FY26 = 126.0        # M£ : bénéfice avant impôt ajusté FY26 (172,6 M£) après ~27 % d'impôt
MONZO_CROISSANCE_RN = 0.30   # hyp. : croissance annuelle du résultat net de Monzo
MONZO_COUT_NUMERAIRE = 0.04  # hyp. : coût après impôt du numéraire (dette levée ou trésorerie)
# FY26 (avril 2025-mars 2026) est centré sur le 01/10/2025 : l'année 2027 est 1,75 an plus
# loin, le BPA des 12 mois suivant le 30/09/2030 est 5,5 ans plus loin.
MONZO_ANS_2027, MONZO_ANS_2030 = 1.75, 5.5
MONZO_CAS = [
    # (libellé, valorisation en Md£, part payée en numéraire, part du capital acquise,
    #  plafond de P/E de sortie imposé ou None). Un P/E de 13 (médiane 1 an de Nu : 13,75)
    #  traduit la décote d'un groupe moins rentable après l'achat.
    ("Pas d'accord", 0.0, 0.0, 0.0, None),
    ("Participation de 15 % (valorisation 10 Md£)", 10.0, 1.0, 0.15, None),
    ("Rachat à 8 Md£, 75 % en numéraire", 8.0, 0.75, 1.0, None),
    ("Rachat à 9 Md£, moitié numéraire, moitié actions", 9.0, 0.5, 1.0, None),
    ("Rachat à 10 Md£, 75 % en actions", 10.0, 0.25, 1.0, None),
    ("Rachat à 10 Md£, tout en actions", 10.0, 0.0, 1.0, None),
    ("Tout en actions et P/E de sortie plafonné à 13", 10.0, 0.0, 1.0, 13.0),
]


def fnum(x):
    try:
        return float(x) if x not in ("", None) else None
    except ValueError:
        return None


def load(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# --------------------------------------------------------------------------
# BPA calendarisés
# --------------------------------------------------------------------------
def fiscal_series(r):
    """{année fiscale: BPA} complétée si besoin (drapeaux dans r['alertes'])."""
    m = int(r["fye"])
    fy0 = FY0_ANNEE.get(r["ticker"], 2025)
    e0, e1, e2 = fnum(r["eps_fy0"]), fnum(r["eps_f1"]), fnum(r["eps_f2"])
    if e2 is None and e1 is not None:
        e2 = e1 * 1.10
        r["alertes"].append("F2 absent : +10% extrapolé")
    if e0 is None and e1 is not None and e2 is not None and m != 12:
        e0 = e1 / (e2 / e1) if e1 > 0 and e2 > 0 else e1
        r["alertes"].append("FY0 absent : rétro-extrapolé")
    s = {fy0: e0, fy0 + 1: e1, fy0 + 2: e2}
    if e1 and e2 and e1 > 0:
        g = min(max(e2 / e1 - 1, 0.0), EXTRAP_CAP)
    else:
        g = 0.0
    s[fy0 + 3] = e2 * (1 + g) if e2 is not None else None
    return s, m


def calendar_eps(s, m, year):
    if m == 12:
        return s.get(year)
    a, b = s.get(year), s.get(year + 1)
    if a is None or b is None:
        return None
    return (m / 12) * a + ((12 - m) / 12) * b


# --------------------------------------------------------------------------
# Moteur de scénarios (règles identiques pour le portefeuille et l'indice)
# --------------------------------------------------------------------------
def pe_sortie(pe_now, g, scen, cap, constant=False):
    """P/E NTM en 2030. Base : convergence à mi-chemin vers un PEG entre 1 et 1,5.
    Bull : réévaluation jusqu'à PEG 1 (au plus +50 %). Bear : compression vers
    PEG 1,5 sur la croissance bear, bornée entre -20 % et -50 %."""
    if scen == "bear":
        ratio = max(0.5, min(0.8, 1.5 * max(g, 5.0) / pe_now))
        return pe_now * ratio
    if constant:
        return pe_now
    if pe_now > 1.5 * g:
        pe = pe_now - 0.5 * (pe_now - 1.5 * g)
    elif pe_now < g:
        pe = pe_now + 0.5 * (g - pe_now) if scen == "base" else min(g, 1.5 * pe_now)
    else:
        pe = pe_now
    return min(pe, max(pe_now, cap))


def rendements(r, h, constant=False, dg=0.0, ratio_base=None, facteur_bpa=1.0):
    """Rendement total sur l'horizon, par scénario (dividendes réinvestis).
    constant : multiples inchangés (hors bear) ; dg : choc sur la croissance (pts) ;
    ratio_base : BPA 2030 / BPA NTM imposé pour un cyclique en base ;
    facteur_bpa : BPA 2030 multiplié par ce facteur (dilution d'une acquisition)."""
    out = {}
    div = (fnum(r["div_yield"]) or 0.0) / 100
    pe_now = r["pe_ntm"]
    for scen in ("bear", "base", "bull"):
        if h["cyclique"] == "1":
            ratio = fnum(h[f"ratio_bpa_{scen}"])
            if ratio_base is not None and scen == "base":
                ratio = ratio_base
            pe = fnum(h[f"pe_sortie_{scen}"])
            mult = ratio * pe / pe_now
        else:
            g = fnum(h[f"g_{scen}"]) + dg
            cap = fnum(h["pe_plafond"]) or 35.0
            pe = pe_sortie(pe_now, g, scen, cap, constant)
            mult = (1 + g / 100) ** HORIZON * pe / pe_now
        out[scen] = facteur_bpa * mult * (1 + div) ** HORIZON - 1
        out[f"pe_{scen}"] = pe
    out["esperance"] = sum(PROBAS[s] * out[s] for s in PROBAS)
    for k in ("bear", "base", "bull", "esperance"):
        out[f"tcam_{k}"] = (1 + out[k]) ** (1 / HORIZON) - 1
    return out


def pct_rank(values, higher_is_better):
    items = sorted(values.items(), key=lambda kv: kv[1], reverse=higher_is_better)
    n = len(items)
    return {t: 100.0 * (n - i - 1) / (n - 1) if n > 1 else 50.0 for i, (t, _) in enumerate(items)}


# --------------------------------------------------------------------------
# Agrégats de portefeuille
# --------------------------------------------------------------------------
def agregats(poids, rows):
    tot = sum(poids.values())
    w = {t: p / tot for t, p in poids.items()}
    inv_pe = sum(w[t] / rows[t]["pe_ntm"] for t in w)
    pe = 1 / inv_pe
    # croissance pondérée par les bénéfices (part de BPA « achetée »)
    num = den = num_lt = 0.0
    for t in w:
        r = rows[t]
        e = w[t] / r["pe_ntm"]
        g = r["g27_norm"]
        if g is not None:
            num += e * g
            den += e
        num_lt += e * r["g_lt_base"]
    g27 = num / den if den else None
    g_lt = num_lt / inv_pe
    beta = sum(w[t] * (fnum(rows[t]["beta"]) or 1.0) for t in w)
    div = sum(w[t] * (fnum(rows[t]["div_yield"]) or 0.0) for t in w)
    ia = sum(w[t] for t in w if rows[t]["theme"] in THEMES_IA)
    res = {"pe_ntm": pe, "g27": g27, "peg27": pe / min(g27, G27_CAP) if g27 else None,
           "g_lt": g_lt, "peg_lt": pe / g_lt, "beta": beta, "div": div, "part_ia": ia}
    for scen in ("bear", "base", "bull", "esperance"):
        tv = sum(w[t] * (1 + rows[t]["scen"][scen]) for t in w)
        res[scen] = tv - 1
        res[f"tcam_{scen}"] = tv ** (1 / HORIZON) - 1
    return res


def terminal(poids, rendement):
    """TCAM du portefeuille quand rendement(t) donne le rendement total de chaque titre."""
    tot = sum(poids.values())
    tv = sum(p / tot * (1 + rendement(t)) for t, p in poids.items())
    return tv ** (1 / HORIZON) - 1


def monzo(r, h):
    """Effet d'un accord Monzo sur le BPA de Nu (2027 et horizon 2030) et sur ses rendements."""
    prix = fnum(r["prix"])
    n0 = fnum(r["cap_musd"]) / prix  # millions d'actions
    rn27 = r["cy27"] * n0
    bpa30 = r["eps_ntm"] * (1 + fnum(h["g_base"]) / 100) ** HORIZON
    rn30 = bpa30 * n0
    m27 = MONZO_RN_FY26 * MONZO_GBPUSD * (1 + MONZO_CROISSANCE_RN) ** MONZO_ANS_2027
    m30 = MONZO_RN_FY26 * MONZO_GBPUSD * (1 + MONZO_CROISSANCE_RN) ** MONZO_ANS_2030
    cas = []
    for nom, val, part_num, part_cap, pe_cap in MONZO_CAS:
        prix_musd = val * 1000 * MONZO_GBPUSD * part_cap
        numeraire = prix_musd * part_num
        nouvelles = (prix_musd - numeraire) / prix
        cout = numeraire * MONZO_COUT_NUMERAIRE
        n1 = n0 + nouvelles
        d27 = (rn27 + part_cap * m27 - cout) / n1 / r["cy27"] - 1
        d30 = (rn30 + part_cap * m30 - cout) / n1 / bpa30 - 1
        cas.append({"cas": nom, "valorisation_md_gbp": val, "part_numeraire": part_num,
                    "part_capital": part_cap, "prix_md_usd": prix_musd / 1000,
                    "actions_emises_m": nouvelles, "hausse_actions": nouvelles / n0,
                    "bpa_2027_var": d27, "bpa_2030_var": d30, "pe_plafond": pe_cap,
                    "scen": rendements(r, dict(h, pe_plafond=pe_cap) if pe_cap else h,
                                       facteur_bpa=1 + d30)})
    return cas


def main():
    univ = load("zacks_univers.csv")
    hyp = {h["ticker"]: h for h in load("hypotheses.csv")}
    qqq = load("qqq_holdings.csv")

    rows = {}
    for r in univ:
        t = r["ticker"]
        r["alertes"] = []
        s, m = fiscal_series(r)
        cy26, cy27 = calendar_eps(s, m, 2026), calendar_eps(s, m, 2027)
        h = hyp[t]
        if h["ntm_ajuste"] == "cy27":
            ntm = cy27
            r["alertes"].append("BPA 2026 non normalisé : NTM = BPA 2027")
        else:
            ntm = 0.25 * cy26 + 0.75 * cy27
        prix = fnum(r["prix"])
        r.update(cy26=cy26, cy27=cy27, eps_ntm=ntm, pe_ntm=prix / ntm, pe_27=prix / cy27)
        g27 = (cy27 / cy26 - 1) * 100 if cy26 and cy26 > 0 else None
        r["g27"] = g27
        # croissance « normalisée » pour les agrégats : hypothèse de base si 2026 non normalisé
        r["g27_norm"] = fnum(h["g_base"]) if h["ntm_ajuste"] == "cy27" else g27
        r["cyclique"] = h["cyclique"] == "1"
        if r["cyclique"]:
            r["g_lt_base"] = (fnum(h["ratio_bpa_base"]) ** (1 / HORIZON) - 1) * 100
        else:
            r["g_lt_base"] = fnum(h["g_base"])
        valid_g = g27 is not None and g27 > 0 and not r["cyclique"] and h["ntm_ajuste"] != "cy27"
        r["peg27"] = r["pe_27"] / min(g27, G27_CAP) if valid_g else None
        r["peg_lt"] = r["pe_ntm"] / r["g_lt_base"] if not r["cyclique"] and r["g_lt_base"] > 0 else None
        div = fnum(r["div_yield"]) or 0.0
        r["ratio_lynch"] = (r["g_lt_base"] + div) / r["pe_ntm"] if not r["cyclique"] else None
        hi = fnum(r["high_52w"])
        r["repli_52s"] = (prix / hi - 1) * 100 if hi else None
        r["scen"] = rendements(r, h)
        if not r["cyclique"]:
            g = r["g_lt_base"]
            r["prix_peg1"] = g * ntm
            r["prix_peg08"] = 0.8 * g * ntm
        else:
            r["prix_peg1"] = r["prix_peg08"] = None
        r["justification"] = h["justification"]
        rows[t] = r

    # ---------------- score Lynch (titres éligibles) ----------------
    elig = {t: r for t, r in rows.items()
            if not r["cyclique"] and r["peg_lt"] is not None and r["peg_lt"] <= 1.5}
    p_peg = pct_rank({t: r["peg_lt"] for t, r in elig.items()}, False)
    p_ret = pct_rank({t: r["scen"]["tcam_esperance"] for t, r in elig.items()}, True)
    p_p27 = pct_rank({t: (r["peg27"] if r["peg27"] is not None else 2.0) for t, r in elig.items()}, False)
    for t, r in elig.items():
        rank = int(r["zacks_rank"])
        pen = {4: 5.0, 5: 10.0}.get(rank, 0.0)
        r["score_lynch"] = 0.5 * p_peg[t] + 0.3 * p_ret[t] + 0.2 * p_p27[t] - pen
    classement = sorted(elig, key=lambda t: -rows[t]["score_lynch"])
    for i, t in enumerate(classement, 1):
        rows[t]["rang_lynch"] = i

    # ---------------- Nasdaq 100 reconstitué ----------------
    poids_ndx = {}
    for q in qqq:
        t = "GOOGL" if q["ticker"] == "GOOG" else q["ticker"]
        if t in rows:
            poids_ndx[t] = poids_ndx.get(t, 0.0) + float(q["poids_pct"])
    couverture = sum(poids_ndx.values())

    ptf = agregats(PORTEFEUILLE, rows)
    ndx = agregats(poids_ndx, rows)
    ndx_hm = agregats({t: p for t, p in poids_ndx.items() if t not in ("MU", "SNDK")}, rows)
    eq = agregats(PORTEFEUILLE_8, rows)

    # ---------------- accord Nu-Monzo ----------------
    cas_monzo = monzo(rows["NU"], hyp["NU"])
    tout_actions = next(c for c in cas_monzo if c["cas"] == "Rachat à 10 Md£, tout en actions")
    for c in cas_monzo:
        c["ptf_tcam_esperance"] = terminal(
            PORTEFEUILLE, lambda t: (c if t == "NU" else rows[t])["scen"]["esperance"])

    # ---------------- stress tests ----------------
    def ia(t):
        return rows[t]["theme"] in THEMES_IA

    def scen(choix):
        return lambda t: rows[t]["scen"][choix(t)]

    def nu_dilue(s):
        return lambda t: tout_actions["scen"][s] if t == "NU" else rows[t]["scen"]["base"]

    tests = [
        ("Krach du capex IA (valeurs IA en bear, le reste en base)",
         scen(lambda t: "bear" if ia(t) else "base")),
        ("Supercycle mémoire prolongé (MU/SNDK en bull, le reste en base)",
         scen(lambda t: "bull" if t in ("MU", "SNDK") else "base")),
        ("Choc de crédit ou politique au Brésil (NU en bear)",
         scen(lambda t: "bear" if t == "NU" else "base")),
        ("Paix durable en Ukraine (RNMBY en bear)", scen(lambda t: "bear" if t == "RNMBY" else "base")),
        ("Broadcom perd un grand client XPU (AVGO en bear)", scen(lambda t: "bear" if t == "AVGO" else "base")),
        ("Double choc : NU et RNMBY en bear", scen(lambda t: "bear" if t in ("NU", "RNMBY") else "base")),
        ("Nu rachète Monzo 10 Md£ tout en actions (NU en base, BPA dilué)", nu_dilue("base")),
        ("Monzo tout en actions et choc Brésil (NU en bear, BPA dilué)", nu_dilue("bear")),
        ("Tout en base", scen(lambda t: "base")),
    ]
    stress = [(nom, terminal(PORTEFEUILLE, f), terminal(poids_ndx, f)) for nom, f in tests]

    # ---------------- sensibilités (scénario de base) ----------------
    def variante(poids=PORTEFEUILLE, constant=False, dg_ptf=0.0, ratio_mem=None):
        def fn_for(in_ptf):
            def fn(t):
                h = hyp[t]
                dg = dg_ptf if (in_ptf and t in poids) else 0.0
                rb = ratio_mem if t in ("MU", "SNDK") else None
                return rendements(rows[t], h, constant, dg, rb)["base"]
            return fn
        return terminal(poids, fn_for(True)), terminal(poids_ndx, fn_for(False))

    sensib = [
        ("Base du modèle (convergence des PEG à mi-chemin)", *variante()),
        ("Multiples constants pour tous (croissance pure)", *variante(constant=True)),
        ("Croissance du portefeuille -5 pts/an (NDX inchangé)", *variante(dg_ptf=-5.0)),
        ("Croissance du portefeuille -5 pts + multiples constants", *variante(constant=True, dg_ptf=-5.0)),
        ("Mémoire : BPA MU/SNDK maintenus au pic (ratio 1,0)", *variante(ratio_mem=1.0)),
        ("Pire combinaison : -5 pts, multiples constants, mémoire au pic",
         *variante(constant=True, dg_ptf=-5.0, ratio_mem=1.0)),
    ]

    # ---------------- trios à poids égaux ----------------
    candidats = classement[:8] + [t for t in CANDIDATS_EN_PLUS if t in elig and t not in classement[:8]]
    trios = []
    for combo in itertools.combinations(candidats, 3):
        poids = {t: 1 / 3 for t in combo}
        a = agregats(poids, rows)
        a["pessimiste"] = variante(poids, constant=True, dg_ptf=-5.0, ratio_mem=1.0)[0]
        a["nb_ia"] = sum(1 for t in combo if ia(t))
        trios.append((combo, a))
    trios.sort(key=lambda x: -x[1]["tcam_esperance"])
    ndx_pess = variante(constant=True, dg_ptf=-5.0, ratio_mem=1.0)[1]

    # ---------------- sorties CSV ----------------
    cols = ["ticker", "nom", "theme", "prix", "cap_musd", "zacks_rank", "cy26", "cy27", "eps_ntm",
            "pe_ntm", "pe_27", "g27", "peg27", "g_lt_base", "peg_lt", "ratio_lynch", "repli_52s",
            "prix_peg1", "prix_peg08", "score_lynch", "rang_lynch"]
    scols = ["bear", "base", "bull", "esperance", "tcam_bear", "tcam_base", "tcam_bull",
             "tcam_esperance", "pe_bear", "pe_base", "pe_bull"]
    with open(os.path.join(HERE, "resultats_univers.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(cols + scols + ["alertes", "justification"])
        for t in sorted(rows, key=lambda t: (rows[t].get("rang_lynch") or 999, t)):
            r = rows[t]
            line = []
            for c in cols:
                v = r.get(c)
                line.append(round(v, 4) if isinstance(v, float) else v)
            line += [round(r["scen"][c], 4) for c in scols]
            line += [" | ".join(r["alertes"]), r["justification"]]
            wr.writerow(line)

    with open(os.path.join(HERE, "portefeuille.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["ticker", "nom", "poids", "theme", "pe_ntm", "g27", "peg27", "g_lt_base", "peg_lt",
                     "tcam_bear", "tcam_base", "tcam_bull", "tcam_esperance", "prix", "prix_peg1"])
        for t, p in sorted(PORTEFEUILLE.items(), key=lambda kv: -kv[1]):
            r = rows[t]
            wr.writerow([t, r["nom"], p, r["theme"], round(r["pe_ntm"], 2),
                         round(r["g27"], 1) if r["g27"] is not None else "",
                         round(r["peg27"], 2) if r["peg27"] is not None else "",
                         r["g_lt_base"], round(r["peg_lt"], 2),
                         *[round(r["scen"][k], 4) for k in ("tcam_bear", "tcam_base", "tcam_bull", "tcam_esperance")],
                         r["prix"], round(r["prix_peg1"], 2)])

    with open(os.path.join(HERE, "comparaison.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        keys = ["pe_ntm", "g27", "peg27", "g_lt", "peg_lt", "beta", "div", "part_ia",
                "tcam_bear", "tcam_base", "tcam_bull", "tcam_esperance"]
        wr.writerow(["indicateur", "portefeuille", "nasdaq100_reconstitue", "nasdaq100_hors_memoire",
                     "version_8_lignes"])
        for k in keys:
            wr.writerow([k] + [round(x[k], 4) if x[k] is not None else "" for x in (ptf, ndx, ndx_hm, eq)])
        wr.writerow(["couverture_ndx_pct", "", round(couverture, 2), ""])

    with open(os.path.join(HERE, "stress_tests.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["scenario", "tcam_portefeuille", "tcam_nasdaq100", "ecart_pts"])
        for nom, a, b in stress:
            wr.writerow([nom, round(a, 4), round(b, 4), round((a - b) * 100, 2)])

    with open(os.path.join(HERE, "sensibilites.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["variante_scenario_base", "tcam_portefeuille", "tcam_nasdaq100", "ecart_pts"])
        for nom, a, b in sensib:
            wr.writerow([nom, round(a, 4), round(b, 4), round((a - b) * 100, 2)])

    with open(os.path.join(HERE, "trios.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["trio", "nb_valeurs_ia", "pe_ntm", "g27", "peg_lt", "tcam_bear", "tcam_base",
                     "tcam_bull", "tcam_esperance", "tcam_pessimiste"])
        for combo, a in trios:
            wr.writerow([" + ".join(combo), a["nb_ia"], round(a["pe_ntm"], 2), round(a["g27"], 1),
                         round(a["peg_lt"], 2),
                         *[round(a[k], 4) for k in ("tcam_bear", "tcam_base", "tcam_bull", "tcam_esperance",
                                                    "pessimiste")]])
        wr.writerow(["Nasdaq 100 reconstitué", "", round(ndx["pe_ntm"], 2), round(ndx["g27"], 1),
                     round(ndx["peg_lt"], 2),
                     *[round(ndx[k], 4) for k in ("tcam_bear", "tcam_base", "tcam_bull", "tcam_esperance")],
                     round(ndx_pess, 4)])

    with open(os.path.join(HERE, "monzo.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["cas", "valorisation_md_gbp", "part_numeraire", "part_capital", "pe_plafond_impose",
                     "prix_md_usd", "actions_emises_m", "hausse_actions_pct", "bpa_2027_var_pct",
                     "bpa_2030_var_pct", "nu_tcam_bear", "nu_tcam_base", "nu_tcam_bull",
                     "nu_tcam_esperance", "nu_cours_2030_base", "ptf_tcam_esperance"])
        prix_nu = fnum(rows["NU"]["prix"])
        for c in cas_monzo:
            s = c["scen"]
            wr.writerow([c["cas"], c["valorisation_md_gbp"], c["part_numeraire"], c["part_capital"],
                         c["pe_plafond"] or "",
                         round(c["prix_md_usd"], 2), round(c["actions_emises_m"], 0),
                         round(c["hausse_actions"] * 100, 1), round(c["bpa_2027_var"] * 100, 1),
                         round(c["bpa_2030_var"] * 100, 1),
                         *[round(s[k], 4) for k in ("tcam_bear", "tcam_base", "tcam_bull", "tcam_esperance")],
                         round(prix_nu * (1 + s["base"]), 2), round(c["ptf_tcam_esperance"], 4)])

    # ---------------- affichage ----------------
    def pct(x):
        return f"{x * 100:6.1f}%" if x is not None else "   n.d."

    def num(x, d=1):
        return f"{x:6.{d}f}" if x is not None else "  n.d."

    print(f"Nasdaq 100 reconstitué : {len(poids_ndx)} titres, {couverture:.1f} % du poids de l'indice\n")
    print("Classement Lynch (PEG long terme <= 1,5, hors cycliques)")
    print("rg  ticker  P/E NTM  g27    PEG27  g LT  PEG LT  TCAM esp.  score")
    for t in classement:
        r = rows[t]
        print(f"{r['rang_lynch']:>2}  {t:<6} {num(r['pe_ntm'])}  {num(r['g27'], 0)} {num(r['peg27'], 2)}"
              f"  {r['g_lt_base']:4.0f} {num(r['peg_lt'], 2)}  {pct(r['scen']['tcam_esperance'])}  {r['score_lynch']:5.1f}")
    print("\nExclus du classement (PEG LT > 1,5 ou cycliques)")
    for t in sorted(set(rows) - set(elig), key=lambda t: rows[t]["pe_ntm"]):
        r = rows[t]
        lab = "cyclique" if r["cyclique"] else f"PEG LT {r['peg_lt']:.2f}"
        print(f"    {t:<6} P/E NTM {num(r['pe_ntm'])}  {lab:<14} TCAM esp. {pct(r['scen']['tcam_esperance'])}")

    print("\nPortefeuille")
    for t, p in sorted(PORTEFEUILLE.items(), key=lambda kv: -kv[1]):
        r = rows[t]
        s = r["scen"]
        print(f"  {t:<6} {p * 100:4.0f}%  P/E NTM {num(r['pe_ntm'])}  PEG LT {num(r['peg_lt'], 2)}  "
              f"TCAM bear {pct(s['tcam_bear'])} base {pct(s['tcam_base'])} bull {pct(s['tcam_bull'])} "
              f"esp. {pct(s['tcam_esperance'])}  prix PEG1 {r['prix_peg1']:.2f} (cours {r['prix']})")

    print("\n                       Portefeuille   Nasdaq 100  NDX hors mém.  Version 8 lignes")
    for k, lab in (("pe_ntm", "P/E NTM"), ("g27", "Croiss. BPA 2027 %"), ("peg27", "PEG 2027"),
                   ("g_lt", "Croiss. LT hyp. %"), ("peg_lt", "PEG LT"), ("beta", "Bêta"),
                   ("div", "Rendement div. %"), ("part_ia", "Part IA")):
        vals = [x[k] for x in (ptf, ndx, ndx_hm, eq)]
        if k == "part_ia":
            print(f"  {lab:<20} " + "  ".join(f"{v * 100:10.0f}%" for v in vals))
        else:
            print(f"  {lab:<20} " + "  ".join(f"{v:11.2f}" for v in vals))
    for k in ("tcam_bear", "tcam_base", "tcam_bull", "tcam_esperance"):
        print(f"  {k:<20} " + "  ".join(f"{x[k] * 100:10.1f}%" for x in (ptf, ndx, ndx_hm, eq)))

    print("\nSensibilités du scénario de base (TCAM 4 ans)")
    for nom, a, b in sensib:
        print(f"  {nom:<66} ptf {a * 100:6.1f}%  ndx {b * 100:6.1f}%  écart {(a - b) * 100:+5.1f} pts")

    print("\nStress tests (TCAM 4 ans)")
    for nom, a, b in stress:
        print(f"  {nom:<66} ptf {a * 100:6.1f}%  ndx {b * 100:6.1f}%  écart {(a - b) * 100:+5.1f} pts")

    print("\nAccord Nu-Monzo : effet sur le BPA de Nu et sur le portefeuille")
    print("  cas                                                 actions  BPA 2027  BPA 2030  NU esp.  ptf esp.")
    for c in cas_monzo:
        print(f"  {c['cas']:<50} {c['hausse_actions'] * 100:+6.1f}%  {c['bpa_2027_var'] * 100:+7.1f}%"
              f"  {c['bpa_2030_var'] * 100:+7.1f}%  {pct(c['scen']['tcam_esperance'])}  {pct(c['ptf_tcam_esperance'])}")

    print("\nTrios à poids égaux (TCAM 4 ans ; pessimiste = -5 pts, multiples constants, mémoire au pic)")
    print(f"  candidats : {', '.join(candidats)}")
    for i, (combo, a) in enumerate(trios, 1):
        if i <= 12 or any(t in CANDIDATS_EN_PLUS for t in combo):
            print(f"  {i:>2}. {' + '.join(combo):<22} IA {a['nb_ia']}  esp. {pct(a['tcam_esperance'])}  "
                  f"bear {pct(a['tcam_bear'])}  base {pct(a['tcam_base'])}  bull {pct(a['tcam_bull'])}  "
                  f"pess. {pct(a['pessimiste'])}")
    print(f"      Nasdaq 100 reconstitué        esp. {pct(ndx['tcam_esperance'])}  bear {pct(ndx['tcam_bear'])}  "
          f"base {pct(ndx['tcam_base'])}  bull {pct(ndx['tcam_bull'])}  pess. {pct(ndx_pess)}")


if __name__ == "__main__":
    main()
