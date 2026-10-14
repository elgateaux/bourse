#!/usr/bin/env python3
"""RAPPORT.md de la formation GARP et sa ligne dans le README, générés depuis les données.

`python3 rapport.py [--lien URL]` : URL facultative de la version en ligne du diaporama.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(HERE, "..", ".."))
DOSSIER = "screens/2026-10-13_formation-stock-picking-garp"
sys.path.insert(0, HERE)
from calcul import fr, pct, eur, load  # noqa: E402

D = json.load(open(os.path.join(HERE, "diaporama", "donnees_formation.json"), encoding="utf-8"))
PLAN = json.load(open(os.path.join(HERE, "diaporama", "plan.json"), encoding="utf-8"))
TESTS = load(os.path.join(HERE, "calculatrice_tests.csv"))
lien = sys.argv[sys.argv.index("--lien") + 1] if "--lien" in sys.argv else ""
R, V, H = D["ratios"], D["val"], D["hyp"]
env = {e["enveloppe"]: e for e in D["enveloppes"]}
fx = D["frais"]
dca = D["dca"]
hz = D["horizon"]
etf = D["etf"]

chap = []
for x in PLAN:
    if not chap or chap[-1][0] != x["section"]:
        chap.append([x["section"], x["n"], x["n"]])
    chap[-1][2] = x["n"]

L = []
w = L.append
w("# Formation : le stock picking GARP, de zéro à autonome")
w("")
w(f"Diaporama du {D['date']} (cours du {D['date_cours']}) pour un investisseur français débutant : {len(PLAN)} diapositives, une calculatrice d'intérêts composés, "
  "un calculateur de PEG, un quiz de dix questions, un glossaire et des sources numérotées. Même style que la vidéo du portefeuille du même jour.")
w("")
w("*La Gazette du PEG est un titre fictif : il ne correspond à aucune publication existante. Analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé.*")
w("")
w("## Livrables")
w("")
if lien:
    w(f"- Version en ligne (privée tant qu'elle n'est pas partagée) : {lien}")
w("- [diaporama/index.html](diaporama/index.html) : la page autonome (polices embarquées, fonctionne hors ligne). Flèches du clavier pour avancer, T pour le sommaire ; mode lecture automatique sur téléphone.")
w("- [Formation_GARP_2026-10-13.pdf](Formation_GARP_2026-10-13.pdf) : une diapositive par page A4 paysage, rendue par Chromium et Playwright.")
w("- [planche_contact.jpg](planche_contact.jpg) : toutes les pages du PDF en vignettes.")
w("")
w("## Plan")
w("")
w("| Chapitre | Diapositives |")
w("|---|---|")
for c, a, b in chap:
    w(f"| {c} | {a} à {b} |")
w("")
w("## Chiffres clés (tous calculés par `calcul.py`)")
w("")
n, t = R["NVDA"], R["TSM"]
w(f"- **Lire les comptes.** NVIDIA, exercice 2026 : marge opérationnelle de {pct(n['marge_operationnelle'])}, FCF de {fr(n['fcf'] / 1000, 1)} Md$, ROIC de {pct(n['roic'])}. "
  f"TSMC, 2025 : capex de {pct(t['capex_ca'])} du chiffre d'affaires, contre {pct(n['capex_ca'])} pour NVIDIA. Reddit : {pct(R['RDDT']['dilution'], 1, True)} d'actions en un an.")
w(f"- **Valoriser.** Cinq P/E pour le même cours de NVIDIA, de {fr(min(p for *_, p in D['pe5']), 1)} à {fr(max(p for *_, p in D['pe5']), 1)}. "
  f"PEG de long terme du portefeuille : {fr(D['comparaison']['peg_lt']['ptf'], 2)}, contre {fr(D['comparaison']['peg_lt']['ndx'], 2)} pour le Nasdaq 100 reconstitué.")
w(f"- **Enveloppes.** {eur(D['defauts']['capital'])} puis {eur(D['defauts']['mensuel'])} par mois, {fr(D['defauts']['annees'], 0)} ans, {fr(D['defauts']['rendement'] * 100, 0)} % brut, "
  f"{fr(D['defauts']['frais'] * 100, 1)} % de frais : {eur(env['PEA']['net'])} nets dans un PEA, {eur(env['AV']['net'])} en assurance-vie, {eur(env['CTO']['net'])} sur un compte-titres.")
w(f"- **Frais.** Sur 30 ans, {pct(fx[2]['frais'], 0)} de frais par an coûtent {pct(fx[2]['part_perdue'])} du capital final ; {pct(fx[0]['frais'])} en coûtent {pct(fx[0]['part_perdue'])}. "
  f"Entre un ETF à {fr(D['etf_frais']['etf_frais_bas']['frais'] * 100, 2)} % et un ETF à {fr(D['etf_frais']['etf_frais_haut']['frais'] * 100, 2)} %, l'écart atteint "
  f"{eur(D['etf_frais']['etf_frais_bas']['valeur'] - D['etf_frais']['etf_frais_haut']['valeur'])} en 20 ans au scénario par défaut.")
b, h = dca["baisse_puis_rebond"], dca["hausse_reguliere"]
w(f"- **DCA.** Exemple pédagogique : après une baisse puis un rebond, le DCA finit à {eur(b['valeur_dca'])} contre {eur(b['valeur_lump'])} ; en hausse régulière, l'investissement en une fois finit à "
  f"{eur(h['valeur_lump'])} contre {eur(h['valeur_dca'])}. Vanguard (2023, MSCI World, 1976-2022) : l'investissement en une fois a gagné dans {fr(float(hz['dca_vanguard_2023']['valeur']), 0)} % des cas.")
w(f"- **Temps.** {eur(H['temps_versement'])} par mois de {fr(H['temps_age_tot'], 0)} à {fr(H['temps_age_fin'], 0)} ans : {eur(D['temps']['temps_age_tot']['valeur'])} ; "
  f"de {fr(H['temps_age_tard'], 0)} à {fr(H['temps_age_fin'], 0)} ans : {eur(D['temps']['temps_age_tard']['valeur'])}.")
w("")
w("## Données signalées et corrigées")
w("")
w(f"- BPA 2028 de NVIDIA : {fr(V['NVDA']['bpa_f2'], 2)} $ dans le comparateur Zacks, {D['nvda_zacks']['bpa_fy2028_fiche'].replace('.', ',')} $ sur la fiche Zacks du même jour. La formation retient le premier, comme le modèle.")
w(f"- Plus haut de 52 semaines de NVIDIA : {fr(V['NVDA']['plus_haut_52s'], 2)} $ dans le comparateur Zacks, un autre chiffre sur la fiche. Le comparateur est utilisé pour les cinq valeurs.")
w("- « À court terme le marché est une machine à voter… » : formule de Buffett résumant Graham, souvent prêtée à Graham. « Huitième merveille du monde » : citation apocryphe d'Einstein (Quote Investigator).")
w("- Frais courants des ETF : plusieurs sources se contredisent.")
for r in etf:
    if r["precision"] and ("%" in r["precision"]):
        w(f"  - {r['nom']} ({r['ticker']}) : {r['precision']}.")
w("- Part des périodes de perte du S&P 500 par horizon : les pourcentages dépendent de la base de données (Dimensional 1926-2017 pour 1, 5 et 10 ans ; Ben Carlson pour 20 ans).")
w(f"- Inflation de septembre 2026 : estimation provisoire de l'Insee ({hz['inflation_2026']['valeur'].replace('.', ',')} %), chiffre définitif attendu le 15/10/2026.")
w("- Retenue à la source de Taïwan sur les dividendes de TSMC : sources contradictoires, à vérifier auprès du courtier.")
w("- Accès aux sources : les pages de première main (AMF, Oaktree, Quote Investigator, émetteurs d'ETF) étaient inaccessibles depuis l'environnement de calcul (DNS ou proxy). "
  "Les chiffres ont été recoupés par la recherche web et par Zacks ; [Bigdata.com](https://bigdata.com) n'a pas pu être utilisé (crédits épuisés).")
w("")
w("## Hypothèses")
w("")
w("Toutes les hypothèses éditoriales sont marquées « hyp. » et justifiées ligne par ligne dans [data/hypotheses.csv](data/hypotheses.csv) : valeurs par défaut de la calculatrice "
  f"(rendement de {fr(H['calc_rendement'], 0)} %, sous les {fr(D['comparaison']['tcam_esperance']['ndx'] * 100, 1)} %/an espérés pour le Nasdaq 100), seuils de la grille GARP, noyau de "
  f"{fr(H['noyau_min'], 0)} à {fr(H['noyau_max'], 0)} %, exemples pédagogiques (formule cours = BPA × P/E, DCA).")
w("")
w("## Calculatrice")
w("")
w("Capitalisation mensuelle ; frais prélevés sur l'encours ; versement en fin de mois ; impôt d'un retrait total en fin de période :")
w(f"- PEA : {pct(D['params']['ps'])} de prélèvements sociaux après {fr(D['params']['pea_duree'], 0)} ans, {pct(D['params']['pfu'])} avant ;")
w(f"- compte-titres : {pct(D['params']['pfu'])} ;")
w(f"- assurance-vie, avant {fr(D['params']['av_duree'], 0)} ans : {pct(D['params']['ir_pfu'] + D['params']['ps_av'])} ;")
w(f"- assurance-vie, après {fr(D['params']['av_duree'], 0)} ans : {pct(D['params']['ps_av'])} de prélèvements sociaux, plus {pct(D['params']['av_taux_reduit'])} d'impôt au-delà de l'abattement "
  f"({eur(D['params']['av_abat_seul'])} ou {eur(D['params']['av_abat_couple'])}), et {pct(D['params']['ir_pfu'])} pour la part des primes au-delà de {eur(D['params']['av_seuil'])}.")
w("")
w("Les dividendes ne sont pas modélisés. "
  f"Le JavaScript est la traduction ligne à ligne de `simuler()` dans `calcul.py` : `verifier.js` le confronte aux {len(TESTS)} cas de "
  "[calculatrice_tests.csv](calculatrice_tests.csv), avec un écart maximal inférieur au centime.")
w("")
w("## Reproduire")
w("")
w("```sh")
w(f"cd {DOSSIER}")
w("python3 calcul.py                       # ratios, valorisation, grille, frais, enveloppes, tests -> CSV et diaporama/donnees_formation.json")
w("python3 build_slides.py                 # diaporama/index.html (ajouter --fragment CHEMIN pour la version Artifact)")
w("NODE_PATH=$(npm root -g) node verifier.js /tmp/captures   # captures, débordements, chevauchements, lisibilité, calculatrice, téléphone")
w("NODE_PATH=$(npm root -g) node pdf.js \"$PWD/Formation_GARP_2026-10-13.pdf\"")
w("python3 planche_contact.py && python3 rapport.py")
w("```")
w("")
w("Données d'entrée dans [data/](data/) : comptes annuels et consensus Zacks, résultats trimestriels de Nu, Reddit et Adyen, fiscalité 2026, citations, ETF, horizon et DCA, "
  "chacune avec deux sources par chiffre clé. Les sorties datées de l'analyse vidéo du même jour (P/E NTM, PEG, scénarios) sont réutilisées telles quelles.")
w("")
w("## Contrôles avant livraison")
w("")
w("- Aucun élément ne sort de sa diapositive ni ne passe sous le pied de page ; aucun texte ne chevauche un autre (contrôle automatique sur les 1 920 × 1 080 pixels de chaque diapositive).")
w("- Lisibilité : police d'au moins 14 px en présentation plein écran et 11 px sur téléphone ; contraste du texte d'au moins 4,5:1 (norme WCAG AA).")
w("- Téléphone (390 px) : pas de défilement horizontal, tableaux et graphiques larges défilent dans leur propre cadre.")
w("- PDF : polices embarquées, une diapositive par page, planche contact relue.")
open(os.path.join(HERE, "RAPPORT.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

ligne = (f"| {D['date']} | [Formation : le stock picking GARP, de zéro à autonome]({DOSSIER}/RAPPORT.md) | "
         f"Diaporama de {len(PLAN)} diapositives pour débutant (objectifs et horizon, DCA, comptes, valorisation, PEG, grille GARP, PEA, compte-titres, assurance-vie, ETF, grands investisseurs), "
         f"avec calculatrice : {eur(D['defauts']['capital'])} + {eur(D['defauts']['mensuel'])}/mois sur {fr(D['defauts']['annees'], 0)} ans à {fr(D['defauts']['rendement'] * 100, 0)} % brut "
         f"donnent {eur(env['PEA']['net'])} nets en PEA contre {eur(env['CTO']['net'])} sur un compte-titres ; {pct(fx[2]['frais'], 0)} de frais par an coûtent {pct(fx[2]['part_perdue'], 0)} du capital en 30 ans "
         f"· [PDF]({DOSSIER}/Formation_GARP_2026-10-13.pdf)" + (f" · [en ligne]({lien})" if lien else "") + " |")
readme = os.path.join(RACINE, "README.md")
lignes = open(readme, encoding="utf-8").read().split("\n")
idx = [i for i, l in enumerate(lignes) if l.startswith(f"| {D['date']} | [Formation")]
if idx:
    lignes[idx[0]] = ligne
else:
    dernier = max(i for i, l in enumerate(lignes) if l.startswith("| ") and "/" in l[:14])
    lignes.insert(dernier + 1, ligne)
open(readme, "w", encoding="utf-8").write("\n".join(lignes))
print("RAPPORT.md écrit ; README.md : ligne du", D["date"], "à jour")
