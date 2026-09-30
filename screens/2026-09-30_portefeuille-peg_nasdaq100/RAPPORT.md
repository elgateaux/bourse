# Trois valeurs pour battre le Nasdaq 100 : Nu, Broadcom, Rheinmetall

*Méthode PEG de Peter Lynch, horizon 3 à 5 ans. Données arrêtées au 30/09/2026, cours de clôture du 29/09/2026. Consensus de BPA non-GAAP Zacks.*
*Document d'analyse, pas un conseil en investissement personnalisé. Les chiffres marqués « hyp. » sont des hypothèses éditoriales, modifiables dans `data/hypotheses.csv`.*

---

## En bref

**Un tiers du portefeuille pour chaque valeur, trois moteurs de croissance indépendants.**

| | Nu Holdings (NU) | Broadcom (AVGO) | Rheinmetall (RHM / RNMBY) |
|---|---|---|---|
| Méga-tendance | Banque numérique des émergents | Puces d'IA sur mesure, n° 1 des fournisseurs d'Anthropic | Réarmement européen |
| Poids | 1/3 | 1/3 | 1/3 |
| Cours (29/09/2026) | 12,35 $ | 355,10 $ | 218,29 $ (ADR) ≈ 957,65 € (Xetra) |
| P/E des 12 prochains mois | **11,3** | **19,9** | **20,2** |
| Croissance du BPA 2027 (consensus) | +35 % | +50 % | +39 % |
| PEG 2027 | 0,30 | 0,36 | 0,49 |
| PEG long terme (hyp.) | **0,51** | **0,99** | **0,92** |
| Rendement annuel espéré sur 4 ans (modèle) | 27,8 % | 23,4 % | 26,3 % |
| Scénarios bear / base / bull | 0,1 % / 30,9 % / 39,5 % | −12,8 % / 21,0 % / 44,9 % | −10,9 % / 24,4 % / 47,7 % |
| Cours implicite en 2030, scénario base | 36 $ | 761 $ | 522 $ (ADR) |
| Zone d'achat (PEG LT ≤ 1) | ≤ 24,0 $ | ≤ 358 $ | ≤ 237 $ (ADR) |

| | Portefeuille à 3 valeurs | Nasdaq 100 reconstitué | Nasdaq 100 hors mémoire |
|---|---:|---:|---:|
| P/E des 12 prochains mois | **16,0** | 22,2 | 27,4 |
| Croissance du BPA 2027 (consensus) | +40 % | +40 % | +31 % |
| PEG 2027 | **0,40** | 0,56 | 0,87 |
| PEG long terme (hyp.) | **0,74** | 2,90 | 1,96 |
| Rendement annuel espéré, 4 ans (modèle) | **25,8 %** | 10,0 % | 10,5 % |
| Scénario bear | −7,3 % | −12,3 % | −12,5 % |
| Part « infrastructure IA » | 33 % | 38 % | 32 % |

**Trois messages**

1. **Autant de croissance que l'indice, pour 28 % de moins en P/E.** Le trio offre la même croissance du BPA 2027 que le Nasdaq 100 (+40 %) pour 16 fois les bénéfices, contre 22 pour l'indice. Hors Micron et SanDisk, dont les bénéfices sont au pic du cycle, l'indice cote même 27 fois.
2. **Trois paris qui ne dépendent pas du même facteur.** Le crédit à la consommation en Amérique latine (Nu), le capex IA des laboratoires (Broadcom) et les budgets de défense européens (Rheinmetall). Une seule des trois lignes dépend de l'IA ; c'est la plus directement exposée au prospectus d'Anthropic.
3. **La concentration a un prix.** Selon les hypothèses, l'écart avec le Nasdaq 100 va de +1,5 à +15,3 points par an. Un seul stress test fait perdre le portefeuille face à l'indice : **Nu et Rheinmetall en scénario bear en même temps** (5,9 % par an contre 10,3 %). Chaque ligne vaut un tiers du portefeuille, donc chaque thèse doit être suivie de près (§9).

**Mise à jour du 30/09 : Monzo et Adyen**

- **Monzo : la baisse de Nu a déjà payé une bonne partie de la dilution.** Le 28/09, la rumeur d'un rachat de Monzo pour 8 à 10 Md£ a fait perdre 10 % à Nu, soit 6,6 Md$ de capitalisation.
  - Pire montage (tout en actions, puis décote du titre) : l'espérance de Nu tombe de 27,8 % à 19,4 % par an, celle du portefeuille de 25,8 % à 23,1 %.
  - Nu reste dans le trio. Si un rachat payé surtout en actions est annoncé et que le titre repasse au-dessus d'environ 12,5 $, on le remplace (§5.8).
- **Adyen : belle entreprise à prix correct, pas une aubaine.** PEG long terme de 1,0, 19,1 % par an espérés : Adyen est 10e du classement, derrière les trois valeurs retenues (23 à 28 %).
  - OpenAI et l'Inde sont réels, mais pèsent moins de 1 % du chiffre d'affaires à horizon 3-5 ans.
  - À la place de Broadcom, Adyen donne le trio le plus résistant des 84 testés : scénario bear à −4,6 % par an contre −7,3 %, pour 1,3 point d'espérance en moins.
  - Il entrerait dans le trio sous 685 € environ, soit un P/E de 15 (§8).
- **Rheinmetall : −52 % depuis son record, pour des raisons d'exécution plus que de demande.** Le T1 a été manqué, la frégate F126 annulée, la cible de carnet 2026 ramenée de 135 à 100-120 Md€, et les pourparlers sur l'Ukraine ont repris.
  - Rheinmetall a le PEG 2027 le plus bas des grands de la défense européenne : 0,49, contre 0,73 à 1,32 pour Leonardo, Thales et BAE.
  - Le cours actuel correspond à un objectif 2030 atteint à moitié, et le PDG achète des actions (§7).

---

## 1. Pourquoi ces trois-là, et pas les autres

Nous avons comparé les 84 combinaisons de trois valeurs possibles entre les huit meilleures du classement PEG et Adyen, ajouté à la demande. Les trios sont à poids égaux et suivent les mêmes règles de scénario (`trios.csv`).

| Trio (poids égaux) | Rendement espéré | Bear | Base | Bull | Cas pessimiste* | Nombre de valeurs IA |
|---|---:|---:|---:|---:|---:|---:|
| NU + RNMBY + CRDO | 26,5 % | −8,2 % | 26,9 % | 44,5 % | 18,4 % | 1 |
| **NU + AVGO + RNMBY** | **25,8 %** | **−7,3 %** | 25,6 % | 44,1 % | 17,0 % | 1 |
| NU + UBER + RNMBY | 25,6 % | −7,5 % | 26,6 % | 42,4 % | 16,7 % | 0 |
| NU + AVGO + CRDO | 25,6 % | −8,7 % | 25,8 % | 43,6 % | 17,7 % | 2 |
| NU + AVGO + UBER | 24,7 % | −8,0 % | 25,5 % | 41,3 % | 16,0 % | 1 |
| NU + RNMBY + ADYEY (Adyen à la place de Broadcom) | 24,5 % | **−4,6 %** | 25,0 % | 40,6 % | 16,4 % | 0 |
| NU + RNMBY + NVDA | 24,2 % | −8,1 % | 24,1 % | 42,0 % | 15,3 % | 1 |
| UBER + AVGO + RNMBY (Uber à la place de Nu) | 24,2 % | −12,3 % | 23,2 % | 44,1 % | 16,3 % | 1 |
| NU + AVGO + ADYEY (Adyen à la place de Rheinmetall) | 23,6 % | −5,1 % | 24,0 % | 39,6 % | 15,6 % | 1 |
| ADYEY + AVGO + RNMBY (Adyen à la place de Nu) | 23,0 % | −9,0 % | 21,5 % | 42,4 % | 16,0 % | 1 |
| *Nasdaq 100 reconstitué* | *10,0 %* | *−12,3 %* | *10,3 %* | *23,1 %* | *15,4 %* | |

\* Cas pessimiste : croissance de nos titres inférieure de 5 points par an, multiples constants pour tous, et bénéfices de la mémoire maintenus au pic dans l'indice.

- **Nu s'impose partout.** C'est le PEG le plus bas de l'univers (0,51), le meilleur rendement espéré et le seul scénario bear positif.
- **Broadcom plutôt que Credo.** Credo ferait gagner 0,7 point de rendement espéré, mais deux clients font 61 % de son chiffre d'affaires et son bêta est de 3,2. À un tiers du portefeuille, c'est trop. Broadcom apporte l'exposition à l'IA avec 39 Md$ de FCF annuel et six clients XPU.
- **Rheinmetall plutôt qu'Uber.** Dans le modèle, Rheinmetall bat Uber sur le rendement espéré (26,3 % contre 22,8 %), le scénario bear (−10,9 % contre −13,4 %) et le cas pessimiste. Il ajoute surtout un moteur sans aucun lien avec les deux autres.
- **NVIDIA en remplaçant.** À 17 fois les bénéfices, NVIDIA n'est pas cher, mais son PEG long terme (1,14) est le plus élevé des candidats. Le prospectus d'Anthropic montre que le deuxième laboratoire d'IA mondial achète surtout du silicium sur mesure, c'est-à-dire du Broadcom (§4).
- **Adyen, la variante prudente.** Adyen est trop cher pour entrer dans le trio sur le seul critère du rendement : 19,2 fois les bénéfices pour environ 19 % de croissance, contre 11 à 20 fois pour 20 à 22 % chez les trois retenus.
  - À la place de Broadcom, Adyen coûte 1,3 point d'espérance, mais donne le meilleur scénario bear des 84 trios. Le trio ne compte alors plus aucune valeur IA, et Rheinmetall comme Adyen sont éligibles au PEA.
  - Pour remplacer Nu, Uber rapporte plus qu'Adyen (24,2 % contre 23,0 % pour le trio). Adyen résiste mieux (bear à −9,0 % contre −12,3 %).
- **Devises et enveloppes (investisseur français).** Rheinmetall s'achète directement à Francfort (RHM) en euros et, société allemande, est éligible au PEA. Nu et Broadcom sont des actions américaines, à loger en compte-titres, avec un risque de change EUR/USD. S'y ajoute le réal brésilien pour les bénéfices de Nu.

---

## 2. Méthode

- **PEG de Lynch.** P/E divisé par la croissance du BPA. Une action est bien valorisée à PEG 1 et bon marché nettement en dessous. Le P/E est calculé sur le **BPA non-GAAP** du consensus Zacks. Il est calendarisé : les exercices décalés sont ramenés en années civiles, puis en 12 mois glissants.
- **Deux PEG.** Le *PEG 2027* utilise la croissance du consensus 2027, plafonnée à 50 %. Le *PEG LT* utilise notre hypothèse de croissance annuelle 2027-2031, plus prudente : 22 % pour Nu contre +35 % au consensus 2027, 20 % pour Broadcom contre +50 %, 22 % pour Rheinmetall contre +39 %.
- **Univers de 43 valeurs.** Les favoris (NVIDIA, Nu, Uber, Rheinmetall, Reddit, Adyen), les principaux poids du Nasdaq 100 et les goulots de l'IA. Les cycliques au pic sont exclus d'office, selon la règle de Lynch : sur un cyclique, un P/E bas annonce souvent le sommet. C'est le cas de Micron et de SanDisk.
- **Scénarios du 30/09/2026 au 30/09/2030.** Rendement = croissance du BPA × variation du multiple × dividendes.
  - **Base** : le multiple converge à mi-chemin vers un PEG compris entre 1 et 1,5.
  - **Bull** : réévaluation jusqu'à un PEG de 1 (au plus +50 %).
  - **Bear** : croissance faible et multiple compressé de 20 à 50 %.
  - Pondération 25 % / 50 % / 25 %.
  - Les mêmes règles s'appliquent au Nasdaq 100, reconstitué titre par titre : 31 valeurs, 74,2 % du poids du QQQ.
- Code : `portefeuille.py` (Python standard, sans dépendance).

---

## 3. Le contexte en quatre faits

1. **Un indice dopé par la mémoire.** Micron (5,03 % du QQQ, +537 % sur 52 semaines) et SanDisk (1,13 %, +1 442 %) pèsent 6,2 % de l'indice mais environ 25 % des bénéfices des 12 prochains mois de notre reconstitution. Micron a publié une marge brute non-GAAP de 84,9 % au dernier trimestre. Hors mémoire, le Nasdaq 100 cote 27,4 fois ses bénéfices.
2. **Des taux au plus haut depuis vingt ans.** Taux à 10 ans américain autour de 5,1 %, Brent vers 105 $ avec la guerre en Iran, et guerre tarifaire entre les États-Unis et la Chine dans son 18e mois (Zacks, 24/09/2026). Des taux élevés pénalisent d'abord les multiples élevés, ce qui plaide pour la discipline PEG.
3. **Le capex IA accélère encore.** Environ 725 Md$ d'investissements prévus par les quatre hyperscalers en 2026, relevés en juillet. Le consensus 2027 approche 1 000 Md$.
4. **Les goulots d'étranglement se déplacent.** Selon SemiAnalysis (Dylan Patel, podcast Dwarkesh, mars 2026) :
   - trois goulots structurent la course : la logique, la mémoire et l'énergie ;
   - le goulot ultime de 2028-2030 serait les machines EUV d'ASML, avec un plafond d'environ 200 GW de calcul produit par an ;
   - la mémoire passerait d'environ 8 % du capex des hyperscalers (2023-2024) à environ 30 % (2026) ;
   - les TPU de Google coûteraient 20 à 50 % de moins par FLOP utile que les GB200/GB300 de NVIDIA pour les grands acheteurs.
   Ces conclusions sont citées à travers des sources secondaires, SemiAnalysis étant payant et inaccessible depuis notre environnement.

---

## 4. Le prospectus d'Anthropic : l'impact sur le trio

**Statut du document.**
- Anthropic a déposé un projet confidentiel de S-1 le 01/06/2026.
- Un projet de prospectus a fuité et a été révélé par Reuters le 28/09/2026. Il n'était **pas sur EDGAR au 29/09**.
- Les chiffres pourront changer dans la version publique.

| Élément rapporté | Valeur |
|---|---|
| Chiffre d'affaires 2025 | 4,59 Md$ (×12) |
| CA T2 2026 (préliminaire) | > 11,5 Md$, soit environ 46 Md$ en rythme annuel |
| Perte nette 2025 | 41,97 Md$, dont environ 34 Md$ non monétaires |
| Engagements de calcul | **518 Md$** sur environ 10 ans, dont **environ 80 % non annulables** |
| … dont Broadcom (locations d'équipements) | **161,2 Md$ (31 %)** |
| … Google / Amazon / xAI-SpaceX / Microsoft / AMD | 111,1 / 110 / jusqu'à 84,5 (annulable) / 31,4 / > 20 Md$ |
| Valorisation visée | > 2 000 Md$, après les élections de mi-mandat de novembre |

**Ce que cela change pour chaque ligne**

- **Broadcom, impact direct et double.**
  - *Côté positif*, Broadcom est la plus grosse ligne du prospectus. Son PDG l'a confirmé : *« Anthropic is on track to become our largest XPU customer in 2027 and sustain that in 2028 »*, soit « Anthropic est en passe de devenir notre premier client XPU en 2027 et de le rester en 2028 » (Hock Tan, T3 FY26). Anthropic prévoit 1 GW de TPU en 2026, 5 GW de TPU v8i en 2027 et jusqu'à 10 GW en 2028.
  - *Côté risque*, les 161,2 Md$ correspondent à des locations d'équipements financées par des véhicules dédiés (plateforme « AI XPV »). Pour la première tranche de 35 Md$, bouclée avec Apollo et Blackstone, Broadcom **garantit la valeur résiduelle** des puces sur 30 Md$ de dette senior : si Anthropic cesse de payer et que les puces se revendent mal, Broadcom couvre la perte. Broadcom porte donc une partie du risque de crédit d'un client qui perd de l'argent.
  - *Notre lecture* : une introduction réussie d'Anthropic, qui lèverait des dizaines de milliards, réduirait fortement ce risque. C'est un catalyseur pour AVGO.
- **Nu et Rheinmetall : aucune exposition directe.** C'est voulu : deux des trois moteurs du portefeuille ne dépendent pas de l'économie des laboratoires d'IA.
- **Pour le marché.** Une introduction à plus de 2 000 Md$, après celle de SpaceX, déjà dans le QQQ à 1,24 %, créera une offre massive de « papier IA ». Ne pas détenir Anthropic est un risque relatif si le titre entre vite dans l'indice.

---

## 5. Analyse détaillée n° 1 : Nu Holdings (NU), la banque qui coûte 1 $ par client et par mois

### 5.1 Fiche

| | |
|---|---|
| Cours / capitalisation | 12,35 $ / 60,0 Md$ (NYSE) |
| P/E NTM / P/E 2027 | 11,3 / 10,6 |
| Médiane 1 an du P/E 12 mois (Zacks) | 13,75 |
| BPA 2025 → 2026e → 2027e | 0,62 $ (base du consensus ; 0,58 $ en GAAP dilué) → 0,86 $ (+39 %) → 1,17 $ (+35 %) |
| ROE (T2 2026, annualisé) | 33 % |
| Clients | 139 M (Brésil ~118 M, Mexique ~16 M, Colombie > 5 M) |
| Taux d'activité mensuelle | 83,5 % (Brésil > 86 %) |
| Coût de service | ~1,0 $ par client actif et par mois |
| Coefficient d'exploitation | 19,5 % (T2 2026) |
| Dépôts | 45,3 Md$ (+18 %), coût à 88 % du taux interbancaire |
| Portefeuille de crédit | 39,4 Md$ (+37 %), marge d'intérêts nette 22,9 % |
| Créances douteuses 90 j / couverture | 6,9 % / 244 % |
| Repli vs plus haut 52 semaines | −35 % |
| Prochaine publication | 12/11/2026 |

### 5.2 Le modèle économique

Nu est une banque 100 % mobile, sans agences. Elle gagne de l'argent de trois façons :
- **les intérêts sur le crédit** : cartes, prêts personnels, et de plus en plus de crédit garanti et de prêts sur salaire ;
- **les commissions d'interchange** sur les paiements par carte ;
- **la marge sur les dépôts**, collectés à 88 % du taux interbancaire.

L'avantage tient en un chiffre : **environ 1 $ de coût de service par client et par mois**, pour un revenu moyen par client actif (ARPAC) d'environ 17 $. Le coefficient d'exploitation de 19,5 % est une fraction de celui des banques traditionnelles brésiliennes. La direction indique qu'elle est la banque principale d'environ 60 % de ses clients du grand public au Brésil.

### 5.3 L'historique (Zacks, en M$)

| | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|---:|
| Revenus | 1 698 | 4 792 | 8 029 | 11 517 | 15 775 |
| Résultat net | −165 | −365 | 1 031 | 1 972 | 2 869 |
| BPA dilué ($) | −0,10 | −0,08 | 0,21 | 0,40 | 0,58 |

| | T3 24 | T4 24 | T1 25 | T2 25 | T3 25 | T4 25 | T1 26 | T2 26 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Revenus | 2 943 | 2 989 | 3 248 | 3 668 | 4 173 | 4 686 | 4 968 | 5 513 |
| Résultat net | 553 | 553 | 557 | 637 | 782 | 892 | 872 | 1 060 |

Le résultat net a été multiplié par 2,8 en deux ans (2023 → 2025). La société a dépassé pour la première fois le milliard de dollars de résultat trimestriel au T2 2026.

### 5.4 Les avantages concurrentiels

- **Coût structurel.** Nu a le coût de service le plus bas du secteur. Il peut prêter moins cher ou gagner plus que les banques à agences.
- **Marque et engagement.** Taux d'activité de 83,5 %. Les clients qui en font leur banque principale ont des taux de défaut environ deux fois plus faibles que la moyenne du portefeuille.
- **Données de crédit.** Plus de 100 M de clients alimentent les modèles de risque.
- **Financement bon marché.** 45 Md$ de dépôts.

### 5.5 Les moteurs 2026-2030

1. **Monétisation au Brésil.** Hausse de l'ARPAC (offres Ultravioleta et Croma), crédit garanti et prêt sur salaire, investissements.
2. **Mexique.** Nu opère désormais comme une banque, avec plus de 16 M de clients. Le Mexique a atteint le point mort plus vite que le Brésil. La licence ouvre les dépôts de salaires et des montants assurés plus élevés.
3. **Colombie.** Plus de 5 M de clients.
4. **États-Unis.**
   - Agrément conditionnel de l'OCC en février 2026 pour une banque nationale.
   - Lancement le 10/09/2026 via Lead Bank : compte rémunéré à 3,50 %, compte multidevise en stablecoins USDC et EURC.
   - Pilotage par la cofondatrice Cristina Junqueira, avec l'ancien gouverneur de la banque centrale du Brésil, Roberto Campos Neto, à la présidence du conseil.
5. **Europe (option, et risque).** Des discussions sur le rachat de Monzo pour 8 à 10 Md£ ont été rapportées. Nu « ne commente pas les rumeurs ». Voir §5.8.

### 5.6 Ce que dit le PDG

- *« For the first time, we generated more than $1 billion in net income »*, soit plus d'un milliard de dollars de résultat net pour la première fois (David Vélez, 13/08/2026).
- *« A bank built on technology, with no branches and no legacy to defend could serve hundreds of millions of people better and at a fraction of the cost »* : une banque technologique, sans agences ni héritage à défendre, peut mieux servir des centaines de millions de personnes pour une fraction du coût.

### 5.7 La valorisation

- **11,3 fois les bénéfices des 12 prochains mois.** Pour un PEG de 1, le marché price une croissance d'environ 11 % par an. Le consensus attend +35 % en 2027 ; nous retenons 22 % par an.
- **Rentabilité.** Un ROE de 33 % sans dividende permet en théorie jusqu'à environ 30 % de croissance annuelle des fonds propres.
- **Cours implicites en septembre 2030, avec un P/E de sortie plafonné à 15 :**

| Scénario | Croissance du BPA/an | P/E de sortie | Cours en 2030 | Rendement annuel |
|---|---:|---:|---:|---:|
| Bear | 6 % | 9,0 | 12,4 $ | 0,1 % |
| Base | 22 % | 15,0 | 36,2 $ | 30,9 % |
| Bull | 30 % | 15,0 | 46,7 $ | 39,5 % |
| **Espéré (25/50/25)** | | | **32,9 $** | **27,8 %** |

- **Zone d'achat PEG ≤ 1 : jusqu'à 24 $.** Le titre est à 12,35 $ : achat complet dès maintenant.

### 5.8 Monzo : la rumeur qui a fait chuter le titre

**Les faits**

- **26/09/2026.** Sky News révèle des discussions entre Nu et Monzo, puis Bloomberg et le Financial Times les confirment.
  - Valorisation évoquée : **8 à 10 Md£, soit 10,6 à 13,3 Md$**, payés en numéraire et en actions.
  - Monzo est conseillée par Morgan Stanley et Slaughter and May.
  - Les discussions sont à un stade précoce. Selon le FT, Nu pourrait se contenter d'une participation, et Monzo étudie aussi la cession de 15 % de son capital à des fonds.
- **28/09.** Nu perd **10,0 % à 12,23 $, soit 6,6 Md$ de capitalisation**, alors que le S&P 500 ne recule que de 0,8 %. Le titre reprend 1 % le lendemain, à 12,35 $.
- **Analystes.** Needham (achat, objectif relevé à 19 $) et Rothschild Redburn (achat) jugent la baisse excessive.

**Ce que Nu achèterait** (Monzo, exercice clos en mars 2026)

| | |
|---|---|
| Chiffre d'affaires | 1,7 Md£ (+39 %) |
| Bénéfice avant impôt ajusté / publié | 172,6 M£ (+20 %) / 87,3 M£ |
| Clients / dépôts | plus de 15 M / 25,7 Md£ (+55 %) |
| Revenu par client actif | 183 £ par an (+11 %) |
| Dernière valorisation | 4,5 Md£ (octobre 2024) |
| Prix évoqué | 5 à 6 fois le chiffre d'affaires, 63 à 79 fois le résultat net ajusté estimé (après environ 27 % d'impôt) |

- **Stratégie.** Monzo a fermé ses activités américaines en 2026 pour se concentrer sur l'Europe. Elle a obtenu une licence bancaire européenne en Irlande en décembre 2025.
- **Direction.** Diana Layfield, ancienne de Google, dirige Monzo depuis février 2026.
- **Conformité.** La FCA a infligé à Monzo une amende de 21,1 M£ en juillet 2025 pour des contrôles anti-blanchiment défaillants.

**L'effet sur le BPA de Nu selon le montage** (`monzo.csv`)

Nos hypothèses :
- le résultat net de Monzo croît de 30 % par an ;
- le numéraire coûte 4 % par an après impôt : il faudrait s'endetter, car l'excédent de capital de Nu n'était que de 1,85 Md$ au T2 2026 ;
- les actions sont émises au cours du 29/09.

| Montage | Actions nouvelles | BPA 2027 | BPA 2030 | Rendement espéré de Nu | Portefeuille |
|---|---:|---:|---:|---:|---:|
| Pas d'accord | — | — | — | 27,8 % | 25,8 % |
| Participation de 15 % | — | −0,7 % | +0,2 % | 27,8 % | 25,9 % |
| Rachat à 8 Md£, 75 % en numéraire | +4,4 % | −5,2 % | −1,1 % | 27,4 % | 25,7 % |
| Rachat à 9 Md£, moitié-moitié | +10,0 % | −8,7 % | −5,4 % | 26,0 % | 25,2 % |
| Rachat à 10 Md£, 75 % en actions | +16,6 % | −12,3 % | −10,0 % | 24,4 % | 24,7 % |
| Rachat à 10 Md£, tout en actions | +22,2 % | −14,3 % | −13,2 % | 23,3 % | 24,4 % |
| Idem, avec un P/E de sortie ramené de 15 à 13 | +22,2 % | −14,3 % | −13,2 % | **19,4 %** | 23,1 % |

**Notre lecture**

1. **Le marché a déjà payé une bonne partie de l'addition.** La baisse de 10 % équivaut à la dilution d'un rachat payé pour moitié à trois quarts en actions.
2. **Même le pire montage ne fait pas sortir Nu du trio au cours actuel.**
   - Rachat tout en actions et décote du titre : 19,4 % par an espérés, au niveau d'Adyen (19,1 %, §8).
   - La dilution se résorbe avec le temps, car Monzo croît plus vite que Nu.
3. **Le vrai risque n'est pas arithmétique.**
   - **La « diworseification ».** Peter Lynch désignait ainsi les acquisitions coûteuses qui dispersent une entreprise gagnante. Monzo reste de la banque numérique, mais dans un pays, une réglementation et une concurrence (Revolut, Starling, Chase) que Nu ne connaît pas.
   - **Un discours qui change.** En janvier 2025 à Davos, David Vélez jugeait que l'Europe n'était pas une priorité pour lancer des services, à cause de la réglementation et de la concurrence (Reuters).
   - **Une rentabilité moindre.** Monzo dégage environ 7 % de marge nette, contre 19 % pour Nu au T2 2026.
   - **Une contradiction.** Nu a autorisé en juin un rachat de ses propres actions pour 1 Md$. En émettre jusqu'à 13 Md$ quelques mois plus tard serait incohérent.
4. **Règle de décision.**
   - **Rumeur, simple participation ou rachat surtout en numéraire** : on garde Nu. L'effet sur le BPA 2030 reste compris entre +0,2 % et −5,4 %.
   - **Rachat annoncé surtout en actions** : c'est le prix qui décide.
     - Sous 12,5 $ environ, Nu reste le meilleur choix, même dans le pire scénario.
     - Au-dessus, son espérance passe sous celle d'Adyen, et plus encore sous celle d'Uber (22,8 %) : on remplace Nu, par Uber sur les chiffres ou par Adyen pour un profil plus prudent ou un PEA.

### 5.9 Les risques

- **Cycle du crédit brésilien.**
  - Créances douteuses à 90 jours : de 6,5 à 6,9 % en un trimestre. Défauts des ménages au Brésil au plus haut depuis 2011.
  - Nu a lancé une campagne de renégociation (« Recomeço ») avec des remises allant jusqu'à 99,9 %.
- **Politique.**
  - Élection présidentielle le **04/10/2026**, second tour le 25/10. Lula et son rival Flávio Bolsonaro proposent tous deux de freiner l'endettement des ménages, y compris par un encadrement plus strict des offres de crédit (Reuters, 18/09/2026).
  - Un État brésilien poursuit Nu au sujet des intérêts du crédit renouvelable.
  - La loi de 2023 plafonne déjà les intérêts du crédit renouvelable au montant de la dette initiale.
- **Monzo.** Risque de payer trop cher, de dilution si le paiement se fait en actions, et d'intégration hors d'Amérique latine (§5.8).
- **Change.** Bénéfices en réals et en pesos, action cotée en dollars.
- **Gouvernance.** Actions à droits de vote multiples détenues par les fondateurs.

### 5.10 Ce qu'il faut surveiller, et quand vendre

- **Indicateurs** : créances douteuses à 15-90 et 90 jours, coût du risque, marge d'intérêts nette, ARPAC, coefficient d'exploitation, dépôts, clients au Mexique, conditions d'un éventuel accord avec Monzo.
- **Vendre si** :
  - les créances douteuses à 90 jours dépassent 8 % durablement ;
  - un rachat de Monzo payé surtout en actions est annoncé et le titre cote au-dessus de 12,5 $ environ (§5.8) ;
  - le ROE passe sous 25 % ;
  - une loi plafonne les taux des cartes à un niveau qui casse la rentabilité du crédit.
- **Avis Zacks** : Rank 3 (Hold), pas de rapport d'analyste disponible. Un article du 29/09/2026 préfère Chime, tout en notant que le P/E 12 mois de Nu (11,23) est sous sa médiane d'un an (13,75).

---

## 6. Analyse détaillée n° 2 : Broadcom (AVGO), l'usine à puces sur mesure de l'IA

### 6.1 Fiche

| | |
|---|---|
| Cours / capitalisation | 355,10 $ / 1 695 Md$ |
| P/E NTM / P/E FY27 | 19,9 / 18,7 (médiane 5 ans selon Zacks : 25,5) |
| BPA non-GAAP FY25 → FY26e → FY27e | 6,82 $ → 11,79 $ (+73 %) → 19,04 $ (+61 %) |
| CA 12 mois | 89,1 Md$ ; T3 FY26 +85,5 % |
| Marge brute / opérationnelle T3 (non-GAAP) | 75 % / 67,9 % |
| FCF 12 mois | 39,4 Md$ ; T3 : 13,7 Md$, soit 46 % du CA |
| Dette brute / trésorerie | 59,4 Md$ / 24,0 Md$ (dette nette : 0,7× l'EBITDA) |
| Dividende | 2,60 $ par an (0,7 %) |
| Repli vs plus haut 52 semaines | −26 % |
| Prochaine publication | 10/12/2026 |

### 6.2 Le modèle économique

**Semi-conducteurs : 70 % du CA au T3 FY26.** L'IA fait à elle seule 56 % du CA total.
- **XPU, 73 % du CA IA.** Broadcom transforme l'architecture d'un client (le TPU de Google, par exemple) en puce fabricable. Il apporte les interconnexions SerDes, l'alimentation, le packaging avancé 3.5D et sécurise l'approvisionnement.
- **Réseau IA.** Commutateurs Ethernet Tomahawk 6, puis Tomahawk 7 à 200 Tb/s. CA multiplié par plus de 2,5 sur un an.
- **Semi-conducteurs hors IA.** Haut débit, Wi-Fi, stockage : 4,2 Md$ par trimestre, stables.

**Logiciel d'infrastructure : 30 % du CA.** VMware (cloud privé), mainframe et cybersécurité. Marge opérationnelle d'environ 84 %, ARR en hausse de 15 %. Cette rente finance la R&D.

**Clients XPU : six au total.** Google (sept générations de TPU depuis 2014), Anthropic, OpenAI (accord de 10 GW signé en octobre 2025), Meta (MTIA, plusieurs GW à partir de 2027), ByteDance, et un sixième dont l'identité varie selon les sources.

### 6.3 L'historique

| Exercice (fin oct./nov.) | FY21 | FY22 | FY23 | FY24 | FY25 | FY26e | FY27e | FY28 (objectif) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CA total (Md$) | 27,5 | 33,2 | 35,8 | 51,6 | 63,9 | ~106 | ~174 | n.d. |
| **CA IA (Md$)** | | | | 12,2 | ~20,3 | **58** | **115** | **230** |
| BPA GAAP dilué ($) | 1,50 | 2,65 | 3,30 | 1,23 | 4,77 | | | |
| BPA non-GAAP ($) | | | | | 6,82 | 11,79 | 19,04 | |

Le BPA GAAP de FY24 est déprimé par l'amortissement des actifs incorporels de VMware, ce qui justifie ici l'usage du BPA non-GAAP. CA trimestriel GAAP : 14,1 Md$ au T4 FY24, puis 18,0, puis 29,6 Md$ au T3 FY26, et 34,8 Md$ attendus au T4.

### 6.4 Les avantages concurrentiels

- **Co-conception et propriété intellectuelle.** SerDes et packaging 3.5D : Broadcom livre déjà la 7e génération de TPU.
- **Échelle d'approvisionnement.** Broadcom a sécurisé l'offre pour 115 Md$ de CA IA en FY27 (plaquettes, substrats, mémoire), dans un monde de goulots.
- **Double position.** Broadcom vend à la fois l'accélérateur et le réseau qui relie les accélérateurs. Ses commutateurs équipent aussi les clusters de GPU concurrents.
- **Économie des TPU.** Selon SemiAnalysis, le TPU coûte 20 à 50 % de moins par FLOP utile que les GPU haut de gamme de NVIDIA pour les grands acheteurs. Chaque client qui bascule vers du sur-mesure est un client Broadcom potentiel.
- **Un dirigeant bâtisseur.** Hock Tan est reconduit jusqu'en 2030 au moins. Sa rémunération en actions est indexée sur le CA IA de FY2028 à FY2030 : rien sous 60 Md$, la cible à 90 Md$, le maximum au-delà de 120 Md$ sur quatre trimestres. L'objectif FY27 (115 Md$) touche déjà presque le plafond.

### 6.5 Les moteurs 2026-2028

- **Anthropic** : 1 GW de TPU en 2026, 5 GW de TPU v8i en 2027, jusqu'à 10 GW en 2028. Commandes de racks Ironwood de 10 Md$ en 2025 et de 11 Md$ en 2026.
- **OpenAI** : premier accélérateur maison, « Jalapeno », livré ; accord pluriannuel de 10 GW.
- **Meta** : MTIA en production au T4 FY26.
- **Réseau IA** : la direction attend une croissance au même rythme que les XPU.

### 6.6 Ce que dit le PDG

- *« Anthropic is on track to become our largest XPU customer in 2027 and sustain that in 2028. »* Anthropic est en passe de devenir le premier client XPU en 2027 et de le rester en 2028 (Hock Tan, T3 FY26, 02/09/2026).
- La direction voit un CA IA de 58 Md$ en FY26, 115 Md$ en FY27 sur la base d'une offre sécurisée, puis 230 Md$ en FY28. Elle précise que la demande dépasse l'objectif FY27 et que le calendrier dépend de l'énergie, des terrains, des substrats et de la mémoire des clients.

### 6.7 La valorisation : le marché ne croit pas aux 230 Md$

- **Aujourd'hui.** P/E NTM de 19,9, contre une médiane de 25,5 sur cinq ans. PEG LT de 0,99, avec seulement 20 % de croissance annuelle supposée après 2027.
- **Notre estimation du BPA FY28** (calcul personnel, pas un consensus) :
  - CA IA de 230 Md$ avec une marge brute d'environ 60 %, logiciel d'environ 42 Md$ à 93 %, semi-conducteurs hors IA d'environ 18 Md$ ;
  - soit un CA d'environ 290 Md$ et une marge opérationnelle d'environ 61 % ;
  - soit un **BPA d'environ 31 $**. À 355 $, cela fait **11,5 fois les bénéfices FY28**. Avec une marge IA de 50 % seulement : environ 27 $ de BPA, 13 fois.
- **Ce que price le marché.** Il décote fortement la trajectoire annoncée, à cause de la concentration des clients, du financement et des marges. C'est une asymétrie favorable si Broadcom tient ne serait-ce que les deux tiers de l'objectif.
- **Cours implicites en septembre 2030 :**

| Scénario | Croissance du BPA/an | P/E de sortie | Cours en 2030 | Rendement annuel |
|---|---:|---:|---:|---:|
| Bear | 3 % | 9,9 | 206 $ | −12,8 % |
| Base | 20 % | 19,9 | 761 $ | 21,0 % |
| Bull | 30 % | 29,8 | 1 566 $ | 44,9 % |
| **Espéré** | | | **823 $** | **23,4 %** |

- **Zone d'achat PEG ≤ 1 : jusqu'à 358 $.** Le titre est à 355 $ : achat complet dès maintenant, et renforcement sur repli.

### 6.8 Les risques

- **Anthropic, premier client et risque de crédit.**
  - Un client qui perd de l'argent (8,06 Md$ de perte opérationnelle en 2025) et porte 518 Md$ d'engagements.
  - Broadcom garantit la valeur résiduelle de 30 Md$ de dette dans la première tranche XPV. Selon la presse, il chercherait 60 à 100 Md$ de financements supplémentaires pour les puces d'Anthropic et d'OpenAI.
  - Un analyste crédit a abaissé sa recommandation sur la dette de Broadcom (« Marketweight ») en citant ce risque.
- **Concentration.** Les 5 premiers clients faisaient environ 40 % du CA FY25. Quatre clients XPU portent l'essentiel de la croissance.
- **Marge.** La marge brute non-GAAP passe de 78 % un an plus tôt à environ 73 % au T4, à mesure que les XPU pèsent plus, avec davantage de mémoire embarquée.
- **Exécution.** Le calendrier dépend de l'énergie, des datacenters, des substrats et de la mémoire des clients.
- **Dette.** 59 Md$ de dette brute. Garanties de valeur résiduelle possibles sur les prochaines tranches.

### 6.9 Ce qu'il faut surveiller, et quand vendre

- **Indicateurs** : CA IA trimestriel face à la guidance (21,7 Md$ au T4), marge brute, taille et garanties des tranches XPV, introduction en bourse d'Anthropic, guidance FY27 lors de la publication du 10/12/2026.
- **Vendre si** :
  - un grand client XPU reporte ses déploiements ;
  - la trajectoire FY28 de 230 Md$ est abandonnée ;
  - les garanties de valeur résiduelle dépassent environ 25 % des fonds propres.
- **Avis Zacks (04/09/2026)** : Neutral, Rank 3, objectif 375 $ (20,9 fois les bénéfices 12 mois).

---

## 7. Analyse détaillée n° 3 : Rheinmetall (RHM / RNMBY), l'arsenal de l'Europe

### 7.1 Fiche

| | |
|---|---|
| Cours | 957,65 € (Xetra, 30/09) ; 218,29 $ l'ADR, qui vaut 1/5 d'action |
| Capitalisation | 44,6 Md€ (50,9 Md$) |
| P/E NTM / P/E 2027 | 20,2 / 18,8 |
| BPA 2025 → 2026e → 2027e | 22,73 € (activités poursuivies) → ~36,6 € (+61 %) → ~50,8 € (+39 %) |
| CA 2026 visé | 13,7 à 14,2 Md€ (+38 à +43 %, dont 28 à 31 % de croissance organique) ; marge opérationnelle d'environ 19 % |
| Carnet de commandes | 63,8 Md€ fin 2025 → **80,5 Md€ fin juin 2026** (+44 %, dont 70 % de commandes fermes) → 100 à 120 Md€ visés fin 2026 |
| Dividende 2025 | 11,50 € par action (1,2 %) |
| FCF opérationnel | +1,22 Md€ en 2025 ; −1,62 Md€ au S1 2026 |
| Repli | −52 % depuis le record de 2 008 € (03/10/2025) ; −38 % depuis janvier |
| Zacks | Rank 2 (Buy), un seul analyste sur l'ADR |
| Prochaines dates | Résultats du T3 le 05/11/2026 ; journée investisseurs du 25 au 27/11 à Hambourg |
| Enveloppe | Éligible au PEA (société allemande), à acheter sur Xetra |

Consensus 2026-2027 converti depuis le BPA par ADR de Zacks (8,35 $ et 11,59 $, soit ×5 à 1,14 $/€). Un seul analyste suit l'ADR chez Zacks : prudence.

### 7.2 Pourquoi le titre a perdu la moitié de sa valeur

| Date | Événement | Réaction |
|---|---|---|
| 03/10/2025 | Record historique à 2 008 € | Euphorie du réarmement |
| 18/11/2025 | Journée investisseurs : environ 50 Md€ de CA et une marge supérieure à 20 % visés en 2030 | Le PDG parle lui-même de « wonderworld » |
| 11/03/2026 | Résultats 2025 : 40 à 45 % de croissance visés en 2026, sur fond de guerre en Iran | — |
| 07/05/2026 | T1 2026 : CA de 1,94 Md€, nettement sous les attentes des analystes ; FCF de −285 M€ | Forte baisse |
| 24/06/2026 | Berlin annule les frégates F126, dont Rheinmetall devait être maître d'œuvre, au profit de frégates MEKO A-200 de TKMS | Plus bas à 902,50 € ; le PDG achète plus de 3 M€ d'actions |
| 06/08/2026 | S1 : marge record de 17,1 % au T2, mais CA 2026 abaissé de 300 M€ et carnet visé ramené d'environ 135 Md€ à 100-120 Md€ | −5,7 % dans la séance |
| Début 09/2026 | JPMorgan place le titre sous « Negative Catalyst Watch » avant la journée investisseurs de novembre | Nouvelle baisse |
| 25/09/2026 | Reprise des discussions de paix sur l'Ukraine, menées par les États-Unis | — |
| 29/09/2026 | Le PDG rachète 525 actions, environ 0,5 M€ | — |

**Le diagnostic**

- **Le marché ne doute pas de la demande, il doute de l'exécution.** La question est de transformer 80 Md€ de carnet en chiffre d'affaires et en cash au rythme promis. Le T1 manqué et le FCF négatif du S1 ont nourri ce doute.
- **Tout le secteur a été dévalorisé.** En mars 2026, les valeurs de défense européennes cotaient plus cher que la tech, et les investisseurs ont commencé à exiger des preuves de bénéfices (Bloomberg, 17/03/2026). BAE Systems, Thales et Leonardo ont reculé de 18 à 26 % depuis leurs plus hauts de 52 semaines (§7.8).
- **La coopération franco-allemande se fissure.** Le programme d'avion de combat SCAF a échoué, et le char du futur MGCS, dont Rheinmetall est partenaire, est remis en cause. Armin Papperger s'inquiète publiquement des coupes budgétaires françaises.
- **La paix fait peur, à tort selon la direction** (§7.7).

### 7.3 Le modèle économique

Rheinmetall compte cinq segments de défense depuis la journée investisseurs de novembre 2025 : Armes et Munitions, Systèmes de véhicules, Défense aérienne, Naval (rachat des chantiers de Lürssen) et Digital. La branche automobile civile est en cours de cession.

| T2 2026 | CA | Marge opérationnelle |
|---|---:|---:|
| Armes et Munitions | 1 156 M€ | **25,8 %** (22,7 % un an plus tôt) |
| Systèmes de véhicules | 1 446 M€ | 12,5 % (10,4 %) |
| Défense aérienne | 285 M€ (presque ×2) | 16,3 % (12,3 %) |
| **Groupe** | **3 289 M€ (+69 %)** | **17,1 % (record)** |

**Clients.** Surtout l'État allemand, puis les pays de l'OTAN et l'Ukraine. Le « Rheinmetall Nomination » (commandes et nouveaux contrats-cadres) atteint 16,2 Md€ au S1 2026, dont 11,4 Md€ au T2 (+476 %), avec un ratio commandes sur facturation supérieur à 3.

### 7.4 L'historique (données de la société)

| | 2024 | 2025 | S1 2026 | 2026 (guidance) | 2030 (objectif) |
|---|---:|---:|---:|---:|---:|
| CA (Md€) | 7,7 | 9,9 (+29 %) | 5,2 (+39 %) | 13,7-14,2 | ~50 |
| Marge opérationnelle | | 18,5 % | 15,0 % | ~19 % | > 20 % |
| BPA des activités poursuivies (€) | 17,19 | 22,73 | | | |
| Carnet de commandes (Md€, fin de période) | ~47 | 63,8 | 80,5 | 100-120 | |

2024 et 2025 : activités poursuivies, hors branche automobile. Carnet 2024 déduit de la hausse de 36 % annoncée.

### 7.5 Les avantages concurrentiels

- **Premier producteur de munitions d'Europe.** Environ 1,1 M d'obus de 155 mm en 2027 et environ 1,5 M en 2030. La chaîne est intégrée, de la poudre à l'obus : c'est le goulot physique du réarmement.
- **La poudre, le goulot dans le goulot.** Le programme « Project Firepower » vise 20 000 tonnes de poudre propulsive par an en 2030. La nouvelle usine d'Aschau am Inn (500 M€, production à partir de 2027) en fournira 4 200 tonnes.
- **Plateformes terrestres.** Boxer, Puma, Lynx et Panther.
- **Défense aérienne anti-drones Skyranger.** La Bundeswehr a commandé 19 Skyranger 30 sur Boxer, un segment dont le CA a presque doublé.
- **Visibilité.** 70 % du carnet correspond à des commandes fermes, soit environ quatre ans du CA 2026.

### 7.6 Les moteurs 2026-2030

- **Budgets.**
  - OTAN : objectif de 5 % du PIB d'ici 2035, dont 3,5 % pour la défense au sens strict (sommet de La Haye, juin 2025).
  - Allemagne : 108,2 Md€ de budget de défense en 2026. Budget ordinaire porté à 153,9 Md€ en 2028, 162,9 Md€ en 2029 et 183,7 Md€ en 2030 (projet de juillet 2026), soit environ 3,5 % du PIB en 2029.
- **Commandes.** Un carnet de 100 à 120 Md€ est visé fin 2026, selon le calendrier des contrats allemands, soit 7 à 9 ans du CA 2026.
- **Nouveaux produits.** Des missiles de croisière avec Destinus et Lockheed Martin, avec un premier contrat attendu fin 2026 ou début 2027. S'y ajoutent les drones, le spatial et le numérique.
- **Trésorerie.** Les investissements sont ramenés à 8-9 % du CA, contre 16 % prévus, ce qui doit améliorer le FCF.
- **Objectif 2030 de la direction** : environ 50 Md€ de CA, soit 5 fois 2024, une marge supérieure à 20 % et une conversion en cash supérieure à 50 %.

### 7.7 Ce que dit le PDG, et ce qu'il fait

- *« We are maintaining our solid growth trajectory and continuing to improve profitability, partly through a significant expansion of our capacity. In the second quarter, we were even able to increase the operating result margin to 17.1% – a new high. »* La croissance reste solide, la rentabilité progresse grâce à l'extension des capacités, et la marge du T2 est un record (Armin Papperger, 06/08/2026).
- **Sur l'objectif 2030**, en novembre 2025, il a reconnu que les chiffres pouvaient ressembler à un « wonderworld ».
- **Sur la paix.** Un accord ou un gel du conflit en Ukraine n'arrêterait pas la croissance : les pays de l'OTAN sont décidés à réarmer, et la demande restera forte longtemps (journée investisseurs de novembre 2025).
- **Sur les missiles.** Il attend un premier contrat de missiles de croisière d'ici fin 2026 ou début 2027.
- **Il achète ses propres actions.** Plus de 3 M€ fin juin 2026, près du plus bas de 52 semaines (902,50 €), après la chute provoquée par l'annulation de la frégate F126. Puis 525 actions, soit environ 499 000 €, le 29/09/2026. Pour Lynch, les achats d'initiés sont l'un des meilleurs signaux.

### 7.8 Rheinmetall face aux autres grands de la défense européenne

Données Zacks au 29/09/2026 (ADR) ; P/E NTM calendarisé comme pour les autres titres.

| | P/E NTM | Croissance du BPA 2027 | PEG 2027 | Repli vs plus haut 52 semaines | Analystes (Zacks) |
|---|---:|---:|---:|---:|---:|
| **Rheinmetall** (RNMBY) | 20,2 | +39 % | **0,49** | −53 % | 1 |
| Leonardo (FINMY) | 17,2 | +22 % | 0,73 | −26 % | 1 |
| Thales (THLLY) | 18,9 | +15 % | 1,24 | −22 % | 1 |
| BAE Systems (BAESY) | 20,3 | +15 % | 1,32 | −18 % | 5 |

- **Au même P/E que BAE Systems, Rheinmetall offre 2,6 fois plus de croissance attendue.** C'est le PEG le plus bas du groupe.
- **C'est aussi celui qui a le plus baissé.** Le marché fait payer à Rheinmetall ses problèmes d'exécution, pas seulement ceux du secteur.
- **Réserve.** Trois des quatre consensus reposent sur un seul analyste.

### 7.9 La valorisation

- **20 fois les bénéfices 12 mois pour +39 % de croissance en 2027** : PEG 2027 de 0,49 et PEG LT de 0,92.
- **Test de l'objectif 2030.** 50 Md€ × 20 % donnent un résultat opérationnel d'environ 10 Md€, soit environ 7 Md€ de résultat net et **un BPA d'environ 150 €**. Le cours actuel ne ferait que 6,4 fois ce BPA. Notre base (22 % par an) ne suppose qu'environ 60 % de la trajectoire.
- **Et si Rheinmetall n'atteignait que la moitié de son objectif ?** 25 Md€ de CA à 18 % de marge donneraient environ 3,1 Md€ de résultat net, soit un BPA d'environ 67 €. À 15 fois ce BPA, le titre vaudrait environ 1 000 € en 2030, à peu près son cours actuel : **le prix d'aujourd'hui intègre déjà un objectif atteint à moitié.**
- **Cours implicites en septembre 2030 (ADR) :**

| Scénario | Croissance du BPA/an | P/E de sortie | Cours ADR en 2030 | Rendement annuel |
|---|---:|---:|---:|---:|
| Bear | 5 % | 10,1 | 137 $ | −10,9 % |
| Base | 22 % | 21,1 | 522 $ (≈ 2 290 € l'action) | 24,4 % |
| Bull | 35 % | 28,0 | 1 038 $ | 47,7 % |
| **Espéré** | | | **555 $** | **26,3 %** |

- **Zone d'achat PEG ≤ 1 : jusqu'à 237 $ par ADR, environ 1 040 € par action.** Le titre est à 957,65 € : achat complet, de préférence sur Xetra en euros.

### 7.10 Les risques

- **Paix en Ukraine.** Les discussions menées par les États-Unis ont repris en septembre 2026, après les trêves d'avril et de mai, sans avancée notable pour l'instant. Une paix durable pèserait sur le sentiment. Le réarmement de l'OTAN, lui, ne dépend pas de l'Ukraine.
- **Exécution et trésorerie.**
  - FCF opérationnel de −1,6 Md€ au S1 (décalage des acomptes, stocks, investissements).
  - T1 manqué, puis CA 2026 abaissé de 300 M€ après l'annulation de la frégate F126 (12,8 Md€).
- **La journée investisseurs de fin novembre.** JPMorgan craint que le nouvel objectif fasse plus de place aux drones, aux missiles, au numérique et au spatial. Ces activités sont moins rentables que les munitions et les blindés : c'est un risque sur la marge.
- **La commande publique allemande.** Le budget 2027 doit encore être voté, et l'annulation de la F126 montre que Berlin peut revenir sur un programme.
- **La coopération franco-allemande.** Le MGCS est remis en cause.
- **Sentiment.** Le titre est volatil : le bêta de 0,17 mesuré sur l'ADR ne le reflète pas.
- **Données.** Consensus mince chez Zacks (un seul analyste), ADR OTC peu liquide, change EUR/USD.

### 7.11 Ce qu'il faut surveiller, et quand vendre

- **Indicateurs** : carnet (100 à 120 Md€ visés fin 2026), « Nomination » trimestrielle, marges par segment, FCF du S2 (conversion en cash supérieure à 40 % attendue), journée investisseurs du 25 au 27/11, vote du budget allemand 2027, négociations sur l'Ukraine, premier contrat de missiles de croisière.
- **Vendre si** :
  - le carnet recule deux trimestres de suite ;
  - la conversion en cash de 2026 reste sous 20 % ;
  - l'objectif 2030 est abandonné ou ramené sous 30 Md€ de CA, le niveau que suppose notre scénario de base.
- **Avis Zacks** : Rank 2 (Buy), estimations très peu nombreuses.

---

## 8. Le candidat examiné : Adyen (ADYEN), l'infrastructure de paiement des géants

*Adyen a été ajouté à l'univers à la demande de l'investisseur, pour deux catalyseurs : l'Inde et OpenAI. Il n'entre pas dans le trio. Cette section explique pourquoi, et à quelles conditions cela changerait.*

### 8.1 Fiche

| | |
|---|---|
| Cours / capitalisation | 870 € (Euronext Amsterdam, 29/09/2026) / environ 27,5 Md€ ; ADR ADYEY à 9,80 $ pour 1/100 d'action |
| P/E NTM / P/E 2027 | 19,2 / 18,3 |
| BPA par ADR 2025 → 2026e → 2027e | 0,38 $ → 0,44 $ (+16 %) → 0,535 $ (+22 %) |
| Chiffre d'affaires net 2025 | 2 364 M€ (+18 %, +21 % à changes constants) |
| Résultat net 2025 / S1 2026 | 1,06 Md€ (+15 %) / 544 M€ (+13 %) |
| Marge d'EBITDA | 53 % en 2025 ; 49 % au S1 2026 (50 % hors coûts ponctuels) |
| Volume traité | 1 394 Md€ en 2025 ; 804 Md€ au S1 2026 (+24 %) |
| Commission moyenne (take rate) | 0,162 % du volume au S1 2026 |
| Bilan | Aucune dette ; 10,8 Md€ de liquidités, dont une partie due aux commerçants |
| Repli vs plus haut 52 semaines | −46 % (1 600,80 €) |
| Zacks | Rank 3 (Hold), 4 analystes |
| Éligible au PEA | Oui (société néerlandaise cotée à Amsterdam) |

### 8.2 Le modèle économique

- **Une plateforme unique, développée en interne.** Adyen relie directement les commerçants à Visa, Mastercard et aux moyens de paiement locaux, en ligne comme en magasin.
- **Des revenus proportionnels au volume.** Adyen prend une commission sur le volume traité (0,162 % en moyenne) et des frais fixes par transaction. S'y ajoutent des services autour du paiement : paiements intégrés pour les éditeurs de logiciels, financement, émission de cartes.
- **De très grands clients.** Meta, Uber, Spotify, Microsoft et L'Oréal (Zacks), et OpenAI depuis 2026.
- **Une rentabilité élevée.** En 2025, 87 % de l'EBITDA a été converti en cash libre, pour des investissements limités à 5 % du chiffre d'affaires.

### 8.3 OpenAI et l'Inde, chiffrés

**OpenAI : une vitrine, pas encore un moteur**

- **Le contrat.** OpenAI est devenu client au S1 2026 pour les paiements de ses clients particuliers, et partenaire d'Adyen Agentic.
  - Pieter van der Does, cofondateur et co-PDG : *« If you look at a company like OpenAI working for us, that is just for payments. That is for payments of their consumers »*, soit « chez nous, OpenAI, ce sont uniquement les paiements, ceux de ses clients particuliers ».
- **L'ordre de grandeur.** 10 Md$ de paiements par an au taux moyen de 0,162 % rapporteraient environ 16 M$ de chiffre d'affaires net. C'est à peine 0,5 % du chiffre d'affaires d'Adyen en 2026.
- **Le commerce par agents avance lentement.**
  - Le 17/03/2026, OpenAI a réduit le paiement intégré à ChatGPT (« Instant Checkout ») et renvoie désormais les acheteurs vers les sites des marchands.
  - Le protocole de paiement d'OpenAI (ACP) a été co-développé avec Stripe, le grand concurrent d'Adyen.
  - Adyen Agentic, lancé le 16/06/2026, n'est encore qu'en diffusion limitée aux États-Unis.
- **L'angle IA le plus concret, c'est Orb.** Adyen l'a racheté 335 M$. Orb gère la facturation à l'usage, le modèle de prix des entreprises d'IA.

**L'Inde : une vraie option, mais à long terme**

- **La présence.** Adyen est agréé par la banque centrale indienne comme agrégateur de paiement en ligne, pour les paiements domestiques et transfrontaliers.
  - Son acquisition locale fonctionne depuis janvier 2026, avec UPI et RuPay.
  - Adyen dispose d'un centre technologique à Bangalore.
- **Le catalyseur du 15/10/2026.** Les paiements UPI de plus de 2 000 ₹ supporteront une commission de 0,4 %, plafonnée à 300 ₹, après six ans de gratuité.
  - Les courtiers estiment ce nouveau revenu entre 15 000 et 20 600 crores de roupies par an, soit environ 1,7 à 2,3 Md$.
  - Selon Citi, environ 15 % iraient aux agrégateurs non bancaires, soit 250 à 350 M$ à partager entre tous.
  - Même avec une belle part de ce montant, l'Inde pèserait au mieux de l'ordre de 1 % du chiffre d'affaires d'Adyen d'ici 2030.

**Les vrais moteurs 2026-2030**

1. **Le commerce unifié** : 311 Md€ de volume en magasin en 2025 (+34 %).
2. **Les plateformes** : les paiements intégrés aux logiciels, comme Toast dans la restauration.
3. **Les marges** : un objectif d'EBITDA supérieur à 55 % en 2028.
4. **Les premières acquisitions de son histoire**, finalisées le 01/07/2026 : Talon.One (750 M€, moteur de promotions et de fidélité) et Orb.

### 8.4 Ce que disent les dirigeants

- **Objectifs.** Croissance du chiffre d'affaires net de 21 à 23 % à changes constants en 2026, acquisitions incluses, puis d'environ 20 % par an. Marge d'EBITDA supérieure à 55 % en 2028.
- **Stratégie.** Lettre aux actionnaires du S1 2026 : *« By expanding our role well beyond payments, we execute our long-term strategy and solve deeper structural complexity for our merchants »*, soit « en allant bien au-delà du paiement, nous résolvons des problèmes plus profonds pour nos marchands ».
- **Agents d'IA.** Ingo Uytdehaage, co-PDG, présente Adyen Agentic comme une réponse d'infrastructure : les marchands n'ont pas à courir après chaque nouvelle interface d'IA.
- **Direction financière.** Niclas Neglen, directeur financier de Klarna, occupera le même poste chez Adyen à partir du 01/02/2027. Le titre a perdu 4,7 % à l'annonce, le 23/09.

### 8.5 La valorisation

- **19,2 fois les bénéfices des 12 prochains mois, soit un PEG long terme de 1,01** avec notre hypothèse de 19 % de croissance par an. C'est un prix correct pour cette qualité, pas une aubaine.
- **Au plus haut de l'an dernier, le titre valait 1 600 €**, près de deux fois plus, pour des bénéfices plus faibles. La déception vient de la croissance : +17 % au S2 2025, puis un objectif 2026 abaissé en février, qui a fait chuter le titre de 19 % en une séance.
- **Cours implicites en septembre 2030** (en euros par action, au change du 29/09) :

| Scénario | Croissance du BPA/an | P/E de sortie | Cours en 2030 | Rendement annuel |
|---|---:|---:|---:|---:|
| Bear | 8 % | 12,0 | 741 € | −3,9 % |
| Base | 19 % | 19,2 | 1 745 € | 19,0 % |
| Bull | 25 % | 25,0 | 2 770 € | 33,6 % |
| **Espéré (25/50/25)** | | | **1 750 €** | **19,1 %** |

- **Zones de prix.**
  - PEG long terme de 1 : 862 € environ. Le titre est à ce seuil.
  - Entrée dans le trio : **685 € environ**, soit un P/E de 15. À ce prix, l'espérance d'Adyen rejoint celle de Broadcom (23,4 %).

### 8.6 Les risques

- **Stripe.** Partenaire historique d'OpenAI et coauteur de son protocole de paiement, Stripe est en position de force chez les entreprises d'IA.
- **Une commission moyenne en baisse.** Les grands comptes et les paiements en magasin rapportent moins par euro traité.
- **Une croissance qui ralentit.** +16 % au T1 2026 en publié. Les objectifs ont déjà été revus à la baisse : la marge en 2023, la croissance 2026 en février 2026.
- **La concentration des clients.** Un grand client a réduit ses volumes en 2025 : le volume total n'a crû que de 8 %, contre 21 % hors ce client.
- **Un changement de modèle.** Adyen fait ses premières acquisitions après avoir tout construit en interne, et change de directeur financier.
- **Les taux.** Une baisse des taux de la BCE réduit les intérêts perçus sur la trésorerie.

### 8.7 Verdict

- **Pas dans le trio aujourd'hui.** Adyen est 10e sur 14 au classement Lynch, avec 19,1 % par an espérés, contre 23,4 à 27,8 % pour les trois valeurs retenues.
- **Trois usages possibles :**
  1. **La variante prudente, à la place de Broadcom.** L'espérance passe de 25,8 % à 24,5 % par an. En échange, c'est le meilleur scénario bear des 84 trios (−4,6 %), sans aucune valeur IA, avec deux lignes sur trois en PEA.
  2. **Un remplaçant de Nu** si le rachat de Monzo tourne mal (§5.8). Uber rapporte plus, Adyen résiste mieux.
  3. **Une entrée dans le trio à la place de Broadcom**, sous 685 € environ.
- **À surveiller** : la croissance du chiffre d'affaires net (21 à 23 % visés en 2026), la commission moyenne, la marge d'EBITDA, les premiers volumes indiens après le 15/10, et la montée en charge d'OpenAI et d'Adyen Agentic.

---

## 9. Le portefeuille assemblé

### 9.1 Les résultats du modèle

| | Bear | Base | Bull | Espéré |
|---|---:|---:|---:|---:|
| Nu | 0,1 % | 30,9 % | 39,5 % | 27,8 % |
| Broadcom | −12,8 % | 21,0 % | 44,9 % | 23,4 % |
| Rheinmetall | −10,9 % | 24,4 % | 47,7 % | 26,3 % |
| **Portefeuille (1/3 chacun)** | **−7,3 %** | **25,6 %** | **44,1 %** | **25,8 %** |
| Nasdaq 100 reconstitué | −12,3 % | 10,3 % | 23,1 % | 10,0 % |
| Version 8 lignes (première itération) | −10,7 % | 22,6 % | 40,9 % | 22,8 % |

Rendements annuels sur 4 ans.

### 9.2 Sensibilité de l'écart

| Variante (scénario de base) | Portefeuille | Nasdaq 100 | Écart |
|---|---:|---:|---:|
| Modèle de base | 25,6 % | 10,3 % | +15,3 pts |
| Multiples constants pour tous | 22,0 % | 14,6 % | +7,4 pts |
| Croissance du trio −5 pts par an | 19,3 % | 10,3 % | +9,0 pts |
| −5 pts et multiples constants | 17,0 % | 14,6 % | +2,3 pts |
| Pire combinaison (et mémoire au pic dans l'indice) | 17,0 % | 15,4 % | +1,5 pt |

### 9.3 Stress tests

La ou les valeurs visées passent en scénario bear, le reste en base.

| Scénario | Portefeuille | Nasdaq 100 | Écart |
|---|---:|---:|---:|
| Krach du capex IA | 18,5 % | 2,9 % | +15,5 pts |
| Supercycle mémoire prolongé | 25,6 % | 11,4 % | +14,2 pts |
| Choc de crédit ou politique au Brésil (NU) | 16,6 % | 10,3 % | +6,3 pts |
| Paix durable en Ukraine (RNMBY) | 17,4 % | 10,3 % | +7,1 pts |
| Broadcom perd un grand client XPU | 18,5 % | 9,2 % | +9,2 pts |
| **Double choc : Nu et Rheinmetall en bear** | **5,9 %** | **10,3 %** | **−4,4 pts** |
| Nu rachète Monzo 10 Md£ tout en actions (Nu en base, BPA dilué) | 24,0 % | 10,3 % | +13,6 pts |
| Rachat de Monzo tout en actions et choc au Brésil (Nu en bear, BPA dilué) | 15,9 % | 10,3 % | +5,6 pts |

### 9.4 Mise en œuvre

- **Achat.** Un tiers chacun, tout de suite : les trois lignes sont dans leur zone d'achat PEG ≤ 1. Rheinmetall sur Xetra (RHM), éligible au PEA. Nu et Broadcom en compte-titres.
- **Rééquilibrage.** Une fois par an, ou si une ligne dépasse 45 % du portefeuille.
- **Vente.** Uniquement si l'histoire change (critères aux §5.10, 6.9 et 7.11), pas parce que le cours baisse.
- **Monzo.** Pas de vente sur la rumeur. Si un rachat payé surtout en actions est annoncé, Nu reste en portefeuille sous 12,5 $ environ ; au-dessus, il cède sa place à Uber ou à Adyen (§5.8).
- **Variante prudente.** Adyen à la place de Broadcom : 1,3 point d'espérance en moins, le meilleur scénario bear des 84 trios, deux lignes sur trois en PEA (§8.7).
- **Calendrier.**
  - Élections au Brésil le 04/10, second tour le 25/10.
  - Commission de 0,4 % sur les gros paiements UPI en Inde à partir du 15/10 (Adyen).
  - Rheinmetall publie le 05/11, Nu le 12/11, Broadcom le 10/12.
  - Introduction en bourse d'Anthropic attendue après les élections américaines de mi-mandat.

---

## 10. Critique des choix et des possibilités

1. **Trois lignes, c'est un pari et non une stratégie de gestion du risque.** Chaque thèse ratée coûte un tiers du capital exposé. Le double choc Brésil + Ukraine suffit à faire perdre le portefeuille face à l'indice.
2. **Nos hypothèses font une partie du résultat.** Avec des multiples constants et 5 points de croissance en moins, l'avance tombe à +2,3 points par an. Elle tient d'abord à la croissance des bénéfices ; la convergence des PEG est un bonus.
3. **Ce que le portefeuille rate.** Micron (5 % de l'indice) si le « supercycle » de la mémoire dure : Micron dit ne servir que la moitié aux deux tiers de la demande de ses plus gros clients. NVIDIA (8,85 % de l'indice) si le GPU garde sa part face au sur-mesure. Anthropic et SpaceX, non détenus.
4. **Les favoris écartés, en toute franchise.**
   - **NVIDIA** reste une entreprise exceptionnelle : ROIC de 83 %, P/E de 17. Mais Broadcom capte la bascule vers le sur-mesure, qui porte l'essentiel du calcul d'Anthropic, pour un PEG plus bas.
   - **Uber** (PEG 0,78, rendement FCF de 7 %) est la meilleure alternative à Rheinmetall, et le meilleur remplaçant de Nu sur les chiffres. On le préférera si l'on ne veut pas de défense ou si un accord de paix se dessine.
   - **Adyen** est une entreprise de grande qualité : marge d'EBITDA de 53 %, aucune dette. Mais à 19 fois les bénéfices pour 19 % de croissance, il est au juste prix. OpenAI et l'Inde sont de bonnes nouvelles qui ne changent pas les chiffres avant 2030 (§8).
5. **Remplaçants avec zones d'achat.**
   - NVDA : sous 200 $, soit un PEG LT de 1.
   - UBER : sous 89 $.
   - ADYEN : sous 685 € environ pour entrer dans le trio (P/E de 15) ; PEG LT de 1 vers 862 €.
   - TSM : sous 361 $.
   - ASML, le vrai goulot EUV selon SemiAnalysis : vers 1 200-1 300 $.
6. **BPA non-GAAP.** Pour Broadcom, l'écart avec le GAAP vient surtout de l'amortissement de VMware, c'est acceptable. Pour Nu, GAAP et ajusté sont proches. Pour Rheinmetall, nous retenons le BPA des activités poursuivies.

---

## 11. Et Reddit ?

- **Accès.** reddit.com bloque les robots d'Anthropic ; ce blocage fait d'ailleurs partie du litige Reddit contre Anthropic. Nous n'avons donc pas pu lire les fils directement.
- **Ce que disent les compteurs.** Selon AltIndex, qui compte les mentions sur r/wallstreetbets, les titres les plus cités le 30/09/2026 sont Micron (259 mentions, sentiment haussier), Meta, Uber (+3 800 % de mentions en 24 h), NVIDIA, Google, SpaceX, Tesla et Amazon. **Aucune de nos trois valeurs n'y figure.**
- **Lecture « à la Lynch ».** C'est plutôt bon signe : Lynch cherchait les histoires que la foule n'a pas encore adoptées. L'euphorie sur Micron, cyclique au pic, conforte notre choix de nous en tenir à l'écart.

---

## 12. Limites

- **Consensus Zacks.** Les bases de BPA (GAAP ou ajustée) diffèrent selon les sociétés, et Rheinmetall n'est suivi que par un analyste.
- **Rheinmetall** : chiffres de la société (en euros) pour l'historique, consensus par ADR (en dollars) pour les prévisions.
- **Adyen** : consensus Zacks de l'ADR non sponsorisé ADYEY (4 analystes), en dollars. Le BPA 2025 est déduit de la croissance 2026 publiée par Zacks. Les cours en euros sont convertis au rapport ADR / action du 29/09.
- **Monzo** : chiffres de l'exercice 2026 et conditions de l'accord tirés de la presse. La croissance du résultat de Monzo (30 % par an) et le coût du numéraire (4 %) sont nos hypothèses ; la décote à 13 fois les bénéfices aussi.
- **Prospectus d'Anthropic.** Version ayant fuité, pas de document public sur EDGAR au 29/09/2026.
- **SemiAnalysis.** Cité via des sources secondaires.
- **Bigdata.com** ([bigdata.com](https://bigdata.com)) : crédits épuisés, non utilisé.
- **Modèle.** Hypothèses éditoriales, règles de multiple simplificatrices. Nasdaq 100 reconstitué à 74 %.

## 13. Reproduction

```bash
cd screens/2026-09-30_portefeuille-peg_nasdaq100
python3 portefeuille.py
```

| Fichier | Contenu |
|---|---|
| `data/zacks_univers.csv` | Consensus des 43 valeurs |
| `data/hypotheses.csv` | Hypothèses de croissance et de sortie |
| `data/qqq_holdings.csv` | Composition du Nasdaq 100 (QQQ) |
| `data/fondamentaux_finalistes.csv` | Fondamentaux des finalistes |
| `resultats_univers.csv` | Sortie du modèle, titre par titre |
| `portefeuille.csv` | Sortie du modèle, lignes du portefeuille |
| `comparaison.csv` | Sortie du modèle, portefeuille vs indice |
| `sensibilites.csv` | Sortie du modèle, variantes |
| `stress_tests.csv` | Sortie du modèle, scénarios de rupture |
| `trios.csv` | Sortie du modèle, les 84 trios à poids égaux |
| `monzo.csv` | Sortie du modèle, effet d'un accord Nu-Monzo selon le montage |

La première version à 8 lignes reste calculée dans `portefeuille.py` (`PORTEFEUILLE_8`).

---

## Sources

**Zacks Investment Research** : cours, consensus, états financiers et composition du QQQ au 30/09/2026.
- Fiches : [NU](https://www.zacks.com/stock/quote/NU) · [AVGO](https://www.zacks.com/stock/quote/AVGO) · [RNMBY](https://www.zacks.com/stock/quote/RNMBY) · [QQQ](https://www.zacks.com/stock/quote/QQQ)
- Rapport d'analyste : [Broadcom, 04/09/2026](https://www.zacks.com/stock/research/snapshot/AVGO)
- Articles :
  - [Nu vs. Chime, 29/09/2026](https://www.zacks.com/stock/news/2997596/nu-vs.-chime:-which-digital-banking-stock-is-the-better-buy?)
  - [Nu Holdings Expands Lending, 24/09/2026](https://www.zacks.com/stock/news/2995403/nu-holdings-expands-lending:-can-credit-quality-hold-up?)
  - [Trump & Xi Meet While Oil & Bond Yields Rise, 24/09/2026](https://www.zacks.com/stock/news/2995198/trump-&-xi-meet-while-oil-&-bond-yields-rise)

**Nu Holdings**
- Résultats du T2 2026 : [Business Wire](https://www.businesswire.com/news/home/20260813187996/en/Nu-Holdings-Ltd.-Reports-Second-Quarter-2026-Financial-Results) · [6-K](https://www.sec.gov/Archives/edgar/data/0001691493/000129281426004222/nupr2q26_6k.htm) · [transcription (Investing.com)](https://www.investing.com/news/transcripts/earnings-call-transcript-nubank-tops-1-billion-in-q2-2026-net-income-93CH-4859540)
- États-Unis : [PYMNTS : agrément de l'OCC](https://www.pymnts.com/legal/bank-regulation/2026/nu-wins-conditional-approval-for-us-national-bank-charter) · [lancement avec Lead Bank](https://www.pymnts.com/news/banking/2026/nu-partners-with-lead-bank-launch-full-unitd-states-banking-suite/)
- Monzo, les discussions :
  - [Axios, 28/09/2026](https://www.axios.com/2026/09/28/nu-monzo-acquisition-talks)
  - [Bloomberg, 26/09/2026](https://www.bloomberg.com/news/articles/2026-09-26/monzo-in-talks-on-possible-sale-to-brazil-s-nubank-sky-reports)
  - [PYMNTS, d'après le FT](https://www.pymnts.com/news/banking/2026/nubank-weighs-13-billion-bid-for-monzo/)
  - [Retail Banker International](https://www.retailbankerinternational.com/news/monzo-potential-sale-nubank/)
- Monzo, la réaction du marché :
  - [FX Leaders, 29/09/2026](https://www.fxleaders.com/news/2026/09/29/nu-holdings-stock-drops-monzo-deal-talks/)
  - [TIKR](https://www.tikr.com/blog/nu-holdings-stock-fell-10-in-a-day-on-reported-monzo-talks-heres-what-a-deal-would-mean-for-shareholders)
  - [Benzinga, rebond du 29/09](https://www.benzinga.com/trading-ideas/movers/26/09/62058583/nu-holdings-stock-bounces-back-whats-happening)
  - [Invezz, Needham](https://invezz.com/news/2026/09/28/needham-says-buy-nu-stock-as-it-sinks-on-acquisition-reports/)
  - [Investing.com, Rothschild Redburn](https://www.investing.com/news/analyst-ratings/rothschild-redburn-reiterates-buy-on-nu-holdings-stock-on-monzo-deal-93CH-4919494)
- Monzo, la société :
  - [Payment Expert : résultats FY26](https://paymentexpert.com/2026/05/19/monzo-fy2026-results-revenue-profit/)
  - [Yahoo Finance : Diana Layfield et l'Europe](https://finance.yahoo.com/markets/stocks/articles/monzo-chief-eyes-european-expansion-115617343.html)
  - [FCA : amende de juillet 2025](https://www.fca.org.uk/news/press-releases/fca-fines-monzo-21m-failings-financial-crime-controls)
- Nu, capital et stratégie :
  - [The Globe and Mail : rachat d'actions de 1 Md$](https://www.theglobeandmail.com/investing/markets/markets-news/Tipranks/2322689/nu-holdings-launches-us1-billion-share-buyback-program/)
  - [Reuters via The Globe and Mail : Vélez à Davos, 2025](https://www.theglobeandmail.com/business/article-nubank-ceo-considers-moving-domicile-to-britain-expanding-in-us/)
- Brésil : [Reuters, 18/09/2026 (via WSAU)](https://wsau.com/2026/09/18/some-brazilian-voters-are-feeling-burned-by-fintech-revolution/) · [élections 2026](https://en.wikipedia.org/wiki/2026_Brazilian_general_election) · [procès sur le crédit renouvelable (Rio Times)](https://www.riotimesonline.com/nubank-sued-revolving-credit-interest-brazil-2026/)

**Broadcom**
- [CNBC, 02/09/2026](https://www.cnbc.com/2026/09/02/broadcom-avgo-q3-earnings-report-2026.html)
- [Benzinga : Anthropic, premier client XPU](https://www.benzinga.com/markets/tech/26/09/61594615/broadcom-ceo-hock-tan-anthropic-largest-xpu-customer-google-tpu-orders)
- [KuCoin : 1 → 5 → 10 GW](https://www.kucoin.com/news/flash/anthropic-to-become-broadcom-s-largest-xpu-customer-by-2027)
- [Capacity : tranche XPV de 35 Md$](https://capacityglobal.com/news/anthropic-blackstone-apollo-35bn-ai-infrastructure-spv/)
- [Investing.com : Apollo et Blackstone](https://www.investing.com/news/company-news/apollo-blackstone-finalize-35-billion-ai-chip-financing-for-anthropic-4729436)
- [Investing.com : note crédit « Marketweight »](https://www.investing.com/news/stock-market-news/broadcom-credit-rating-cut-to-marketweight-on-xpv-concerns-93CH-4850949)
- [TipRanks : prime de Hock Tan](https://www.tipranks.com/news/broadcom-avgo-ties-ceos-award-to-120b-ai-revenue-goal-by-2030)
- [8-K du T4 FY24 : CA IA de 12,2 Md$](https://www.sec.gov/Archives/edgar/data/1730168/000173016824000125/avgo-11032024x8kxex99.htm)
- [The Next Platform, 10/09/2026](https://www.nextplatform.com/connect/2026/09/10/broadcom-rides-rocketing-trend-for-custom-ai-accelerators/5295681)

**Rheinmetall**
- [Rapport annuel 2025 (11/03/2026)](https://www.rheinmetall.com/en/media/news-watch/news/2026/03/2026-03-11-rheinmetall-presents-annual-report-for-2025)
- [Rapport semestriel S1 2026](https://www.rheinmetall.com/en/media/news-watch/news/2026/08/2026-08-06-rheinmetall-news-half-yearly-financial-report-h1)
- [Investing.com : T2 2026 par segment](https://www.investing.com/news/company-news/rheinmetall-q2-2026-slides-record-growth-amid-f126-setback-93CH-4843386)
- [CNBC, 06/08/2026](https://www.cnbc.com/2026/08/06/rheinmetall-stock-earnings-guidance-frigate.html)
- [CNBC, 11/03/2026](https://www.cnbc.com/2026/03/11/rheinmetall-rhm-fy-earnings-stock-2025.html)
- [Bloomberg : objectif 2030](https://www.bloomberg.com/news/articles/2025-11-18/rheinmetall-targets-annual-sales-of-50-billion-in-2030)
- [ad-hoc-news : achats du PDG](https://www.ad-hoc-news.de/boerse/news/unternehmensnachrichten/rheinmetall-insider-buy-lands-as-execution-doubts-keep-the-stock-under/70200830)
- [GuruFocus : budget allemand 2027](https://www.gurufocus.com/news/8945877/germanys-2027-budget-boosts-defense-spending-impacts-rheinmetall-rnmbf)
- [Al Jazeera : pourparlers sur l'Ukraine, 25/09/2026](https://www.aljazeera.com/news/2026/9/25/us-seeking-to-revive-russia-ukraine-ceasefire-talks)
- La chute du titre :
  - [MarketScreener : passage des 2 000 €](https://www.marketscreener.com/news/rheinmetall-surpasses-a-2-000-for-the-first-time-hensoldt-also-hits-record-high-ce7d5bdbd88efe20)
  - [Rheinmetall : chiffres du T1 2026](https://www.rheinmetall.com/Rheinmetall%20Group/Presse/News/Documents/2026/05/2026-05-07-Rheinmetall-News-Quarterly-Statement-Q1.pdf)
  - [Investing.com : T1 2026 sous les attentes](https://www.investing.com/news/transcripts/earnings-call-transcript-rheinmetall-ag-q1-2026-misses-forecasts-stock-tumbles-93CH-4686091)
  - [Investing.com : T2 2026, −5,7 % et carnet visé de 100 à 120 Md€](https://www.investing.com/news/transcripts/earnings-call-transcript-rheinmetall-posts-strong-q2-2026-growth-shares-fall-57-93CH-4842893)
  - [Baird Maritime : F126, carnet visé et investissements](https://www.bairdmaritime.com/security/naval/naval-ships/rheinmetall-cuts-sales-guidance-after-germany-drops-delayed-frigate-order)
  - [finanznachrichten.de : JPMorgan, « Negative Catalyst Watch »](https://www.finanznachrichten.de/nachrichten-2026-09/69554319-rheinmetall-aktie-jpmorgan-sieht-jetzt-ein-neues-risiko-486.htm)
  - [Bloomberg : la défense européenne doit prouver ses bénéfices, 17/03/2026](https://www.bloomberg.com/news/articles/2026-03-17/european-defense-stocks-stall-as-investors-seek-earnings-proof)
  - [ad-hoc-news : paix, MGCS et plus bas annuel](https://www.ad-hoc-news.de/boerse/news/ueberblick/rheinmetall-stock-nears-one-year-low-as-peace-hopes-and-tank-fears/69550394)
- Les moteurs :
  - [Rheinmetall : journée investisseurs 2026](https://www.rheinmetall.com/en/events/2026/ir/capital-markets-day)
  - [defence-industry.eu : missiles de croisière](https://defence-industry.eu/rheinmetall-ceo-says-first-cruise-missile-order-expected-by-year-end-or-early-2027-as-destinus-and-lockheed-martin-ventures-near-signing)
  - [ESD : usine de poudre d'Aschau](https://euro-sd.com/2026/07/news/52524/rheinmetall-powder-plant-foundation-laying-in-aschau-am-inn/)
  - [Yahoo Finance : objectif 2030 et la paix](https://finance.yahoo.com/news/germanys-rheinmetall-aims-quintuple-sales-115631236.html)
- Les pairs, données Zacks : [BAE Systems](https://www.zacks.com/stock/quote/BAESY) · [Thales](https://www.zacks.com/stock/quote/THLLY) · [Leonardo](https://www.zacks.com/stock/quote/FINMY)

**Adyen**
- Données Zacks : [fiche ADYEY](https://www.zacks.com/stock/quote/ADYEY) (Rank, consensus par ADR au 29/09/2026)
- Résultats et objectifs :
  - [Résultats du S1 2026](https://www.adyen.com/press-and-media/adyen-publishes-h1-2026-financial-results-3wjne)
  - [Résultats du S2 2025](https://www.adyen.com/press-and-media/adyen-publishes-h2-2025-financial-results-3pgu2)
  - [Investing.com : chute de février 2026](https://www.investing.com/news/earnings/adyen-shares-plummet-17-on-soft-outlook-q4-miss-4501893)
  - [Bloomberg : objectifs après 2026](https://www.bloomberg.com/news/articles/2025-11-11/adyen-forecasts-20-annual-net-revenue-growth-after-2026)
- Dirigeants :
  - [Transcription du S1 2026 (StockAnalysis)](https://stockanalysis.com/quote/ams/ADYEN/transcripts/575001-h1-2026/)
  - [ad-hoc-news : nouveau directeur financier](https://www.ad-hoc-news.de/boerse/news/vorboerse/adyen-stock-falls-4-70-percent-ahead-of-the-open/70174676)
- Acquisitions :
  - [Talon.One et Orb finalisés](https://www.adyen.com/knowledge-hub/talon-one-orb-acquisitions)
  - [FinTech Futures : Orb pour 335 M$](https://www.fintechfutures.com/m-a/adyen-to-acquire-orb-for-335m)
- IA et agents :
  - [Adyen Agentic](https://www.adyen.com/press-and-media/adyen-agentic)
  - [TechRound : OpenAI réduit Instant Checkout](https://techround.co.uk/news/%E2%81%A0openai-scales-instant-checkout-feature-commerce/)
- Inde :
  - [Finance Magnates : agrément de la RBI](https://www.financemagnates.com/fintech/adyen-expands-in-india-with-rbi-approval-for-online-payment-aggregation/)
  - [Adyen : l'Inde](https://www.adyen.com/the-latest/india-expansion-made-easy)
  - [Business Standard : commission UPI](https://www.business-standard.com/amp/finance/news/upi-fee-why-government-is-putting-a-price-on-big-merchant-payments-126091600484_1.html)
  - [Business Standard : un revenu de 15 000 à 20 600 crores](https://www.business-standard.com/industry/banking/upi-mdr-could-add-15-000-20-600-crore-to-fintechs-and-banks-annually-126091601015_1.html)
  - [Trade Brains : le partage selon Citi](https://tradebrains.in/indian-markets/upi-linked-stocks-in-focus-why-jpmorgan-and-citi-see-up-to-rs17000-cr-revenue-opportunity-12539156)

**Anthropic**
- [Communiqué S-1 (01/06/2026)](https://www.anthropic.com/news/confidential-draft-s1-sec)
- [Fortune, 29/09/2026](https://fortune.com/2026/09/29/anthropic-leaked-ipo-prospectus-losses-growth-ai-end-humanity/)
- [Reuters via WTVB](https://wtvbam.com/2026/09/29/anthropics-518-billion-ai-buildout-hinges-largely-on-deals-that-cannot-be-canceled-filing-shows/)
- [SiliconANGLE](https://siliconangle.com/2026/09/29/leaked-anthropic-ipo-filing-reveals-8b-operating-loss-rapid-revenue-growth/)
- [MarketBeat](https://marketbeat.com/articles/broadcoms-ai-growth-story-faces-a-161-billion-anthropic-test)
- [TheStreet](https://www.thestreet.com/crypto/markets/anthropic-filing-discloses-up-to-84-5b-spacex-commitment)

**SemiAnalysis** (sources secondaires)
- [Dwarkesh Podcast : Dylan Patel](https://www.dwarkesh.com/p/dylan-patel)
- [Dwarkesh sur X : ~200 GW/an](https://x.com/dwarkesh_sp/status/2032514120461988204?lang=en)
- [KuCoin : part de la mémoire dans le capex](https://www.kucoin.com/news/flash/memory-to-account-for-nearly-50-of-hyperscaler-capex-by-2027-per-semianalysis-and-clsa)
- [Rohan Paul sur X : TCO des TPU](https://x.com/rohanpaul_ai/status/1994542476091429008)

**Contexte** : [Micron, 24/7 Wall St](https://247wallst.com/investing/2026/09/21/hbm-sold-out-through-2027-microns-customers-are-begging-can-anything-go-wrong/) · [capex des hyperscalers](https://aiweekly.co/alerts/amazon-microsoft-alphabet-meta-plan-725b-ai-capex-in-2026) · [AltIndex, r/wallstreetbets](https://altindex.com/wallstreetbets)

**Style** : présentation inspirée de l'approche qualité et croissance de [Bourseko](https://bourseko.fr/articles/notre-philosophie-dinvestissement), sans affiliation.
