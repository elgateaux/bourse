#!/usr/bin/env python3
"""Bande-son de la vidéo « L'essentiel », synthétisée par script (bibliothèque standard seulement).

`python3 bande_son.py video_essentiel.csv sortie.wav` écrit un WAV stéréo 44,1 kHz en flottants 32 bits.
Appelé par video_essentiel.js ; le WAV est temporaire, seul le MP4 est livré.

Musique originale, sans échantillon extérieur, pensée pour accompagner la lecture :
- nappe d'accords en la mineur, un accord toutes les 6 s, sur un cycle de 16 accords (96 s) qui boucle sans couture ;
- basse douce ; notes de piano électrique clairsemées (motif tiré d'un générateur pseudo-aléatoire à graine fixe) ;
- souffle discret à chaque changement de diapositive, cloche à chaque intertitre de chapitre.
Les instants viennent de video_essentiel.csv (colonnes debut_s, duree_s, type).
"""
import array
import csv
import math
import random
import struct
import sys

SR = 44100
rnd = random.Random(2026)

plan = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
sortie = sys.argv[2]
TOTAL = float(plan[-1]["debut_s"]) + float(plan[-1]["duree_s"])
N = int(math.ceil(TOTAL * SR)) + SR


def table(harm=8, pente=1.9, taille=4096):
    t = [0.0] * taille
    for h in range(1, harm + 1):
        a = 1.0 / h ** pente
        for i in range(taille):
            t[i] += a * math.sin(2 * math.pi * h * i / taille)
    m = max(abs(x) for x in t)
    return [x / m for x in t]


TAB = table()
MASK = len(TAB)

# ---------------- cycle de 16 accords (96 s), synthétisé une fois, bouclé ensuite ----------------
HZ = {"D2": 73.42, "E2": 82.41, "F2": 87.31, "G2": 98.0, "A2": 110.0, "D3": 146.83, "E3": 164.81, "F3": 174.61,
      "G3": 196.0, "A3": 220.0, "B3": 246.94, "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 392.0,
      "A4": 440.0, "B4": 493.88, "C5": 523.25, "D5": 587.33, "E5": 659.25}
ACCORDS = [  # (basse, notes de la nappe)
    ("F2", ("F3", "A3", "C4", "E4")), ("E2", ("E3", "G3", "C4", "D4")), ("A2", ("A3", "C4", "E4", "G4")),
    ("G2", ("G3", "B3", "D4", "E4")), ("D2", ("D3", "F3", "A3", "C4")), ("A2", ("A3", "B3", "C4", "E4")),
    ("F2", ("A3", "C4", "E4", "G4")), ("E2", ("E3", "A3", "B3", "E4")),
]
CYCLE_ACC = ACCORDS + ACCORDS
DUREE_ACC = 6.0
C = int(len(CYCLE_ACC) * DUREE_ACC * SR)
cyc_l = [0.0] * C
cyc_r = [0.0] * C


def ajouter_boucle(buf, i0, samples, gain):
    for k, v in enumerate(samples):
        buf[(i0 + k) % C] += v * gain


def nappe(notes, dur):
    n = int(dur * SR)
    att, rel = int(1.8 * SR), int(2.6 * SR)
    g, d = [0.0] * n, [0.0] * n
    for nom in notes:
        for desac, buf in ((-6, g), (+6, d)):
            inc = HZ[nom] * 2 ** (desac / 1200) * MASK / SR
            ph = rnd.random() * MASK
            for i in range(n):
                buf[i] += TAB[int(ph) % MASK]
                ph += inc
    for buf in (g, d):
        lp = 0.0
        for i in range(n):
            e = min(1.0, i / att) ** 1.5 * (min(1.0, (n - i) / rel) ** 1.3)
            lp += 0.06 * (buf[i] - lp)
            buf[i] = lp * e
    return g, d


def basse(freq, dur):
    n = int(dur * SR)
    return [(math.sin(2 * math.pi * freq * i / SR) + 0.18 * math.sin(4 * math.pi * freq * i / SR))
            * min(1.0, i / (0.25 * SR)) * math.exp(-i / SR * 0.55) for i in range(n)]


def piano(freq):
    n = int(2.4 * SR)
    return [(math.sin(2 * math.pi * freq * i / SR) + 0.35 * math.sin(4 * math.pi * freq * i / SR)
             + 0.08 * math.sin(6 * math.pi * freq * i / SR)) * math.exp(-i / SR * 2.4) * min(1.0, i / (0.006 * SR))
            for i in range(n)]


NOIRE = 0.75  # 80 battements par minute : huit noires par accord
for j, (b, notes) in enumerate(CYCLE_ACC):
    i0 = int(j * DUREE_ACC * SR)
    g, d = nappe(notes, DUREE_ACC + 2.6)
    ajouter_boucle(cyc_l, i0, g, 0.050)
    ajouter_boucle(cyc_r, i0, d, 0.050)
    bs = basse(HZ[b], DUREE_ACC + 0.8)
    ajouter_boucle(cyc_l, i0, bs, 0.11)
    ajouter_boucle(cyc_r, i0, bs, 0.11)
    if j >= len(ACCORDS) // 2:  # notes de piano à partir du cinquième accord, plus denses au second tour : le cycle respire
        aigus = [HZ[x] * 2 for x in notes]
        for q in range(8):
            if rnd.random() < (0.55 if j >= len(ACCORDS) else 0.35):
                f = rnd.choice(aigus)
                if f > 900:
                    f /= 2
                note = piano(f)
                pan = 0.35 + 0.3 * rnd.random()
                for echo, ge in ((0.0, 1.0), (0.375, 0.32), (0.75, 0.11)):
                    k0 = i0 + int((q * NOIRE + echo) * SR)
                    ajouter_boucle(cyc_l, k0, note, 0.030 * ge * (1 - pan) * 2)
                    ajouter_boucle(cyc_r, k0, note, 0.030 * ge * pan * 2)

crete = max(max(abs(x) for x in cyc_l), max(abs(x) for x in cyc_r))
k = 0.55 / crete
cyc_l = array.array("f", (x * k for x in cyc_l))
cyc_r = array.array("f", (x * k for x in cyc_r))

# ---------------- piste complète : le cycle répété, puis les événements ----------------
reps = N // C + 1
full_l = (cyc_l * reps)[:N]
full_r = (cyc_r * reps)[:N]
out = array.array("f", bytes(8 * N))
out[0::2] = full_l
out[1::2] = full_r


def ajouter(t, samples, gain, pan=0.5):
    i0 = int(t * SR)
    for kk, v in enumerate(samples):
        i = i0 + kk
        if 0 <= i < N:
            out[2 * i] += v * gain * (1 - pan) * 2
            out[2 * i + 1] += v * gain * pan * 2


def souffle(dur):
    n = int(dur * SR)
    res, lp = [0.0] * n, 0.0
    for i in range(n):
        p = i / n
        a = p ** 2.4 if p < 0.88 else (1 - (p - 0.88) / 0.12)
        lp += (0.015 + 0.25 * p) * (rnd.uniform(-1, 1) - lp)
        res[i] = lp * a
    m = max(abs(x) for x in res)
    return [x / m for x in res]


def cloche():
    n = int(3.2 * SR)
    parts = ((HZ["A4"], 1.0, 1.6), (HZ["E5"], 0.45, 2.2), (HZ["A4"] * 2.76, 0.18, 4.5), (HZ["A4"] * 5.4, 0.06, 7.0))
    return [sum(a * math.sin(2 * math.pi * f * i / SR) * math.exp(-i / SR * dec) for f, a, dec in parts)
            * min(1.0, i / (0.004 * SR)) for i in range(n)]


WH, BELL = souffle(0.7), cloche()
for k_, r in enumerate(plan):
    t = float(r["debut_s"])
    if k_ > 0:
        ajouter(t - 0.62, WH, 0.06, 0.35 + 0.3 * (k_ % 2))
    if r["type"] in ("intertitre", "couverture"):
        ajouter(t + 0.15, BELL, 0.07, 0.5)

crete = max(max(out), -min(out))
if crete > 0.98:  # garde-fou : jamais d'écrêtage
    k = 0.95 / crete
    out = array.array("f", (x * k for x in out))

# ---------------- WAV en flottants 32 bits (format 3, IEEE) ----------------
data = out.tobytes() if sys.byteorder == "little" else (lambda a: (a.byteswap(), a.tobytes())[1])(array.array("f", out))
with open(sortie, "wb") as w:
    w.write(b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVE")
    w.write(b"fmt " + struct.pack("<IHHIIHH", 16, 3, 2, SR, SR * 2 * 4, 2 * 4, 32))
    w.write(b"data" + struct.pack("<I", len(data)) + data)
print(f"{sortie} : {TOTAL:.1f} s, cycle de {C / SR:.0f} s, crête {crete:.3f}")
