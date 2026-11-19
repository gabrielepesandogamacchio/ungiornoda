"""Mini-builder per disegnare pagine web in VectorCraft con vectorcraft-cli (comandi in batch).

- testi veri (modificabili), in Bricolage Grotesque; il logo: simbolo in tracciati + scritta in Paquito Bold (testo vivo)
- le altezze dei paragrafi si stimano con PIL sullo stesso font, per impilare i blocchi
"""
import json
import os
import subprocess
import sys

from PIL import ImageFont

LOGO = os.path.expanduser("~/Desktop/UN_Giorno_DA/logo_prove")
CLI = LOGO + "/tools/vectorcraft-cli-0.23.0-macos-universal/vectorcraft-cli"
MK = json.load(open(LOGO + "/script/mark_rifinito.json"))
TM = json.load(open(LOGO + "/script/text_metrics.json"))
WORD_MET = TM["Paquito|Bold|-20|100|un giorno da"]   # dx, dy, w, h a 100 pt (inchiostro)

# ---- colori (manuale del logo)
ARANCIO = "#EA6525"; NERO = "#000000"; INK = "#141414"; BIANCO = "#FFFFFF"; CARTA = "#F4F1EC"
GRIGIO_CARTA = "#57524C"; GRIGIO_NERO = "#ABABAB"; RIGA_CARTA = "#D3CDC4"; RIGA_NERO = "#3A3A3A"
NOTE = "#8C8C8C"

FAM = "Bricolage Grotesque"
TITOLO = (FAM, "96pt ExtraBold")
XB = (FAM, "ExtraBold")
SB = (FAM, "SemiBold")
MED = (FAM, "Medium")
REG = (FAM, "Regular")

_TTF = os.path.expanduser("~/Library/Fonts/BricolageGrotesque[opsz,wdth,wght].ttf")
_PIL = {}


def pil(font, size):
    k = (font, round(size))
    if k not in _PIL:
        f = ImageFont.truetype(_TTF, round(size))
        f.set_variation_by_name(font[1].encode())
        _PIL[k] = f
    return _PIL[k]


def width(text, font, size, tracking=0):
    f = pil(font, size)
    return f.getlength(text) + tracking / 1000 * size * max(len(text) - 1, 0)


def wrap(text, font, size, w, tracking=0):
    lines = []
    for par in text.split("\n"):
        cur = ""
        for word in par.split(" "):
            t = (cur + " " + word).strip()
            if width(t, font, size, tracking) <= w * 0.985 or not cur:
                cur = t
            else:
                lines.append(cur); cur = word
        lines.append(cur)
    return lines


def svg_doc(paths, w, h, vbw, vbh):
    body = "".join(f'<path fill-rule="evenodd" fill="{f}" d="{d}"/>' for d, f in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}pt" height="{h}pt" '
            f'viewBox="0 0 {vbw} {vbh}">{body}</svg>')


class Doc:
    def __init__(self, title, out_path):
        self.out_path = out_path
        self.c = []
        self.add("file.new", {"width": 100, "height": 100, "units": "Pixels", "colorMode": "rgb",
                              "name": title, "rasterEffectsPpi": 72})
        self.add("layer.setProps", {"name": "Pagina"})
        self.artboards = []

    def add(self, cmd, params=None):
        self.c.append((cmd, params or {}))
        return len(self.c) - 1

    @staticmethod
    def ref(step, key="id"):
        return f"${step}.{key}"

    def name(self, step, name, key="id"):
        if name:
            if key == "ids":
                self.add("object.setProps", {"ids": self.ref(step, "ids"), "name": name})
            else:
                self.add("object.setProps", {"id": self.ref(step), "name": name})

    # ---- tavole
    def artboard(self, name, x, y, w, h):
        if not self.artboards:
            self.add("artboard.setProps", {"index": 0, "x": x, "y": y, "width": w, "height": h, "name": name})
        else:
            self.add("artboard.new", {"x": x, "y": y, "width": w, "height": h, "name": name})
        self.artboards.append((name, x, y, w, h))
        return len(self.artboards) - 1

    # ---- forme
    def _paint(self, s, fill, stroke=None, sw=None, opacity=None):
        rid = self.ref(s)
        if fill is None:
            self.add("paint.setFill", {"id": rid, "none": True})
        elif isinstance(fill, dict):
            self.add("paint.setFill", {"id": rid, "gradient": fill})
        else:
            self.add("paint.setFill", {"id": rid, "color": fill})
        if stroke is None:
            self.add("paint.setStroke", {"id": rid, "none": True})
        else:
            self.add("paint.setStroke", {"id": rid, "color": stroke})
            self.add("select.set", {"ids": [rid]})
            self.add("stroke.set", {"weight": sw or 1})
        if opacity is not None:
            self.add("object.setProps", {"id": rid, "opacity": opacity})

    def rect(self, x, y, w, h, fill=None, stroke=None, sw=None, radius=None, opacity=None, name=None):
        p = {"x": x, "y": y, "width": w, "height": h}
        if radius:
            p["radius"] = radius
        s = self.add("shape.rectangle", p)
        self._paint(s, fill, stroke, sw, opacity)
        self.name(s, name)
        return s

    def ellipse(self, x, y, w, h, fill=None, stroke=None, sw=None, opacity=None, name=None):
        s = self.add("shape.ellipse", {"x": x, "y": y, "width": w, "height": h})
        self._paint(s, fill, stroke, sw, opacity)
        self.name(s, name)
        return s

    def gradient(self, x, y, w, h, a_top, a_bottom, color=NERO, name="velo"):
        # angle -90: stop 0 in alto, stop 1 in basso
        g = {"kind": "linear", "angle": -90,
             "stops": [{"offset": 0, "color": color, "opacity": a_top},
                       {"offset": 1, "color": color, "opacity": a_bottom}]}
        return self.rect(x, y, w, h, fill=g, name=name)

    def radial(self, x, y, w, h, a=0.6, color=NERO, name="velo centrale"):
        """Rettangolo con sfumatura radiale dal centro (scuro) ai bordi (trasparente): nessun bordo visibile."""
        g = {"kind": "radial", "stops": [{"offset": 0, "color": color, "opacity": a},
                                          {"offset": 0.45, "color": color, "opacity": a * 0.55},
                                          {"offset": 1, "color": color, "opacity": 0}]}
        return self.rect(x, y, w, h, fill=g, name=name)

    def hline(self, x, y, w, color, t=1, name=None):
        return self.rect(x, y, w, t, fill=color, name=name)

    def vline(self, x, y, h, color, t=1, name=None):
        return self.rect(x, y, t, h, fill=color, name=name)

    # ---- testo
    def text(self, x, y, txt, size, color, font, justify="left", tracking=None, name=None):
        """Testo su una riga. y = linea di base."""
        txt = txt.replace("'", "\u2019")
        s = self.add("text.create", {"x": x, "y": y, "text": txt, "size": size, "font": font[0],
                                     "style": font[1], "color": color, "justify": justify})
        if tracking:
            self.add("text.setStyle", {"id": self.ref(s), "tracking": tracking})
        self.name(s, name or txt[:40])
        return s

    def para(self, x, top, w, txt, size, color, font, leading=None, tracking=None, name=None, justify="left"):
        """Paragrafo in un'area di testo larga w (altezza automatica). Ritorna l'altezza stimata."""
        leading = leading or round(size * 1.4, 1)
        txt = txt.replace("'", "\u2019")
        n = len(wrap(txt, font, size, w, tracking or 0))
        h = n * leading
        s = self.add("text.create", {"x": x, "y": top, "text": txt, "size": size, "font": font[0],
                                     "style": font[1], "color": color, "justify": justify,
                                     "area": {"width": w, "height": h + leading, "fit": "autoHeight"}})
        st = {"id": self.ref(s), "leading": leading}
        if tracking:
            st["tracking"] = tracking
        self.add("text.setStyle", st)
        self.add("text.areaOptions", {"id": self.ref(s), "firstBaseline": "capHeight"})
        self.name(s, name or txt[:40])
        # altezza visiva: dalla cima delle maiuscole alla linea di base dell'ultima riga
        return (n - 1) * leading + 0.72 * size

    # ---- immagini
    def image(self, path, x, y, w, h, name=None):
        s = self.add("file.place", {"path": path, "rect": [x, y, w, h], "link": False})
        self.name(s, name or os.path.basename(path), key="ids")
        return s

    # ---- vettoriali
    def svg(self, svg, cx, cy, name):
        self.add("clipboard.importSvg", {"svg": svg, "center": [cx, cy]})
        p = self.add("edit.pasteInPlace")
        g = self.add("object.group", {"ids": self.ref(p, "ids")})
        self.name(g, name)
        return g

    def mark(self, x, y, w=None, h=None, style="color", name="simbolo"):
        s = (w / MK["W"]) if w else (h / MK["H"])
        W, H = MK["W"] * s, MK["H"] * s
        paths = {"color": [(MK["mono"], ARANCIO), (MK["white"], BIANCO)],
                 "orange": [(MK["mono"], ARANCIO)], "white": [(MK["mono"], BIANCO)],
                 "black": [(MK["mono"], INK)]}[style]
        self.svg(svg_doc(paths, W, H, MK["W"], MK["H"]), x + W / 2, y + H / 2, name)
        return W, H

    def word(self, x, top, W, color=BIANCO, align="left", name="scritta un giorno da"):
        """Scritta 'un giorno da' (Paquito Bold, spaziatura -20, spazi +100) larga W sull'inchiostro."""
        dx, dy, iw, ih = WORD_MET
        size = 100 * W / iw
        k = size / 100
        left = x - (W / 2 if align == "center" else 0)
        s = self.add("text.create", {"x": left - dx * k, "y": top - dy * k, "text": "un giorno da",
                                     "size": size, "font": "Paquito", "style": "Bold", "color": color})
        self.add("text.setStyle", {"id": self.ref(s), "tracking": -20})
        for j in (2, 9):
            self.add("text.setStyle", {"id": self.ref(s), "tracking": 100, "start": j, "end": j + 1})
        self.name(s, name)
        return ih * k

    @staticmethod
    def word_h(W):
        return W * WORD_MET[3] / WORD_MET[2]

    def lockup_v(self, xc, top, W, word_color=BIANCO, mark_style="color"):
        mw = 0.75 * W
        mh = mw * MK["H"] / MK["W"]
        self.mark(xc - mw / 2, top, w=mw, style=mark_style)
        wh = self.word(xc, top + mh + 0.09 * W, W, word_color, align="center")
        return mh + 0.09 * W + wh

    def lockup_h(self, x, top, Hm, word_color=BIANCO, mark_style="color"):
        mw = Hm * MK["W"] / MK["H"]
        self.mark(x, top, h=Hm, style=mark_style)
        W = 1.95 * mw
        wh = self.word_h(W)
        self.word(x + mw + 0.22 * Hm, top + 0.66 * Hm - wh / 2, W, word_color)
        return mw + 0.22 * Hm + W

    # ---- livelli, note, salvataggio
    def layer(self, name):
        self.add("layer.new", {"name": name, "top": True})

    def note(self, ab, lines):
        _, x, y, w, h = self.artboards[ab]
        yy = y + h + 56
        for i, ln in enumerate(lines):
            self.text(x, yy, ln, 26 if i == 0 else 21, NOTE, (FAM, "Bold" if i == 0 else "Regular"),
                      name="nota")
            yy += 40 if i == 0 else 32

    def save(self, png_dir, tag):
        self.add("select.none")
        self.add("file.saveAs", {"path": self.out_path, "pdfCompatible": False})
        os.makedirs(png_dir, exist_ok=True)
        self.add("document.export", {"path": os.path.join(png_dir, tag + ".png"), "format": "png",
                                     "useArtboards": True, "ppi": 72})
        path = os.path.join(os.environ.get("TMPDIR", "/tmp"), f"vc_{tag}.json")
        json.dump([{"command": c, "params": p} for c, p in self.c], open(path, "w"))
        r = subprocess.run([CLI, "run", "--commands", path], capture_output=True, text=True)
        out = []
        for line in r.stdout.splitlines():
            try:
                out.append(json.loads(line))
            except Exception:
                out.append({"raw": line})
        warn = [o for o in out if isinstance(o, dict) and "warning" in json.dumps(o.get("result", {}))]
        for o in warn[:5]:
            print("WARN", json.dumps(o)[:300])
        if r.returncode != 0:
            print("STDERR:", r.stderr[-2500:])
            for o in out[-3:]:
                print(str(o)[:1200])
            sys.exit("run failed")
        print("steps:", len(self.c))
        return out
