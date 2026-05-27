/* =========================================================
   BZN MAP — sostituisce l'iframe OSM con una mappa Leaflet
   interattiva. Self-init su [data-map].
   - Marker SVG arancio brand
   - Tile OpenStreetMap (zero API key)
   - Bottoni "Indicazioni" + "Apri in Maps"
   - Carica Leaflet da CDN solo se necessario, una volta sola.
   ========================================================= */
(() => {
  'use strict';

  const els = document.querySelectorAll('[data-map]');
  if (!els.length) return;

  const LEAFLET_CSS = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
  const LEAFLET_JS  = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';

  function loadCSS(href) {
    if (document.querySelector(`link[href="${href}"]`)) return Promise.resolve();
    return new Promise((resolve, reject) => {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = href;
      link.crossOrigin = 'anonymous';
      link.onload = resolve;
      link.onerror = reject;
      document.head.appendChild(link);
    });
  }

  function loadJS(src) {
    if (window.L) return Promise.resolve();
    if (document.querySelector(`script[src="${src}"]`)) {
      return new Promise(r => setTimeout(r, 200));
    }
    return new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = src;
      s.crossOrigin = 'anonymous';
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  function initOne(el) {
    const lat = parseFloat(el.dataset.lat);
    const lng = parseFloat(el.dataset.lng);
    if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;
    const label = el.dataset.label || 'Motor Garden Bazzana';
    const address = el.dataset.address || 'Via U. Bellora 73, 24020 Cene (BG)';

    // Costruisci la struttura: mappa + barra azioni
    el.classList.add('bzn-map');
    el.innerHTML = `
      <div class="bzn-map__canvas" aria-label="Mappa interattiva ${label}"></div>
      <div class="bzn-map__layer-toggle" role="group" aria-label="Vista mappa">
        <button type="button" class="bzn-map__layer-btn is-active" data-layer="map">Mappa</button>
        <button type="button" class="bzn-map__layer-btn" data-layer="sat">Satellite</button>
      </div>
      <div class="bzn-map__overlay" aria-hidden="true">
        <div class="bzn-map__card">
          <span class="bzn-map__card-eyebrow">Motor Garden Bazzana</span>
          <p class="bzn-map__card-addr">${address}</p>
          <div class="bzn-map__card-actions">
            <a class="bzn-map__btn bzn-map__btn--primary" href="https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}&destination_place_id=Motor+Garden+Bazzana" target="_blank" rel="noopener">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14" aria-hidden="true"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
              <span>Indicazioni</span>
            </a>
            <a class="bzn-map__btn" href="https://www.google.com/maps?q=${lat},${lng}" target="_blank" rel="noopener">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              <span>Apri in Maps</span>
            </a>
          </div>
        </div>
      </div>
    `;

    const canvas = el.querySelector('.bzn-map__canvas');
    const map = L.map(canvas, {
      center: [lat, lng],
      zoom: 16,
      scrollWheelZoom: false,
      attributionControl: true,
      zoomControl: true
    });

    /* Layer: mappa OSM e vista satellitare (ESRI World Imagery, gratuita). */
    const layerMap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
    });
    const layerSat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19,
      attribution: 'Tiles &copy; <a href="https://www.esri.com/" target="_blank" rel="noopener">Esri</a> · World Imagery'
    });
    const layerSatLabels = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19,
      pane: 'shadowPane'
    });
    layerMap.addTo(map);

    // Switch tra mappa e satellite
    const btns = el.querySelectorAll('.bzn-map__layer-btn');
    btns.forEach(b => b.addEventListener('click', () => {
      const which = b.dataset.layer;
      btns.forEach(x => x.classList.toggle('is-active', x === b));
      if (which === 'sat') {
        if (map.hasLayer(layerMap)) map.removeLayer(layerMap);
        if (!map.hasLayer(layerSat)) layerSat.addTo(map);
        if (!map.hasLayer(layerSatLabels)) layerSatLabels.addTo(map);
        el.classList.add('is-satellite');
      } else {
        if (map.hasLayer(layerSat)) map.removeLayer(layerSat);
        if (map.hasLayer(layerSatLabels)) map.removeLayer(layerSatLabels);
        if (!map.hasLayer(layerMap)) layerMap.addTo(map);
        el.classList.remove('is-satellite');
      }
    }));

    // Marker SVG custom (arancio brand)
    const pinSVG = `
      <svg viewBox="0 0 36 48" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <filter id="bzn-pin-shadow" x="-20%" y="0%" width="140%" height="120%">
            <feDropShadow dx="0" dy="3" stdDeviation="2.2" flood-color="#000" flood-opacity="0.35"/>
          </filter>
        </defs>
        <path filter="url(#bzn-pin-shadow)" d="M18 1.2C9.4 1.2 2.4 8.2 2.4 16.8c0 11.6 13.7 28.5 14.3 29.2.5.6 1.3.9 2.1.8.7-.1 1.4-.5 1.8-1.1.7-1 13.5-17 13.5-28.9 0-8.6-7-15.6-15.6-15.6z" fill="#ee5e1f"/>
        <circle cx="18" cy="17" r="6.5" fill="#0a0b0a"/>
        <circle cx="18" cy="17" r="3" fill="#ee5e1f"/>
      </svg>`;
    const icon = L.divIcon({
      className: 'bzn-map__pin',
      html: pinSVG,
      iconSize: [36, 48],
      iconAnchor: [18, 46],
      popupAnchor: [0, -42]
    });
    L.marker([lat, lng], { icon, title: label, riseOnHover: true })
      .addTo(map)
      .bindPopup(`<strong>${label}</strong><br><span style="color: rgba(0,0,0,0.65); font-size: 0.85em;">${address}</span>`, {
        offset: [0, -8],
        closeButton: false,
        autoClose: false
      });

    // Riallinea la mappa quando l'utente la mette in viewport (lazy init dei tile)
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach(en => {
          if (en.isIntersecting) {
            map.invalidateSize();
            io.disconnect();
          }
        });
      }, { threshold: 0.1 });
      io.observe(el);
    }

    // Riallinea su resize finestra
    let rt;
    window.addEventListener('resize', () => {
      clearTimeout(rt);
      rt = setTimeout(() => map.invalidateSize(), 200);
    }, { passive: true });
  }

  // Bootstrap: carica Leaflet, poi inizializza
  Promise.all([loadCSS(LEAFLET_CSS), loadJS(LEAFLET_JS)])
    .then(() => {
      // Aspetta che L sia disponibile (se loadJS è ritornato presto)
      const waitForL = (tries = 30) => {
        if (window.L) {
          els.forEach(initOne);
        } else if (tries > 0) {
          setTimeout(() => waitForL(tries - 1), 80);
        } else {
          console.warn('Leaflet non si è caricato — la mappa non sarà interattiva.');
        }
      };
      waitForL();
    })
    .catch(err => console.warn('Errore caricamento Leaflet:', err));
})();
