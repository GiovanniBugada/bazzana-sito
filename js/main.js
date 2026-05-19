/* =======================================================
   Motor Garden Bazzana — Main JS
   ======================================================= */

(() => {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ——— Loader ——— */
  const loader = document.querySelector('.loader');
  if (loader) {
    window.addEventListener('load', () => {
      const min = reduced ? 200 : 1400;
      setTimeout(() => {
        loader.classList.add('is-done');
        document.body.classList.add('is-loaded');
        const hero = document.querySelector('.hero');
        if (hero) hero.classList.add('is-loaded');
      }, min);
    });
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

  /* ——— Custom cursor ——— */
  if (!reduced && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    const cursor = document.createElement('div');
    cursor.className = 'cursor';
    const label = document.createElement('span');
    label.className = 'cursor__label';
    cursor.appendChild(label);
    document.body.appendChild(cursor);

    let x = window.innerWidth / 2, y = window.innerHeight / 2;
    let tx = x, ty = y;

    window.addEventListener('mousemove', e => {
      x = e.clientX; y = e.clientY;
    });

    const animate = () => {
      tx += (x - tx) * 0.22;
      ty += (y - ty) * 0.22;
      cursor.style.transform = `translate(${tx}px, ${ty}px) translate(-50%, -50%)`;
      requestAnimationFrame(animate);
    };
    animate();

    const hoverables = 'a, button, .cat-card, .card, .chip, [data-cursor]';
    document.addEventListener('mouseover', e => {
      const t = e.target.closest(hoverables);
      if (t) {
        cursor.classList.add('is-hover');
        const lbl = t.getAttribute('data-cursor');
        if (lbl) label.textContent = lbl;
        else label.textContent = '';
      }
    });
    document.addEventListener('mouseout', e => {
      const t = e.target.closest(hoverables);
      if (t) {
        cursor.classList.remove('is-hover');
        label.textContent = '';
      }
    });
  }

  /* ——— Reveal on scroll ——— */
  const revealEls = document.querySelectorAll('.reveal, .reveal-mask');
  if ('IntersectionObserver' in window && revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          en.target.classList.add('in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -10% 0px' });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('in'));
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

  /* ——— Page transition out (mask) ——— */
  const mask = document.createElement('div');
  mask.className = 'page-mask';
  document.body.appendChild(mask);
  // entry: in
  if (!reduced) {
    mask.classList.add('is-out');
    setTimeout(() => mask.classList.remove('is-out'), 950);
  }
  // exit: applied on internal link click
  document.addEventListener('click', e => {
    const a = e.target.closest('a');
    if (!a) return;
    const href = a.getAttribute('href');
    if (!href) return;
    if (href.startsWith('#')) return;
    if (a.target === '_blank') return;
    if (href.startsWith('http') && !href.includes(location.host)) return;
    if (href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('https://wa.me')) return;
    if (reduced) return;
    e.preventDefault();
    mask.classList.add('is-in');
    setTimeout(() => { window.location.href = href; }, 700);
  });

  /* ——— Filtri prodotti ——— */
  const chips = document.querySelectorAll('.chip[data-filter]');
  if (chips.length) {
    const cards = document.querySelectorAll('[data-cat]');
    chips.forEach(c => {
      c.addEventListener('click', () => {
        chips.forEach(x => x.classList.remove('is-active'));
        c.classList.add('is-active');
        const f = c.getAttribute('data-filter');
        cards.forEach(card => {
          if (f === 'all' || card.getAttribute('data-cat') === f) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  /* ——— Anno corrente in footer ——— */
  document.querySelectorAll('[data-year]').forEach(el => {
    el.textContent = new Date().getFullYear();
  });

  /* ——— Suono ambientale (opzionale) ——— */
  const soundBtn = document.querySelector('.sound-toggle');
  if (soundBtn) {
    let audio = null;
    soundBtn.addEventListener('click', () => {
      if (!audio) {
        audio = new Audio('https://cdn.freesound.org/previews/467/467900_5121236-lq.mp3');
        audio.loop = true;
        audio.volume = 0.18;
      }
      if (audio.paused) {
        audio.play().catch(() => {});
        soundBtn.textContent = 'Audio ON';
      } else {
        audio.pause();
        soundBtn.textContent = 'Audio';
      }
    });
  }

})();
