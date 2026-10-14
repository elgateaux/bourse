#!/usr/bin/env python3
"""Calculs de la formation « Le stock picking GARP » du 13/10/2026 (bibliothèque standard seulement).

`python3 calcul.py` lit les CSV de data/ et les sorties datées de l'analyse vidéo du même jour
(../2026-10-13_video-portefeuille_hyperframes : valeurs.csv, comparaison.csv, retroviseur.csv,
stress_tests.csv et data/zacks_2026-10-13.csv), puis écrit :

- ratios.csv : marges, croissance, FCF, capex, trésorerie nette, ROE, ROIC, dilution ;
- valorisation.csv : capitalisation, valeur d'entreprise, P/E, PEG, P/S, VE/EBIT, rendement FCF ;
- grille_garp.csv : la grille en 7 critères appliquée aux 5 valeurs ;
- interets_composes.csv, frais.csv, enveloppes.csv : intérêts composés, frais et fiscalité ;
- calculatrice_tests.csv : cas de contrôle de la calculatrice (le JavaScript doit retrouver ces valeurs) ;
- diaporama/donnees_formation.json : tout ce qu'affiche le diaporama.

La simulation `simuler()` est la référence : le JavaScript de la calculatrice en est la traduction ligne à ligne.
"""
import csv
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
VIDEO = os.path.join(HERE, "..", "2026-10-13_video-portefeuille_hyperframes")
NBSP = " "
CINQ = ["NVDA", "TSM", "NU", "RDDT", "ADYEY"]
COMPTES = ["NVDA", "TSM", "NU", "RDDT"]


def load(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(x):
    if x is None or str(x).strip() == "":
        return None
    return float(x)


def fr(x, d=1, signe=False):
    if x is None:
        return "n.d."
    s = f"{abs(x):,.{d}f}".replace(",", " ").replace(".", ",").replace(" ", NBSP)
    if x < 0 and float(s.replace(",", ".").replace(NBSP, "")) != 0:
        return "−" + s
    return ("+" + s) if signe else s


def pct(x, d=1, signe=False):
    return "n.d." if x is None else fr(x * 100, d, signe) + NBSP + "%"


def eur(x, d=0):
    return fr(x, d) + NBSP + "€"


def ecrire(nom, lignes):
    champs = []
    for l in lignes:
        champs += [k for k in l if k not in champs]
    with open(os.path.join(HERE, nom), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs, lineterminator="\n")
        w.writeheader()
        for l in lignes:
            w.writerow({k: (round(v, 6) if isinstance(v, float) else v) for k, v in l.items()})


# ---------------------------------------------------------------- paramètres
FISC = {r["id"]: r for r in load(os.path.join(DATA, "fiscalite.csv"))}
HYP = {r["id"]: num(r["valeur"]) for r in load(os.path.join(DATA, "hypotheses.csv"))}


def fv(i):
    return float(FISC[i]["valeur"])


PARAMS = {
    "pfu": fv("pfu_total") / 100, "ps": fv("ps_2026") / 100, "ps_av": fv("ps_av") / 100, "ir_pfu": fv("pfu_ir") / 100,
    "av_taux_reduit": fv("av_taux_reduit") / 100, "av_seuil": fv("av_seuil_primes"),
    "av_abat_seul": fv("av_abattement_seul"), "av_abat_couple": fv("av_abattement_couple"),
    "pea_duree": fv("pea_duree"), "av_duree": fv("av_duree"), "pea_plafond": fv("pea_plafond"),
}


# ---------------------------------------------------------------- simulation (référence de la calculatrice)
def impot_sortie(env, annees, gains, verse, couple, P=PARAMS):
    """Impôt et prélèvements sociaux dus sur les gains lors d'un retrait total en fin de période."""
    if gains <= 0:
        return 0.0
    if env == "PEA":
        return gains * (P["ps"] if annees >= P["pea_duree"] else P["pfu"])
    if env == "CTO":
        return gains * P["pfu"]
    # assurance-vie, unités de compte, un seul assuré
    if annees < P["av_duree"]:
        return gains * (P["ir_pfu"] + P["ps_av"])
    abat = P["av_abat_couple"] if couple else P["av_abat_seul"]
    part_haute = max(0.0, verse - P["av_seuil"]) / verse if verse > 0 else 0.0
    taux_ir = P["av_taux_reduit"] * (1 - part_haute) + P["ir_pfu"] * part_haute
    return gains * P["ps_av"] + max(0.0, gains - abat) * taux_ir


def simuler(capital, mensuel, annees, rendement, frais, env="PEA", couple=False, inflation=0.0):
    """Capitalisation mensuelle : rendement brut, frais prélevés sur l'encours, versement en fin de mois."""
    g = (1 + rendement) ** (1 / 12)
    k = (1 - frais) ** (1 / 12)
    v, v0, verse = capital, capital, capital
    serie = [{"annee": 0, "verse": verse, "valeur": v, "sans_frais": v0}]
    for mois in range(1, int(round(annees * 12)) + 1):
        v = v * g * k + mensuel
        v0 = v0 * g + mensuel
        verse += mensuel
        if mois % 12 == 0:
            serie.append({"annee": mois // 12, "verse": verse, "valeur": v, "sans_frais": v0})
    gains = v - verse
    impot = impot_sortie(env, annees, gains, verse, couple)
    net = v - impot
    return {"verse": verse, "valeur": v, "sans_frais": v0, "cout_frais": v0 - v, "gains": gains, "impot": impot,
            "net": net, "reel": net / (1 + inflation) ** annees, "serie": serie}


# ---------------------------------------------------------------- comptes et ratios
def tcam(debut, fin, annees):
    return (fin / debut) ** (1 / annees) - 1 if debut and debut > 0 and fin > 0 and annees > 0 else None


def ratios():
    out = {}
    for r in load(os.path.join(DATA, "comptes_annuels.csv")):
        t = r["ticker"]
        g = {k: num(v) for k, v in r.items() if k not in ("ticker", "societe", "exercice", "fin_exercice", "devise", "annee_il_y_a_4_ans", "source")}
        an_fin = int(r["fin_exercice"][:4])
        an_debut = int(r["annee_il_y_a_4_ans"].replace("FY", ""))
        if r["exercice"].startswith("FY"):  # NVIDIA : l'exercice FY2026 se termine en janvier 2026
            an_fin = int(r["exercice"][2:])
        n = an_fin - an_debut
        ca = g["chiffre_affaires"]
        taux_is = g["impot"] / g["resultat_avant_impot"] if g["resultat_avant_impot"] else None
        fcf = g["flux_operationnel"] - g["capex"]
        ci = g["capitaux_propres"] + g["dette_financiere"] - g["tresorerie"]
        ci_n1 = g["capitaux_propres_n1"] + g["dette_financiere_n1"] - g["tresorerie_n1"]
        ci_moy = (ci + ci_n1) / 2
        nopat = g["resultat_operationnel"] * (1 - max(0.0, taux_is or 0.0))
        banque = t == "NU"
        roic = None if banque else nopat / ci_moy
        out[t] = {
            "ticker": t, "societe": r["societe"], "exercice": r["exercice"],
            "chiffre_affaires": ca, "marge_brute": g["marge_brute"] / ca, "marge_operationnelle": g["resultat_operationnel"] / ca,
            "marge_nette": g["resultat_net"] / ca, "taux_impot": taux_is,
            "tcam_ca": tcam(g["ca_il_y_a_4_ans"], ca, n), "annees_tcam": n, "annee_depart": an_debut,
            "ca_depart": g["ca_il_y_a_4_ans"], "rn_depart": g["resultat_net_il_y_a_4_ans"],
            "resultat_operationnel": g["resultat_operationnel"], "resultat_avant_impot": g["resultat_avant_impot"],
            "impot": g["impot"], "resultat_net": g["resultat_net"], "marge_brute_m": g["marge_brute"],
            "bpa_gaap": g["bpa_dilue_gaap"], "bpa_non_gaap": g["bpa_non_gaap_zacks"],
            "ecart_non_gaap": g["bpa_non_gaap_zacks"] / g["bpa_dilue_gaap"] - 1,
            "bpa_recalcule": g["resultat_net"] / g["actions_moyennes_m"],
            "actions_moyennes": g["actions_moyennes_m"],
            "dilution": g["actions_fin_m"] / g["actions_fin_n1_m"] - 1,
            "flux_operationnel": g["flux_operationnel"], "capex": g["capex"], "fcf": fcf,
            "capex_ca": g["capex"] / ca, "marge_fcf": fcf / ca, "conversion_fcf": fcf / g["resultat_net"],
            "rachats": g["rachats_actions"], "dividendes": g["dividendes_verses"],
            "retour_actionnaire_fcf": (g["rachats_actions"] + g["dividendes_verses"]) / fcf,
            "tresorerie": g["tresorerie"], "dette": g["dette_financiere"],
            "tresorerie_nette": None if banque else g["tresorerie"] - g["dette_financiere"],
            "capitaux_propres": g["capitaux_propres"],
            "roe": g["resultat_net"] / ((g["capitaux_propres"] + g["capitaux_propres_n1"]) / 2),
            "nopat": nopat, "capital_investi": ci, "capital_investi_n1": ci_n1, "capital_investi_moyen": ci_moy,
            "roic": roic,
            # ROIC non significatif quand le capital investi est minuscule face au résultat (trésorerie abondante)
            "roic_significatif": (not banque) and ci_moy > 0.25 * g["capitaux_propres"],
        }
    return out


# ---------------------------------------------------------------- valorisation
def valorisation(R):
    Z = {}
    for r in load(os.path.join(VIDEO, "data", "zacks_2026-10-13.csv")):
        Z.setdefault(r["ticker"], r)
    V = {r["ticker"]: r for r in load(os.path.join(VIDEO, "valeurs.csv"))}
    out = {}
    for t in CINQ + ["MU", "INTC", "AAPL", "GOOGL"]:
        z = Z[t]
        prix, cap = float(z["prix"]), float(z["cap_musd"])
        e0, e1, e2 = num(z["eps_fy0"]), num(z["eps_f1"]), num(z["eps_f2"])
        o = {"ticker": t, "nom": z["nom"], "prix": prix, "capitalisation": cap, "zacks_rank": int(z["zacks_rank"]),
             "bpa_fy0": e0, "bpa_f1": e1, "bpa_f2": e2, "pe_dernier_exercice": prix / e0 if e0 and e0 > 0 else None,
             "pe_f1": prix / e1 if e1 and e1 > 0 else None, "pe_f2": prix / e2 if e2 and e2 > 0 else None,
             "croissance_f1": e1 / e0 - 1 if e0 and e0 > 0 else None, "croissance_f2": e2 / e1 - 1 if e1 and e1 > 0 else None,
             "ltg": num(z["ltg"]), "beta": num(z["beta"]), "dividende": num(z["div_yield"]),
             "plus_haut_52s": float(z["high_52w"]), "plus_bas_52s": float(z["low_52w"]),
             "ecart_plus_haut": prix / float(z["high_52w"]) - 1, "amplitude_52s": float(z["high_52w"]) / float(z["low_52w"]) - 1,
             "chg_52s": num(z["chg_52s"]) / 100, "chg_ytd": num(z["chg_ytd"]) / 100}
        if t in V:
            v = V[t]
            o.update({"pe_ntm": float(v["pe_ntm"]), "bpa_ntm": float(v["bpa_ntm"]), "croissance_retenue": float(v["croiss_retenue_pct"]) / 100,
                      "peg_lt": float(v["peg_lt"]), "peg_2027": float(v["peg_2027"]), "croissance_2027": float(v["croiss_bpa_2027_pct"]) / 100,
                      "prix_peg1": float(v["prix_peg1"]), "ecart_zone": float(v["ecart_zone_pct"]) / 100,
                      "tcam_bear": float(v["tcam_bear"]), "tcam_base": float(v["tcam_base"]), "tcam_bull": float(v["tcam_bull"]),
                      "tcam_esperance": float(v["tcam_esperance"]), "theme": v["theme"]})
            o["prix_peg08"] = o["prix_peg1"] * HYP["zone_peg_forte"]
        if t in R:
            c = R[t]
            o["p_s"] = cap / c["chiffre_affaires"]
            if c["tresorerie_nette"] is not None:
                o["valeur_entreprise"] = cap - c["tresorerie_nette"]
                o["ve_ebit"] = o["valeur_entreprise"] / c["resultat_operationnel"]
                o["rendement_fcf"] = c["fcf"] / cap
            else:
                o["p_b"] = cap / c["capitaux_propres"]
        out[t] = o
    return out


# ---------------------------------------------------------------- grille GARP
def grille(R, VAL, ady):
    lignes = []
    for t in CINQ:
        v, c = VAL[t], R.get(t)
        crit = []
        crit.append(("Croissance retenue ≥ " + fr(HYP["garp_croissance_min"], 0) + NBSP + "%", pct(v["croissance_retenue"], 0), v["croissance_retenue"] * 100 >= HYP["garp_croissance_min"]))
        crit.append(("PEG long terme ≤ " + fr(HYP["garp_peg_max"], 1), fr(v["peg_lt"], 2), v["peg_lt"] <= HYP["garp_peg_max"]))
        if c is None:
            crit.append(("ROIC (ROE pour une banque) ≥ " + fr(HYP["garp_rentabilite_min"], 0) + NBSP + "%", "n.d.", None))
        elif c["roic"] is not None and c["roic_significatif"]:
            crit.append(("ROIC (ROE pour une banque) ≥ " + fr(HYP["garp_rentabilite_min"], 0) + NBSP + "%", "ROIC " + pct(c["roic"], 0), c["roic"] * 100 >= HYP["garp_rentabilite_min"]))
        else:
            crit.append(("ROIC (ROE pour une banque) ≥ " + fr(HYP["garp_rentabilite_min"], 0) + NBSP + "%", "ROE " + pct(c["roe"], 0), c["roe"] * 100 >= HYP["garp_rentabilite_min"]))
        mn = c["marge_nette"] if c else ady["marge_nette"]
        crit.append(("Marge nette ≥ " + fr(HYP["garp_marge_nette_min"], 0) + NBSP + "%", pct(mn, 0) + ("" if c else " (S1)"), mn * 100 >= HYP["garp_marge_nette_min"]))
        if c:
            crit.append(("Dilution ≤ " + fr(HYP["garp_dilution_max"], 0) + NBSP + "% par an", pct(c["dilution"], 1, True), c["dilution"] * 100 <= HYP["garp_dilution_max"]))
        else:
            crit.append(("Dilution ≤ " + fr(HYP["garp_dilution_max"], 0) + NBSP + "% par an", "n.d.", None))
        if c and c["tresorerie_nette"] is not None:
            crit.append(("Trésorerie nette ≥ 0", fr(c["tresorerie_nette"] / 1000, 1) + NBSP + "Md$", c["tresorerie_nette"] >= HYP["garp_tresorerie_nette_min"]))
        else:
            crit.append(("Trésorerie nette ≥ 0", "banque" if t == "NU" else "n.d.", None))
        crit.append(("Rang Zacks ≤ " + fr(HYP["garp_rank_max"], 0), str(v["zacks_rank"]), v["zacks_rank"] <= HYP["garp_rank_max"]))
        ok = sum(1 for _, _, p in crit if p is True)
        evalues = sum(1 for _, _, p in crit if p is not None)
        lignes.append({"ticker": t, "criteres": crit, "score": ok, "evalues": evalues})
    return lignes


def main():
    R = ratios()
    VAL = valorisation(R)
    ADY = {r["indicateur"]: float(r["valeur"]) for r in load(os.path.join(DATA, "adyen_s1_2026.csv"))}
    ady = {"ca": ADY["chiffre_affaires_net"], "croissance": ADY["croissance_ca_net"] / 100,
           "marge_ebitda": ADY["ebitda"] / ADY["chiffre_affaires_net"], "marge_nette": ADY["resultat_net"] / ADY["chiffre_affaires_net"],
           "volume_md": ADY["volume_traite"], "take_rate": ADY["chiffre_affaires_net"] / (ADY["volume_traite"] * 1000), "resultat_net": ADY["resultat_net"],
           "ebitda": ADY["ebitda"]}
    NU = {r["indicateur"]: float(r["valeur"]) for r in load(os.path.join(DATA, "nu_t2_2026.csv"))}
    RD = {r["indicateur"]: float(r["valeur"]) for r in load(os.path.join(DATA, "reddit_t2_2026.csv"))}
    NV = {r["indicateur"]: r["valeur"] for r in load(os.path.join(DATA, "nvda_zacks_2026-10-12.csv"))}
    HIST = load(os.path.join(DATA, "historique_bpa.csv"))
    CMP = {r["indicateur"]: r for r in load(os.path.join(VIDEO, "comparaison.csv"))}
    RETRO = {r["periode"]: r for r in load(os.path.join(VIDEO, "retroviseur.csv"))}
    STRESS = load(os.path.join(VIDEO, "stress_tests.csv"))
    CAT = load(os.path.join(DATA, "categories_lynch.csv"))
    INV = load(os.path.join(DATA, "investisseurs.csv"))
    LYN = {r["indicateur"]: r for r in load(os.path.join(DATA, "palmares_lynch.csv"))}
    opt = lambda nom: load(os.path.join(DATA, nom)) if os.path.exists(os.path.join(DATA, nom)) else []
    ETF, ETF_R, HZ = opt("etf.csv"), opt("etf_regles.csv"), opt("horizon_dca.csv")
    ETF_US = load(os.path.join(DATA, "etf_us_zacks_2026-10-13.csv"))
    QQQ = load(os.path.join(DATA, "qqq_positions_2026-09-04.csv"))

    # ---- DCA contre investissement en une fois : deux chemins de prix pédagogiques
    dca = {}
    for r in load(os.path.join(DATA, "dca_exemple.csv")):
        dca.setdefault(r["scenario"], []).append(float(r["prix"]))
    dca_res = {}
    for sc, prix in dca.items():
        n = len(prix)
        tranche = HYP["dca_montant"] / n
        parts_dca = sum(tranche / x for x in prix)
        parts_lump = HYP["dca_montant"] / prix[0]
        dca_res[sc] = {"prix": prix, "tranche": tranche, "parts_dca": parts_dca, "parts_lump": parts_lump,
                       "cout_moyen_dca": HYP["dca_montant"] / parts_dca, "prix_moyen": sum(prix) / n,
                       "valeur_dca": parts_dca * prix[-1], "valeur_lump": parts_lump * prix[-1]}

    # ---- frais courants d'un ETF : écart sur 20 ans au scénario par défaut de la calculatrice
    etf_fr = {}
    for cle in ("etf_frais_bas", "etf_frais_haut"):
        sim = simuler(HYP["calc_capital"], HYP["calc_versement"], HYP["calc_duree"], HYP["calc_rendement"] / 100, HYP[cle] / 100)
        etf_fr[cle] = {"frais": HYP[cle] / 100, "valeur": sim["valeur"], "verse": sim["verse"]}

    # ---- ratios.csv
    ecrire("ratios.csv", [{k: v for k, v in R[t].items()} for t in COMPTES])
    ecrire("valorisation.csv", [VAL[t] for t in VAL])

    # ---- grille
    G = grille(R, VAL, ady)
    ecrire("grille_garp.csv", [dict({"ticker": g["ticker"], "score": g["score"], "evalues": g["evalues"]},
                                    **{f"c{i + 1}_{'ok' if p else ('na' if p is None else 'non')}": val for i, (_, val, p) in enumerate(g["criteres"])})
                               for g in G])

    # ---- exemple cours = BPA × P/E
    ex = {"bpa0": HYP["ex_bpa_depart"], "pe0": HYP["ex_pe_depart"], "bpa1": HYP["ex_bpa_arrivee"], "pe1": HYP["ex_pe_arrivee"], "n": HYP["ex_annees"]}
    ex["cours0"], ex["cours1"] = ex["bpa0"] * ex["pe0"], ex["bpa1"] * ex["pe1"]
    ex["perf"] = ex["cours1"] / ex["cours0"] - 1
    ex["tcam"] = (ex["cours1"] / ex["cours0"]) ** (1 / ex["n"]) - 1
    ex["tcam_bpa"] = (ex["bpa1"] / ex["bpa0"]) ** (1 / ex["n"]) - 1
    ex["tcam_pe"] = (ex["pe1"] / ex["pe0"]) ** (1 / ex["n"]) - 1

    # ---- intérêts composés : 10 000 € à 4/7/10/15 % sur 10/20/30 ans ; règle de 72
    taux = [0.04, 0.07, 0.10, 0.15]
    durees = [10, 20, 30]
    ic = []
    for r_ in taux:
        l = {"taux": r_}
        for n in durees:
            l[f"valeur_{n}ans"] = HYP["calc_capital"] * (1 + r_) ** n
        l["doublement_72"] = 72 / (r_ * 100)
        l["doublement_exact"] = math.log(2) / math.log(1 + r_)
        ic.append(l)
    ecrire("interets_composes.csv", ic)

    # ---- frais : 10 000 € + 300 €/mois, 30 ans, 8 % brut
    fx = []
    base_sans = simuler(HYP["frais_capital"], HYP["frais_versement"], HYP["frais_duree"], HYP["frais_rendement"] / 100, 0.0)
    for cle in ("frais_niveau_bas", "frais_niveau_moyen", "frais_niveau_haut"):
        s = simuler(HYP["frais_capital"], HYP["frais_versement"], HYP["frais_duree"], HYP["frais_rendement"] / 100, HYP[cle] / 100)
        fx.append({"frais": HYP[cle] / 100, "verse": s["verse"], "valeur": s["valeur"], "sans_frais": base_sans["valeur"],
                   "cout": base_sans["valeur"] - s["valeur"], "part_perdue": 1 - s["valeur"] / base_sans["valeur"]})
    ecrire("frais.csv", fx)
    bogle = {"r": HYP["bogle_rendement"] / 100, "f": HYP["bogle_frais"] / 100, "n": HYP["bogle_duree"]}
    bogle["part_perdue"] = 1 - ((1 + bogle["r"]) * (1 - bogle["f"])) ** bogle["n"] / (1 + bogle["r"]) ** bogle["n"]
    # variante « rendement net = brut − frais », la convention de Frontline
    bogle["part_perdue_soustraction"] = 1 - ((1 + bogle["r"] - bogle["f"]) / (1 + bogle["r"])) ** bogle["n"]

    # ---- enveloppes : scénario par défaut de la calculatrice
    dflt = {"capital": HYP["calc_capital"], "mensuel": HYP["calc_versement"], "annees": HYP["calc_duree"],
            "rendement": HYP["calc_rendement"] / 100, "frais": HYP["calc_frais"] / 100, "inflation": HYP["calc_inflation"] / 100}
    env = []
    for e, couple in (("PEA", False), ("AV", False), ("AV", True), ("CTO", False)):
        s = simuler(dflt["capital"], dflt["mensuel"], dflt["annees"], dflt["rendement"], dflt["frais"], e, couple, dflt["inflation"])
        env.append({"enveloppe": e + (" (couple)" if couple else ""), "verse": s["verse"], "valeur": s["valeur"], "gains": s["gains"],
                    "impot": s["impot"], "net": s["net"], "reel": s["reel"], "taux_effectif": s["impot"] / s["gains"]})
    ecrire("enveloppes.csv", env)
    pv = HYP["plus_value_exemple"]
    fisc_pv = {"PEA (après 5 ans)": impot_sortie("PEA", 5, pv, pv, False), "PEA (avant 5 ans)": impot_sortie("PEA", 4, pv, pv, False),
               "Compte-titres": impot_sortie("CTO", 5, pv, pv, False), "Assurance-vie (après 8 ans, seul)": impot_sortie("AV", 8, pv, pv, False),
               "Assurance-vie (après 8 ans, couple)": impot_sortie("AV", 8, pv, pv, True), "Assurance-vie (avant 8 ans)": impot_sortie("AV", 7, pv, pv, False)}

    # ---- le temps plutôt que le timing
    tps = {}
    for cle in ("temps_age_tot", "temps_age_tard"):
        n = HYP["temps_age_fin"] - HYP[cle]
        s = simuler(0, HYP["temps_versement"], n, dflt["rendement"], dflt["frais"])
        tps[cle] = {"age": HYP[cle], "annees": n, "verse": s["verse"], "valeur": s["valeur"], "serie": [p["valeur"] for p in s["serie"]]}

    # ---- calculatrice : cas de contrôle
    cas = [(10000, 300, 20, 0.08, 0.005, "PEA", False, 0.02), (10000, 300, 20, 0.08, 0.005, "CTO", False, 0.02),
           (10000, 300, 20, 0.08, 0.005, "AV", False, 0.02), (10000, 300, 20, 0.08, 0.005, "AV", True, 0.02),
           (50000, 800, 25, 0.10, 0.01, "AV", False, 0.02), (5000, 100, 4, 0.06, 0.002, "PEA", False, 0.02),
           (20000, 0, 6, 0.07, 0.0075, "AV", False, 0.0), (0, 1000, 30, 0.12, 0.0, "PEA", False, 0.025)]
    tests = []
    for c0, m, n, r_, f_, e, cp, i_ in cas:
        s = simuler(c0, m, n, r_, f_, e, cp, i_)
        tests.append({"capital": c0, "mensuel": m, "annees": n, "rendement": r_, "frais": f_, "enveloppe": e, "couple": int(cp), "inflation": i_,
                      "verse": s["verse"], "valeur": s["valeur"], "cout_frais": s["cout_frais"], "impot": s["impot"], "net": s["net"], "reel": s["reel"]})
    ecrire("calculatrice_tests.csv", tests)

    # ---- historique cyclique / redressement
    hist = {}
    for h in HIST:
        hist.setdefault(h["ticker"], []).append({"exercice": h["exercice"], "ca": num(h["chiffre_affaires"]), "mb": num(h["marge_brute"]),
                                                 "rn": num(h["resultat_net"]), "bpa": num(h["bpa_dilue_gaap"]), "bpa_ng": num(h["bpa_non_gaap"]),
                                                 "nature": h["nature"],
                                                 "taux_mb": (num(h["marge_brute"]) / num(h["chiffre_affaires"])) if num(h["chiffre_affaires"]) else None})

    # ---- catégories de Lynch : indicateurs calculés
    def indicateur(t, cle):
        if cle == "croissance_f2":
            return ("croissance du BPA attendue N+2", pct(VAL[t]["croissance_f2"], 1, True))
        if cle == "croissance_f1":
            return ("croissance du BPA attendue N+1", pct(VAL[t]["croissance_f1"], 0, True))
        if cle == "tcam_ca":
            return (f"croissance annuelle du CA {R[t]['annee_depart']}-{R[t]['exercice']}", pct(R[t]["tcam_ca"], 1))
        if cle == "croissance_ca_s1":
            return ("croissance du CA net, S1 2026", pct(ady["croissance"], 0, True))
        if cle == "resultat_net":
            return (f"résultat net {R[t]['exercice']}", fr(R[t]["resultat_net"], 0) + NBSP + "M$")
        if cle == "bpa_creux_pic":
            h = hist[t]
            creux = min(h, key=lambda x: x["bpa"] if x["bpa"] is not None else 1e9)
            pic = [x for x in h if x["nature"] == "publié"][-1]
            return (f"BPA {creux['exercice']} → {pic['exercice']}", fr(creux["bpa"], 2) + " → " + fr(pic["bpa"], 2) + NBSP + "$")
        if cle == "bpa_2024_vs_f1":
            h = {x["exercice"]: x for x in hist[t]}
            return ("BPA 2024 → consensus 2026", fr(h["2024"]["bpa"], 2) + " → " + fr(h["2026"]["bpa_ng"], 2) + NBSP + "$")
        raise KeyError(cle)

    cats = []
    for c in CAT:
        lab, val = indicateur(c["ticker"], c["indicateur"])
        cats.append({"ticker": c["ticker"], "nom": c["nom"], "categorie": c["categorie"], "indicateur": lab, "valeur": val, "justification": c["justification"]})

    # ---- NVIDIA : cinq P/E pour un seul cours
    nv = VAL["NVDA"]
    pe5 = [("Dernier exercice publié (FY2026)", nv["bpa_fy0"], nv["prix"] / nv["bpa_fy0"]),
           ("12 derniers mois", float(NV["bpa_12_derniers_mois"]), nv["prix"] / float(NV["bpa_12_derniers_mois"])),
           ("Exercice en cours (FY2027)", nv["bpa_f1"], nv["pe_f1"]),
           ("12 prochains mois (NTM)", nv["bpa_ntm"], nv["pe_ntm"]),
           ("Exercice suivant (FY2028)", nv["bpa_f2"], nv["pe_f2"])]

    D = {
        "date": "13/10/2026", "date_cours": "12/10/2026", "params": PARAMS, "defauts": dflt,
        "hyp": HYP, "fisc": {k: {"valeur": v["valeur"], "unite": v["unite"], "precision": v["precision"], "parametre": v["parametre"],
                                 "s1": [v["source_titre"], v["source_url"]], "s2": [v["source2_titre"], v["source2_url"]]} for k, v in FISC.items()},
        "ratios": R, "val": VAL, "adyen": ady, "nu": NU, "reddit": RD, "nvda_zacks": NV, "hist": hist,
        "grille": G, "exemple_pe": ex, "interets": ic, "frais": fx, "bogle": bogle, "enveloppes": env, "fisc_pv": fisc_pv,
        "temps": tps, "categories": cats, "pe5": pe5,
        "comparaison": {k: {"ptf": num(v["portefeuille"]), "ndx": num(v["nasdaq100_reconstitue"]), "ndx_hm": num(v["nasdaq100_hors_memoire"])} for k, v in CMP.items()},
        "retro": RETRO, "stress": STRESS, "investisseurs": INV, "lynch": LYN,
        "etf": ETF, "etf_regles": {r["id"]: r for r in ETF_R}, "horizon": {r["id"]: r for r in HZ}, "etf_us": {r["ticker"]: r for r in ETF_US},
        "qqq": QQQ, "dca": dca_res, "etf_frais": etf_fr,
        "sources_societes": {"adyen": load(os.path.join(DATA, "adyen_s1_2026.csv")), "nu": load(os.path.join(DATA, "nu_t2_2026.csv")),
                             "reddit": load(os.path.join(DATA, "reddit_t2_2026.csv"))},
        "calc_serie_defaut": simuler(dflt["capital"], dflt["mensuel"], dflt["annees"], dflt["rendement"], dflt["frais"], "PEA", False, dflt["inflation"]),
    }
    os.makedirs(os.path.join(HERE, "diaporama"), exist_ok=True)
    with open(os.path.join(HERE, "diaporama", "donnees_formation.json"), "w", encoding="utf-8") as f:
        json.dump(D, f, ensure_ascii=False, indent=1)

    # ---- résumé console
    for t in COMPTES:
        r = R[t]
        print(f"{t:5} marge op {pct(r['marge_operationnelle'])} | TCAM CA {pct(r['tcam_ca'])} ({r['annees_tcam']} ans) | FCF {fr(r['fcf'], 0)} | "
              f"capex/CA {pct(r['capex_ca'])} | ROE {pct(r['roe'])} | ROIC {pct(r['roic']) if r['roic'] is not None else 'n.a.'}"
              f"{'' if r['roic_significatif'] else ' (non significatif)'} | dilution {pct(r['dilution'], 1, True)}")
    for g in G:
        print(g["ticker"], f"{g['score']}/{g['evalues']}", " ; ".join(f"{v}{'✓' if p else ('–' if p is None else '✗')}" for _, v, p in g["criteres"]))
    for e in env:
        print(f"{e['enveloppe']:13} net {eur(e['net'])} impôt {eur(e['impot'])} ({pct(e['taux_effectif'])})")
    print("frais :", " | ".join(f"{pct(x['frais'])} → {eur(x['valeur'])} (−{pct(x['part_perdue'])})" for x in fx))
    print("Bogle 7 %/2 %/50 ans : part perdue", pct(bogle["part_perdue"]), "| convention soustraction", pct(bogle["part_perdue_soustraction"]))
    print("P/E NVIDIA :", " | ".join(f"{l} {fr(p, 1)}" for l, _, p in pe5))
    print("Temps :", {k: eur(v["valeur"]) for k, v in tps.items()})
    print("Adyen take rate", pct(ady["take_rate"], 3), "marge nette", pct(ady["marge_nette"]))


if __name__ == "__main__":
    main()
