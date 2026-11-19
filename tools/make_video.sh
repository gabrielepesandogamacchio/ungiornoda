#!/bin/bash
# Video di sfondo dell'apertura (PROVVISORIO: spezzoni della sigla, https://youtu.be/MVeWe8grijE).
# Uso: tools/make_video.sh <video sorgente> ["inizio:fine inizio:fine ..."]
# Esempio con una clip nuova di Riccardo:  tools/make_video.sh clip.mov "0:12"
# La sigla ha i sottotitoli impressi in basso: si taglia il 14% inferiore del fotogramma (CROP_H).
# Scrive docs/assets/video/hero-1080.mp4, hero-540.mp4 e docs/assets/img/poster-*.jpg
set -e
SRC="$1"
SEGS="${2:-23.3:27.6 33.0:37.8 5.2:8.6 14.0:16.8 28.0:31.5}"
POSTER_AT="${POSTER_AT:-2.5}"
CROP_H="${CROP_H:-0.86}"     # quota di altezza tenuta (1 = nessun taglio)   # secondo del video finale usato come immagine fissa
cd "$(dirname "$0")/.."
OUT=docs/assets/video; IMG=docs/assets/img
ins=(); fc=""; n=0
for s in $SEGS; do
  ins+=(-ss "${s%:*}" -to "${s#*:}" -i "$SRC")
  fc="$fc[$n:v]fps=25,setpts=PTS-STARTPTS[a$n];"; n=$((n+1))
done
for ((i=0;i<n;i++)); do fc="$fc[a$i]"; done
fc="${fc}concat=n=$n:v=1:a=0,crop=iw:trunc(ih*$CROP_H/2)*2:0:0,scale=1920:-2:flags=lanczos,format=yuv420p[o]"
ffmpeg -v error -y "${ins[@]}" -filter_complex "$fc" -map "[o]" -an \
  -c:v libx264 -preset slow -crf 30 -profile:v high -movflags +faststart $OUT/hero-1080.mp4
ffmpeg -v error -y -i $OUT/hero-1080.mp4 -vf scale=960:-2 -an \
  -c:v libx264 -preset slow -crf 29 -movflags +faststart $OUT/hero-540.mp4
ffmpeg -v error -y -ss "$POSTER_AT" -i $OUT/hero-1080.mp4 -frames:v 1 -q:v 4 $IMG/poster-1920.jpg
ffmpeg -v error -y -ss "$POSTER_AT" -i $OUT/hero-1080.mp4 -frames:v 1 -vf scale=960:-2 -q:v 4 $IMG/poster-960.jpg
ls -la $OUT $IMG/poster-*.jpg
