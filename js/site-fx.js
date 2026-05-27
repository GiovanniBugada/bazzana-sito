/* =========================================================
   SITE FX — micro-interazioni globali su tutte le pagine.
   - Custom cursor (dot + ring inerziale, blend difference)
   - Scroll-progress bar (fixed bottom, gradient arancio)
   - Reveal-on-scroll (IntersectionObserver per .reveal)
   - Auto-injection: niente HTML da modificare per pagina
   ========================================================= */
(() => {
  'use strict';

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hover = matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ——— Auto-inject cursor + scroll bar ——— */
  function injectChrome() {
    if (!document.getElementById('cur')) {
      const cur = document.createElement('div');
      cur.id = 'cur';
      cur.className = 'cur';
      cur.setAttribute('aria-hidden', 'true');
      cur.innerHTML = '<div class="cur__dot"></div><div class="cur__ring"></div><div class="cur__label"></div>';
      document.body.appendChild(cur);
    }
    if (!document.querySelector('.scroll-progress-bar')) {
      const bar = document.createElement('div');
      bar.className = 'scroll-progress-bar';
      bar.setAttribute('aria-hidden', 'true');
      document.body.appendChild(bar);
    }
  }

  /* ——— Custom cursor — BUG FIXES integrati:
     1. Reduced-motion / touch → no cursor (existing)
     2. Mouse leave window → hide cursor immediato + reset is-hover
     3. Page reload / visibilitychange → reset state
     4. Loop spegne quando mouse fermo per risparmiare CPU
     5. Initial position out-of-view fino a primo mousemove (evita "scatto")
     6. is-hover su body tag a fallback se cursor manca elementi
  */
  /* ——— Cursor v3 — dot + ring + label contestuale.
     Fix:
     - mouse fuori window → hide istantaneo
     - iframe → hide (l'iframe ha il suo nativo)
     - page transition → hide
     - tab nascosta → reset
     - reduced motion / touch → niente cursor
     - label letta da [data-cursor] sull'elemento o default per role
  */
  function initCursor() {
    if (reduced || !hover) return;
    if (matchMedia('(pointer: coarse)').matches) return;
    const cur = document.getElementById('cur');
    if (!cur) return;
    const label = cur.querySelector('.cur__label');

    let mx = -100, my = -100;
    let initialized = false;
    let pendingMove = false;
    let getInteractiveSel = () => '';

    cur.classList.add('is-hidden');

    /* Cursore v9: un solo elemento (.cur stesso), inline transform.
       FIX FLUIDITA': il mousemove batched via requestAnimationFrame
       (1 update per frame max) invece di chiamare setPos a ogni evento.
       Su pagine con DOM pesante (es. prodotti.html con ~650 card)
       evita scatti dovuti a transform applicati piu' volte per frame. */
    function setPos(x, y) {
      cur.style.transform = 'translate3d(' + x + 'px,' + y + 'px,0)';
    }
    function flushMove() {
      pendingMove = false;
      setPos(mx, my);
    }

    document.addEventListener('mousemove', (e) => {
      mx = e.clientX;
      my = e.clientY;
      if (!pendingMove) {
        pendingMove = true;
        requestAnimationFrame(flushMove);
      }
      if (!initialized) {
        initialized = true;
        cur.classList.remove('is-hidden');
      }
    }, { passive: true });

    /* Safety: ogni 200ms, se siamo in hover ma non c'e' piu' un elemento
       interattivo sotto (es. e' stato rimosso), togli hover. */
    setInterval(() => {
      if (!cur.classList.contains('is-hover')) return;
      const sel = getInteractiveSel();
      const under = document.elementFromPoint(mx, my);
      const hit = under && under.closest && sel ? under.closest(sel) : null;
      if (!hit) {
        cur.classList.remove('is-hover');
        if (label) label.textContent = '';
      }
    }, 200);

    function startLoop() {}
    function stopLoop() {}

    document.addEventListener('mousedown', () => cur.classList.add('is-down'));
    document.addEventListener('mouseup', () => cur.classList.remove('is-down'));

    // Mouse esce dalla window → hide
    document.addEventListener('mouseleave', () => {
      cur.classList.add('is-hidden');
      cur.classList.remove('is-hover');
    });
    document.addEventListener('mouseenter', () => {
      if (initialized) cur.classList.remove('is-hidden');
    });

    // IFRAME → hide (es. mappa OpenStreetMap)
    document.querySelectorAll('iframe').forEach(iframe => {
      iframe.addEventListener('mouseenter', () => {
        cur.classList.add('is-hidden');
        cur.classList.remove('is-hover');
      });
      iframe.addEventListener('mouseleave', () => {
        cur.classList.remove('is-hidden');
      });
    });
    // Re-bind se iframes vengono aggiunti dopo
    const ifObs = new MutationObserver(muts => {
      muts.forEach(m => m.addedNodes.forEach(n => {
        if (n.tagName === 'IFRAME' || (n.querySelectorAll && n.querySelectorAll('iframe').length)) {
          const ifrs = n.tagName === 'IFRAME' ? [n] : Array.from(n.querySelectorAll('iframe'));
          ifrs.forEach(ifr => {
            ifr.addEventListener('mouseenter', () => { cur.classList.add('is-hidden'); cur.classList.remove('is-hover'); });
            ifr.addEventListener('mouseleave', () => { cur.classList.remove('is-hidden'); });
          });
        }
      }));
    });
    ifObs.observe(document.body, { childList: true, subtree: true });

    // Page transition: hide
    const ptObs = new MutationObserver(() => {
      const trans = document.querySelector('.page-trans');
      if (trans && (trans.classList.contains('is-entering') || trans.classList.contains('is-leaving'))) {
        cur.classList.add('is-hidden');
      }
    });
    ptObs.observe(document.body, { childList: true, subtree: false, attributes: true, attributeFilter: ['class'] });

    // Visibility change: reset
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        stopLoop();
      } else if (initialized) {
        cur.classList.remove('is-hidden');
        startLoop();
      }
    });

    // Selettore "interactive" + lettura label contestuale
    const INTERACTIVE_SEL =
      'a, button, [role="button"], label, summary, [data-cursor],' +
      ' .h3-card, .h3-pillar__media, .h3-bento__cell, .h3-brand,' +
      ' .h3-visit__contact, .fab-stack__btn, .menu-toggle,' +
      ' .menu-overlay__close, .h3-hero__scroll,' +
      ' .galleria__item, .dual-focus__card, .hero-v2__card,' +
      ' .product-pro__cta, .product-pro__desc-toggle, .storia__cta-btn,' +
      ' .featured-strip__card, .site-footer__social a, .foto__item,' +
      ' .foto__filter, .foto__layout-btn, .product-modal__cta,' +
      ' .product-modal__close, .audio-toggle, details summary, .faq-item summary,' +
      ' .brands-v2__item, .chip, .cat-card,' +
      ' .nav-search__item, .nav-search__close, .nav-search__clear,' +
      ' .nav-search__mobile-trigger, .nav-search__mobile-close,' +
      ' .bzn-map__btn, .bzn-map__layer-btn,' +
      ' .generic-detail__cta, .generic-detail__similar-card';
    // Espone il selettore al tick() per il safety cleanup di is-hover
    getInteractiveSel = () => INTERACTIVE_SEL;

    // Nascondi il cursor su elementi con cursore nativo (Leaflet drag, ecc.)
    const NATIVE_CURSOR_SEL = '.leaflet-container, .bzn-map__canvas, input, textarea';
    const labelFor = (el) => {
      if (!el || !el.closest) return '';
      const target = el.closest(INTERACTIVE_SEL);
      if (!target) return '';
      // Esplicito da attributo
      if (target.dataset.cursor) return target.dataset.cursor;
      // Default contestuali
      if (target.tagName === 'A') {
        const href = target.getAttribute('href') || '';
        if (href.startsWith('tel:')) return 'Chiama';
        if (href.startsWith('mailto:')) return 'Scrivi';
        if (href.includes('wa.me')) return 'Chatta';
        if (href.includes('instagram')) return 'Segui';
        if (target.classList.contains('h3-card')) return 'Vedi';
        return 'Vai';
      }
      if (target.tagName === 'BUTTON') return 'Apri';
      return '';
    };

    document.addEventListener('mouseover', (e) => {
      // Nascondi il cursor su Leaflet/iframe/input nativi
      if (e.target.closest && e.target.closest(NATIVE_CURSOR_SEL)) {
        cur.classList.add('is-hidden');
        cur.classList.remove('is-hover');
        return;
      } else if (initialized) {
        cur.classList.remove('is-hidden');
      }
      const target = e.target.closest && e.target.closest(INTERACTIVE_SEL);
      if (target) {
        cur.classList.add('is-hover');
        if (label) label.textContent = labelFor(e.target);
      } else {
        cur.classList.remove('is-hover');
      }
    });
    document.addEventListener('mouseout', (e) => {
      const fromInteractive = e.target.closest && e.target.closest(INTERACTIVE_SEL);
      const toInteractive = e.relatedTarget && e.relatedTarget.closest && e.relatedTarget.closest(INTERACTIVE_SEL);
      if (fromInteractive && !toInteractive) {
        cur.classList.remove('is-hover');
      }
    });

    window.addEventListener('beforeunload', () => {
      cur.classList.add('is-hidden');
    });
  }

  /* ——— Scroll-progress bar ——— */
  function initScrollProgress() {
    if (reduced) return;
    const bar = document.querySelector('.scroll-progress-bar');
    if (!bar) return;
    let ticking = false;
    const update = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      const p = max > 0 ? Math.min(1, Math.max(0, scrollY / max)) : 0;
      bar.style.transform = `scaleX(${p})`;
      ticking = false;
    };
    const onScroll = () => {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    };
    addEventListener('scroll', onScroll, { passive: true });
    addEventListener('resize', onScroll, { passive: true });
    update();
  }

  /* ——— Reveal-on-scroll (fallback se non gestito da main.js)
     FIX: trigger anticipato + elementi già sopra viewport → in subito.
     Vedi commit fix-reveal-anticipato. */
  function initReveal() {
    const els = document.querySelectorAll('.reveal:not(.in):not(.is-in)');
    if (!els.length) return;
    if (reduced || !('IntersectionObserver' in window)) {
      els.forEach(el => { el.classList.add('in'); el.classList.add('is-in'); });
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          en.target.classList.add('in');
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px 200px 0px' });
    els.forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.bottom < 0) { el.classList.add('in'); el.classList.add('is-in'); return; }
      io.observe(el);
    });
    setTimeout(() => {
      els.forEach(el => {
        if (el.classList.contains('in')) return;
        const r = el.getBoundingClientRect();
        if (r.top < innerHeight + 100) { el.classList.add('in'); el.classList.add('is-in'); }
      });
    }, 1500);
  }

  /* ——— Background ambient: glow segue mouse su sezioni opt-in ——— */
  function initAmbientGlow() {
    if (reduced || !hover) return;
    document.querySelectorAll('[data-ambient-glow], .hero-v2, .immersive, .visit-v2').forEach(sec => {
      sec.addEventListener('mousemove', (e) => {
        const r = sec.getBoundingClientRect();
        const x = ((e.clientX - r.left) / r.width) * 100;
        const y = ((e.clientY - r.top) / r.height) * 100;
        sec.style.setProperty('--glow-x', x + '%');
        sec.style.setProperty('--glow-y', y + '%');
      }, { passive: true });
    });
  }

  /* ——— Newsletter footer (auto-inject prima del .site-footer__bottom) ——— */
  function initNewsletter() {
    const footerInner = document.querySelector('.site-footer__inner');
    if (!footerInner || footerInner.querySelector('.newsletter')) return;
    const bottom = footerInner.querySelector('.site-footer__bottom');
    if (!bottom) return;
    const nl = document.createElement('div');
    nl.className = 'newsletter';
    nl.innerHTML = `
      <div class="newsletter__head">
        <span class="newsletter__eyebrow">Resta in contatto</span>
        <h3 class="newsletter__title">Le novità del negozio,<br><em>una mail ogni tanto.</em></h3>
      </div>
      <div>
        <form class="newsletter__form" action="https://formsubmit.co/bazzanamotorgarden@gmail.com" method="POST">
          <input type="hidden" name="_subject" value="Iscrizione newsletter MGB" />
          <input type="hidden" name="_template" value="table" />
          <input class="newsletter__input" type="email" name="email" placeholder="la-tua-email@esempio.it" required autocomplete="email" aria-label="La tua email">
          <button class="newsletter__submit" type="submit">Iscriviti →</button>
        </form>
        <p class="newsletter__note">Niente spam. Solo aggiornamenti veri. Disiscrivibile in ogni momento.</p>
      </div>
    `;
    bottom.parentNode.insertBefore(nl, bottom);
    // Submit handler
    nl.querySelector('form').addEventListener('submit', (e) => {
      if (!nl.querySelector('form').checkValidity()) return;
      nl.classList.add('is-sent');
      const btn = nl.querySelector('.newsletter__submit');
      if (btn) {
        btn.textContent = 'Grazie!';
        setTimeout(() => { nl.classList.remove('is-sent'); btn.textContent = 'Iscriviti →'; }, 5000);
      }
    });
  }

  /* ——— Init ——— */
  function init() {
    injectChrome();
    initCursor();
    initScrollProgress();
    initReveal();
    initAmbientGlow();
    // Newsletter rimossa per ora — non è ancora pronta una vera mailing-list
    // initNewsletter();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
