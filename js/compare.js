/* =========================================================
   CONFRONTA PRODOTTI — fino a 3 prodotti side-by-side
   ========================================================= */
(() => {
  'use strict';

  const MAX = 3;
  const KEY = 'mgb_compare_v1';

  let selected = [];
  try { selected = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { selected = []; }

  // Bar fluttuante
  let bar = null;
  let modal = null;

  function persist() {
    try { localStorage.setItem(KEY, JSON.stringify(selected)); } catch (e) {}
  }

  function getCardData(article) {
    return {
      id: article.getAttribute('data-product-id'),
      name: article.getAttribute('data-product-name'),
      brand: article.getAttribute('data-product-brand'),
      cat: article.getAttribute('data-product-cat'),
      img: article.getAttribute('data-product-img')
    };
  }

  function findArticleById(id) {
    return document.querySelector(`.depth-card[data-product-id="${id}"]`);
  }

  function buildBar() {
    if (bar) return bar;
    bar = document.createElement('div');
    bar.className = 'compare-bar';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'Barra confronto prodotti');
    bar.innerHTML = `
      <div class="compare-bar__inner">
        <span class="compare-bar__count"><span data-count>0</span> selezionati</span>
        <div class="compare-bar__thumbs" data-thumbs></div>
        <div class="compare-bar__actions">
          <button type="button" class="compare-bar__btn compare-bar__btn--ghost" data-clear>Svuota</button>
          <button type="button" class="compare-bar__btn compare-bar__btn--primary" data-open>Confronta →</button>
        </div>
      </div>`;
    document.body.appendChild(bar);
    bar.querySelector('[data-clear]').addEventListener('click', clearAll);
    bar.querySelector('[data-open]').addEventListener('click', openModal);
    return bar;
  }

  function buildModal() {
    if (modal) return modal;
    modal = document.createElement('div');
    modal.className = 'compare-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'Confronto prodotti');
    modal.innerHTML = `
      <div class="compare-modal__overlay" data-close></div>
      <div class="compare-modal__panel">
        <header class="compare-modal__head">
          <h2>Confronta prodotti</h2>
          <button type="button" class="compare-modal__close" data-close aria-label="Chiudi confronto">×</button>
        </header>
        <div class="compare-modal__grid" data-grid></div>
        <p class="compare-modal__hint">Per disponibilità, prezzo e prova diretta vieni in negozio o scrivici su <a href="https://wa.me/393464156981" target="_blank" rel="noopener">WhatsApp</a>.</p>
      </div>`;
    document.body.appendChild(modal);
    modal.querySelectorAll('[data-close]').forEach(el => el.addEventListener('click', closeModal));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('is-open')) closeModal();
    });
    return modal;
  }

  function refreshBar() {
    const b = buildBar();
    const count = b.querySelector('[data-count]');
    const thumbs = b.querySelector('[data-thumbs]');
    count.textContent = selected.length;
    thumbs.innerHTML = '';
    selected.forEach(id => {
      const article = findArticleById(id);
      if (!article) return;
      const data = getCardData(article);
      const thumb = document.createElement('button');
      thumb.type = 'button';
      thumb.className = 'compare-bar__thumb';
      thumb.title = `Rimuovi ${data.name}`;
      thumb.innerHTML = `<img src="${data.img}" alt=""><span aria-hidden="true">×</span>`;
      thumb.addEventListener('click', () => toggle(id));
      thumbs.appendChild(thumb);
    });
    b.classList.toggle('is-visible', selected.length > 0);
  }

  function refreshCheckboxes() {
    document.querySelectorAll('.depth-card input[data-compare]').forEach(input => {
      const article = input.closest('.depth-card');
      if (!article) return;
      const id = article.getAttribute('data-product-id');
      input.checked = selected.includes(id);
      article.classList.toggle('is-compare', input.checked);
    });
  }

  function toggle(id) {
    const idx = selected.indexOf(id);
    if (idx >= 0) {
      selected.splice(idx, 1);
    } else {
      if (selected.length >= MAX) {
        // Toast: limit
        if (typeof window.showToast === 'function') {
          window.showToast(`Massimo ${MAX} prodotti a confronto. Rimuovi prima un elemento.`, 'info');
        }
        return false;
      }
      selected.push(id);
    }
    persist();
    refreshCheckboxes();
    refreshBar();
    return true;
  }

  function clearAll() {
    selected = [];
    persist();
    refreshCheckboxes();
    refreshBar();
    closeModal();
  }

  function openModal() {
    if (selected.length === 0) return;
    const m = buildModal();
    const grid = m.querySelector('[data-grid]');
    grid.innerHTML = '';
    grid.style.setProperty('--compare-cols', selected.length);
    selected.forEach(id => {
      const article = findArticleById(id);
      if (!article) return;
      const data = getCardData(article);
      const col = document.createElement('article');
      col.className = 'compare-modal__col';
      const waText = encodeURIComponent(`Ciao! Vorrei info su ${data.brand} ${data.name}`);
      col.innerHTML = `
        <button type="button" class="compare-modal__remove" data-remove-id="${data.id}" aria-label="Rimuovi">×</button>
        <div class="compare-modal__col-media"><img src="${data.img}" alt="${data.name}"></div>
        <div class="compare-modal__col-body">
          <span class="compare-modal__brand">${data.brand}</span>
          <h3 class="compare-modal__name">${data.name}</h3>
          <p class="compare-modal__cat">${data.cat}</p>
          <dl class="compare-modal__specs">
            <dt>Brand</dt><dd>${data.brand}</dd>
            <dt>Modello</dt><dd>${data.name}</dd>
            <dt>Categoria</dt><dd>${data.cat}</dd>
            <dt>Disponibilità</dt><dd>In negozio · chiamaci</dd>
            <dt>Officina</dt><dd>Autorizzata Stihl + tutti i marchi</dd>
          </dl>
          <a class="compare-modal__cta" href="https://wa.me/393464156981?text=${waText}" target="_blank" rel="noopener">Chiedi su WhatsApp →</a>
        </div>`;
      grid.appendChild(col);
    });
    grid.querySelectorAll('[data-remove-id]').forEach(btn => {
      btn.addEventListener('click', () => {
        toggle(btn.getAttribute('data-remove-id'));
        if (selected.length === 0) { closeModal(); return; }
        openModal();
      });
    });
    requestAnimationFrame(() => m.classList.add('is-open'));
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  function init() {
    // Validate persisted selection
    selected = selected.filter(id => !!findArticleById(id));
    persist();

    document.querySelectorAll('.depth-card input[data-compare]').forEach(input => {
      input.addEventListener('change', (e) => {
        const article = input.closest('.depth-card');
        if (!article) return;
        const id = article.getAttribute('data-product-id');
        const accepted = toggle(id);
        if (!accepted) input.checked = false;
      });
      // Stop propagation così il click sul checkbox NON triggera nessun overlay
      input.addEventListener('click', (e) => e.stopPropagation());
    });
    // Prevent label click from also triggering anything
    document.querySelectorAll('.depth-card__compare').forEach(l => {
      l.addEventListener('click', (e) => e.stopPropagation());
    });

    refreshCheckboxes();
    refreshBar();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
