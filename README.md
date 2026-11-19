# ungiornoda.net

Sito vetrina della docuserie *Un giorno da…*. Pagina statica (HTML + CSS + un po' di JS, nessuna libreria), pubblicata con GitHub Pages dalla cartella `docs/`.

## Struttura
- `docs/index.html`: la pagina (apertura con video, il progetto + sigla, prima stagione, team, contatti)
- `docs/assets/css/style.css`: stile. Colori e caratteri dal manuale del logo (arancio `#EA6525`, Paquito Bold nel logo, Bricolage Grotesque nei testi)
- `docs/assets/js/main.js`: video, sigla, timeline senza spoiler, copia email
- `docs/assets/video/`: `hero-*.mp4` (loop di sfondo, senza audio), `sigla-1080.mp4` (sigla con audio)
- `tools/`: script per rigenerare loghi, video e immagini di anteprima

## Modificare
- **Testi:** direttamente in `docs/index.html`.
- **Episodi:** ogni episodio è un `<li class="puntata" data-mese="AAAA-MM">`. Il pallino "Il prossimo" si sposta da solo in base alla data.
- **Video di apertura:** `tools/make_video.sh <clip> "inizio:fine inizio:fine"` (taglia, comprime, crea il poster). Per una clip senza sottotitoli: `CROP_H=1 tools/make_video.sh clip.mov "0:15"`.
- **Loghi:** `python3 tools/make_logo.py` (dal logo rifinito in `logo_prove/`).
- **Anteprima social e icone:** `tools/make_social.sh`.

Provare in locale: `cd docs && python3 -m http.server 8765` → http://127.0.0.1:8765

## Dominio
GoDaddy → DNS di `ungiornoda.net`:
- 4 record **A** su `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- 1 record **CNAME** `www` → `gabrielepesandogamacchio.github.io`

Poi su GitHub: Settings → Pages → Custom domain `ungiornoda.net` → Enforce HTTPS.
I record MX/TXT dell'inoltro email non vanno toccati.
