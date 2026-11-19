// Un giorno da… — comportamento del sito (nessuna libreria)
(() => {
  const ridotto = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const hasIO = "IntersectionObserver" in window;

  // Testata: diventa piena (con il logo) quando si esce dall'apertura
  const testata = document.querySelector("[data-testata]");
  const apertura = document.querySelector(".apertura");
  if (testata && apertura && hasIO) {
    new IntersectionObserver(([e]) => {
      testata.classList.toggle("is-solida", !e.isIntersecting);
    }, { rootMargin: "-90px 0px 0px 0px" }).observe(apertura);
  }

  // Voce di menu della sezione che si sta leggendo
  const voci = [...document.querySelectorAll(".testata__nav a:not(.testata__scrivi)")];
  if (hasIO && voci.length) {
    const perId = new Map(voci.map((a) => [a.getAttribute("href").slice(1), a]));
    const obs = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        voci.forEach((v) => v.removeAttribute("aria-current"));
        perId.get(e.target.id)?.setAttribute("aria-current", "true");
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    perId.forEach((_, id) => { const el = document.getElementById(id); if (el) obs.observe(el); });
  }

  // Video di apertura: pausa / riprendi; fermo se l'utente chiede meno movimento
  const video = document.querySelector("[data-video]");
  const pausa = document.querySelector("[data-pausa]");
  const pausaTesto = document.querySelector("[data-pausa-testo]");
  const segnaPausa = (inPausa) => {
    if (!pausa) return;
    pausa.setAttribute("aria-pressed", String(inPausa));
    pausaTesto.textContent = inPausa ? "Riprendi il video" : "Metti in pausa il video";
  };
  if (video) {
    if (ridotto) { video.removeAttribute("autoplay"); video.pause(); segnaPausa(true); }
    pausa?.addEventListener("click", () => {
      if (video.paused) { video.play(); segnaPausa(false); }
      else { video.pause(); segnaPausa(true); }
    });
    if (hasIO) {
      new IntersectionObserver(([e]) => {
        if (pausa?.getAttribute("aria-pressed") === "true") return;
        if (e.isIntersecting) video.play().catch(() => {});
        else video.pause();
      }).observe(video);
    }
  }

  // Sigla: il video (con audio) si carica solo quando si preme play
  const apriSigla = () => {
    const btn = document.querySelector("[data-sigla]");
    if (!btn) return;
    const v = document.createElement("video");
    v.src = btn.dataset.src;
    v.poster = btn.querySelector("img")?.src || "";
    v.controls = true;
    v.playsInline = true;
    v.setAttribute("aria-label", "Sigla di Un giorno da");
    btn.replaceWith(v);
    if (video && !video.paused) { video.pause(); segnaPausa(true); }
    v.play().catch(() => {});
    v.focus();
  };
  document.querySelector("[data-sigla]")?.addEventListener("click", apriSigla);
  document.querySelector("[data-apri-sigla]")?.addEventListener("click", (ev) => {
    ev.preventDefault();
    document.getElementById("sigla")?.scrollIntoView({ behavior: ridotto ? "auto" : "smooth", block: "center" });
    setTimeout(apriSigla, ridotto ? 0 : 700);
  });

  // Prima stagione: segna il prossimo episodio in base alla data di oggi
  const meseOggi = new Date().getFullYear() * 12 + new Date().getMonth();
  [...document.querySelectorAll("[data-mese]")].find((p) => {
    const [a, m] = p.dataset.mese.split("-").map(Number);
    return a * 12 + (m - 1) >= meseOggi;
  })?.classList.add("is-prossima");

  // Prima stagione: niente spoiler
  const nota = document.querySelector("[data-nota]");
  const battute = [
    (m) => `Niente spoiler. Si scopre ${m}.`,
    (m) => `Ancora segreto. Appuntamento ${m}.`,
    (m) => `Ci hai provato. Lo vedi ${m}.`,
  ];
  let giro = 0;
  document.querySelectorAll("[data-segreto]").forEach((b) => {
    b.addEventListener("click", () => {
      b.classList.remove("is-scossa");
      void b.offsetWidth; // riavvia l'animazione
      b.classList.add("is-scossa");
      const mese = b.dataset.segreto;
      const quando = (/^[aeiou]/.test(mese) ? "ad " : "a ") + mese;
      if (nota) {
        nota.textContent = battute[giro++ % battute.length](quando);
        nota.classList.add("is-attiva");
      }
    });
    b.addEventListener("animationend", () => b.classList.remove("is-scossa"));
  });

  // Scrivici: copia l'indirizzo
  const copia = document.querySelector("[data-copia]");
  const copiaTesto = document.querySelector("[data-copia-testo]");
  copia?.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(copia.dataset.copia);
      copiaTesto.textContent = "Indirizzo copiato";
      copia.classList.add("is-fatto");
    } catch {
      copiaTesto.textContent = "Copia non riuscita: seleziona l'indirizzo qui sopra";
    }
    setTimeout(() => {
      copiaTesto.textContent = "Copia l'indirizzo";
      copia.classList.remove("is-fatto");
    }, 2600);
  });
})();
