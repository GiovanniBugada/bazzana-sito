/* ============================================================
   EXTRAS JS — wishlist + toast + cookie GDPR + search + lightbox
   ============================================================ */
(() => {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ——— TOAST NOTIFICATION SYSTEM ——— */
  function showToast(message, type) {
    type = type || 'info';
    let host = document.getElementById('toast-host');
    if (!host) {
      host = document.createElement('div');
      host.id = 'toast-host';
      host.className = 'toast-host';
      document.body.appendChild(host);
    }
    const t = document.createElement('div');
    t.className = 'toast toast--' + type;
    t.setAttribute('role', 'status');
    t.innerHTML = '<span class="toast__msg">' + message + '</span>';
    host.appendChild(t);
    requestAnimationFrame(() => t.classList.add('is-in'));
    setTimeout(() => {
      t.classList.remove('is-in');
      setTimeout(() => t.remove(), 400);
    }, 3200);
  }
  window.showToast = showToast;

  /* ——— WISHLIST localStorage ——— */
  const WL_KEY = 'bzn_wishlist_v1';
  function getWishlist() {
    try { return JSON.parse(localStorage.getItem(WL_KEY) || '[]'); }
    catch (e) { return []; }
  }
  function saveWishlist(list) {
    try { localStorage.setItem(WL_KEY, JSON.stringify(list)); } catch (e) {}
    updateWishlistBadge();
    refreshWishlistBtns();
  }
  function toggleWishlistItem(id, name, img) {
    const list = getWishlist();
    const idx = list.findIndex(x => x.id === id);
    if (idx >= 0) {
      list.splice(idx, 1);
      saveWishlist(list);
      showToast('Rimosso dai preferiti: ' + name, 'info');
      return false;
    } else {
      list.push({ id, name, img, ts: Date.now() });
      saveWishlist(list);
      showToast('Aggiunto ai preferiti: ' + name, 'success');
      return true;
    }
  }
  function isInWishlist(id) {
    return getWishlist().some(x => x.id === id);
  }
  function updateWishlistBadge() {
    const count = getWishlist().length;
    document.querySelectorAll('[data-wishlist-count]').forEach(el => {
      el.textContent = count;
      el.classList.toggle('is-empty', count === 0);
    });
  }
  function refreshWishlistBtns() {
    document.querySelectorAll('.wl-btn').forEach(btn => {
      const id = btn.getAttribute('data-id');
      btn.classList.toggle('is-active', isInWishlist(id));
    });
  }

  // Inserisci bottone cuore su ogni depth-card del catalogo
  function injectWishlistButtons() {
    document.querySelectorAll('.product-catalog .depth-card').forEach(card => {
      if (card.querySelector('.wl-btn')) return;
      const img = card.querySelector('img');
      const nameEl = card.querySelector('.depth-card__name');
      if (!img || !nameEl) return;
      const id = img.getAttribute('src');
      const name = nameEl.textContent.trim();
      const btn = document.createElement('button');
      btn.className = 'wl-btn';
      btn.setAttribute('type', 'button');
      btn.setAttribute('aria-label', 'Aggiungi ai preferiti');
      btn.setAttribute('data-id', id);
      btn.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12 21s-7-4.5-9-9c-1.5-3.4 1-7 4.5-7 2 0 3.5 1 4.5 2.5C13 6 14.5 5 16.5 5 20 5 22.5 8.6 21 12c-2 4.5-9 9-9 9z"/></svg>';
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        toggleWishlistItem(id, name, id);
      });
      const base = card.querySelector('.depth-card__base');
      if (base) base.appendChild(btn);
    });
    refreshWishlistBtns();
  }

  /* ——— SEARCH catalogo (filtro istantaneo) ——— */
  function initCatalogSearch() {
    const input = document.getElementById('catalog-search');
    if (!input) return;
    const cards = document.querySelectorAll('.product-catalog .depth-card');
    const counter = document.getElementById('catalog-search-count');
    const debounce = (fn, ms) => {
      let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
    };
    const apply = () => {
      const q = input.value.trim().toLowerCase();
      let visible = 0;
      cards.forEach(card => {
        const name = card.querySelector('.depth-card__name')?.textContent.toLowerCase() || '';
        const desc = card.querySelector('.depth-card__desc')?.textContent.toLowerCase() || '';
        const hay = name + ' ' + desc;
        const ok = !q || hay.includes(q);
        card.style.display = ok ? '' : 'none';
        if (ok) visible++;
      });
      if (counter) counter.textContent = visible + ' risultati';
      // Nascondi gruppi vuoti
      document.querySelectorAll('.product-catalog .cat-group').forEach(g => {
        const anyVisible = Array.from(g.querySelectorAll('.depth-card'))
          .some(c => c.style.display !== 'none');
        g.style.display = anyVisible ? '' : 'none';
      });
    };
    input.addEventListener('input', debounce(apply, 160));
  }

  /* ——— COOKIE BANNER GDPR ——— */
  const COOKIE_KEY = 'bzn_cookies_v1';
  function initCookieBanner() {
    if (localStorage.getItem(COOKIE_KEY)) return;
    const banner = document.createElement('div');
    banner.className = 'cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Informativa cookie');
    banner.innerHTML = '\
      <div class="cookie-banner__inner">\
        <div class="cookie-banner__text">\
          <strong>Usiamo i cookie</strong>\
          <p>Usiamo cookie tecnici per il funzionamento del sito. Nessun tracker pubblicitario, nessuna profilazione. Vedi la <a href="#" tabindex="0">Privacy Policy</a>.</p>\
        </div>\
        <div class="cookie-banner__actions">\
          <button class="cookie-banner__btn cookie-banner__btn--primary" data-act="accept">Accetta</button>\
          <button class="cookie-banner__btn" data-act="essential">Solo tecnici</button>\
        </div>\
      </div>';
    document.body.appendChild(banner);
    requestAnimationFrame(() => banner.classList.add('is-in'));
    banner.querySelectorAll('[data-act]').forEach(b => {
      b.addEventListener('click', () => {
        const a = b.getAttribute('data-act');
        try { localStorage.setItem(COOKIE_KEY, JSON.stringify({ accepted: a, ts: Date.now() })); } catch (e) {}
        banner.classList.remove('is-in');
        setTimeout(() => banner.remove(), 500);
      });
    });
  }

  /* ——— LIGHTBOX immagini ——— */
  function initLightbox() {
    const targets = document.querySelectorAll('[data-lightbox], .img-marquee__item img, .gallery-img');
    if (!targets.length) return;
    let box = document.getElementById('lightbox');
    if (!box) {
      box = document.createElement('div');
      box.id = 'lightbox';
      box.className = 'lightbox';
      box.innerHTML = '<button class="lightbox__close" aria-label="Chiudi">×</button><img class="lightbox__img" alt="">';
      document.body.appendChild(box);
      box.querySelector('.lightbox__close').addEventListener('click', () => box.classList.remove('is-open'));
      box.addEventListener('click', (e) => { if (e.target === box) box.classList.remove('is-open'); });
      document.addEventListener('keydown', (e) => { if (e.key === 'Escape') box.classList.remove('is-open'); });
    }
    const img = box.querySelector('.lightbox__img');
    targets.forEach(t => {
      t.style.cursor = 'zoom-in';
      t.addEventListener('click', (e) => {
        const src = t.getAttribute('src') || t.getAttribute('data-lightbox');
        const alt = t.getAttribute('alt') || '';
        if (!src) return;
        img.src = src;
        img.alt = alt;
        box.classList.add('is-open');
      });
    });
  }

  /* ——— WHATSAPP SMART link ——— */
  function initWhatsAppSmart() {
    document.querySelectorAll('[data-wa-product]').forEach(link => {
      const name = link.getAttribute('data-wa-product') || 'prodotto';
      const msg = 'Ciao! Vorrei informazioni su: ' + name;
      const url = 'https://wa.me/39035719411?text=' + encodeURIComponent(msg);
      link.setAttribute('href', url);
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener');
    });
  }

  /* ——— STICKY FAB STACK (WhatsApp + Phone + Top) ——— */
  function initFabStack() {
    const stack = document.getElementById('fab-stack');
    if (!stack) return;
    const update = () => {
      stack.classList.toggle('is-visible', window.scrollY > 400);
    };
    window.addEventListener('scroll', update, { passive: true });
    update();
    const topBtn = document.getElementById('fab-top');
    if (topBtn) {
      topBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
      });
    }
  }

  /* ——— PAGE TRANSITION CURTAIN orizzontale ——— */
  function initPageCurtain() {
    if (reduced) return;
    // Crea overlay curtain
    const curtain = document.createElement('div');
    curtain.className = 'page-curtain';
    curtain.setAttribute('aria-hidden', 'true');
    const logo = document.createElement('img');
    logo.src = 'assets/brand/logo-bazzana.png';
    logo.alt = '';
    logo.className = 'page-curtain__logo';
    curtain.appendChild(logo);
    document.body.appendChild(curtain);

    // Entry animation on first load (gia' visualizzata dal loader, salto)

    // Click su link interno -> curtain leave -> navigazione -> reveal
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a');
      if (!a) return;
      const href = a.getAttribute('href');
      if (!href) return;
      if (href.startsWith('#')) return;
      if (a.target === '_blank') return;
      if (href.startsWith('http') && !href.includes(location.host)) return;
      if (href.startsWith('mailto:') || href.startsWith('tel:') || href.includes('wa.me')) return;
      e.preventDefault();
      curtain.classList.add('is-entering');
      setTimeout(() => { window.location.href = href; }, 750);
    });
  }

  /* ——— OBSERVERS section-entrance + headline-shift ——— */
  function initEntranceObservers() {
    if (reduced || !('IntersectionObserver' in window)) {
      document.querySelectorAll('.section-entrance, .headline-shift').forEach(el => el.classList.add('is-in'));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.15 });
    document.querySelectorAll('.section-entrance, .headline-shift').forEach(el => io.observe(el));
  }

  /* ——— INIT ——— */
  function init() {
    initFabStack();
    initEntranceObservers();
    initPageCurtain();
    updateWishlistBadge();
    injectWishlistButtons();
    initCatalogSearch();
    initCookieBanner();
    initLightbox();
    initWhatsAppSmart();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
