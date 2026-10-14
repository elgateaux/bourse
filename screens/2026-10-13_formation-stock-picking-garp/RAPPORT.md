# Formation : le stock picking GARP, de zéro à autonome

Diaporama du 13/10/2026 (cours du 12/10/2026) pour un investisseur français débutant : 84 diapositives, une calculatrice d'intérêts composés, un calculateur de PEG, un quiz de dix questions, un glossaire et des sources numérotées. Même style que la vidéo du même jour. NVIDIA, TSMC, Nu, Reddit et Adyen servent uniquement d'exemples d'analyse : le diaporama ne présente ni portefeuille ni comparaison de performance avec un indice.

*La Gazette du PEG est un titre fictif : il ne correspond à aucune publication existante. Analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé.*

## Livrables

- Version en ligne (privée tant qu'elle n'est pas partagée) : https://claude.ai/artifact/RNUsiMEr4V3eoAc7Tud62i
- [diaporama/index.html](diaporama/index.html) : la page autonome (polices embarquées, fonctionne hors ligne). Flèches du clavier pour avancer, T pour le sommaire ; mode lecture automatique sur téléphone.
- [Formation_GARP_2026-10-13.pdf](Formation_GARP_2026-10-13.pdf) : une diapositive par page A4 paysage, rendue par Chromium et Playwright.
- [planche_contact.jpg](planche_contact.jpg) : toutes les pages du PDF en vignettes.

## Plan

| Chapitre | Diapositives |
|---|---|
| Ouverture | 1 à 3 |
| Objectifs et horizon | 4 à 10 |
| Les bases | 11 à 15 |
| Lire les comptes | 16 à 28 |
| Valoriser | 29 à 36 |
| La méthode GARP | 37 à 45 |
| Enveloppes, frais et impôts | 46 à 52 |
| Les ETF | 53 à 59 |
| Intérêts composés | 60 à 65 |
| Grands investisseurs | 66 à 73 |
| Passer à l'action | 74 à 84 |

## Chiffres clés (tous calculés par `calcul.py`)

- **Lire les comptes.** NVIDIA, exercice 2026 : marge opérationnelle de 60,4 %, FCF de 96,7 Md$, ROIC de 149,8 %. TSMC, 2025 : capex de 33,4 % du chiffre d'affaires, contre 2,8 % pour NVIDIA. Reddit : +5,8 % d'actions en un an.
- **Valoriser.** Cinq P/E pour le même cours de NVIDIA, de 14,6 à 47,4. Son PEG tombe à 0,30 avec la croissance de pic attendue pour 2027, mais vaut 1,10 avec une croissance durable de 15 % (hyp.).
- **Enveloppes.** 10 000 € puis 300 € par mois, 20 ans, 8 % brut, 0,5 % de frais : 180 180 € nets dans un PEA, 173 167 € en assurance-vie, 164 741 € sur un compte-titres.
- **Frais.** Sur 30 ans, 2 % de frais par an coûtent 35,2 % du capital final ; 0,2 % en coûtent 4,3 %. Entre un ETF à 0,07 % et un ETF à 0,38 %, l'écart atteint 9 145 € en 20 ans au scénario par défaut.
- **DCA.** Exemple pédagogique : après une baisse puis un rebond, le DCA finit à 8 102 € contre 6 600 € ; en hausse régulière, l'investissement en une fois finit à 7 500 € contre 6 705 €. Vanguard (2023, MSCI World, 1976-2022) : l'investissement en une fois a gagné dans 68 % des cas.
- **Temps.** 200 € par mois de 25 à 65 ans : 557 978 € ; de 35 à 65 ans : 254 676 €.

## Données signalées et corrigées

- BPA 2028 de NVIDIA : 15,53 $ dans le comparateur Zacks, 15,33 $ sur la fiche Zacks du même jour. La formation retient le premier, comme le modèle.
- Plus haut de 52 semaines de NVIDIA : 239,24 $ dans le comparateur Zacks, un autre chiffre sur la fiche. Le comparateur est utilisé pour les cinq valeurs.
- « À court terme le marché est une machine à voter… » : formule de Buffett résumant Graham, souvent prêtée à Graham. « Huitième merveille du monde » : citation apocryphe d'Einstein (Quote Investigator).
- Frais courants des ETF : plusieurs sources se contredisent.
  - Amundi PEA S&P 500 UCITS ETF (PSP5) : 0,12 % affiché par Fortuneo ; encours au 30/06/2026 selon le reporting Amundi.
  - Amundi MSCI World UCITS ETF (CW8) : 0,28 % sur une page Fortuneo, sans doute obsolète.
  - iShares MSCI World Swap PEA UCITS ETF (WPEA) : 0,25 % au lancement ; 0,20 % sur la page de l'émetteur (avril 2026).
  - Amundi PEA Emergent (MSCI Emerging) ESG Transition UCITS ETF (PAEEM) : frais de 0,20 % à 0,30 % selon les sources : vérifier le DIC ; indice émergent avec filtres ESG et climat depuis 2023.
  - Vanguard FTSE All-World UCITS ETF (Acc) (VWCE) : frais de 0,14 % à 0,22 % selon les sources : vérifier le DIC de Vanguard ; environ 3 700 lignes.
  - iShares Nasdaq 100 UCITS ETF (CNDX / CSNDX) : 0,33 % chez un agrégateur ; encours de 23,5 à 26,3 Md€.
- Part des périodes de perte du S&P 500 par horizon : les pourcentages dépendent de la base de données (Dimensional 1926-2017 pour 1, 5 et 10 ans ; Ben Carlson pour 20 ans).
- Inflation de septembre 2026 : estimation provisoire de l'Insee (3,0 %), chiffre définitif attendu le 15/10/2026.
- Retenue à la source de Taïwan sur les dividendes de TSMC : sources contradictoires, à vérifier auprès du courtier.
- Accès aux sources : les pages de première main (AMF, Oaktree, Quote Investigator, émetteurs d'ETF) étaient inaccessibles depuis l'environnement de calcul (DNS ou proxy). Les chiffres ont été recoupés par la recherche web et par Zacks ; [Bigdata.com](https://bigdata.com) n'a pas pu être utilisé (crédits épuisés).

## Hypothèses

Toutes les hypothèses éditoriales sont marquées « hyp. » et justifiées ligne par ligne dans [data/hypotheses.csv](data/hypotheses.csv) : valeurs par défaut de la calculatrice (rendement de 8 % brut par an), seuils de la grille GARP, noyau de 50 à 80 %, exemples pédagogiques (formule cours = BPA × P/E, DCA).

## Calculatrice

Capitalisation mensuelle ; frais prélevés sur l'encours ; versement en fin de mois ; impôt d'un retrait total en fin de période :
- PEA : 18,6 % de prélèvements sociaux après 5 ans, 31,4 % avant ;
- compte-titres : 31,4 % ;
- assurance-vie, avant 8 ans : 30,0 % ;
- assurance-vie, après 8 ans : 17,2 % de prélèvements sociaux, plus 7,5 % d'impôt au-delà de l'abattement (4 600 € ou 9 200 €), et 12,8 % pour la part des primes au-delà de 150 000 €.

Les dividendes ne sont pas modélisés. Le JavaScript est la traduction ligne à ligne de `simuler()` dans `calcul.py` : `verifier.js` le confronte aux 8 cas de [calculatrice_tests.csv](calculatrice_tests.csv), avec un écart maximal inférieur au centime.

## Reproduire

```sh
cd screens/2026-10-13_formation-stock-picking-garp
python3 calcul.py                       # ratios, valorisation, grille, frais, enveloppes, tests -> CSV et diaporama/donnees_formation.json
python3 build_slides.py                 # diaporama/index.html (ajouter --fragment CHEMIN pour la version Artifact)
NODE_PATH=$(npm root -g) node verifier.js /tmp/captures   # captures, débordements, chevauchements, lisibilité, calculatrice, téléphone
NODE_PATH=$(npm root -g) node pdf.js "$PWD/Formation_GARP_2026-10-13.pdf"
python3 planche_contact.py && python3 rapport.py
```

Données d'entrée dans [data/](data/) : comptes annuels et consensus Zacks, résultats trimestriels de Nu, Reddit et Adyen, fiscalité 2026, citations, ETF, horizon et DCA, chacune avec deux sources par chiffre clé. Les P/E NTM, croissances supposées, scénarios et zones d'achat par société viennent du modèle PEG du dépôt, daté du même jour.

## Contrôles avant livraison

- Aucun élément ne sort de sa diapositive ni ne passe sous le pied de page ; aucun texte ne chevauche un autre (contrôle automatique sur les 1 920 × 1 080 pixels de chaque diapositive).
- Lisibilité : police d'au moins 14 px en présentation plein écran et 11 px sur téléphone ; contraste du texte d'au moins 4,5:1 (norme WCAG AA).
- Téléphone (390 px) : pas de défilement horizontal, tableaux et graphiques larges défilent dans leur propre cadre.
- PDF : polices embarquées, une diapositive par page, planche contact relue.
