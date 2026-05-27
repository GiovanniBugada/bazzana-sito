/* =========================================================
   STORIA PRO — scroll-driven storytelling
   - Capitolo "is-active" quando al centro del viewport
   - Track laterale con dot evidenziato + linea che cresce
   - Click sui dot per saltare al capitolo
   - Visual che si ingrandisce quando attivo (via CSS)
   - Particelle nel hero
   ========================================================= */
(() => {
  'use strict';

  const main = document.querySelector('main.storia');
  if (!main) return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ——— 1. Capitoli — is-active on middle-of-viewport ——— */
  const chapters = Array.from(document.querySelectorAll('.storia__chapter'));
  if (chapters.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          en.target.classList.add('is-active');
          updateTrackDot(en.target.id);
        }
      });
    }, { threshold: 0.18, rootMargin: '-25% 0px -25% 0px' });
    chapters.forEach(c => io.observe(c));
  } else {
    chapters.forEach(c => c.classList.add('is-active'));
  }

  /* ——— 2. Track laterale ——— */
  const track = document.querySelector('.storia__track');
  const trackFill = document.querySelector('.storia__track-fill');
  const trackDots = Array.from(document.querySelectorAll('.storia__track-dots li'));

  // Mostra track dopo il hero
  const hero = document.querySelector('.storia__hero');
  if (track && hero && 'IntersectionObserver' in window) {
    const heroIO = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        // Quando il hero NON è più visibile (uscito dalla viewport), mostra track
        if (en.intersectionRatio < 0.4) {
          track.classList.add('is-visible');
        } else {
          track.classList.remove('is-visible');
        }
      });
    }, { threshold: [0.4] });
    heroIO.observe(hero);
  }

  function updateTrackDot(activeId) {
    trackDots.forEach(li => {
      const anchor = li.dataset.anchor;
      li.classList.toggle('is-active', anchor === activeId);
    });
  }

  // Click sui dot per saltare al capitolo
  trackDots.forEach(li => {
    li.addEventListener('click', () => {
      const target = document.getElementById(li.dataset.anchor);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    // Tastiera
    li.setAttribute('tabindex', '0');
    li.setAttribute('role', 'button');
    li.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        li.click();
      }
    });
  });

  // Progress fill della linea verticale
  function updateProgress() {
    if (!trackFill || !chapters.length) return;
    const first = chapters[0];
    const last = chapters[chapters.length - 1];
    const start = first.offsetTop;
    const end = last.offsetTop + last.offsetHeight;
    const span = end - start;
    const scrolled = scrollY + innerHeight * 0.5 - start;
    const p = Math.max(0, Math.min(1, scrolled / span));
    trackFill.style.height = (p * 100) + '%';
  }
  if (!reduced) {
    let ticking = false;
    addEventListener('scroll', () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        updateProgress();
        ticking = false;
      });
    }, { passive: true });
    updateProgress();
  }

  /* ——— 3. Scroll-driven scale & parallax sulle immagini ——— */
  if (!reduced) {
    const stages = Array.from(document.querySelectorAll('.storia__chapter-stage img'));
    let ticking2 = false;
    const updateScale = () => {
      stages.forEach(img => {
        const r = img.getBoundingClientRect();
        const centerY = innerHeight / 2;
        const dist = Math.abs(r.top + r.height / 2 - centerY);
        const maxDist = innerHeight;
        const p = Math.max(0, 1 - dist / maxDist);
        // Scala 1.0 al centro, 1.12 ai bordi (parallax-like)
        const scale = 1 + (1 - p) * 0.08;
        // Translate verticale leggero (parallax)
        const ty = (r.top + r.height / 2 - centerY) * 0.04;
        img.style.transform = `scale(${scale}) translateY(${ty}px)`;
      });
      ticking2 = false;
    };
    addEventListener('scroll', () => {
      if (ticking2) return;
      ticking2 = true;
      requestAnimationFrame(updateScale);
    }, { passive: true });
    updateScale();
  }

  /* ——— 4. Particelle hero ——— */
  function initStoriaParticles() {
    if (reduced) return;
    const canvas = document.getElementById('storia-particles');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const host = canvas.parentElement || document.querySelector('.storia__hero');
    let w = 0, h = 0;
    let mx = -9999, my = -9999;
    const N = 48;
    const particles = [];

    function resize() {
      const dpr = Math.min(devicePixelRatio || 1, 2);
      const rect = host.getBoundingClientRect();
      w = Math.max(rect.width, 320);
      h = Math.max(rect.height, 320);
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function reset(p) {
      p.x = Math.random() * w;
      p.y = h + Math.random() * 100;
      p.r = 0.8 + Math.random() * 2.4;
      p.vx = (Math.random() - 0.5) * 0.2;
      p.vy = -0.12 - Math.random() * 0.32;
      p.a = 0.2 + Math.random() * 0.7;
      p.life = 0;
      p.maxLife = 260 + Math.random() * 220;
    }
    for (let i = 0; i < N; i++) {
      const p = {};
      reset(p);
      p.y = Math.random() * h;
      p.life = Math.random() * p.maxLife;
      particles.push(p);
    }
    resize();
    setTimeout(resize, 250);
    addEventListener('resize', resize);

    host.addEventListener('mousemove', (e) => {
      const r = canvas.getBoundingClientRect();
      mx = e.clientX - r.left;
      my = e.clientY - r.top;
    });
    host.addEventListener('mouseleave', () => { mx = -9999; my = -9999; });

    function step() {
      if (!canvas.isConnected) return;
      ctx.clearRect(0, 0, w, h);
      for (const p of particles) {
        const ddx = p.x - mx;
        const ddy = p.y - my;
        const d2 = ddx * ddx + ddy * ddy;
        if (d2 < 16000) {
          const d = Math.sqrt(d2) || 1;
          const f = (1 - d / 126) * 1.4;
          p.vx += (ddx / d) * f * 0.16;
          p.vy += (ddy / d) * f * 0.16;
        }
        p.vx *= 0.97;
        p.vy *= 0.97;
        p.x += p.vx;
        p.y += p.vy;
        p.life++;
        if (p.life > p.maxLife || p.y < -20 || p.x < -20 || p.x > w + 20) reset(p);
        const fade = 1 - p.life / p.maxLife;
        const a = p.a * fade;
        const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 6);
        grad.addColorStop(0, 'rgba(255, 154, 84, ' + a + ')');
        grad.addColorStop(0.4, 'rgba(242, 101, 34, ' + (a * 0.35) + ')');
        grad.addColorStop(1, 'rgba(242, 101, 34, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r * 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = 'rgba(255, 220, 180, ' + (a * 0.85) + ')';
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
      }
      requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  initStoriaParticles();
})();
