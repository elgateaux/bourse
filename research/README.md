# Dossiers de recherche

Les faits datés des analyses vivent ici, avec leurs sources numérotées. Les articles et les rapports les citent ; le standard qui les exige est le [cahier des charges de l'enquête longue](../prompts/cahier-des-charges-enquete.md).

| Fichier | Contenu | Modèle |
|---|---|---|
| `histoire/TICKER.md` | histoire, chronologie, huit ans de chiffres, Bourse, capital et dirigeants | [histoire/_modele.md](histoire/_modele.md) |
| `deepdives/TICKER.md` | derniers résultats, consensus, moteurs, hypothèses, ours, règles de vente, calendrier, fiscalité | [deepdives/_modele.md](deepdives/_modele.md) |
| `megatrends/megatrends.json` | méga-tendances, goulots d'étranglement, qui capte la valeur | schéma ci-dessous |

## Règles

- **Nom des fichiers.** `TICKER` est l'identifiant de la valeur dans les CSV du modèle (`NU`, `RNMBY`, `TSM`…), pour que les scripts relient dossiers et données. La cotation à acheter est précisée dans le dossier lui-même, par exemple Rheinmetall sur Xetra en euros.
- **Sources.**
  - Chaque chiffre, date ou citation est suivi de sa référence : « 16,3 Md$ [3] ».
  - Les références sont numérotées en fin de fichier : titre, éditeur, date de publication, URL, date de consultation.
  - Les opinions (courtiers, Zacks, presse) sont attribuées et datées, jamais présentées comme des faits.
- **Deux sources par chiffre clé.** L'écart entre deux sources est noté, avec le choix retenu.
- **Mise à jour.** Un dossier se met à jour, il ne se duplique pas. La date de dernière mise à jour figure en tête, et chaque passage ajoute une ligne datée au journal en pied de fichier.
- **Données chiffrées.** Les huit ans de chiffres sont aussi saisis dans `screens/<analyse>/data/historique.csv`, d'où l'article génère ses tableaux et graphiques. Les colonnes de ce fichier :
  - ticker, exercice, devise, norme ;
  - chiffre d'affaires, marge opérationnelle, BPA, flux de trésorerie libre, nombre d'actions ;
  - source.
- **Couverture.** Chaque valeur retenue a ses deux dossiers. Chaque valeur de la liste d'attente a au moins son deep dive.

## Schéma de `megatrends/megatrends.json`

```json
{
  "date": "AAAA-MM-JJ",
  "megatendances": [
    {
      "id": "ia-calcul",
      "nom": "Calcul pour l'intelligence artificielle",
      "marche": { "taille": "…", "croissance": "…", "horizon": "…", "source": 1 },
      "goulots": ["packaging avancé", "mémoire HBM", "électricité"],
      "qui_capte_la_valeur": ["TSM", "NVDA"],
      "risques": ["…"],
      "citations": [
        { "texte": "…", "traduction": "…", "auteur": "…", "fonction": "…", "date": "AAAA-MM-JJ", "source": 2 }
      ],
      "sources": [
        { "n": 1, "titre": "…", "editeur": "…", "date": "AAAA-MM-JJ", "url": "…", "consulte": "AAAA-MM-JJ" }
      ]
    }
  ]
}
```
