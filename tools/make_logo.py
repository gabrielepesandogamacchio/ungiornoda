"""Loghi del sito dal logo ORIGINALE di Paola Feder (versione "prima", scelta da Gabriele).

Fonti in tools/logo_originale/ (esportate in SVG da "Logo Definitivo 2 (1).vectorcraft", variante V_arancio):
- simbolo.svg  (camaleonte + spirale, arancio e bianco)
- scritta.svg  ("un giorno da" in tracciati, bianca)
- V_arancio.svg (simbolo sopra la scritta)
Uso: python3 tools/make_logo.py  -> docs/assets/img/
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "logo_originale")
OUT = os.path.join(HERE, "..", "docs", "assets", "img")
INK = "#141414"


def load(name):
    s = open(os.path.join(SRC, name)).read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = s[s.index('<g id="Layer_1"'):s.rindex("</svg>")]
    body = body.replace(' id="Layer_1" data-name="Layer 1"', "")
    w, h = [float(v) for v in vb.split()[2:]]
    return w, h, body


def doc(w, h, body, title="un giorno da"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')


def main():
    os.makedirs(OUT, exist_ok=True)
    mw, mh, mark = load("simbolo.svg")
    ww, wh, word = load("scritta.svg")
    vw, vh, vert = load("V_arancio.svg")
    files = {
        "simbolo.svg": doc(mw, mh, mark),
        "scritta-bianca.svg": doc(ww, wh, word),
        "scritta-ink.svg": doc(ww, wh, word.replace('fill="#ffffff"', f'fill="{INK}"')),
        "logo-verticale.svg": doc(vw, vh, vert),
    }
    # favicon: simbolo su quadrato nero arrotondato
    S, pad = 64, 7
    s = (S - 2 * pad) / max(mw, mh)
    tx, ty = (S - mw * s) / 2, (S - mh * s) / 2
    files["favicon.svg"] = doc(S, S, f'<rect width="{S}" height="{S}" rx="14" fill="#000"/>'
                                     f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">{mark}</g>')
    for n, c in files.items():
        open(os.path.join(OUT, n), "w").write(c)
        print(n, len(c))
    for old in ("logo-orizzontale.svg", "logo-orizzontale-ink.svg", "simbolo-bianco.svg"):
        p = os.path.join(OUT, old)
        if os.path.exists(p):
            os.remove(p)
    print("simbolo", mw, mh, "scritta", ww, wh)


if __name__ == "__main__":
    main()
