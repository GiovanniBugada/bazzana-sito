#!/usr/bin/env python3
"""Rewrite the <footer class="site-footer">...</footer> block on every HTML page
with a new Awwwards-tier markup. Preserves the per-page wordmark text.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

NEW_TEMPLATE = '''<footer class="site-footer">

  <!-- 1 · KINETIC TAGLINE STRIP -->
  <div class="site-footer__strip" aria-hidden="true">
    <div class="site-footer__strip-track">
      <span>Stihl official dealer</span><span class="site-footer__strip-dot"></span>
      <span>Officina autorizzata</span><span class="site-footer__strip-dot"></span>
      <span>Ricambi originali in 48h</span><span class="site-footer__strip-dot"></span>
      <span>Cene · Val Seriana</span><span class="site-footer__strip-dot"></span>
      <span>Aperti 2026 · esperienza decennale</span><span class="site-footer__strip-dot"></span>
      <span>Stihl · Honda · Active · Echo · Oleo-Mac · Kress · Ligier</span><span class="site-footer__strip-dot"></span>
      <span>Stihl official dealer</span><span class="site-footer__strip-dot"></span>
      <span>Officina autorizzata</span><span class="site-footer__strip-dot"></span>
      <span>Ricambi originali in 48h</span><span class="site-footer__strip-dot"></span>
      <span>Cene · Val Seriana</span><span class="site-footer__strip-dot"></span>
      <span>Aperti 2026 · esperienza decennale</span><span class="site-footer__strip-dot"></span>
      <span>Stihl · Honda · Active · Echo · Oleo-Mac · Kress · Ligier</span><span class="site-footer__strip-dot"></span>
    </div>
  </div>

  <div class="site-footer__inner">

    <!-- 2 · MAIN GRID -->
    <div class="site-footer__main">
      <div class="site-footer__brand">
        <a class="site-footer__brand-mark" href="{PREFIX}index.html" aria-label="Motor Garden Bazzana — Home">
          <img src="{PREFIX}assets/brand/logo-bazzana.png" alt="Motor Garden Bazzana" width="200" height="68" loading="lazy">
        </a>
        <p class="site-footer__motto">
          Cene, valle Seriana.<br>
          <em>Aperti 2026 — esperienza decennale.</em>
        </p>
        <ul class="site-footer__social" aria-label="Social e contatti rapidi">
          <li><a href="https://wa.me/393464156981?text=Ciao%21%20Vorrei%20info%20su%20Motor%20Garden%20Bazzana" target="_blank" rel="noopener" aria-label="WhatsApp">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19.05 4.91A9.82 9.82 0 0 0 12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01zM12.04 20.15c-1.48 0-2.93-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.26 8.26 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.24-8.24 2.2 0 4.27.86 5.82 2.42a8.18 8.18 0 0 1 2.41 5.83c.02 4.54-3.68 8.23-8.22 8.23z"/></svg>
          </a></li>
          <li><a href="https://www.instagram.com/bazzanamotorgarden/" target="_blank" rel="noopener" aria-label="Instagram">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
          </a></li>
          <li><a href="tel:+393464156981" aria-label="Telefono">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          </a></li>
          <li><a href="mailto:bazzanamotorgarden@gmail.com" aria-label="Email">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="2 6 12 13 22 6"/></svg>
          </a></li>
        </ul>
      </div>

      <nav class="site-footer__col" aria-label="Naviga">
        <h4 class="site-footer__h">Naviga</h4>
        <ul>
          <li><a href="{PREFIX}officina.html">Officina<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
          <li><a href="{PREFIX}prodotti.html">Prodotti<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
          <li><a href="{PREFIX}storia.html">Storia<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
          <li><a href="{PREFIX}contatti.html">Contatti<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
        </ul>
      </nav>

      <div class="site-footer__col">
        <h4 class="site-footer__h">Contatti</h4>
        <ul>
          <li><a href="tel:+393464156981">+39 346 4156981</a></li>
          <li><a href="https://wa.me/393464156981" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="mailto:bazzanamotorgarden@gmail.com">bazzanamotorgarden@gmail.com</a></li>
          <li><a href="https://www.instagram.com/bazzanamotorgarden/" target="_blank" rel="noopener">@bazzanamotorgarden</a></li>
        </ul>
      </div>

      <div class="site-footer__col site-footer__col--find">
        <h4 class="site-footer__h">Trovaci</h4>
        <address class="site-footer__addr">
          Via U. Bellora, 73<br>
          24020 Cene (BG)<br>
          Italia
        </address>
        <dl class="site-footer__hours">
          <dt>Lun-Ven</dt><dd>07:45-12:00 · 13:30-19:15</dd>
          <dt>Sabato</dt><dd>07:45-16:00</dd>
          <dt>Domenica</dt><dd>Chiuso</dd>
        </dl>
      </div>
    </div>

    <!-- 3 · KINETIC WORDMARK -->
    <div class="site-footer__kinetic" aria-hidden="true">
      <div class="site-footer__kinetic-track">
        <span class="site-footer__kinetic-word">{WORDMARK}</span>
        <span class="site-footer__kinetic-sep">·</span>
        <span class="site-footer__kinetic-sub">Motor Garden</span>
        <span class="site-footer__kinetic-sep">·</span>
        <span class="site-footer__kinetic-word">{WORDMARK}</span>
        <span class="site-footer__kinetic-sep">·</span>
        <span class="site-footer__kinetic-sub">Cene · Val Seriana</span>
        <span class="site-footer__kinetic-sep">·</span>
        <span class="site-footer__kinetic-word">{WORDMARK}</span>
        <span class="site-footer__kinetic-sep">·</span>
        <span class="site-footer__kinetic-sub">Bazzana</span>
        <span class="site-footer__kinetic-sep">·</span>
      </div>
    </div>

    <!-- 4 · BOTTOM STRIP -->
    <div class="site-footer__bottom">
      <div class="site-footer__bottom-left">
        <span class="site-footer__copy">© <span data-year>2026</span> Motor Garden Bazzana</span>
        <span class="site-footer__sep" aria-hidden="true">·</span>
        <span>P.IVA 02234180169</span>
      </div>
      <nav class="site-footer__legal" aria-label="Legal">
        <a href="{PREFIX}privacy.html">Privacy</a>
        <a href="{PREFIX}index.html">Home</a>
      </nav>
      <span class="site-footer__credit">Cene · BG · Italia</span>
    </div>
  </div>
</footer>'''


FOOTER_PATTERN = re.compile(
    r'<footer class="site-footer">.*?</footer>',
    re.DOTALL
)
WORDMARK_PATTERN = re.compile(
    r'<div class="site-footer__wordmark">([^<]+)</div>'
)


def process(path, prefix):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    m = FOOTER_PATTERN.search(content)
    if not m:
        return False, 'no footer'

    old = m.group(0)
    wm = WORDMARK_PATTERN.search(old)
    wordmark = wm.group(1).strip() if wm else 'BAZZANA'

    new = NEW_TEMPLATE.replace('{PREFIX}', prefix).replace('{WORDMARK}', wordmark)
    content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True, wordmark


def main():
    targets = []
    # Root pages
    for fn in ['index.html', 'officina.html', 'storia.html', 'contatti.html',
               'prodotti.html', 'privacy.html', '404.html']:
        full = os.path.join(ROOT, fn)
        if os.path.exists(full):
            targets.append((full, ''))
    # Product pages
    prod_dir = os.path.join(ROOT, 'prodotti')
    if os.path.isdir(prod_dir):
        for fn in sorted(os.listdir(prod_dir)):
            if fn.endswith('.html'):
                targets.append((os.path.join(prod_dir, fn), '../'))

    for path, prefix in targets:
        ok, info = process(path, prefix)
        rel = os.path.relpath(path, ROOT)
        print(f'{rel:50s} prefix={prefix!r:6s} wm={info}')


if __name__ == '__main__':
    main()
