/* =========================================================
   PHOTO RICH — interazioni per le sezioni foto-centriche.
   - Feature pin sticky: scroll-driven step switch (Opal-style)
   - Featured strip card hover micro-tilt
   - Marquee-free, niente loop
   ========================================================= */
(() => {
  'use strict';

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hover = matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ——— 1. FEATURE PIN — switch step in base allo scroll ——— */
  function initFeaturePin() {
    const section = document.querySelector('.feature-pin');
    if (!section) return;
    const panels = section.querySelectorAll('.feature-pin__panel');
    if (!panels.length) return;

    if (!('IntersectionObserver' in window)) {
      panels.forEach(p => p.classList.add('is-active'));
      return;
    }

    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          const step = en.target.dataset.step;
          // Activate this panel, deactivate others
          panels.forEach(p => p.classList.toggle('is-active', p === en.target));
          // Update section class for visual switch
          section.classList.remove('is-step-1', 'is-step-2', 'is-step-3');
          section.classList.add('is-step-' + parseInt(step, 10));
        }
      });
    }, {
      threshold: 0.5,
      rootMargin: '-30% 0px -30% 0px'
    });
    panels.forEach(p => io.observe(p));

    // Inizializza primo step
    section.classList.add('is-step-1');
    if (panels[0]) panels[0].classList.add('is-active');
  }

  /* ——— 2. Featured strip card: micro-tilt 3D leggero su hover ——— */
  function initFeaturedTilt() {
    if (reduced || !hover) return;
    const cards = document.querySelectorAll('.featured-strip__card');
    cards.forEach(card => {
      let raf = null;
      card.style.transformStyle = 'preserve-3d';
      card.addEventListener('mousemove', (e) => {
        if (raf) cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => {
          const r = card.getBoundingClientRect();
          const x = (e.clientX - r.left) / r.width;
          const y = (e.clientY - r.top) / r.height;
          const rx = (y - 0.5) * -3;
          const ry = (x - 0.5) * 4;
          card.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-6px)`;
        });
      }, { passive: true });
      card.addEventListener('mouseleave', () => {
        if (raf) cancelAnimationFrame(raf);
        card.style.transition = 'transform 600ms cubic-bezier(0.22, 1, 0.36, 1)';
        card.style.transform = '';
        setTimeout(() => { card.style.transition = ''; }, 600);
      });
    });
  }

  /* ——— 3. HSCROLL — horizontal scroll showcase ———
     Altezza section calcolata da JS in base a track width reale:
     section_height = innerHeight + (trackScrollWidth - innerWidth)
     Così lo scroll verticale combacia esattamente con la traslazione
     orizzontale: niente dead-space nero a fine sezione.
  */
  function initHScroll() {
    if (reduced) return;
    const section = document.querySelector('.hscroll');
    const track = document.querySelector('#hscroll-track');
    const progress = document.querySelector('.hscroll__progress-bar');
    if (!section || !track) return;

    // Su mobile (track collassa verticale via CSS): rimuove altezza fissa
    if (innerWidth < 900) {
      section.style.height = 'auto';
      return;
    }

    // Calcola altezza ideale: viewport + scroll orizzontale necessario
    let maxTranslate = 0;
    const calcHeight = () => {
      maxTranslate = Math.max(0, track.scrollWidth - innerWidth);
      const idealH = innerHeight + maxTranslate + innerHeight * 0.1; // 10% di "rest" finale
      section.style.height = idealH + 'px';
    };

    let ticking = false;
    let lastP = -1;

    const update = () => {
      const r = section.getBoundingClientRect();
      const totalScroll = section.offsetHeight - innerHeight;
      const scrolled = -r.top;
      const p = Math.max(0, Math.min(1, scrolled / totalScroll));
      if (Math.abs(p - lastP) < 0.001) { ticking = false; return; }
      lastP = p;

      // Traslazione orizzontale calcolata in modo che fine-scroll = ultimo panel allineato a destra
      track.style.transform = `translate3d(${-(p * maxTranslate).toFixed(1)}px, 0, 0)`;
      if (progress) progress.style.width = (p * 100).toFixed(1) + '%';
      ticking = false;
    };

    // Ricalcola altezza dopo che immagini sono caricate (scrollWidth può cambiare)
    calcHeight();
    setTimeout(calcHeight, 400);
    setTimeout(calcHeight, 1200);

    addEventListener('scroll', () => {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    addEventListener('resize', () => {
      if (innerWidth < 900) {
        section.style.height = 'auto';
        return;
      }
      calcHeight();
      lastP = -1;
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });

    update();
  }

  /* ——— 4. THEME SWITCH — body cambia tono in base alla sezione ——— */
  function initThemeSwitch() {
    if (!('IntersectionObserver' in window)) return;
    const sections = document.querySelectorAll('[data-theme]');
    if (!sections.length) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          document.documentElement.setAttribute('data-active-theme', en.target.dataset.theme);
        }
      });
    }, { threshold: 0.4, rootMargin: '-30% 0px -30% 0px' });
    sections.forEach(s => io.observe(s));
  }

  /* ——— 5. IMAGE HOVER ZOOM-TO-CURSOR ——— */
  function initImageZoom() {
    if (reduced || !hover) return;
    const images = document.querySelectorAll('[data-zoom-cursor], .featured-strip__media, .galleria__item');
    images.forEach(wrap => {
      const img = wrap.querySelector('img');
      if (!img) return;
      wrap.addEventListener('mousemove', (e) => {
        const r = wrap.getBoundingClientRect();
        const x = ((e.clientX - r.left) / r.width) * 100;
        const y = ((e.clientY - r.top) / r.height) * 100;
        img.style.transformOrigin = `${x}% ${y}%`;
      });
      wrap.addEventListener('mouseleave', () => {
        img.style.transformOrigin = '';
      });
    });
  }

  /* ——— Init ——— */
  function init() {
    initFeaturePin();
    initFeaturedTilt();
    initHScroll();
    initThemeSwitch();
    initImageZoom();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
