/* =========================================================
   PDF SCHEDA — genera il PDF di una scheda prodotto, lo fa scaricare,
   poi apre WhatsApp con un messaggio prefilled.

   USO da altro JS:
     window.bznGenerateProductPDF({
       brand: 'Active',
       model: '51.51',
       category: 'Motoseghe - Da Abbattimento',
       description: '...',
       specs: [{label:'Cilindrata', value:'51.7 cc'}, ...],
       img: 'assets/img/...'  // path relativo dalla root del sito
     })

   Carica jsPDF da CDN al primo uso (lazy).
   ========================================================= */
(() => {
  'use strict';

  const JSPDF_CDN = 'https://cdn.jsdelivr.net/npm/jspdf@2.5.2/dist/jspdf.umd.min.js';
  const PHONE = '+393464156981';
  const PHONE_DISPLAY = '346 4156981';
  const EMAIL = 'bazzanamotorgarden@gmail.com';
  const SITE = 'motorgardenbazzana.it';
  const ADDRESS = 'Cene (BG) · Val Seriana';

  let jspdfPromise = null;
  function loadJsPDF() {
    if (window.jspdf) return Promise.resolve(window.jspdf);
    if (jspdfPromise) return jspdfPromise;
    jspdfPromise = new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = JSPDF_CDN;
      s.async = true;
      s.onload = () => resolve(window.jspdf);
      s.onerror = reject;
      document.head.appendChild(s);
    });
    return jspdfPromise;
  }

  /* Risolve path relativo: se il chiamante è in /prodotti/, '../assets/...' funziona,
     altrimenti 'assets/...' funziona dalla root. */
  function resolveImg(src) {
    if (!src) return null;
    // Se assoluto (http/data), usalo cosi
    if (/^(https?:|data:)/i.test(src)) return src;
    // Pulisci eventuale '../' iniziale per ricostruire l'URL assoluto
    const clean = src.replace(/^(\.\.\/)+/, '');
    return location.origin + '/' + clean;
  }

  /* Converte un'immagine a dataURL via canvas (necessario per jsPDF).
     Ritorna null se cross-origin/onerror. */
  function imgToDataURL(src) {
    return new Promise((resolve) => {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => {
        try {
          const canvas = document.createElement('canvas');
          // Max 800px lato lungo (file più leggero)
          let { naturalWidth: w, naturalHeight: h } = img;
          if (!w || !h) return resolve(null);
          const MAX = 800;
          if (Math.max(w, h) > MAX) {
            const r = MAX / Math.max(w, h);
            w = Math.round(w * r); h = Math.round(h * r);
          }
          canvas.width = w; canvas.height = h;
          const ctx = canvas.getContext('2d');
          ctx.fillStyle = '#f4f1ea';
          ctx.fillRect(0, 0, w, h);
          ctx.drawImage(img, 0, 0, w, h);
          // SVG cross-origin: drawImage potrebbe taintare il canvas.
          // Proviamo PNG, se fallisce torniamo null.
          try {
            resolve({ data: canvas.toDataURL('image/jpeg', 0.82), w, h });
          } catch (e) {
            resolve(null);
          }
        } catch (e) {
          resolve(null);
        }
      };
      img.onerror = () => resolve(null);
      img.src = src;
    });
  }

  function safeName(s) {
    return (s || '').replace(/[^a-zA-Z0-9-_]+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
  }

  /* Render del PDF con jsPDF "umd" */
  async function buildPDF(info) {
    const { jsPDF } = await loadJsPDF();
    const doc = new jsPDF({ unit: 'mm', format: 'a4', compress: true });
    const W = doc.internal.pageSize.getWidth();   // 210
    const H = doc.internal.pageSize.getHeight();  // 297
    const M = 18;
    let y = M;

    // Header: nome negozio + tagline
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(22);
    doc.setTextColor(14, 15, 14);
    doc.text('MOTOR GARDEN BAZZANA', M, y);
    y += 6;
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(9);
    doc.setTextColor(120, 120, 120);
    doc.text('Cene, Val Seriana · Stihl official dealer · Officina autorizzata', M, y);
    y += 8;
    // Linea decorativa
    doc.setDrawColor(238, 94, 31);
    doc.setLineWidth(1);
    doc.line(M, y, W - M, y);
    y += 10;

    // Box scheda
    doc.setFillColor(244, 241, 234);
    doc.rect(M, y, W - 2 * M, 10, 'F');
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(9);
    doc.setTextColor(238, 94, 31);
    doc.text('SCHEDA PRODOTTO', M + 4, y + 6.5);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(80, 80, 80);
    doc.setFontSize(8);
    const now = new Date();
    const dateStr = now.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit', year: 'numeric' });
    doc.text('Generata il ' + dateStr, W - M - 4, y + 6.5, { align: 'right' });
    y += 16;

    // Layout 2 colonne: immagine sinistra (60mm), testo destra
    const IMG_W = 60;
    const IMG_H = 60;
    const COL_GAP = 8;
    const TXT_X = M + IMG_W + COL_GAP;
    const TXT_W = W - M - TXT_X;
    const yStartContent = y;

    // Immagine
    let imgPlaced = false;
    if (info.img) {
      const url = resolveImg(info.img);
      const data = await imgToDataURL(url);
      if (data && data.data) {
        try {
          // Calcola dimensioni mantenendo l'aspect ratio
          const aspect = data.w / data.h;
          let drawW = IMG_W, drawH = IMG_H;
          if (aspect > 1) drawH = IMG_W / aspect;
          else drawW = IMG_H * aspect;
          const dx = M + (IMG_W - drawW) / 2;
          const dy = y + (IMG_H - drawH) / 2;
          // Sfondo crema
          doc.setFillColor(244, 241, 234);
          doc.rect(M, y, IMG_W, IMG_H, 'F');
          doc.addImage(data.data, 'JPEG', dx, dy, drawW, drawH);
          imgPlaced = true;
        } catch (e) {
          imgPlaced = false;
        }
      }
    }
    if (!imgPlaced) {
      // Placeholder grafico
      doc.setFillColor(244, 241, 234);
      doc.rect(M, y, IMG_W, IMG_H, 'F');
      doc.setTextColor(180, 180, 180);
      doc.setFontSize(8);
      doc.text('Foto in arrivo', M + IMG_W / 2, y + IMG_H / 2, { align: 'center' });
    }

    // Testo a destra
    let ty = y;
    if (info.brand) {
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(8);
      doc.setTextColor(238, 94, 31);
      doc.text((info.brand || '').toUpperCase(), TXT_X, ty);
      ty += 5;
    }
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(18);
    doc.setTextColor(14, 15, 14);
    const titleLines = doc.splitTextToSize(info.model || '', TXT_W);
    titleLines.forEach(line => {
      doc.text(line, TXT_X, ty);
      ty += 7;
    });
    if (info.category) {
      doc.setFont('helvetica', 'italic');
      doc.setFontSize(10);
      doc.setTextColor(80, 80, 80);
      const catLines = doc.splitTextToSize(info.category, TXT_W);
      catLines.forEach(line => { doc.text(line, TXT_X, ty); ty += 5; });
    }
    ty += 2;

    // Garantisci che dopo l'immagine siamo almeno y + IMG_H
    y = Math.max(ty, yStartContent + IMG_H) + 10;

    // Descrizione
    if (info.description) {
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(10);
      doc.setTextColor(14, 15, 14);
      doc.text('Descrizione', M, y);
      y += 5;
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(10);
      doc.setTextColor(60, 60, 60);
      const lines = doc.splitTextToSize(info.description, W - 2 * M);
      lines.forEach(line => {
        if (y > H - 50) { doc.addPage(); y = M; }
        doc.text(line, M, y);
        y += 5;
      });
      y += 4;
    }

    // Specifiche
    if (info.specs && info.specs.length) {
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(10);
      doc.setTextColor(14, 15, 14);
      doc.text('Specifiche tecniche', M, y);
      y += 5;
      // Tabella semplice
      const colA = M;
      const colB = M + 60;
      info.specs.forEach(s => {
        if (y > H - 50) { doc.addPage(); y = M; }
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(9);
        doc.setTextColor(120, 120, 120);
        doc.text(s.label, colA, y);
        doc.setTextColor(14, 15, 14);
        const valLines = doc.splitTextToSize(String(s.value || ''), W - colB - M);
        valLines.forEach((line, i) => {
          doc.text(line, colB, y + i * 4.5);
        });
        y += Math.max(5, valLines.length * 4.5);
      });
      y += 6;
    }

    // Footer fisso in fondo
    const footerY = H - 26;
    doc.setDrawColor(220, 220, 220);
    doc.setLineWidth(0.3);
    doc.line(M, footerY, W - M, footerY);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(10);
    doc.setTextColor(14, 15, 14);
    doc.text('Per disponibilità e prezzo, contattaci:', M, footerY + 6);
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(10);
    doc.setTextColor(60, 60, 60);
    doc.text('Tel/WhatsApp: ' + PHONE_DISPLAY + '   ·   Email: ' + EMAIL, M, footerY + 12);
    doc.text(ADDRESS + '   ·   ' + SITE, M, footerY + 18);

    // Salva
    const filename = 'scheda-' + safeName(info.brand) + '-' + safeName(info.model) + '.pdf';
    doc.save(filename);
    return filename;
  }

  /* Auto-attacca a tutti i bottoni "Chiedi disponibilità":
     - Espliciti: [data-product-cta="pdf"]
     - Impliciti: a[href*="wa.me/393464156981"] che dicono "Chiedi disponibilità"
       (anche dopo che product-pro.js rigenera la struttura)
     I dati prodotto si leggono da data-* sulla pagina o sul bottone stesso. */
  function autoAttach() {
    // Marca anche i bottoni impliciti che hanno il testo "Chiedi disponibilità"
    document.querySelectorAll('a[href*="wa.me/393464156981"]').forEach(a => {
      if (a.dataset.productCta) return;
      const txt = (a.textContent || '').trim().toLowerCase();
      if (txt.includes('chiedi disponibilit') || txt.includes('chiedi sopralluogo')) {
        a.setAttribute('data-product-cta', 'pdf');
      }
    });
    document.querySelectorAll('[data-product-cta="pdf"]').forEach(btn => {
      if (btn.dataset.bznBound === '1') return;
      btn.dataset.bznBound = '1';
      btn.addEventListener('click', async (ev) => {
        ev.preventDefault();
        // Cerca i dati prodotto: prima il bottone, poi un elemento con data-bzn-product
        const host = btn.closest('[data-bzn-product]') || document.querySelector('[data-bzn-product]') || btn;
        const info = {
          brand: host.dataset.brand || btn.dataset.brand || '',
          model: host.dataset.model || btn.dataset.model || '',
          category: host.dataset.category || btn.dataset.category || '',
          description: host.dataset.description || btn.dataset.description || '',
          img: host.dataset.img || btn.dataset.img || '',
          specs: null
        };
        // Specs JSON dentro data-specs
        const specsRaw = host.dataset.specs || btn.dataset.specs;
        if (specsRaw) {
          try { info.specs = JSON.parse(specsRaw); } catch (e) {}
        }
        if (!info.brand && !info.model) {
          // Niente dati: apri WhatsApp e basta
          window.open(btn.href, '_blank', 'noopener');
          return;
        }
        await window.bznGenerateProductPDF(info);
      });
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoAttach);
  } else {
    autoAttach();
  }
  // Riattacca quando la DOM cambia (es. modal aperto)
  if (window.MutationObserver) {
    new MutationObserver(autoAttach).observe(document.body, { childList: true, subtree: true });
  }

  /* API pubblica: genera PDF, apre WhatsApp */
  window.bznGenerateProductPDF = async function (info) {
    try {
      const filename = await buildPDF(info);
      // Apri WhatsApp con messaggio prefilled che chiede di allegare il file
      const msg =
        'Buongiorno, vorrei info su ' + info.brand + ' ' + info.model + '.\n' +
        'Ho scaricato la scheda (' + filename + '), te la allego in chat.';
      const url = 'https://wa.me/393464156981?text=' + encodeURIComponent(msg);
      // Apri in nuova tab così il download principale non viene cancellato
      window.open(url, '_blank', 'noopener');
      return { ok: true, filename };
    } catch (e) {
      console.warn('PDF gen failed', e);
      // Fallback: solo WhatsApp senza PDF
      const msg = 'Buongiorno, vorrei info su ' + info.brand + ' ' + info.model;
      const url = 'https://wa.me/393464156981?text=' + encodeURIComponent(msg);
      window.open(url, '_blank', 'noopener');
      return { ok: false, error: String(e) };
    }
  };
})();
