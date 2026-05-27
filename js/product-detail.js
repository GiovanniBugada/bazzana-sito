/* =========================================================
   PRODUCT DETAIL — pagina dettaglio generica (dettaglio.html?id=...)
   Funziona per i ~620 prodotti senza scheda dedicata.
   Se l'URL ha ?slug e quello slug ha una scheda dedicata, redirect.
   ========================================================= */
(() => {
  'use strict';

  const host = document.querySelector('[data-detail-host]');
  if (!host) return;

  const INDEX = window.BZN_SEARCH_INDEX || [];
  const DB = window.BAZZANA_PRODUCTS || [];

  /* ——— Params ——— */
  const params = new URLSearchParams(location.search);
  const idParam = params.get('id');
  const slugParam = params.get('slug');
  const brandParam = (params.get('brand') || '').toLowerCase();
  const nameParam = (params.get('name') || '').toLowerCase();

  /* ——— Risoluzione del prodotto ———
     Strategia "never fail": se l'URL ha brand+name, generiamo SEMPRE
     una scheda anche se il prodotto non è nell'indice. La descrizione
     è prodotta da generateDesc() e l'immagine cade sul placeholder. */
  function findItem() {
    // 1) Slug → redirect alla scheda dedicata se esiste fisicamente
    if (slugParam) {
      const dbHit = DB.find(p => p.slug === slugParam);
      if (dbHit) {
        location.replace(slugParam + '.html');
        return null;
      }
    }
    // 2) brand+name → match nell'indice (case-insensitive)
    if (brandParam && nameParam) {
      const hit = INDEX.find(p =>
        p.brand.toLowerCase() === brandParam &&
        p.name.toLowerCase() === nameParam
      );
      if (hit) return hit;
      // Fallback: nessun match → costruisci un item minimale.
      // L'URL ci ha dato brand+name: rispetta questi e usa il placeholder.
      const origBrand = (new URLSearchParams(location.search).get('brand') || '').trim();
      const origName  = (new URLSearchParams(location.search).get('name')  || '').trim();
      return {
        brand: origBrand,
        name:  origName,
        cat:   '',
        img:   'assets/img/placeholder-foto-arrivo.svg',
        slug:  '',
        _synthetic: true
      };
    }
    // 3) Solo ID → fetchById sotto
    if (idParam) return null;
    return null;
  }

  async function fetchById(id) {
    // Recupera prodotti.html (cached dal browser), estrae la card con data-product-id=id
    try {
      const res = await fetch('../prodotti.html', { cache: 'force-cache' });
      const html = await res.text();
      const re = new RegExp(`<article[^>]*data-product-id="${id}"[^>]*>`, 'i');
      const m = html.match(re);
      if (!m) return null;
      const tag = m[0];
      const get = (attr) => {
        const r = new RegExp(`${attr}="([^"]*)"`).exec(tag);
        return r ? r[1] : '';
      };
      return {
        brand: get('data-product-brand'),
        name: get('data-product-name'),
        cat: get('data-product-cat').replace(/ - /g, ' · '),
        img: get('data-product-img'),
        slug: ''
      };
    } catch (e) {
      console.warn('Impossibile recuperare prodotti.html', e);
      return null;
    }
  }

  /* ——— Descrizione: stesso algoritmo di catalog-pro.js, copiato qui per non dipendere ——— */
  const BRAND_NOTES = {
    stihl: 'Standard Stihl, ricambi originali ordinabili in 48h.',
    honda: 'Motore Honda, partenza affidabile anche dopo l’inverno fermo.',
    active: 'Progettato e assemblato in Italia, ricambi sempre reperibili.',
    echo: 'Echo X-Series, garanzia estesa per uso privato e professionale.',
    'oleo-mac': 'Gamma Oleo-Mac, assistenza in officina autorizzata.',
    'oleomac': 'Gamma Oleo-Mac, assistenza in officina autorizzata.',
    kress: 'Piattaforma 60V Kress: batterie e caricabatterie intercambiabili sull’intera gamma.',
    ligier: 'Microcar Ligier omologata L6e, guidabile dai 14 anni con patente AM.',
    shindaiwa: 'Shindaiwa: ricambi e accessori originali in showroom.',
    geotech: 'Geotech, motore robusto e prezzo onesto.',
    valex: 'Linea Valex, soluzione hobby con prezzo accessibile.',
    sondaven: 'Sondaven, attrezzatura specifica per il verde.',
    husqvarna: 'Husqvarna, soluzioni professionali per agricoltori e manutentori.'
  };
  function brandTail(brand) {
    const k = (brand || '').toLowerCase().trim();
    return BRAND_NOTES[k] || 'In showroom a Cene (BG) — manutenzione e ricambi in officina autorizzata.';
  }

  function parseModelHints(model, category, brand) {
    const m = (model || '').toUpperCase();
    const cat = (category || '').toLowerCase();
    const b = (brand || '').toLowerCase();
    const hints = {};
    const nums = (m.match(/\d+(?:[.,]\d+)?/g) || []).map(n => parseFloat(n.replace(',', '.')));
    if (b === 'active' && /^\d+[.\d]+$/.test(m.replace(/\s/g, ''))) hints.cc = Math.round(nums[0]);
    else if (b === 'oleo-mac' || b === 'oleomac') {
      const cm = m.match(/^[A-Z]+\s*(\d{2,4})/);
      if (cm && cat.includes('motoseg')) {
        const n = parseInt(cm[1], 10);
        if (n >= 200 && n <= 999) hints.cc = Math.round(n / 10);
        else if (n >= 30 && n <= 99) hints.cc = n;
      }
    } else if (b === 'shindaiwa') {
      const cm = m.match(/^(\d{3,4})/);
      if (cm && cat.includes('motoseg')) {
        const n = parseInt(cm[1], 10);
        if (n >= 1000 && n <= 9999) hints.cc = Math.floor(n / 100);
        else if (n >= 200 && n <= 999) hints.cc = Math.floor(n / 10);
      }
      const bm = m.match(/(\d{2})$/);
      if (bm) {
        const n = parseInt(bm[1], 10);
        if (n >= 25 && n <= 70) hints.barCm = n;
      }
    }
    if (cat.includes('tosaerb') || cat.includes('rasaerb')) {
      const nm = m.match(/^(\d{2,4})/);
      if (nm) {
        const n = parseInt(nm[1], 10);
        if (n >= 4000 && n <= 6999) hints.cutCm = Math.floor(n / 100);
        else if (n >= 36 && n <= 70) hints.cutCm = n;
      }
    }
    const vm = m.match(/(\d{2})\s*V/i);
    if (vm) {
      const v = parseInt(vm[1], 10);
      if (v >= 18 && v <= 80) hints.voltage = v;
    }
    return hints;
  }

  function generateDesc(brand, model, category) {
    const cat = (category || '').toLowerCase();
    const sub = (cat.split(/\s*[-·]\s*/)[1] || '');
    const m = model || 'questo modello';
    const hints = parseModelHints(model, category, brand);
    let dataNote = '';
    if (hints.cc) dataNote += ` Cilindrata indicativa ${hints.cc} cc.`;
    if (hints.cutCm) dataNote += ` Larghezza di taglio circa ${hints.cutCm} cm.`;
    if (hints.barCm) dataNote += ` Lunghezza spranga ${hints.barCm} cm.`;
    if (hints.voltage) dataNote += ` Piattaforma batteria ${hints.voltage} V.`;
    let core = '';
    if (cat.includes('motoseg')) {
      if (sub.includes('abbat'))     core = `${brand} ${m}: motosega da abbattimento per lavori forestali, spranga lunga e potenza per tronchi importanti.`;
      else if (sub.includes('potatura')) core = `${brand} ${m}: motosega da potatura leggera, ideale in tree-climbing e per rami sopra testa.`;
      else if (sub.includes('professional')) core = `${brand} ${m}: motosega professionale per uso intensivo quotidiano, manutenzione semplificata.`;
      else core = `${brand} ${m}: motosega della gamma, affilatura catena disponibile in officina.`;
    } else if (cat.includes('tosaerb') || cat.startsWith('rasaerba')) {
      if (sub.includes('mulching')) core = `${brand} ${m}: rasaerba con sistema mulching che restituisce l’erba al prato come concime naturale.`;
      else if (sub.includes('alluminio')) core = `${brand} ${m}: rasaerba con scocca in alluminio, leggero e resistente alla corrosione.`;
      else if (sub.includes('acciaio') || sub.includes('accaio')) core = `${brand} ${m}: rasaerba con scocca in acciaio verniciato, robusto per terreni irregolari.`;
      else core = `${brand} ${m}: rasaerba a spinta o semovente per giardini di varie dimensioni.`;
    } else if (cat.includes('robot')) {
      core = `${brand} ${m}: robot rasaerba con installazione cavo perimetrale a cura del nostro tecnico, manutenzione lame in officina.`;
    } else if (cat.includes('trattorin') || cat.includes('rider')) {
      core = `${brand} ${m}: trattorino rasaerba per giardini di grandi dimensioni, raccolta o scarico posteriore.`;
    } else if (cat.includes('decespu')) {
      if (sub.includes('zaino')) core = `${brand} ${m}: decespugliatore a zaino, peso scaricato sulla schiena per giornate intere senza fatica.`;
      else if (sub.includes('asta fissa') || sub.includes('asta-fissa')) core = `${brand} ${m}: decespugliatore ad asta fissa, robusto, manubrio bike-handle e cinghia ergonomica.`;
      else if (sub.includes('attrezzi') || sub.includes('multifunzione')) core = `${brand} ${m}: accessorio della linea multifunzione, intercambiabile su un’unica unità motore.`;
      else if (sub.includes('evolution')) core = `${brand} ${m}: powerhead della linea Multifunzione Evolution, attrezzi intercambiabili.`;
      else core = `${brand} ${m}: decespugliatore per erba alta, sterpaglia e prati irregolari.`;
    } else if (cat.includes('tagliasi')) {
      core = `${brand} ${m}: tagliasiepi a doppia lama per taglio netto su siepi formali e arbusti densi.`;
    } else if (cat.includes('soffia') || cat.includes('aspirator')) {
      core = `${brand} ${m}: soffiatore per pulizia di viali, cortili e residui leggeri. Versioni a benzina o batteria.`;
    } else if (cat.includes('genera')) {
      if (sub.includes('inverter')) core = `${brand} ${m}: generatore inverter sinusoidale, sicuro per laptop e dispositivi elettronici sensibili.`;
      else if (sub.includes('avr')) core = `${brand} ${m}: generatore con regolazione AVR, ideale per cantieri e attrezzature elettriche.`;
      else core = `${brand} ${m}: generatore portatile per cantiere, emergenza o eventi outdoor.`;
    } else if (cat.includes('motozap') || cat.includes('motoco')) {
      core = `${brand} ${m}: motozappa con frese in acciaio temprato per lavorazione orto e piccoli appezzamenti.`;
    } else if (cat.includes('trincia')) {
      if (sub.includes('hd')) core = `${brand} ${m}: trinciasarmenti serie HD per uso semi-intensivo su erba alta e ramaglia leggera.`;
      else if (sub.includes('pro')) core = `${brand} ${m}: trinciasarmenti serie PRO per uso professionale e terreni difficili.`;
      else core = `${brand} ${m}: trinciasarmenti per manutenzione di terreni incolti e bordure.`;
    } else if (cat.includes('arieggi')) {
      core = `${brand} ${m}: arieggiatore per arieggiare il prato a primavera e in autunno, prato più sano in poche ore.`;
    } else if (cat.includes('levazoll')) {
      core = `${brand} ${m}: levazolle per rimuovere il manto erboso e preparare il terreno alla risemina.`;
    } else if (cat.includes('scuotit') || cat.includes('abbacch')) {
      if (sub.includes('batter')) core = `${brand} ${m}: abbacchiatore a batteria per la raccolta olive, leggero e silenzioso.`;
      else core = `${brand} ${m}: scuotitore a motore per raccolta intensiva di olive e frutta secca.`;
    } else if (cat.includes('trivell')) {
      core = `${brand} ${m}: trivella per scavare buche di piantagione, recinzioni o pali per la vigna.`;
    } else if (cat.includes('potator')) {
      core = `${brand} ${m}: potatore ad asta per tagliare rami in altezza senza scala, lunghezza estendibile.`;
    } else if (cat.includes('spazzan')) {
      core = `${brand} ${m}: spazzaneve per liberare viali e accessi dopo le nevicate, getto orientabile.`;
    } else if (cat.includes('powertrack') || cat.includes('carriol') || cat.includes('transport')) {
      core = `${brand} ${m}: mini-transporter cingolato per spostare carichi su terreni difficili, vigneto, frutteto o cantiere.`;
    } else if (cat.includes('cippa') || cat.includes('biotri')) {
      core = `${brand} ${m}: biotrituratore per ridurre rami e potature in cippato pronto per la pacciamatura.`;
    } else if (cat.includes('micro') || cat.includes('quadric')) {
      core = `${brand} ${m}: microcar omologata L6e, guidabile dai 14 anni con patente AM, ricarica da presa di casa.`;
    } else if (cat.includes('access') || cat.includes('ricam')) {
      if (cat.includes('decespu')) core = `${brand} ${m}: accessorio originale per decespugliatori della gamma.`;
      else if (cat.includes('motoseg')) core = `${brand} ${m}: accessorio o ricambio originale per motoseghe.`;
      else if (cat.includes('batter')) core = `${brand} ${m}: batteria o caricabatterie compatibile con la piattaforma del marchio.`;
      else core = `${brand} ${m}: accessorio o ricambio originale, disponibile in negozio o in 48h.`;
    } else if (cat.includes('olio') || cat.includes('lubrif') || cat.includes('tanich') || cat.includes('miscel')) {
      core = `${brand} ${m}: olio o carburante consigliato dal costruttore, prolunga la vita del motore e mantiene la garanzia.`;
    } else if (cat.includes('abbiglia') || cat.includes('dpi') || cat.includes('protet')) {
      core = `${brand} ${m}: dispositivi di protezione individuale certificati per uso forestale e con utensili motorizzati.`;
    } else {
      core = `${brand} ${m}: attrezzatura per la cura del verde, disponibile in showroom a Cene (BG).`;
    }
    return core + dataNote + ' ' + brandTail(brand);
  }

  /* ——— "Trovati simili": 4 prodotti dello stesso brand, escluso quello aperto ——— */
  function findSimilar(item, limit = 4) {
    const others = INDEX.filter(p =>
      p.brand === item.brand && (p.name + p.cat) !== (item.name + item.cat)
    );
    // Mescola e prendi i primi N
    for (let i = others.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [others[i], others[j]] = [others[j], others[i]];
    }
    return others.slice(0, limit);
  }

  function escapeHtml(s) {
    return (s || '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  /* ——— Generatore SPECIFICHE per categoria + parsing modello ———
     Restituisce un array {label, value} con specifiche sensate per
     ogni categoria del catalogo. Quando il dato non si puo' parsare
     dal modello, mostra "su richiesta" / "vedi configuratore". */
  function generateSpecs(brand, model, category) {
    const cat = (category || '').toLowerCase();
    const hints = parseModelHints(model, category, brand);
    const specs = [];
    const cc = hints.cc ? hints.cc + ' cc' : 'su richiesta';
    const cut = hints.cutCm ? hints.cutCm + ' cm' : 'su richiesta';
    const bar = hints.barCm ? hints.barCm + ' cm' : 'su richiesta';
    const volt = hints.voltage ? hints.voltage + ' V' : null;
    const isBatt = /batter|elettr|cordless|\bv\b/i.test(model + ' ' + category) || !!volt;

    if (cat.includes('motoseg') || cat.includes('motosega')) {
      if (isBatt && volt) {
        specs.push({ label: 'Alimentazione', value: 'Batteria ' + volt });
      } else {
        specs.push({ label: 'Cilindrata', value: cc });
      }
      specs.push({ label: 'Spranga', value: bar });
      specs.push({ label: 'Catena', value: 'originale ' + brand });
      specs.push({ label: 'Freno catena', value: 'inerziale' });
      specs.push({ label: 'Affilatura', value: 'in officina' });
      specs.push({ label: 'Garanzia', value: '2 anni privati' });
    } else if (cat.includes('tosaerb') || cat.includes('rasaerb')) {
      specs.push({ label: 'Alimentazione', value: isBatt ? ('Batteria ' + (volt || '')) : 'Benzina' });
      specs.push({ label: 'Larghezza taglio', value: cut });
      specs.push({ label: 'Mulching', value: cat.includes('mulching') ? 'Sì, integrato' : 'Compatibile (kit)' });
      specs.push({ label: 'Trazione', value: /sa$|sva$|sh$|sv$|semove|trazion/i.test(model + cat) ? 'A spinta semovente' : 'A spinta' });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    } else if (cat.includes('robot')) {
      specs.push({ label: 'Area max', value: 'su richiesta (varia per modello)' });
      specs.push({ label: 'Pendenza max', value: 'fino a 45%' });
      specs.push({ label: 'Connettività', value: 'App + Bluetooth + GPS' });
      specs.push({ label: 'Installazione', value: 'da noi inclusa' });
      specs.push({ label: 'Tagliando primo anno', value: 'incluso' });
      specs.push({ label: 'Garanzia', value: '2 anni + estensione su richiesta' });
    } else if (cat.includes('trattorin') || cat.includes('rider')) {
      specs.push({ label: 'Motore', value: brand === 'Honda' ? 'Honda GCV/GXV' : 'a benzina 4 tempi' });
      specs.push({ label: 'Larghezza taglio', value: cut });
      specs.push({ label: 'Raccolta', value: 'cesto posteriore o scarico laterale' });
      specs.push({ label: 'Trasmissione', value: 'idrostatica (a leva)' });
      specs.push({ label: 'Consegna a domicilio', value: 'su appuntamento' });
      specs.push({ label: 'Garanzia', value: '2 anni privati' });
    } else if (cat.includes('decespu')) {
      if (isBatt && volt) {
        specs.push({ label: 'Alimentazione', value: 'Batteria ' + volt });
      } else {
        specs.push({ label: 'Cilindrata', value: cc });
      }
      const sub = cat.split(/\s*[-·]\s*/)[1] || '';
      specs.push({ label: 'Configurazione', value: sub.includes('zaino') ? 'A zaino' : (sub.includes('asta') ? 'Ad asta fissa' : 'Bike-handle') });
      specs.push({ label: 'Cinghia', value: 'ergonomica inclusa' });
      specs.push({ label: 'Accessori', value: 'testina filo + lama 3 denti' });
      specs.push({ label: 'Avviamento', value: 'easy-start' });
      specs.push({ label: 'Garanzia', value: '2 anni privati' });
    } else if (cat.includes('tagliasi')) {
      specs.push({ label: 'Alimentazione', value: isBatt ? ('Batteria ' + (volt || '')) : 'Benzina 2 tempi' });
      specs.push({ label: 'Lama', value: 'doppia, antiurto' });
      specs.push({ label: 'Lunghezza taglio', value: 'su richiesta (varia per modello)' });
      specs.push({ label: 'Bilanciamento', value: 'baricentrato' });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    } else if (cat.includes('soffia') || cat.includes('aspirator')) {
      if (isBatt && volt) {
        specs.push({ label: 'Alimentazione', value: 'Batteria ' + volt });
      } else {
        specs.push({ label: 'Cilindrata', value: cc });
      }
      specs.push({ label: 'Velocità aria', value: 'su richiesta' });
      specs.push({ label: 'Volume aria', value: 'su richiesta' });
      const sub = cat.split(/\s*[-·]\s*/)[1] || '';
      specs.push({ label: 'Configurazione', value: sub.includes('zaino') ? 'A zaino' : 'Portatile' });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    } else if (cat.includes('genera')) {
      specs.push({ label: 'Tipo', value: cat.includes('inverter') ? 'Inverter sinusoidale' : (cat.includes('avr') ? 'Con regolazione AVR' : 'Portatile') });
      specs.push({ label: 'Potenza', value: hints.kw ? hints.kw + ' kW' : (hints.watt ? hints.watt + ' W' : 'vedi modello') });
      specs.push({ label: 'Avviamento', value: 'manuale o elettrico (su modello)' });
      specs.push({ label: 'Autonomia', value: 'da 6 a 14 h (varia per carico)' });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    } else if (cat.includes('motozap') || cat.includes('motoco')) {
      specs.push({ label: 'Motore', value: '4 tempi a benzina' });
      specs.push({ label: 'Larghezza lavoro', value: 'su richiesta' });
      specs.push({ label: 'Frese', value: 'acciaio temprato' });
      specs.push({ label: 'Profondità lavoro', value: 'regolabile' });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    } else if (cat.includes('trincia')) {
      specs.push({ label: 'Motore', value: '4 tempi a benzina' });
      specs.push({ label: 'Larghezza taglio', value: 'su richiesta' });
      specs.push({ label: 'Tipo lame', value: 'a Y forgiate / a martello (su modello)' });
      specs.push({ label: 'Trazione', value: 'semovente a leva' });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    } else if (cat.includes('arieggi')) {
      specs.push({ label: 'Tipo', value: 'A lame fisse' });
      specs.push({ label: 'Larghezza lavoro', value: 'su richiesta' });
      specs.push({ label: 'Regolazione altezza', value: 'a manopola' });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    } else if (cat.includes('scuotit') || cat.includes('abbacch')) {
      specs.push({ label: 'Alimentazione', value: isBatt ? ('Batteria ' + (volt || '')) : 'Benzina o asta' });
      specs.push({ label: 'Frequenza vibrazione', value: 'regolabile' });
      specs.push({ label: 'Lunghezza asta', value: 'fissa o telescopica' });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    } else if (cat.includes('potator')) {
      specs.push({ label: 'Alimentazione', value: isBatt ? ('Batteria ' + (volt || '')) : 'Benzina 2 tempi' });
      specs.push({ label: 'Spranga', value: bar });
      specs.push({ label: 'Lunghezza asta', value: 'telescopica / fissa' });
      specs.push({ label: 'Catena', value: 'originale ' + brand });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    } else if (cat.includes('cippa') || cat.includes('biotri')) {
      specs.push({ label: 'Motore', value: '4 tempi a benzina' });
      specs.push({ label: 'Diametro max ramo', value: 'su richiesta' });
      specs.push({ label: 'Tipo trituratura', value: 'a coltelli o a martelli' });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    } else if (cat.includes('micro') || cat.includes('quadric')) {
      specs.push({ label: 'Omologazione', value: 'L6e' });
      specs.push({ label: 'Velocità max', value: '45 km/h' });
      specs.push({ label: 'Posti', value: '2' });
      specs.push({ label: 'Età minima', value: '14 anni (patente AM)' });
      specs.push({ label: 'Ricarica', value: 'da presa domestica' });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    } else if (cat.includes('idropulit')) {
      specs.push({ label: 'Pressione max', value: 'su richiesta' });
      specs.push({ label: 'Portata acqua', value: 'su richiesta' });
      specs.push({ label: 'Tipo motore', value: 'elettrico' });
      specs.push({ label: 'Accessori', value: 'pistola, lancia, ugelli' });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    } else if (cat.includes('access') || cat.includes('ricam')) {
      specs.push({ label: 'Tipo', value: 'Accessorio o ricambio originale ' + brand });
      specs.push({ label: 'Compatibilità', value: 'con la gamma del marchio' });
      specs.push({ label: 'Disponibilità', value: 'in negozio o in 48 h' });
      specs.push({ label: 'Montaggio', value: 'in officina su richiesta' });
    } else if (cat.includes('olio') || cat.includes('miscel') || cat.includes('lubrif') || cat.includes('tanich')) {
      specs.push({ label: 'Tipo prodotto', value: 'Olio / carburante ' + brand });
      specs.push({ label: 'Uso', value: 'consigliato per ' + brand + ' originali' });
      specs.push({ label: 'Confezione', value: 'multipla (varia per articolo)' });
      specs.push({ label: 'Garanzia motore', value: 'mantenuta con originale' });
    } else if (cat.includes('abbiglia') || cat.includes('dpi') || cat.includes('protet')) {
      specs.push({ label: 'Categoria', value: 'DPI uso forestale' });
      specs.push({ label: 'Certificazione', value: 'EN ISO' });
      specs.push({ label: 'Taglie', value: 'in showroom a Cene' });
    } else {
      specs.push({ label: 'Categoria', value: category || 'Attrezzatura giardinaggio' });
      specs.push({ label: 'Brand', value: brand });
      specs.push({ label: 'Ricambi', value: 'in officina autorizzata' });
      specs.push({ label: 'Garanzia', value: '2 anni' });
    }
    return specs;
  }

  /* ——— Render della scheda ——— */
  function render(item) {
    if (!item) {
      host.innerHTML = `
        <section class="generic-detail__empty">
          <p class="eyebrow">Scheda non trovata</p>
          <h1>Questo prodotto<br><em class="serif-italic">non c'è (più).</em></h1>
          <p>Magari l'indirizzo è cambiato o il prodotto è uscito di catalogo.</p>
          <div class="generic-detail__cta-row">
            <a class="btn btn--primary" href="../prodotti.html">Torna al catalogo</a>
            <a class="btn btn--outline" href="https://wa.me/393464156981?text=Buongiorno%2C%20vorrei%20info%20su%20un%20prodotto%20del%20catalogo" target="_blank" rel="noopener">Chiedi info</a>
          </div>
        </section>
      `;
      return;
    }

    document.title = `${item.brand} ${item.name} — Motor Garden Bazzana`;
    const md = document.querySelector('meta[name="description"]');
    if (md) md.setAttribute('content', `${item.brand} ${item.name}: ${item.cat}. Disponibile da Motor Garden Bazzana, Cene (BG).`);

    const desc = generateDesc(item.brand, item.name, item.cat);
    const similar = findSimilar(item);
    const waText = encodeURIComponent(`Buongiorno, vorrei info su ${item.brand} ${item.name}`);
    const imgSrc = item.img ? ('../' + item.img.replace(/^\/+/, '')) : '';
    const specs = generateSpecs(item.brand, item.name, item.cat);
    const specsHTML = specs.map(s => `<dt>${escapeHtml(s.label)}</dt><dd>${escapeHtml(s.value)}</dd>`).join('');

    host.innerHTML = `
      <p class="generic-detail__crumbs"><a href="../index.html">Home</a> / <a href="../prodotti.html">Prodotti</a> / ${escapeHtml(item.brand)} ${escapeHtml(item.name)}</p>

      <section class="generic-detail__hero">
        <div class="generic-detail__media">
          ${imgSrc ? `<img src="${escapeHtml(imgSrc)}" alt="${escapeHtml(item.brand)} ${escapeHtml(item.name)}" loading="eager" onerror="this.onerror=null;this.src='../assets/img/placeholder-foto-arrivo.svg';">` : ''}
        </div>
        <div class="generic-detail__body">
          <div class="generic-detail__meta">
            <span class="generic-detail__brand-chip">${escapeHtml(item.brand)}</span>
            <span class="generic-detail__cat">${escapeHtml(item.cat)}</span>
          </div>
          <h1 class="generic-detail__title">
            <span class="generic-detail__model">${escapeHtml(item.name)}</span>
          </h1>
          <p class="generic-detail__desc">${escapeHtml(desc)}</p>
          <div class="generic-detail__cta-row">
            <a class="generic-detail__cta generic-detail__cta--primary" href="https://wa.me/393464156981?text=${waText}" target="_blank" rel="noopener" data-product-cta="pdf">
              <span>Chiedi disponibilità (+ PDF)</span>
              <span class="generic-detail__cta-arrow" aria-hidden="true">→</span>
            </a>
            <a class="generic-detail__cta generic-detail__cta--ghost" href="tel:+393464156981">
              <span>346 4156981</span>
            </a>
          </div>
          <p class="generic-detail__note">
            <strong>Per prezzo e disponibilità esatti, contattaci.</strong>
            I prezzi possono variare in base alla configurazione e alle promo del momento. Passa in showroom a Cene (BG) per vedere e provare la macchina.
          </p>
        </div>
      </section>

      <!-- Pannello "DESCRIZIONE TECNICA" / "SPECIFICHE" — stesso layout delle schede dedicate (Ligier, Stihl MS 251 ecc.) -->
      <section class="generic-detail__panel">
        <div class="generic-detail__panel-inner">
          <div class="generic-detail__panel-col">
            <span class="generic-detail__panel-eyebrow">Descrizione tecnica</span>
            <h2 class="generic-detail__panel-title">Cosa fa<br><em class="serif-italic">${escapeHtml(item.brand)} ${escapeHtml(item.name)}</em></h2>
            <p class="generic-detail__panel-body">${escapeHtml(desc)}</p>
          </div>
          <div class="generic-detail__panel-col">
            <span class="generic-detail__panel-eyebrow">Specifiche</span>
            <dl class="generic-detail__panel-specs">${specsHTML}</dl>
            <p class="generic-detail__panel-disclaimer">
              <strong>Valori indicativi.</strong> Specifiche esatte e configurazioni disponibili in showroom o via WhatsApp.
            </p>
          </div>
        </div>
      </section>

      <section class="generic-detail__shop">
        <div class="generic-detail__shop-inner">
          <p class="eyebrow">In showroom a Cene</p>
          <h2>Prova la macchina<br><em class="serif-italic">prima di prenderla.</em></h2>
          <p>Il banco è acceso, l'officina anche. Ti diciamo subito ricambi, tempi di consegna e ti facciamo provare la macchina prima dell'acquisto.</p>
          <div class="generic-detail__cta-row">
            <a class="generic-detail__cta generic-detail__cta--primary" href="https://wa.me/393464156981?text=${waText}" target="_blank" rel="noopener">WhatsApp →</a>
            <a class="generic-detail__cta generic-detail__cta--ghost" href="../contatti.html">Vieni a trovarci</a>
          </div>
        </div>
      </section>

      ${similar.length ? `
      <section class="generic-detail__similar">
        <header class="generic-detail__similar-head">
          <p class="eyebrow">Altri ${escapeHtml(item.brand)}</p>
          <h3>Modelli affini</h3>
        </header>
        <div class="generic-detail__similar-grid">
          ${similar.map(p => `
            <a class="generic-detail__similar-card" href="dettaglio.html?brand=${encodeURIComponent(p.brand)}&name=${encodeURIComponent(p.name)}">
              ${p.img ? `<img src="../${escapeHtml(p.img.replace(/^\/+/, ''))}" alt="" loading="lazy" onerror="this.onerror=null;this.src='../assets/img/placeholder-foto-arrivo.svg';">` : '<span class="generic-detail__similar-thumb-empty"></span>'}
              <div class="generic-detail__similar-meta">
                <span class="generic-detail__similar-brand">${escapeHtml(p.brand)}</span>
                <p class="generic-detail__similar-name">${escapeHtml(p.name)}</p>
                <p class="generic-detail__similar-cat">${escapeHtml(p.cat)}</p>
              </div>
              <span class="generic-detail__similar-arrow" aria-hidden="true">→</span>
            </a>
          `).join('')}
        </div>
      </section>
      ` : ''}
    `;

    /* Aggancia la generazione PDF al click su "Chiedi disponibilità" */
    document.querySelectorAll('[data-product-cta="pdf"]').forEach(btn => {
      btn.addEventListener('click', (ev) => {
        ev.preventDefault();
        if (window.bznGenerateProductPDF) {
          window.bznGenerateProductPDF({
            brand: item.brand,
            model: item.name,
            category: item.cat,
            description: desc,
            img: item.img,
            specs: null
          });
        } else {
          window.open(btn.href, '_blank', 'noopener');
        }
      });
    });
  }

  /* ——— Bootstrap ——— */
  (async () => {
    let item = findItem();
    if (!item && idParam) {
      item = await fetchById(idParam);
    }
    // Estremo fallback: se ancora non c'è item ma abbiamo almeno brand+name
    // o un id, generiamo una scheda sintetica (placeholder + desc generata).
    if (!item) {
      const p = new URLSearchParams(location.search);
      const b = (p.get('brand') || '').trim();
      const n = (p.get('name') || '').trim();
      if (b || n) {
        item = {
          brand: b || 'Motor Garden Bazzana',
          name:  n || 'Prodotto',
          cat:   '',
          img:   'assets/img/placeholder-foto-arrivo.svg',
          slug:  '',
          _synthetic: true
        };
      }
    }
    render(item);
  })();
})();
