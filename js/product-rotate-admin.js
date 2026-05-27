/* =========================================================
   PRODUCT ROTATE ADMIN — su qualsiasi pagina prodotto con ?admin=1
   compare un piccolo pannello in alto a destra per testare al volo
   la rotazione dell'immagine principale e copiare il codice di rotazione
   da applicare al file (server-side).

   Output console: comando Python per ruotare il file in modo permanente.
   ========================================================= */
(() => {
  'use strict';
  const isAdmin = new URLSearchParams(location.search).get('admin') === '1';
  if (!isAdmin) return;

  function findHeroImg() {
    return (
      document.querySelector('.product-pro__hero img') ||
      document.querySelector('.product__media img') ||
      document.querySelector('.generic-detail__media img') ||
      document.querySelector('main img')
    );
  }

  function init() {
    const img = findHeroImg();
    if (!img) return;

    // Stato locale
    let rot = 0;

    // Pannello floating
    const panel = document.createElement('div');
    panel.style.cssText = `
      position: fixed; top: 100px; right: 16px; z-index: 100000;
      background: rgba(14, 15, 14, 0.92); color: #f4f1ea;
      padding: 12px 14px; border-radius: 12px;
      font-family: 'JetBrains Mono', monospace; font-size: 12px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.4);
      display: flex; flex-direction: column; gap: 8px; min-width: 230px;
      border: 1px solid rgba(238, 94, 31, 0.4);
    `;
    panel.innerHTML = `
      <div style="font-weight:600;color:#ee5e1f;letter-spacing:0.06em;">ADMIN: ROTAZIONE FOTO</div>
      <div id="rot-info" style="font-size:11px;opacity:0.7;line-height:1.4;"></div>
      <div style="display:flex;gap:6px;">
        <button id="rot-left" style="flex:1;background:#ee5e1f;border:none;color:#fff;padding:8px;border-radius:6px;cursor:pointer;font-weight:600;">↺ -90°</button>
        <button id="rot-right" style="flex:1;background:#ee5e1f;border:none;color:#fff;padding:8px;border-radius:6px;cursor:pointer;font-weight:600;">+90° ↻</button>
      </div>
      <button id="rot-flip" style="background:#444;border:none;color:#fff;padding:8px;border-radius:6px;cursor:pointer;">↕ Capovolgi 180°</button>
      <button id="rot-reset" style="background:transparent;border:1px solid #555;color:#aaa;padding:6px;border-radius:6px;cursor:pointer;font-size:11px;">Reset</button>
      <pre id="rot-cmd" style="background:#0a0b0a;padding:8px;border-radius:6px;font-size:10px;color:#9bf3a4;overflow:auto;max-width:100%;white-space:pre-wrap;display:none;"></pre>
      <button id="rot-copy" style="background:#9bf3a4;color:#0a0b0a;border:none;padding:6px;border-radius:6px;cursor:pointer;font-weight:600;display:none;">Copia comando Python</button>
    `;
    document.body.appendChild(panel);

    const info = panel.querySelector('#rot-info');
    const cmdEl = panel.querySelector('#rot-cmd');
    const copyBtn = panel.querySelector('#rot-copy');

    function updateRot() {
      img.style.transformOrigin = 'center center';
      img.style.transform = rot ? `rotate(${rot}deg)` : '';

      const src = img.getAttribute('src') || '';
      // Risali al .jpg sorgente partendo dal .webp se necessario
      const srcJpg = src.replace(/\.webp(\?|$)/, '.jpg$1');
      info.innerHTML =
        'File: <span style="color:#fff">' + srcJpg.split('/').pop() + '</span><br>' +
        'Rotazione: <span style="color:#ee5e1f;font-weight:600;">' + rot + '°</span>';

      if (rot === 0) {
        cmdEl.style.display = 'none';
        copyBtn.style.display = 'none';
      } else {
        // Calcola la trasposizione PIL equivalente
        // PIL: ROTATE_90=90deg CCW, ROTATE_180=180deg, ROTATE_270=90deg CW
        const map = { 90: 'ROTATE_270', '-90': 'ROTATE_90', 180: 'ROTATE_180', '-180': 'ROTATE_180', 270: 'ROTATE_90', '-270': 'ROTATE_270' };
        const norm = ((rot % 360) + 360) % 360; // 0..359
        const pilCode = { 90: 'ROTATE_270', 180: 'ROTATE_180', 270: 'ROTATE_90' }[norm] || 'ROTATE_180';
        const relPath = srcJpg.replace(location.origin + '/', '').replace(/^\//, '');
        const cmd =
          'python -c "' +
          'from PIL import Image; from pathlib import Path; ' +
          "p=Path('" + relPath + "'); " +
          'img=Image.open(p).convert(\\"RGB\\"); ' +
          'rot=img.transpose(Image.' + pilCode + '); ' +
          'rot.save(p, \\"JPEG\\", quality=85, optimize=True, progressive=True, exif=b\\"\\"); ' +
          'rot.save(p.with_suffix(\\".webp\\"), \\"WEBP\\", quality=85, method=6); ' +
          "print('done')\"";
        cmdEl.textContent = cmd;
        cmdEl.style.display = 'block';
        copyBtn.style.display = 'block';
      }
    }

    panel.querySelector('#rot-left').onclick = () => { rot = (rot - 90) % 360; updateRot(); };
    panel.querySelector('#rot-right').onclick = () => { rot = (rot + 90) % 360; updateRot(); };
    panel.querySelector('#rot-flip').onclick = () => { rot = (rot + 180) % 360; updateRot(); };
    panel.querySelector('#rot-reset').onclick = () => { rot = 0; updateRot(); };
    copyBtn.onclick = async () => {
      try {
        await navigator.clipboard.writeText(cmdEl.textContent);
        copyBtn.textContent = '✓ Copiato!';
        setTimeout(() => { copyBtn.textContent = 'Copia comando Python'; }, 1500);
      } catch (e) {
        // Fallback: select
        const r = document.createRange(); r.selectNodeContents(cmdEl);
        const sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
      }
    };

    updateRot();
  }

  // Ritarda per essere sicuri che product-pro.js abbia rigenerato la struttura
  if (document.readyState === 'complete') {
    setTimeout(init, 200);
  } else {
    window.addEventListener('load', () => setTimeout(init, 200));
  }
})();
