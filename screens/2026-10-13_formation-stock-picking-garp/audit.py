#!/usr/bin/env python3
"""Audit des données de la formation : chaque ligne des CSV de data/ est-elle utilisée par le diaporama ?

`python3 audit.py` (après calcul.py et build_slides.py) écrit AUDIT_DONNEES.md :
- par fichier, le nombre de lignes et celles qui n'apparaissent pas dans le document, avec la raison ;
- les diapositives de contenu sans source en pied de page.
La fonction `couverture()` sert aussi à l'annexe « Les données » du diaporama.
"""
import csv
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# fichiers lus en entier (boucles) : toutes leurs lignes sont affichées ou calculées
EN_ENTIER = {"comptes_annuels.csv": "comptes des quatre sociétés, lus en boucle par calcul.py",
             "etf.csv": "tableau des principaux ETF, lu en boucle",
             "dca_exemple.csv": "chemins de prix de l'exemple de DCA",
             "historique_bpa.csv": "historiques de Micron et d'Intel",
             "categories_lynch.csv": "six catégories de Lynch, lues en boucle",
             "palmares_lynch.csv": "palmarès de Lynch",
             "hypotheses.csv": "hypothèses, toutes justifiées et chargées par calcul.py"}
# lignes volontairement non affichées, avec la raison
RAISONS = {("qqq_positions_2026-09-04.csv", "*"): "le diaporama montre les 10 premières lignes de QQQ sur 15 relevées",
           ("investisseurs.csv", "lynch_magellan"): "doublon du palmarès de Lynch (palmares_lynch.csv), déjà affiché",
           ("nvda_zacks_2026-10-12.csv", "pe_12_derniers_mois"): "valeur de contrôle : le P/E 12 mois est recalculé (cours ÷ BPA 12 mois)",
           ("etudes_immobilier.csv", "demers_eisfeldt"): "rendement nominal américain, non comparable aux rendements réels : cité dans RAPPORT.md",
           ("etudes_immobilier.csv", "senat_actions"): "chiffre repris dans le texte du résultat du Sénat (6,2 %)"}
DESCRIPTIONS = {"comptes_annuels.csv": "Comptes annuels (Zacks)", "adyen_s1_2026.csv": "Adyen, premier semestre 2026", "nu_t2_2026.csv": "Nu, deuxième trimestre 2026",
                "reddit_t2_2026.csv": "Reddit, deuxième trimestre 2026", "nvda_zacks_2026-10-12.csv": "NVIDIA, consensus Zacks", "historique_bpa.csv": "Historiques de BPA (cycliques)",
                "fiscalite.csv": "Fiscalité et frais 2026", "hypotheses.csv": "Hypothèses justifiées", "investisseurs.csv": "Citations des grands investisseurs",
                "super_investisseurs.csv": "Stratégies de huit autres investisseurs", "palmares_lynch.csv": "Palmarès de Peter Lynch", "categories_lynch.csv": "Catégories de Lynch",
                "horizon_dca.csv": "Horizon, krachs et DCA", "dca_exemple.csv": "Exemple de DCA", "etf.csv": "Principaux ETF", "etf_regles.csv": "Règles des ETF",
                "etf_us_zacks_2026-10-13.csv": "ETF américains (Zacks)", "qqq_positions_2026-09-04.csv": "Positions de QQQ", "moat.csv": "Moat : définitions et preuves",
                "bible.csv": "PER, déclaration, ordres, indices, change, arnaques", "immobilier.csv": "Immobilier : rendements, risques, frais, fiscalité",
                "etudes_immobilier.csv": "Études académiques sur l'immobilier"}


def lire(nom):
    with open(os.path.join(DATA, nom), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def couverture():
    code = "".join(open(os.path.join(HERE, n), encoding="utf-8").read() for n in ("build_slides.py", "calcul.py"))
    out = []
    for nom in sorted(os.listdir(DATA)):
        if not nom.endswith(".csv"):
            continue
        rows = lire(nom)
        cle = next((k for k in ("id", "indicateur", "ticker", "scenario") if rows and k in rows[0]), None)
        manquants = []
        if nom not in EN_ENTIER and cle:
            for r in rows:
                i = r[cle]
                if f'"{i}"' in code or f"'{i}'" in code:
                    continue
                raison = RAISONS.get((nom, i)) or RAISONS.get((nom, "*"))
                manquants.append((i, raison))
        out.append({"fichier": nom, "description": DESCRIPTIONS.get(nom, nom), "lignes": len(rows),
                    "non_affichees": manquants, "sans_raison": [i for i, r in manquants if not r],
                    "mode": EN_ENTIER.get(nom, "lignes appelées une à une par leur identifiant")})
    return out


def sans_source():
    h = open(os.path.join(HERE, "diaporama", "index.html"), encoding="utf-8").read()
    manque = []
    for m in re.finditer(r'<section class="slide([^"]*)" id="s(\d+)"[^>]*data-titre="([^"]*)".*?<span class="src">(.*?)</span>', h, flags=re.S):
        cls, n, titre, src = m.groups()
        if " op" in cls or "cover" in cls or " nav" in cls or "ret-sl" in cls:
            continue
        if not re.sub(r"<[^>]+>", "", src).strip():
            manque.append((int(n), html.unescape(titre)))
    return manque


if __name__ == "__main__":
    C = couverture()
    L = ["# Audit des données de la formation", "",
         "Généré par `audit.py`. Une ligne est « utilisée » quand le diaporama l'appelle par son identifiant ou lit son fichier en entier.", "",
         "| Fichier | Contenu | Lignes | Non affichées | Lecture |", "|---|---|---|---|---|"]
    for c in C:
        L.append(f"| `data/{c['fichier']}` | {c['description']} | {c['lignes']} | {len(c['non_affichees'])} | {c['mode']} |")
    L += ["", "## Lignes non affichées, et pourquoi", ""]
    for c in C:
        for i, r in c["non_affichees"]:
            L.append(f"- `{c['fichier']}` · `{i}` : {r or 'SANS RAISON : à intégrer au document'}")
    s = sans_source()
    L += ["", "## Diapositives de contenu sans source", "", "Aucune." if not s else "\n".join(f"- {n}. {t}" for n, t in s)]
    tot = sum(c["lignes"] for c in C)
    nonaff = sum(len(c["non_affichees"]) for c in C)
    L += ["", f"Total : {tot} lignes de données, {tot - nonaff} utilisées dans le diaporama, {nonaff} non affichées avec raison ; "
          f"{sum(len(c['sans_raison']) for c in C)} sans raison."]
    open(os.path.join(HERE, "AUDIT_DONNEES.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L[-1:]))
    print("diapositives sans source :", s or "aucune")
