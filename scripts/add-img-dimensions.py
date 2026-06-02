"""Aggiunge width e height alle <img> che ne sono prive,
leggendo le dimensioni native del file su disco. Previene CLS."""
import re, glob, os
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

# Cache dimensioni
cache = {}
def get_dims(src):
    if src.startswith(('http://', 'https://', 'data:')):
        return None
    if src in cache: return cache[src]
    # Risolvi path
    path = src
    if path.startswith('/'): path = path[1:]
    full = ROOT / path
    if not full.exists():
        cache[src] = None
        return None
    try:
        with Image.open(full) as img:
            cache[src] = img.size
            return img.size
    except Exception:
        cache[src] = None
        return None

# Pattern: <img ... src="X" ...> SENZA width/height
IMG_RE = re.compile(r'<img\b([^>]*?)>', re.I)
SRC_RE = re.compile(r'src="([^"]+)"')

def fix_img(m):
    attrs = m.group(1)
    if 'width=' in attrs or 'height=' in attrs:
        return m.group(0)
    src_m = SRC_RE.search(attrs)
    if not src_m: return m.group(0)
    src = src_m.group(1)
    # Risolvi path relativo: se è ../ o assoluto
    test_src = src
    if test_src.startswith('../'):
        # Per subfolder HTML
        test_src = test_src[3:]
    dims = get_dims(test_src)
    if not dims:
        return m.group(0)
    w, h = dims
    new_attrs = attrs.rstrip() + f' width="{w}" height="{h}"'
    return f'<img{new_attrs}>'

files = list(ROOT.glob('*.html')) + list((ROOT / 'prodotti').glob('*.html')) + list((ROOT / 'note').glob('*.html'))
total = 0
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f: s = f.read()
    orig = s
    s = IMG_RE.sub(fix_img, s)
    if s != orig:
        with open(fp, 'w', encoding='utf-8') as f: f.write(s)
        diff = s.count(' width="') - orig.count(' width="')
        total += diff
        print(f'  [OK] {fp.relative_to(ROOT)}: +{diff} dimensions')

print(f'\nTotale: +{total} width/height aggiunti')
