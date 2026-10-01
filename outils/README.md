# Outils de mise en page

Ces scripts produisent les articles et les PDF du dépôt à partir des CSV du modèle. Ils servent de point de départ aux prochaines enquêtes : feuille de style des articles (thèmes clair et sombre, mobile, impression A4), graphiques SVG générés depuis les données, rendu PDF et contrôles.

| Dossier | Ce qu'il produit |
|---|---|
| `bilan/` | `BILAN.html` du 1er octobre 2026 et son PDF ; reproduit l'article à l'octet près |
| `article/` | `template.html`, dont le bilan reprend les polices et la feuille de style |
| `prompt_pdf/` | le PDF du prompt `prompts/portefeuille-peg-3-valeurs.md` |

## Commandes

Depuis la racine du dépôt, avec `S=screens/2026-09-30_portefeuille-peg_nasdaq100` et un dossier de travail `T` hors du dépôt :

```sh
# Article : les chiffres viennent des CSV de sortie de portefeuille.py, importé depuis $S
python3 outils/bilan/build_bilan.py "$S" "$S/BILAN.html"

# Pages d'aperçu et d'impression, captures de contrôle (bureau, mobile, sombre), puis PDF A4
sh outils/bilan/emballer.sh "$S" "$T"
NODE_PATH=$(npm root -g) node outils/bilan/check.js "$T"
NODE_PATH=$(npm root -g) node outils/bilan/pdf.js "$T" "$S/Bilan_portefeuille_PEG_2026-10-01.pdf"

# Prompt en PDF
python3 outils/prompt_pdf/build.py prompts/portefeuille-peg-3-valeurs.md "$T/prompt.html"
NODE_PATH=$(npm root -g) node outils/prompt_pdf/pdf.js "$T/prompt.html" prompts/portefeuille-peg-3-valeurs.pdf
```

`check.js` signale tout élément qui dépasse la largeur de la page et vérifie que les polices sont chargées. Avant de livrer un PDF, relire aussi une planche contact de toutes ses pages.

## Dépendances

- Python 3. Le bilan n'utilise que la bibliothèque standard ; le prompt demande en plus le paquet `markdown`.
- Node avec `playwright` et Chromium, préinstallés dans l'environnement de Claude Code sur le web.
- Les polices Archivo, Newsreader et IBM Plex Mono, chargées depuis Google Fonts.
