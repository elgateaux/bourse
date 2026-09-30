#!/usr/bin/env python3
"""Screen de qualité des bénéfices — tech mondiale (arrêté au 30/09/2026).

Étape 1 (qualité) : à partir des fondamentaux Zacks (data/zacks_snapshot.csv),
reconstitue les flux trimestriels (les cash-flows Zacks sont en cumul annuel),
calcule sur 12 mois glissants (TTM) :
  - ratio d'accruals de Sloan  = (RN - CFO) / actif total moyen
  - conversion cash            = CFO / RN
  - dépendance au non-opérationnel = RN / résultat opérationnel
  - dynamique des marges (brute, opérationnelle) vs TTM précédent
et en déduit un score de qualité des bénéfices (EQS, 0-100, rangs centiles).

Étape 2 (opportunité) : si data/zacks_profile.csv existe (valorisation, révisions,
Zacks Rank), combine EQS + valorisation + momentum des estimations.

Étape 3 (cash-flow libre) : si data/zacks_cashflow.csv existe (CFO et capex), écarte les
finalistes dont le FCF ne couvre pas le bénéfice, puis calcule le score final et teste
sa sensibilité aux pondérations (sensibilite.csv).

Usage : python3 screen.py   (aucune dépendance hors bibliothèque standard)
"""
from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"
STALE_BEFORE = date(2025, 12, 31)  # dernier exercice/trimestre antérieur => données périmées

# Mois de clôture quand aucun enregistrement annuel n'est présent dans la fenêtre.
FYE_OVERRIDE = {"TSM": 12}

UNIVERSE = {
    # ticker: (nom, pays, segment)
    "AAPL": ("Apple", "US", "Hardware"),
    "MSFT": ("Microsoft", "US", "Logiciel / cloud"),
    "NVDA": ("Nvidia", "US", "Semi-conducteurs"),
    "AVGO": ("Broadcom", "US", "Semi-conducteurs"),
    "GOOGL": ("Alphabet", "US", "Internet"),
    "META": ("Meta Platforms", "US", "Internet"),
    "AMZN": ("Amazon", "US", "Internet / cloud"),
    "ORCL": ("Oracle", "US", "Logiciel / cloud"),
    "CRM": ("Salesforce", "US", "Logiciel"),
    "ADBE": ("Adobe", "US", "Logiciel"),
    "AMD": ("AMD", "US", "Semi-conducteurs"),
    "CSCO": ("Cisco", "US", "Réseaux"),
    "ACN": ("Accenture", "IE", "Services IT"),
    "IBM": ("IBM", "US", "Services IT / logiciel"),
    "INTU": ("Intuit", "US", "Logiciel"),
    "NOW": ("ServiceNow", "US", "Logiciel"),
    "QCOM": ("Qualcomm", "US", "Semi-conducteurs"),
    "TXN": ("Texas Instruments", "US", "Semi-conducteurs"),
    "AMAT": ("Applied Materials", "US", "Équipement semi"),
    "LRCX": ("Lam Research", "US", "Équipement semi"),
    "KLAC": ("KLA", "US", "Équipement semi"),
    "MU": ("Micron", "US", "Mémoire"),
    "ADI": ("Analog Devices", "US", "Semi-conducteurs"),
    "INTC": ("Intel", "US", "Semi-conducteurs"),
    "PANW": ("Palo Alto Networks", "US", "Cybersécurité"),
    "CRWD": ("CrowdStrike", "US", "Cybersécurité"),
    "ANET": ("Arista Networks", "US", "Réseaux"),
    "SNPS": ("Synopsys", "US", "Logiciel EDA"),
    "CDNS": ("Cadence Design", "US", "Logiciel EDA"),
    "PLTR": ("Palantir", "US", "Logiciel"),
    "APP": ("AppLovin", "US", "Logiciel adtech"),
    "FTNT": ("Fortinet", "US", "Cybersécurité"),
    "WDAY": ("Workday", "US", "Logiciel"),
    "ADSK": ("Autodesk", "US", "Logiciel"),
    "MRVL": ("Marvell", "US", "Semi-conducteurs"),
    "DELL": ("Dell Technologies", "US", "Hardware"),
    "APH": ("Amphenol", "US", "Composants"),
    "MSI": ("Motorola Solutions", "US", "Équipements"),
    "TEL": ("TE Connectivity", "CH", "Composants"),
    "GLW": ("Corning", "US", "Composants"),
    "MPWR": ("Monolithic Power", "US", "Semi-conducteurs"),
    "MCHP": ("Microchip", "US", "Semi-conducteurs"),
    "ON": ("ON Semiconductor", "US", "Semi-conducteurs"),
    "STX": ("Seagate", "IE", "Stockage"),
    "WDC": ("Western Digital", "US", "Stockage"),
    "SMCI": ("Super Micro Computer", "US", "Hardware"),
    "HPQ": ("HP Inc.", "US", "Hardware"),
    "HPE": ("Hewlett Packard Enterprise", "US", "Hardware"),
    "NTAP": ("NetApp", "US", "Stockage"),
    "SNOW": ("Snowflake", "US", "Logiciel"),
    "DDOG": ("Datadog", "US", "Logiciel"),
    "NET": ("Cloudflare", "US", "Logiciel"),
    "ZS": ("Zscaler", "US", "Cybersécurité"),
    "TEAM": ("Atlassian", "US", "Logiciel"),
    "HUBS": ("HubSpot", "US", "Logiciel"),
    "ROP": ("Roper Technologies", "US", "Logiciel"),
    "FICO": ("Fair Isaac", "US", "Logiciel / analytique"),
    "IT": ("Gartner", "US", "Services IT"),
    "CTSH": ("Cognizant", "US", "Services IT"),
    "KEYS": ("Keysight", "US", "Instruments"),
    "TSM": ("TSMC", "TW", "Fonderie"),
    "ASML": ("ASML", "NL", "Équipement semi"),
    "SAP": ("SAP", "DE", "Logiciel"),
    "SONY": ("Sony", "JP", "Électronique / divertissement"),
    "ARM": ("Arm Holdings", "GB", "Semi-conducteurs (IP)"),
    "SHOP": ("Shopify", "CA", "Logiciel e-commerce"),
    "INFY": ("Infosys", "IN", "Services IT"),
    "WIT": ("Wipro", "IN", "Services IT"),
    "UMC": ("United Microelectronics", "TW", "Fonderie"),
    "ASX": ("ASE Technology", "TW", "Assemblage & test"),
    "STM": ("STMicroelectronics", "FR/IT", "Semi-conducteurs"),
    "NXPI": ("NXP Semiconductors", "NL", "Semi-conducteurs"),
    "LOGI": ("Logitech", "CH", "Hardware"),
    "ERIC": ("Ericsson", "SE", "Équipements télécom"),
    "NOK": ("Nokia", "FI", "Équipements télécom"),
    "CHKP": ("Check Point", "IL", "Cybersécurité"),
    "NICE": ("NICE", "IL", "Logiciel"),
    "MNDY": ("monday.com", "IL", "Logiciel"),
    "GIB": ("CGI", "CA", "Services IT"),
    "OTEX": ("OpenText", "CA", "Logiciel"),
    "WIX": ("Wix.com", "IL", "Logiciel"),
    "TCEHY": ("Tencent", "CN", "Internet"),
    "BABA": ("Alibaba", "CN", "Internet / cloud"),
    "BIDU": ("Baidu", "CN", "Internet"),
    "NTES": ("NetEase", "CN", "Jeux / internet"),
    "LNVGY": ("Lenovo", "CN", "Hardware"),
    "IFNNY": ("Infineon", "DE", "Semi-conducteurs"),
    "DASTY": ("Dassault Systèmes", "FR", "Logiciel"),
    "ASMIY": ("ASM International", "NL", "Équipement semi"),
    "BESIY": ("BE Semiconductor", "NL", "Équipement semi"),
    "ATEYY": ("Advantest", "JP", "Équipement test"),
    "KYCCF": ("Keyence", "JP", "Automatisation"),
    "TER": ("Teradyne", "US", "Équipement test"),
    "COHR": ("Coherent", "US", "Optique"),
    "CIEN": ("Ciena", "US", "Réseaux optiques"),
    "LITE": ("Lumentum", "US", "Optique"),
    "JBL": ("Jabil", "US", "Sous-traitance électronique"),
    "FLEX": ("Flex", "SG", "Sous-traitance électronique"),
    "CLS": ("Celestica", "CA", "Sous-traitance électronique"),
    "GFS": ("GlobalFoundries", "US", "Fonderie"),
    "CRDO": ("Credo Technology", "US", "Semi-conducteurs"),
    "ALAB": ("Astera Labs", "US", "Semi-conducteurs"),
    "VRSN": ("VeriSign", "US", "Infrastructure internet"),
    "GDDY": ("GoDaddy", "US", "Internet"),
    "AKAM": ("Akamai", "US", "Infrastructure internet"),
    "FFIV": ("F5", "US", "Réseaux"),
    "PTC": ("PTC", "US", "Logiciel"),
    "TYL": ("Tyler Technologies", "US", "Logiciel"),
    "ZM": ("Zoom Communications", "US", "Logiciel"),
    "DOCU": ("DocuSign", "US", "Logiciel"),
    "GRMN": ("Garmin", "CH", "Électronique"),
    "CDW": ("CDW", "US", "Distribution IT"),
    "GEN": ("Gen Digital", "US", "Cybersécurité"),
    "TWLO": ("Twilio", "US", "Logiciel"),
    "OKTA": ("Okta", "US", "Cybersécurité"),
    "MDB": ("MongoDB", "US", "Logiciel"),
    "NTNX": ("Nutanix", "US", "Logiciel"),
    "ZBRA": ("Zebra Technologies", "US", "Hardware"),
    "TRMB": ("Trimble", "US", "Logiciel / instruments"),
    "SNDK": ("SanDisk", "US", "Mémoire"),
    "EPAM": ("EPAM Systems", "US", "Services IT"),
    "CNSWF": ("Constellation Software", "CA", "Logiciel"),
    "CGEMY": ("Capgemini", "FR", "Services IT"),
    "NTDOY": ("Nintendo", "JP", "Jeux"),
    "HNHPF": ("Hon Hai (Foxconn)", "TW", "Sous-traitance électronique"),
    "ADYEY": ("Adyen", "NL", "Paiements"),
}

# Poids du score de qualité des bénéfices (EQS)
EQS_WEIGHTS = {
    "accruals": 0.30,   # plus bas = mieux (plancher -15 % : au-delà, c'est surtout la rémunération
                        # en actions, non cash, qui écrase le RN — pas un surcroît de qualité)
    "cfo_ni": 0.20,     # plus haut = mieux (plafonné à 2)
    "ni_oi": 0.20,      # plus bas = mieux (RN peu dopé par le non-opérationnel)
    "om": 0.15,         # niveau de marge opérationnelle GAAP (pénalise les profits « ajustés »)
    "d_om": 0.10,       # variation de marge opérationnelle
    "d_gm": 0.05,       # variation de marge brute
}
ACCRUALS_FLOOR = -0.15
CFO_NI_CAP = 2.0
NI_OI_FLOOR = 0.85


def fnum(x: str | None) -> float | None:
    return float(x) if x not in ("", None) else None


def months_between(d1: date, d2: date) -> int:
    return (d2.year - d1.year) * 12 + (d2.month - d1.month)


def load_snapshot(path: Path) -> dict[str, list[dict]]:
    by_ticker: dict[str, list[dict]] = defaultdict(list)
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            by_ticker[r["ticker"]].append({
                "date": date.fromisoformat(r["period_end"]),
                "type": r["type"],
                "rev": fnum(r["revenue"]),
                "gp": fnum(r["gross_profit"]),
                "oi": fnum(r["operating_income"]),
                "ni": fnum(r["net_income"]),
                "ta": fnum(r["total_assets"]),
                "ocf_ytd": fnum(r["operating_cash_flow_ytd"]),
            })
    return by_ticker


def fiscal_pos(d: date, fye_month: int) -> int:
    """0 = fin d'exercice (T4), 3 = T1, 6 = S1, 9 = 9 mois."""
    return (d.month - fye_month) % 12


def quarter_at(qs: list[dict], d: date, offset_months: int) -> dict | None:
    for q in qs:
        if months_between(q["date"], d) == offset_months:
            return q
    return None


def standalone_ocf(q: dict, qs: list[dict], fye: int, field: str = "ocf_ytd") -> float | None:
    """Les flux de trésorerie Zacks trimestriels sont cumulés depuis le début de l'exercice."""
    if q.get(field) is None:
        return None
    if fiscal_pos(q["date"], fye) == 3:
        return q[field]
    prev = quarter_at(qs, q["date"], 3)
    if prev is None or prev.get(field) is None:
        return None
    return q[field] - prev[field]


def ttm_ytd_field(recs: list[dict], field: str) -> tuple[float | None, date | None]:
    """TTM d'un flux publié en cumul annuel (dernier trimestre calculable, sinon dernier exercice)."""
    recs = sorted(recs, key=lambda r: r["date"])
    qs = [r for r in recs if r["type"] == "Q"]
    annuals = [r for r in recs if r["type"] == "A"]
    fye = annuals[-1]["date"].month if annuals else 12
    for anchor in reversed([q for q in qs if q.get(field) is not None][-2:]):
        window = [quarter_at(qs, anchor["date"], k) for k in (9, 6, 3, 0)]
        if all(window):
            vals = [standalone_ocf(w, qs, fye, field) for w in window]
            if None not in vals:
                return sum(vals), anchor["date"]
        pos = fiscal_pos(anchor["date"], fye)
        if pos == 0:
            return anchor[field], anchor["date"]
        prior = quarter_at(qs, anchor["date"], 12)
        fy_prev = next((a for a in annuals if months_between(a["date"], anchor["date"]) == pos), None)
        if prior and fy_prev and prior.get(field) is not None and fy_prev.get(field) is not None:
            return anchor[field] + fy_prev[field] - prior[field], anchor["date"]
    if annuals and annuals[-1].get(field) is not None:
        return annuals[-1][field], annuals[-1]["date"]
    return None, None


def load_cashflow(path: Path) -> dict[str, dict]:
    """data/zacks_cashflow.csv : CFO et capex (cumul annuel) -> FCF TTM par société."""
    if not path.exists():
        return {}
    by_ticker: dict[str, list[dict]] = defaultdict(list)
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            by_ticker[r["ticker"]].append({
                "date": date.fromisoformat(r["period_end"]), "type": r["type"],
                "ocf": fnum(r["operating_cash_flow_ytd"]), "capex": fnum(r["capex_ytd"]),
            })
    out = {}
    for t, recs in by_ticker.items():
        ocf, end = ttm_ytd_field(recs, "ocf")
        capex, end_c = ttm_ytd_field(recs, "capex")
        if ocf is not None and capex is not None and end == end_c:
            # capex publié en négatif (sortie de trésorerie)
            out[t] = {"cfo_ttm_cf": ocf, "capex_ttm": abs(capex), "fcf_ttm": ocf - abs(capex), "fin_fcf": end}
    return out


def sum_or_none(vals):
    return None if any(v is None for v in vals) else sum(vals)


def ttm_block(qs: list[dict], anchor: dict, fye: int, annuals: list[dict]) -> dict | None:
    """Agrège 4 trimestres se terminant à `anchor`."""
    window = [quarter_at(qs, anchor["date"], k) for k in (9, 6, 3, 0)]
    if any(w is None for w in window):
        return None
    out = {k: sum_or_none([w[k] for w in window]) for k in ("rev", "gp", "oi", "ni")}
    if out["rev"] is None or out["ni"] is None or out["oi"] is None:
        return None
    ocf = sum_or_none([standalone_ocf(w, qs, fye) for w in window])
    if ocf is None:  # repli : YTD(t) + exercice précédent - YTD(t-12 mois)
        pos = fiscal_pos(anchor["date"], fye)
        if pos == 0:
            ocf = anchor["ocf_ytd"]
        else:
            prior_same = quarter_at(qs, anchor["date"], 12)
            fy_prev = next((a for a in annuals if months_between(a["date"], anchor["date"]) == pos), None)
            if prior_same and fy_prev and None not in (anchor["ocf_ytd"], prior_same["ocf_ytd"], fy_prev["ocf_ytd"]):
                ocf = anchor["ocf_ytd"] + fy_prev["ocf_ytd"] - prior_same["ocf_ytd"]
    out["ocf"] = ocf
    ta_now = anchor["ta"]
    ta_prev = (quarter_at(qs, anchor["date"], 12) or {}).get("ta")
    out["avg_ta"] = (ta_now + ta_prev) / 2 if ta_now and ta_prev else ta_now
    out["end"] = anchor["date"]
    out["basis"] = "TTM"
    # trimestres « dopés » : RN > 1,3 x ROP, ou RN > 0 avec ROP < 0
    out["boosted_q"] = sum(
        1 for w in window
        if w["ni"] is not None and w["oi"] is not None
        and ((w["oi"] > 0 and w["ni"] > 1.3 * w["oi"]) or (w["oi"] <= 0 < w["ni"]))
    )
    return out


def fy_block(a: dict, annuals: list[dict]) -> dict:
    prev = next((p for p in annuals if months_between(p["date"], a["date"]) == 12), None)
    ta_prev = prev["ta"] if prev else None
    return {
        "rev": a["rev"], "gp": a["gp"], "oi": a["oi"], "ni": a["ni"], "ocf": a["ocf_ytd"],
        "avg_ta": (a["ta"] + ta_prev) / 2 if a["ta"] and ta_prev else a["ta"],
        "end": a["date"], "basis": "Exercice",
        "boosted_q": int(a["oi"] is not None and a["ni"] is not None and a["oi"] > 0 and a["ni"] > 1.3 * a["oi"]),
    }


def analyse(ticker: str, recs: list[dict]) -> dict:
    recs = sorted(recs, key=lambda r: r["date"])
    qs = [r for r in recs if r["type"] == "Q"]
    annuals = [r for r in recs if r["type"] == "A"]
    fye = annuals[-1]["date"].month if annuals else FYE_OVERRIDE.get(ticker, 12)

    cur = prev = None
    usable = [q for q in qs if q["ni"] is not None and q["rev"] is not None]
    # ancre = dernier trimestre dont le CFO TTM est calculable (le plus récent est parfois incomplet)
    for anchor in reversed(usable[-3:]):
        cur = ttm_block(qs, anchor, fye, annuals)
        if cur is not None and cur["ocf"] is not None:
            prior_anchor = quarter_at(qs, anchor["date"], 12)
            prev = ttm_block(qs, prior_anchor, fye, annuals) if prior_anchor else None
            break
        cur = None
    if cur is None and annuals:
        a = annuals[-1]
        if a["ocf_ytd"] is not None and a["ni"] is not None:
            cur = fy_block(a, annuals)
            p = next((x for x in annuals if months_between(x["date"], a["date"]) == 12), None)
            prev = fy_block(p, annuals) if p else None

    name, country, segment = UNIVERSE.get(ticker, (ticker, "?", "?"))
    res = {"ticker": ticker, "nom": name, "pays": country, "segment": segment}
    if cur is None:
        res["statut"] = "exclu : données insuffisantes"
        return res

    res.update({
        "base": cur["basis"], "fin_periode": cur["end"].isoformat(),
        "ca": cur["rev"], "rn": cur["ni"], "rop": cur["oi"], "cfo": cur["ocf"],
        "trim_dopes": cur["boosted_q"],
    })
    res["marge_op"] = cur["oi"] / cur["rev"] if cur["rev"] else None
    res["marge_brute"] = cur["gp"] / cur["rev"] if cur["rev"] and cur["gp"] is not None else None
    res["accruals"] = (cur["ni"] - cur["ocf"]) / cur["avg_ta"] if cur["avg_ta"] else None
    res["cfo_rn"] = cur["ocf"] / cur["ni"] if cur["ni"] > 0 else None
    res["rn_rop"] = cur["ni"] / cur["oi"] if cur["oi"] > 0 else None
    if prev:
        res["croiss_ca"] = cur["rev"] / prev["rev"] - 1 if prev["rev"] else None
        pm = prev["oi"] / prev["rev"] if prev["rev"] else None
        res["d_marge_op"] = res["marge_op"] - pm if pm is not None and res["marge_op"] is not None else None
        pg = prev["gp"] / prev["rev"] if prev["rev"] and prev["gp"] is not None else None
        res["d_marge_brute"] = (res["marge_brute"] - pg) if (pg is not None and res["marge_brute"] is not None) else None
        res["croiss_rop"] = cur["oi"] / prev["oi"] - 1 if prev["oi"] and prev["oi"] > 0 else None

    if cur["end"] < STALE_BEFORE:
        res["statut"] = "exclu : données périmées"
    elif cur["ni"] <= 0:
        res["statut"] = "exclu : résultat net TTM négatif"
    elif cur["oi"] <= 0:
        res["statut"] = "exclu : résultat opérationnel TTM négatif"
    else:
        res["statut"] = "retenu"
    return res


def pct_rank(values: dict[str, float], higher_is_better: bool) -> dict[str, float]:
    """Rang centile 0-100 (ex aequo moyennés)."""
    items = sorted(values.items(), key=lambda kv: kv[1], reverse=higher_is_better)  # meilleur en tête
    n = len(items)
    out = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and items[j + 1][1] == items[i][1]:
            j += 1
        score = 100.0 * (1 - ((i + j) / 2) / (n - 1)) if n > 1 else 100.0
        for k in range(i, j + 1):
            out[items[k][0]] = score
        i = j + 1
    return out


def score_quality(rows: list[dict]) -> None:
    kept = [r for r in rows if r["statut"] == "retenu"]
    comps = {
        "accruals": ({r["ticker"]: max(r["accruals"], ACCRUALS_FLOOR)
                      for r in kept if r.get("accruals") is not None}, False),
        "cfo_ni": ({r["ticker"]: min(r["cfo_rn"], CFO_NI_CAP) for r in kept if r.get("cfo_rn") is not None}, True),
        "ni_oi": ({r["ticker"]: max(r["rn_rop"], NI_OI_FLOOR) for r in kept if r.get("rn_rop") is not None}, False),
        "om": ({r["ticker"]: r["marge_op"] for r in kept if r.get("marge_op") is not None}, True),
        "d_om": ({r["ticker"]: r["d_marge_op"] for r in kept if r.get("d_marge_op") is not None}, True),
        "d_gm": ({r["ticker"]: r["d_marge_brute"] for r in kept if r.get("d_marge_brute") is not None}, True),
    }
    ranks = {k: pct_rank(v, hib) for k, (v, hib) in comps.items()}
    for r in kept:
        tot = wsum = 0.0
        for k, w in EQS_WEIGHTS.items():
            if r["ticker"] in ranks[k]:
                tot += w * ranks[k][r["ticker"]]
                wsum += w
        r["eqs"] = tot / wsum if wsum else None
        flags = []
        if r.get("accruals") is not None and r["accruals"] > 0.10:
            flags.append("accruals élevés")
        if r.get("cfo_rn") is not None and r["cfo_rn"] < 0.8:
            flags.append("conversion cash faible")
        if r.get("rn_rop") is not None and r["rn_rop"] > 1.0:
            flags.append("RN > ROP (gains non opérationnels)")
        if r.get("trim_dopes", 0) >= 2:
            flags.append(f"{r['trim_dopes']} trimestres dopés")
        if r.get("d_marge_op") is not None and r["d_marge_op"] < -0.03:
            flags.append("marge op. en baisse")
        r["alertes"] = "; ".join(flags)


# ---------------------------------------------------------------- étape 2
def load_profile(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    with open(path, newline="") as f:
        return {r["ticker"]: {k: (fnum(v) if k not in ("ticker", "zacks_industry", "next_eps_date") else v)
                              for k, v in r.items()} for r in csv.DictReader(f)}


def score_opportunity(rows: list[dict], prof: dict[str, dict], cash: dict[str, dict]) -> None:
    cand = [r for r in rows if r.get("eqs") is not None and r["ticker"] in prof]
    if not cand:
        return
    for r in cand:
        p = prof[r["ticker"]]
        r.update({k: p.get(k) for k in p if k != "ticker"})
        price, tgt = p.get("price"), p.get("target_avg")
        r["upside"] = tgt / price - 1 if price and tgt else None
        mcap = p.get("market_cap")
        # P/E sur résultat net GAAP TTM (la rémunération en actions y reste une charge)
        r["pe_gaap"] = mcap / r["rn"] if mcap and r.get("rn") and r["rn"] > 0 else None
        c = cash.get(r["ticker"])
        if c:
            r.update(c)
            r["fcf_yield"] = c["fcf_ttm"] / mcap if mcap else None
            r["fcf_rn"] = c["fcf_ttm"] / r["rn"] if r.get("rn") and r["rn"] > 0 else None
            r["capex_cfo"] = c["capex_ttm"] / c["cfo_ttm_cf"] if c["cfo_ttm_cf"] and c["cfo_ttm_cf"] > 0 else None
        eps_f1, eps_f2 = p.get("eps_f1"), p.get("eps_f2")
        r["croiss_bpa_f2"] = eps_f2 / eps_f1 - 1 if eps_f1 and eps_f2 and eps_f1 > 0 else None
        # PEG « maison » : P/E N+1 / croissance BPA N+1 (en %), à défaut PEG Zacks
        g = r["croiss_bpa_f2"]
        pe2 = p.get("pe_f2")
        r["peg2"] = pe2 / (100 * g) if pe2 and g and g > 0.02 else p.get("peg")
        r["revision"] = (p.get("rev4w_f1") or 0) * 0.5 + (p.get("rev4w_f2") or 0) * 0.5

    val = {
        "pe_f2": pct_rank({r["ticker"]: r["pe_f2"] for r in cand if r.get("pe_f2") and r["pe_f2"] > 0}, False),
        "peg2": pct_rank({r["ticker"]: r["peg2"] for r in cand if r.get("peg2") and r["peg2"] > 0}, False),
        "p_cf": pct_rank({r["ticker"]: r["p_cf"] for r in cand if r.get("p_cf") and r["p_cf"] > 0}, False),
        "pe_gaap": pct_rank({r["ticker"]: r["pe_gaap"] for r in cand if r.get("pe_gaap")}, False),
    }
    mom = {
        "rank": pct_rank({r["ticker"]: r["zacks_rank"] for r in cand if r.get("zacks_rank")}, False),
        "revision": pct_rank({r["ticker"]: r["revision"] for r in cand if r.get("revision") is not None}, True),
        "upside": pct_rank({r["ticker"]: r["upside"] for r in cand if r.get("upside") is not None}, True),
    }

    def avg(parts, t):
        xs = [p[t] for p in parts if t in p]
        return sum(xs) / len(xs) if xs else None

    for r in cand:
        t = r["ticker"]
        r["score_valo"] = avg(list(val.values()), t)
        r["score_momentum"] = avg(list(mom.values()), t)
        parts = [(0.45, r["eqs"]), (0.30, r["score_valo"]), (0.25, r["score_momentum"])]
        wsum = sum(w for w, v in parts if v is not None)
        r["score_opportunite"] = sum(w * v for w, v in parts if v is not None) / wsum


# ---------------------------------------------------------------- étape 3
FCF_RN_MIN = 0.8  # le bénéfice doit se retrouver en cash disponible APRÈS investissements


def score_final(rows: list[dict]) -> None:
    """Contrôle cash-flow libre sur les finalistes (ceux dont le capex a été collecté).

    Le ratio de Sloan ignore le capex : un groupe qui réinvestit tout (voire plus) de son
    cash opérationnel peut afficher d'excellents accruals. D'où une barrière FCF, puis un
    score final = 40 % EQS + 20 % rendement FCF + 20 % valorisation + 20 % momentum.
    """
    fin = [r for r in rows if r.get("score_opportunite") is not None and r.get("fcf_ttm") is not None]
    for r in fin:
        ok = r["fcf_ttm"] > 0 and (r.get("fcf_rn") or 0) >= FCF_RN_MIN
        r["controle_fcf"] = "ok" if ok else "échec"
    passed = [r for r in fin if r["controle_fcf"] == "ok"]
    fy = pct_rank({r["ticker"]: r["fcf_yield"] for r in passed if r.get("fcf_yield") is not None}, True)
    for r in passed:
        r["score_final"] = (0.40 * r["eqs"] + 0.20 * fy.get(r["ticker"], 50.0)
                            + 0.20 * (r["score_valo"] or 50.0) + 0.20 * (r["score_momentum"] or 50.0))
    for i, r in enumerate(sorted(passed, key=lambda x: -x["score_final"]), 1):
        r["rang_final"] = i


SENSIBILITE = {  # (EQS, rendement FCF, valorisation, momentum)
    "base 40/20/20/20": (0.40, 0.20, 0.20, 0.20),
    "égal 25/25/25/25": (0.25, 0.25, 0.25, 0.25),
    "qualité 55/15/15/15": (0.55, 0.15, 0.15, 0.15),
    "sans momentum 50/25/25/0": (0.50, 0.25, 0.25, 0.00),
    "valeur 30/30/30/10": (0.30, 0.30, 0.30, 0.10),
    "cash 35/35/15/15": (0.35, 0.35, 0.15, 0.15),
}


def sensibilite(rows: list[dict]) -> list[tuple[str, list[tuple[str, float]]]]:
    """Le n°1 dépend-il des pondérations ? Recalcule le score final sous 6 jeux de poids."""
    passed = [r for r in rows if r.get("rang_final")]
    fy = pct_rank({r["ticker"]: r["fcf_yield"] for r in passed}, True)
    out = []
    for name, (a, b, c, d) in SENSIBILITE.items():
        sc = {r["ticker"]: a * r["eqs"] + b * fy[r["ticker"]] + c * r["score_valo"] + d * r["score_momentum"]
              for r in passed}
        out.append((name, sorted(sc.items(), key=lambda kv: -kv[1])))
    return out


# ---------------------------------------------------------------- sorties
COLS = ["ticker", "nom", "pays", "segment", "statut", "base", "fin_periode", "ca", "rn", "rop", "cfo",
        "marge_brute", "marge_op", "croiss_ca", "d_marge_brute", "d_marge_op", "accruals", "cfo_rn", "rn_rop",
        "trim_dopes", "eqs", "alertes", "zacks_rank", "price", "target_avg", "upside", "pe_f1", "pe_f2",
        "croiss_bpa_f2", "peg2", "p_cf", "pe_gaap", "fcf_ttm", "fcf_yield", "fcf_rn", "capex_cfo", "rev4w_f1",
        "rev4w_f2", "chg_52w", "market_cap", "score_valo", "score_momentum", "score_opportunite", "controle_fcf",
        "score_final", "rang_final"]


def fmt(v):
    if isinstance(v, float):
        return f"{v:.4f}"
    return "" if v is None else v


def main() -> None:
    snap = load_snapshot(DATA / "zacks_snapshot.csv")
    rows = [analyse(t, recs) for t, recs in snap.items()]
    score_quality(rows)
    score_opportunity(rows, load_profile(DATA / "zacks_profile.csv"), load_cashflow(DATA / "zacks_cashflow.csv"))
    score_final(rows)
    rows.sort(key=lambda r: (r.get("rang_final") is None, r.get("rang_final") or 0,
                             r.get("score_opportunite") is None, -(r.get("score_opportunite") or 0),
                             -(r.get("eqs") or -1)))
    with open(HERE / "resultats.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for r in rows:
            w.writerow([fmt(r.get(c)) for c in COLS])

    kept = [r for r in rows if r.get("eqs") is not None]
    print(f"Univers : {len(rows)} sociétés — retenues : {len(kept)}")
    for r in rows:
        if r["statut"] != "retenu":
            print(f"  {r['ticker']:6} {r['statut']}")
    print("\nTop qualité des bénéfices (EQS) :")
    for r in sorted(kept, key=lambda r: -r["eqs"])[:40]:
        print(f"  {r['ticker']:6} EQS {r['eqs']:5.1f} | accruals {r['accruals']:+.3f} | CFO/RN "
              f"{(r['cfo_rn'] or 0):5.2f} | RN/ROP {(r['rn_rop'] or 0):4.2f} | dMop "
              f"{(r.get('d_marge_op') or 0):+.3f} | CA {(r.get('croiss_ca') or 0):+.1%} | {r['base']} "
              f"{r['fin_periode']} | {r['alertes']}")
    if any(r.get("score_opportunite") is not None for r in rows):
        print("\nClassement opportunité :")
        for r in [x for x in rows if x.get("score_opportunite") is not None][:25]:
            print(f"  {r['ticker']:6} {r['score_opportunite']:5.1f} (EQS {r['eqs']:5.1f}, valo "
                  f"{(r['score_valo'] or 0):5.1f}, momentum {(r['score_momentum'] or 0):5.1f}) | P/E N+1 "
                  f"{(r.get('pe_f2') or 0):5.1f} | P/E GAAP {(r.get('pe_gaap') or 0):5.1f} | PEG {(r.get('peg2') or 0):4.2f} | "
                  f"rank {r.get('zacks_rank')} | upside {(r.get('upside') or 0):+.0%} | FCF/RN "
                  f"{(r.get('fcf_rn') if r.get('fcf_rn') is not None else float('nan')):5.2f} | FCF yield "
                  f"{(r.get('fcf_yield') if r.get('fcf_yield') is not None else float('nan')):+.1%}")
    fin = [r for r in rows if r.get("controle_fcf")]
    if fin:
        print("\nContrôle FCF (finalistes) :")
        for r in [x for x in fin if x["controle_fcf"] == "échec"]:
            print(f"  {r['ticker']:6} ÉCHEC — FCF TTM {r['fcf_ttm']:,.0f} M$ | FCF/RN {r['fcf_rn']:.2f}")
        print("\nClassement final :")
        for r in sorted([x for x in fin if x.get("rang_final")], key=lambda x: x["rang_final"]):
            print(f"  {r['rang_final']:2d}. {r['ticker']:6} {r['score_final']:5.1f} | EQS {r['eqs']:5.1f} | FCF yield "
                  f"{r['fcf_yield']:+.1%} | FCF/RN {r['fcf_rn']:.2f} | P/E N+1 {r['pe_f2']:5.1f} | P/E GAAP "
                  f"{r['pe_gaap']:5.1f} | rank {r['zacks_rank']:.0f} | révisions 4 sem. {r['revision']:+.2f}% | "
                  f"upside {'n.d.' if r['upside'] is None else format(r['upside'], '+.0%')}")
        sens = sensibilite(rows)
        with open(HERE / "sensibilite.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["ponderation", "rang", "ticker", "score"])
            for name, order in sens:
                for i, (t, v) in enumerate(order, 1):
                    w.writerow([name, i, t, f"{v:.2f}"])
        print("\nSensibilité aux pondérations (EQS / rdt FCF / valo / momentum) :")
        for name, order in sens:
            print(f"  {name:26} -> " + ", ".join(f"{t} {v:.1f}" for t, v in order[:3]))


if __name__ == "__main__":
    main()
