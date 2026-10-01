#!/bin/sh
# Enveloppe BILAN.html comme le fera la publication (apercu.html) et pour l'impression A4 (impression.html).
# Usage : sh emballer.sh <dossier de l'analyse> <dossier de sortie>
S=$1
D=${2:-.}
mkdir -p "$D"
TETE='<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
{ printf '%s' "$TETE"; printf '%s' '<style>:root{color-scheme:light}body{margin:0}img{max-width:100%}</style>'; cat "$S/BILAN.html"; } > "$D/apercu.html"
{ printf '%s' "$TETE"; printf '%s' '<style>@page{size:A4;margin:13mm 12mm 15mm}:root{color-scheme:light}body{margin:0}img{max-width:100%}</style>'; cat "$S/BILAN.html"; } > "$D/impression.html"
