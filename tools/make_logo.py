"""Genera i loghi SVG del sito dal logo definitivo.

Fonti:
- simbolo: ~/Desktop/UN_Giorno_DA/logo_prove/script/mark_rifinito.json (tracciati del logo rifinito)
- scritta: Paquito Bold, spaziatura -20 (spazi +100), convertita in tracciati
- proporzioni: le stesse di build_rifinito.py (RATIO, GAP_V, H_WORD, H_GAP, H_CENTER)

Uso: python3 tools/make_logo.py   (scrive in docs/assets/img/)
"""
import json
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "docs", "assets", "img")
MK = json.load(open(os.path.expanduser(
    "~/Desktop/UN_Giorno_DA/logo_prove/script/mark_rifinito.json")))
FONT = os.path.expanduser("~/Library/Fonts/Paquito-Bold.otf")

ORANGE, WHITE, INK = "#EA6525", "#FFFFFF", "#141414"
RATIO, GAP_V = 0.75, 0.09
H_WORD, H_GAP, H_CENTER = 1.95, 0.22, 0.66


def wordmark(text="un giorno da", tracking=-20, spaces=100):
    """Ritorna (d, x0, y0, w, h) della scritta in unità font, y verso il basso."""
    f = TTFont(FONT)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f["head"].unitsPerEm
    hmtx = f["hmtx"]
    pen = SVGPathPen(gs)
    bounds = BoundsPen(gs)
    x = 0
    for ch in text:
        g = cmap[ord(ch)]
        # y in giù: scala (1, -1)
        for p in (pen, bounds):
            tp = TransformPen(p, (1, 0, 0, -1, x, 0))
            gs[g].draw(tp)
        adv = hmtx[g][0]
        x += adv + (spaces if ch == " " else tracking) * upm / 1000
    x0, y0, x1, y1 = bounds.bounds
    return pen.getCommands(), x0, y0, x1 - x0, y1 - y0


def mark_paths(style):
    if style == "color":
        return [(MK["mono"], ORANGE), (MK["white"], WHITE)]
    if style == "orange":
        return [(MK["mono"], ORANGE)]
    if style == "white":
        return [(MK["mono"], WHITE)]
    raise ValueError(style)


def g_paths(paths, tx, ty, s):
    body = "".join(f'<path fill-rule="evenodd" fill="{f}" d="{d}"/>' for d, f in paths)
    return f'<g transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})">{body}</g>'


def svg_doc(w, h, inner, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{inner}</svg>\n')


def word_g(d, x0, y0, s, tx, ty, color):
    return (f'<g transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f}) translate({-x0:.2f} {-y0:.2f})">'
            f'<path fill="{color}" d="{d}"/></g>')


def lockup_vertical(style="color", word_color=WHITE, W=1000):
    d, x0, y0, ww, wh = wordmark()
    sw = W / ww
    Wh = wh * sw
    mw = RATIO * W
    sm = mw / MK["W"]
    mh = MK["H"] * sm
    gap = GAP_V * W
    H = mh + gap + Wh
    inner = g_paths(mark_paths(style), (W - mw) / 2, 0, sm)
    inner += word_g(d, x0, y0, sw, 0, mh + gap, word_color)
    return svg_doc(W, H, inner, "un giorno da")


def lockup_horizontal(style="color", word_color=WHITE, Hm=100):
    d, x0, y0, ww, wh = wordmark()
    sm = Hm / MK["H"]
    mw = MK["W"] * sm
    Ww = H_WORD * mw
    sw = Ww / ww
    Wh = wh * sw
    gap = H_GAP * Hm
    W = mw + gap + Ww
    inner = g_paths(mark_paths(style), 0, 0, sm)
    inner += word_g(d, x0, y0, sw, mw + gap, H_CENTER * Hm - Wh / 2, word_color)
    return svg_doc(W, Hm, inner, "un giorno da")


def word_only(color=WHITE, H=100):
    d, x0, y0, ww, wh = wordmark()
    s = H / wh
    return svg_doc(ww * s, H, word_g(d, x0, y0, s, 0, 0, color), "un giorno da")


def mark_only(style="color", H=100):
    s = H / MK["H"]
    return svg_doc(MK["W"] * s, H, g_paths(mark_paths(style), 0, 0, s), "un giorno da")


def favicon():
    # simbolo arancio su quadrato nero arrotondato
    S = 64
    pad = 7
    s = (S - 2 * pad) / max(MK["W"], MK["H"])
    tx = (S - MK["W"] * s) / 2
    ty = (S - MK["H"] * s) / 2
    inner = f'<rect width="{S}" height="{S}" rx="14" fill="#000"/>' + g_paths(mark_paths("color"), tx, ty, s)
    return svg_doc(S, S, inner, "un giorno da")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    files = {
        "logo-verticale.svg": lockup_vertical("color", WHITE),
        "logo-orizzontale.svg": lockup_horizontal("color", WHITE),
        "logo-orizzontale-ink.svg": lockup_horizontal("orange", INK),
        "scritta-bianca.svg": word_only(WHITE),
        "scritta-ink.svg": word_only(INK),
        "simbolo.svg": mark_only("color"),
        "simbolo-bianco.svg": mark_only("white"),
        "favicon.svg": favicon(),
    }
    for name, s in files.items():
        open(os.path.join(OUT, name), "w").write(s)
        print(name, len(s))
