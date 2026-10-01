# Cahier des charges : l'enquête longue sur un portefeuille PEG

Ce document fixe le standard des prochaines recherches du dépôt. Il reprend la structure, la profondeur et les règles de preuve de l'article « Cinq valeurs pour battre le Nasdaq 100 : l'enquête complète sur un portefeuille PEG » (*La Gazette du PEG*, titre fictif, 31 pages), fourni comme modèle le 1er octobre 2026 : [PDF de l'article de référence](article-de-reference_enquete-longue_2026-10-01.pdf).

On en garde la méthode, pas les chiffres. L'article part d'un univers de 159 valeurs et d'hypothèses qui ne sont pas celles du modèle du dépôt (47 valeurs au 1er octobre 2026). Ses conclusions ne remplacent donc pas celles du [bilan du 1er octobre 2026](../screens/2026-09-30_portefeuille-peg_nasdaq100/BILAN.html) sans être recalculées. Ces conclusions sont Broadcom plutôt que NVIDIA, et les poids suivants : Nu 25 %, Rheinmetall, Broadcom et Uber 20 % chacun, TSMC 15 %.

La méthode de calcul est décrite dans le [prompt du portefeuille de 3 valeurs](portefeuille-peg-3-valeurs.md) : métriques de Lynch, scénarios, score, stress tests. Ce document décrit l'enquête qui l'accompagne.

## 1. Dix règles

1. **L'histoire avant les promesses.** Une entreprise se juge sur ce qu'elle a déjà fait avant de se juger sur ce qu'elle promet. Chaque valeur retenue reçoit son histoire, ses huit derniers exercices et ses chutes de Bourse avant toute projection.
2. **Chaque fait daté a sa source.**
   - Une date, un montant ou une citation renvoie à une référence numérotée dans le dossier de la valeur sous `research/`. La référence donne le titre, l'éditeur, la date et l'URL.
   - Les dossiers cités sont versionnés dans le dépôt avec l'article.
3. **Aucun chiffre recopié à la main.** Valorisation, scénarios, stress tests, mais aussi les huit ans de chiffres : tout passe par un CSV. Les tableaux et graphiques de l'article sont générés par script.
4. **Deux sources par chiffre clé.** Consensus, BPA réalisé, cours : au moins deux sources. L'écart est écrit quand il existe, par exemple « deux compilations divergent de 4 € sur 2026 ».
5. **Des hypothèses sous le consensus, montrées une par une.**
   - Pour chaque ligne : la croissance retenue face au consensus, la raison de l'écart, le plafond de P/E de sortie et sa raison.
   - On publie aussi le résultat à multiples constants.
6. **L'ours a la parole.**
   - Le cas baissier est écrit avec ses meilleurs arguments, chiffrés et datés, et avec l'objectif de cours des baissiers.
   - Suivent notre réponse, la probabilité que l'ours ait tort et ce qui nous ferait changer d'avis.
7. **Des règles de vente mesurables.**
   - Chaque règle fixe un indicateur, un seuil et une durée. Exemple : « créances à plus de 90 jours au-dessus de 7,5 % deux trimestres de suite ».
   - Jamais « si la thèse se dégrade ».
8. **Le rendement net de l'investisseur.** Pour chaque ligne :
   - la cotation à acheter ;
   - l'éligibilité au PEA ;
   - le dividende et sa retenue à la source ;
   - l'exposition de change ;
   - la ligne à éviter, un ADR non sponsorisé par exemple.
9. **Les dirigeants dans le texte.**
   - Leurs phrases sont citées en langue originale, avec la traduction, le nom, la fonction, l'occasion et la date.
   - Leurs achats et ventes d'actions sont donnés avec leurs dates et leurs montants.
10. **Dire ce que le modèle ne voit pas.** Une crise à Taïwan, un krach général comme en 2022, le change : on l'écrit au lieu de le noyer dans une moyenne.

## 2. Le plan de l'article

L'article compte treize sections pour cinq valeurs et onze pour trois, précédées de la une. Les titres disent quelque chose : « Uber : la place de marché que le robotaxi est censé tuer », plutôt que « Uber : analyse ».

- **La une.**
  - Le bandeau du titre fictif et son avertissement.
  - Un titre qui énonce la thèse.
  - Un sommaire numéroté avec liens.
  - Un chapeau de quatre ou cinq phrases. Il contient les noms, le critère de Lynch en une phrase, le P/E du portefeuille et celui de l'indice, et les deux rendements espérés. Il annonce aussi ce que l'article apporte : « voici pourquoi, ce qui peut mal tourner, et à quel prix nous achèterions ce que nous avons écarté ».
- **En bref.**
  - Quatre puces, toujours les mêmes :
    - *Le pari* : croissance du BPA au consensus, P/E et PEG long terme, portefeuille contre indice ;
    - *Le rendement* : espéré, central, pessimiste et optimiste, pour le portefeuille puis pour l'indice, avec la phrase « 100 investis deviennent X contre Y » ;
    - *Le risque* : le double choc et la probabilité de finir sous l'indice ;
    - *Ce que nous n'achetons pas*, en une phrase.
  - Le tableau récapitulatif, avec une ligne portefeuille et une ligne indice. Ses colonnes :
    - valeur, thème, poids, cours ;
    - P/E 12 mois, croissance du BPA N+1 ;
    - PEG long terme.
  - Le graphique des fourchettes : pour chaque ligne, le portefeuille et l'indice, une barre va du scénario pessimiste à l'optimiste et un point marque le central.
- **Pourquoi ces cinq-là.**
  - Le contexte chiffré de l'indice :
    - sa performance depuis janvier et son P/E ;
    - sa part d'IA ;
    - la part de ses bénéfices qui vient de cycliques au sommet.
  - La stratégie en une phrase : des bénéfices qui croissent aussi vite que ceux de l'indice, payés moins cher.
  - L'univers : le nombre de valeurs, les continents, les sources.
  - Le PEG expliqué, puis le nuage P/E contre croissance avec les droites PEG = 1 et PEG = 1,5.
  - Une phrase par valeur retenue, qui dit pourquoi le marché la paie mal.
  - La croissance retenue face au consensus, ligne par ligne, et le rendement à multiples constants.
  - Un encadré « Comment lire les chapitres ».
- **Un chapitre par valeur**, dans l'ordre des poids (gabarit en partie 3).
- **Le portefeuille face à l'indice et aux alternatives.**
  - Un tableau à trois colonnes :
    - le portefeuille ;
    - l'indice reconstitué, avec son nombre de lignes et la part du poids couverte ;
    - la variante équipondérée.
  - Ses lignes :
    - le P/E 12 mois ;
    - la croissance du BPA N+1 (consensus, pondérée) et la croissance retenue (hyp., pondérée) ;
    - le PEG long terme et le bêta ;
    - les rendements pessimiste, central, optimiste et espéré ;
    - la valeur de 100 investis en fin d'horizon.
  - Un graphique en barres : le rendement espéré et le pire cas du portefeuille, de ses variantes et de l'indice. Le pire cas est le scénario « tout en pessimiste », calculé de la même façon pour toutes les barres.
  - Un paragraphe sur les variantes testées : combien, lesquelles, pourquoi elles sont écartées. Il donne aussi l'effet d'une poche d'ETF de l'indice.
- **Les stress tests.**
  - Un tableau avec trois colonnes : le portefeuille, l'indice en central, l'écart. Ses lignes :
    - chaque ligne seule en pessimiste ;
    - le double choc des deux plus grosses lignes ;
    - le krach du thème dominant ;
    - tout en pessimiste, tout en optimiste.
  - Une phrase « Le tableau se lit ainsi ».
  - Le pire cas (tout en pessimiste), présenté comme un plancher sous nos hypothèses et non comme une prévision. On dit aussi ce qui n'y figure pas : krach général, crise géopolitique.
  - Les sensibilités à part, sous leur nom exact. Exemple : « croissance −5 points, multiples figés ».
- **Ce que nous n'achetons pas, et à quel prix nous le ferions.**
  - Le texte est rangé par famille : cycliques au sommet, belles entreprises à prix plein, piliers de l'indice, liste d'attente.
  - Pour chaque nom : la raison chiffrée, et le prix (zone de Lynch) ou l'événement qui le ferait acheter.
- **La critique : les questions qui fâchent.** Au moins huit questions numérotées :
  1. la concentration ;
  2. le poids des hypothèses, mesuré par le rendement avec 5 points de croissance en moins et des multiples figés ;
  3. les lignes corrélées (même capex, même pays) ;
  4. la conviction la plus fragile et sa probabilité ;
  5. le change, que le modèle ne compte pas (effet d'une baisse de 10 % du dollar) ;
  6. la qualité inégale des données ;
  7. la fiscalité : PEA, compte-titres, retenues à la source ;
  8. ce que le portefeuille rate si la mode continue.
- **Mode d'emploi.**
  - L'achat : en une fois dans la zone d'achat, en deux fois sinon. Les exceptions liées aux événements (élection, publication) sont précisées.
  - Les dates à surveiller.
  - Une règle de vente par ligne.
  - Le rééquilibrage :
    - une fois par an à date fixe, ou dès qu'une ligne dépasse un seuil (35 % pour cinq lignes) ;
    - vendre la moitié d'une ligne dont le PEG dépasse 2 ;
    - renforcer celle dont le PEG repasse sous 0,8 sans avoir déclenché sa règle de vente.
- **Méthode et sources.**
  - Les mots à connaître : BPA, non-GAAP, P/E, NTM, PEG.
  - Comment on calcule : scénarios, P/E de sortie, cycliques, indice reconstitué.
  - D'où viennent les chiffres, avec leurs dates.
  - Ce que ce n'est pas :
    - pas un conseil personnalisé ;
    - des scénarios qui ne sont pas des prévisions ;
    - des baisses de 30 à 50 % à accepter sur une ligne ;
    - un retard possible sur l'indice pendant un ou deux ans.
  - Où sont les sources : `research/`, `data/`, rapport complet.
  - L'avertissement du titre fictif.

## 3. Le gabarit d'un chapitre de valeur

Le titre suit la forme « Société : une accroche qui dit l'enjeu ». Exemples du modèle :
- « Nu Holdings : la banque sans agences qui gagne plus d'un milliard par trimestre » ;
- « Rheinmetall : l'arsenal de l'Europe, acheté après la chute » ;
- « TSMC : le péage de toute l'intelligence artificielle ».

Compter quatre à six pages A4 par valeur, en huit parties, toujours dans cet ordre.

1. **D'où vient [la société].** Cinq à sept paragraphes, chacun ouvert par une phrase-titre en gras (« Un étranger contre cinq banques. », « L'introduction en Bourse et la chute. ») :
   - la fondation : date, lieu, fondateurs, l'intuition de départ et le marché attaqué ;
   - la croissance et son financement : tours de table, valorisations, années de pertes ;
   - l'introduction en Bourse et la chute : prix, date, plus bas, réponse de la direction ;
   - comment elle a gagné : deux ou trois décisions et une citation datée du fondateur ;
   - les concurrents d'hier et d'aujourd'hui, chiffrés ;
   - le capital et le dirigeant :
     - les actionnaires et les droits de vote ;
     - la rémunération du dirigeant ;
     - ses achats et ventes d'actions ;
     - les dividendes et les rachats ;
   - pour finir, une phrase qui donne « la leçon de N ans d'histoire ».
2. **Huit ans de chiffres.**
   - Un tableau des huit derniers exercices. Ses colonnes :
     - chiffre d'affaires et croissance ;
     - marge opérationnelle ;
     - BPA, en précisant la norme (IFRS, GAAP ou non-GAAP) ;
     - flux de trésorerie libre.
   - Sous le tableau, deux graphiques en barres (chiffre d'affaires, BPA) et une légende de source.
   - « Ce que disent les chiffres » :
     - par combien le chiffre d'affaires a été multiplié ;
     - la trajectoire de la marge ;
     - le nombre d'actions (dilution ou rachats) ;
     - le flux de trésorerie.
   - « La Bourse » :
     - le prix d'introduction ;
     - chaque chute de plus de 40 % : dates, ampleur, cause, et ce que faisaient les bénéfices pendant ce temps ;
     - les rendements par année civile et sur trois, cinq ou dix ans ;
     - le P/E de fin d'année face au P/E actuel.
3. **Le métier aujourd'hui, et comment il gagne de l'argent.**
   - Les sources de marge, séparées par niveau de risque, « parce qu'elles n'ont pas le même risque ».
   - Deux ou trois chiffres qui rendent le modèle singulier : coût d'acquisition, ratio d'efficacité, part de marché.
   - Le dernier trimestre, avec la date du communiqué.
   - Une citation de dirigeant.
4. **Les moteurs des quatre prochaines années, et leur prix.**
   - Deux ou trois moteurs, chacun chiffré : taille, croissance, rentabilité.
   - Ce qu'ils coûtent : capex, dilution de marge.
   - Les moteurs que les chiffres ne comptent pas, nommés.
5. **Ce que le cours suppose, et ce qu'il faut croire.**
   - P/E 12 mois et N+1, croissance au consensus, PEG N+1 (Lynch voit une aubaine sous 0,5).
   - Ce que le prix suppose, en clair : « il faudrait croire que les bénéfices cessent de croître d'ici deux ans ».
   - La croissance retenue face au consensus, et pourquoi. Le plafond de P/E de sortie, et pourquoi.
   - Le rendement espéré, le cours central en fin d'horizon et la zone d'achat. Si l'on achète au-dessus de la zone, on le dit et on dit pourquoi.
   - Le tableau des scénarios, avec une ligne « Espéré (25/50/25) ». Ses colonnes :
     - croissance du BPA et P/E de sortie ;
     - BPA et cours en fin d'horizon ;
     - rendement annuel.
6. **Pourquoi nous y croyons.** Trois raisons, dans l'ordre. Si une concurrente a été écartée, « pourquoi X plutôt que Y », en trois raisons.
7. **Le cas de l'ours.**
   - Ses meilleurs arguments, chiffrés et datés, avec l'objectif de cours des baissiers. Il peut y avoir plusieurs ours (le cycle, la géopolitique).
   - Notre réponse.
   - La probabilité que l'ours ait tort. C'est un jugement, pas un calcul : il est justifié dans le deep dive et pèse sur le poids de la ligne.
   - Ce qui nous ferait changer d'avis, dans un sens ou dans l'autre.
8. **Règles de vente, calendrier, fiscalité.**
   - Trois à six règles de vente mesurables.
   - Les dates à surveiller : publications, élections, journées investisseurs, décisions réglementaires.
   - La cotation à acheter : place, devise, ratio d'ADR.
   - L'éligibilité au PEA, avec sa raison.
   - Le dividende et sa retenue à la source : taux, part créditable.
   - L'exposition de change : devise de cotation, devises des revenus.
   - La ligne à éviter.
   - Le remplaçant désigné si la ligne est vendue.

## 4. Les dossiers de recherche

Avant d'écrire, chaque fait est rangé dans `research/`. Les modèles et les règles sont dans [research/README.md](../research/README.md).
- `research/histoire/TICKER.md` : histoire, chronologie, huit ans de chiffres, Bourse, capital et dirigeants.
- `research/deepdives/TICKER.md` : derniers résultats, consensus, moteurs, hypothèses, ours, règles de vente, calendrier, fiscalité.
- `research/megatrends/megatrends.json` : les méga-tendances, leurs goulots et qui capte la valeur.

Les dossiers sont mis à jour, pas dupliqués : chaque mise à jour ajoute une ligne datée à leur journal. Les huit ans de chiffres vont aussi dans le fichier `data/historique.csv` de l'analyse, d'où l'article tire ses tableaux et graphiques.

Chaque valeur retenue a ses deux dossiers. Chaque valeur de la liste d'attente a au moins son deep dive.

## 5. Tableaux, graphiques et mise en page

- La mise en page reste celle des articles du dépôt ([BILAN.html](../screens/2026-09-30_portefeuille-peg_nasdaq100/BILAN.html)) : thèmes clair et sombre, lecture sur mobile, PDF A4. Le modèle de référence apporte le plan et la profondeur, pas le dessin.
- Le générateur du bilan, dans [outils/](../outils/README.md), sert de point de départ : feuille de style, graphiques SVG tirés des CSV, rendu PDF, contrôles de débordement.
- Figures obligatoires :
  - les fourchettes de scénarios (En bref) ;
  - le nuage P/E contre croissance avec les droites PEG = 1 et PEG = 1,5 (Pourquoi ces cinq-là) ;
  - pour chaque valeur, le tableau des huit ans, deux graphiques en barres (chiffre d'affaires, BPA) et le tableau des scénarios ;
  - le tableau face à l'indice et les barres du rendement espéré et du pire cas ;
  - le tableau des stress tests.
- Chaque figure a une légende de source. Exemples :
  - « — calculs du modèle portefeuille.py, 1er octobre 2026 » ;
  - « Historique NU — rapports annuels et communiqués cités dans research/histoire/NU.md ».
- Le format est français partout, y compris dans les tableaux de scénarios :
  - 8,0 % et non 8.0 % ;
  - 1 234,5 $ ;
  - le signe moins « − » ;
  - les unités Md$, M€, Md NT$.
- Aucune table ni légende n'est coupée en PDF. Une table trop large passe en police réduite ou en deux tables. À l'écran, seule la table défile, jamais la page.

## 6. Ce que le modèle doit calculer en plus

À ajouter à `portefeuille.py` lors de la prochaine recherche :
- le bêta pondéré du portefeuille et de l'indice ;
- la valeur de 100 investis en fin d'horizon ;
- un pire cas défini une fois (par défaut, tout en pessimiste), et calculé de la même façon pour le portefeuille, chaque variante et l'indice ;
- la recherche exhaustive des combinaisons parmi les premières du classement, en plus des variantes nommées (le modèle de référence a testé les 1 287 quintets possibles parmi 13 valeurs) ;
- pour chaque valeur, un indicateur « achetée au-dessus de sa zone d'achat » ;
- les signaux de rééquilibrage : ligne au-dessus du seuil, PEG au-dessus de 2, PEG sous 0,8 ;
- un univers élargi de 47 à environ 150 valeurs sur quatre continents, avec des cotations européennes et asiatiques (Taïwan, Hong Kong, Shenzhen).

## 7. Les défauts du modèle de référence à ne pas reproduire

- **Des tables coupées dans le PDF**, avec une barre de défilement imprimée. Trois cas :
  - la colonne « Flux de trésorerie libre » des huit ans de chiffres ;
  - la colonne « Portefeuille équipondéré » de la comparaison ;
  - la légende du graphique des pires cas.
- **Des décimales à point** (8.0 %) dans les tableaux de scénarios.
- **Une colonne de comparaison presque vide.** La variante équipondérée n'a que des tirets pour le P/E, la croissance, le PEG et le bêta : on la remplit ou on la retire.
- **Un « pire cas » qui ne mesure pas la même chose d'une barre à l'autre.**
  - Celui du portefeuille (+2,6 %, croissance −5 points et multiples figés) est meilleur que son scénario « tout en pessimiste » (−4,2 %). Ce n'est donc pas un plancher, contrairement à ce qu'écrit l'article.
  - Celui de l'indice (−11,8 %) est son scénario pessimiste.
- **Des dossiers cités qui ne figurent pas dans le dépôt.** L'article renvoie à `research/histoire/` et à `research/deepdives/`, absents du dépôt elgateaux/bourse : le lecteur ne peut rien vérifier.

## 8. Contrôles avant publication

- Dix faits datés pris au hasard retrouvent leur source dans `research/`.
- Aucun nombre n'est saisi à la main dans le gabarit de l'article. Tous viennent des CSV, avec les mêmes arrondis dans l'article et dans le rapport.
- Les rendements et les pires cas comparés sont calculés de la même façon pour toutes les colonnes.
- La planche contact de toutes les pages du PDF est relue : aucune table coupée, aucun titre orphelin en bas de page, polices chargées.
- Les données Zacks sont datées et accompagnées de leur lien. Bigdata.com est écrit ainsi, avec un lien vers https://bigdata.com.
- L'avertissement du titre fictif figure en haut et en bas de l'article.
- Le README a sa ligne : date, lien, conclusion chiffrée.
