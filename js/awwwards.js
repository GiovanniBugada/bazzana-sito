/* =========================================================
   AWWWARDS — sistema unico premium di animazioni.
   - Smooth scroll Lenis-like (lerp 0.085, non hijack-totale)
   - Section reveal con clip-path mask (cinematografico)
   - Scroll-bound parallax fluido
   - Magnetic CTA
   - 3D tilt su card
   Sovrascrive cool-fx.js e altre animazioni precedenti.
   ========================================================= */
(() => {
  'use strict';

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hover = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const touch = matchMedia('(pointer: coarse)').matches;

  /* ============================================================
     1 · SMOOTH SCROLL — disabilitato.
     Il wheel hijack + scrollTo ogni frame causava lag e layout thrashing.
     Usiamo lo scroll nativo del browser (scroll-behavior: smooth via CSS).
     ============================================================ */
  function initSmoothScroll() { /* no-op */ }

  /* ============================================================
     2 · REVEAL ON SCROLL — clip-path mask + fade
     I `.reveal` e i target marcati si svelano UNA volta quando
     entrano in viewport. Cinematografico, leggero.
     ============================================================ */
  function initReveal() {
    if (!('IntersectionObserver' in window)) {
      document.querySelectorAll('.reveal, [data-reveal]').forEach(el => {
        el.classList.add('in', 'is-in');
      });
      return;
    }
    const targets = document.querySelectorAll(
      '.reveal:not(.in), [data-reveal]:not(.is-in),' +
      ' .galleria__item:not(.is-in-view), .dual-focus__card:not(.is-in),' +
      ' .stats-bar:not(.is-in), .immersive:not(.is-in),' +
      ' .brands-v2__list:not(.is-in), .visit-v2__grid:not(.is-in)'
    );
    if (!targets.length) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          en.target.classList.add('in');
          en.target.classList.add('is-in');
          en.target.classList.add('is-in-view');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px 200px 0px' });
    targets.forEach(t => {
      const r = t.getBoundingClientRect();
      if (r.bottom < 0) { t.classList.add('in', 'is-in', 'is-in-view'); return; }
      io.observe(t);
    });
    setTimeout(() => {
      targets.forEach(t => {
        if (t.classList.contains('in')) return;
        const r = t.getBoundingClientRect();
        if (r.top < innerHeight + 100) t.classList.add('in', 'is-in', 'is-in-view');
      });
    }, 1500);
  }

  /* ============================================================
     3 · SCROLL-BOUND PARALLAX — un solo rAF tick, will-change
     ============================================================ */
  function initParallax() {
    if (reduced) return;
    const layers = [];

    // Forte: immersive + product hero
    document.querySelectorAll('.immersive__media img, [data-parallax-strong]').forEach(el => {
      el.style.willChange = 'transform';
      layers.push({ el, mul: 0.14, base: 1.06 });
    });

    // Medio: galleria, dual focus, chapter, feature pin
    document.querySelectorAll('.galleria__item img, .dual-focus__media img, .storia__chapter-stage img').forEach(el => {
      el.style.willChange = 'transform';
      layers.push({ el, mul: 0.08, base: 1.04 });
    });

    if (!layers.length) return;
    let ticking = false;
    let lastY = -1;
    const update = () => {
      const vh = innerHeight;
      const sy = scrollY;
      // Skip se non c'è stato un cambio reale di scroll position
      if (sy === lastY) { ticking = false; return; }
      lastY = sy;
      for (const l of layers) {
        const r = l.el.getBoundingClientRect();
        if (r.bottom < -100 || r.top > vh + 100) continue;
        const p = (r.top + r.height / 2 - vh / 2) / vh;
        const ty = -p * 80 * l.mul;
        l.el.style.transform = `translate3d(0, ${ty.toFixed(1)}px, 0) scale(${l.base})`;
      }
      ticking = false;
    };
    addEventListener('scroll', () => {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    addEventListener('resize', () => {
      lastY = -1;
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  /* ============================================================
     4 · MAGNETIC CTA — bottoni "vivi" su hover
     ============================================================ */
  function initMagnetic() {
    if (reduced || !hover) return;
    const targets = document.querySelectorAll(
      '.hero-v2__card, .storia__cta-btn--primary, .product-pro__cta,' +
      ' .product-pro__cta-final-actions .btn,' +
      ' [data-magnetic], .btn--primary, .nav a'
    );
    targets.forEach(el => {
      let raf = null;
      const strength = el.matches('.nav a') ? 0.08 : 0.16;
      el.addEventListener('mousemove', (e) => {
        if (raf) cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => {
          const r = el.getBoundingClientRect();
          const cx = r.left + r.width / 2;
          const cy = r.top + r.height / 2;
          const dx = (e.clientX - cx) * strength;
          const dy = (e.clientY - cy) * (strength + 0.04);
          el.style.transform = `translate3d(${dx.toFixed(1)}px, ${dy.toFixed(1)}px, 0)`;
        });
      }, { passive: true });
      el.addEventListener('mouseleave', () => {
        if (raf) cancelAnimationFrame(raf);
        el.style.transition = 'transform 700ms cubic-bezier(0.22, 1, 0.36, 1)';
        el.style.transform = '';
        setTimeout(() => { el.style.transition = ''; }, 700);
      });
    });
  }

  /* ============================================================
     5 · 3D TILT su card grandi (dual-focus)
     ============================================================ */
  function initTilt() {
    if (reduced || !hover) return;
    const cards = document.querySelectorAll('.dual-focus__card, [data-tilt]');
    cards.forEach(card => {
      let raf = null;
      card.style.transformStyle = 'preserve-3d';
      card.addEventListener('mousemove', (e) => {
        if (raf) cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => {
          const r = card.getBoundingClientRect();
          const x = (e.clientX - r.left) / r.width;
          const y = (e.clientY - r.top) / r.height;
          const rx = (y - 0.5) * -3.5;
          const ry = (x - 0.5) * 4.5;
          card.style.transform = `perspective(1400px) rotateX(${rx}deg) rotateY(${ry}deg)`;
        });
      }, { passive: true });
      card.addEventListener('mouseleave', () => {
        if (raf) cancelAnimationFrame(raf);
        card.style.transition = 'transform 700ms cubic-bezier(0.22, 1, 0.36, 1)';
        card.style.transform = '';
        setTimeout(() => { card.style.transition = ''; }, 700);
      });
    });
  }

  /* ============================================================
     6 · STAGGERED reveal su brand items + stats + galleria
     ============================================================ */
  function initStaggerReveal() {
    const groups = [
      { container: '.galleria__grid', items: '.galleria__item', delay: 80 },
      { container: '.brands-v2__list', items: '.brands-v2__item', delay: 70 },
      { container: '.stats-bar', items: '.stats-bar__item', delay: 90 }
    ];
    groups.forEach(g => {
      const container = document.querySelector(g.container);
      if (!container) return;
      const items = container.querySelectorAll(g.items);
      items.forEach((item, i) => {
        item.style.transitionDelay = (i * g.delay) + 'ms';
      });
    });
  }

  /* ============================================================
     INIT
     ============================================================ */
  function init() {
    initSmoothScroll();
    initReveal();
    initParallax();
    initMagnetic();
    initTilt();
    initStaggerReveal();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
