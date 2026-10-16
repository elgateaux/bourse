#!/bin/sh
# Fabrique la vidéo du bilan avec HyperFrames : voix, musique, composition, rendu MP4.
#
# Usage : sh outils/video/fabriquer.sh SCREEN TRAVAIL SORTIE.mp4
#   SCREEN  dossier du screen (CSV du modèle et data/video_*.csv)
#   TRAVAIL dossier de travail hors du dépôt (projet HyperFrames assemblé)
# Variables : HYPERFRAMES (commande, défaut « hyperframes »), HYPERFRAMES_PYTHON (Python avec
# kokoro-onnx et soundfile), HYPERFRAMES_BROWSER_PATH (Chrome sans interface), VOIX (ff_siwis), VITESSE (1.07).
set -eu
S=$1; T=$2; OUT=$(cd "$(dirname "$3")" && pwd)/$(basename "$3")
ICI=$(cd "$(dirname "$0")" && pwd)
HF=${HYPERFRAMES:-hyperframes}
VOIX=${VOIX:-ff_siwis}
VITESSE=${VITESSE:-1.07}
mkdir -p "$T"

# 1. Textes lus, puis voix de synthèse (Kokoro, locale), une scène par fichier
python3 "$ICI/build_video.py" textes "$S" "$T"
for f in "$T"/voix/*.txt; do
  w=${f%.txt}.wav
  [ -s "$w" ] && [ "$w" -nt "$f" ] && continue
  $HF tts "$f" -v "$VOIX" -s "$VITESSE" -o "$w" > /dev/null
done

# 2. Composition minutée sur la durée des voix, puis musique de la même durée
python3 "$ICI/build_video.py" html "$S" "$T"
python3 "$ICI/musique.py" "$(cat "$T/duree.txt")" "$T/musique.wav" -33

# 3. Ressources locales : polices et GSAP (depuis npm, sans CDN)
[ -f "$T/polices/polices.css" ] || python3 "$ICI/polices.py" "$T/polices"
if [ ! -f "$T/vendor/gsap.min.js" ]; then
  mkdir -p "$T/vendor" "$T/.npm"
  (cd "$T/.npm" && npm pack gsap@3.14.2 --silent > /dev/null && tar -xzf gsap-3.14.2.tgz package/dist/gsap.min.js)
  cp "$T/.npm/package/dist/gsap.min.js" "$T/vendor/"
fi
printf '{\n  "id": "bilan-peg-video",\n  "name": "Bilan PEG en video"\n}\n' > "$T/meta.json"

# 4. Contrôle et rendu
(cd "$T" && $HF lint)
(cd "$T" && $HF render -o "$OUT" --fps 30 --crf 24 --quiet)
ffprobe -v error -show_entries format=duration,size -of compact "$OUT"
