#!/usr/bin/env python3
"""Portefeuille de cinq valeurs (NVIDIA, TSMC, Nu, Reddit, Adyen) face au Nasdaq 100, au 13/10/2026.

Stdlib uniquement : `python3 calcul.py`.

Mêmes règles que le modèle du 30/09/2026 : les fonctions de scénarios, d'agrégats et de
probabilités sont importées de screens/2026-09-30_portefeuille-peg_nasdaq100/portefeuille.py.
Seules changent les données (consensus Zacks du 13/10/2026, cours du 12/10/2026) et le poids
du BPA de l'année en cours dans le BPA des 12 prochains mois, calculé à la date d'analyse.

Entrées (data/) :
  zacks_2026-10-13.csv   consensus BPA non-GAAP, cours, variations ; 5 valeurs + 31 du Nasdaq 100
  hypotheses.csv         croissances 2027-2030 par scénario (hyp. du 30/09, SPCX ajusté)
  portefeuille.csv       poids des cinq lignes (hyp. : poids égaux)
  indices_2026-10-13.csv performances du QQQ et du SPY
  citations.csv, megatendances.csv   textes sourcés de la vidéo
  ../2026-09-30_portefeuille-peg_nasdaq100/data/qqq_holdings.csv   poids du Nasdaq 100 (30/09)

Sorties :
  valeurs.csv, comparaison.csv, stress_tests.csv, retroviseur.csv
  video/donnees_video.json   chiffres déjà formatés pour la vidéo
"""
import csv
import datetime as dt
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
MODELE_DIR = os.path.join(HERE, "..", "2026-09-30_portefeuille-peg_nasdaq100")

spec = importlib.util.spec_from_file_location("modele", os.path.join(MODELE_DIR, "portefeuille.py"))
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

DATE_ANALYSE = dt.date(2026, 10, 13)
DATE_COURS = "12/10/2026"
HORIZON = M.HORIZON  # 4 ans : 13/10/2026 -> 13/10/2030
# Mois écoulés dans l'année : le BPA NTM pèse (12 - k)/12 de l'année N et k/12 de l'année N+1.
K_MOIS = (DATE_ANALYSE - dt.date(2026, 1, 1)).days / 365.25 * 12
W_N, W_N1 = (12 - K_MOIS) / 12, K_MOIS / 12

TICKERS = ("NVDA", "TSM", "NU", "RDDT", "ADYEY")


def load(name, base=DATA):
    with open(os.path.join(base, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fnum(x):
    return M.fnum(x)


def fiscal_series(r):
    """Comme le modèle du 30/09, mais l'année du dernier exercice publié vient du CSV
    (lue dans la section EDT de Zacks) au lieu d'une table dans le code."""
    m, fy0 = int(r["fye"]), int(r["fy0_annee"])
    e0, e1, e2 = fnum(r["eps_fy0"]), fnum(r["eps_f1"]), fnum(r["eps_f2"])
    s = {fy0: e0, fy0 + 1: e1, fy0 + 2: e2}
    g = min(max(e2 / e1 - 1, 0.0), M.EXTRAP_CAP) if e1 and e2 and e1 > 0 else 0.0
    s[fy0 + 3] = e2 * (1 + g) if e2 is not None else None
    return s, m


def construire_lignes():
    univ = load("zacks_2026-10-13.csv")
    hyp = {h["ticker"]: h for h in load("hypotheses.csv")}
    rows = {}
    for r in univ:
        t = r["ticker"]
        h = hyp[t]
        r["alertes"] = []
        s, m = fiscal_series(r)
        cy26, cy27 = M.calendar_eps(s, m, 2026), M.calendar_eps(s, m, 2027)
        if h["ntm_ajuste"] == "cy27":
            ntm = cy27
            r["alertes"].append("BPA 2026 non normalisé : NTM = BPA 2027")
        else:
            ntm = W_N * cy26 + W_N1 * cy27
        prix = fnum(r["prix"])
        r.update(cy26=cy26, cy27=cy27, eps_ntm=ntm, pe_ntm=prix / ntm, pe_27=prix / cy27)
        g27 = (cy27 / cy26 - 1) * 100 if cy26 and cy26 > 0 else None
        r["g27"] = g27
        r["g27_norm"] = fnum(h["g_base"]) if h["ntm_ajuste"] == "cy27" else g27
        r["cyclique"] = h["cyclique"] == "1"
        if r["cyclique"]:
            r["g_lt_base"] = (fnum(h["ratio_bpa_base"]) ** (1 / HORIZON) - 1) * 100
        else:
            r["g_lt_base"] = fnum(h["g_base"])
        ok = g27 is not None and g27 > 0 and not r["cyclique"] and h["ntm_ajuste"] != "cy27"
        r["peg27"] = r["pe_27"] / min(g27, M.G27_CAP) if ok else None
        r["peg_lt"] = r["pe_ntm"] / r["g_lt_base"] if not r["cyclique"] and r["g_lt_base"] > 0 else None
        r["scen"] = M.rendements(r, h)
        r["prix_peg1"] = None if r["cyclique"] else r["g_lt_base"] * ntm
        r["hyp"] = h
        rows[t] = r
    return rows


def poids_nasdaq(rows):
    qqq = load("qqq_holdings.csv", os.path.join(MODELE_DIR, "data"))
    poids = {}
    for q in qqq:
        t = "GOOGL" if q["ticker"] == "GOOG" else q["ticker"]
        if t in rows:
            poids[t] = poids.get(t, 0.0) + float(q["poids_pct"])
    return poids


# --------------------------------------------------------------------------
# Format français
# --------------------------------------------------------------------------
NBSP = " "  # espace fine insécable


def fr(x, d=1, signe=False):
    if x is None:
        return "n.d."
    s = f"{abs(x):,.{d}f}".replace(",", " ").replace(".", ",").replace(" ", NBSP)
    if x < 0 and float(s.replace(",", ".").replace(NBSP, "")) != 0:
        return "−" + s
    return ("+" + s) if signe else s


def pct(x, d=1, signe=False):
    return None if x is None else fr(x * 100, d, signe) + NBSP + "%"


def main():
    rows = construire_lignes()
    ptf = {r["ticker"]: float(r["poids"]) for r in load("portefeuille.csv")}
    meta_ptf = {r["ticker"]: r for r in load("portefeuille.csv")}
    ndx_poids = poids_nasdaq(rows)
    couverture = sum(ndx_poids.values())

    agg_ptf = M.agregats(ptf, rows)
    agg_ndx = M.agregats(ndx_poids, rows)
    agg_ndx_hm = M.agregats({t: p for t, p in ndx_poids.items() if t not in ("MU", "SNDK")}, rows)
    p_sous, p_perte = M.probas_sous(ptf, rows, agg_ndx["tcam_base"])
    part_usd = sum(p for t, p in ptf.items() if t != "ADYEY") / sum(ptf.values())

    # ---------------- stress tests (mêmes chocs pour le portefeuille et l'indice) ----------------
    def scen(choix):
        return lambda t: rows[t]["scen"][choix(t)]

    def ia(t):
        return rows[t]["theme"] in M.THEMES_IA

    tests = [
        ("Krach du capex IA (valeurs IA en bear, le reste en base)", scen(lambda t: "bear" if ia(t) else "base")),
        ("Choc géopolitique sur Taïwan (TSM en bear)", scen(lambda t: "bear" if t == "TSM" else "base")),
        ("NVIDIA perd du terrain face au sur-mesure (NVDA en bear)", scen(lambda t: "bear" if t == "NVDA" else "base")),
        ("Choc de crédit ou politique au Brésil (NU en bear)", scen(lambda t: "bear" if t == "NU" else "base")),
        ("Reddit perd le trafic de recherche (RDDT en bear)", scen(lambda t: "bear" if t == "RDDT" else "base")),
        ("Stripe comprime les commissions d'Adyen (ADYEY en bear)", scen(lambda t: "bear" if t == "ADYEY" else "base")),
        ("Double choc fintech : NU et ADYEY en bear", scen(lambda t: "bear" if t in ("NU", "ADYEY") else "base")),
        ("Tout en base", scen(lambda t: "base")),
        ("Tout en bear", scen(lambda t: "bear")),
        ("Tout en bull", scen(lambda t: "bull")),
    ]
    stress = [(nom, M.terminal(ptf, f), M.terminal(ndx_poids, f)) for nom, f in tests]

    # ---------------- rétroviseur : performances passées, poids égaux sans rééquilibrage ----------------
    idx = {r["ticker"]: r for r in load("indices_2026-10-13.csv")}
    retro = {}
    for cle, col_v, col_i in (("1an", "chg_52s", "perf_1an_pct"), ("ytd", "chg_ytd", "perf_ytd_pct")):
        p = sum(ptf[t] * fnum(rows[t][col_v]) for t in ptf) / sum(ptf.values())
        retro[cle] = {"portefeuille": p, "QQQ": fnum(idx["QQQ"][col_i]), "SPY": fnum(idx["SPY"][col_i]),
                      "valeurs": {t: fnum(rows[t][col_v]) for t in ptf}}

    # ---------------- CSV de sortie ----------------
    def ecrire(nom, champs, lignes):
        with open(os.path.join(HERE, nom), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(champs)
            w.writerows(lignes)

    ecrire("valeurs.csv",
           ["ticker", "nom", "theme", "poids", "prix", "bpa_2026", "bpa_2027", "bpa_ntm", "pe_ntm", "pe_2027",
            "croiss_bpa_2027_pct", "peg_2027", "croiss_retenue_pct", "peg_lt", "prix_peg1", "ecart_zone_pct",
            "tcam_bear", "tcam_base", "tcam_bull", "tcam_esperance", "chg_52s_pct", "chg_ytd_pct", "zacks_rank"],
           [[t, rows[t]["nom"], rows[t]["theme"], ptf[t], rows[t]["prix"], round(rows[t]["cy26"], 4),
             round(rows[t]["cy27"], 4), round(rows[t]["eps_ntm"], 4), round(rows[t]["pe_ntm"], 3),
             round(rows[t]["pe_27"], 3), round(rows[t]["g27"], 2), round(rows[t]["peg27"], 3),
             rows[t]["g_lt_base"], round(rows[t]["peg_lt"], 3), round(rows[t]["prix_peg1"], 2),
             round((fnum(rows[t]["prix"]) / rows[t]["prix_peg1"] - 1) * 100, 1)]
            + [round(rows[t]["scen"][k], 6) for k in ("tcam_bear", "tcam_base", "tcam_bull", "tcam_esperance")]
            + [rows[t]["chg_52s"], rows[t]["chg_ytd"], rows[t]["zacks_rank"]] for t in TICKERS])

    cles = ("pe_ntm", "g27", "peg27", "g_lt", "peg_lt", "beta", "div", "part_ia",
            "tcam_bear", "tcam_base", "tcam_bull", "tcam_esperance")
    lignes = [[k, round(agg_ptf[k], 6), round(agg_ndx[k], 6), round(agg_ndx_hm[k], 6)] for k in cles]
    lignes.append(["valeur_100_esperance", round(100 * (1 + agg_ptf["esperance"]), 1),
                   round(100 * (1 + agg_ndx["esperance"]), 1), round(100 * (1 + agg_ndx_hm["esperance"]), 1)])
    lignes.append(["p_sous_indice_central", round(p_sous, 6), "", ""])
    lignes.append(["p_perte", round(p_perte, 6), "", ""])
    lignes.append(["couverture_ndx_pct", "", round(couverture, 2), ""])
    ecrire("comparaison.csv", ["indicateur", "portefeuille", "nasdaq100_reconstitue", "nasdaq100_hors_memoire"],
           lignes)
    ecrire("stress_tests.csv", ["scenario", "tcam_portefeuille", "tcam_nasdaq100", "ecart_pts"],
           [[n, round(a, 6), round(b, 6), round((a - b) * 100, 2)] for n, a, b in stress])
    ecrire("retroviseur.csv", ["periode", "portefeuille_poids_egaux", "QQQ", "SPY"] + list(TICKERS),
           [[k, round(v["portefeuille"], 2), v["QQQ"], v["SPY"]] + [v["valeurs"][t] for t in TICKERS]
            for k, v in retro.items()])

    # ---------------- données de la vidéo ----------------
    cit = {c["id"]: c for c in load("citations.csv")}
    meg = load("megatendances.csv")
    couleurs = {"NVDA": "#76d672", "TSM": "#ff6b5b", "NU": "#b07cff", "RDDT": "#ff8a3d", "ADYEY": "#3ddc97"}
    noms_courts = {"NVDA": "NVIDIA", "TSM": "TSMC", "NU": "Nu", "RDDT": "Reddit", "ADYEY": "Adyen"}
    symboles = {"NVDA": "NVDA", "TSM": "TSM", "NU": "NU", "RDDT": "RDDT", "ADYEY": "ADYEN"}
    cit_valeur = {"NVDA": "huang", "TSM": "wei", "NU": "velez", "RDDT": "huffman", "ADYEY": "adyen"}
    accroches = {
        "NVDA": "Le moteur de l'IA",
        "TSM": "Le péage de toutes les puces",
        "NU": "La banque sans agences",
        "RDDT": "La mémoire humaine du web",
        "ADYEY": "La tuyauterie des paiements",
    }
    valeurs = []
    for t in TICKERS:
        r = rows[t]
        c = cit[cit_valeur[t]]
        valeurs.append({
            "ticker": t, "symbole": symboles[t], "nom": noms_courts[t], "theme": accroches[t],
            "couleur": couleurs[t], "poids": pct(ptf[t], 0),
            "prix": fr(fnum(r["prix"]), 2) + NBSP + "$",
            "bpa26": fr(r["cy26"], 2), "bpa27": fr(r["cy27"], 2),
            "bpa26_v": r["cy26"], "bpa27_v": r["cy27"],
            "g27": fr(r["g27"], 0, True) + NBSP + "%", "g27_v": r["g27"],
            "pe": fr(r["pe_ntm"], 1), "pe_v": r["pe_ntm"],
            "peg27": fr(r["peg27"], 2), "peg_lt": fr(r["peg_lt"], 2), "peg_lt_v": r["peg_lt"],
            "g_lt": fr(r["g_lt_base"], 0) + NBSP + "%", "g_lt_v": r["g_lt_base"],
            "esperance": pct(r["scen"]["tcam_esperance"], 1), "esperance_v": r["scen"]["tcam_esperance"],
            "bear": pct(r["scen"]["tcam_bear"], 1, True), "bull": pct(r["scen"]["tcam_bull"], 1, True),
            "chg_52s": fr(fnum(r["chg_52s"]), 1, True) + NBSP + "%", "chg_52s_v": fnum(r["chg_52s"]),
            "zacks_rank": r["zacks_rank"],
            "zone": fr(r["prix_peg1"], 2) + NBSP + "$",
            "ecart_zone": fr((fnum(r["prix"]) / r["prix_peg1"] - 1) * 100, 0, True) + NBSP + "%",
            "pea": meta_ptf[t]["pea"], "cotation": meta_ptf[t]["cotation_a_acheter"],
            "citation": {"texte": c["texte_original"], "traduction": c["traduction"], "auteur": c["auteur"],
                         "fonction": c["fonction"], "date": c["date"], "occasion": c["occasion"]},
        })

    def agg_fmt(a):
        return {
            "pe": fr(a["pe_ntm"], 1), "pe_v": a["pe_ntm"],
            "g27": fr(a["g27"], 0, True) + NBSP + "%", "g27_v": a["g27"],
            "peg27": fr(a["peg27"], 2), "peg27_v": a["peg27"],
            "g_lt": fr(a["g_lt"], 1) + NBSP + "%", "g_lt_v": a["g_lt"],
            "peg_lt": fr(a["peg_lt"], 2), "peg_lt_v": a["peg_lt"],
            "beta": fr(a["beta"], 2), "part_ia": pct(a["part_ia"], 0),
            "bear": pct(a["tcam_bear"], 1, True), "bear_v": a["tcam_bear"],
            "base": pct(a["tcam_base"], 1, True), "base_v": a["tcam_base"],
            "bull": pct(a["tcam_bull"], 1, True), "bull_v": a["tcam_bull"],
            "esperance": pct(a["tcam_esperance"], 1, True), "esperance_v": a["tcam_esperance"],
            "cent": fr(100 * (1 + a["esperance"]), 0), "cent_v": 100 * (1 + a["esperance"]),
        }

    def mega_chiffre(m):
        v = float(m["chiffre"])
        return fr(v, 0 if v == int(v) else 1) + NBSP + m["unite"], v

    donnees = {
        "date_analyse": DATE_ANALYSE.strftime("%d/%m/%Y"), "date_cours": DATE_COURS,
        "horizon": HORIZON, "valeurs": valeurs,
        "portefeuille": agg_fmt(agg_ptf), "nasdaq": agg_fmt(agg_ndx), "nasdaq_hm": agg_fmt(agg_ndx_hm),
        "ndx_lignes": len(ndx_poids), "ndx_couverture": fr(couverture, 1) + NBSP + "%",
        "p_sous_indice": pct(p_sous, 0), "p_perte": pct(p_perte, 1),
        "stress": [{"nom": n, "ptf": pct(a, 1, True), "ptf_v": a, "ndx": pct(b, 1, True), "ndx_v": b}
                   for n, a, b in stress],
        "retro": {k: {"ptf": fr(v["portefeuille"], 1, True) + NBSP + "%", "ptf_v": v["portefeuille"],
                      "qqq": fr(v["QQQ"], 1, True) + NBSP + "%", "qqq_v": v["QQQ"],
                      "spy": fr(v["SPY"], 1, True) + NBSP + "%", "spy_v": v["SPY"]} for k, v in retro.items()},
        "megatendances": [dict(m, chiffre_txt=mega_chiffre(m)[0], chiffre_v=mega_chiffre(m)[1],
                               valeurs=[noms_courts[x] for x in m["valeurs"].split(";")]) for m in meg],
        "citations": {k: {kk: c[kk] for kk in ("auteur", "fonction", "texte_original", "traduction", "date",
                                                "occasion")} for k, c in cit.items()},
        "part_ia_ptf": pct(agg_ptf["part_ia"], 0),
        # Lignes cotées en dollars (Adyen s'achète en euros à Amsterdam) : effet d'une baisse de 10 %
        # du dollar sur la valeur du portefeuille en euros, à cours inchangés en dollars.
        "part_usd": pct(part_usd, 0), "effet_dollar_10": pct(-0.10 * part_usd, 0),
    }
    os.makedirs(os.path.join(HERE, "video"), exist_ok=True)
    with open(os.path.join(HERE, "video", "donnees_video.json"), "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=1)

    # ---------------- résumé ----------------
    print(f"Date {DATE_ANALYSE} : BPA NTM = {W_N:.3f} x BPA 2026 + {W_N1:.3f} x BPA 2027 ; horizon {HORIZON} ans")
    print(f"Nasdaq 100 reconstitué : {len(ndx_poids)} valeurs, {couverture:.2f} % du QQQ")
    print("\nValeur  P/E NTM  BPA26   BPA27   g27     PEG27  g LT  PEG LT  zone PEG1  espéré  bear    bull")
    for t in TICKERS:
        r = rows[t]
        print(f"{t:<6} {r['pe_ntm']:7.1f} {r['cy26']:7.3f} {r['cy27']:7.3f} {r['g27']:6.1f}% {r['peg27']:6.2f}"
              f" {r['g_lt_base']:4.0f} {r['peg_lt']:6.2f} {r['prix_peg1']:9.2f}  {r['scen']['tcam_esperance']:6.1%}"
              f" {r['scen']['tcam_bear']:6.1%} {r['scen']['tcam_bull']:6.1%}")
    print("\nIndicateur        Portefeuille  Nasdaq 100  NDX hors mémoire")
    for k in cles:
        print(f"{k:<16} {agg_ptf[k]:12.4f} {agg_ndx[k]:11.4f} {agg_ndx_hm[k]:11.4f}")
    print(f"P(sous l'indice central) = {p_sous:.1%} ; P(perte) = {p_perte:.1%}")
    print("\nStress tests (TCAM 4 ans)")
    for n, a, b in stress:
        print(f"  {n:<58} ptf {a:7.1%}  ndx {b:7.1%}")
    print("\nRétroviseur (poids égaux, sans rééquilibrage)")
    for k, v in retro.items():
        print(f"  {k}: ptf {v['portefeuille']:+.1f} %  QQQ {v['QQQ']:+.1f} %  SPY {v['SPY']:+.1f} %")
    for t in TICKERS:
        for a in rows[t]["alertes"]:
            print("  alerte", t, a)


if __name__ == "__main__":
    main()
