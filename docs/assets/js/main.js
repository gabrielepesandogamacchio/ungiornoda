// Un giorno da… — comportamento del sito (nessuna libreria)
(() => {
  const ridotto = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Testata: diventa piena quando si esce dall'apertura
  const testata = document.querySelector("[data-testata]");
  const apertura = document.querySelector(".apertura");
  if (testata && apertura && "IntersectionObserver" in window) {
    new IntersectionObserver(([e]) => {
      testata.classList.toggle("is-solida", !e.isIntersecting);
    }, { rootMargin: "-80px 0px 0px 0px" }).observe(apertura);
  }

  // Video di apertura: pausa / riprendi, fermo se l'utente ha chiesto meno movimento
  const video = document.querySelector("[data-video]");
  const pausa = document.querySelector("[data-pausa]");
  const pausaTesto = document.querySelector("[data-pausa-testo]");
  const segnaPausa = (inPausa) => {
    if (!pausa) return;
    pausa.setAttribute("aria-pressed", String(inPausa));
    pausaTesto.textContent = inPausa ? "Riprendi il video" : "Metti in pausa il video";
  };
  if (video) {
    if (ridotto) {
      video.removeAttribute("autoplay");
      video.pause();
      segnaPausa(true);
    }
    pausa?.addEventListener("click", () => {
      if (video.paused) { video.play(); segnaPausa(false); }
      else { video.pause(); segnaPausa(true); }
    });
    // non consumare batteria quando il video non si vede
    if ("IntersectionObserver" in window) {
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
    // il video di sfondo si ferma mentre si guarda la sigla
    if (video && !video.paused) { video.pause(); segnaPausa(true); }
    v.play().catch(() => {});
    v.focus();
  };
  document.querySelector("[data-sigla]")?.addEventListener("click", apriSigla);
  document.querySelector("[data-apri-sigla]")?.addEventListener("click", (ev) => {
    ev.preventDefault();
    document.getElementById("sigla")?.scrollIntoView({ behavior: ridotto ? "auto" : "smooth", block: "center" });
    setTimeout(apriSigla, ridotto ? 0 : 650);
  });

  // Prima stagione: segna il prossimo episodio in base alla data di oggi
  const puntate = [...document.querySelectorAll("[data-mese]")];
  const oggi = new Date();
  const meseOggi = oggi.getFullYear() * 12 + oggi.getMonth();
  const prossima = puntate.find((p) => {
    const [a, m] = p.dataset.mese.split("-").map(Number);
    return a * 12 + (m - 1) >= meseOggi;
  });
  prossima?.classList.add("is-prossima");

  // Prima stagione: niente spoiler
  const nota = document.querySelector("[data-nota]");
  const battute = [
    (m) => `Niente spoiler. Si scopre a ${m}.`,
    (m) => `Ancora segreto. Appuntamento a ${m}.`,
    (m) => `Ci hai provato. Lo vedi a ${m}.`,
  ];
  let giro = 0;
  document.querySelectorAll("[data-segreto]").forEach((b) => {
    b.addEventListener("click", () => {
      b.classList.remove("is-scossa");
      void b.offsetWidth; // riavvia l'animazione
      b.classList.add("is-scossa");
      const mese = b.dataset.segreto;
      const frase = battute[giro++ % battute.length](mese);
      if (nota) {
        nota.textContent = frase.replace(" a a", " ad a");
        nota.classList.add("is-attiva");
      }
    });
    b.addEventListener("animationend", () => b.classList.remove("is-scossa"));
  });

  // Contatti: copia l'indirizzo
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
