"""Sito ungiornoda.net, versione 2: progetto in VectorCraft (desktop 1440 + telefono 390 + sistema).

Uso: python3 design/build_v2.py  ->  design/UGD_sito_v2.vectorcraft + design/png/
Il file .vectorcraft si modifica a mano nell'app; questo script serve solo a rigenerarlo da zero.
"""
import os

from vc import *

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img") + "/"
OUT = os.path.join(HERE, "UGD_sito_v2.vectorcraft")
PNG = os.path.join(HERE, "png")
SITE_IMG = os.path.join(HERE, "..", "docs", "assets", "img") + "/"
TEAM = os.path.expanduser("~/Desktop/UN_Giorno_DA/BCC/assets/tondo_{}.png")

# ---------------------------------------------------------------- griglia desktop
W = 1440
L, R = 168, 1344          # contenuto: a sinistra resta la colonna degli orari
CW = R - L                # 1176
COL, GUT = 76, 24


def cx(i):                # x della colonna i (0..11)
    return L + i * (COL + GUT)


def span(n):
    return n * COL + (n - 1) * GUT


GAP_AB = 360              # spazio verticale tra le tavole (per le note sotto)
MX = W + 420              # x delle tavole telefono
SX = MX + 390 + 420       # x della tavola "sistema"

TRI = '<svg xmlns="http://www.w3.org/2000/svg" width="{s}pt" height="{s}pt" viewBox="0 0 24 24"><path fill="{c}" d="M7 4.5v15l12.5-7.5z"/></svg>'
PAUSA = '<svg xmlns="http://www.w3.org/2000/svg" width="{s}pt" height="{s}pt" viewBox="0 0 24 24"><path fill="{c}" d="M6.5 4h4v16h-4zM13.5 4h4v16h-4z"/></svg>'
LUCCHETTO = open(SITE_IMG + "lucchetto.svg").read()


def lucchetto(d, x, y, h, color=NERO):
    s = LUCCHETTO.replace('viewBox="0 0 20 24"', f'width="{h * 20 / 24}pt" height="{h}pt" viewBox="0 0 20 24"')
    s = s.replace('fill="#000"', f'fill="{color}"')
    return d.svg(s, x + h * 10 / 24, y + h / 2, "lucchetto")


def pill(d, x, y, label, font=SB, size=17, fill=None, stroke=None, color=NERO, icon=None, h=52, pad=26,
         name="bottone"):
    """Bottone a pillola. Ritorna la larghezza."""
    tw = width(label, font, size)
    iw = 18 if icon else 0
    gap = 10 if icon else 0
    w = pad + iw + gap + tw + pad - (4 if icon else 0)
    d.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.5, radius=h / 2, name=name)
    tx = x + pad - (4 if icon else 0)
    if icon:
        d.svg(icon.format(s=iw, c=color), tx + iw / 2, y + h / 2, "icona")
        tx += iw + gap
    d.text(tx, y + h / 2 + size * 0.36, label, size, color, font, name=label)
    return w


def orario(d, top, h, ora, y_label, dark):
    """Colonna degli orari: la pagina è una giornata, come i capitoli degli episodi."""
    line = RIGA_NERO if dark else RIGA_CARTA
    d.vline(112, top, h, line, name="orario linea")
    d.ellipse(108, y_label - 9, 9, 9, fill=ARANCIO, name="orario punto")
    d.text(40, y_label, ora, 15, ARANCIO if dark else "#B4461A", MED, tracking=40, name="orario " + ora)


def sfondo(d, step):
    d.add("object.arrange.sendToBack", {"ids": [d.ref(step)]})


def rulecell(d, x, top, w, key, val, dark=False):
    """Voce della scheda: etichetta piccola + valore."""
    d.text(x, top + 34, key, 15, GRIGIO_NERO if dark else GRIGIO_CARTA, MED, name=key)
    h = d.para(x, top + 52, w, val, 23, BIANCO if dark else INK, SB, leading=30, tracking=-5)
    return 52 + h


# ================================================================ DESKTOP
def apertura(d, y):
    H = 900
    d.layer("01 Apertura")
    ab = d.artboard("Desktop 01 · Apertura (video)", 0, y, W, H)
    d.image(IMG + "hero_desk.jpg", 0, y, W, H, name="POSTER del video (nel sito: video in loop)")
    d.rect(0, y, W, H, fill=NERO, opacity=0.18, name="velo")
    d.gradient(0, y, W, 260, 0.6, 0.0, name="velo alto")
    d.gradient(0, y + H - 380, W, 380, 0.0, 0.88, name="velo basso")
    d.radial(0, y - 20, W, 920, 0.6)

    # testata: solo le voci, il logo è al centro
    px = R - 112
    d.rect(px, y + 28, 112, 42, stroke=ARANCIO, sw=1.5, radius=21, name="Scrivici (bordo)")
    d.text(px + 56, y + 55, "Scrivici", 16, BIANCO, SB, justify="center")
    labels = ["Il progetto", "Il format", "Prima stagione", "Team"]
    ws = [width(t, MED, 16) for t in labels]
    x = px - 40 - sum(ws) - 36 * (len(ws) - 1)
    for t, w_ in zip(labels, ws):
        d.text(x, y + 55, t, 16, BIANCO, MED)
        x += w_ + 36

    # logo, più piccolo: scritta larga 210 px (prima 470)
    Wl = 210
    lh = 0.75 * Wl * MK["H"] / MK["W"] + 0.09 * Wl + Doc.word_h(Wl)
    top = y + 440 - (lh + 56) / 2
    d.lockup_v(W / 2, top, Wl)
    d.text(W / 2, top + lh + 54, "UNA GIORNATA.   UN MESTIERE.   UN RACCONTO.", 13, BIANCO, MED,
           justify="center", tracking=260, name="motto")

    # piede dell'apertura
    by = y + H - 56
    d.text(96, by - 72, "La docuserie sul lavoro in Valle d'Aosta.", 20, BIANCO, REG, name="intro")
    pill(d, 96, by - 52, "Guarda la sigla", fill=ARANCIO, icon=TRI, color=NERO)
    d.text(R - 76, by - 32, "Prima stagione", 15, "#D6D6D6", MED, justify="right")
    d.text(R - 76, by - 2, "da dicembre 2026", 24, BIANCO, XB, justify="right", tracking=-10)
    d.ellipse(R - 52, by - 42, 52, 52, stroke="#BDBDBD", sw=1.5, name="pausa video")
    d.svg(PAUSA.format(s=16, c=BIANCO), R - 26, by - 16, "icona pausa")
    d.note(ab, ["Apertura: logo più piccolo (scritta 210 px invece di 470), centrato sul video.",
                "Il video resta a tutto schermo; qui c'è un fotogramma della sigla come segnaposto.",
                "La testata ha solo le voci: il logo orizzontale compare in alto a sinistra quando si scorre."])
    return H


def progetto(d, y):
    d.layer("02 Il progetto")
    top = y + 150
    th = d.para(L, top, span(8), "Che lavoro voglio fare, davvero?", 92, INK, TITOLO, leading=90, tracking=-25,
                name="titolo")
    t2 = top + th + 72
    h1 = d.para(cx(5), t2, span(7),
                "È la domanda che quasi tutti, prima o poi, si fanno: dopo la scuola, durante gli studi, nei primi "
                "anni di lavoro. Spesso non manca la voglia. Manca l'occasione di vedere un mestiere da vicino e di "
                "parlarne con chi lo fa ogni giorno.", 25, INK, REG, leading=36)
    h2 = d.para(cx(5), t2 + h1 + 40, span(7),
                "Un giorno da… è una docuserie girata in Valle d'Aosta. In ogni episodio Carlo passa una giornata "
                "intera dentro un mestiere: arriva quando si comincia, prova a fare quello che fanno gli altri e "
                "resta fino a fine turno.", 25, INK, REG, leading=36)
    # nota a margine, con la fonte
    d.hline(L, t2 - 4, span(4), ARANCIO, 2, name="nota riga")
    nh = d.para(L, t2 + 22, span(4) - 20,
                "In Valle d'Aosta il 10,3% dei ragazzi tra 15 e 29 anni non studia e non lavora. In Italia è il 15,2%.",
                18, INK, MED, leading=26)
    d.para(L, t2 + 22 + nh + 20, span(4) - 20,
           "Fonte: Istat, Il benessere equo e sostenibile dei territori, Valle d'Aosta, dicembre 2025 (dati 2024).",
           14, GRIGIO_CARTA, REG, leading=20)
    # la serie in breve
    s0 = t2 + h1 + 40 + h2 + 130
    d.text(L, s0, "La serie in breve", 24, INK, SB, tracking=-10)
    d.hline(L, s0 + 24, CW, INK, 2, name="scheda riga")
    cells = [("Formato", "Docuserie per YouTube e i social"),
             ("Episodi", "Cinque, da circa 40 minuti"),
             ("Girata in", "Valle d'Aosta"),
             ("Per chi", "Chi ha tra 15 e 29 anni e sta scegliendo che lavoro fare"),
             ("Tono", "Diretto e reale. Niente attori, niente finzione"),
             ("Prima stagione", "Da dicembre 2026 ad agosto 2027")]
    rh = 0
    for i, (k, v) in enumerate(cells[:3]):
        rh = max(rh, rulecell(d, cx(i * 4), s0 + 24, span(4) - 24, k, v))
    r2 = s0 + 24 + rh + 34
    d.hline(L, r2, CW, RIGA_CARTA, 1, name="scheda riga 2")
    rh2 = 0
    for i, (k, v) in enumerate(cells[3:]):
        rh2 = max(rh2, rulecell(d, cx(i * 4), r2, span(4) - 24, k, v))
    H = (r2 + rh2 + 150) - y
    bg = d.rect(0, y, W, H, fill=CARTA, name="sfondo carta")
    sfondo(d, bg)
    orario(d, y, H, "07:00", top + 16, False)
    ab = d.artboard("Desktop 02 · Il progetto", 0, y, W, H)
    d.note(ab, ["Il progetto: si parte dalla domanda che c'è dietro la serie (dalla slide 'Da dove nasce').",
                "Nota a margine con il dato Istat e la fonte; poi la scheda della serie come i titoli di un documentario.",
                "Colonna degli orari a sinistra: la pagina scorre come una giornata (07:00 → 19:00). Facoltativa."])
    return H


def formato(d, y):
    d.layer("03 Il format")
    top = y + 150
    th = d.para(L, top, span(9), "Dentro il mestiere. Senza filtri.", 92, BIANCO, TITOLO, leading=90, tracking=-25,
                name="titolo")
    p0 = top + th + 80
    ph = span(8) * 9 / 16
    d.image(IMG + "sigla_poster.jpg", L, p0, span(8), ph, name="sigla (poster)")
    d.rect(L, p0, span(8), ph, fill=NERO, opacity=0.12, name="velo sigla")
    c = (L + span(8) / 2, p0 + ph / 2)
    d.ellipse(c[0] - 48, c[1] - 48, 96, 96, fill=ARANCIO, name="play")
    d.svg(TRI.format(s=34, c=NERO), c[0] + 3, c[1], "icona play")
    d.text(L, p0 + ph + 34, "La sigla, 44 secondi. Con l'audio.", 16, GRIGIO_NERO, MED)
    # tre pilastri a destra della sigla
    x = cx(8) + 12
    w = span(4) - 12
    yy = p0
    for head, body in [("Il lato professionale",
                        "Come funziona il mestiere nella pratica: gli strumenti, le competenze, una giornata tipo."),
                       ("Il lato umano",
                        "Il percorso dietro ogni scelta: dubbi, cambiamenti, sacrifici, e cosa ti fa sentire nel posto giusto."),
                       ("Niente finzione",
                        "Ritmo veloce, riprese immersive, qualità da documentario. Niente attori e nessun copione da recitare.")]:
        d.hline(x, yy, w, RIGA_NERO, 1)
        d.text(x, yy + 44, head, 25, BIANCO, SB, tracking=-10)
        bh = d.para(x, yy + 64, w, body, 17, GRIGIO_NERO, REG, leading=25)
        yy += 64 + bh + 34
    # striscia di fotogrammi
    s0 = max(p0 + ph + 34, yy) + 96
    fw = (CW - 4 * 16) / 5
    fh = fw * 5 / 4
    for i, f in enumerate(["7.2", "10.5", "20.0", "23.6", "37.2"]):
        d.image(IMG + f"strip_{f}.jpg", L + i * (fw + 16), s0, fw, fh, name=f"fotogramma {f}s")
    d.text(L, s0 + fh + 34, "Fotogrammi dalla sigla.", 16, GRIGIO_NERO, MED)
    H = (s0 + fh + 34 + 150) - y
    bg = d.rect(0, y, W, H, fill=NERO, name="sfondo nero")
    sfondo(d, bg)
    orario(d, y, H, "09:30", top + 16, True)
    ab = d.artboard("Desktop 03 · Il format", 0, y, W, H)
    d.note(ab, ["Il format: la sigla diventa il pezzo forte della sezione (si apre lì, con l'audio).",
                "A destra i tre pilastri del format (dalla slide 'Il format'); sotto, fotogrammi della sigla.",
                "Le foto si sostituiscono con foto di scena di Riccardo quando ci sono."])
    return H


def episodio(d, y):
    d.layer("04 Come nasce un episodio")
    top = y + 150
    th = d.para(L, top, span(7), "Come nasce un episodio", 92, INK, TITOLO, leading=90, tracking=-25, name="titolo")
    lh = d.para(cx(7) + 12, top + 6, span(5) - 12,
                "Per ogni episodio servono tre cose: una realtà che apre le porte, un mestiere da raccontare e "
                "chi lo fa ogni giorno.", 23, INK, REG, leading=33)
    s0 = top + max(th, lh) + 110
    sw_ = (CW - 4 * 24) / 5
    steps = [("Incontro", "Con la realtà che ci apre le porte scegliamo mestieri, persone e luoghi."),
             ("Scrittura", "Copione e scaletta: le tappe della giornata e cosa mettere in risalto."),
             ("Riprese", "Più giornate di riprese per raccontare una sola giornata sullo schermo."),
             ("Montaggio", "Circa 40 minuti di episodio, più le clip brevi per i social."),
             ("Uscita", "L'episodio su YouTube, teaser e clip sui social, incontri nelle scuole.")]
    mh = 0
    for i, (h_, b) in enumerate(steps):
        x = L + i * (sw_ + 24)
        d.hline(x, s0, sw_, INK, 4, name=f"passo {i + 1} riga")
        d.text(x, s0 + 40, f"{i + 1:02d}", 16, "#B4461A", MED, tracking=40)
        d.text(x, s0 + 86, h_, 30, INK, XB, tracking=-20)
        bh = d.para(x, s0 + 108, sw_ - 10, b, 17, GRIGIO_CARTA, REG, leading=25)
        mh = max(mh, 108 + bh)
    H = (s0 + mh + 150) - y
    bg = d.rect(0, y, W, H, fill=CARTA, name="sfondo carta")
    sfondo(d, bg)
    orario(d, y, H, "12:00", top + 16, False)
    ab = d.artboard("Desktop 04 · Come nasce un episodio", 0, y, W, H)
    d.note(ab, ["Come nasce un episodio: i cinque passi della slide del CdA, in ordine (qui i numeri hanno senso).",
                "Serve a chi pensa di aprirci le porte: capisce subito cosa gli chiediamo."])
    return H


MESI = ["Dicembre", "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto"]


def stagione(d, y):
    d.layer("05 Prima stagione")
    top = y + 150
    th = d.para(L, top, span(6), "Prima stagione", 92, BIANCO, TITOLO, leading=90, tracking=-25, name="titolo")
    d.para(cx(7) + 12, top + 6, span(5) - 12,
           "Cinque episodi, uno ogni due mesi. I mestieri restano segreti fino all'uscita: per ora possiamo dirvi "
           "solo quando.", 23, "#D6D6D6", REG, leading=33)
    ly = top + th + 230
    cw_ = 206
    step = (CW - cw_) / 8
    d.hline(L, ly, CW, "#4A4A4A", 2, name="linea del tempo")
    for i in range(9):
        x = L + i * step
        if i % 2:
            d.vline(x, ly - 5, 12, "#4A4A4A", 2, name="tacca " + MESI[i])
            d.text(x, ly + 28, MESI[i][:3].lower(), 13, "#7A7A7A", MED, justify="center")
    for k in range(5):
        i = 2 * k
        x = L + i * step
        anno = "2026" if i == 0 else "2027"
        d.text(x, ly - 88, anno, 15, GRIGIO_NERO, MED, tracking=60)
        d.text(x, ly - 34, MESI[i], 40, BIANCO, TITOLO, tracking=-25)
        if k == 0:
            d.ellipse(x - 14, ly - 13, 28, 28, fill=ARANCIO, opacity=0.25, name="alone prossimo")
            d.ellipse(x - 8, ly - 7, 16, 16, fill=ARANCIO, name="punto prossimo")
            tw = width("IL PROSSIMO", MED, 11, 180)
            d.rect(x + 50, ly - 106, tw + 22, 24, stroke=ARANCIO, sw=1.5, radius=12, name="etichetta prossimo")
            d.text(x + 61, ly - 89.5, "IL PROSSIMO", 11, ARANCIO, MED, tracking=180)
        else:
            d.ellipse(x - 8, ly - 7, 16, 16, fill=NERO, stroke=ARANCIO, sw=2, name="punto episodio")
        c0 = ly + 48
        d.text(x, c0 + 12, f"Episodio {k + 1}", 15, GRIGIO_NERO, MED)
        d.word(x, c0 + 34, 150, BIANCO)
        d.rect(x, c0 + 34 + Doc.word_h(150) + 14, cw_, 58, fill=ARANCIO, radius=3, name="mestiere segreto")
        lucchetto(d, x + cw_ - 34, c0 + 34 + Doc.word_h(150) + 14 + 19, 20, NERO)
    cb = ly + 48 + 34 + Doc.word_h(150) + 14 + 58
    d.text(L, cb + 46, "Tocca un mestiere per provare a sbirciare.", 16, GRIGIO_NERO, MED, name="suggerimento")
    # oltre agli episodi
    o0 = cb + 160
    d.text(L, o0, "Oltre agli episodi", 30, BIANCO, XB, tracking=-20)
    mh = 0
    for i, (h_, b) in enumerate([
            ("Sui social", "Teaser prima di ogni uscita, clip brevi dagli episodi e rubriche pensate per il telefono."),
            ("Nelle scuole", "Incontri nelle ore di orientamento delle superiori, da dicembre a maggio."),
            ("Dal vivo", "Una serata di lancio con la prima visione, a dicembre, e una serata finale a fine stagione.")]):
        x = cx(i * 4)
        d.hline(x, o0 + 34, span(4) - 24, RIGA_NERO, 1)
        d.text(x, o0 + 78, h_, 24, BIANCO, SB, tracking=-10)
        bh = d.para(x, o0 + 98, span(4) - 44, b, 17, GRIGIO_NERO, REG, leading=25)
        mh = max(mh, 98 + bh)
    H = (o0 + mh + 150) - y
    bg = d.rect(0, y, W, H, fill=NERO, name="sfondo nero")
    sfondo(d, bg)
    orario(d, y, H, "14:30", top + 16, True)
    ab = d.artboard("Desktop 05 · Prima stagione", 0, y, W, H)
    d.note(ab, ["Prima stagione: linea del tempo da dicembre ad agosto, senza nessun mestiere (date dal Gantt su Notion).",
                "Ogni episodio è il titolo d'apertura del video con il mestiere coperto: 'un giorno da' + barra col lucchetto.",
                "'Dal vivo' (serata di lancio e finale) e 'Nelle scuole' vengono dal piano su Notion: DA CONFERMARE prima di pubblicare."])
    return H


def team(d, y):
    d.layer("06 Team")
    top = y + 150
    th = d.para(L, top, span(5), "Chi la fa", 92, INK, TITOLO, leading=90, tracking=-25, name="titolo")
    d.para(cx(6), top + 6, span(6),
           "Siamo in tre. Carlo va sul posto e ci mette la faccia, Riccardo riprende e monta, Gabriele scrive gli "
           "episodi e segue la parte tecnica.", 23, INK, REG, leading=33)
    p0 = top + th + 110
    people = [("riccardo", "Riccardo Fiou", "Videomaker e produttore",
               "Videomaker freelance, laureato in Ingegneria del Cinema al Politecnico di Torino. Ha lavorato con "
               "Golden Goose, Adidas, AW LAB e con la Regione per «Aosta capitale della cultura»."),
              ("carlo", "Carlo Giordano", "Conduttore e protagonista della serie",
               "Entra nei mestieri, li vive e li racconta in prima persona. Libero professionista nelle politiche "
               "giovanili: progettazione e mobilità internazionale con Erasmus+."),
              ("gabriele", "Gabriele Pesando", "Autore e parte tecnica",
               "Ricercatore, laurea magistrale in Intelligenza Artificiale alla Statale di Milano. Consulente in "
               "progetti di ricerca applicata e sviluppo software.")]
    mh = 0
    for i, (k, n, r, b) in enumerate(people):
        x = cx(i * 4)
        d.image(TEAM.format(k), x, p0, 210, 210, name=n)
        d.text(x, p0 + 210 + 62, n, 34, INK, TITOLO, tracking=-20)
        d.text(x, p0 + 210 + 96, r, 18, INK, SB)
        bh = d.para(x, p0 + 210 + 124, span(4) - 44, b, 17, GRIGIO_CARTA, REG, leading=25)
        mh = max(mh, 210 + 124 + bh)
    H = (p0 + mh + 150) - y
    bg = d.rect(0, y, W, H, fill=CARTA, name="sfondo carta")
    sfondo(d, bg)
    orario(d, y, H, "17:00", top + 16, False)
    ab = d.artboard("Desktop 06 · Team", 0, y, W, H)
    d.note(ab, ["Team: foto rotonde delle slide, ruolo e due righe di presentazione (dalla slide 'Chi siamo' del CdA).",
                "Le presentazioni erano scritte per la banca: rileggetele e decidete cosa tenere sul sito."])
    return H


def contatti(d, y):
    d.layer("07 Scrivici")
    top = y + 140
    d.text(L - 10, top + 190, "Scrivici.", 250, INK, TITOLO, tracking=-45, name="titolo")
    l0 = top + 300
    voci = [("Aziende e realtà del territorio",
             "Apriteci le porte per una giornata: scegliamo insieme mestieri, persone e luoghi."),
            ("Scuole", "Portiamo la serie in classe, nelle ore di orientamento."),
            ("Stampa, radio e tv", "Interviste, materiali e anteprime degli episodi."),
            ("Un'idea", "C'è un mestiere che vorresti vedere raccontato? Diccelo.")]
    nl = max(len(wrap(h_, SB, 23, span(3) - 24, -10)) for h_, _ in voci)
    hh = (nl - 1) * 28 + 0.72 * 23
    mh = 0
    for i, (h_, b) in enumerate(voci):
        x = cx(i * 3)
        d.hline(x, l0, span(3) - 12, INK, 2)
        d.para(x, l0 + 26, span(3) - 24, h_, 23, INK, SB, leading=28, tracking=-10)
        bh = d.para(x, l0 + 26 + hh + 22, span(3) - 24, b, 17, INK, REG, leading=25)
        mh = max(mh, 26 + hh + 22 + bh)
    e0 = l0 + mh + 170
    ew = width("team@ungiornoda.net", TITOLO, 112, -40)
    d.text(L - 4, e0, "team@ungiornoda.net", 112, INK, TITOLO, tracking=-40, name="email")
    d.hline(L, e0 + 30, ew, INK, 4, name="sottolineatura email")
    pill(d, L, e0 + 72, "Copia l'indirizzo", stroke=INK, color=INK)
    H = (e0 + 72 + 52 + 140) - y
    bg = d.rect(0, y, W, H, fill=ARANCIO, name="sfondo arancio")
    sfondo(d, bg)
    d.vline(112, y, H, "#C9561F", name="orario linea")
    d.text(40, top + 16, "19:00", 15, INK, MED, tracking=40)
    ab = d.artboard("Desktop 07 · Scrivici", 0, y, W, H)
    d.note(ab, ["Scrivici: quattro motivi per scrivere, ognuno con cosa succede dopo. L'indirizzo è il bottone principale."])
    return H


def piede(d, y):
    d.layer("08 Piede")
    H = 320
    d.rect(0, y, W, H, fill=NERO, name="sfondo nero")
    d.lockup_h(L, y + 80, 56)
    cols = [("Seguici", "YouTube, Instagram e TikTok:\ni link arrivano a breve."),
            ("Contatti", "team@ungiornoda.net"),
            ("Dove", "Girata in Valle d'Aosta.")]
    for i, (h_, b) in enumerate(cols):
        x = cx(6 + i * 2)
        d.text(x, y + 98, h_, 16, BIANCO, SB)
        d.para(x, y + 116, span(2) - 8, b, 15, GRIGIO_NERO, REG, leading=22)
    d.hline(L, y + 220, CW, RIGA_NERO, 1)
    d.text(L, y + 264, "© 2026 Un giorno da", 14, "#8A8A8A", REG)
    d.text(R, y + 264, "Logo di Paola Feder", 14, "#8A8A8A", REG, justify="right")
    d.vline(112, y, H, RIGA_NERO, name="orario linea")
    d.text(40, y + 98, "21:00", 15, ARANCIO, MED, tracking=40)
    ab = d.artboard("Desktop 08 · Piede", 0, y, W, H)
    d.note(ab, ["Piede: logo orizzontale, social (quando ci sono i link), crediti del logo."])
    return H


# ================================================================ TELEFONO
MW, ML = 390, 22
MC = MW - 2 * ML


def m_apertura(d, y):
    H = 844
    d.layer("Telefono · Apertura")
    x0 = MX
    d.image(IMG + "hero_mob.jpg", x0, y, MW, H, name="POSTER del video")
    d.rect(x0, y, MW, H, fill=NERO, opacity=0.18)
    d.gradient(x0, y, MW, 200, 0.6, 0.0)
    d.gradient(x0, y + H - 360, MW, 360, 0.0, 0.9)
    d.radial(x0 - 60, y + 20, MW + 120, 600, 0.6)
    d.rect(x0 + MW - ML - 96, y + 22, 96, 38, stroke=ARANCIO, sw=1.5, radius=19)
    d.text(x0 + MW - ML - 48, y + 46.5, "Scrivici", 15, BIANCO, SB, justify="center")
    Wl = 168
    lh = 0.75 * Wl * MK["H"] / MK["W"] + 0.09 * Wl + Doc.word_h(Wl)
    top = y + 300 - lh / 2
    d.lockup_v(x0 + MW / 2, top, Wl)
    for i, t in enumerate(["UNA GIORNATA.", "UN MESTIERE.", "UN RACCONTO."]):
        d.text(x0 + MW / 2, top + lh + 46 + i * 24, t, 12, BIANCO, MED, justify="center", tracking=240)
    by = y + H - 34
    d.para(x0 + ML, by - 150, MC - 60, "La docuserie sul lavoro in Valle d'Aosta. Prima stagione da dicembre 2026.",
           17, BIANCO, REG, leading=24)
    pill(d, x0 + ML, by - 52, "Guarda la sigla", fill=ARANCIO, icon=TRI, color=NERO, size=16)
    d.ellipse(x0 + MW - ML - 48, by - 50, 48, 48, stroke="#BDBDBD", sw=1.5)
    d.svg(PAUSA.format(s=15, c=BIANCO), x0 + MW - ML - 24, by - 26, "icona pausa")
    ab = d.artboard("Telefono 01 · Apertura", x0, y, MW, H)
    d.note(ab, ["Telefono: logo largo 168 px,", "motto su tre righe."])
    return H


def m_progetto(d, y):
    d.layer("Telefono · Il progetto")
    x0 = MX + ML
    top = y + 84
    d.text(x0, top, "07:00", 14, "#B4461A", MED, tracking=40)
    th = d.para(x0, top + 26, MC, "Che lavoro voglio fare, davvero?", 46, INK, TITOLO, leading=46, tracking=-20)
    yy = top + 26 + th + 40
    for t in ["È la domanda che quasi tutti, prima o poi, si fanno. Spesso non manca la voglia: manca l'occasione "
              "di vedere un mestiere da vicino.",
              "Un giorno da… è una docuserie girata in Valle d'Aosta. In ogni episodio Carlo passa una giornata "
              "intera dentro un mestiere, dalla prima ora all'ultima."]:
        yy += d.para(x0, yy, MC, t, 19, INK, REG, leading=28) + 28
    d.hline(x0, yy + 8, MC, ARANCIO, 2)
    yy += 8 + 22
    yy += d.para(x0, yy, MC, "In Valle d'Aosta il 10,3% dei ragazzi tra 15 e 29 anni non studia e non lavora. "
                 "In Italia è il 15,2%.", 16, INK, MED, leading=23) + 14
    yy += d.para(x0, yy, MC, "Fonte: Istat, BES dei territori, Valle d'Aosta, dic. 2025 (dati 2024).", 13,
                 GRIGIO_CARTA, REG, leading=18) + 64
    d.text(x0, yy, "La serie in breve", 21, INK, SB)
    yy += 20
    d.hline(x0, yy, MC, INK, 2)
    for k, v in [("Formato", "Docuserie per YouTube e i social"), ("Episodi", "Cinque, da circa 40 minuti"),
                 ("Girata in", "Valle d'Aosta"), ("Per chi", "Chi ha tra 15 e 29 anni e sta scegliendo che lavoro fare"),
                 ("Tono", "Diretto e reale. Niente attori, niente finzione"),
                 ("Prima stagione", "Da dicembre 2026 ad agosto 2027")]:
        d.text(x0, yy + 30, k, 14, GRIGIO_CARTA, MED)
        vh = d.para(x0, yy + 44, MC, v, 19, INK, SB, leading=25)
        yy += 44 + vh + 20
        d.hline(x0, yy, MC, RIGA_CARTA, 1)
    H = yy + 90 - y
    bg = d.rect(MX, y, MW, H, fill=CARTA)
    sfondo(d, bg)
    ab = d.artboard("Telefono 02 · Il progetto", MX, y, MW, H)
    d.note(ab, ["L'orario va sopra il titolo,", "la scheda diventa un elenco."])
    return H


def m_stagione(d, y):
    d.layer("Telefono · Prima stagione")
    x0 = MX + ML
    top = y + 84
    d.text(x0, top, "14:30", 14, ARANCIO, MED, tracking=40)
    th = d.para(x0, top + 26, MC, "Prima stagione", 46, BIANCO, TITOLO, leading=46, tracking=-20)
    yy = top + 26 + th + 34
    yy += d.para(x0, yy, MC, "Cinque episodi, uno ogni due mesi. I mestieri restano segreti fino all'uscita.", 18,
                 "#D6D6D6", REG, leading=26) + 56
    lx = x0 + 7
    start = yy
    for k in range(5):
        mese = MESI[2 * k]
        anno = "2026" if k == 0 else "2027"
        if k == 0:
            d.ellipse(lx - 13, yy - 13, 26, 26, fill=ARANCIO, opacity=0.25)
            d.ellipse(lx - 7, yy - 7, 14, 14, fill=ARANCIO)
        else:
            d.ellipse(lx - 7, yy - 7, 14, 14, fill=NERO, stroke=ARANCIO, sw=2)
        tx = x0 + 34
        d.text(tx, yy + 12, mese, 32, BIANCO, TITOLO, tracking=-20)
        d.text(tx + width(mese, TITOLO, 32, -20) + 10, yy + 12, anno, 14, GRIGIO_NERO, MED, tracking=60)
        d.text(tx, yy + 44, f"Episodio {k + 1}" + ("  ·  il prossimo" if k == 0 else ""), 14,
               ARANCIO if k == 0 else GRIGIO_NERO, MED)
        d.word(tx, yy + 62, 128, BIANCO)
        bw = MC - 34
        d.rect(tx, yy + 62 + Doc.word_h(128) + 12, bw, 48, fill=ARANCIO, radius=3)
        lucchetto(d, tx + bw - 30, yy + 62 + Doc.word_h(128) + 12 + 15, 18, NERO)
        yy += 62 + Doc.word_h(128) + 12 + 48 + 58
    sfondo(d, d.vline(lx - 1, start, yy - 58 - start - 60, "#4A4A4A", 2))
    yy += 10
    d.text(x0, yy, "Oltre agli episodi", 24, BIANCO, XB, tracking=-15)
    yy += 18
    for h_, b in [("Sui social", "Teaser, clip brevi dagli episodi e rubriche pensate per il telefono."),
                  ("Nelle scuole", "Incontri nelle ore di orientamento delle superiori, da dicembre a maggio."),
                  ("Dal vivo", "Serata di lancio con la prima visione, a dicembre, e serata finale.")]:
        d.hline(x0, yy + 14, MC, RIGA_NERO, 1)
        d.text(x0, yy + 50, h_, 20, BIANCO, SB)
        yy += 66 + d.para(x0, yy + 66, MC, b, 16, GRIGIO_NERO, REG, leading=23) + 12
    H = yy + 80 - y
    bg = d.rect(MX, y, MW, H, fill=NERO)
    sfondo(d, bg)
    ab = d.artboard("Telefono 05 · Prima stagione", MX, y, MW, H)
    d.note(ab, ["Sul telefono la linea del tempo", "diventa verticale."])
    return H


def m_team(d, y):
    d.layer("Telefono · Team")
    x0 = MX + ML
    top = y + 84
    d.text(x0, top, "17:00", 14, "#B4461A", MED, tracking=40)
    th = d.para(x0, top + 26, MC, "Chi la fa", 46, INK, TITOLO, leading=46, tracking=-20)
    yy = top + 26 + th + 34
    yy += d.para(x0, yy, MC, "Siamo in tre. Carlo va sul posto e ci mette la faccia, Riccardo riprende e monta, "
                 "Gabriele scrive gli episodi e segue la parte tecnica.", 18, INK, REG, leading=26) + 48
    for k, n, r, b in [("riccardo", "Riccardo Fiou", "Videomaker e produttore",
                        "Videomaker freelance, Ingegneria del Cinema al Politecnico di Torino."),
                       ("carlo", "Carlo Giordano", "Conduttore e protagonista",
                        "Entra nei mestieri, li vive e li racconta in prima persona."),
                       ("gabriele", "Gabriele Pesando", "Autore e parte tecnica",
                        "Ricercatore, laurea magistrale in Intelligenza Artificiale.")]:
        d.image(TEAM.format(k), x0, yy, 104, 104, name=n)
        d.text(x0 + 124, yy + 40, n, 24, INK, TITOLO, tracking=-15)
        d.text(x0 + 124, yy + 66, r, 15, INK, SB)
        d.para(x0 + 124, yy + 80, MC - 124, b, 14, GRIGIO_CARTA, REG, leading=20)
        yy += 104 + 34
    H = yy + 60 - y
    bg = d.rect(MX, y, MW, H, fill=CARTA)
    sfondo(d, bg)
    ab = d.artboard("Telefono 06 · Team", MX, y, MW, H)
    d.note(ab, ["Foto a sinistra, testo a destra;", "presentazioni accorciate."])
    return H


def m_contatti(d, y):
    d.layer("Telefono · Scrivici")
    x0 = MX + ML
    top = y + 70
    d.text(x0 - 4, top + 84, "Scrivici.", 104, INK, TITOLO, tracking=-40)
    yy = top + 140
    for h_, b in [("Aziende e realtà del territorio", "Apriteci le porte per una giornata."),
                  ("Scuole", "Portiamo la serie in classe."),
                  ("Stampa, radio e tv", "Interviste, materiali e anteprime."),
                  ("Un'idea", "C'è un mestiere che vorresti vedere? Diccelo.")]:
        d.hline(x0, yy, MC, INK, 2)
        d.text(x0, yy + 32, h_, 19, INK, SB)
        d.text(x0, yy + 58, b, 16, INK, REG)
        yy += 84
    yy += 50
    d.text(x0, yy, "team@ungiornoda.net", 33, INK, TITOLO, tracking=-30)
    d.hline(x0, yy + 11, width("team@ungiornoda.net", TITOLO, 33, -30), INK, 2)
    pill(d, x0, yy + 40, "Copia l'indirizzo", stroke=INK, color=INK, size=16, h=48)
    H = yy + 40 + 48 + 70 - y
    bg = d.rect(MX, y, MW, H, fill=ARANCIO)
    sfondo(d, bg)
    ab = d.artboard("Telefono 07 · Scrivici", MX, y, MW, H)
    d.note(ab, ["L'indirizzo resta grande", "e si copia con un tocco."])
    return H


# ================================================================ SISTEMA
def sistema(d, y):
    d.layer("Sistema")
    x0, Wd, H = SX, 1440, 1360
    d.rect(x0, y, Wd, H, fill=BIANCO)
    d.text(x0 + 80, y + 120, "Sistema", 72, INK, TITOLO, tracking=-25)
    d.para(x0 + 80, y + 150, 820,
           "Colori e caratteri vengono dal manuale del logo. Il logo (Paquito Bold) non si usa per i testi: "
           "titoli e testi sono in Bricolage Grotesque, lo stesso delle prove per il titolo del mestiere.",
           19, GRIGIO_CARTA, REG, leading=28)
    # colori
    cy = y + 290
    d.text(x0 + 80, cy, "Colori", 24, INK, SB)
    for i, (n, hx, txt) in enumerate([("Arancio", ARANCIO, NERO), ("Nero", NERO, BIANCO), ("Carta", CARTA, INK),
                                      ("Inchiostro", INK, BIANCO), ("Bianco", BIANCO, INK)]):
        x = x0 + 80 + i * 252
        d.rect(x, cy + 24, 230, 150, fill=hx, stroke="#DDDDDD" if hx in (BIANCO, CARTA) else None, sw=1)
        d.text(x + 18, cy + 24 + 104, n, 20, txt, SB)
        d.text(x + 18, cy + 24 + 130, hx, 14, txt, MED, tracking=40)
    # caratteri
    ty = cy + 260
    d.text(x0 + 80, ty, "Caratteri", 24, INK, SB)
    rows = [("Titolo · 92 px · 96pt ExtraBold", "Prima stagione", 92, TITOLO, -25),
            ("Lead · 25 px · Regular", "Una giornata intera dentro un mestiere.", 25, REG, 0),
            ("Voce · 25 px · SemiBold", "Il lato professionale", 25, SB, -10),
            ("Testo · 17 px · Regular", "Ritmo veloce, riprese immersive, qualità da documentario.", 17, REG, 0),
            ("Orario · 15 px · Medium", "07:00", 15, MED, 40)]
    yy = ty + 40
    for lab, sample, sz, f, tr in rows:
        d.text(x0 + 80, yy + 20, lab, 14, GRIGIO_CARTA, MED)
        d.text(x0 + 420, yy + max(sz * 0.8, 20), sample, sz, INK, f, tracking=tr or None)
        yy += max(sz * 1.05, 34) + 26
        d.hline(x0 + 80, yy - 12, 1280, "#E5E1DA", 1)
    # componenti
    ky = yy + 60
    d.text(x0 + 80, ky, "Componenti", 24, INK, SB)
    d.rect(x0 + 80, ky + 30, 640, 260, fill=NERO)
    pill(d, x0 + 110, ky + 60, "Guarda la sigla", fill=ARANCIO, icon=TRI, color=NERO)
    d.rect(x0 + 360, ky + 63, 112, 42, stroke=ARANCIO, sw=1.5, radius=21)
    d.text(x0 + 416, ky + 90, "Scrivici", 16, BIANCO, SB, justify="center")
    d.ellipse(x0 + 520, ky + 58, 52, 52, stroke="#BDBDBD", sw=1.5)
    d.svg(PAUSA.format(s=16, c=BIANCO), x0 + 546, ky + 84, "icona pausa")
    d.word(x0 + 110, ky + 140, 150, BIANCO)
    d.rect(x0 + 110, ky + 140 + Doc.word_h(150) + 14, 206, 58 - 8, fill=ARANCIO, radius=3)
    lucchetto(d, x0 + 110 + 206 - 34, ky + 140 + Doc.word_h(150) + 14 + 15, 20, NERO)
    d.para(x0 + 360, ky + 150, 330, "Mestiere segreto: la barra prende il posto del titolo del mestiere. "
           "Toccandola trema e dice quando esce.", 15, "#D6D6D6", REG, leading=21)
    d.rect(x0 + 760, ky + 30, 600, 260, fill=ARANCIO)
    pill(d, x0 + 790, ky + 60, "Copia l'indirizzo", stroke=INK, color=INK)
    d.para(x0 + 790, ky + 140, 520, "Su arancio si scrive in inchiostro, mai in bianco: il bianco sull'arancio "
           "non si legge abbastanza.", 15, INK, REG, leading=21)
    ab = d.artboard("Sistema · colori, caratteri, componenti", x0, y, Wd, H)
    return H


def main():
    d = Doc("Un giorno da · sito v2", OUT)
    y = 0
    ys = {}
    for key, fn in [("apertura", apertura), ("progetto", progetto), ("formato", formato), ("episodio", episodio),
                    ("stagione", stagione), ("team", team), ("contatti", contatti), ("piede", piede)]:
        ys[key] = y
        y += fn(d, y) + GAP_AB
    # telefono: allineate alla sezione corrispondente
    my = 0
    for fn in (m_apertura, m_progetto, m_stagione, m_team, m_contatti):
        my += fn(d, my) + 300
    sistema(d, 0)
    d.save(PNG, "UGD_sito_v2")


if __name__ == "__main__":
    main()
