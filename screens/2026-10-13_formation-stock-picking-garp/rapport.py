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
IM = {k: float(v["valeur"]) for k, v in D["immo_data"].items() if v["valeur"]}
immo, dcf, chg, per = D["immo"], D["dcf"], D["change"], D["per"]
NQ = open(os.path.join(HERE, "diaporama", "index.html"), encoding="utf-8").read().count('class="card qz-q')

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
  f"un calculateur de PEG, un quiz de {NQ} questions, un glossaire et des sources numérotées. Même style que la vidéo du même jour. "
  "Conçu comme une « bible » de l'investisseur français : moat, DCF, taux, change, PER, déclaration fiscale, ordres de Bourse, arnaques, "
  "comparaison Bourse-immobilier et stratégies de quinze grands investisseurs. "
  "NVIDIA, TSMC, Nu, Reddit et Adyen servent uniquement d'exemples d'analyse : le diaporama ne présente ni portefeuille ni comparaison de performance avec un indice.")
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
w(f"- [Formation_GARP_L-essentiel_2026-10-13.pdf](Formation_GARP_L-essentiel_2026-10-13.pdf) : le parcours « L'essentiel », {sum(1 for x in PLAN if x.get('niv') == 'e')} diapositives, "
  "avec une page « À retenir » par chapitre. Dans le diaporama, la touche E ou le bouton « Parcours » bascule entre l'essentiel et le complet.")
w("- [AUDIT_DONNEES.md](AUDIT_DONNEES.md) : audit des données (`audit.py`) : chaque ligne des CSV utilisée dans le document, ou la raison de son absence.")
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
  f"Son PEG tombe à {fr(V['NVDA']['peg_2027'], 2)} avec la croissance de pic attendue pour 2027, mais vaut {fr(V['NVDA']['peg_lt'], 2)} avec une croissance durable de {pct(V['NVDA']['croissance_retenue'], 0)} (hyp.).")
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
w(f"- **Moat.** TSMC détient {fr(float(D['moat']['tsm_part_fonderie']['valeur']), 1)} % de la fonderie mondiale. Intel montre l'érosion : marge brute de "
  f"{pct(D['hist']['INTC'][0]['taux_mb'], 0)} en {D['hist']['INTC'][0]['exercice']}, puis perte nette de {fr(-float(D['moat']['intel_perte_2024']['valeur']), 1)} Md$ en 2024.")
w(f"- **DCF et taux.** Exemple pédagogique : {fr(dcf['bas']['valeur'], 0)} M€ de valeur à {pct(dcf['bas']['taux'], 0)}, {fr(dcf['haut']['valeur'], 0)} M€ à {pct(dcf['haut']['taux'], 0)} "
  f"({pct(dcf['variation'], 1, True)}) ; la valeur terminale pèse {pct(dcf['bas']['part_vt'], 0)} de la valeur.")
w(f"- **Change et PER.** Avec un euro en hausse de {pct(chg['hausse_euro'], 0)}, une action américaine stable en dollars perd {pct(-chg['perte_euro'])} en euros. "
  f"Plafond du PER en 2026 : {eur(per['plafond_max'])} ; {eur(per['versement'])} versés à {pct(per['tmi'], 0)} de tranche marginale économisent {eur(per['economie'])} d'impôt (hyp.).")
w(f"- **Bourse ou immobilier.** IEIF, 1983-2023 : {fr(IM['ieif_actions_40'], 1)} % par an pour les actions françaises, {fr(IM['ieif_paris_40'], 1)} % pour le logement parisien ; "
  f"sur 2008-2023, {fr(IM['ieif_actions_15'], 1)} % contre {fr(IM['ieif_paris_15'], 1)} %. Logement de {eur(immo['prix'])} (hyp.) : rendement net de {pct(immo['net']['france']['rdt_net'], 2)} "
  f"({pct(immo['net']['paris']['rdt_net'], 2)} à Paris), effort d'épargne de {eur(immo['effort_m'])} par mois avec un crédit à {pct(immo['taux'], 2)} sur {fr(immo['mois'] / 12, 0)} ans, "
  f"apport qui varie de ±{pct(immo['effet_apport'], 0)} pour ±{pct(immo['variation'], 0)} sur le prix. Paris a perdu {fr(-IM['paris_krach_1990'], 0)} % en euros constants de 1990 à 1997.")
w(f"- **Grands investisseurs.** Huit stratégies de plus, sourcées : Dalio, Druckenmiller, Soros, Simons, Greenblatt, Templeton, Terry Smith, Nick Sleep ; "
  "classées selon qu'elles sont à la portée d'un particulier ou non.")
w("")
w("## Immobilier : ce que dit la recherche, et l'effet de levier")
w("")
ETU = D["etudes"]
LV = immo["levier"]
refs = []
def cite(i):
    r = ETU[i]
    out = []
    for t, u in ((r["source_titre"], r["source_url"]), (r["source2_titre"], r["source2_url"])):
        if (t, u) not in refs:
            refs.append((t, u))
        out.append(refs.index((t, u)) + 1)
    return "".join(f"[{n}]" for n in out)
w("Aucune méta-analyse statistique des rendements du logement n'a été trouvée. La revue de littérature la plus proche est celle de Chambers, Dimson, Ilmanen et Rintamäki (2024) " + cite("revue_2024") + ". Les études de référence :")
w("")
w("| Étude | Période, lieu | Résultat |")
w("|---|---|---|")
for i, r in ETU.items():
    if r["resultat"]:
        w(f"| {r['auteurs']} ({r['annee']}), *{r['etude']}*, {r['publication']} {cite(i)} | {r['periode']} ; {r['lieu']} | {r['resultat']} |")
w("")
w(f"Chiffres repris : logement {fr(float(ETU['jkkst_logement']['valeur']), 2)} % réels par an contre {fr(float(ETU['jkkst_actions']['valeur']), 2)} % pour les actions dans 16 pays (1870-2015), "
  f"volatilité de {fr(float(ETU['jkkst_vol_logement']['valeur']), 0)} % contre {fr(float(ETU['jkkst_vol_actions']['valeur']), 0)} % {cite('jkkst_logement')} ; "
  f"Paris {fr(float(ETU['eichholtz_paris']['valeur']), 1)} % réels nets de frais et d'impôts (1809-1943) {cite('eichholtz_paris')} ; Royaume-Uni {fr(float(ETU['chambers_residentiel']['valeur']), 1)} % réels nets (1901-1983) {cite('chambers_residentiel')}.")
w("")
b, c = LV["base"], LV["comptant"]
w(f"**Simulation à effort égal sur {fr(H['immo_duree_credit'], 0)} ans** (`simuler_immo()` dans `calcul.py`, résultats dans [immobilier_simulation.csv](immobilier_simulation.csv)). "
  f"Un logement de {eur(H['immo_prix'])} acheté avec {eur(b['apport'])} d'apport et {eur(b['emprunt'])} de crédit à {pct(immo['taux'], 2)}, loué nu au régime réel, revendu après {fr(H['immo_duree_credit'], 0)} ans ; "
  f"en face, les mêmes sommes, aux mêmes dates, dans un ETF (PEA jusqu'au plafond, puis compte-titres).")
w(f"- Cas central (prix +{fr(H['immo_hausse'], 0)} % par an, ETF à {fr(H['immo_rdt_actions'], 1)} % brut) : logement {eur(b['net_immo'])} nets (TRI {pct(b['tri_immo'], 2)}), ETF {eur(b['net_etf'])} (TRI {pct(b['tri_etf'], 2)}) ; "
  f"le même logement payé comptant rapporte {pct(c['tri_immo'], 2)} : le levier ajoute {fr((b['tri_immo'] - c['tri_immo']) * 100, 1)} point de TRI.")
w(f"- Point d'équilibre : avec l'ETF à {fr(H['immo_rdt_actions'], 1)} %, le logement gagne si son prix monte de plus de {pct(LV['hausse_equilibre'], 2)} par an pendant {fr(H['immo_duree_credit'], 0)} ans.")
w(f"- Risque : un levier de {fr(b['levier'], 1)} porte la volatilité de l'apport à environ {pct(LV['vol_levier'], 0)} au départ, contre {pct(LV['vol_actions'], 0)} pour un ETF d'actions.")
w(f"- Limites : rendements des actions et des prix supposés réguliers (pas de krach simulé) ; pas de travaux exceptionnels ni d'impayés au-delà des {fr(H['immo_charges'], 0)} % de charges ; "
  "déficit foncier reporté seulement sur les revenus fonciers (prudent : l'imputation de 10 700 € sur le revenu global est ignorée) ; frais de garantie et de dossier du crédit non comptés.")
w("")
w("**Stress tests** (`stress_tests()` dans `calcul.py`, résultats dans [stress_tests_immobilier.csv](stress_tests_immobilier.csv)) : chaque choc historique est rejoué sur le cas central, "
  "puis les hypothèses centrales reprennent. Patrimoine net à la revente, à effort égal.")
w("")
w("| Scénario | Choc | Logement à crédit | ETF | Écart | Fonds propres négatifs |")
w("|---|---|---|---|---|---|")
for x in LV["stress"]:
    w(f"| {x['scenario']} | {x['choc']} | {eur(x['net_immo'])} | {eur(x['net_etf'])} | {eur(x['ecart'])} | {x['annees_fp_negatifs']} an(s) |")
w("")
w("Lecture : le logement souffre des chocs concentrés (krach local à l'achat, impayé, travaux), l'ETF du krach juste avant la vente. "
  "À effort égal, un choc payé par le propriétaire est aussi versé dans l'ETF : il creuse l'écart sans changer la valeur du logement.")
w("")
w("Sources de cette section :")
w("")
for k, (t, u) in enumerate(refs, 1):
    w(f"{k}. [{t}]({u})")
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
w(f"- IEIF : un site attribue {fr(4.45, 2)} % par an au logement parisien sur 1984-2024 ; ce chiffre n'a pas été retrouvé dans l'étude et contredit deux sources ({fr(IM['ieif25_paris_40'], 1)} %). Il est écarté.")
w("- Baisse des prix à Paris dans les années 1990 : −36 % en euros courants (mars 1991 à mars 1998), −42 % en euros constants (Notaires, 1990-1997), −46 % en termes réels (CEPII, 1991-1997). La formation retient −42 %.")
w("- Rendement locatif brut national 2025 : 4,78 % selon Lokimo, jusqu'à 5,9 % selon d'autres études ; Paris : 4,11 % à 4,33 %. La formation retient les deux premiers chiffres de chaque fourchette.")
w("- Prélèvements sociaux 2026 : 17,2 % sur les revenus fonciers et les plus-values immobilières, mais 18,6 % sur la location meublée (LMNP) selon plusieurs sources ; à vérifier sur la déclaration.")
w("- Super-investisseurs : performances déclarées ou reconstituées, rarement auditées (Druckenmiller : chiffres du fonds repris par Bloomberg ; Medallion : 39,1 % net selon Zuckerman, d'autres estimations vont de 35,6 % à 40 % ; "
  "Nomad : 18,4 % par an selon une source, 21 % selon une autre ; Fundsmith 2025 : 0,8 % ou 0,9 % selon la part). La citation de Templeton n'a pas de source primaire retrouvée.")
w("- Accès aux sources : les pages de première main (AMF, Oaktree, Quote Investigator, émetteurs d'ETF) étaient inaccessibles depuis l'environnement de calcul (DNS ou proxy). "
  "Les chiffres ont été recoupés par la recherche web et par Zacks ; [Bigdata.com](https://bigdata.com) n'a pas pu être utilisé (crédits épuisés, puis connexion refusée par le proxy). "
  "Le 14/10/2026, les sites de l'IEIF, de l'Insee et de l'IGEDD étaient aussi inaccessibles : les chiffres immobiliers viennent de la recherche web, avec deux sources chacun.")
w("")
w("## Hypothèses")
w("")
w("Toutes les hypothèses éditoriales sont marquées « hyp. » et justifiées ligne par ligne dans [data/hypotheses.csv](data/hypotheses.csv) : valeurs par défaut de la calculatrice "
  f"(rendement de {fr(H['calc_rendement'], 0)} % brut par an), seuils de la grille GARP, noyau de "
  f"{fr(H['noyau_min'], 0)} à {fr(H['noyau_max'], 0)} %, exemples pédagogiques (formule cours = BPA × P/E, DCA, DCF, PER), et l'exemple d'investissement locatif : "
  f"logement de {eur(H['immo_prix'])}, apport de {fr(H['immo_apport'], 0)} % plus les frais, charges de {fr(H['immo_charges'], 0)} % des loyers, tranche marginale de {fr(H['tmi_exemple'], 0)} %, "
  f"hausse des prix de {fr(H['immo_hausse'], 0)} % par an, assurance emprunteur de {fr(H['immo_assurance'], 2)} %, frais de revente de {fr(H['immo_frais_vente'], 0)} %, "
  f"ETF à {fr(H['immo_rdt_actions'], 1)} % brut et {fr(H['immo_frais_etf'], 1)} % de frais.")
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
w("python3 planche_contact.py && python3 audit.py && python3 rapport.py")
w("NODE_PATH=$(npm root -g) node pdf.js \"$PWD/Formation_GARP_L-essentiel_2026-10-13.pdf\" --essentiel")
w("```")
w("")
w("Données d'entrée dans [data/](data/) : comptes annuels et consensus Zacks, résultats trimestriels de Nu, Reddit et Adyen, fiscalité 2026, citations, ETF, horizon et DCA, "
  "moat ([moat.csv](data/moat.csv)), compléments de la bible ([bible.csv](data/bible.csv)), immobilier ([immobilier.csv](data/immobilier.csv)), "
  "super-investisseurs ([super_investisseurs.csv](data/super_investisseurs.csv)), études sur l'immobilier ([etudes_immobilier.csv](data/etudes_immobilier.csv)), "
  "chacune avec deux sources par chiffre clé. Les P/E NTM, croissances supposées, scénarios et zones d'achat par société viennent du modèle PEG du dépôt, daté du même jour.")
w("")
w("## Contrôles avant livraison")
w("")
w("- Aucun élément ne sort de sa diapositive ni ne passe sous le pied de page ; aucun texte ne chevauche un autre (contrôle automatique sur les 1 920 × 1 080 pixels de chaque diapositive).")
w("- Lisibilité : police d'au moins 14 px en présentation plein écran et 11 px sur téléphone ; contraste du texte d'au moins 4,5:1 (norme WCAG AA).")
w("- Téléphone (390 px) : pas de défilement horizontal, tableaux et graphiques larges défilent dans leur propre cadre.")
w("- PDF : polices embarquées, une diapositive par page, planche contact relue.")
open(os.path.join(HERE, "RAPPORT.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

ligne = (f"| {D['date']} | [Formation : le stock picking GARP, de zéro à autonome]({DOSSIER}/RAPPORT.md) | "
         f"Diaporama « bible » de {len(PLAN)} diapositives pour débutant (horizon, DCA, comptes, moat, PEG, DCF, taux, change, grille GARP, PEA, compte-titres, assurance-vie, PER, ETF, "
         f"Bourse contre immobilier, quinze grands investisseurs, ordres, arnaques), "
         f"avec calculatrice : {eur(D['defauts']['capital'])} + {eur(D['defauts']['mensuel'])}/mois sur {fr(D['defauts']['annees'], 0)} ans à {fr(D['defauts']['rendement'] * 100, 0)} % brut "
         f"donnent {eur(env['PEA']['net'])} nets en PEA contre {eur(env['CTO']['net'])} sur un compte-titres ; {pct(fx[2]['frais'], 0)} de frais par an coûtent {pct(fx[2]['part_perdue'], 0)} du capital en 30 ans ; "
         f"IEIF sur 40 ans : {fr(IM['ieif_actions_40'], 1)} % par an pour les actions françaises contre {fr(IM['ieif_paris_40'], 1)} % pour le logement parisien ; "
         f"à effort égal sur 20 ans, logement à crédit {eur(immo['levier']['base']['net_immo'])} contre {eur(immo['levier']['base']['net_etf'])} en ETF (hyp.) "
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
