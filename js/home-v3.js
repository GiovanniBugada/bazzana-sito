/* =========================================================
   HOME V3 — interazioni dedicate (awwwards-style)
   - Orologio live nell'hero
   - Hero media parallax dolce
   - Bento: parallax scroll-bound sulle img
   - Card featured: 3D tilt sul mousemove
   - CTA: magnetic effect (translate dolce verso il cursor)
   - FAB stack: visibilità + back-to-top
   - Hero title: aggiunge .in al wrapper per attivare mask reveal
   ========================================================= */
(() => {
  'use strict';
  if (document.body.dataset.page !== 'home') return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hoverable = matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ——— Orologio Europe/Rome nell'hero ——— */
  const nowEls = document.querySelectorAll('[data-now]');
  if (nowEls.length) {
    const fmt = new Intl.DateTimeFormat('it-IT', {
      timeZone: 'Europe/Rome',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });
    const tick = () => {
      const t = fmt.format(new Date());
      nowEls.forEach(el => { el.textContent = t + ' · Cene'; });
    };
    tick();
    setInterval(tick, 30 * 1000);
  }

  /* ——— Hero media: parallax dolce su scroll (solo desktop, non touch) ——— */
  if (!reduced) {
    const heroMedia = document.querySelector('.h3-hero__media img');
    if (heroMedia) {
      let ticking = false;
      const onScroll = () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
          const y = Math.min(window.scrollY, window.innerHeight);
          const offset = y * 0.18;
          heroMedia.style.transform = `scale(1.08) translateY(${offset.toFixed(1)}px)`;
          ticking = false;
        });
      };
      window.addEventListener('scroll', onScroll, { passive: true });
    }
  }

  /* ——— Bento gallery: parallax scroll-bound sulle img ——— */
  if (!reduced) {
    const parallaxImgs = Array.from(document.querySelectorAll('[data-parallax-img]'));
    if (parallaxImgs.length) {
      parallaxImgs.forEach(img => { img.style.willChange = 'transform'; });
      let ticking = false;
      const update = () => {
        const vh = window.innerHeight;
        parallaxImgs.forEach(img => {
          const r = img.getBoundingClientRect();
          if (r.bottom < -50 || r.top > vh + 50) return;
          // -1 (top of viewport) → 0 (centro) → 1 (bottom)
          const center = r.top + r.height / 2;
          const progress = (center - vh / 2) / vh;
          const ty = progress * 24; // 24px max shift
          img.style.transform = `translateY(${ty.toFixed(1)}px) scale(1.08)`;
        });
        ticking = false;
      };
      window.addEventListener('scroll', () => {
        if (!ticking) { requestAnimationFrame(update); ticking = true; }
      }, { passive: true });
      window.addEventListener('resize', update, { passive: true });
      update();
    }
  }

  /* ——— Cards: 3D tilt (mousemove rotate, dolce e leggero) ——— */
  if (!reduced && hoverable) {
    document.querySelectorAll('[data-tilt]').forEach(card => {
      card.style.transformStyle = 'preserve-3d';
      let raf = null;
      let rx = 0, ry = 0, tx = 0, ty = 0;
      const apply = () => {
        card.style.transform = `perspective(1000px) rotateX(${rx.toFixed(2)}deg) rotateY(${ry.toFixed(2)}deg) translateY(${ty}px)`;
        raf = null;
      };
      card.addEventListener('mousemove', e => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        rx = -py * 4; // max 4° su asse X
        ry = px * 4;  // max 4° su asse Y
        ty = -6;
        if (!raf) raf = requestAnimationFrame(apply);
      });
      card.addEventListener('mouseleave', () => {
        rx = 0; ry = 0; ty = 0;
        card.style.transition = 'transform 700ms cubic-bezier(0.22, 1, 0.36, 1)';
        apply();
        setTimeout(() => { card.style.transition = ''; }, 700);
      });
      card.addEventListener('mouseenter', () => {
        card.style.transition = '';
      });
    });
  }

  /* ——— Magnetic CTA: il bottone si avvicina al cursor (sottile) ——— */
  if (!reduced && hoverable) {
    document.querySelectorAll('[data-magnetic]').forEach(el => {
      const strength = 0.25;
      let raf = null;
      const apply = (x, y) => {
        el.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px)`;
        raf = null;
      };
      el.addEventListener('mousemove', e => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * strength;
        const y = (e.clientY - r.top - r.height / 2) * strength;
        if (!raf) raf = requestAnimationFrame(() => apply(x, y));
      });
      el.addEventListener('mouseleave', () => {
        el.style.transition = 'transform 600ms cubic-bezier(0.34, 1.56, 0.64, 1)';
        apply(0, 0);
        setTimeout(() => { el.style.transition = ''; }, 600);
      });
      el.addEventListener('mouseenter', () => { el.style.transition = ''; });
    });
  }

  /* ——— FAB stack: visibile dopo 600px ——— */
  const fab = document.getElementById('fab-stack');
  const fabTop = document.getElementById('fab-top');
  if (fab) {
    let ticking = false;
    const update = () => {
      fab.classList.toggle('is-visible', window.scrollY > 600);
      ticking = false;
    };
    window.addEventListener('scroll', () => {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }
  if (fabTop) {
    fabTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ——— Mask reveal: chiude .h3-mask con .in se è già visibile (safety) ——— */
  // (la classe .reveal e .h3-mask sono già gestite dall'IO globale di main.js)

})();
