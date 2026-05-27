/* =========================================================
   PRODUCT PRO — enhance pagine prodotto in stile MSI/Apple.
   Legge i dati dal markup esistente e aggiunge:
   - Hero ricco con badge brand + sigla modello prominente
   - Scroll showcase con visual pinned + step cascade
   - Bottone "Descrizione" che apre pannello dettagliato
   - Sezione "Vantaggi" con icone + descrizioni
   - Pull-quote citazione
   ========================================================= */
(() => {
  'use strict';

  // Esegui solo su pagine prodotto (.product main)
  const main = document.querySelector('main.product');
  if (!main) return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ——— 1. Estrai dati dal markup + (preferito) dal database ——— */
  function getSlugFromUrl() {
    const path = location.pathname;
    const last = path.split('/').pop() || '';
    return last.replace(/\.html$/, '');
  }

  function extract() {
    const titleEl = main.querySelector('.product__title');
    const brandEl = main.querySelector('.product__brand');
    const leadEl = main.querySelector('.product__lead');
    const descEl = main.querySelector('.product__desc');
    const mediaEl = main.querySelector('.product__media img');

    // 1) Cerca nel database
    const slug = getSlugFromUrl();
    const db = (window.BAZZANA_PRODUCTS || []).find(p => p.slug === slug);

    // 2) Estrai dal markup come fallback
    const specsFromDom = [];
    main.querySelectorAll('.spec').forEach(dl => {
      const dts = dl.querySelectorAll('dt');
      const dds = dl.querySelectorAll('dd');
      dts.forEach((dt, i) => {
        if (dds[i]) specsFromDom.push({ label: dt.textContent.trim(), value: dds[i].textContent.trim() });
      });
    });

    let model = '';
    let subtitle = '';
    if (titleEl) {
      const clone = titleEl.cloneNode(true);
      const em = clone.querySelector('em');
      if (em) {
        subtitle = em.textContent.trim();
        em.remove();
      }
      model = clone.textContent.replace(/\s+/g, ' ').trim();
    }

    let brand = '', category = '';
    if (brandEl) {
      const parts = brandEl.textContent.split('·').map(s => s.trim());
      brand = parts[0] || '';
      category = parts[1] || '';
    }

    return {
      brand: db?.brand || brand,
      category: db?.category || category,
      model: db?.model || model,
      modelFull: db?.modelFull || ((db?.brand || brand) + ' ' + (db?.model || model)).trim(),
      subtitle: db?.tagline || subtitle,
      lead: db?.lead || leadEl?.textContent.trim() || '',
      desc: db?.description || descEl?.textContent.trim() || '',
      mediaSrc: mediaEl?.getAttribute('src') || '',
      mediaAlt: mediaEl?.getAttribute('alt') || '',
      specs: (db?.specs && db.specs.length) ? db.specs : specsFromDom,
      highlights: db?.highlights || []
    };
  }

  /* ——— 2. Costruisce HTML enhanced ——— */
  function buildEnhancedHero(data) {
    const wrap = document.createElement('section');
    wrap.className = 'product-pro__hero';
    wrap.innerHTML = `
      <div class="product-pro__hero-bg" aria-hidden="true"></div>
      <div class="product-pro__hero-inner">
        <div class="product-pro__hero-text">
          <div class="product-pro__meta">
            <span class="product-pro__brand-chip">${data.brand}</span>
            ${data.category ? `<span class="product-pro__cat">${data.category}</span>` : ''}
          </div>
          <h1 class="product-pro__model">
            <span class="product-pro__model-num">${data.model}</span>
            ${data.subtitle ? `<em class="product-pro__model-sub">${data.subtitle}</em>` : ''}
          </h1>
          <p class="product-pro__lead">${data.lead}</p>
          <div class="product-pro__cta-row">
            <a class="product-pro__cta" href="https://wa.me/393464156981?text=Buongiorno%2C%20vorrei%20info%20sulla%20${encodeURIComponent(data.brand + ' ' + data.model)}" target="_blank" rel="noopener">
              <span>Chiedi disponibilità</span>
              <span class="product-pro__cta-arrow" aria-hidden="true">→</span>
            </a>
            <button class="product-pro__desc-toggle" data-toggle="desc" aria-expanded="false">
              <span>Descrizione completa</span>
              <span class="product-pro__plus" aria-hidden="true">+</span>
            </button>
          </div>
        </div>
        <div class="product-pro__hero-media">
          <div class="product-pro__hero-stage">
            <img src="${data.mediaSrc}" alt="${data.mediaAlt}" loading="eager">
          </div>
          <div class="product-pro__model-watermark" aria-hidden="true">${data.model}</div>
        </div>
      </div>
    `;
    return wrap;
  }

  function buildDescPanel(data) {
    const panel = document.createElement('section');
    panel.className = 'product-pro__desc-panel';
    panel.setAttribute('hidden', '');
    const specsHTML = data.specs.map(s => `<dt>${s.label}</dt><dd>${s.value}</dd>`).join('');
    panel.innerHTML = `
      <div class="product-pro__desc-inner">
        <div class="product-pro__desc-col">
          <span class="product-pro__desc-eyebrow">Descrizione tecnica</span>
          <h2 class="product-pro__desc-title">Cosa fa<br><em>${data.brand} ${data.model}</em></h2>
          <p class="product-pro__desc-body">${data.desc}</p>
        </div>
        <div class="product-pro__desc-col">
          <span class="product-pro__desc-eyebrow">Specifiche</span>
          <dl class="product-pro__desc-specs">${specsHTML}</dl>
        </div>
      </div>
    `;
    return panel;
  }

  function buildScrollShowcase(data) {
    const wrap = document.createElement('section');
    wrap.className = 'product-pro__showcase';
    // Preferenza: usa gli highlights specifici del prodotto; fallback alle specs
    let steps;
    if (data.highlights && data.highlights.length >= 3) {
      steps = data.highlights.slice(0, 3).map((h, i) => ({
        num: String(i + 1).padStart(2, '0'),
        label: h.title,
        value: h.value
      }));
    } else {
      steps = data.specs.slice(0, 3).map((s, i) => ({
        num: String(i + 1).padStart(2, '0'),
        label: s.label,
        value: s.value
      }));
    }
    if (steps.length < 3) {
      const fallback = [
        { num: '01', label: 'Costruito per durare', value: 'Materiali professionali, garanzia 2 anni.' },
        { num: '02', label: 'Officina autorizzata', value: 'Ricambi originali, assistenza in 48h.' },
        { num: '03', label: 'Prova in showroom', value: 'Cene · Val Seriana · su appuntamento.' }
      ];
      while (steps.length < 3) steps.push(fallback[steps.length]);
    }

    wrap.innerHTML = `
      <div class="product-pro__showcase-inner">
        <div class="product-pro__showcase-visual">
          <div class="product-pro__showcase-stage">
            <img src="${data.mediaSrc}" alt="${data.mediaAlt}" loading="lazy">
          </div>
          <div class="product-pro__showcase-num" aria-hidden="true">01</div>
        </div>
        <div class="product-pro__showcase-steps">
          <p class="product-pro__showcase-eyebrow">Perché questa, perché qui</p>
          <h2 class="product-pro__showcase-title">${data.brand}<br><em>${data.model}</em></h2>
          <ol class="product-pro__step-list">
            ${steps.map((s, i) => `
              <li class="product-pro__step" data-step="${i + 1}">
                <span class="product-pro__step-num">${s.num}</span>
                <h3 class="product-pro__step-label">${s.label}</h3>
                <p class="product-pro__step-value">${s.value}</p>
              </li>
            `).join('')}
          </ol>
        </div>
      </div>
    `;
    return wrap;
  }

  function buildCTAFinal(data) {
    const wrap = document.createElement('section');
    wrap.className = 'product-pro__cta-final';
    wrap.innerHTML = `
      <div class="product-pro__cta-final-inner">
        <p class="product-pro__cta-final-eyebrow">Disponibilità</p>
        <h2 class="product-pro__cta-final-title">Vuoi vederla<br><em>dal vivo?</em></h2>
        <p class="product-pro__cta-final-text">Passa in showroom a Cene o chiamaci. Ti diciamo subito tempi, ricambi e modi.</p>
        <div class="product-pro__cta-final-actions">
          <a class="btn btn--primary" href="https://wa.me/393464156981?text=Buongiorno%2C%20vorrei%20info%20sulla%20${encodeURIComponent(data.brand + ' ' + data.model)}" target="_blank" rel="noopener">WhatsApp →</a>
          <a class="btn btn--outline-light" href="tel:+393464156981">346 4156981</a>
          <a class="btn btn--ghost" href="../prodotti.html">Torna al catalogo</a>
        </div>
      </div>
    `;
    return wrap;
  }

  /* ——— 3. Inietta nella pagina ——— */
  const data = extract();
  if (!data.model) return; // safety

  // Nasconde il vecchio product__grid (lo sostituiamo)
  const oldGrid = main.querySelector('.product__grid');
  const crumbs = main.querySelector('.product__crumbs');

  const heroEl = buildEnhancedHero(data);
  const descEl = buildDescPanel(data);
  const showcaseEl = buildScrollShowcase(data);
  const finalCTA = buildCTAFinal(data);

  if (crumbs) {
    crumbs.after(heroEl, descEl, showcaseEl, finalCTA);
  } else {
    main.prepend(finalCTA);
    main.prepend(showcaseEl);
    main.prepend(descEl);
    main.prepend(heroEl);
  }
  if (oldGrid) oldGrid.remove();

  /* ——— 4. Toggle descrizione ——— */
  const descToggle = heroEl.querySelector('[data-toggle="desc"]');
  if (descToggle) {
    descToggle.addEventListener('click', () => {
      const open = descEl.hasAttribute('hidden');
      if (open) {
        descEl.removeAttribute('hidden');
        descToggle.setAttribute('aria-expanded', 'true');
        descToggle.classList.add('is-open');
        descEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        descEl.setAttribute('hidden', '');
        descToggle.setAttribute('aria-expanded', 'false');
        descToggle.classList.remove('is-open');
      }
    });
  }

  /* ——— 5. Scroll-driven 3D rotation della media nell'hero ——— */
  if (!reduced) {
    const stage = heroEl.querySelector('.product-pro__hero-stage');
    if (stage) {
      let ticking = false;
      const onScroll = () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
          const r = heroEl.getBoundingClientRect();
          const p = Math.max(-0.5, Math.min(0.5, (innerHeight / 2 - r.top - r.height / 2) / innerHeight));
          stage.style.transform = `translateY(${p * -40}px) rotate(${p * -3}deg) scale(${1 + Math.abs(p) * 0.04})`;
          ticking = false;
        });
      };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }

    /* ——— 6. Showcase: step in evidenza in base allo scroll ——— */
    const showSteps = showcaseEl.querySelectorAll('.product-pro__step');
    const showNum = showcaseEl.querySelector('.product-pro__showcase-num');
    const showVisual = showcaseEl.querySelector('.product-pro__showcase-stage img');
    if ('IntersectionObserver' in window && showSteps.length) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach(en => {
          if (en.isIntersecting) {
            showSteps.forEach(s => s.classList.remove('is-active'));
            en.target.classList.add('is-active');
            const n = en.target.dataset.step;
            if (showNum) showNum.textContent = '0' + n;
            if (showVisual) {
              const ang = (parseInt(n, 10) - 1) * 8 - 8;
              showVisual.style.transform = `rotate(${ang}deg) scale(${1 + (parseInt(n, 10) - 1) * 0.02})`;
            }
          }
        });
      }, { threshold: 0.55, rootMargin: '-30% 0px -30% 0px' });
      showSteps.forEach(s => io.observe(s));
    }
  }
})();
