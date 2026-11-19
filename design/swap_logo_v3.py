"""v2 (modificata da Gabriele) -> v3: stesso layout, logo originale di Paola ("prima") al posto di quello rifinito.

- ogni gruppo "simbolo" -> simbolo originale, stessa altezza, stesso angolo in alto a sinistra
- ogni testo "scritta un giorno da" -> scritta originale in tracciati, stessa altezza d'inchiostro e stesso inizio
- nelle due aperture il blocco simbolo+scritta viene ricentrato
Uso: python3 design/swap_logo_v3.py
"""
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
CLI = os.path.expanduser("~/Desktop/UN_Giorno_DA/logo_prove/tools/vectorcraft-cli-0.23.0-macos-universal/vectorcraft-cli")
SRC = os.path.join(HERE, "UGD_sito_v2.vectorcraft")
OUT = os.path.join(HERE, "UGD_sito_v3.vectorcraft")
PNG = os.path.join(HERE, "png_v3")
LOGO = os.path.join(HERE, "..", "tools", "logo_originale")


def load(name):
    s = open(os.path.join(LOGO, name)).read()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    body = s[s.index("<g id=\"Layer_1\""):s.rindex("</svg>")]
    return vb[2], vb[3], body


MW, MH, MBODY = load("simbolo.svg")
WW, WH, WBODY = load("scritta.svg")


def svg(body, vw, vh, w, h, color=None):
    if color:
        body = body.replace('fill="#ffffff"', f'fill="{color}"')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}pt" height="{h}pt" viewBox="0 0 {vw} {vh}">'
            f'{body}</svg>')


def run(cmds):
    p = os.path.join(os.environ.get("TMPDIR", "/tmp"), "vc_swap.json")
    json.dump([{"command": c, "params": q} for c, q in cmds], open(p, "w"))
    r = subprocess.run([CLI, "run", "--commands", p], capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2000:]); raise SystemExit(1)
    return [json.loads(l) for l in r.stdout.splitlines() if l.startswith("{")]


# 1) trova gli oggetti del logo
out = run([("document.open", {"path": SRC}), ("document.inspect", {"depth": 20, "childLimit": 10000})])
tree = [o for o in out if o.get("command") == "document.inspect"][0]["result"]


def walk(n, layer):
    yield n, layer
    for c in n.get("children", []) or []:
        yield from walk(c, layer)


marks, words = [], []
for L in tree["layers"]:
    for n, _ in walk(L, L["name"]):
        if n.get("kind") == "Group" and n.get("name") == "simbolo":
            marks.append((n["id"], n["bounds"], L["name"]))
        if n.get("kind") == "Type" and n.get("name") == "scritta un giorno da":
            words.append((n["id"], n["bounds"], L["name"]))
print(len(marks), "simboli,", len(words), "scritte")

# colore e corpo delle scritte
q = [("document.open", {"path": SRC})] + [("text.getRange", {"id": i, "effective": True}) for i, _, _ in words]
res = [o["result"] for o in run(q) if o.get("command") == "text.getRange"]

cmds = [("document.open", {"path": SRC})]
placed = {}   # layer -> lista di (kind, left, top, w, h)


def place(svgtxt, left, top, w, h, name):
    cmds.append(("clipboard.importSvg", {"svg": svgtxt, "center": [left + w / 2, top + h / 2]}))
    p = len(cmds)
    cmds.append(("edit.pasteInPlace", {}))
    cmds.append(("object.group", {"ids": f"${p}.ids"}))
    g = len(cmds) - 1
    cmds.append(("object.setProps", {"id": f"${g}.id", "name": name}))
    return g


for i, b, layer in marks:
    h = b["height"]
    w = h * MW / MH
    cmds += [("select.set", {"ids": [i]}), ("edit.clear", {})]
    g = place(svg(MBODY, MW, MH, w, h), b["x"], b["y"], w, h, "simbolo (originale)")
    placed.setdefault(layer, []).append(("m", g, b["x"], b["y"], w, h))

for (i, b, layer), r in zip(words, res):
    st = r["runs"][0]["style"]
    size = st["size"]
    color = (st.get("fill") or {}).get("color") if isinstance(st.get("fill"), dict) else st.get("fill")
    color = color if isinstance(color, str) and color.startswith("#") else "#FFFFFF"
    ink_left = b["x"] + 0.008 * size
    ink_top = b["y"] + 0.347 * size
    h = 0.95 * size
    w = h * WW / WH
    cmds += [("select.set", {"ids": [i]}), ("edit.clear", {})]
    g = place(svg(WBODY, WW, WH, w, h, None if color.upper() == "#FFFFFF" else color), ink_left, ink_top, w, h,
              "scritta un giorno da (originale)")
    placed.setdefault(layer, []).append(("w", g, ink_left, ink_top, w, h))

# 2) aperture: ricentra il blocco simbolo + scritta (quelli vicino al centro, non il simbolo della testata)
for layer, xc in [("01 Apertura", 720), ("Telefono · Apertura", 1860 + 195)]:
    items = [p for p in placed.get(layer, []) if p[3] > 200]
    if not items:
        continue
    x0 = min(p[2] for p in items); x1 = max(p[2] + p[4] for p in items)
    dx = xc - (x0 + x1) / 2
    for p in items:
        cmds.append(("object.transform", {"ids": [f"${p[1]}.id"], "matrix": [1, 0, 0, 1, dx, 0]}))

cmds += [("select.none", {}), ("file.saveAs", {"path": OUT, "pdfCompatible": False})]
os.makedirs(PNG, exist_ok=True)
cmds.append(("document.export", {"path": os.path.join(PNG, "v3.png"), "format": "png", "useArtboards": True, "ppi": 72}))
out = run(cmds)
print("ok", OUT)

# 3) piede: stesse proporzioni del blocco dell'apertura (scritta alta 0,58 x simbolo, allineata in basso, spazio 0,22 x simbolo)
out = run([("document.open", {"path": OUT}), ("document.inspect", {"depth": 20, "childLimit": 10000})])
tree = [o for o in out if o.get("command") == "document.inspect"][0]["result"]
piede = [L for L in tree["layers"] if L["name"] == "08 Piede"][0]
m = [n for n, _ in walk(piede, "") if n.get("name") == "simbolo (originale)"][0]["bounds"]
w = [n for n, _ in walk(piede, "") if n.get("name") == "scritta un giorno da (originale)"][0]
wb = w["bounds"]
h_new = 0.58 * m["height"]
s = h_new / wb["height"]
left = m["x"] + m["width"] + 0.22 * m["height"]
top = m["y"] + m["height"] - h_new
cmds = [("document.open", {"path": OUT}),
        ("object.transform", {"ids": [w["id"]], "matrix": [s, 0, 0, s, left - s * wb["x"], top - s * wb["y"]]}),
        ("select.none", {}), ("file.saveAs", {"path": OUT, "pdfCompatible": False}),
        ("document.export", {"path": os.path.join(PNG, "v3.png"), "format": "png", "useArtboards": True, "ppi": 72})]
run(cmds)
print("piede ok")
