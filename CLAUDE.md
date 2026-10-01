# Consignes de recherche pour ce dépôt

Ce dépôt réunit des analyses boursières en français. Ce sont des portefeuilles concentrés, construits avec la méthode PEG de Peter Lynch pour battre le Nasdaq 100 sur trois à cinq ans.

## Avant toute nouvelle recherche

1. Lire [prompts/cahier-des-charges-enquete.md](prompts/cahier-des-charges-enquete.md). C'est le standard des articles :
   - le plan de l'enquête longue ;
   - le gabarit de chapitre par valeur ;
   - les règles de preuve ;
   - les contrôles avant publication.
2. Méthode de calcul : [prompts/portefeuille-peg-3-valeurs.md](prompts/portefeuille-peg-3-valeurs.md) et le modèle `screens/2026-09-30_portefeuille-peg_nasdaq100/portefeuille.py`. Garder les mêmes règles pour que les résultats restent comparables d'une analyse à l'autre.
3. Repartir des dossiers existants de `research/` et les mettre à jour plutôt que tout refaire.

## Ce que veut l'investisseur

- **Objectif.** La performance contre le Nasdaq 100, sur trois à cinq ans. La diversification n'est pas un but ; l'indépendance des moteurs de croissance, si.
- **Investisseur.** Résident français, en euros, avec un PEA et un compte-titres.
- **Matière.** BPA non-GAAP, méga-tendances, goulots d'étranglement (SemiAnalysis, TrendForce), déclarations des dirigeants, deep dives, critique sans complaisance.
- **Valeurs suivies, à étudier à chaque fois.** NVIDIA, Nu Holdings, Rheinmetall, Uber.
- **Style.** Celui d'un journal financier (façon Bourseko) : clair, très chiffré, phrases courtes, voix active.

## Organisation

- `screens/<date>_<sujet>/` : une analyse. On y trouve :
  - `RAPPORT.md` ;
  - le script de calcul, en Python avec la seule bibliothèque standard ;
  - `data/`, les CSV d'entrée, dont les hypothèses justifiées ligne par ligne ;
  - les CSV de sortie ;
  - les articles en HTML et en PDF.
- `research/` : faits datés et sources numérotées (voir [research/README.md](research/README.md)).
  - `histoire/TICKER.md` : histoire de chaque société ;
  - `deepdives/TICKER.md` : deep dive de chaque valeur ;
  - `megatrends/megatrends.json` : méga-tendances.
- `prompts/` : prompts réutilisables et cahier des charges.
- `outils/` : génération des articles et des PDF à partir des CSV (voir [outils/README.md](outils/README.md)). C'est le point de départ de tout nouvel article, pour garder la même mise en page.
- `README.md` : une ligne par livrable, avec la date, le lien et la conclusion chiffrée.

## Règles

- **Chiffres.**
  - Aucun chiffre inventé, aucun chiffre recopié à la main. Les données vont dans des CSV, et les tableaux et graphiques sont générés par script.
  - Toute donnée corrigée en cours de route est signalée dans les livrables.
- **Hypothèses.** Les hypothèses éditoriales sont plus prudentes que le consensus quand celui-ci extrapole un pic. Elles sont marquées « hyp. » et justifiées dans `data/hypotheses.csv`.
- **Sources.**
  - Au moins deux sources par chiffre clé.
  - Le consensus Zacks est daté et cité avec son lien. Les opinions sont présentées comme des opinions datées.
  - On écrit « Bigdata.com », avec un lien vers https://bigdata.com.
  - Si une source web est bloquée, on le dit et on passe par la recherche web, Zacks ou Bigdata.com.
- **Format.** Format français des nombres : 24,2 % ; 1 234,5 $ ; signe moins « − ».
- **Articles.**
  - Le titre de journal est fictif. Un avertissement précise qu'il ne correspond à aucune publication existante.
  - Chaque article porte la mention « analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé ».
- **PDF.**
  - Le rendu passe par Chromium et Playwright, au format A4, avec les scripts de `outils/`.
  - Les scripts de génération d'un article sont versionnés dans le dépôt avec l'article.
  - Avant de livrer, on relit une planche contact de toutes les pages : aucune table coupée, aucun titre orphelin, polices chargées.
