/* =========================================================
   WEBP UPGRADE — se il browser supporta WebP, sostituisce
   trasparentemente tutte le immagini .png/.jpg con la
   versione .webp parallela (se esistente).
   Risparmio: 50-70% di banda. Browser vecchi: tutto invariato.
   ========================================================= */
(() => {
  'use strict';

  // 1) Test WebP support una sola volta
  function supportsWebP() {
    const c = document.createElement('canvas');
    if (!c.getContext || !c.getContext('2d')) return false;
    return c.toDataURL('image/webp').indexOf('data:image/webp') === 0;
  }

  if (!supportsWebP()) return;

  // 2) Helper: trasforma path .png/.jpg/.jpeg → .webp (case insensitive)
  function toWebp(url) {
    if (!url) return url;
    return url.replace(/\.(png|jpg|jpeg)(\?.*)?$/i, '.webp$2');
  }

  // 3) Upgrade di tutti gli <img> già presenti
  function upgradeImg(img) {
    if (img.dataset.webpUpgraded) return;
    img.dataset.webpUpgraded = '1';
    const oldSrc = img.getAttribute('src');
    if (oldSrc) {
      const w = toWebp(oldSrc);
      if (w !== oldSrc) {
        // Fallback se il .webp non esiste: ritorna al PNG/JPG
        img.addEventListener('error', function fallback() {
          img.removeEventListener('error', fallback);
          img.src = oldSrc;
        }, { once: true });
        img.src = w;
      }
    }
    // srcset (responsive)
    const ss = img.getAttribute('srcset');
    if (ss) {
      const newSs = ss.split(',').map(part => {
        const t = part.trim().split(/\s+/);
        t[0] = toWebp(t[0]);
        return t.join(' ');
      }).join(', ');
      img.setAttribute('srcset', newSs);
    }
  }

  function upgradeSource(src) {
    if (src.dataset.webpUpgraded) return;
    src.dataset.webpUpgraded = '1';
    const ss = src.getAttribute('srcset');
    if (ss) {
      const newSs = ss.split(',').map(part => {
        const t = part.trim().split(/\s+/);
        t[0] = toWebp(t[0]);
        return t.join(' ');
      }).join(', ');
      src.setAttribute('srcset', newSs);
    }
  }

  function upgradeAll(root = document) {
    root.querySelectorAll('img:not([data-no-webp])').forEach(upgradeImg);
    root.querySelectorAll('source:not([data-no-webp])').forEach(upgradeSource);
  }

  // 4) Esegui all'init
  upgradeAll();

  // 5) Osserva il DOM per immagini iniettate dopo (catalog modal, search, ecc.)
  if ('MutationObserver' in window) {
    const obs = new MutationObserver(muts => {
      muts.forEach(m => {
        m.addedNodes.forEach(n => {
          if (n.nodeType !== 1) return;
          if (n.tagName === 'IMG') upgradeImg(n);
          else if (n.tagName === 'SOURCE') upgradeSource(n);
          else if (n.querySelectorAll) upgradeAll(n);
        });
      });
    });
    obs.observe(document.body, { childList: true, subtree: true });
  }

  // 6) Esponi anche utility globale per chi vuole upgradar manualmente
  window.BZN_toWebp = toWebp;
})();
