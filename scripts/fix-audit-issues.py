#!/usr/bin/env python3
"""Applica tutti i fix degli audit:
1. Versioni JS allineate su foto.html
2. Rimozione console.log da catalog-pro.js
3. og:image + og:title + og:description su pagine senza
4. aria-label mancanti
5. canonical su 404.html
6. Cancella 5 CSS orphan files
"""
import os
import re
from pathlib import Path

ROOT = Path(os.path.dirname(__file__)).parent

# === FIX 1: Versioni JS in foto.html ===
foto = ROOT / 'foto.html'
c = foto.read_text(encoding='utf-8')
c = c.replace('site-fx.js?v=43', 'site-fx.js?v=45')
c = c.replace('awwwards.js?v=42', 'awwwards.js?v=45')
c = c.replace('wow-fx.js?v=42', 'wow-fx.js?v=45')
c = c.replace('extras.js?v=42', 'extras.js?v=45')
c = c.replace('foto-manifest.js?v=42', 'foto-manifest.js?v=45')
c = c.replace('foto-gallery.js?v=42', 'foto-gallery.js?v=45')
foto.write_text(c, encoding='utf-8')
print('FIX 1: foto.html versioni JS allineate')

# === FIX 2: Rimuovi console.log da catalog-pro.js ===
catalog_pro = ROOT / 'js' / 'catalog-pro.js'
if catalog_pro.exists():
    c = catalog_pro.read_text(encoding='utf-8')
    # Rimuovi tutto il blocco if-console-log finale
    c = re.sub(
        r'\s*if \(window\.console\) \{\s*\n\s*console\.log\(.*?\n\s*\}',
        '',
        c,
        flags=re.DOTALL
    )
    catalog_pro.write_text(c, encoding='utf-8')
    print('FIX 2: console.log rimosso da catalog-pro.js')

# === FIX 3: og:image + og: meta su pagine senza ===
OG_TEMPLATE = '''
<meta property="og:type" content="website" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:image" content="https://www.motorgardenbazzana.it/assets/img/hero/facciata-esterna-rossa.jpg" />
<meta property="og:locale" content="it_IT" />
'''

pages_to_fix_og = ['contatti.html', 'officina.html', 'prodotti.html', 'foto.html', 'storia.html', 'privacy.html']
for page in pages_to_fix_og:
    p = ROOT / page
    if not p.exists():
        continue
    c = p.read_text(encoding='utf-8')
    if 'property="og:image"' in c:
        continue
    # Estrai title + description
    title = re.search(r'<title>([^<]+)</title>', c)
    desc = re.search(r'<meta name="description" content="([^"]+)"', c)
    if not title or not desc:
        continue
    og = OG_TEMPLATE.format(title=title.group(1), description=desc.group(1))
    # Inserisci PRIMA del canonical o del primo link
    c = c.replace('<link rel="canonical"', og + '<link rel="canonical"', 1)
    p.write_text(c, encoding='utf-8')
    print(f'FIX 3: og: meta aggiunte a {page}')

# === FIX 4: aria-label mancanti su storia + contatti ===
# storia.html
storia = ROOT / 'storia.html'
c = storia.read_text(encoding='utf-8')
c = c.replace('<nav class="nav">\n', '<nav class="nav" aria-label="Navigazione principale">\n', 1)
c = c.replace('<button class="menu-toggle"><span></span></button>', '<button class="menu-toggle" aria-label="Apri menu"><span></span></button>')
c = c.replace('<button class="menu-overlay__close">×</button>', '<button class="menu-overlay__close" aria-label="Chiudi menu">×</button>')
storia.write_text(c, encoding='utf-8')
print('FIX 4a: aria-label su storia.html')

# contatti.html
contatti = ROOT / 'contatti.html'
c = contatti.read_text(encoding='utf-8')
c = c.replace('<button class="menu-toggle"><span></span></button>', '<button class="menu-toggle" aria-label="Apri menu"><span></span></button>')
c = c.replace('<button class="menu-overlay__close">×</button>', '<button class="menu-overlay__close" aria-label="Chiudi menu">×</button>')
contatti.write_text(c, encoding='utf-8')
print('FIX 4b: aria-label su contatti.html')

# === FIX 5: canonical su 404.html ===
fourohfour = ROOT / '404.html'
c = fourohfour.read_text(encoding='utf-8')
if 'rel="canonical"' not in c:
    c = c.replace(
        '<meta name="robots" content="noindex" />',
        '<meta name="robots" content="noindex" />\n<link rel="canonical" href="https://www.motorgardenbazzana.it/404.html" />'
    )
    fourohfour.write_text(c, encoding='utf-8')
    print('FIX 5: canonical su 404.html')

# === FIX 6: Cancella 5 CSS orphan files ===
orphans = ['density-fix.css', 'minimal-pass.css', 'calm-pass.css', 'stripped.css', 'final.css']
deleted = 0
for f in orphans:
    p = ROOT / 'css' / 'pages' / f
    if p.exists():
        p.unlink()
        deleted += 1
print(f'FIX 6: {deleted} CSS orphan files eliminati')

print('\nTutti i fix applicati.')
