#!/usr/bin/env python3
"""Musique de fond de la vidéo, synthétisée par calcul (bibliothèque standard uniquement).

Usage : musique.py DUREE_S SORTIE.wav [RMS_DBFS]

Nappe d'accords en la mineur (la m, fa, do, sol), basse douce sur les temps 1 et 3 et arpège
léger, à 76 battements par minute. Fondu d'entrée et de sortie. Le niveau moyen est réglé sur
RMS_DBFS (−30 dBFS par défaut) pour rester loin sous la voix. Tout est déterministe : aucune
source aléatoire, aucun échantillon externe.
"""
import array
import math
import sys
import wave

DUREE = float(sys.argv[1])
SORTIE = sys.argv[2]
RMS_CIBLE = float(sys.argv[3]) if len(sys.argv) > 3 else -30.0

SR = 32000
BPM = 76
TEMPS = 60 / BPM
MESURE = 4 * TEMPS
# accords en notes MIDI (nappe), et fondamentale de la basse
ACCORDS = [((57, 60, 64), 45), ((53, 57, 60), 41), ((48, 52, 55), 36), ((55, 59, 62), 43)]
TABLE_N = 4096
TABLE = [math.sin(2 * math.pi * i / TABLE_N) for i in range(TABLE_N)]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def osc(phase):
    return TABLE[int(phase * TABLE_N) % TABLE_N]


n = int(DUREE * SR)
gauche = [0.0] * n
droite = [0.0] * n
X = 0.7  # fondu enchaîné entre deux accords, en secondes

for i in range(n):
    t = i / SR
    k = int(t / MESURE)
    dans = t - k * MESURE
    # nappe : accord courant, et le précédent qui s'efface pendant X secondes
    l = r = 0.0
    for kk, g in ((k, min(1.0, dans / X)), (k - 1, max(0.0, 1 - dans / X))):
        if g <= 0 or kk < 0:
            continue
        g = 0.5 - 0.5 * math.cos(math.pi * g)
        notes, _ = ACCORDS[kk % 4]
        for m in notes:
            f = hz(m)
            l += g * (osc(f * t) + 0.25 * osc(2 * f * t)) * 0.16
            r += g * (osc(f * 1.003 * t) + 0.25 * osc(2.006 * f * t)) * 0.16
    # basse : temps 1 et 3
    temps = dans / TEMPS
    dt = (temps % 2) * TEMPS
    fb = hz(ACCORDS[k % 4][1])
    b = (osc(fb * t) + 0.3 * osc(2 * fb * t)) * math.exp(-2.2 * dt) * 0.35
    l += b
    r += b
    # arpège en croches, après l'introduction et avant la fin
    if 8.0 < t < DUREE - 6.0:
        croche = int(dans / (TEMPS / 2))
        da = dans - croche * TEMPS / 2
        notes, _ = ACCORDS[k % 4]
        m = notes[(0, 1, 2, 1)[croche % 4]] + 12
        a = osc(hz(m) * t) * math.exp(-7.0 * da) * 0.10
        l += a * (0.8 if croche % 2 else 1.0)
        r += a * (1.0 if croche % 2 else 0.8)
    # fondus d'entrée (3 s) et de sortie (4 s)
    fg = min(1.0, t / 3.0, (DUREE - t) / 4.0)
    gauche[i] = l * fg
    droite[i] = r * fg

rms = math.sqrt(sum(v * v for v in gauche) / n)
gain = 10 ** (RMS_CIBLE / 20) / rms
pic = max(max(abs(v) for v in gauche), max(abs(v) for v in droite)) * gain
assert pic < 1.0, pic
out = array.array("h")
for a, b in zip(gauche, droite):
    out.append(int(round(a * gain * 32767)))
    out.append(int(round(b * gain * 32767)))
with wave.open(SORTIE, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(out.tobytes())
print(f"musique : {DUREE:.1f} s, RMS {RMS_CIBLE:.0f} dBFS, pic {20 * math.log10(pic):.1f} dBFS")
