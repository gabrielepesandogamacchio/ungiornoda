#!/bin/bash
# Immagine di anteprima per i social (og.jpg) e icone PNG, renderizzate con Chrome headless.
set -e
cd "$(dirname "$0")"
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
P="$HOME/.hermes/cache/scratch/chrome-ugd"
IMG=../docs/assets/img
"$CH" --headless=new --user-data-dir="$P" --hide-scrollbars --allow-file-access-from-files --window-size=1200,630 --screenshot=/tmp/ugd_og.png "file://$PWD/og.html" 2>/dev/null
sips -s format jpeg -s formatOptions 82 /tmp/ugd_og.png --out $IMG/og.jpg >/dev/null
# Chrome ha una finestra minima: si renderizza a 512 px e si riduce con sips
"$CH" --headless=new --user-data-dir="$P" --hide-scrollbars --default-background-color=00000000 --window-size=512,512 --screenshot=/tmp/ugd_fav512.png "file://$PWD/fav.html" 2>/dev/null
sips -z 32 32 /tmp/ugd_fav512.png --out $IMG/favicon-32.png >/dev/null
sips -z 180 180 /tmp/ugd_fav512.png --out $IMG/apple-touch-icon.png >/dev/null
ls -la $IMG/og.jpg $IMG/favicon-32.png $IMG/apple-touch-icon.png
