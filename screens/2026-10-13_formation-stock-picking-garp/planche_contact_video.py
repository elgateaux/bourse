#!/usr/bin/env python3
"""Planche contact de la vidéo « L'essentiel » : une image par plan, prise aux 85 % du plan, huit par rangée.

`python3 planche_contact_video.py` (FFmpeg requis) lit Video_GARP_L-essentiel_2026-10-13.mp4 et video_essentiel.csv,
puis écrit planche_contact_video.jpg. Elle sert à relire la vidéo avant livraison : chaque plan est fixé,
animations terminées, sans diapositive manquante ni écran noir.
"""
import csv
import math
import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MP4 = os.path.join(HERE, "Video_GARP_L-essentiel_2026-10-13.mp4")
PLAN = list(csv.DictReader(open(os.path.join(HERE, "video_essentiel.csv"), encoding="utf-8")))
SORTIE = os.path.join(HERE, "planche_contact_video.jpg")
COLS = 8

instants = [float(r["debut_s"]) + 0.85 * float(r["duree_s"]) for r in PLAN]
with tempfile.TemporaryDirectory() as tmp:
    for i, t in enumerate(instants):
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", MP4,
                        "-frames:v", "1", "-vf", "scale=400:225", os.path.join(tmp, f"f{i:03d}.png")], check=True)
    rangs = math.ceil(len(instants) / COLS)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", "1", "-i", os.path.join(tmp, "f%03d.png"),
                    "-vf", f"tile={COLS}x{rangs}:padding=6:color=0x222222", "-frames:v", "1", "-q:v", "3", SORTIE], check=True)
print(SORTIE, ":", len(instants), "plans")
