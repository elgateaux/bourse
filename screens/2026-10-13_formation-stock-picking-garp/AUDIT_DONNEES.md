# Audit des données de la formation

Généré par `audit.py`. Une ligne est « utilisée » quand le diaporama l'appelle par son identifiant ou lit son fichier en entier.

| Fichier | Contenu | Lignes | Non affichées | Lecture |
|---|---|---|---|---|
| `data/adyen_s1_2026.csv` | Adyen, premier semestre 2026 | 5 | 0 | lignes appelées une à une par leur identifiant |
| `data/bible.csv` | PER, déclaration, ordres, indices, change, arnaques | 19 | 0 | lignes appelées une à une par leur identifiant |
| `data/categories_lynch.csv` | Catégories de Lynch | 8 | 0 | six catégories de Lynch, lues en boucle |
| `data/comptes_annuels.csv` | Comptes annuels (Zacks) | 4 | 0 | comptes des quatre sociétés, lus en boucle par calcul.py |
| `data/dca_exemple.csv` | Exemple de DCA | 12 | 0 | chemins de prix de l'exemple de DCA |
| `data/etf.csv` | Principaux ETF | 9 | 0 | tableau des principaux ETF, lu en boucle |
| `data/etf_regles.csv` | Règles des ETF | 7 | 0 | lignes appelées une à une par leur identifiant |
| `data/etf_us_zacks_2026-10-13.csv` | ETF américains (Zacks) | 4 | 0 | lignes appelées une à une par leur identifiant |
| `data/etudes_immobilier.csv` | Études académiques sur l'immobilier | 20 | 2 | lignes appelées une à une par leur identifiant |
| `data/fiscalite.csv` | Fiscalité et frais 2026 | 25 | 0 | lignes appelées une à une par leur identifiant |
| `data/historique_bpa.csv` | Historiques de BPA (cycliques) | 14 | 0 | historiques de Micron et d'Intel |
| `data/horizon_dca.csv` | Horizon, krachs et DCA | 18 | 0 | lignes appelées une à une par leur identifiant |
| `data/hypotheses.csv` | Hypothèses justifiées | 69 | 0 | hypothèses, toutes justifiées et chargées par calcul.py |
| `data/immobilier.csv` | Immobilier : rendements, risques, frais, fiscalité | 41 | 0 | lignes appelées une à une par leur identifiant |
| `data/investisseurs.csv` | Citations des grands investisseurs | 23 | 1 | lignes appelées une à une par leur identifiant |
| `data/moat.csv` | Moat : définitions et preuves | 12 | 0 | lignes appelées une à une par leur identifiant |
| `data/nu_t2_2026.csv` | Nu, deuxième trimestre 2026 | 4 | 0 | lignes appelées une à une par leur identifiant |
| `data/nvda_zacks_2026-10-12.csv` | NVIDIA, consensus Zacks | 11 | 1 | lignes appelées une à une par leur identifiant |
| `data/palmares_lynch.csv` | Palmarès de Peter Lynch | 5 | 0 | palmarès de Lynch |
| `data/qqq_positions_2026-09-04.csv` | Positions de QQQ | 15 | 10 | lignes appelées une à une par leur identifiant |
| `data/reddit_t2_2026.csv` | Reddit, deuxième trimestre 2026 | 5 | 0 | lignes appelées une à une par leur identifiant |
| `data/super_investisseurs.csv` | Stratégies de huit autres investisseurs | 8 | 0 | lignes appelées une à une par leur identifiant |

## Lignes non affichées, et pourquoi

- `etudes_immobilier.csv` · `senat_actions` : chiffre repris dans le texte du résultat du Sénat (6,2 %)
- `etudes_immobilier.csv` · `demers_eisfeldt` : rendement nominal américain, non comparable aux rendements réels : cité dans RAPPORT.md
- `investisseurs.csv` · `lynch_magellan` : doublon du palmarès de Lynch (palmares_lynch.csv), déjà affiché
- `nvda_zacks_2026-10-12.csv` · `pe_12_derniers_mois` : valeur de contrôle : le P/E 12 mois est recalculé (cours ÷ BPA 12 mois)
- `qqq_positions_2026-09-04.csv` · `MSFT` : le diaporama montre les 10 premières lignes de QQQ sur 15 relevées
- `qqq_positions_2026-09-04.csv` · `AMZN` : le diaporama montre les 10 premières lignes de QQQ sur 15 relevées
- `qqq_positions_2026-09-04.csv` · `AMD` : le diaporama montre les 10 premières lignes de QQQ sur 15 relevées
- `qqq_positions_2026-09-04.csv` · `GOOG` : le diaporama montre les 10 premières lignes de QQQ sur 15 relevées
- `qqq_positions_2026-09-04.csv` · `META` : le diaporama montre les 10 premières lignes de QQQ sur 15 relevées
- `qqq_positions_2026-09-04.csv` · `TSLA` : le diaporama montre les 10 premières lignes de QQQ sur 15 relevées
- `qqq_positions_2026-09-04.csv` · `AVGO` : le diaporama montre les 10 premières lignes de QQQ sur 15 relevées
- `qqq_positions_2026-09-04.csv` · `WMT` : le diaporama montre les 10 premières lignes de QQQ sur 15 relevées
- `qqq_positions_2026-09-04.csv` · `CSCO` : le diaporama montre les 10 premières lignes de QQQ sur 15 relevées
- `qqq_positions_2026-09-04.csv` · `COST` : le diaporama montre les 10 premières lignes de QQQ sur 15 relevées

## Diapositives de contenu sans source

Aucune.

Total : 338 lignes de données, 324 utilisées dans le diaporama, 14 non affichées avec raison ; 0 sans raison.
