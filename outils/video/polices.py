#!/usr/bin/env python3
"""Copie locale des polices des articles (Archivo, Newsreader, IBM Plex Mono) depuis Google Fonts.

Usage : polices.py DOSSIER
Écrit DOSSIER/polices.css et les fichiers woff2 qu'il référence, pour que le rendu HyperFrames
n'ait aucun appel réseau à faire. Bibliothèque standard uniquement.
"""
import os
import re
import sys
import urllib.request

DOSSIER = sys.argv[1]
URL = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900"
       "&family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..600"
       "&family=IBM+Plex+Mono:wght@400;500;600&display=block")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"}


def lire(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


os.makedirs(DOSSIER, exist_ok=True)
css = lire(URL).decode("utf-8")
# seulement les sous-ensembles latins : le texte est en français
blocs = re.findall(r"/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})", css, flags=re.S)
garde = []
for i, (sous, bloc) in enumerate(blocs):
    if sous not in ("latin", "latin-ext"):
        continue
    url = re.search(r"url\((https://[^)]+\.woff2)\)", bloc).group(1)
    nom = f"p{i:02d}.woff2"
    with open(os.path.join(DOSSIER, nom), "wb") as fh:
        fh.write(lire(url))
    garde.append(bloc.replace(url, nom))
assert garde, "aucune police latine trouvée"
with open(os.path.join(DOSSIER, "polices.css"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(garde) + "\n")
print(f"{len(garde)} fichiers de police copiés dans {DOSSIER}")
