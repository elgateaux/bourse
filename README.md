# bourse

Analyses boursières reproductibles : chaque screen vit dans `screens/<date>_<sujet>/` avec
son rapport (`RAPPORT.md`), le script de calcul (`screen.py`, bibliothèque standard Python
uniquement), les données brutes utilisées (`data/`) et les résultats (`resultats.csv`).

| Date | Screen | Conclusion |
|---|---|---|
| 30/09/2026 | [Qualité des bénéfices — tech mondiale](screens/2026-09-30_qualite-benefices_tech-mondiale/RAPPORT.md) | GoDaddy (GDDY) : meilleur compromis qualité des bénéfices / FCF / valorisation sur 126 valeurs tech de 17 pays ; Adobe en alternative grande capitalisation |
| 30/09/2026 | [Portefeuille PEG pour battre le Nasdaq 100 (3 valeurs)](screens/2026-09-30_portefeuille-peg_nasdaq100/RAPPORT.md) | Nu Holdings, Broadcom, Rheinmetall à un tiers chacun : P/E 12 mois de 16 contre 22 pour l'indice, même croissance du BPA 2027 (+40 %), rendement espéré modélisé de 25,8 %/an contre 10,0 % ; deep dives, prospectus d'Anthropic, rachat de Monzo chiffré (Nu reste en portefeuille), Adyen examiné (variante prudente, entrée sous ~685 €), critique · PDF : [rapport](screens/2026-09-30_portefeuille-peg_nasdaq100/Portefeuille_PEG_Nasdaq100_rapport.pdf), [présentation](screens/2026-09-30_portefeuille-peg_nasdaq100/Portefeuille_PEG_Nasdaq100_presentation.pdf) |
| 01/10/2026 | [Article : Nu, Rheinmetall, NVIDIA, TSMC](screens/2026-09-30_portefeuille-peg_nasdaq100/Article_PEG_Nu_Rheinmetall_NVIDIA_TSMC.pdf) | Broadcom remplacé par NVIDIA et TSMC (1/6 chacun) : P/E 12 mois de 15,9 contre 22,2, rendement espéré modélisé de 24,1 %/an contre 10,0 % (25,8 % avec Broadcom) ; dossier Reddit (candidat le plus proche) · source : [ARTICLE.html](screens/2026-09-30_portefeuille-peg_nasdaq100/ARTICLE.html) |
| 01/10/2026 | [Bilan : Nu, Rheinmetall, TSMC, Uber, NVIDIA](screens/2026-09-30_portefeuille-peg_nasdaq100/Bilan_portefeuille_PEG_2026-10-01.pdf) | Portefeuille à cinq lignes (Nu 30 %, Rheinmetall 30 %, TSMC 15 %, Uber 15 %, NVIDIA 10 %) : P/E 12 mois de 15,9 contre 22,2, rendement espéré modélisé de 24,2 %/an contre 10,0 % ; Uber réduit le principal risque (Nu et Rheinmetall en échec ensemble : 7,1 %/an au lieu de 4,1 %) ; puces conçues par l'IA, mémoire, ETF Nasdaq 100, small caps européennes et Asie examinés ; Oracle, Grab, Advantest et SK Hynix ajoutés au screen · source : [BILAN.html](screens/2026-09-30_portefeuille-peg_nasdaq100/BILAN.html) |

Prompt réutilisable pour refaire la démarche : [portefeuille concentré de 3 valeurs, méthode PEG](prompts/portefeuille-peg-3-valeurs.md) ([PDF](prompts/portefeuille-peg-3-valeurs.pdf)).

Standard des prochaines recherches : le [cahier des charges de l'enquête longue](prompts/cahier-des-charges-enquete.md). Il fixe le plan de l'article, un chapitre en huit parties par valeur, les règles de preuve et les contrôles. Il s'accompagne des dossiers de recherche par valeur ([research/](research/README.md)), des outils de mise en page ([outils/](outils/README.md)) et des consignes de [CLAUDE.md](CLAUDE.md).

Article de référence de ce standard : [« Cinq valeurs pour battre le Nasdaq 100 »](prompts/article-de-reference_enquete-longue_2026-10-01.pdf) (titre de journal fictif, 31 pages, 01/10/2026). Il sert de modèle pour la forme et la méthode. Ses chiffres viennent d'un autre univers (159 valeurs) et d'autres hypothèses que le modèle du dépôt, et les dossiers `research/` qu'il cite n'y figurent pas.

Ces analyses sont quantitatives et datées ; elles ne constituent pas un conseil en investissement.
