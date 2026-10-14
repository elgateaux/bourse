# Formation : le stock picking GARP, de zéro à autonome

Diaporama du 13/10/2026 (cours du 12/10/2026) pour un investisseur français débutant : 127 diapositives, une calculatrice d'intérêts composés, un calculateur de PEG, un quiz de 16 questions, un glossaire et des sources numérotées. Même style que la vidéo du même jour. Conçu comme une « bible » de l'investisseur français : moat, DCF, taux, change, PER, déclaration fiscale, ordres de Bourse, arnaques, comparaison Bourse-immobilier et stratégies de quinze grands investisseurs. NVIDIA, TSMC, Nu, Reddit et Adyen servent uniquement d'exemples d'analyse : le diaporama ne présente ni portefeuille ni comparaison de performance avec un indice.

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
| Les bases | 11 à 16 |
| Lire les comptes | 17 à 29 |
| Le moat | 30 à 36 |
| Valoriser | 37 à 46 |
| La méthode GARP | 47 à 55 |
| Enveloppes, frais et impôts | 56 à 64 |
| Les ETF | 65 à 72 |
| Bourse ou immobilier | 73 à 88 |
| Intérêts composés | 89 à 94 |
| Grands investisseurs | 95 à 107 |
| Passer à l'action | 108 à 127 |

## Chiffres clés (tous calculés par `calcul.py`)

- **Lire les comptes.** NVIDIA, exercice 2026 : marge opérationnelle de 60,4 %, FCF de 96,7 Md$, ROIC de 149,8 %. TSMC, 2025 : capex de 33,4 % du chiffre d'affaires, contre 2,8 % pour NVIDIA. Reddit : +5,8 % d'actions en un an.
- **Valoriser.** Cinq P/E pour le même cours de NVIDIA, de 14,6 à 47,4. Son PEG tombe à 0,30 avec la croissance de pic attendue pour 2027, mais vaut 1,10 avec une croissance durable de 15 % (hyp.).
- **Enveloppes.** 10 000 € puis 300 € par mois, 20 ans, 8 % brut, 0,5 % de frais : 180 180 € nets dans un PEA, 173 167 € en assurance-vie, 164 741 € sur un compte-titres.
- **Frais.** Sur 30 ans, 2 % de frais par an coûtent 35,2 % du capital final ; 0,2 % en coûtent 4,3 %. Entre un ETF à 0,07 % et un ETF à 0,38 %, l'écart atteint 9 145 € en 20 ans au scénario par défaut.
- **DCA.** Exemple pédagogique : après une baisse puis un rebond, le DCA finit à 8 102 € contre 6 600 € ; en hausse régulière, l'investissement en une fois finit à 7 500 € contre 6 705 €. Vanguard (2023, MSCI World, 1976-2022) : l'investissement en une fois a gagné dans 68 % des cas.
- **Temps.** 200 € par mois de 25 à 65 ans : 557 978 € ; de 35 à 65 ans : 254 676 €.
- **Moat.** TSMC détient 72,5 % de la fonderie mondiale. Intel montre l'érosion : marge brute de 55 % en 2021, puis perte nette de 18,8 Md$ en 2024.
- **DCF et taux.** Exemple pédagogique : 2 311 M€ de valeur à 9 %, 1 717 M€ à 11 % (−25,7 %) ; la valeur terminale pèse 78 % de la valeur.
- **Change et PER.** Avec un euro en hausse de 13 %, une action américaine stable en dollars perd 11,5 % en euros. Plafond du PER en 2026 : 38 448 € ; 5 000 € versés à 30 % de tranche marginale économisent 1 500 € d'impôt (hyp.).
- **Bourse ou immobilier.** IEIF, 1983-2023 : 12,4 % par an pour les actions françaises, 10,4 % pour le logement parisien ; sur 2008-2023, 9,9 % contre 5,1 %. Logement de 200 000 € (hyp.) : rendement net de 1,87 % (1,60 % à Paris), effort d'épargne de 425 € par mois avec un crédit à 3,27 % sur 20 ans, apport qui varie de ±57 % pour ±10 % sur le prix. Paris a perdu 42 % en euros constants de 1990 à 1997.
- **Grands investisseurs.** Huit stratégies de plus, sourcées : Dalio, Druckenmiller, Soros, Simons, Greenblatt, Templeton, Terry Smith, Nick Sleep ; classées selon qu'elles sont à la portée d'un particulier ou non.

## Immobilier : ce que dit la recherche, et l'effet de levier

Aucune méta-analyse statistique des rendements du logement n'a été trouvée. La revue de littérature la plus proche est celle de Chambers, Dimson, Ilmanen et Rintamäki (2024) [1][2]. Les études de référence :

| Étude | Période, lieu | Résultat |
|---|---|---|
| Jordà, Knoll, Kuvshinov, Schularick, Taylor (2019), *The Rate of Return on Everything, 1870–2015*, Quarterly Journal of Economics, vol. 134 (3) [3][4] | 1870-2015 ; 16 pays avancés, dont la France | Le logement rapporte autant que les actions, environ 7 % réels par an, avec deux fois moins de volatilité. |
| Eichholtz, Korevaar, Lindenthal, Tallec (2021), *The Total Return and Risk to Residential Real Estate*, Review of Financial Studies, vol. 34 (8) [5][6] | Paris 1809-1943 ; Amsterdam 1900-1979 ; France et Pays-Bas | À Paris, le logement locatif a rapporté 4,0 % réels par an après frais et impôts, et ce rendement vient entièrement des loyers : le prix réel n'a pas progressé. |
| Chambers, Spaenjers, Steiner (2021), *The Rate of Return on Real Estate: Long-Run Micro-Level Evidence*, Review of Financial Studies, vol. 34 (8) [7][8] | 1901-1983 ; Royaume-Uni (patrimoine de quatre collèges d'Oxford et de Cambridge) | Le logement détenu par des investisseurs institutionnels a rapporté environ 2,3 % réels par an, net de frais, de 1901 à 1983. |
| Amaral, Dohmen, Kohl, Schularick (2025), *Superstar Returns? Spatial Heterogeneity in Returns to Housing*, Journal of Finance, vol. 80 (5) [9][10] | environ 150 ans ; 15 pays de l'OCDE, grandes villes et reste du pays | Dans les grandes villes, les prix montent plus vite, mais les loyers rapportent moins : le rendement total y est inférieur d'environ 1 point par an. |
| Giacoletti (2021), *Idiosyncratic Risk in Housing Markets*, Review of Financial Studies, vol. 34 (8) [11][12] | reventes répétées de logements individuels ; États-Unis | Le risque propre à chaque logement est important : un bien isolé est bien plus risqué que l'indice de son marché, ce qui réduit son ratio rendement/risque. |
| Shiller (2019), *Indice des prix des logements américains depuis 1890*, Irrational Exuberance (données mises à jour) [13][14] | 1890-2019 ; États-Unis | Après inflation, les prix des logements américains ont progressé de moins de 0,6 % par an en plus d'un siècle. |
| Sénat, commission des finances (A. de Montgolfier) (2017), *La rente immobilière : mythe et réalités*, rapport d'information n° 75 [15][16] | 1990-2015 ; France | Avant impôt, le logement locatif a rapporté environ 6 % par an de 1990 à 2015, contre 6,2 % pour les actions ; sa rentabilité récente est nettement inférieure à sa moyenne historique. |
| IGF et CGEDD (J. Friggit) (2021), *Prix, loyers et couple rendement-risque du placement en logement*, annexe de rapport, avril 2021 [17][15] | 1965-2020 ; France, Paris | Sur longue période, le couple rendement-volatilité du logement se situe entre celui des obligations et celui des actions. |
| IGF et CGEDD (2019), *Évaluation du dispositif d'aide fiscale à l'investissement locatif Pinel*, rapport, novembre 2019 [18][19] | investissement de 9 ans ; France | Dans la moitié des cas, un investissement Pinel a un rendement global net négatif après 9 ans, hors hausse des prix. |
| Chambers, Dimson, Ilmanen, Rintamäki (2024), *Long-Run Asset Returns*, Annual Review of Financial Economics, vol. 16 [1][2] | XIXe-XXIe siècles ; revue de la littérature | Revue des rendements de long terme : les mesures souffrent de biais (données faciles, survivants) et omettent souvent les revenus ; pour le logement, les transactions sont rares et les valeurs difficiles à observer. |
| Journal of Real Estate Portfolio Management et Morningstar (2023), *Investable Real Estate Allocations in a Mixed Asset Portfolio*, JRPM, vol. 30 (2) ; synthèse de Morningstar [20][21] | 45 ans ; États-Unis | Comparée à 45 études antérieures, l'immobilier améliore un portefeuille actions-obligations ; la littérature situe sa part entre 5 et 20 %. |
| Demers, Eisfeldt (2018), *Total Returns to Single Family Rentals*, NBER w21804 [22][23] | 1986-2014 ; 30 grandes métropoles américaines | Les maisons louées ont rapporté environ 8,5 % par an, comme les actions ; dans les villes chères, le rendement vient du prix, dans les villes bon marché, du loyer. |

Chiffres repris : logement 7,05 % réels par an contre 6,98 % pour les actions dans 16 pays (1870-2015), volatilité de 10 % contre 22 % [3][4] ; Paris 4,0 % réels nets de frais et d'impôts (1809-1943) [5][6] ; Royaume-Uni 2,3 % réels nets (1901-1983) [7][8].

**Simulation à effort égal sur 20 ans** (`simuler_immo()` dans `calcul.py`, résultats dans [immobilier_simulation.csv](immobilier_simulation.csv)). Un logement de 200 000 € acheté avec 35 000 € d'apport et 180 000 € de crédit à 3,27 %, loué nu au régime réel, revendu après 20 ans ; en face, les mêmes sommes, aux mêmes dates, dans un ETF (PEA jusqu'au plafond, puis compte-titres).
- Cas central (prix +2 % par an, ETF à 6,6 % brut) : logement 276 789 € nets (TRI 4,24 %), ETF 329 970 € (TRI 5,57 %) ; le même logement payé comptant rapporte 3,20 % : le levier ajoute 1,0 point de TRI.
- Point d'équilibre : avec l'ETF à 6,6 %, le logement gagne si son prix monte de plus de 3,02 % par an pendant 20 ans.
- Risque : un levier de 5,7 porte la volatilité de l'apport à environ 57 % au départ, contre 22 % pour un ETF d'actions.
- Limites : rendements des actions et des prix supposés réguliers (pas de krach simulé) ; pas de travaux exceptionnels ni d'impayés au-delà des 25 % de charges ; déficit foncier reporté seulement sur les revenus fonciers (prudent : l'imputation de 10 700 € sur le revenu global est ignorée) ; frais de garantie et de dossier du crédit non comptés.

**Stress tests** (`stress_tests()` dans `calcul.py`, résultats dans [stress_tests_immobilier.csv](stress_tests_immobilier.csv)) : chaque choc historique est rejoué sur le cas central, puis les hypothèses centrales reprennent. Patrimoine net à la revente, à effort égal.

| Scénario | Choc | Logement à crédit | ETF | Écart | Fonds propres négatifs |
|---|---|---|---|---|---|
| Cas central | aucun choc | 276 789 € | 329 970 € | −53 181 € | 0 an(s) |
| Krach immobilier « Paris 1990 » | logement −42 % réels en 7 ans dès l'achat | 163 751 € | 329 970 € | −166 219 € | 5 an(s) |
| Un an d'impayé | 12 mois sans loyer la 3e année | 276 789 € | 345 043 € | −68 254 € | 0 an(s) |
| Gros travaux | 30 000 € la 8e année (rénovation énergétique) | 276 789 € | 365 199 € | −88 410 € | 0 an(s) |
| Tempête parfaite | krach « Paris 1990 », impayé et travaux | 163 751 € | 380 152 € | −216 401 € | 5 an(s) |
| Krach « 2008 » dès le départ | ETF −56,8 % en 2 ans | 276 789 € | 258 244 € | 18 545 € | 0 an(s) |
| Krach « 2000-2003 » dès le départ | ETF −65 % en 3 ans (CAC 40) | 276 789 € | 240 777 € | 36 012 € | 0 an(s) |
| Krach « 2008 » l'année de la vente | ETF −56,8 % la 20e année | 276 789 € | 152 581 € | 124 208 € | 0 an(s) |
| Décennie perdue en Bourse | « 2000-2003 » dès le départ, puis « 2008 » les années 8 et 9 | 276 789 € | 168 480 € | 108 309 € | 0 an(s) |
| Vente forcée à 5 ans | marchés en baisse : logement −10 %, ETF −25,4 % la 5e année | 39 741 € | 59 339 € | −19 599 € | 0 an(s) |

Lecture : le logement souffre des chocs concentrés (krach local à l'achat, impayé, travaux), l'ETF du krach juste avant la vente. À effort égal, un choc payé par le propriétaire est aussi versé dans l'ETF : il creuse l'écart sans changer la valeur du logement.

Sources de cette section :

1. [Annual Reviews : Long-Run Asset Returns (2024)](https://www.annualreviews.org/content/journals/10.1146/annurev-financial-082123-105515)
2. [CEPR : Long-run asset returns, version de travail (novembre 2023)](https://cepr.org/system/files/2023-11/Long-run%20asset%20returns%20-%20Chambers%20Dimson%20Ilmanen%20Rintamaki%20-%207%20November23.pdf)
3. [NBER : The Rate of Return on Everything, 1870–2015 (w24112)](https://www.nber.org/papers/w24112)
4. [CXO Advisory : worldwide long-run returns on housing, equities, bonds and bills](https://www.cxoadvisory.com/equity-premium/worldwide-long-run-returns-on-housing-equities-bonds-and-bills/)
5. [Tinbergen Institute : The Total Return and Risk to Residential Real Estate (RFS 2021)](https://tinbergen.nl/publication/168067/the-total-return-and-risk-to-residential-real-estate)
6. [T. Lindenthal : new publication, the total return to real estate](https://www.lindenthal.eu/publications/total-return-to-real-estate/)
7. [Cambridge Judge Business School : Not as rosy (2021)](https://www.jbs.cam.ac.uk/2021/not-as-rosy/)
8. [CEPR : DP15657, The Rate of Return on Real Estate](https://cepr.org/publications/dp15657)
9. [Wiley : Journal of Finance, Superstar Returns? (2025)](https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13479)
10. [Swiss Finance Institute : Superstar Returns? Spatial Heterogeneity in Returns to Housing](https://www.sfi.ch/en/publications/superstar-returns-spatial-heterogeneity-in-returns-to-housing)
11. [SSRN : Idiosyncratic Risk in Housing Markets](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2995323)
12. [EconPapers : Idiosyncratic Risk in Housing Markets (RFS 2021)](https://econpapers.repec.org/RePEc:oup:rfinst:v:34:y:2021:i:8:p:3695-3741.)
13. [NPR : is buying a house overrated? (2019)](https://www.npr.org/sections/money/2019/04/30/718348115/is-buying-a-house-overrated)
14. [A Wealth of Common Sense : is housing a good investment? (2022)](https://awealthofcommonsense.com/2022/02/is-housing-a-good-investment/)
15. [Sénat : La rente immobilière, mythe et réalités (rapport n° 75, 2017)](https://www.senat.fr/rap/r17-075/r17-075_mono.html)
16. [Études fiscales internationales : le régime fiscal et la rentabilité des biens immobiliers (20/11/2017)](https://www.etudes-fiscales-internationales.com/archive/2017/11/19/le-regime-fiscal-et-la-rentabilite-des-biens-immobiliers-25660.html)
17. [IGEDD : prix, loyers et couple rendement-risque du placement en logement (avril 2021)](https://www.igedd.developpement-durable.gouv.fr/IMG/pdf/prix-loyer-rendement-risque_cle274d11.pdf)
18. [Vie publique : rapport IGF-CGEDD sur le dispositif Pinel (2019)](https://vie-publique.fr/files/rapport/pdf/271773_0.pdf)
19. [Boursorama : le dispositif Pinel critiqué](https://www.boursorama.com/patrimoine/actualites/le-dispositif-pinel-critique-366830cddce8ee6f942456612f2cef7b)
20. [Taylor & Francis : Investable Real Estate Allocations in a Mixed Asset Portfolio (2023)](https://www.tandfonline.com/doi/full/10.1080/10835547.2023.2247172)
21. [Morningstar : the role of real estate investments in a portfolio](https://www.morningstar.com/funds/role-real-estate-investments-portfolio)
22. [NBER : Total Returns to Single Family Rentals (w21804)](https://www.nber.org/papers/w21804)
23. [UCLA Anderson Review : single-family rentals](https://anderson-review.ucla.edu/single-family-rentals/)

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
- IEIF : un site attribue 4,45 % par an au logement parisien sur 1984-2024 ; ce chiffre n'a pas été retrouvé dans l'étude et contredit deux sources (10,1 %). Il est écarté.
- Baisse des prix à Paris dans les années 1990 : −36 % en euros courants (mars 1991 à mars 1998), −42 % en euros constants (Notaires, 1990-1997), −46 % en termes réels (CEPII, 1991-1997). La formation retient −42 %.
- Rendement locatif brut national 2025 : 4,78 % selon Lokimo, jusqu'à 5,9 % selon d'autres études ; Paris : 4,11 % à 4,33 %. La formation retient les deux premiers chiffres de chaque fourchette.
- Prélèvements sociaux 2026 : 17,2 % sur les revenus fonciers et les plus-values immobilières, mais 18,6 % sur la location meublée (LMNP) selon plusieurs sources ; à vérifier sur la déclaration.
- Super-investisseurs : performances déclarées ou reconstituées, rarement auditées (Druckenmiller : chiffres du fonds repris par Bloomberg ; Medallion : 39,1 % net selon Zuckerman, d'autres estimations vont de 35,6 % à 40 % ; Nomad : 18,4 % par an selon une source, 21 % selon une autre ; Fundsmith 2025 : 0,8 % ou 0,9 % selon la part). La citation de Templeton n'a pas de source primaire retrouvée.
- Accès aux sources : les pages de première main (AMF, Oaktree, Quote Investigator, émetteurs d'ETF) étaient inaccessibles depuis l'environnement de calcul (DNS ou proxy). Les chiffres ont été recoupés par la recherche web et par Zacks ; [Bigdata.com](https://bigdata.com) n'a pas pu être utilisé (crédits épuisés, puis connexion refusée par le proxy). Le 14/10/2026, les sites de l'IEIF, de l'Insee et de l'IGEDD étaient aussi inaccessibles : les chiffres immobiliers viennent de la recherche web, avec deux sources chacun.

## Hypothèses

Toutes les hypothèses éditoriales sont marquées « hyp. » et justifiées ligne par ligne dans [data/hypotheses.csv](data/hypotheses.csv) : valeurs par défaut de la calculatrice (rendement de 8 % brut par an), seuils de la grille GARP, noyau de 50 à 80 %, exemples pédagogiques (formule cours = BPA × P/E, DCA, DCF, PER), et l'exemple d'investissement locatif : logement de 200 000 €, apport de 10 % plus les frais, charges de 25 % des loyers, tranche marginale de 30 %, hausse des prix de 2 % par an, assurance emprunteur de 0,30 %, frais de revente de 5 %, ETF à 6,6 % brut et 0,2 % de frais.

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

Données d'entrée dans [data/](data/) : comptes annuels et consensus Zacks, résultats trimestriels de Nu, Reddit et Adyen, fiscalité 2026, citations, ETF, horizon et DCA, moat ([moat.csv](data/moat.csv)), compléments de la bible ([bible.csv](data/bible.csv)), immobilier ([immobilier.csv](data/immobilier.csv)), super-investisseurs ([super_investisseurs.csv](data/super_investisseurs.csv)), études sur l'immobilier ([etudes_immobilier.csv](data/etudes_immobilier.csv)), chacune avec deux sources par chiffre clé. Les P/E NTM, croissances supposées, scénarios et zones d'achat par société viennent du modèle PEG du dépôt, daté du même jour.

## Contrôles avant livraison

- Aucun élément ne sort de sa diapositive ni ne passe sous le pied de page ; aucun texte ne chevauche un autre (contrôle automatique sur les 1 920 × 1 080 pixels de chaque diapositive).
- Lisibilité : police d'au moins 14 px en présentation plein écran et 11 px sur téléphone ; contraste du texte d'au moins 4,5:1 (norme WCAG AA).
- Téléphone (390 px) : pas de défilement horizontal, tableaux et graphiques larges défilent dans leur propre cadre.
- PDF : polices embarquées, une diapositive par page, planche contact relue.
