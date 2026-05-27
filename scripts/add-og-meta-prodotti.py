#!/usr/bin/env python3
"""Aggiunge og:image specifico per ogni pagina prodotto.
Per ogni file prodotti/*.html: estrae product image src, costruisce og:* meta tags.
"""
import os
import re
from pathlib import Path

ROOT = Path(os.path.dirname(__file__)).parent
PROD_DIR = ROOT / 'prodotti'

for path in sorted(PROD_DIR.glob('*.html')):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'property="og:image"' in c:
        continue
    title = re.search(r'<title>([^<]+)</title>', c)
    desc = re.search(r'<meta name="description" content="([^"]+)"', c)
    # Trova primo img in product__media
    img = re.search(r'<img src="([^"]+)"[^>]*>', c)
    if not title or not desc or not img:
        print(f'SKIP {path.name} — missing title/desc/img')
        continue
    img_path = img.group(1).replace('../', '')
    img_url = f'https://www.motorgardenbazzana.it/{img_path}'
    og_block = f'''
<meta property="og:type" content="product" />
<meta property="og:title" content="{title.group(1)}" />
<meta property="og:description" content="{desc.group(1)}" />
<meta property="og:image" content="{img_url}" />
<meta property="og:locale" content="it_IT" />
<link rel="canonical" href="https://www.motorgardenbazzana.it/prodotti/{path.name}" />
'''
    # Inserisci dopo theme-color o prima del prossimo <link>
    if 'theme-color' in c:
        c = re.sub(
            r'(<meta name="theme-color" content="[^"]+" />)',
            r'\1' + og_block,
            c,
            count=1
        )
    else:
        c = c.replace('<link rel="icon"', og_block + '<link rel="icon"', 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'OK {path.name}')

print('done')
