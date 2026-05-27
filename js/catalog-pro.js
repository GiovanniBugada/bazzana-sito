/* =========================================================
   CATALOG PRO — descrizione + scheda per OGNI prodotto
   - Per i 15 prodotti del database: descrizione completa + link detail page
   - Per i ~620 prodotti rimanenti: descrizione generata da brand+modello+categoria
   - Bottone "Scheda" su overlay di ogni card che apre modal popup
   ========================================================= */
(() => {
  'use strict';

  const catalogRoot = document.querySelector('.product-catalog');
  if (!catalogRoot) return;

  /* ——— Sposta tutti i gruppi "accessori" in fondo al catalogo ———
     Le macchine (motori) vanno mostrate prima, poi una sezione
     dedicata "Accessori, ricambi e DPI" raccoglie il resto. */
  (function moveAccessoriToBottom() {
    const accGroups = Array.from(
      catalogRoot.querySelectorAll('.cat-group[data-type="accessori"]')
    );
    if (!accGroups.length) return;

    let accSection = catalogRoot.querySelector('.brand-section[data-brand="accessori"]');
    if (!accSection) {
      accSection = document.createElement('div');
      accSection.className = 'brand-section';
      accSection.setAttribute('data-brand', 'accessori');
      const h3 = document.createElement('h3');
      h3.className = 'brand-section__title';
      h3.textContent = 'Accessori, ricambi e DPI';
      accSection.appendChild(h3);
      catalogRoot.appendChild(accSection);
    }

    accGroups.forEach(g => accSection.appendChild(g));
  })();

  const products = window.BAZZANA_PRODUCTS || [];

  // Mappa: brand+model → product detail
  const byKey = new Map();
  products.forEach(p => {
    const keyFull = (p.brand + ' ' + p.model).toLowerCase().replace(/\s+/g, ' ').trim();
    byKey.set(keyFull, p);
    byKey.set(p.model.toLowerCase().replace(/\s+/g, ' ').trim(), p);
  });

  /* ——— Genera descrizione fallback per i prodotti NON in database ———
     Più ricca: combina sotto-categoria + brand per dare un blurb specifico
     anziché una frase generica per categoria. */
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
    const key = (brand || '').toLowerCase().trim();
    return BRAND_NOTES[key] || 'In showroom a Cene (BG) — manutenzione e ricambi in officina autorizzata.';
  }

  /* ——— Parser del codice modello —————————————————————————
     Estrae info utili dal model code (cilindrata, larghezza, voltaggio…)
     per arricchire la descrizione con dati specifici di QUEL modello. */
  function parseModelHints(model, category, brand) {
    const m = (model || '').toUpperCase();
    const cat = (category || '').toLowerCase();
    const b = (brand || '').toLowerCase();
    const hints = {};

    // Estrai TUTTI i numeri dal modello
    const nums = (m.match(/\d+(?:[.,]\d+)?/g) || []).map(n => parseFloat(n.replace(',', '.')));

    /* Cilindrata (motoseghe / decespugliatori benzina) ————————
       Convenzioni comuni dei produttori che teniamo:
       - Active: "51.51" / "56.56" / "62.62" → cilindrata = prima parte
       - Active da potatura "28.28" "31.31" "39.39" → 28cc, 31cc, 39cc
       - Oleo-Mac: "GS451" / "GS650" → estrai prime 2-3 cifre come cc
       - Shindaiwa: "7310SX" / "362TS30" → prime 3 cifre = cc/10 (es. 731 = 73.1 cc)
       - Stihl: "MS 251" / "FS 131" → numero come cc
       - Kress: "60V" → voltaggio batteria, non cilindrata */

    // Pattern brand-specifici
    if (b === 'active' && /^\d+[.\d]+$/.test(m.replace(/\s/g, ''))) {
      // "51.51" → 51cc, "28.28" → 28cc
      hints.cc = Math.round(nums[0]);
    } else if (b === 'oleo-mac' || b === 'oleomac') {
      // "GS451" → 45cc, "GS650" → 65cc (le ultime cifre indicano cc*10)
      const codeMatch = m.match(/^[A-Z]+\s*(\d{2,4})/);
      if (codeMatch && cat.includes('motoseg')) {
        const n = parseInt(codeMatch[1], 10);
        if (n >= 200 && n <= 999) hints.cc = Math.round(n / 10);
        else if (n >= 30 && n <= 99) hints.cc = n;
      }
    } else if (b === 'shindaiwa') {
      // "7310SX" → 73cc, "362TS30" → 36cc/30cm spranga
      // Le prime 3-4 cifre = cc*10 (es. "7310"→73.1cc, "362"→36.2cc)
      const codeMatch = m.match(/^(\d{3,4})/);
      if (codeMatch && cat.includes('motoseg')) {
        const n = parseInt(codeMatch[1], 10);
        if (n >= 1000 && n <= 9999) hints.cc = Math.floor(n / 100);
        else if (n >= 200 && n <= 999) hints.cc = Math.floor(n / 10);
      }
      // Spranga: "...30" o "...40" alla fine
      const barMatch = m.match(/(\d{2})$/);
      if (barMatch) {
        const n = parseInt(barMatch[1], 10);
        if (n >= 25 && n <= 70) hints.barCm = n;
      }
    } else if (b === 'stihl') {
      // "MS 251" → 25cc circa (in realtà 45cc, codice diverso)
      // Per Stihl il numero non è cc lineare, lasciamo solo nome
    }

    /* Larghezza taglio (rasaerba) ————————————————————————————
       I rasaerba spesso hanno il numero di larghezza nel modello:
       - "4760SA" → 47cm taglio
       - "5400SA" → 54cm taglio
       - "4260A"  → 42cm taglio */
    if (cat.includes('tosaerb') || cat.includes('rasaerb')) {
      const numMatch = m.match(/^(\d{2,4})/);
      if (numMatch) {
        const n = parseInt(numMatch[1], 10);
        // "4760" → 47cm taglio, "5400" → 54cm. Floor non round.
        if (n >= 4000 && n <= 6999) hints.cutCm = Math.floor(n / 100);
        else if (n >= 36 && n <= 70) hints.cutCm = n;
      }
    }

    /* Voltaggio batteria (Kress 60V ecc.) */
    const voltMatch = m.match(/(\d{2})\s*V/i);
    if (voltMatch) {
      const v = parseInt(voltMatch[1], 10);
      if (v >= 18 && v <= 80) hints.voltage = v;
    }

    /* Potenza in kW (generatori) */
    if (cat.includes('genera')) {
      const kwMatch = m.match(/(\d{1,5})\s*(I|S|A|GE)/);
      if (kwMatch) {
        const n = parseInt(kwMatch[1], 10);
        if (n >= 1000) hints.watt = n;
        else if (n >= 1 && n <= 12) hints.kw = n;
      }
    }

    return hints;
  }

  /* ——— Genera descrizione ricca per ciascun prodotto ———
     Combina: categoria + brand + parsing del codice modello +
     dettagli specifici. Niente più descrizioni "fotocopia". */
  function generateFallbackDesc(brand, model, category) {
    const cat = (category || '').toLowerCase();
    const parts = cat.split(/\s*[-·]\s*/);
    const sub = parts[1] || '';
    const m = model || 'questo modello';
    const hints = parseModelHints(model, category, brand);

    /* Stringa di "dato specifico" che si aggiunge alla descrizione */
    let dataNote = '';
    if (hints.cc) dataNote = ` Cilindrata indicativa ${hints.cc} cc.`;
    if (hints.cutCm) dataNote += ` Larghezza di taglio circa ${hints.cutCm} cm.`;
    if (hints.barCm) dataNote += ` Lunghezza spranga ${hints.barCm} cm.`;
    if (hints.voltage) dataNote += ` Piattaforma batteria ${hints.voltage} V.`;
    if (hints.kw) dataNote += ` Potenza ${hints.kw} kW.`;
    if (hints.watt) dataNote += ` Potenza ${hints.watt} W.`;

    let core = '';

    // ——— MOTOSEGHE ———
    if (cat.includes('motosega') || cat.includes('motoseg')) {
      if (sub.includes('abbat')) {
        core = `Il ${brand} ${m} è una motosega da abbattimento pensata per lavori forestali impegnativi: spranga lunga, motore robusto, freno catena di sicurezza. Per chi taglia legna in proprio o lavora il bosco, è la macchina che porta a casa anche le giornate intere.${dataNote}`;
      } else if (sub.includes('potatura')) {
        core = `Il ${brand} ${m} è una motosega da potatura leggera, equilibrata per uso in tree-climbing e per tagliare rami sopra testa con una sola mano in sicurezza. Ottima per arboricoltori, manutentori del verde e potatori esperti.${dataNote}`;
      } else if (sub.includes('professional')) {
        core = `Il ${brand} ${m} è una motosega professionale per uso intensivo quotidiano. Motore generoso, accesso facilitato alle parti di manutenzione, regolazioni semplificate per ridurre i fermo macchina.${dataNote}`;
      } else {
        core = `Il ${brand} ${m} è una motosega della gamma per lavori di taglio legna, manutenzione del giardino o piccoli abbattimenti. Affilatura catena disponibile in officina, ricambi originali in 48 h.${dataNote}`;
      }
    }
    // ——— TOSAERBA / RASAERBA ———
    else if (cat.includes('tosaerb') || cat === 'rasaerba' || cat.startsWith('rasaerba')) {
      if (sub.includes('mulching')) {
        core = `Il ${brand} ${m} è un rasaerba con sistema mulching che taglia finemente l'erba e la restituisce al prato come concime naturale. Niente cesto da svuotare, prato più sano e meno stress sull'utente.${dataNote}`;
      } else if (sub.includes('alluminio')) {
        core = `Il ${brand} ${m} è un rasaerba con scocca in alluminio pressofuso: leggero da spingere, resistente alla corrosione, durata maggiore rispetto all'acciaio.${dataNote}`;
      } else if (sub.includes('accaio') || sub.includes('acciaio')) {
        core = `Il ${brand} ${m} è un rasaerba con scocca in acciaio verniciato, robusto e adatto a terreni irregolari o con piccoli sassi. Manutenzione semplice, ricambi sempre disponibili.${dataNote}`;
      } else if (sub.includes('semove') || sub.includes('trazion')) {
        core = `Il ${brand} ${m} è un rasaerba semovente con trazione che ti spinge la macchina e ti scarica le braccia su pendenze leggere e prati grandi.${dataNote}`;
      } else if (sub.includes('elettr') || sub.includes('batter')) {
        core = `Il ${brand} ${m} è un rasaerba a batteria, silenzioso e senza emissioni dirette. Ideale per giardini residenziali medio-piccoli e per chi non vuole più gestire benzina e miscela.${dataNote}`;
      } else {
        core = `Il ${brand} ${m} è un rasaerba pensato per il giardino di casa: taglio netto, raccolta efficiente, manutenzione semplice. Disponibile in versione a spinta o semovente.${dataNote}`;
      }
    }
    // ——— ROBOT RASAERBA ———
    else if (cat.includes('robot')) {
      core = `Il ${brand} ${m} è un robot rasaerba che mantiene il prato sempre tagliato lavorando in autonomia. Installazione del cavo perimetrale a cura del nostro tecnico, manutenzione lame e batteria gestita in officina.${dataNote}`;
    }
    // ——— TRATTORINI ———
    else if (cat.includes('trattorin') || cat.includes('rider')) {
      core = `Il ${brand} ${m} è un trattorino rasaerba per giardini di grandi dimensioni. Sterzo confortevole, sedile a comando rapido, raccolta o scarico posteriore.${dataNote}`;
    }
    // ——— DECESPUGLIATORI ———
    else if (cat.includes('decespu')) {
      if (sub.includes('zaino')) {
        core = `Il ${brand} ${m} è un decespugliatore a zaino con il peso del motore scaricato sulla schiena, per giornate intere di lavoro senza affaticare braccia e spalle. Ideale per professionisti del verde.${dataNote}`;
      } else if (sub.includes('asta fissa') || sub.includes('asta-fissa')) {
        core = `Il ${brand} ${m} è un decespugliatore ad asta fissa, robusto, con manubrio bike-handle a doppia impugnatura per controllo su grandi superfici. Cinghia ergonomica inclusa.${dataNote}`;
      } else if (sub.includes('attrezzi') || sub.includes('multifunzione') || sub.includes('evolution')) {
        core = `Il ${brand} ${m} fa parte della linea multifunzione: un'unica unità motore con attrezzi intercambiabili (decespugliatore, tagliasiepi, potatore, soffiatore) per chi non vuole comprare macchine diverse.${dataNote}`;
      } else {
        core = `Il ${brand} ${m} è un decespugliatore per erba alta, sterpaglia, polloni e prati irregolari. Versatile, ricambi sempre disponibili in officina.${dataNote}`;
      }
    }
    // ——— TAGLIASIEPI ———
    else if (cat.includes('tagliasi')) {
      core = `Il ${brand} ${m} è un tagliasiepi a doppia lama per taglio netto su siepi formali, arbusti densi, recinzioni verdi. Lame antiurto, bilanciamento studiato per ridurre l'affaticamento.${dataNote}`;
    }
    // ——— SOFFIATORI ———
    else if (cat.includes('soffia') || cat.includes('aspirator')) {
      if (sub.includes('zaino')) {
        core = `Il ${brand} ${m} è un soffiatore a zaino professionale: alta velocità dell'aria, peso ben distribuito sulla schiena, autonomia per pulire intere proprietà in una mattinata.${dataNote}`;
      } else if (sub.includes('batter')) {
        core = `Il ${brand} ${m} è un soffiatore a batteria, silenzioso e immediato all'accensione. Ottimo per chi pulisce in orari "sensibili" o vicino a clienti/abitazioni.${dataNote}`;
      } else {
        core = `Il ${brand} ${m} è un soffiatore per pulizia di viali, cortili, vialetti e residui leggeri. Versioni a benzina per uso intensivo o a batteria per silenziosità.${dataNote}`;
      }
    }
    // ——— GENERATORI ———
    else if (cat.includes('genera')) {
      if (sub.includes('inverter')) {
        core = `Il ${brand} ${m} è un generatore inverter sinusoidale: corrente pulita, sicura per laptop, frigoriferi e dispositivi elettronici sensibili. Silenzioso, leggero, ideale per camper e backup casa.${dataNote}`;
      } else if (sub.includes('avr')) {
        core = `Il ${brand} ${m} è un generatore con regolazione automatica del voltaggio (AVR), ideale per cantieri, attrezzature elettriche e emergenze prolungate.${dataNote}`;
      } else {
        core = `Il ${brand} ${m} è un generatore portatile per cantiere, emergenza domestica o eventi outdoor. Avviamento a strappo o elettrico, autonomia generosa.${dataNote}`;
      }
    }
    // ——— MOTOZAPPE ———
    else if (cat.includes('motozap') || cat.includes('motoco')) {
      core = `Il ${brand} ${m} è una motozappa con frese in acciaio temprato per lavorazione orto, aiuole, piccoli appezzamenti. Trasmissione robusta, ideale per la preparazione del terreno a primavera.${dataNote}`;
    }
    // ——— TRINCIASARMENTI ———
    else if (cat.includes('trincia')) {
      if (sub.includes('hd')) {
        core = `Il ${brand} ${m} è un trinciasarmenti serie HD per uso semi-intensivo su erba alta e ramaglia leggera. Telaio rinforzato, lame a Y forgiate.${dataNote}`;
      } else if (sub.includes('pro')) {
        core = `Il ${brand} ${m} è un trinciasarmenti serie PRO per uso professionale e terreni difficili. Ribaltabile, manutenzione veloce, lame a martello.${dataNote}`;
      } else {
        core = `Il ${brand} ${m} è un trinciasarmenti per manutenzione di terreni incolti, bordure e ramaglia. Lavora dove un rasaerba non riesce.${dataNote}`;
      }
    }
    else if (cat.includes('arieggi')) {
      core = `Il ${brand} ${m} è un arieggiatore per arieggiare il prato a primavera e in autunno: rimuove feltro e muschio, ossigena le radici, prato più sano in poche ore.${dataNote}`;
    } else if (cat.includes('levazoll')) {
      core = `Il ${brand} ${m} è una levazolle per rimuovere il manto erboso e preparare il terreno alla risemina o alla posa di una nuova zollatura.${dataNote}`;
    }
    else if (cat.includes('scuotit') || cat.includes('abbacch')) {
      if (sub.includes('batter')) {
        core = `Il ${brand} ${m} è un abbacchiatore a batteria per la raccolta delle olive: leggero, silenzioso, autonomia per una giornata di lavoro standard.${dataNote}`;
      } else {
        core = `Il ${brand} ${m} è uno scuotitore a motore per raccolta intensiva di olive e frutta secca: produttività superiore alla raccolta manuale, fatica ridotta.${dataNote}`;
      }
    }
    else if (cat.includes('trivell')) {
      core = `Il ${brand} ${m} è una trivella per scavare buche per piantagione, paletti di recinzione, pali da vigna. Punte intercambiabili di diametri diversi.${dataNote}`;
    }
    else if (cat.includes('potator')) {
      core = `Il ${brand} ${m} è un potatore ad asta per tagliare rami in altezza senza scala. Asta telescopica/fissa, catena d'acciaio, perfetto per la potatura di alberi medi.${dataNote}`;
    }
    else if (cat.includes('spazzan')) {
      core = `Il ${brand} ${m} è uno spazzaneve per liberare viali, accessi e piazzali dopo le nevicate. Getto orientabile, trazione su ruote o cingoli.${dataNote}`;
    }
    else if (cat.includes('powertrack') || cat.includes('carriol') || cat.includes('transport')) {
      core = `Il ${brand} ${m} è un mini-transporter cingolato per spostare carichi su terreni difficili: vigneto, frutteto, cantieri di montagna. Portata generosa, ribaltabile idraulico opzionale.${dataNote}`;
    }
    else if (cat.includes('cippa') || cat.includes('biotri')) {
      core = `Il ${brand} ${m} è un biotrituratore per ridurre rami e potature in cippato pronto per la pacciamatura o per il caminetto. Diametri di lavoro variabili per modello.${dataNote}`;
    }
    else if (cat.includes('micro') || cat.includes('quadric')) {
      core = `Il ${brand} ${m} è una microcar omologata L6e, guidabile dai 14 anni con patente AM (€80 il rinnovo). Ricarica da presa di casa, autonomia per la routine quotidiana città-paese.${dataNote}`;
    }
    else if (cat.includes('access') || cat.includes('ricam')) {
      if (cat.includes('decespu')) {
        core = `${brand} ${m}: accessorio o ricambio originale per decespugliatori della gamma. Montaggio in officina o consegna a casa.`;
      } else if (cat.includes('motoseg')) {
        core = `${brand} ${m}: accessorio o ricambio originale per motoseghe. Catene, spranghe, filtri, candele — tutto a magazzino.`;
      } else if (cat.includes('batter')) {
        core = `${brand} ${m}: batteria o caricabatterie compatibile con la piattaforma del marchio. Garanzia ufficiale, sostituzione lithium in officina.`;
      } else {
        core = `${brand} ${m}: accessorio o ricambio originale, disponibile in negozio o in 48 h dal nostro fornitore.`;
      }
    }
    else if (cat.includes('olio') || cat.includes('lubrif') || cat.includes('tanich') || cat.includes('miscel')) {
      core = `${brand} ${m}: olio o miscela carburante consigliato dal costruttore. Usa l'originale: prolunga la vita del motore e mantiene la garanzia ufficiale del produttore.`;
    }
    else if (cat.includes('abbiglia') || cat.includes('dpi') || cat.includes('protet')) {
      core = `${brand} ${m}: dispositivi di protezione individuale certificati per uso forestale e con utensili motorizzati. Sicurezza prima di tutto: meglio il DPI che la trasferta in pronto soccorso.`;
    }
    else {
      core = `Il ${brand} ${m} è un'attrezzatura per la cura del verde, disponibile in showroom a Cene (BG).${dataNote}`;
    }

    return core + ' ' + brandTail(brand);
  }

  /* ——— Crea modal popup riusabile (1 per pagina) ——— */
  let modal = null;
  function getModal() {
    if (modal) return modal;
    modal = document.createElement('div');
    modal.className = 'product-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.innerHTML = `
      <div class="product-modal__backdrop"></div>
      <div class="product-modal__panel">
        <button class="product-modal__close" aria-label="Chiudi">×</button>
        <div class="product-modal__media">
          <img class="product-modal__img" src="" alt="">
        </div>
        <div class="product-modal__body">
          <span class="product-modal__brand"></span>
          <h2 class="product-modal__title"></h2>
          <p class="product-modal__cat"></p>
          <div class="product-modal__desc"></div>
          <dl class="product-modal__specs" hidden></dl>
          <div class="product-modal__actions">
            <a class="product-modal__cta product-modal__cta--primary" href="#" target="_blank" rel="noopener">
              <span>Chiedi disponibilità</span>
              <span aria-hidden="true">→</span>
            </a>
            <a class="product-modal__cta product-modal__cta--ghost" href="#" hidden>Scheda completa</a>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
    const close = () => modal.classList.remove('is-open');
    modal.querySelector('.product-modal__close').addEventListener('click', close);
    modal.querySelector('.product-modal__backdrop').addEventListener('click', close);
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('is-open')) close();
    });
    return modal;
  }

  function openModal({ brand, model, category, desc, img, alt, detailHref, specs }) {
    const m = getModal();
    m.querySelector('.product-modal__brand').textContent = brand;
    m.querySelector('.product-modal__title').textContent = model;
    m.querySelector('.product-modal__cat').textContent = category;
    m.querySelector('.product-modal__desc').textContent = desc;
    const imgEl = m.querySelector('.product-modal__img');
    imgEl.onerror = function() { this.onerror = null; this.src = 'assets/img/placeholder-foto-arrivo.svg'; };
    imgEl.src = img;
    imgEl.alt = alt || (brand + ' ' + model);
    // Specs
    const specsEl = m.querySelector('.product-modal__specs');
    if (specs && specs.length) {
      specsEl.innerHTML = specs.map(s => `<dt>${s.label}</dt><dd>${s.value}</dd>`).join('');
      specsEl.hidden = false;
    } else {
      specsEl.hidden = true;
    }
    // CTA "Chiedi disponibilità": genera PDF + apre WhatsApp.
    // Fallback: se il PDF non viene generato (es. jsPDF non si carica),
    // la funzione apre comunque WhatsApp.
    const waText = encodeURIComponent('Buongiorno, vorrei info su ' + brand + ' ' + model);
    const primaryCTA = m.querySelector('.product-modal__cta--primary');
    primaryCTA.href = 'https://wa.me/393464156981?text=' + waText;
    primaryCTA.onclick = function (e) {
      e.preventDefault();
      if (window.bznGenerateProductPDF) {
        window.bznGenerateProductPDF({
          brand, model, category, description: desc, img, specs: specs || null
        });
      } else {
        // Fallback senza PDF
        window.open(this.href, '_blank', 'noopener');
      }
    };
    // Detail link
    const detailBtn = m.querySelector('.product-modal__cta--ghost');
    if (detailHref) {
      detailBtn.href = detailHref;
      detailBtn.hidden = false;
    } else {
      detailBtn.hidden = true;
    }
    m.classList.add('is-open');
  }

  /* ——— Processa ogni card del catalogo (no per-card listeners!) ———
     Cache productInfo in WeakMap keyed by card → 1 listener delegato sul root.
     Riduzione drastica del lag con 600+ card. */
  const productInfoCache = new WeakMap();
  const cards = document.querySelectorAll('.depth-card');
  let withDetail = 0, withFallback = 0;

  cards.forEach(card => {
    const brand = (card.dataset.productBrand || '').trim();
    const name = (card.dataset.productName || '').trim();
    const category = (card.dataset.productCat || '').replace(/-/g, '·').trim();
    const imgSrc = card.dataset.productImg || card.querySelector('img')?.src || '';
    if (!brand || !name) return;

    // Database lookup
    const keyFull = (brand + ' ' + name).toLowerCase();
    const keyShort = name.toLowerCase();
    const dbProduct = byKey.get(keyFull) || byKey.get(keyShort);

    const productInfo = dbProduct ? {
      brand: dbProduct.brand,
      model: dbProduct.model,
      category: dbProduct.category,
      desc: dbProduct.description,
      img: imgSrc,
      alt: brand + ' ' + name,
      detailHref: 'prodotti/' + dbProduct.slug + '.html',
      specs: dbProduct.specs
    } : {
      brand,
      model: name,
      category: category || (brand + ' · catalogo'),
      desc: generateFallbackDesc(brand, name, category),
      img: imgSrc,
      alt: brand + ' ' + name,
      detailHref: 'prodotti/dettaglio.html?id=' + encodeURIComponent(card.dataset.productId || '') + '&brand=' + encodeURIComponent(brand) + '&name=' + encodeURIComponent(name),
      specs: null
    };

    if (dbProduct) { withDetail++; card.classList.add('has-detail'); }
    else withFallback++;
    productInfoCache.set(card, productInfo);

    // Sostituisci overlay con titolo + descrizione preview + bottoni
    const overlay = card.querySelector('.depth-card__overlay');
    if (overlay) {
      const preview = makePreview(productInfo.desc);
      overlay.innerHTML = `
        <h4 class="depth-card__title">${productInfo.brand} ${productInfo.model}</h4>
        <p class="depth-card__desc-preview">${preview}</p>
        <button class="depth-card__detail-cta" type="button" data-action="open-modal">
          <span>Scheda</span>
          <span aria-hidden="true">→</span>
        </button>
      `;
      card.style.cursor = 'pointer';
    }
  });

  /* UN SOLO listener delegato sul root del catalogo per tutte le card */
  catalogRoot.addEventListener('click', (e) => {
    const card = e.target.closest('.depth-card');
    if (!card) return;
    // Skip se cliccato su un controllo interattivo dentro la card
    if (e.target.closest('input, label, .depth-card__compare, a')) return;
    const info = productInfoCache.get(card);
    if (info) {
      e.preventDefault();
      openModal(info);
    }
  });

  /* Fallback img errore: 1 listener delegato (capture phase per pescare 'error') */
  catalogRoot.addEventListener('error', (e) => {
    const img = e.target;
    if (img && img.tagName === 'IMG' && !img.dataset.bznFallbackApplied) {
      img.dataset.bznFallbackApplied = '1';
      img.src = 'assets/img/placeholder-foto-arrivo.svg';
    }
  }, true);

  /* ——— Toolbar filtri arricchita: conteggi brand + filtri categoria + search AND ——— */
  enhanceFilterToolbar();

  function normalize(s) {
    return (s || '').toString().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').trim();
  }

  function enhanceFilterToolbar() {
    const allCards = Array.from(document.querySelectorAll('.product-catalog .depth-card'));
    if (!allCards.length) return;

    // ——— Conteggio per brand ———
    const brandCount = new Map();
    const catCount = new Map();
    allCards.forEach(c => {
      const b = (c.dataset.productBrand || '').toLowerCase();
      brandCount.set(b, (brandCount.get(b) || 0) + 1);
      // Categoria "macro" = prima parte prima del " - " / " · "
      const fullCat = (c.dataset.productCat || '').split(/\s*[-·]\s*/)[0].trim();
      if (fullCat) catCount.set(fullCat, (catCount.get(fullCat) || 0) + 1);
    });
    const totalCount = allCards.length;

    // ——— Aggiunge i conteggi sui chip brand già presenti in HTML ———
    document.querySelectorAll('.filter-chips .chip[data-filter]').forEach(chip => {
      const f = chip.dataset.filter;
      const n = f === 'all' ? totalCount : (brandCount.get(f) || 0);
      // Evita duplicati se aggiunto già
      if (!chip.querySelector('.chip__count')) {
        const span = document.createElement('span');
        span.className = 'chip__count';
        span.textContent = n;
        chip.appendChild(span);
      }
    });

    // ——— Riga categorie sotto i brand ———
    const brandRow = document.querySelector('.filter-chips');
    if (brandRow && !document.querySelector('.filter-chips--cat')) {
      // Top 10 categorie per conteggio
      const cats = Array.from(catCount.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
      const catRow = document.createElement('div');
      catRow.className = 'filter-chips filter-chips--cat';
      catRow.setAttribute('role', 'tablist');
      catRow.setAttribute('aria-label', 'Filtra per categoria');
      catRow.innerHTML = `
        <span class="filter-chips__label">Categoria:</span>
        <button class="chip chip--cat is-active" data-cat="all">Tutte<span class="chip__count">${totalCount}</span></button>
        ${cats.map(([name, n]) => `
          <button class="chip chip--cat" data-cat="${escapeAttr(name)}">${escapeHtml(name)}<span class="chip__count">${n}</span></button>
        `).join('')}
      `;
      brandRow.parentNode.insertBefore(catRow, brandRow.nextSibling);
    }

    // ——— Counter "X prodotti totali" e search input ———
    const searchInput = document.getElementById('catalog-search');
    const counter = document.getElementById('catalog-search-count');

    // Stato attivo dei filtri
    let activeBrand = 'all';
    let activeCat = 'all';
    let query = '';

    /* Applica i filtri AND */
    function applyFilters() {
      const qNorm = normalize(query);
      let visible = 0;

      allCards.forEach(card => {
        const b = (card.dataset.productBrand || '').toLowerCase();
        const fullCat = (card.dataset.productCat || '').split(/\s*[-·]\s*/)[0].trim();
        const hay = normalize(`${card.dataset.productBrand} ${card.dataset.productName} ${card.dataset.productCat}`);

        const okBrand = activeBrand === 'all' || b === activeBrand;
        const okCat = activeCat === 'all' || fullCat === activeCat;
        const okQuery = !qNorm || hay.includes(qNorm);

        const visibleNow = okBrand && okCat && okQuery;
        card.style.display = visibleNow ? '' : 'none';
        if (visibleNow) visible++;
      });

      // Nascondi sezioni/gruppi vuoti
      document.querySelectorAll('.product-catalog .cat-group').forEach(g => {
        const anyVisible = Array.from(g.querySelectorAll('.depth-card'))
          .some(c => c.style.display !== 'none');
        g.style.display = anyVisible ? '' : 'none';
      });
      document.querySelectorAll('.product-catalog .brand-section').forEach(s => {
        const anyVisible = Array.from(s.querySelectorAll('.depth-card'))
          .some(c => c.style.display !== 'none');
        s.style.display = anyVisible ? '' : 'none';
      });
      // Anche subgroup
      document.querySelectorAll('.product-catalog .subgroup').forEach(sg => {
        const anyVisible = Array.from(sg.querySelectorAll('.depth-card'))
          .some(c => c.style.display !== 'none');
        sg.style.display = anyVisible ? '' : 'none';
      });

      // Aggiorna counter
      if (counter) {
        if (query || activeBrand !== 'all' || activeCat !== 'all') {
          counter.textContent = visible + ' risultat' + (visible === 1 ? 'o' : 'i');
        } else {
          counter.textContent = totalCount + ' prodotti totali';
        }
      }

      // Mostra/nascondi messaggio "nessun risultato"
      let empty = document.querySelector('.product-catalog__empty');
      if (visible === 0) {
        if (!empty) {
          empty = document.createElement('div');
          empty.className = 'product-catalog__empty';
          empty.innerHTML = `
            <p>Nessun prodotto corrisponde ai filtri scelti.</p>
            <button type="button" class="btn btn--outline" data-reset-filters>Reset filtri</button>
          `;
          document.querySelector('.product-catalog').appendChild(empty);
          empty.querySelector('[data-reset-filters]').addEventListener('click', resetFilters);
        }
        empty.style.display = '';
      } else if (empty) {
        empty.style.display = 'none';
      }
    }

    function resetFilters() {
      activeBrand = 'all';
      activeCat = 'all';
      query = '';
      if (searchInput) searchInput.value = '';
      document.querySelectorAll('.filter-chips .chip').forEach(c => c.classList.remove('is-active'));
      document.querySelector('.filter-chips .chip[data-filter="all"]')?.classList.add('is-active');
      document.querySelector('.filter-chips--cat .chip[data-cat="all"]')?.classList.add('is-active');
      applyFilters();
    }

    /* Auto-scroll alle filter chips dopo il filtro brand.
       Cosi' l'utente vede SUBITO i prodotti del brand scelto a partire dall'alto,
       coerentemente per tutti i brand (Stihl, Ligier, Active, etc).
       Posizione fissa = nessuna dipendenza dal layout filtrato. */
    function scrollToFirstVisible() {
      const chipsRow = document.querySelector('.filter-chips');
      if (!chipsRow) return;
      const header = document.querySelector('.site-header');
      const headerH = header ? header.getBoundingClientRect().height : 70;
      const targetY = chipsRow.getBoundingClientRect().top + window.scrollY - headerH - 16;
      window.scrollTo({ top: Math.max(0, targetY), behavior: 'smooth' });
    }

    /* Wire-up chip brand (toglie il vecchio handler in main.js: usiamo evento "click" diverso) */
    document.querySelectorAll('.filter-chips:not(.filter-chips--cat) .chip[data-filter]').forEach(chip => {
      chip.addEventListener('click', (e) => {
        e.stopPropagation();
        document.querySelectorAll('.filter-chips:not(.filter-chips--cat) .chip').forEach(c => c.classList.remove('is-active'));
        chip.classList.add('is-active');
        activeBrand = chip.dataset.filter;
        applyFilters();
        // Se ho selezionato un brand specifico, scrolla alla prima sezione visibile
        if (activeBrand !== 'all') scrollToFirstVisible();
      }, true);
    });

    /* Wire-up chip categoria */
    document.querySelectorAll('.filter-chips--cat .chip[data-cat]').forEach(chip => {
      chip.addEventListener('click', () => {
        document.querySelectorAll('.filter-chips--cat .chip').forEach(c => c.classList.remove('is-active'));
        chip.classList.add('is-active');
        activeCat = chip.dataset.cat;
        applyFilters();
        if (activeCat !== 'all') scrollToFirstVisible();
      });
    });

    /* Wire-up search input (sostituisce il debounce di main.js) */
    if (searchInput) {
      let t;
      searchInput.addEventListener('input', () => {
        clearTimeout(t);
        t = setTimeout(() => {
          query = searchInput.value;
          applyFilters();
          renderSuggestions(query);
        }, 140);
      });
      // Apri suggerimenti al focus
      searchInput.addEventListener('focus', () => renderSuggestions(searchInput.value));
      // Chiudi suggerimenti al blur (delay per consentire click)
      searchInput.addEventListener('blur', () => {
        setTimeout(() => {
          if (suggestionsBox) suggestionsBox.classList.remove('is-open');
        }, 180);
      });
      // Keyboard: Esc chiude, frecce navigano
      searchInput.addEventListener('keydown', (e) => {
        if (!suggestionsBox || !suggestionsBox.classList.contains('is-open')) return;
        const items = Array.from(suggestionsBox.querySelectorAll('.cat-suggest__item'));
        if (!items.length) return;
        let idx = items.findIndex(it => it.classList.contains('is-active'));
        if (e.key === 'Escape') {
          suggestionsBox.classList.remove('is-open');
          e.preventDefault();
        } else if (e.key === 'ArrowDown') {
          e.preventDefault();
          idx = (idx + 1) % items.length;
          items.forEach(it => it.classList.remove('is-active'));
          items[idx].classList.add('is-active');
          items[idx].scrollIntoView({ block: 'nearest' });
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          idx = (idx - 1 + items.length) % items.length;
          items.forEach(it => it.classList.remove('is-active'));
          items[idx].classList.add('is-active');
          items[idx].scrollIntoView({ block: 'nearest' });
        } else if (e.key === 'Enter') {
          if (idx >= 0) {
            e.preventDefault();
            items[idx].click();
          }
        }
      });
    }

    /* ——— Autocomplete: suggerimenti tra i prodotti dell'indice ——— */
    let suggestionsBox = null;
    function getSuggestionsBox() {
      if (suggestionsBox) return suggestionsBox;
      const field = document.querySelector('.catalog-search__field');
      if (!field) return null;
      suggestionsBox = document.createElement('div');
      suggestionsBox.className = 'cat-suggest';
      suggestionsBox.setAttribute('role', 'listbox');
      // Inserisci dopo il field (sotto)
      field.parentNode.insertBefore(suggestionsBox, field.nextSibling);
      return suggestionsBox;
    }

    function normalizeQ(s) {
      return (s || '').toString().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').trim();
    }

    function renderSuggestions(q) {
      const box = getSuggestionsBox();
      if (!box) return;
      const qN = normalizeQ(q);
      const INDEX = window.BZN_SEARCH_INDEX || [];
      let results;

      if (!qN) {
        // Quando vuoto: mostra 8 prodotti random di brand vari
        const sample = [];
        const brandsSet = new Set();
        const shuffled = INDEX.slice().sort(() => Math.random() - 0.5);
        for (const p of shuffled) {
          if (!brandsSet.has(p.brand) || sample.length < 8) {
            sample.push(p);
            brandsSet.add(p.brand);
          }
          if (sample.length >= 8) break;
        }
        results = sample;
      } else {
        // Match: tokens del query devono apparire in brand+name+cat
        const tokens = qN.split(/\s+/).filter(Boolean);
        // Stem: rimuovi vocale finale per matchare singolare/plurale
        // (es. "motosega" matcha anche "motoseghe", "robot" matcha "robots")
        const stems = tokens.map(t => {
          if (t.length >= 4) return t.replace(/[aeiou]+$/, '');
          return t;
        });
        results = INDEX.filter(p => {
          const hay = normalizeQ(p.brand + ' ' + p.name + ' ' + p.cat);
          // Ogni token deve essere presente (esatto OR via stem)
          return stems.every((stem, i) => hay.includes(stem) || hay.includes(tokens[i]));
        }).slice(0, 10);
      }

      if (!results.length) {
        box.innerHTML = '<div class="cat-suggest__empty">Nessun risultato</div>';
        box.classList.add('is-open');
        return;
      }

      box.innerHTML = results.map(p => `
        <button type="button" class="cat-suggest__item" data-brand="${escapeAttr(p.brand)}" data-name="${escapeAttr(p.name)}" role="option">
          ${p.img ? `<img class="cat-suggest__thumb" src="${escapeAttr(p.img)}" alt="" loading="lazy" onerror="this.style.opacity=0.2">` : '<span class="cat-suggest__thumb cat-suggest__thumb--empty"></span>'}
          <span class="cat-suggest__meta">
            <span class="cat-suggest__brand">${escapeHtml(p.brand)}</span>
            <span class="cat-suggest__name">${escapeHtml(p.name)}</span>
            <span class="cat-suggest__cat">${escapeHtml(p.cat)}</span>
          </span>
          <span class="cat-suggest__arrow" aria-hidden="true">→</span>
        </button>
      `).join('');
      box.classList.add('is-open');

      // Click su suggerimento: scrolla al prodotto + lo evidenzia
      box.querySelectorAll('.cat-suggest__item').forEach(btn => {
        btn.addEventListener('mousedown', (e) => { e.preventDefault(); });
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const brand = btn.dataset.brand;
          const name = btn.dataset.name;
          // Cerca card corrispondente
          const card = Array.from(allCards).find(c =>
            (c.dataset.productBrand || '').toLowerCase() === brand.toLowerCase() &&
            (c.dataset.productName || '').toLowerCase() === name.toLowerCase()
          );
          if (card) {
            // Reset filtri per assicurare visibilità
            activeBrand = 'all';
            activeCat = 'all';
            query = '';
            searchInput.value = '';
            document.querySelectorAll('.filter-chips .chip').forEach(c => c.classList.remove('is-active'));
            document.querySelector('.filter-chips .chip[data-filter="all"]')?.classList.add('is-active');
            applyFilters();
            // Scroll + evidenzia
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            card.classList.add('is-highlighted');
            setTimeout(() => card.classList.remove('is-highlighted'), 2200);
            // Apri modal
            setTimeout(() => {
              card.click();
            }, 400);
          }
          box.classList.remove('is-open');
        });
      });
    }
  }

  function escapeAttr(s) {
    return (s || '').replace(/"/g, '&quot;');
  }
  function escapeHtml(s) {
    return (s || '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  /* ——— Anteprima: prima frase reale (non spezza i decimali tipo "5.5") ——— */
  function makePreview(text) {
    if (!text) return '';
    const trimmed = text.trim();
    // Punto/!/? seguito da spazio + maiuscola o fine stringa = fine frase reale
    const m = trimmed.match(/^([\s\S]+?[.!?])(?=\s+[A-ZÀ-Ù]|$)/);
    if (m && m[1].length <= 200) return m[1].trim();
    // Fallback: tronca a ~140 caratteri sul prossimo spazio
    if (trimmed.length <= 140) return trimmed;
    const cut = trimmed.slice(0, 140);
    const last = cut.lastIndexOf(' ');
    return (last > 80 ? cut.slice(0, last) : cut) + '…';
  }
})();
