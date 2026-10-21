# Affiches « Caves à vendre » (21 octobre 2026)

Deux affiches A4 à imprimer, mises au propre d'après l'affiche manuscrite. Elles ont la même mise en page ; seule la ligne « sur rue » ou « sur cour » change. Le nom de famille a été retiré : il ne reste que « Merci de contacter Anne » et le numéro.

| Fichier | Contenu |
|---|---|
| `affiche_caves_sur_rue.pdf` | À vendre, caves sur rue |
| `affiche_caves_sur_cour.pdf` | À vendre, caves sur cour |

Impression : A4, à 100 % (sans « ajuster à la page »), en couleur ou en noir et blanc. Le cadre laisse 12 mm de marge, ce qui convient aux imprimantes de bureau.

## Régénérer

Le prénom, le numéro et les deux variantes sont en tête de `build.py`. Depuis la racine du dépôt :

```sh
D=affiches/2026-10-21_caves-a-vendre
python3 $D/build.py $D
NODE_PATH=$(npm root -g) node $D/pdf.js $D $D /tmp
```

`pdf.js` vérifie que la police Archivo (Google Fonts) est chargée et que rien ne déborde du cadre. Il contrôle aussi qu'aucun bloc de texte ne passe sur deux lignes et que chaque affiche tient sur une seule page. Il écrit un PNG d'aperçu de chaque affiche dans le troisième dossier.
