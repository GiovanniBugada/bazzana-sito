/* =========================================================
   WOW FX — Fase 10.2-10.5
   Hero scene change · Confetti form · Konami code · Easter cursor
   Audio ambient toggle · Page transitions
   ========================================================= */
(() => {
  'use strict';

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hover = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const touch = matchMedia('(pointer: coarse)').matches;

  /* ============================================================
     10.2 · HERO SCROLL-DRIVEN SCENE CHANGE
     Inietta una scene-photo nel hero, attiva is-scrolled dopo 80px
     ============================================================ */
  function initHeroScene() {
    const hero = document.querySelector('.hero-v2');
    if (!hero) return;
    if (innerWidth < 960) return;

    // Inietta scene-photo card se non esiste
    if (!hero.querySelector('.hero-v2__scene')) {
      const scene = document.createElement('div');
      scene.className = 'hero-v2__scene';
      scene.setAttribute('aria-hidden', 'true');
      scene.innerHTML = `
        <img src="assets/img/bazzana/scena-15.jpg" alt="" loading="lazy">
        <span class="hero-v2__scene-cap">Showroom · Cene</span>
      `;
      hero.appendChild(scene);
    }

    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        const r = hero.getBoundingClientRect();
        const scrolled = Math.abs(Math.min(0, r.top));
        if (scrolled > 80) hero.classList.add('is-scrolled');
        else hero.classList.remove('is-scrolled');
        ticking = false;
      });
    };
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ============================================================
     10.3 · CONFETTI BURST (canvas)
     ============================================================ */
  function fireConfetti() {
    if (reduced) return;
    let canvas = document.querySelector('.confetti');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.className = 'confetti';
      document.body.appendChild(canvas);
    }
    canvas.width = innerWidth;
    canvas.height = innerHeight;
    const ctx = canvas.getContext('2d');

    const colors = ['#ee5e1f', '#ff7a45', '#c84d18', '#f2efe7', '#1f3a2e'];
    const N = 120;
    const particles = [];
    for (let i = 0; i < N; i++) {
      particles.push({
        x: innerWidth / 2,
        y: innerHeight / 2,
        vx: (Math.random() - 0.5) * 16,
        vy: (Math.random() - 1.2) * 14,
        size: 4 + Math.random() * 5,
        color: colors[Math.floor(Math.random() * colors.length)],
        rot: Math.random() * Math.PI * 2,
        vr: (Math.random() - 0.5) * 0.4,
        life: 0,
        maxLife: 120 + Math.random() * 60
      });
    }
    const gravity = 0.55;
    const damp = 0.98;
    let raf = null;
    const step = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      let alive = 0;
      for (const p of particles) {
        if (p.life > p.maxLife) continue;
        alive++;
        p.vy += gravity;
        p.vx *= damp;
        p.x += p.vx;
        p.y += p.vy;
        p.rot += p.vr;
        p.life++;
        const fade = 1 - p.life / p.maxLife;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.globalAlpha = fade;
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.4);
        ctx.restore();
      }
      if (alive > 0) raf = requestAnimationFrame(step);
      else { canvas.remove(); }
    };
    raf = requestAnimationFrame(step);
  }

  /* ============================================================
     10.3 · FORM SUBMIT HANDLER (contatti)
     ============================================================ */
  function initContactForm() {
    const form = document.querySelector('.contact__form');
    if (!form) return;
    form.addEventListener('submit', (e) => {
      // Lascia partire la submit nativa MA mostra confetti subito
      if (!form.checkValidity()) return;
      form.classList.add('is-sent');
      fireConfetti();
      // Cambia testo bottone
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        const orig = btn.textContent;
        btn.textContent = 'Grazie. Ti rispondiamo presto.';
        setTimeout(() => { btn.textContent = orig; form.classList.remove('is-sent'); }, 6000);
      }
    });
  }

  /* ============================================================
     10.4 · KONAMI CODE — ↑↑↓↓←→←→BA
     ============================================================ */
  function initKonami() {
    const sequence = ['ArrowUp','ArrowUp','ArrowDown','ArrowDown','ArrowLeft','ArrowRight','ArrowLeft','ArrowRight','b','a'];
    let pos = 0;
    addEventListener('keydown', (e) => {
      const key = e.key.length === 1 ? e.key.toLowerCase() : e.key;
      if (key === sequence[pos]) {
        pos++;
        if (pos === sequence.length) {
          pos = 0;
          openKonami();
        }
      } else {
        pos = 0;
      }
    });
  }
  function openKonami() {
    let modal = document.querySelector('.konami');
    if (!modal) {
      modal = document.createElement('div');
      modal.className = 'konami';
      modal.setAttribute('role', 'dialog');
      modal.setAttribute('aria-label', 'Easter egg');
      modal.innerHTML = `
        <div class="konami__inner">
          <button class="konami__close" aria-label="Chiudi">×</button>
          <span class="konami__eyebrow">Easter egg · BAZZANA</span>
          <h2 class="konami__title">Hai trovato<br><em>il banco segreto.</em></h2>
          <div class="konami__photo">
            <img src="assets/img/bazzana/scena-08.jpg" alt="Banco di lavoro Bazzana">
          </div>
          <p class="konami__caption">Cene · Val Seriana · Aperti 2026 · Made with ❤︎ in valle Seriana</p>
        </div>
      `;
      document.body.appendChild(modal);
      const close = () => modal.classList.remove('is-open');
      modal.querySelector('.konami__close').addEventListener('click', close);
      modal.addEventListener('click', (e) => { if (e.target === modal) close(); });
      addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
    }
    modal.classList.add('is-open');
    fireConfetti();
  }

  /* ============================================================
     10.4 · EASTER EGG CURSOR — cambia stile su zone tematiche
     ============================================================ */
  function initEggCursor() {
    if (reduced || !hover || touch) return;
    const cur = document.getElementById('cur');
    if (!cur) return;
    const zones = [
      { sel: '.dual-focus__card[href*="officina"], .immersive, .feature-pin__panel[data-step="01"]', cls: 'is-egg-officina' },
      { sel: '.dual-focus__card[href*="prodotti"], .feature-pin__panel[data-step="02"]', cls: 'is-egg-verde' },
      { sel: '.visit-v2, .feature-pin__panel[data-step="03"]', cls: 'is-egg-cene' }
    ];
    document.addEventListener('mouseover', (e) => {
      let matched = null;
      for (const z of zones) {
        if (e.target.closest(z.sel)) { matched = z.cls; break; }
      }
      cur.classList.remove('is-egg-officina', 'is-egg-verde', 'is-egg-cene');
      if (matched) cur.classList.add(matched);
    });
  }

  /* ============================================================
     10.5 · DARK/LIGHT AUTO — già dark, mantieni semantico
     ============================================================ */
  function initThemeAuto() {
    document.documentElement.setAttribute('data-theme-auto', '1');
  }

  /* ============================================================
     10.5 · AUDIO AMBIENT TOGGLE — vento foresta
     File: assets/audio/ambient.mp3 (opzionale, se presente)
     ============================================================ */
  function initAudioToggle() {
    if (touch) return;
    const btn = document.createElement('button');
    btn.className = 'audio-toggle';
    btn.setAttribute('aria-label', 'Attiva audio ambient');
    btn.setAttribute('aria-pressed', 'false');
    btn.textContent = '♪';
    document.body.appendChild(btn);

    let audio = null;
    let isOn = false;
    btn.addEventListener('click', () => {
      isOn = !isOn;
      btn.classList.toggle('is-on', isOn);
      btn.setAttribute('aria-pressed', String(isOn));
      btn.setAttribute('aria-label', isOn ? 'Disattiva audio' : 'Attiva audio');
      if (isOn) {
        if (!audio) {
          audio = new Audio('assets/audio/ambient.mp3');
          audio.loop = true;
          audio.volume = 0.25;
        }
        audio.play().catch(() => {
          // file non disponibile: chiudi il toggle silenziosamente
          isOn = false;
          btn.classList.remove('is-on');
          btn.setAttribute('aria-pressed', 'false');
        });
      } else if (audio) {
        audio.pause();
      }
    });
  }

  /* ============================================================
     10.4 · PAGE TRANSITIONS — fade overlay su nav interna
     ============================================================ */
  function initPageTransitions() {
    if (reduced) return;
    // Crea overlay
    let overlay = document.querySelector('.page-transition');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'page-transition';
      overlay.setAttribute('aria-hidden', 'true');
      document.body.appendChild(overlay);
    }

    // Se siamo arrivati da una transizione, fai finishing
    if (sessionStorage.getItem('mgb_transition_in') === '1') {
      sessionStorage.removeItem('mgb_transition_in');
      overlay.classList.add('is-active', 'is-finishing');
      setTimeout(() => {
        overlay.classList.remove('is-active', 'is-finishing');
      }, 1100);
    }

    // Intercetta link interni
    document.addEventListener('click', (e) => {
      const link = e.target.closest('a[href]');
      if (!link) return;
      const href = link.getAttribute('href');
      if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('http')) return;
      if (link.target === '_blank') return;
      e.preventDefault();
      overlay.classList.add('is-active');
      sessionStorage.setItem('mgb_transition_in', '1');
      setTimeout(() => { location.href = href; }, 650);
    });
  }

  /* ============================================================
     INIT
     ============================================================ */
  function init() {
    initHeroScene();
    initContactForm();
    initKonami();
    initEggCursor();
    initThemeAuto();
    // initAudioToggle();  // rimosso su richiesta — il sito è no-audio
    initPageTransitions();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
