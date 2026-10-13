#!/usr/bin/env python3
"""Planche contact du MP4 rendu : une image par scène (aux trois quarts de chaque scène), grille 5 × 4.

`python3 planche_contact.py` (FFmpeg requis) écrit planche_contact.jpg à côté du MP4.
"""
import os
import subprocess
import tempfile

from build_video import SCENES, TOTAL

HERE = os.path.dirname(os.path.abspath(__file__))
MP4 = os.path.join(HERE, "Video_portefeuille_5_valeurs_2026-10-13.mp4")
SORTIE = os.path.join(HERE, "planche_contact.jpg")

debuts = [t for _, t, _ in SCENES] + [TOTAL]
instants = [a + 0.75 * (b - a) for a, b in zip(debuts, debuts[1:])]
with tempfile.TemporaryDirectory() as tmp:
    for i, t in enumerate(instants):
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", MP4,
                        "-frames:v", "1", "-vf", "scale=384:216", os.path.join(tmp, f"f{i:02d}.png")], check=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", "1",
                    "-i", os.path.join(tmp, "f%02d.png"), "-vf", "tile=5x4:padding=6:color=0x07090d",
                    "-frames:v", "1", "-q:v", "3", SORTIE], check=True)
print(SORTIE, ":", len(instants), "scènes, instants", ", ".join(f"{t:.1f}" for t in instants))
