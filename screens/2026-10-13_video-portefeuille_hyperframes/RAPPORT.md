# Vidéo : cinq valeurs pour battre le Nasdaq 100 (NVIDIA, TSMC, Nu, Reddit, Adyen)

Analyse du 13/10/2026, cours de clôture du 12/10/2026, consensus Zacks du 13/10/2026.

> Vidéo de présentation en motion design, réalisée avec [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML et GSAP rendus en MP4). Elle reprend la méthode PEG de Peter Lynch et le modèle du [portefeuille du 30/09/2026](../2026-09-30_portefeuille-peg_nasdaq100/RAPPORT.md), appliqués aux cinq valeurs retenues par l'investisseur. Le bandeau « La Gazette du PEG » est un titre fictif : il ne correspond à aucune publication existante. Analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé.

## Le livrable

- **Vidéo** : [`Video_portefeuille_5_valeurs_2026-10-13.mp4`](Video_portefeuille_5_valeurs_2026-10-13.mp4), 1920 × 1080, 30 images par seconde, 3:14 (194 s), bande-son originale synthétisée par script.
- **Planche contact** : [`planche_contact.jpg`](planche_contact.jpg), une image par scène, tirée du MP4 rendu.
- **Composition** : [`video/index.html`](video/index.html), générée par [`build_video.py`](build_video.py) à partir de [`video/donnees_video.json`](video/donnees_video.json). Aucun chiffre n'est saisi à la main dans la composition, sauf l'exemple pédagogique du PEG (P/E de 20, croissance de 20 % puis 40 %), signalé à l'écran.

| Début | Scène | Transition d'entrée |
|---|---|---|
| 0:00 | Ouverture : le pari et le rendement espéré | — |
| 0:08 | Citation de Peter Lynch (le PEG) | fondu flou |
| 0:15 | Le PEG expliqué (exemple pédagogique) | poussée |
| 0:26 | Les cinq valeurs et leurs moteurs | rideaux de couleur |
| 0:30 | NVIDIA | poussée |
| 0:39 | TSMC | poussée |
| 0:47 | Nu Holdings | poussée |
| 0:56 | Reddit | poussée |
| 1:05 | Adyen | poussée |
| 1:13 | Croissance du BPA non-GAAP 2027 | rideaux de couleur |
| 1:23 | Portefeuille contre Nasdaq 100 | poussée |
| 1:35 | Nuage de Lynch : P/E contre croissance | poussée verticale |
| 1:47 | Citation de Warren Buffett | fondu flou |
| 1:53 | Les quatre méga-tendances et la constellation | rideaux de couleur |
| 2:19 | Rétroviseur : 12 mois et depuis janvier | rideaux de couleur |
| 2:30 | Citation de Peter Lynch (les corrections) | fondu flou |
| 2:36 | Scénarios à quatre ans | rideaux de couleur |
| 2:51 | Ce que le modèle ne voit pas | poussée |
| 3:01 | Citation de Peter Lynch (savoir ce qu'on possède) | fondu flou |
| 3:07 | Conclusion, avertissements et sources | fondu flou |

## En bref

- **Le pari.** Cinq valeurs à 20 % chacune (hyp. : aucune pondération n'a été fixée). Elles cotent 18,8 fois leurs bénéfices des 12 prochains mois, contre 21,2 pour le Nasdaq 100 reconstitué. Le consensus attend +39 % de croissance du BPA en 2027, contre +44 % pour l'indice, mais +33 % sans Micron et Sandisk, deux cycliques au sommet.
- **Le prix de la croissance.** PEG long terme de 0,98 contre 3,15 pour l'indice (1,96 hors mémoire).
- **Le rendement.** +19,1 % par an espérés jusqu'en 2030 (pessimiste −9,4 %, central +19,7 %, optimiste +34,5 %), contre +10,4 % pour l'indice. 100 € deviennent 201 € contre 149 €.
- **Le risque.** 12 % de probabilité de finir sous l'indice central, 1,1 % de perdre de l'argent (scénarios indépendants, sans crise corrélée). 40 % du portefeuille dépend du même moteur, l'investissement dans l'IA (NVIDIA et TSMC).
- **Le rétroviseur.** Sur 12 mois, les cinq valeurs à poids égaux font +2,3 %, contre +23,5 % pour le Nasdaq 100 ; depuis janvier, −0,7 % contre +22,7 %. La vidéo le montre : la méthode a coûté cher l'an passé, et c'est aussi ce qui rend ces bénéfices moins chers aujourd'hui.

| Indicateur | Portefeuille (5 × 20 %) | Nasdaq 100 reconstitué | Nasdaq 100 hors mémoire |
|---|---|---|---|
| P/E 12 mois | 18,8 | 21,2 | 27,5 |
| Croissance du BPA 2027 (consensus, pondérée) | +39 % | +44 % | +33 % |
| PEG 2027 | 0,49 | 0,48 | 0,84 |
| Croissance retenue 2027-2030 (hyp., pondérée) | 19,2 % | 6,7 % | 14,0 % |
| PEG long terme | 0,98 | 3,15 | 1,96 |
| Bêta pondéré | 1,79 | 1,60 | 1,49 |
| Rendement annuel pessimiste | −9,4 % | −11,8 % | −12,5 % |
| Rendement annuel central | +19,7 % | +10,6 % | +11,0 % |
| Rendement annuel optimiste | +34,5 % | +23,8 % | +24,1 % |
| Rendement annuel espéré (25/50/25) | +19,1 % | +10,4 % | +10,6 % |
| 100 € deviennent en 2030 (espérance) | 201 € | 149 € | 150 € |

*Calculs de calcul.py (13/10/2026). Nasdaq 100 reconstitué : 31 valeurs, 74,2 % du poids du QQQ (composition du 30/09/2026).*

## Valeur par valeur

| Valeur | Cours (12/10) | BPA 2026 → 2027 ($) | Croissance 2027 | P/E 12 mois | Croissance retenue (hyp.) | PEG LT | Zone PEG 1 | Espéré / an | Pessimiste | Optimiste | 12 mois | Zacks Rank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA (NVDA) | 226,32 $ | 8,87 → 15,01 | +69 % | 16,6 | 15 % | 1,10 | 204,90 $ (+10 %) | 18,2 % | −15,5 % | +38,9 % | +20,2 % | 1 |
| TSMC (TSM) | 444,35 $ | 16,60 → 21,44 | +29 % | 21,8 | 18 % | 1,21 | 366,78 $ (+21 %) | 18,0 % | −10,2 % | +32,7 % | +46,7 % | 2 |
| Nu (NU) | 16,01 $ | 0,86 → 1,16 | +35 % | 14,6 | 22 % | 0,66 | 24,11 $ (−34 %) | 19,9 % | −6,1 % | +30,9 % | +6,2 % | 3 |
| Reddit (RDDT) | 159,93 $ | 5,27 → 6,94 | +32 % | 24,3 | 22 % | 1,11 | 144,55 $ (+11 %) | 20,9 % | −11,7 % | +37,0 % | −21,5 % | 2 |
| Adyen (ADYEN) | 10,21 $ | 0,44 → 0,53 | +21 % | 19,9 | 19 % | 1,05 | 9,73 $ (+5 %) | 18,5 % | −4,9 % | +32,3 % | −40,0 % | 3 |

*BPA non-GAAP calendarisés (consensus Zacks). Adyen : calculs sur l'ADR non sponsorisé ADYEY (1/100 d'action, 4 analystes) ; en PEA, acheter l'action à Amsterdam en euros.*

## Stress tests (rendement annuel sur quatre ans)

| Scénario (mêmes chocs pour l'indice) | Portefeuille | Nasdaq 100 reconstitué |
|---|---|---|
| Krach du capex IA (valeurs IA en bear, le reste en base) | +11,2 % | +3,1 % |
| Choc géopolitique sur Taïwan (TSM en bear) | +15,6 % | +10,6 % |
| NVIDIA perd du terrain face au sur-mesure (NVDA en bear) | +15,8 % | +7,7 % |
| Choc de crédit ou politique au Brésil (NU en bear) | +15,1 % | +10,6 % |
| Reddit perd le trafic de recherche (RDDT en bear) | +14,7 % | +10,6 % |
| Stripe comprime les commissions d'Adyen (ADYEY en bear) | +16,1 % | +10,6 % |
| Double choc fintech : NU et ADYEY en bear | +11,0 % | +10,6 % |
| Tout en base | +19,7 % | +10,6 % |
| Tout en bear | −9,4 % | −11,8 % |
| Tout en bull | +34,5 % | +23,8 % |

## Rétroviseur (performances passées, en dollars)

| Période | Portefeuille (poids égaux) | Nasdaq 100 (QQQ) | S&P 500 (SPY) |
|---|---|---|---|
| 12 mois | +2,3 % | +23,5 % | +17,1 % |
| Depuis le 1er janvier | −0,7 % | +22,7 % | +15,0 % |

*Sources : variations sur 52 semaines et depuis le 1er janvier de Zacks pour les cinq valeurs ; performance sur un an et depuis janvier du QQQ et du SPY (Zacks, 13/10/2026). Poids égaux sans rééquilibrage ; dividendes négligés pour les actions. Le change euro-dollar n'est pas compté.*

## Méga-tendances

| Méga-tendance | Chiffre | Valeurs | Sources |
|---|---|---|---|
| L'usine à intelligence | 700 Md$ d'investissements prévus en 2026 par Microsoft, Alphabet, Amazon et Meta, près du double de 2025 | NVIDIA, TSMC | [Yahoo Finance : Hyperscalers hit $700 billion in 2026 AI spending plans](https://finance.yahoo.com/sectors/technology/articles/hyperscalers-hit-700-billion-2026-111243744.html) · [Om Malik : What I learned about hyperscalers' AI spend (30/04/2026)](https://om.co/2026/04/30/what-i-learned-about-hyperscalers-ai-spend/) |
| La banque dans la poche | 139 M de clients au T2 2026, et plus d'un milliard de dollars de résultat net en un trimestre | Nu | [Nubank : Nu Holdings reports second quarter 2026 financial results](https://international.nubank.com.br/company/nu-holdings-ltd-reports-second-quarter-2026-financial-results/) · [KuCoin : Nu Holdings reports $1.06B net income in Q2 2026 with 139M customers](https://www.kucoin.com/news/flash/nu-holdings-reports-1-06b-net-income-in-q2-2026-with-139m-customers) |
| Les rails de l'argent | 803,8 Md€ de paiements traités au S1 2026, en hausse de 24 % sur un an | Adyen | [Finance Magnates : Adyen lifts 2026 revenue outlook as volume hits €804 billion](https://www.financemagnates.com/fintech/payments/adyen-lifts-2026-revenue-outlook-to-2123-as-volume-hits-804-billion/) · [Financial IT : Adyen publishes H1 2026 financial results](https://financialit.net/news/infrastructure/adyen-publishes-h1-2026-financial-results) |
| Les données humaines | 130,3 M d'utilisateurs actifs chaque jour au T2 2026 (+18 %), chiffre d'affaires en hausse de 61 % | Reddit | [Reddit : communiqué du T2 2026 (8-K déposé à la SEC)](https://www.sec.gov/Archives/edgar/data/0001713445/000171344526000098/earningspressreleaseq226.htm) · [Business Wire : Reddit reports second quarter 2026 results](https://www.businesswire.com/news/home/20260730598707/en/) |

## Citations

| Auteur | Citation (langue originale) | Traduction | Occasion, date | Sources | Fiabilité |
|---|---|---|---|---|---|
| Peter Lynch, gérant du fonds Magellan (Fidelity), 1977-1990 | *The p/e ratio of any company that's fairly priced will equal its growth rate.* | Le P/E d'une société correctement valorisée est égal à son taux de croissance. | livre One Up on Wall Street (chapitre sur les chiffres clés), 1989 | [Validea : The Lynch Approach — GARP, PEGs, and Profits](https://blog.validea.com/?p=7627) · [GuruFocus : Peter Lynch Fair Value (P/E = croissance)](https://gurufocus.com/term/peter-lynch-fair-value/TSLA) | formulation du livre ; règle PEG = 1 confirmée par deux sources secondaires, texte original non consulté |
| Peter Lynch, gérant du fonds Magellan (Fidelity), 1977-1990 | *Know what you own, and know why you own it.* | Sachez ce que vous possédez, et pourquoi vous le possédez. | discours au National Press Club (selon Novel Investor) ; attribuée aussi à One Up on Wall Street, 1994 | [Novel Investor : Peter Lynch — The Single Most Important Thing](https://novelinvestor.com/peter-lynch-single-important-thing/) · [Goodreads : citation de One Up on Wall Street](https://www.goodreads.com/quotes/7317641-know-what-you-own-and-know-why-you-own-it) | attribution solide, formulation condensée |
| Peter Lynch, gérant du fonds Magellan (Fidelity), 1977-1990 | *Far more money has been lost by investors preparing for corrections than has been lost in corrections themselves.* | Les investisseurs ont perdu bien plus d'argent à se préparer aux corrections que dans les corrections elles-mêmes. | citée par le Wall Street Journal (selon Validea), non datée | [Benzinga : Peter Lynch's market observation (mai 2025)](https://www.benzinga.com/markets/25/05/45210591/peter-lynchs-market-observation-far-more-money-has-been-lost-by-investors-preparing-for-corrections) · [A Wealth of Common Sense : Peter Lynch on Stock Market Losses (août 2014)](https://awealthofcommonsense.com/2014/08/peter-lynch-stock-market-losses/) | attribuée ; publication d'origine non identifiée |
| Warren Buffett, PDG de Berkshire Hathaway | *It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price.* | Il vaut bien mieux acheter une entreprise merveilleuse à un prix correct qu'une entreprise correcte à un prix merveilleux. | lettre aux actionnaires de Berkshire Hathaway sur l'exercice 1989, 1989 | [CNBC : Ten pieces of investment advice from America's greatest investor](https://www.cnbc.com/id/101000052) · [The Motley Fool : Warren Buffett's most important money-making revelation (06/07/2014)](https://www.fool.com/investing/general/2014/07/06/warren-buffetts-most-important-money-making-revela.aspx) | lettre publiée sur berkshirehathaway.com (non consultée : site injoignable depuis l'environnement) |
| Jensen Huang, fondateur et PDG de NVIDIA | *We have supply for 70% growth… Our demand is much higher than that.* | Nous avons l'offre pour 70 % de croissance… Notre demande est bien supérieure. | conférence de résultats du T2 de l'exercice 2027, 2026-08-26 | [CNBC : NVIDIA earnings live updates (26/08/2026)](https://www.cnbc.com/2026/08/26/nvidia-nvda-earnings-report-q2-2027-live-updates.html) · [24/7 Wall St : Huang's fiscal Q2 message](https://247wallst.com/cards/huang-s-fiscal-q2-message-shifts-the-demand-story-from-a-sin-nvda-quote-01m0zw3qyj2a5bdqweecppv4he) | reprise de l'article du 01/10/2026 du dépôt |
| C.C. Wei, président et PDG de TSMC | *all the way to probably 2029, 2030* | jusqu'en 2029, 2030 probablement (à propos d'une demande d'IA « très forte ») | conférence de résultats du T2 2026, 2026-07-16 | [MarketBeat : TSMC Q2 earnings call highlights (16/07/2026)](https://www.marketbeat.com/instant-alerts/taiwan-semiconductor-manufacturing-q2-earnings-call-highlights-2026-07-16/) · [VanEck : TSMC Q2 earnings call — what it means for SMH](https://www.vaneck.com/us/en/blogs/thematic-investing/tsmc-q2-earnings-call-what-it-means-for-smh/) | citation partielle rapportée par la presse ; pas de transcription officielle consultée |
| David Vélez, fondateur et PDG de Nu Holdings | *For the first time, we generated more than $1 billion in net income.* | Pour la première fois, nous avons dégagé plus d'un milliard de dollars de résultat net. | conférence de résultats du T2 2026, 2026-08-13 | [Investing.com : transcription du T2 2026 de Nubank](https://www.investing.com/news/transcripts/earnings-call-transcript-nubank-tops-1-billion-in-q2-2026-net-income-93CH-4859540) · [Nubank : Nu Holdings reports second quarter 2026 financial results](https://international.nubank.com.br/company/nu-holdings-ltd-reports-second-quarter-2026-financial-results/) | reprise du rapport du 30/09/2026 du dépôt |
| Adyen, lettre aux actionnaires (co-PDG Pieter van der Does et Ingo Uytdehaage) | *By expanding our role well beyond payments, we execute our long-term strategy and solve deeper structural complexity for our merchants.* | En allant bien au-delà du paiement, nous résolvons des problèmes plus profonds pour nos marchands. | lettre aux actionnaires du S1 2026, 2026-08-13 | [Adyen : résultats du S1 2026](https://www.adyen.com/press-and-media/adyen-publishes-h1-2026-financial-results-3wjne) · [Financial IT : Adyen publishes H1 2026 financial results](https://financialit.net/news/infrastructure/adyen-publishes-h1-2026-financial-results) | reprise du rapport du 30/09/2026 du dépôt |
| Steve Huffman, cofondateur et PDG de Reddit | *would not exist as we know them* | n'existeraient pas tels que nous les connaissons (les grands modèles de langage sans les contenus de Reddit) | entretien au Most Innovative Companies Summit de Fast Company, rapporté par Search Engine Journal, 2026-05-25 | [Search Engine Journal : Reddit CEO — LLMs would not exist without Reddit data](https://www.searchenginejournal.com/reddit-ceo-llms-would-not-exist-without-reddit-data/575786/) · [The ATDB (reprise de l'article de SEJ)](https://www.theatdb.com/news/reddit-ceo-llms-would-not-exist-without-reddit-data-via-sejournal-mattgsouthern) | citation partielle ; remplace la formulation « There is no LLM on Earth… » de l'article du 01/10/2026, introuvable dans l'article de SEJ |

## Méthode

- **Même modèle que le 30/09/2026.** `calcul.py` importe les fonctions de `screens/2026-09-30_portefeuille-peg_nasdaq100/portefeuille.py` : scénarios pessimiste, central et optimiste pondérés 25/50/25, P/E de sortie, plafonds, agrégats, probabilités. Les règles sont identiques pour le portefeuille et pour l'indice.
- **Ce qui change.** Les données (consensus Zacks du 13/10/2026, cours du 12/10/2026) et le poids des années dans le BPA des 12 prochains mois, calculé à la date d'analyse (0,22 × 2026 + 0,78 × 2027 au lieu de 0,25 et 0,75 au 30/09). L'année du dernier exercice publié est lue dans la section EDT de Zacks pour chaque valeur.
- **Hypothèses.** Les croissances 2027-2030 sont celles du 30/09/2026 (`data/hypotheses.csv`, justifiées ligne par ligne), plus prudentes que le consensus. Une seule modification : SpaceX (SPCX), dont le BPA 2026 attendu est proche de zéro (0,07 $), est pris sur son BPA 2027, comme Alphabet et Amazon.
- **Poids.** 20 % par ligne, hypothèse faute de pondération fixée par l'investisseur. Les poids se changent dans `data/portefeuille.csv`.
- **Contrôle d'une ligne, étape par étape (Nu).** BPA NTM = 0,220 × 0,862 + 0,780 × 1,162 = 1,096 $ ; P/E = 16,01 / 1,096 = 14,6. Central : P/E de sortie 15,0 (plafond 15), (1 + 22 %)⁴ × 15,0 / 14,6 = 2,275, soit 22,8 % par an. Pessimiste : P/E × 0,616, (1 + 6 %)⁴ × 0,616 = 0,778, soit −6,1 % par an. Optimiste : (1 + 30 %)⁴ × 15,0 / 14,6 = 2,933. Espérance : (0,25 × 0,778 + 0,5 × 2,275 + 0,25 × 2,933)^(1/4) − 1 = 19,9 %, identique au rendement espéré de la vidéo (19,9 %).

## Données corrigées ou signalées

- **Nu Holdings.** Le cours passe de 12,35 $ (29/09, dans le modèle du 30/09) à 16,01 $ (12/10). Nu a démenti le 30/09, dans un dépôt à la SEC, toute opération sur Monzo ; le titre a rebondi ([24/7 Wall St, 01/10/2026](https://247wallst.com/investing/2026/10/01/nu-holdings-jumps-3-after-ruling-out-monzo-deal-sofi-and-robinhood-sit-out-the-rally/) · [Payment Expert, 05/10/2026](https://paymentexpert.com/2026/10/05/monzo-seeks-capital-nubank-talks-end/)). Le cours vient de deux appels Zacks concordants (comparaison et fiche).
- **Micron.** Son exercice 2026 a été publié le 30/09 : le dernier exercice publié devient 2026 dans les données du 13/10, ce qui relève fortement son BPA des 12 prochains mois et baisse le P/E de l'indice reconstitué par rapport au 30/09.
- **Steve Huffman (Reddit).** L'article du 01/10/2026 citait « There is no LLM on Earth that wasn't significantly trained on Reddit's data… », formulation introuvable dans l'article de Search Engine Journal donné en source. La vidéo cite la formulation rapportée par SEJ : les grands modèles « would not exist as we know them » sans les contenus de Reddit.
- **Citations d'investisseurs.** Les pages d'origine (berkshirehathaway.com, pbs.org) sont injoignables depuis l'environnement de travail ; les citations sont vérifiées sur deux sources secondaires chacune, avec leur degré de fiabilité dans le tableau ci-dessus.
- **Outils indisponibles.** [Bigdata.com](https://bigdata.com) a répondu « crédits épuisés » ; FMP a refusé les cotations et l'historique de cours (offre insuffisante). Les performances passées viennent donc des variations publiées par Zacks, et l'actualité de la recherche web.

## Ce que la vidéo ne dit pas

- Les scénarios ne sont pas des prévisions, et les probabilités ignorent les crises corrélées (krach général, crise à Taïwan qui toucherait TSMC et NVIDIA ensemble).
- Le change : 80 % du portefeuille est coté en dollars ; une baisse de 10 % du dollar coûte environ 8 % en euros, à cours inchangés.
- Le portefeuille est plus volatil que l'indice (bêta de 1,79 contre 1,60) et peut rester derrière lui un ou deux ans.
- La vidéo est une présentation : les chapitres complets par valeur (histoire, huit ans de chiffres, cas de l'ours, règles de vente, fiscalité) relèvent de l'enquête longue du cahier des charges.

## Outils

- **Données** : Zacks Investment Research (consensus EDT et tendance des estimations, fiches, QQQ et SPY), recherche web pour l'actualité et les citations.
- **Typographie** : palettes proposées par Adobe for creativity (sans-serif géométrique et gothique condensée très grasse) ; retenu l'équivalent libre du dépôt, Archivo en largeur condensée, avec Newsreader et IBM Plex Mono (licence OFL, fichiers dans `video/fonts/`).
- **Vidéo** : HyperFrames 0.8.154 (lint et `check` passés, rendu local Chromium + FFmpeg), GSAP 3.14.2 embarqué dans `video/vendor/`.
- **Son** : `bande_son.py`, synthèse par la bibliothèque standard (nappe la mineur, basse, rythmique à 100 battements par minute coupée pendant les citations, souffles sur les transitions), encodée en MP3.

## Reproduction

```sh
cd screens/2026-10-13_video-portefeuille_hyperframes
python3 calcul.py          # CSV de sortie et video/donnees_video.json
python3 build_video.py     # video/index.html
python3 bande_son.py && ffmpeg -i video/audio/bande_son.wav -c:a libmp3lame -b:a 192k video/audio/bande_son.mp3
python3 rapport.py         # RAPPORT.md et research/megatrends/megatrends.json
cd video
npx hyperframes@0.8.154 lint . && npx hyperframes@0.8.154 check .
npx hyperframes@0.8.154 render . --crf 20 --fps 30 -o renders/video.mp4
```

Dans l'environnement de Claude Code sur le web, Chromium est préinstallé : `HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`.

| Fichier | Contenu |
|---|---|
| `data/zacks_2026-10-13.csv` | Consensus BPA non-GAAP, cours et variations : 5 valeurs et 31 valeurs du Nasdaq 100 |
| `data/indices_2026-10-13.csv` | Performances du QQQ et du SPY |
| `data/hypotheses.csv` | Hypothèses de croissance (30/09/2026, SPCX ajusté) |
| `data/portefeuille.csv` | Poids, cotation à acheter, PEA |
| `data/citations.csv`, `data/megatendances.csv` | Textes sourcés de la vidéo |
| `valeurs.csv`, `comparaison.csv`, `stress_tests.csv`, `retroviseur.csv` | Sorties de calcul.py |

## Sources

- **Zacks Investment Research** (consensus et cours au 13/10/2026) : [NVDA — Zacks](https://www.zacks.com/stock/quote/NVDA) · [TSM — Zacks](https://www.zacks.com/stock/quote/TSM) · [NU — Zacks](https://www.zacks.com/stock/quote/NU) · [RDDT — Zacks](https://www.zacks.com/stock/quote/RDDT) · [ADYEY — Zacks](https://www.zacks.com/stock/quote/ADYEY) · [QQQ — Zacks](https://www.zacks.com/stock/quote/QQQ) · [SPY — Zacks](https://www.zacks.com/stock/quote/SPY) ; les 31 valeurs du Nasdaq 100 reconstitué sont listées dans `data/zacks_2026-10-13.csv`.
- Méga-tendances et citations : liens dans les tableaux ci-dessus.
- [Bigdata.com](https://bigdata.com) : sollicité, crédits épuisés le 13/10/2026.
