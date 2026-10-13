#!/usr/bin/env python3
"""Écrit RAPPORT.md et research/megatrends/megatrends.json à partir des sorties de calcul.py.

Stdlib uniquement : `python3 calcul.py && python3 rapport.py`. Les tableaux du rapport sont tirés
de video/donnees_video.json et des CSV : aucun chiffre n'y est saisi à la main.
"""
import csv
import json
import os

from build_video import SCENES, TOTAL, SECTIONS

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(HERE, "..", ".."))
D = json.load(open(os.path.join(HERE, "video", "donnees_video.json"), encoding="utf-8"))
NB = " "


def load(nom):
    with open(os.path.join(HERE, "data", nom), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def table(entetes, lignes):
    out = ["| " + " | ".join(entetes) + " |", "|" + "|".join("---" for _ in entetes) + "|"]
    out += ["| " + " | ".join(str(c) for c in l) + " |" for l in lignes]
    return "\n".join(out)


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


P, N, NH = D["portefeuille"], D["nasdaq"], D["nasdaq_hm"]
V = D["valeurs"]
r1, ry = D["retro"]["1an"], D["retro"]["ytd"]
cit = load("citations.csv")
meg = load("megatendances.csv")
zacks = {r["ticker"]: r for r in load("zacks_2026-10-13.csv")}

LIBELLES = {
    "s1": "Ouverture : le pari et le rendement espéré", "s2": "Citation de Peter Lynch (le PEG)",
    "s3": "Le PEG expliqué (exemple pédagogique)", "s4": "Les cinq valeurs et leurs moteurs",
    "c1": "NVIDIA", "c2": "TSMC", "c3": "Nu Holdings", "c4": "Reddit", "c5": "Adyen",
    "s5": "Croissance du BPA non-GAAP 2027", "s6": "Portefeuille contre Nasdaq 100",
    "s7": "Nuage de Lynch : P/E contre croissance", "s8": "Citation de Warren Buffett",
    "s9": "Les quatre méga-tendances et la constellation", "s10": "Rétroviseur : 12 mois et depuis janvier",
    "s11": "Citation de Peter Lynch (les corrections)", "s12": "Scénarios à quatre ans",
    "s13": "Ce que le modèle ne voit pas", "s14": "Citation de Peter Lynch (savoir ce qu'on possède)",
    "s15": "Conclusion, avertissements et sources",
}
TRANS = {None: "—", "blur": "fondu flou", "push": "poussée", "vpush": "poussée verticale",
         "blocks": "rideaux de couleur"}

scenes = table(["Début", "Scène", "Transition d'entrée"],
               [[mmss(t), LIBELLES[n], TRANS[ty]] for n, t, ty in SCENES])

compar = table(["Indicateur", "Portefeuille (5 × 20 %)", "Nasdaq 100 reconstitué", "Nasdaq 100 hors mémoire"], [
    ["P/E 12 mois", P["pe"], N["pe"], NH["pe"]],
    ["Croissance du BPA 2027 (consensus, pondérée)", P["g27"], N["g27"], NH["g27"]],
    ["PEG 2027", P["peg27"], N["peg27"], NH["peg27"]],
    ["Croissance retenue 2027-2030 (hyp., pondérée)", P["g_lt"], N["g_lt"], NH["g_lt"]],
    ["PEG long terme", P["peg_lt"], N["peg_lt"], NH["peg_lt"]],
    ["Bêta pondéré", P["beta"], N["beta"], NH["beta"]],
    ["Rendement annuel pessimiste", P["bear"], N["bear"], NH["bear"]],
    ["Rendement annuel central", P["base"], N["base"], NH["base"]],
    ["Rendement annuel optimiste", P["bull"], N["bull"], NH["bull"]],
    ["Rendement annuel espéré (25/50/25)", P["esperance"], N["esperance"], NH["esperance"]],
    ["100 € deviennent en 2030 (espérance)", P["cent"] + NB + "€", N["cent"] + NB + "€", NH["cent"] + NB + "€"],
])

valeurs = table(["Valeur", "Cours (12/10)", "BPA 2026 → 2027 ($)", "Croissance 2027", "P/E 12 mois",
                 "Croissance retenue (hyp.)", "PEG LT", "Zone PEG 1", "Espéré / an", "Pessimiste", "Optimiste",
                 "12 mois", "Zacks Rank"],
                [[f"{v['nom']} ({v['symbole']})", v["prix"], f"{v['bpa26']} → {v['bpa27']}", v["g27"], v["pe"],
                  v["g_lt"], v["peg_lt"], f"{v['zone']} ({v['ecart_zone']})", v["esperance"], v["bear"],
                  v["bull"], v["chg_52s"], v["zacks_rank"]] for v in V])

stress = table(["Scénario (mêmes chocs pour l'indice)", "Portefeuille", "Nasdaq 100 reconstitué"],
               [[s["nom"], s["ptf"], s["ndx"]] for s in D["stress"]])

retro = table(["Période", "Portefeuille (poids égaux)", "Nasdaq 100 (QQQ)", "S&P 500 (SPY)"],
              [["12 mois", r1["ptf"], r1["qqq"], r1["spy"]], ["Depuis le 1er janvier", ry["ptf"], ry["qqq"], ry["spy"]]])

megas = table(["Méga-tendance", "Chiffre", "Valeurs", "Sources"],
              [[m["titre"], f"{m['chiffre_txt']} {m['libelle']}", ", ".join(m["valeurs"]),
                f"[{m['source_titre']}]({m['source_url']}) · [{m['source2_titre']}]({m['source2_url']})"]
               for m in D["megatendances"]])

cits = table(["Auteur", "Citation (langue originale)", "Traduction", "Occasion, date", "Sources", "Fiabilité"],
             [[f"{c['auteur']}, {c['fonction']}", f"*{c['texte_original']}*", c["traduction"],
               f"{c['occasion']}, {c['date']}",
               f"[{c['source_titre']}]({c['source_url']}) · [{c['source2_titre']}]({c['source2_url']})", c["fiabilite"]]
              for c in cit])

nu = zacks["NU"]
# Contrôle « à la main » d'une ligne (Nu) : chaque étape recalculée ici, à comparer à la sortie de calcul.py.
import calcul  # noqa: E402  (mêmes fonctions et mêmes pondérations que la vidéo)
hyp = {h["ticker"]: h for h in load("hypotheses.csv")}
h_nu = hyp["NU"]
w0, w1 = calcul.W_N, calcul.W_N1
bpa26, bpa27 = float(nu["eps_f1"]), float(nu["eps_f2"])
ntm = w0 * bpa26 + w1 * bpa27
pe0 = float(nu["prix"]) / ntm
g_b, g_p, g_o, cap = (float(h_nu[k]) for k in ("g_base", "g_bear", "g_bull", "pe_plafond"))
pe_b = min(pe0 + 0.5 * (g_b - pe0), max(pe0, cap))
m_b = (1 + g_b / 100) ** 4 * pe_b / pe0
r_p = max(0.5, min(0.8, 1.5 * max(g_p, 5) / pe0))
m_p = (1 + g_p / 100) ** 4 * r_p
pe_o = min(min(g_o, 1.5 * pe0), max(pe0, cap))
m_o = (1 + g_o / 100) ** 4 * pe_o / pe0
esp = (0.25 * m_p + 0.5 * m_b + 0.25 * m_o) ** 0.25 - 1
f = calcul.fr
ancien = {r["ticker"]: r for r in csv.DictReader(open(os.path.join(
    HERE, "..", "2026-09-30_portefeuille-peg_nasdaq100", "data", "zacks_univers.csv"), encoding="utf-8"))}
controle = (f"BPA NTM = {f(w0, 3)} × {f(bpa26, 3)} + {f(w1, 3)} × {f(bpa27, 3)} = {f(ntm, 3)} $ ; "
            f"P/E = {f(float(nu['prix']), 2)} / {f(ntm, 3)} = {f(pe0, 1)}. "
            f"Central : P/E de sortie {f(pe_b, 1)} (plafond {f(cap, 0)}), (1 + {f(g_b, 0)} %)⁴ × {f(pe_b, 1)} / {f(pe0, 1)} = {f(m_b, 3)}, "
            f"soit {f((m_b ** 0.25 - 1) * 100, 1)} % par an. Pessimiste : P/E × {f(r_p, 3)}, (1 + {f(g_p, 0)} %)⁴ × {f(r_p, 3)} = {f(m_p, 3)}, "
            f"soit {f((m_p ** 0.25 - 1) * 100, 1)} % par an. Optimiste : (1 + {f(g_o, 0)} %)⁴ × {f(pe_o, 1)} / {f(pe0, 1)} = {f(m_o, 3)}. "
            f"Espérance : (0,25 × {f(m_p, 3)} + 0,5 × {f(m_b, 3)} + 0,25 × {f(m_o, 3)})^(1/4) − 1 = {f(esp * 100, 1)} %")
rapport = f"""# Vidéo : cinq valeurs pour battre le Nasdaq 100 (NVIDIA, TSMC, Nu, Reddit, Adyen)

Analyse du {D['date_analyse']}, cours de clôture du {D['date_cours']}, consensus Zacks du {D['date_analyse']}.

> Vidéo de présentation en motion design, réalisée avec [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML et GSAP rendus en MP4). Elle reprend la méthode PEG de Peter Lynch et le modèle du [portefeuille du 30/09/2026](../2026-09-30_portefeuille-peg_nasdaq100/RAPPORT.md), appliqués aux cinq valeurs retenues par l'investisseur. Le bandeau « La Gazette du PEG » est un titre fictif : il ne correspond à aucune publication existante. Analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé.

## Le livrable

- **Vidéo** : [`Video_portefeuille_5_valeurs_2026-10-13.mp4`](Video_portefeuille_5_valeurs_2026-10-13.mp4), 1920 × 1080, 30 images par seconde, {mmss(TOTAL)} ({TOTAL:g} s), bande-son originale synthétisée par script.
- **Planche contact** : [`planche_contact.jpg`](planche_contact.jpg), une image par scène, tirée du MP4 rendu.
- **Composition** : [`video/index.html`](video/index.html), générée par [`build_video.py`](build_video.py) à partir de [`video/donnees_video.json`](video/donnees_video.json). Aucun chiffre n'est saisi à la main dans la composition, sauf l'exemple pédagogique du PEG (P/E de 20, croissance de 20 % puis 40 %), signalé à l'écran.

{scenes}

## En bref

- **Le pari.** Cinq valeurs à 20 % chacune (hyp. : aucune pondération n'a été fixée). Elles cotent {P['pe']} fois leurs bénéfices des 12 prochains mois, contre {N['pe']} pour le Nasdaq 100 reconstitué. Le consensus attend {P['g27']} de croissance du BPA en 2027, contre {N['g27']} pour l'indice, mais {NH['g27']} sans Micron et Sandisk, deux cycliques au sommet.
- **Le prix de la croissance.** PEG long terme de {P['peg_lt']} contre {N['peg_lt']} pour l'indice ({NH['peg_lt']} hors mémoire).
- **Le rendement.** {P['esperance']} par an espérés jusqu'en 2030 (pessimiste {P['bear']}, central {P['base']}, optimiste {P['bull']}), contre {N['esperance']} pour l'indice. 100 € deviennent {P['cent']} € contre {N['cent']} €.
- **Le risque.** {D['p_sous_indice']} de probabilité de finir sous l'indice central, {D['p_perte']} de perdre de l'argent (scénarios indépendants, sans crise corrélée). {D['part_ia_ptf']} du portefeuille dépend du même moteur, l'investissement dans l'IA (NVIDIA et TSMC).
- **Le rétroviseur.** Sur 12 mois, les cinq valeurs à poids égaux font {r1['ptf']}, contre {r1['qqq']} pour le Nasdaq 100 ; depuis janvier, {ry['ptf']} contre {ry['qqq']}. La vidéo le montre : la méthode a coûté cher l'an passé, et c'est aussi ce qui rend ces bénéfices moins chers aujourd'hui.

{compar}

*Calculs de calcul.py ({D['date_analyse']}). Nasdaq 100 reconstitué : {D['ndx_lignes']} valeurs, {D['ndx_couverture']} du poids du QQQ (composition du 30/09/2026).*

## Valeur par valeur

{valeurs}

*BPA non-GAAP calendarisés (consensus Zacks). Adyen : calculs sur l'ADR non sponsorisé ADYEY (1/100 d'action, 4 analystes) ; en PEA, acheter l'action à Amsterdam en euros.*

## Stress tests (rendement annuel sur quatre ans)

{stress}

## Rétroviseur (performances passées, en dollars)

{retro}

*Sources : variations sur 52 semaines et depuis le 1er janvier de Zacks pour les cinq valeurs ; performance sur un an et depuis janvier du QQQ et du SPY (Zacks, {D['date_analyse']}). Poids égaux sans rééquilibrage ; dividendes négligés pour les actions. Le change euro-dollar n'est pas compté.*

## Méga-tendances

{megas}

## Citations

{cits}

## Méthode

- **Même modèle que le 30/09/2026.** `calcul.py` importe les fonctions de `screens/2026-09-30_portefeuille-peg_nasdaq100/portefeuille.py` : scénarios pessimiste, central et optimiste pondérés 25/50/25, P/E de sortie, plafonds, agrégats, probabilités. Les règles sont identiques pour le portefeuille et pour l'indice.
- **Ce qui change.** Les données (consensus Zacks du {D['date_analyse']}, cours du {D['date_cours']}) et le poids des années dans le BPA des 12 prochains mois, calculé à la date d'analyse ({f(w0, 2)} × 2026 + {f(w1, 2)} × 2027 au lieu de 0,25 et 0,75 au 30/09). L'année du dernier exercice publié est lue dans la section EDT de Zacks pour chaque valeur.
- **Hypothèses.** Les croissances 2027-2030 sont celles du 30/09/2026 (`data/hypotheses.csv`, justifiées ligne par ligne), plus prudentes que le consensus. Une seule modification : SpaceX (SPCX), dont le BPA 2026 attendu est proche de zéro ({f(float(zacks['SPCX']['eps_f1']), 2)} $), est pris sur son BPA 2027, comme Alphabet et Amazon.
- **Poids.** 20 % par ligne, hypothèse faute de pondération fixée par l'investisseur. Les poids se changent dans `data/portefeuille.csv`.
- **Contrôle d'une ligne, étape par étape (Nu).** {controle}, identique au rendement espéré de la vidéo ({next(v['esperance'] for v in V if v['ticker'] == 'NU')}).

## Données corrigées ou signalées

- **Nu Holdings.** Le cours passe de {f(float(ancien['NU']['prix']), 2)} $ (29/09, dans le modèle du 30/09) à {f(float(nu['prix']), 2)} $ (12/10). Nu a démenti le 30/09, dans un dépôt à la SEC, toute opération sur Monzo ; le titre a rebondi ([24/7 Wall St, 01/10/2026](https://247wallst.com/investing/2026/10/01/nu-holdings-jumps-3-after-ruling-out-monzo-deal-sofi-and-robinhood-sit-out-the-rally/) · [Payment Expert, 05/10/2026](https://paymentexpert.com/2026/10/05/monzo-seeks-capital-nubank-talks-end/)). Le cours vient de deux appels Zacks concordants (comparaison et fiche).
- **Micron.** Son exercice 2026 a été publié le 30/09 : le dernier exercice publié devient 2026 dans les données du 13/10, ce qui relève fortement son BPA des 12 prochains mois et baisse le P/E de l'indice reconstitué par rapport au 30/09.
- **Steve Huffman (Reddit).** L'article du 01/10/2026 citait « There is no LLM on Earth that wasn't significantly trained on Reddit's data… », formulation introuvable dans l'article de Search Engine Journal donné en source. La vidéo cite la formulation rapportée par SEJ : les grands modèles « would not exist as we know them » sans les contenus de Reddit.
- **Citations d'investisseurs.** Les pages d'origine (berkshirehathaway.com, pbs.org) sont injoignables depuis l'environnement de travail ; les citations sont vérifiées sur deux sources secondaires chacune, avec leur degré de fiabilité dans le tableau ci-dessus.
- **Outils indisponibles.** [Bigdata.com](https://bigdata.com) a répondu « crédits épuisés » ; FMP a refusé les cotations et l'historique de cours (offre insuffisante). Les performances passées viennent donc des variations publiées par Zacks, et l'actualité de la recherche web.

## Ce que la vidéo ne dit pas

- Les scénarios ne sont pas des prévisions, et les probabilités ignorent les crises corrélées (krach général, crise à Taïwan qui toucherait TSMC et NVIDIA ensemble).
- Le change : {D['part_usd']} du portefeuille est coté en dollars ; une baisse de 10 % du dollar coûte environ {D['effet_dollar_10'].replace('−', '')} en euros, à cours inchangés.
- Le portefeuille est plus volatil que l'indice (bêta de {P['beta']} contre {N['beta']}) et peut rester derrière lui un ou deux ans.
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

- **Zacks Investment Research** (consensus et cours au {D['date_analyse']}) : {' · '.join(f'[{t} — Zacks](https://www.zacks.com/stock/quote/{t})' for t in ('NVDA', 'TSM', 'NU', 'RDDT', 'ADYEY', 'QQQ', 'SPY'))} ; les 31 valeurs du Nasdaq 100 reconstitué sont listées dans `data/zacks_2026-10-13.csv`.
- Méga-tendances et citations : liens dans les tableaux ci-dessus.
- [Bigdata.com](https://bigdata.com) : sollicité, crédits épuisés le {D['date_analyse']}.
"""
with open(os.path.join(HERE, "RAPPORT.md"), "w", encoding="utf-8") as f:
    f.write(rapport)

# ---------------- dossier de recherche : méga-tendances ----------------
sources_cit = {c["id"]: c for c in cit}
lien = {"ia-calcul": ["huang", "wei"], "banque-numerique": ["velez"], "paiements": ["adyen"],
        "donnees-humaines": ["huffman"]}
tickers = {"NVDA": "NVDA", "TSM": "TSM", "NU": "NU", "RDDT": "RDDT", "ADYEY": "ADYEY"}
mj = {"date": "2026-10-13", "megatendances": []}
for m in meg:
    srcs = [{"n": 1, "titre": m["source_titre"], "editeur": m["source_titre"].split(" : ")[0], "date": m["date"],
             "url": m["source_url"], "consulte": "2026-10-13"},
            {"n": 2, "titre": m["source2_titre"], "editeur": m["source2_titre"].split(" : ")[0], "date": m["date"],
             "url": m["source2_url"], "consulte": "2026-10-13"}]
    cits_m = []
    for cid in lien[m["id"]]:
        c = sources_cit[cid]
        srcs.append({"n": len(srcs) + 1, "titre": c["source_titre"], "editeur": c["source_titre"].split(" : ")[0],
                     "date": c["date"], "url": c["source_url"], "consulte": "2026-10-13"})
        cits_m.append({"texte": c["texte_original"], "traduction": c["traduction"], "auteur": c["auteur"],
                       "fonction": c["fonction"], "date": c["date"], "source": len(srcs)})
    mj["megatendances"].append({
        "id": m["id"], "nom": m["titre"],
        "marche": {"taille": f"{m['chiffre'].replace('.', ',')} {m['unite']} {m['libelle']}", "croissance": "",
                   "horizon": m["date"], "source": 1},
        "goulots": [], "qui_capte_la_valeur": [tickers[t] for t in m["valeurs"].split(";")],
        "risques": [], "citations": cits_m, "sources": srcs,
    })
os.makedirs(os.path.join(RACINE, "research", "megatrends"), exist_ok=True)
with open(os.path.join(RACINE, "research", "megatrends", "megatrends.json"), "w", encoding="utf-8") as f:
    json.dump(mj, f, ensure_ascii=False, indent=2)
print("RAPPORT.md et research/megatrends/megatrends.json écrits")

# ---------------- ligne du README (date, lien, conclusion chiffrée) ----------------
DOSSIER = "screens/2026-10-13_video-portefeuille_hyperframes"
ligne = (f"| {D['date_analyse']} | [Vidéo en motion design : NVIDIA, TSMC, Nu, Reddit, Adyen]({DOSSIER}/RAPPORT.md) | "
         f"Vidéo de {mmss(TOTAL).replace(':', ' min ')} s (HyperFrames), cinq valeurs à 20 % : P/E 12 mois de {P['pe']} contre {N['pe']}, "
         f"PEG long terme de {P['peg_lt']} contre {N['peg_lt']}, rendement espéré modélisé de {P['esperance']}/an contre {N['esperance']} ; "
         f"mais {r1['ptf']} sur 12 mois contre {r1['qqq']} pour le Nasdaq 100, et {D['part_ia_ptf']} du portefeuille sur le même moteur (IA) "
         f"· [MP4]({DOSSIER}/Video_portefeuille_5_valeurs_2026-10-13.mp4) |")
readme = os.path.join(RACINE, "README.md")
lignes = open(readme, encoding="utf-8").read().split("\n")
idx = [i for i, l in enumerate(lignes) if l.startswith(f"| {D['date_analyse']} | [Vidéo")]
if idx:
    lignes[idx[0]] = ligne
else:
    dernier = max(i for i, l in enumerate(lignes) if l.startswith("| ") and "/" in l[:14])
    lignes.insert(dernier + 1, ligne)
open(readme, "w", encoding="utf-8").write("\n".join(lignes))
print("README.md : ligne du", D["date_analyse"], "à jour")
