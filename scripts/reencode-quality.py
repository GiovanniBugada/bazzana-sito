"""
Ricomprime le foto bazzana a qualità migliore (q=88 invece di q=82)
con chroma subsampling 4:4:4 per ridurre artefatti su dettagli colorati.
Genera anche WebP companion q=85 per dare browser moderni.
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent

# Cartelle da ricompressare con qualità migliore
TARGETS = [
    ROOT / 'assets' / 'img' / 'bazzana',
    ROOT / 'assets' / 'img' / 'hero',
    ROOT / 'assets' / 'img' / 'storia',
    ROOT / 'assets' / 'img' / 'officina',
    ROOT / 'assets' / 'img' / 'ambiente',
    ROOT / 'assets' / 'img' / 'note',
]

JPG_QUALITY = 88
WEBP_QUALITY = 85
MAX_DIM = 1600

def safe_print(*a):
    try: print(*a)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((' '.join(str(x) for x in a)).encode('utf-8', 'replace') + b'\n')

processed = 0
saved_kb = 0

for folder in TARGETS:
    if not folder.exists():
        continue
    for p in folder.rglob('*.jpg'):
        if p.name.startswith('_'): continue
        size_before = p.stat().st_size
        try:
            img = Image.open(p)
            img = ImageOps.exif_transpose(img)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            w, h = img.size
            m = max(w, h)
            if m > MAX_DIM:
                scale = MAX_DIM / m
                img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
            # subsampling=0 = 4:4:4 (no chroma sub) = no artefatti su rossi/verdi
            img.save(p, 'JPEG', quality=JPG_QUALITY, optimize=True, progressive=True, subsampling=0)
            # WebP companion
            webp = p.with_suffix('.webp')
            img.save(webp, 'WEBP', quality=WEBP_QUALITY, method=5)
            size_after = p.stat().st_size
            processed += 1
            saved_kb += (size_before - size_after) // 1024
        except Exception as e:
            safe_print(f'  [ERR] {p.name}: {e}')

safe_print(f'\n=== Ricompresso {processed} JPG con qualità migliore (q={JPG_QUALITY}, 4:4:4) ===')
safe_print(f'Saved: {saved_kb} KB totali')
