/* =========================================================
   FOTO GALLERY — popola masonry + lightbox.

   Rotazioni manuali:
   - js/foto-rotations.js esporta window.BAZZANA_FOTO_ROTATIONS
     come mappa { numeroFoto1Based: gradiOrari (90|180|270) }.
   - Applichiamo la rotazione via CSS transform + scambio w/h
     quando la rotazione è 90 o 270.
   - Aggiunto bottone "ruota" nel lightbox per testare al volo
     una rotazione e copiarne il codice da incollare nel manifest.
   ========================================================= */
(() => {
  'use strict';

  const gallery = document.getElementById('foto-gallery');
  if (!gallery) return;
  const photos = window.BAZZANA_FOTO || [];
  if (!photos.length) return;

  const ROTATIONS = window.BAZZANA_FOTO_ROTATIONS || {};

  /* Lettura/scrittura rotation override (manifest + override locale).
     Il manifest server-side (foto-rotations.js) ha la priorita; in dev
     localStorage permette di provare prima di committare. */
  function getRotation(idx0) {
    const num = idx0 + 1; // 1-based
    const manifest = ROTATIONS[num];
    if (manifest === 90 || manifest === 180 || manifest === 270) return manifest;
    try {
      const local = JSON.parse(localStorage.getItem('bzn_foto_rotations') || '{}');
      const v = local[num];
      if (v === 90 || v === 180 || v === 270) return v;
    } catch (e) {}
    return 0;
  }
  function setLocalRotation(idx0, deg) {
    try {
      const local = JSON.parse(localStorage.getItem('bzn_foto_rotations') || '{}');
      if (deg === 0) delete local[idx0 + 1];
      else local[idx0 + 1] = deg;
      localStorage.setItem('bzn_foto_rotations', JSON.stringify(local));
    } catch (e) {}
  }

  /* Render gallery */
  function render() {
    gallery.innerHTML = '';
    photos.forEach((p, i) => {
      const a = document.createElement('button');
      a.type = 'button';
      a.className = 'foto__item';
      a.dataset.idx = String(i);
      a.dataset.src = p.src;
      a.setAttribute('aria-label', 'Apri foto ' + (i + 1));
      const deg = getRotation(i);
      // Quando ruotiamo di 90/270, dobbiamo "swappare" w/h del wrapper
      // per mantenere proporzioni corrette nel masonry.
      let w = p.w, h = p.h;
      if (deg === 90 || deg === 270) { w = p.h; h = p.w; }
      const rotStyle = deg ? `style="--rotate:${deg}deg"` : '';
      const rotClass = deg ? ' has-rotation' : '';
      a.innerHTML = `
        <img src="${p.src}" alt="Foto ${i + 1} — showroom Motor Garden Bazzana" loading="lazy" width="${w}" height="${h}"${rotStyle ? ' ' + rotStyle : ''} class="foto__item-img${rotClass}">
        <span class="foto__item-num">${String(i + 1).padStart(3, '0')}</span>
      `;
      a.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        openLightbox(i);
      });
      gallery.appendChild(a);
    });
    const counter = document.getElementById('foto-count');
    if (counter) counter.textContent = photos.length;
    revealOnScroll();
  }

  function revealOnScroll() {
    if (!('IntersectionObserver' in window)) {
      document.querySelectorAll('.foto__item').forEach(el => el.classList.add('is-visible'));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          en.target.classList.add('is-visible');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.05, rootMargin: '0px 0px -50px 0px' });
    document.querySelectorAll('.foto__item').forEach(el => io.observe(el));
  }

  /* Layout switch (masonry / grid) */
  function initLayoutSwitch() {
    const buttons = document.querySelectorAll('.foto__layout-btn');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        gallery.classList.toggle('is-grid', btn.dataset.layout === 'grid');
      });
    });
  }

  /* Admin: ?admin=1 nell'URL abilita il bottone "ruota" nel lightbox.
     Comodo per identificare foto storte: ruoti, vedi il numero foto,
     e copi nel manifest. */
  const isAdmin = new URLSearchParams(location.search).get('admin') === '1';

  /* Lightbox cinematic */
  let lightbox = null;
  let currentIdx = 0;
  function getLightbox() {
    if (lightbox) return lightbox;
    lightbox = document.createElement('div');
    lightbox.className = 'foto-lightbox';
    lightbox.innerHTML = `
      <button class="foto-lightbox__close" aria-label="Chiudi">×</button>
      <button class="foto-lightbox__prev" aria-label="Foto precedente">‹</button>
      <button class="foto-lightbox__next" aria-label="Foto successiva">›</button>
      ${isAdmin ? '<button class="foto-lightbox__rotate" aria-label="Ruota 90°" title="Ruota 90° (admin)">↻</button>' : ''}
      <img class="foto-lightbox__img" src="" alt="">
      <span class="foto-lightbox__caption">001 / ${photos.length}</span>
    `;
    document.body.appendChild(lightbox);
    lightbox.querySelector('.foto-lightbox__close').addEventListener('click', closeLightbox);
    lightbox.querySelector('.foto-lightbox__prev').addEventListener('click', prevPhoto);
    lightbox.querySelector('.foto-lightbox__next').addEventListener('click', nextPhoto);
    const rotateBtn = lightbox.querySelector('.foto-lightbox__rotate');
    if (rotateBtn) rotateBtn.addEventListener('click', rotateCurrent);
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener('keydown', (e) => {
      if (!lightbox.classList.contains('is-open')) return;
      if (e.key === 'Escape') closeLightbox();
      else if (e.key === 'ArrowLeft') prevPhoto();
      else if (e.key === 'ArrowRight') nextPhoto();
      else if (isAdmin && e.key.toLowerCase() === 'r') rotateCurrent();
    });
    return lightbox;
  }
  function openLightbox(idx) {
    const lb = getLightbox();
    currentIdx = idx;
    updateLightboxImg();
    lb.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }
  function closeLightbox() {
    if (lightbox) lightbox.classList.remove('is-open');
    document.body.style.overflow = '';
  }
  function updateLightboxImg() {
    if (!lightbox) return;
    const p = photos[currentIdx];
    const img = lightbox.querySelector('.foto-lightbox__img');
    img.src = p.src;
    img.alt = `Foto ${currentIdx + 1} — Motor Garden Bazzana`;
    const deg = getRotation(currentIdx);
    img.style.transform = deg ? `rotate(${deg}deg)` : '';
    let caption = String(currentIdx + 1).padStart(3, '0') + ' / ' + photos.length;
    if (isAdmin && deg) caption += '  ·  rot ' + deg + '°';
    lightbox.querySelector('.foto-lightbox__caption').textContent = caption;
  }
  function rotateCurrent() {
    // Ciclo: 0 -> 90 -> 180 -> 270 -> 0
    const cur = getRotation(currentIdx);
    const next = (cur + 90) % 360;
    setLocalRotation(currentIdx, next);
    updateLightboxImg();
    // Mostra istruzioni: come aggiungere al manifest
    if (next !== 0) {
      console.log(
        '[Bazzana foto-rotations] Aggiungi a js/foto-rotations.js:\n  ' +
        (currentIdx + 1) + ': ' + next + ','
      );
    } else {
      console.log('[Bazzana foto-rotations] foto ' + (currentIdx + 1) + ' tornata a 0°');
    }
  }
  function prevPhoto() {
    currentIdx = (currentIdx - 1 + photos.length) % photos.length;
    updateLightboxImg();
  }
  function nextPhoto() {
    currentIdx = (currentIdx + 1) % photos.length;
    updateLightboxImg();
  }

  /* Init */
  render();
  initLayoutSwitch();

  // Esporta API minima per dev/admin
  window.bznFoto = {
    rotateById: (num1, deg) => {
      setLocalRotation(num1 - 1, deg);
      render();
    },
    exportRotations: () => {
      try {
        return JSON.parse(localStorage.getItem('bzn_foto_rotations') || '{}');
      } catch (e) {
        return {};
      }
    },
    clearRotations: () => {
      localStorage.removeItem('bzn_foto_rotations');
      render();
    }
  };
})();
