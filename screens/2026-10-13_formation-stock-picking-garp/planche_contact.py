#!/usr/bin/env python3
"""Planche contact du PDF : toutes les pages en vignettes, six par rangée.

`python3 planche_contact.py` (pdftoppm et FFmpeg requis) lit Formation_GARP_2026-10-13.pdf et écrit
planche_contact.jpg à côté. Les vignettes servent à relire la mise en page avant livraison :
aucun bloc coupé, aucun titre orphelin, polices chargées.
"""
import glob
import math
import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "Formation_GARP_2026-10-13.pdf")
SORTIE = os.path.join(HERE, "planche_contact.jpg")
COLS = 6

with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(["pdftoppm", "-r", "40", "-png", PDF, os.path.join(tmp, "p")], check=True)
    pages = sorted(glob.glob(os.path.join(tmp, "p-*.png")))
    for i, f in enumerate(pages):
        os.rename(f, os.path.join(tmp, f"v{i:03d}.png"))
    rangs = math.ceil(len(pages) / COLS)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", "1", "-i", os.path.join(tmp, "v%03d.png"),
                    "-vf", f"scale=440:-1,tile={COLS}x{rangs}:padding=8:color=0x222222", "-frames:v", "1", "-q:v", "3", SORTIE], check=True)
print(SORTIE, ":", len(pages), "pages")
