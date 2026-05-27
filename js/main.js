/* =======================================================
   Motor Garden Bazzana — Main JS
   ======================================================= */

(() => {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ——— Loader cinematografico con counter % ——— */
  const loader = document.querySelector('.loader');
  if (loader) {
    document.body.style.overflow = 'hidden';
    const pct = loader.querySelector('.loader__pct');
    const min = reduced ? 200 : 2200;
    // Counter % animato
    if (pct && !reduced) {
      const start = performance.now();
      const animatePct = (now) => {
        const p = Math.min(1, (now - start) / min);
        const eased = 1 - Math.pow(1 - p, 3);
        const v = Math.round(eased * 100);
        pct.textContent = v.toString().padStart(3, '0') + '%';
        if (p < 1) requestAnimationFrame(animatePct);
      };
      requestAnimationFrame(animatePct);
    } else if (pct) {
      pct.textContent = '100%';
    }
    // Hide loader: aspetta load OR timer minimo
    let doneTimer = false, doneLoad = document.readyState === 'complete';
    let alreadyHidden = false;
    const hardHide = () => {
      if (alreadyHidden) return;
      alreadyHidden = true;
      // setProperty con 'important' priority — l'unico modo per sovrascrivere
      // il `display: flex !important` definito in loader-cinematic.css.
      loader.style.setProperty('display', 'none', 'important');
      loader.style.setProperty('pointer-events', 'none', 'important');
      loader.style.setProperty('visibility', 'hidden', 'important');
      loader.setAttribute('hidden', '');
      loader.setAttribute('aria-hidden', 'true');
      // Sblocca body
      document.body.style.overflow = '';
      document.body.classList.add('is-loaded');
    };
    const tryHide = () => {
      if (doneTimer && doneLoad) {
        loader.classList.add('is-done');
        document.body.style.overflow = '';
        document.body.classList.add('is-loaded');
        const hero = document.querySelector('.hero');
        if (hero) hero.classList.add('is-loaded');
        // Hard hide dopo le transition complete + buffer
        setTimeout(hardHide, 1300);
      }
    };
    setTimeout(() => { doneTimer = true; tryHide(); }, min);
    if (!doneLoad) {
      window.addEventListener('load', () => { doneLoad = true; tryHide(); }, { once: true });
    } else {
      tryHide();
    }
    // Failsafe a 3.5s: hard hide assoluto (evita loader stuck su tab throttled)
    setTimeout(hardHide, 3500);
  }

  /* ——— Header scroll state ——— */
  const header = document.querySelector('.site-header');
  if (header) {
    const onScroll = () => {
      if (window.scrollY > 30) header.classList.add('is-scrolled');
      else header.classList.remove('is-scrolled');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ——— Mobile menu ——— */
  const menuToggle = document.querySelector('.menu-toggle');
  const menuOverlay = document.querySelector('.menu-overlay');
  const menuClose = document.querySelector('.menu-overlay__close');
  if (menuToggle && menuOverlay) {
    menuToggle.addEventListener('click', () => {
      menuOverlay.classList.add('is-open');
      document.body.style.overflow = 'hidden';
    });
    if (menuClose) menuClose.addEventListener('click', () => {
      menuOverlay.classList.remove('is-open');
      document.body.style.overflow = '';
    });
    menuOverlay.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        menuOverlay.classList.remove('is-open');
        document.body.style.overflow = '';
      });
    });
  }

  /* Custom cursor disattivato: usiamo cursore nativo OS per consistency */

  /* ——— Reveal on scroll — FIX: trigger anticipato + safety net immediato
     - Elementi già sopra al viewport (es. reload mid-page, anchor jump) → in subito
     - rootMargin positivo: si attivano PRIMA di entrare (200px), pronti a vista
     - threshold 0: basta 1 pixel
     - Se reduced-motion → tutti subito visibili
  */
  function revealNow(el) { el.classList.add('in'); el.classList.add('is-in'); }
  function isPastTop(el) {
    const r = el.getBoundingClientRect();
    return r.bottom < 0; // già sopra il viewport
  }
  const revealEls = document.querySelectorAll('.reveal, .reveal-mask');
  if (revealEls.length) {
    if (reduced || !('IntersectionObserver' in window)) {
      revealEls.forEach(revealNow);
    } else {
      const io = new IntersectionObserver((entries) => {
        entries.forEach(en => {
          if (en.isIntersecting) {
            revealNow(en.target);
            io.unobserve(en.target);
          }
        });
      }, { threshold: 0, rootMargin: '0px 0px 200px 0px' });
      revealEls.forEach(el => {
        if (isPastTop(el)) { revealNow(el); return; } // già passato → in subito
        io.observe(el);
      });
      // Safety net 2s: niente reveal "fantasma"
      setTimeout(() => {
        revealEls.forEach(el => { if (!el.classList.contains('in')) {
          const r = el.getBoundingClientRect();
          // Mostra solo se davvero in/sopra viewport (sotto resta animato)
          if (r.top < window.innerHeight + 100) revealNow(el);
        }});
      }, 2000);
    }
  }

  /* ——— Smooth scroll (light, no lib) ——— */
  if (!reduced) {
    let cur = window.scrollY;
    let tgt = cur;
    let running = false;

    const onWheel = (e) => {
      // Lascia che default funzioni — solo migliora touchpad/mouse?
      // (Lenis-like full takeover sarebbe troppo invasivo per il primo round)
    };
    // Internal anchors smooth
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      a.addEventListener('click', e => {
        const href = a.getAttribute('href');
        if (href.length <= 1) return;
        const target = document.querySelector(href);
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  /* ——— Page transition v2 — dark curtain dal basso, linea arancio ——— */
  if (!reduced) {
    const trans = document.createElement('div');
    trans.className = 'page-trans';
    trans.setAttribute('aria-hidden', 'true');
    document.body.appendChild(trans);

    // Se arriviamo da una navigazione interna → curtain in posizione coperta
    // poi sale verso l'alto rivelando la nuova pagina.
    try {
      if (sessionStorage.getItem('mgb-pt-leaving') === '1') {
        sessionStorage.removeItem('mgb-pt-leaving');
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            trans.classList.add('is-leaving');
          });
        });
        setTimeout(() => trans.classList.remove('is-leaving'), 500);
      }
    } catch (e) {}

    // Intercetta click su link interni → curtain sale dal basso → navigate
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a');
      if (!a) return;
      const href = a.getAttribute('href');
      if (!href) return;
      if (href.startsWith('#')) return;
      if (a.target === '_blank') return;
      if (href.startsWith('http') && !href.includes(location.host)) return;
      if (href.startsWith('mailto:') || href.startsWith('tel:') || href.includes('wa.me')) return;
      // Modifier keys → lascia che il browser apra in nuova tab
      if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      try { sessionStorage.setItem('mgb-pt-leaving', '1'); } catch (err) {}
      trans.classList.add('is-entering');
      setTimeout(() => { window.location.href = href; }, 360);
    });
  }

  /* ——— Filtri prodotti per brand (chip nel catalogo) ——— */
  const chips = document.querySelectorAll('.filter-chips .chip[data-filter]');
  if (chips.length) {
    const brandSections = document.querySelectorAll('.brand-section[data-brand]');
    chips.forEach(c => {
      c.addEventListener('click', () => {
        chips.forEach(x => x.classList.remove('is-active'));
        c.classList.add('is-active');
        const f = c.getAttribute('data-filter');
        brandSections.forEach(sec => {
          if (f === 'all' || sec.getAttribute('data-brand') === f) {
            sec.removeAttribute('hidden');
          } else {
            sec.setAttribute('hidden', '');
          }
        });
        // Scroll a top del catalogo
        const cat = document.querySelector('.product-catalog');
        if (cat) cat.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  /* ——— Cinematic init (spotlight, count-up, reveal-clip, color-invert, scroll-scale) ——— */
  function observeAndAdd(selector, cls /*, threshold (ignored, now uses anticipated trigger) */) {
    const items = document.querySelectorAll(selector);
    if (!items.length) return;
    if (reduced || !('IntersectionObserver' in window)) {
      items.forEach(el => el.classList.add(cls));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          en.target.classList.add(cls);
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px 200px 0px' });
    items.forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.bottom < 0) { el.classList.add(cls); return; } // già sopra viewport
      io.observe(el);
    });
    // Safety net 1500ms — solo elementi davvero "vicini" al viewport
    setTimeout(() => {
      items.forEach(el => {
        if (el.classList.contains(cls)) return;
        const r = el.getBoundingClientRect();
        if (r.top < window.innerHeight + 100) el.classList.add(cls);
      });
    }, 1500);
  }
  observeAndAdd('.scroll-scale-img', 'is-in', 0.25);
  observeAndAdd('.color-invert-reveal', 'is-inverted', 0.4);
  observeAndAdd('.reveal-clip', 'is-revealed', 0.18);

  // Num ticker count-up
  const tickers = document.querySelectorAll('.num-ticker');
  if (tickers.length && 'IntersectionObserver' in window) {
    if (reduced) {
      tickers.forEach(el => {
        const t = parseFloat(el.getAttribute('data-target') || el.textContent) || 0;
        el.textContent = t;
      });
    } else {
      const io = new IntersectionObserver((entries) => {
        entries.forEach(en => {
          if (!en.isIntersecting) return;
          const el = en.target;
          io.unobserve(el);
          const target = parseFloat(el.getAttribute('data-target') || el.textContent) || 0;
          const duration = parseInt(el.getAttribute('data-duration') || '1400', 10);
          const prefix = el.getAttribute('data-prefix') || '';
          const suffix = el.getAttribute('data-suffix') || '';
          const decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
          const start = performance.now();
          const tick = (now) => {
            const p = Math.min(1, (now - start) / duration);
            const eased = 1 - Math.pow(1 - p, 3);
            const v = target * eased;
            el.textContent = prefix + v.toFixed(decimals) + suffix;
            if (p < 1) requestAnimationFrame(tick);
          };
          requestAnimationFrame(tick);
        });
      }, { threshold: 0.3 });
      tickers.forEach(el => io.observe(el));
    }
  }

  // Spotlight cursor (radial glow on mouse move)
  if (!reduced && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    document.querySelectorAll('.spotlight-section').forEach(sec => {
      sec.addEventListener('mousemove', (e) => {
        const r = sec.getBoundingClientRect();
        sec.style.setProperty('--mouse-x', ((e.clientX - r.left) / r.width * 100) + '%');
        sec.style.setProperty('--mouse-y', ((e.clientY - r.top) / r.height * 100) + '%');
      }, { passive: true });
    });
  }

  // Pinned scroll showcase (MSI-style oggetto che ruota + step cascata)
  function initScrollShowcase() {
    if (reduced) return;
    const sections = document.querySelectorAll('.scroll-showcase');
    if (!sections.length) return;
    sections.forEach(sec => {
      const visual = sec.querySelector('.scroll-showcase__chainsaw');
      const visualParent = sec.querySelector('.scroll-showcase__visual');
      const steps = sec.querySelectorAll('.scroll-showcase__step');
      const dotsHost = sec.querySelector('.scroll-showcase__progress');
      let dots = [];
      if (dotsHost && !dotsHost.children.length && steps.length) {
        for (let i = 0; i < steps.length; i++) {
          const d = document.createElement('span');
          d.className = 'scroll-showcase__dot';
          if (i === 0) d.classList.add('is-active');
          dotsHost.appendChild(d);
        }
      }
      dots = dotsHost ? dotsHost.querySelectorAll('.scroll-showcase__dot') : [];
      let ticking = false;
      const update = () => {
        const r = sec.getBoundingClientRect();
        const total = r.height - window.innerHeight;
        const progress = Math.max(0, Math.min(1, -r.top / Math.max(1, total)));
        const rot = (-10 + progress * 20).toFixed(2);
        const mid = Math.sin(progress * Math.PI);
        const scale = (1 + mid * 0.14).toFixed(3);
        const glow = (0.7 + mid * 0.5).toFixed(3);
        if (visual) {
          visual.style.setProperty('--showcase-rot', rot + 'deg');
          visual.style.setProperty('--showcase-scale', scale);
        }
        if (visualParent) visualParent.style.setProperty('--showcase-glow', glow);
        if (steps.length) {
          const idx = Math.min(steps.length - 1, Math.floor(progress * steps.length));
          steps.forEach((s, i) => s.classList.toggle('is-active', i === idx));
          if (dots.length) dots.forEach((d, i) => d.classList.toggle('is-active', i === idx));
        }
        ticking = false;
      };
      window.addEventListener('scroll', () => {
        if (!ticking) { requestAnimationFrame(update); ticking = true; }
      }, { passive: true });
      update();
    });
  }
  initScrollShowcase();

  /* ——— SCROLL PROGRESS BAR in alto ——— */
  (() => {
    const bar = document.createElement('div');
    bar.className = 'scroll-progress';
    bar.setAttribute('aria-hidden', 'true');
    const fill = document.createElement('div');
    fill.className = 'scroll-progress__fill';
    bar.appendChild(fill);
    document.body.appendChild(bar);
    let ticking = false;
    const update = () => {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      const p = h > 0 ? (window.scrollY / h) * 100 : 0;
      fill.style.width = p + '%';
      ticking = false;
    };
    window.addEventListener('scroll', () => {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  })();

  /* ——— RIPPLE on click (CTA btn-ripple) ——— */
  document.querySelectorAll('.btn-ripple, .btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      if (reduced) return;
      const r = this.getBoundingClientRect();
      const size = Math.max(r.width, r.height);
      const w = document.createElement('span');
      w.className = 'ripple-wave';
      w.style.width = w.style.height = size + 'px';
      w.style.left = (e.clientX - r.left - size/2) + 'px';
      w.style.top = (e.clientY - r.top - size/2) + 'px';
      this.classList.add('btn-ripple');
      this.appendChild(w);
      setTimeout(() => w.remove(), 700);
    });
  });

  /* ——— Observers extra per le nuove classi ——— */
  observeAndAdd('.section-fade', 'is-in', 0.18);
  observeAndAdd('.stagger-fade', 'is-in', 0.2);
  observeAndAdd('.section-divider-anim', 'is-in', 0.4);
  observeAndAdd('.zoom-mask', 'is-in', 0.3);

  /* MAGNETIC + 3D TILT disattivati: visivamente troppo invasivi su CTA / cat-card.
     Per riabilitarli, vedi commit 4554641. */

  /* ——— WORD-BY-WORD reveal (titoli) ——— */
  document.querySelectorAll('.word-reveal').forEach(el => {
    if (el.dataset.wordSplit === '1') return;
    el.dataset.wordSplit = '1';
    const text = el.textContent;
    el.innerHTML = text.split(/\s+/).filter(Boolean)
      .map(w => `<span class="word-reveal__word">${w}</span>`)
      .join(' ');
  });
  observeAndAdd('.word-reveal', 'is-in', 0.25);

  /* ——— LETTER-UP per titoli char by char ——— */
  document.querySelectorAll('.letter-up').forEach(el => {
    if (el.dataset.letterSplit === '1') return;
    el.dataset.letterSplit = '1';
    const text = el.textContent;
    el.innerHTML = text.split('').map((c, i) => {
      if (c === ' ') return ' ';
      return `<span class="letter-up__char" style="transition-delay:${i * 28}ms">${c}</span>`;
    }).join('');
  });
  observeAndAdd('.letter-up', 'is-in', 0.25);

  /* ——— SVG line draw on viewport entry ——— */
  observeAndAdd('.line-draw-svg', 'is-drawn', 0.3);

  /* ——— REVEAL DIAGONAL ——— */
  observeAndAdd('.reveal-diagonal', 'is-in', 0.2);

  /* ——— IMG FILTER SHIFT on scroll ——— */
  observeAndAdd('.img-filter-shift', 'is-in', 0.25);

  /* ——— STICKY SCALE-OUT (elemento si rimpicciolisce uscendo dal viewport) ——— */
  if (!reduced && 'IntersectionObserver' in window) {
    const stickyScales = document.querySelectorAll('.sticky-scale');
    if (stickyScales.length) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach(en => {
          en.target.classList.toggle('is-out', !en.isIntersecting);
        });
      }, { threshold: 0.1 });
      stickyScales.forEach(el => io.observe(el));
    }
  }

  /* CURSOR TRAIL + GRAIN OVERLAY disattivati: visivamente troppo "rumorosi".
     Per riabilitarli, vedi commit 4554641 / 479c86b. */

  // Parallax sottile per immagini con data-parallax-speed (sondaven style)
  if (!reduced && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    const parallaxEls = document.querySelectorAll('[data-parallax-speed]');
    if (parallaxEls.length) {
      let ticking = false;
      const updateParallax = () => {
        parallaxEls.forEach(el => {
          const speed = parseFloat(el.getAttribute('data-parallax-speed')) || 0.3;
          const r = el.getBoundingClientRect();
          const center = r.top + r.height / 2 - window.innerHeight / 2;
          el.style.transform = `translate3d(0, ${center * -speed}px, 0)`;
        });
        ticking = false;
      };
      window.addEventListener('scroll', () => {
        if (!ticking) { requestAnimationFrame(updateParallax); ticking = true; }
      }, { passive: true });
      updateParallax();
    }
  }

  /* ——— Anno corrente in footer ——— */
  document.querySelectorAll('[data-year]').forEach(el => {
    el.textContent = new Date().getFullYear();
  });

})();
