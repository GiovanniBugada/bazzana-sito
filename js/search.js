/* =========================================================
   SITE SEARCH — campo di ricerca SEMPRE visibile nella navbar
   con autocomplete fuzzy + suggerimenti casuali quando vuoto.
   ========================================================= */
(() => {
  'use strict';

  if (document.getElementById('nav-search')) return;

  /* ——— Indice ——— */
  const INDEX = window.BZN_SEARCH_INDEX || [];
  if (!INDEX.length) return;

  /* ——— Normalizzazione + Levenshtein ——— */
  function normalize(s) {
    return (s || '')
      .toString()
      .toLowerCase()
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, '')
      .replace(/[^a-z0-9\s.-]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function leven(a, b) {
    if (a === b) return 0;
    const la = a.length, lb = b.length;
    if (!la) return lb;
    if (!lb) return la;
    if (Math.abs(la - lb) > 3) return 99;
    let v0 = new Array(lb + 1);
    let v1 = new Array(lb + 1);
    for (let i = 0; i <= lb; i++) v0[i] = i;
    for (let i = 0; i < la; i++) {
      v1[0] = i + 1;
      for (let j = 0; j < lb; j++) {
        const cost = a.charCodeAt(i) === b.charCodeAt(j) ? 0 : 1;
        v1[j + 1] = Math.min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost);
      }
      [v0, v1] = [v1, v0];
    }
    return v0[lb];
  }

  /* ——— Pre-computa hay per ogni voce ——— */
  const ITEMS = INDEX.map(p => {
    const hay = normalize(`${p.brand} ${p.name} ${p.cat}`);
    const tokens = hay.split(/\s+/).filter(t => t.length > 1);
    return { ...p, _hay: hay, _tokens: tokens };
  });

  // Voci "in evidenza": prima i 15 con scheda dedicata, poi 1-2 per ogni brand
  const FEATURED_POOL = (() => {
    const withSlug = ITEMS.filter(x => x.slug);
    const byBrand = new Map();
    for (const x of ITEMS) {
      if (!byBrand.has(x.brand)) byBrand.set(x.brand, []);
      byBrand.get(x.brand).push(x);
    }
    const extras = [];
    for (const arr of byBrand.values()) {
      // Scegli 1-2 voci casuali per brand (skip quelli già con slug)
      const noSlug = arr.filter(x => !x.slug);
      shuffle(noSlug);
      extras.push(...noSlug.slice(0, 2));
    }
    return [...withSlug, ...extras];
  })();

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  /* ——— Scoring ——— */
  function scoreItem(item, qNorm, qTokens) {
    if (!qNorm) return 0;
    let score = 0;
    const pos = item._hay.indexOf(qNorm);
    if (pos !== -1) {
      score += 1000 - Math.min(pos, 200);
      if (pos === 0) score += 100;
    }
    let matched = 0;
    const typoTokens = [];
    for (const t of qTokens) {
      if (item._hay.includes(t)) { matched++; score += 80; }
      else typoTokens.push(t);
    }
    for (const tq of typoTokens) {
      if (tq.length < 3) continue;
      let best = 99;
      for (const ti of item._tokens) {
        if (Math.abs(ti.length - tq.length) > 3) continue;
        const d = leven(tq, ti);
        if (d < best) best = d;
        if (best === 0) break;
      }
      const threshold = tq.length <= 4 ? 1 : tq.length <= 7 ? 2 : 3;
      if (best <= threshold) {
        matched++;
        score += Math.max(0, 80 - best * 15);
      }
    }
    if (qTokens.length > 1 && matched < Math.ceil(qTokens.length / 2)) {
      score = Math.floor(score * 0.4);
    }
    return score;
  }

  function search(query, limit = 8) {
    const q = normalize(query);
    if (!q) return [];
    const qTokens = q.split(/\s+/).filter(t => t.length > 0);
    const scored = [];
    for (const it of ITEMS) {
      const s = scoreItem(it, q, qTokens);
      if (s > 0) scored.push({ item: it, s });
    }
    scored.sort((a, b) => b.s - a.s);
    return scored.slice(0, limit).map(x => x.item);
  }

  function bestSuggestion(query) {
    const q = normalize(query);
    if (!q || q.length < 4) return '';
    let bestScore = 99;
    let bestStr = '';
    for (const it of ITEMS) {
      for (const t of it._tokens) {
        if (Math.abs(t.length - q.length) > 3) continue;
        const d = leven(q, t);
        if (d < bestScore && d > 0 && d <= 3) {
          bestScore = d;
          bestStr = `${it.brand} ${it.name}`;
        }
      }
    }
    return bestScore <= 2 ? bestStr : '';
  }

  /* ——— URL helper ——— */
  function pathPrefix() {
    const p = location.pathname.replace(/\\/g, '/');
    return /\/prodotti\/[^/]+\.html?$/i.test(p) ? '../' : '';
  }
  function urlFor(item) {
    const pre = pathPrefix();
    if (item.slug) return `${pre}prodotti/${item.slug}.html`;
    // Scheda generica per i prodotti senza pagina dedicata
    return `${pre}prodotti/dettaglio.html?brand=${encodeURIComponent(item.brand)}&name=${encodeURIComponent(item.name)}`;
  }

  /* ——— DOM injection ——— */
  let wrap, input, dropdown, mobileTrigger;
  let currentResults = [];
  let activeIdx = -1;

  function injectSearchBar() {
    const headerInner = document.querySelector('.site-header__inner');
    const headerActions = document.querySelector('.header-actions');
    if (!headerInner || !headerActions) return;

    wrap = document.createElement('div');
    wrap.id = 'nav-search';
    wrap.className = 'nav-search';
    wrap.innerHTML = `
      <div class="nav-search__box" role="search">
        <svg class="nav-search__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="11" cy="11" r="7.5"/>
          <line x1="20.5" y1="20.5" x2="16.65" y2="16.65"/>
        </svg>
        <input type="text" class="nav-search__input" placeholder="Cerca prodotto…" autocomplete="off" aria-label="Cerca prodotto" aria-controls="nav-search-results" aria-expanded="false" />
        <button type="button" class="nav-search__clear" aria-label="Pulisci" hidden>×</button>
      </div>
      <div class="nav-search__dropdown" id="nav-search-results" role="listbox" hidden></div>
    `;
    // Inserisci PRIMA della header-actions, accanto alla nav
    headerInner.insertBefore(wrap, headerActions);

    input = wrap.querySelector('.nav-search__input');
    dropdown = wrap.querySelector('.nav-search__dropdown');
    const clearBtn = wrap.querySelector('.nav-search__clear');

    input.addEventListener('focus', onFocus);
    input.addEventListener('input', onInput);
    input.addEventListener('keydown', onKeydown);
    clearBtn.addEventListener('click', () => {
      input.value = '';
      clearBtn.hidden = true;
      renderRandom();
      input.focus();
    });

    // Click fuori → chiudi
    document.addEventListener('click', (e) => {
      if (!wrap.contains(e.target)) closeDropdown();
    });

    // ESC → chiudi e leva focus
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && isOpen()) {
        closeDropdown();
        input.blur();
      }
      const focusedInForm = document.activeElement && /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName);
      if (!focusedInForm && (e.key === '/' || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k'))) {
        e.preventDefault();
        input.focus();
      }
    });

    // Mobile trigger: l'input principale è nascosto < 900px → mostra una lente
    // dentro la header-actions che apre l'input come overlay full-screen.
    mobileTrigger = document.createElement('button');
    mobileTrigger.type = 'button';
    mobileTrigger.id = 'nav-search-mobile';
    mobileTrigger.className = 'nav-search__mobile-trigger';
    mobileTrigger.setAttribute('aria-label', 'Cerca prodotto');
    mobileTrigger.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <circle cx="11" cy="11" r="7.5"/>
        <line x1="20.5" y1="20.5" x2="16.65" y2="16.65"/>
      </svg>
    `;
    headerActions.insertBefore(mobileTrigger, headerActions.firstChild);
    mobileTrigger.addEventListener('click', () => {
      wrap.classList.add('is-mobile-open');
      setTimeout(() => input.focus(), 80);
    });

    // Inietta il bottone chiusura "mobile" anche dentro il box
    const mClose = document.createElement('button');
    mClose.type = 'button';
    mClose.className = 'nav-search__mobile-close';
    mClose.setAttribute('aria-label', 'Chiudi ricerca');
    mClose.textContent = '×';
    wrap.querySelector('.nav-search__box').appendChild(mClose);
    mClose.addEventListener('click', () => {
      wrap.classList.remove('is-mobile-open');
      closeDropdown();
    });
  }

  function isOpen() { return dropdown && !dropdown.hidden; }
  function openDropdown() {
    dropdown.hidden = false;
    input.setAttribute('aria-expanded', 'true');
  }
  function closeDropdown() {
    if (!dropdown) return;
    dropdown.hidden = true;
    input.setAttribute('aria-expanded', 'false');
    activeIdx = -1;
  }

  /* ——— Event handlers ——— */
  function onFocus() {
    const clearBtn = wrap.querySelector('.nav-search__clear');
    if (input.value.trim()) {
      clearBtn.hidden = false;
      doSearch();
    } else {
      clearBtn.hidden = true;
      renderRandom();
    }
  }

  function onInput() {
    const v = input.value.trim();
    const clearBtn = wrap.querySelector('.nav-search__clear');
    clearBtn.hidden = !v;
    if (!v) {
      renderRandom();
    } else {
      doSearch();
    }
  }

  function onKeydown(e) {
    if (!isOpen()) {
      if (e.key === 'ArrowDown') onFocus();
      return;
    }
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActive(activeIdx + 1);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActive(activeIdx - 1);
    } else if (e.key === 'Enter') {
      if (activeIdx >= 0 && currentResults[activeIdx]) {
        e.preventDefault();
        location.href = urlFor(currentResults[activeIdx]);
      }
    }
  }

  function setActive(i) {
    activeIdx = Math.max(-1, Math.min(currentResults.length - 1, i));
    dropdown.querySelectorAll('.nav-search__item').forEach(el => {
      const isActive = +el.dataset.idx === activeIdx;
      el.classList.toggle('is-active', isActive);
      if (isActive) el.scrollIntoView({ block: 'nearest' });
    });
  }

  /* ——— Rendering ——— */
  function doSearch() {
    const q = input.value;
    const results = search(q, 8);
    renderResults(results, q);
  }

  function renderRandom() {
    // Mescola e prendi 6 voci "in evidenza" (15 con scheda + alcuni random)
    const pool = FEATURED_POOL.slice();
    shuffle(pool);
    const picked = pool.slice(0, 6);
    currentResults = picked;
    activeIdx = -1;

    dropdown.innerHTML = `
      <div class="nav-search__hint">
        <span>Suggerimenti</span>
        <span class="nav-search__hint-meta">
          <kbd>↑</kbd><kbd>↓</kbd> naviga · <kbd>Enter</kbd> apri · <kbd>Esc</kbd> chiudi
        </span>
      </div>
      ${renderList(picked, '')}
      <div class="nav-search__footer">
        <span>Cerca tra <strong>${ITEMS.length}</strong> prodotti — Stihl, Honda, Active, Echo, Oleo-Mac, Kress, Shindaiwa, Ligier, Yashi.</span>
      </div>
    `;
    bindItemEvents();
    openDropdown();
  }

  function renderResults(results, query) {
    currentResults = results;
    activeIdx = results.length ? 0 : -1;

    if (!results.length) {
      const hint = bestSuggestion(query);
      const suggestHTML = hint
        ? ` Forse intendevi <span class="nav-search__suggest" data-suggest="${escapeHtml(hint)}">${escapeHtml(hint)}</span>?`
        : ' Prova con <em>stihl</em>, <em>honda</em>, <em>rasaerba</em>, <em>decespugliatore</em>.';
      dropdown.innerHTML = `
        <div class="nav-search__empty">
          <strong>Nessun risultato per "${escapeHtml(query)}"</strong>
          <span>${suggestHTML}</span>
        </div>
      `;
      const sug = dropdown.querySelector('.nav-search__suggest');
      if (sug) {
        sug.addEventListener('click', () => {
          input.value = sug.dataset.suggest;
          doSearch();
        });
      }
      openDropdown();
      return;
    }

    dropdown.innerHTML = `
      <div class="nav-search__hint">
        <span>${results.length} risultat${results.length === 1 ? 'o' : 'i'}</span>
        <span class="nav-search__hint-meta">
          <kbd>↑</kbd><kbd>↓</kbd> · <kbd>Enter</kbd>
        </span>
      </div>
      ${renderList(results, query)}
    `;
    bindItemEvents();
    openDropdown();
    setActive(0);
  }

  function renderList(items, query) {
    const pre = pathPrefix();
    const q = normalize(query);
    const qTokens = q.split(/\s+/).filter(t => t.length > 0);
    return `
      <ul class="nav-search__results">
        ${items.map((it, i) => {
          const imgSrc = it.img ? (pre + it.img) : '';
          const isFeatured = !!it.slug;
          return `
            <li>
              <a class="nav-search__item" href="${urlFor(it)}" data-idx="${i}" role="option">
                ${imgSrc ? `<img class="nav-search__thumb" src="${escapeHtml(imgSrc)}" alt="" loading="lazy" onerror="this.style.opacity=0">` : '<span class="nav-search__thumb"></span>'}
                <div class="nav-search__meta">
                  <span class="nav-search__brand">${highlight(it.brand, qTokens)}${isFeatured ? '<span class="nav-search__badge">scheda</span>' : ''}</span>
                  <p class="nav-search__name">${highlight(it.name, qTokens)}</p>
                  <p class="nav-search__cat">${highlight(it.cat, qTokens)}</p>
                </div>
                <span class="nav-search__arrow" aria-hidden="true">→</span>
              </a>
            </li>
          `;
        }).join('')}
      </ul>
    `;
  }

  function bindItemEvents() {
    dropdown.querySelectorAll('.nav-search__item').forEach(a => {
      a.addEventListener('mouseenter', () => {
        const idx = +a.dataset.idx;
        if (!Number.isNaN(idx)) setActive(idx);
      });
    });
  }

  function highlight(text, qTokens) {
    if (!qTokens || !qTokens.length) return escapeHtml(text);
    const norm = normalize(text);
    const ranges = [];
    for (const t of qTokens) {
      if (t.length < 2) continue;
      let i = 0;
      while ((i = norm.indexOf(t, i)) !== -1) {
        ranges.push([i, i + t.length]);
        i += t.length;
      }
    }
    if (!ranges.length) return escapeHtml(text);
    ranges.sort((a, b) => a[0] - b[0]);
    const merged = [ranges[0]];
    for (let k = 1; k < ranges.length; k++) {
      const last = merged[merged.length - 1];
      if (ranges[k][0] <= last[1]) last[1] = Math.max(last[1], ranges[k][1]);
      else merged.push(ranges[k]);
    }
    let out = '';
    let last = 0;
    for (const [s, e] of merged) {
      out += escapeHtml(text.slice(last, s));
      out += '<mark class="search-hit">' + escapeHtml(text.slice(s, e)) + '</mark>';
      last = e;
    }
    out += escapeHtml(text.slice(last));
    return out;
  }

  function escapeHtml(s) {
    return (s || '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  /* ——— Bootstrap ——— */
  function init() {
    injectSearchBar();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
