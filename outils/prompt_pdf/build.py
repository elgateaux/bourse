#!/usr/bin/env python3
"""Met en page le prompt (Markdown du dépôt) en HTML imprimable A4."""
import re
import sys
import markdown

SRC, OUT = sys.argv[1], sys.argv[2]
lignes = open(SRC, encoding="utf-8").read().split("\n")

# Python-Markdown attend 4 espaces par niveau d'imbrication ; le fichier en utilise 2 ou 3.
norm = []
for l in lignes:
    n = len(l) - len(l.lstrip(" "))
    if n in (2, 3):
        l = " " * 4 + l.lstrip(" ")
    elif n in (4, 5, 6):
        l = " " * 8 + l.lstrip(" ")
    norm.append(l)
# Une liste doit être précédée d'une ligne vide (contrairement à GitHub, Python-Markdown l'exige).
marqueur = re.compile(r"^(- |\d+\. )")
avec_vides = []
for l in norm:
    prec = avec_vides[-1] if avec_vides else ""
    if marqueur.match(l) and prec.strip() and not marqueur.match(prec) and not prec.startswith(" "):
        avec_vides.append("")
    avec_vides.append(l)
norm = avec_vides
titre = norm[0].lstrip("# ").strip()
corps_md = "\n".join(norm[1:])
corps = markdown.markdown(corps_md, extensions=["sane_lists"], output_format="html5")

# Espaces insécables de la typographie française.
for a, b in ((" :", " :"), (" ;", " ;"), (" %", " %"), (" $", " $"), ("« ", "« "),
             (" »", " »"), (" ?", " ?")):
    corps = corps.replace(a, b)

html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>Prompt PEG 3 valeurs</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
@page {{ size: A4; margin: 17mm 17mm 19mm; }}
:root {{ --paper: #FFFFFF; --ink: #13222A; --ink-2: #33434A; --muted: #66757A; --rule: #C8D0CB; --accent: #1D5FC4; --box: #EEF1EC;
  --display: "Archivo", "Arial Narrow", Arial, sans-serif; --text: "Newsreader", Georgia, serif; --data: "IBM Plex Mono", "Courier New", monospace; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--paper); color: var(--ink-2); font-family: var(--text); font-size: 11pt; line-height: 1.45; }}
.kicker {{ font-family: var(--data); font-size: 8pt; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); font-weight: 600;
  border-bottom: 3px double var(--ink); padding-bottom: 6pt; display: flex; justify-content: space-between; }}
h1 {{ font-family: var(--display); font-stretch: 78%; font-weight: 800; color: var(--ink); font-size: 26pt; line-height: 1.05;
  letter-spacing: -.01em; margin: 14pt 0 8pt; text-wrap: balance; }}
.chapo {{ font-size: 13pt; line-height: 1.4; color: var(--ink); margin: 0 0 12pt; }}
.mode {{ background: var(--box); border-top: 2px solid var(--ink); padding: 9pt 12pt 6pt; margin: 0 0 6pt; break-inside: avoid; }}
.mode h3 {{ font-family: var(--data); font-size: 8pt; letter-spacing: .1em; text-transform: uppercase; color: var(--ink); margin: 0 0 5pt; }}
.mode ul {{ margin: 0; padding-left: 14pt; font-size: 10pt; }}
.mode li {{ margin-bottom: 3pt; }}
.debut {{ font-family: var(--data); font-size: 8pt; letter-spacing: .1em; text-transform: uppercase; color: var(--muted);
  border-top: 1px dashed var(--muted); margin: 16pt 0 0; padding-top: 5pt; text-align: center; }}
.fin {{ border-top: 1px dashed var(--muted); border-bottom: 0; margin: 18pt 0 0; padding-top: 5pt; }}
h2 {{ font-family: var(--display); font-stretch: 85%; font-weight: 800; color: var(--ink); font-size: 15pt; line-height: 1.15;
  margin: 18pt 0 6pt; padding-top: 6pt; border-top: 2px solid var(--ink); break-after: avoid; break-inside: avoid; }}
p {{ margin: 0 0 7pt; }}
p:has(+ ul), p:has(+ ol) {{ break-after: avoid; }}
.fin {{ break-before: avoid; }}
ul, ol {{ margin: 0 0 8pt; padding-left: 16pt; }}
li {{ margin-bottom: 3pt; }}
li > ul, li > ol {{ margin: 3pt 0 4pt; }}
li::marker {{ color: var(--muted); }}
ol > li::marker {{ font-family: var(--data); font-size: 9pt; color: var(--ink); }}
strong {{ color: var(--ink); font-weight: 650; }}
a {{ color: var(--accent); text-decoration: none; }}
</style></head><body>
<div class="kicker"><span>Le Cahier PEG · Méthode réutilisable</span><span>Version du 1er octobre 2026, révision 2</span></div>
<h1>{titre}</h1>
<p class="chapo">Le prompt complet pour faire construire par un assistant d'IA un portefeuille concentré de trois valeurs, avec la méthode PEG de Peter Lynch, le modèle de scénarios du dépôt elgateaux/bourse et le plan de l'enquête longue : un chapitre en huit parties par valeur, de son histoire à ses règles de vente.</p>
<div class="mode"><h3>Mode d'emploi</h3><ul>
<li>Copiez tout le texte entre les deux traits pointillés, puis remplacez ce qui est entre crochets : date, indice, valeurs préférées, enveloppe fiscale. Sinon, les valeurs par défaut s'appliquent.</li>
<li>Le prompt donne son plein résultat avec un assistant qui a accès à Zacks, à Bigdata.com et au web, et qui peut exécuter du Python. Sans ces outils, fournissez-lui les chiffres.</li>
<li>Les règles du modèle (P/E de sortie, score Lynch, double choc) sont celles du script portefeuille.py du dépôt : les résultats restent comparables d'une analyse à l'autre.</li>
<li>Le plan de l'article et le gabarit des chapitres viennent de l'enquête longue de référence du 1er octobre 2026. Le détail, avec les modèles de dossiers de recherche, est dans le cahier des charges du dépôt (prompts/cahier-des-charges-enquete.md).</li>
</ul></div>
<div class="debut">Début du prompt</div>
{corps}
<div class="debut fin">Fin du prompt</div>
</body></html>"""
open(OUT, "w", encoding="utf-8").write(html)
print("ok", len(html))
