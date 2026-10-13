#!/usr/bin/env python3
"""Bande-son de la vidéo, synthétisée par script (bibliothèque standard seulement).

`python3 bande_son.py` écrit video/audio/bande_son.wav (44,1 kHz, stéréo, 16 bits), puis :
`ffmpeg -i video/audio/bande_son.wav -c:a libmp3lame -b:a 192k video/audio/bande_son.mp3`

Musique originale, sans échantillon extérieur : nappe d'accords (la mineur, vi-IV-I-V), basse,
rythmique à 100 battements par minute coupée pendant les citations, souffles et impacts calés sur
les transitions de build_video.py.
"""
import array
import math
import os
import random
import wave

from build_video import SCENES, TOTAL, MEGA_T

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 44100
N = int(TOTAL * SR)
BPM = 100.0
BEAT = 60.0 / BPM
rnd = random.Random(2026)  # bruit déterministe

pad_l = array.array("f", [0.0]) * N
pad_r = array.array("f", [0.0]) * N
rhy = array.array("f", [0.0]) * N


def add(buf, start_s, samples, gain):
    i0 = int(start_s * SR)
    for k, v in enumerate(samples):
        i = i0 + k
        if 0 <= i < N:
            buf[i] += v * gain


def table(harm=10, pente=1.6, taille=4096):
    t = [0.0] * taille
    for h in range(1, harm + 1):
        a = 1.0 / h ** pente
        for i in range(taille):
            t[i] += a * math.sin(2 * math.pi * h * i / taille)
    m = max(abs(x) for x in t)
    return [x / m for x in t]


TAB = table()


def osc(freq, dur, detune_cents=0.0):
    n = int(dur * SR)
    f = freq * 2 ** (detune_cents / 1200)
    inc = f * len(TAB) / SR
    ph, out, mask = 0.0, [0.0] * n, len(TAB)
    for i in range(n):
        out[i] = TAB[int(ph) % mask]
        ph += inc
    return out


def env(n, att, rel, sustain=1.0):
    a, r = int(att * SR), int(rel * SR)
    e = [sustain] * n
    for i in range(min(a, n)):
        e[i] = sustain * (i / a) ** 1.5
    for i in range(max(0, n - r), n):
        e[i] *= max(0.0, (n - i) / r) ** 1.2
    return e


# ---------------- nappe : un accord toutes les deux mesures ----------------
NOTE = {"A2": 110.0, "C3": 130.81, "D3": 146.83, "E3": 164.81, "F3": 174.61, "G3": 196.0, "A3": 220.0,
        "B3": 246.94, "C4": 261.63, "D4": 293.66, "E4": 329.63, "G4": 392.0}
ACCORDS = [("A3", "C4", "E4", "G4"), ("F3", "A3", "C4", "E4"), ("C4", "E4", "G4", "B3"), ("G3", "B3", "D4", "G4")]
BASSES = ["A2", "F3", "C3", "G3"]
DUREE_ACC = 8 * BEAT  # 4,8 s
cache = {}
for j, acc in enumerate(ACCORDS):
    n = int((DUREE_ACC + 1.6) * SR)
    e = env(n, 1.4, 1.8)
    gauche, droite = [0.0] * n, [0.0] * n
    for note in acc:
        a, b = osc(NOTE[note], n / SR, -5), osc(NOTE[note], n / SR, +5)
        for i in range(n):
            gauche[i] += a[i] * e[i]
            droite[i] += b[i] * e[i]
    # adoucissement : moyenne glissante (passe-bas grossier)
    for ch in (gauche, droite):
        acc_v = 0.0
        for i in range(n):
            acc_v += 0.08 * (ch[i] - acc_v)
            ch[i] = acc_v
    cache[j] = (gauche, droite)

t, j = 0.0, 0
while t < TOTAL:
    g, d = cache[j % 4]
    add(pad_l, t, g, 0.055)
    add(pad_r, t, d, 0.055)
    t += DUREE_ACC
    j += 1

# ---------------- sections calmes : pas de rythmique ----------------
calme = [(0.0, 2.4), (TOTAL - 6.6, TOTAL)]
for nom, debut, tr in SCENES:
    if nom in ("s2", "s8", "s11", "s14"):
        fin = next(s[1] for s in SCENES if s[1] > debut)
        calme.append((debut + 0.3, fin))


def rythme_actif(x):
    return not any(a <= x < b for a, b in calme)


def kick():
    n = int(0.42 * SR)
    out, ph = [0.0] * n, 0.0
    for i in range(n):
        x = i / SR
        f = 46 + 84 * math.exp(-x * 28)
        ph += 2 * math.pi * f / SR
        out[i] = math.sin(ph) * math.exp(-x * 8.5)
    return out


def bruit(dur, dec, hp=True):
    n = int(dur * SR)
    out, prev = [0.0] * n, 0.0
    for i in range(n):
        v = rnd.uniform(-1, 1)
        out[i] = (v - prev if hp else v) * math.exp(-i / SR * dec)
        prev = v
    return out


def basse(freq):
    n = int(0.55 * SR)
    return [(math.sin(2 * math.pi * freq * i / SR) + 0.25 * math.sin(4 * math.pi * freq * i / SR))
            * math.exp(-i / SR * 5.5) * min(1.0, i / (0.004 * SR)) for i in range(n)]


K, HAT = kick(), bruit(0.07, 70)
SNARE = [b + 0.5 * math.sin(2 * math.pi * 185 * i / SR) * math.exp(-i / SR * 24)
         for i, b in enumerate(bruit(0.22, 22, hp=False))]
BASS = {nm: basse(NOTE[nm] / 2) for nm in BASSES}

b = 0
while b * BEAT < TOTAL:
    x = b * BEAT
    if rythme_actif(x):
        add(rhy, x, K, 0.30)
        add(rhy, x + BEAT / 2, HAT, 0.045)
        if b % 4 in (1, 3):
            add(rhy, x, SNARE, 0.05)
    if b % 2 == 0:
        add(rhy, x, BASS[BASSES[(b // 8) % 4]], 0.16 if rythme_actif(x) else 0.08)
    b += 1

# ---------------- souffles et impacts sur les transitions ----------------
def souffle(dur):
    n = int(dur * SR)
    out, lp = [0.0] * n, 0.0
    for i in range(n):
        p = i / n
        a = 0.02 + 0.98 * p ** 2.2 if p < 0.85 else (1 - (p - 0.85) / 0.15)
        lp += (0.02 + 0.5 * p) * (rnd.uniform(-1, 1) - lp)
        out[i] = lp * a
    return out


def impact():
    n = int(1.1 * SR)
    return [math.sin(2 * math.pi * (38 + 30 * math.exp(-i / SR * 6)) * i / SR) * math.exp(-i / SR * 3.2)
            for i in range(n)]


WH, IMP = souffle(0.65), impact()
transitions = [(t0, typ) for nom, t0, typ in SCENES if typ]
s9 = next(t0 for nom, t0, typ in SCENES if nom == "s9")
transitions += [(s9 + m, "vpush") for m in MEGA_T[1:]]
for t0, typ in transitions:
    add(rhy, t0 - 0.5, WH, 0.10 if typ != "blur" else 0.06)
    if typ == "blocks":
        add(rhy, t0 + 0.05, IMP, 0.32)

# ---------------- mixage ----------------
mix_l = array.array("f", [0.0]) * N
mix_r = array.array("f", [0.0]) * N
fade_in, fade_out = int(1.5 * SR), int(3.0 * SR)
for i in range(N):
    g = 1.0
    if i < fade_in:
        g = i / fade_in
    elif i > N - fade_out:
        g = max(0.0, (N - i) / fade_out)
    mix_l[i] = (pad_l[i] + rhy[i]) * g
    mix_r[i] = (pad_r[i] + rhy[i]) * g
crete = max(max(abs(x) for x in mix_l), max(abs(x) for x in mix_r))
norm = 0.89 / crete
os.makedirs(os.path.join(HERE, "video", "audio"), exist_ok=True)
sortie = os.path.join(HERE, "video", "audio", "bande_son.wav")
frames = array.array("h", [0]) * (2 * N)
for i in range(N):
    frames[2 * i] = int(math.tanh(mix_l[i] * norm * 1.1) / math.tanh(1.1) * 32000)
    frames[2 * i + 1] = int(math.tanh(mix_r[i] * norm * 1.1) / math.tanh(1.1) * 32000)
with wave.open(sortie, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(frames.tobytes())
print(f"{sortie} : {TOTAL} s, crête avant normalisation {crete:.3f}")
