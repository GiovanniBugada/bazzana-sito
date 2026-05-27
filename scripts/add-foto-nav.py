#!/usr/bin/env python3
"""Aggiunge 'Foto' al nav + menu-overlay su tutte le pagine HTML.
Bumpa anche CSS cache version a v=42.
"""
import os
import re
from pathlib import Path

ROOT = Path(os.path.dirname(__file__)).parent

for path in ROOT.rglob('*.html'):
    if '.git' in str(path) or '.claude' in str(path) or 'scripts' in str(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c

    # Bump CSS
    c = re.sub(r'main\.css\?v=4[01]', 'main.css?v=42', c)
    c = re.sub(r'main\.css\?v=3\d', 'main.css?v=42', c)

    # Prefix: product pages use ../
    in_prodotti = path.parent.name == 'prodotti'
    prefix = '../' if in_prodotti else ''

    if 'foto.html' not in c:
        # nav main
        pattern_nav = (
            r'(<a href="' + re.escape(prefix) + r'prodotti\.html"[^>]*>Prodotti</a>)\s*'
            r'(<a href="' + re.escape(prefix) + r'storia\.html")'
        )
        c = re.sub(pattern_nav, r'\1\n      <a href="' + prefix + r'foto.html">Foto</a>\n      \2', c)

        # menu-overlay
        pattern_menu = (
            r'(<a href="' + re.escape(prefix) + r'prodotti\.html">Prodotti</a>)\s*'
            r'(<a href="' + re.escape(prefix) + r'storia\.html">Storia</a>)'
        )
        c = re.sub(pattern_menu, r'\1\n    <a href="' + prefix + r'foto.html">Foto</a>\n    \2', c)

    if c != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(path)

print('done')
