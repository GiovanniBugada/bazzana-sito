"""
Comprime aggressivamente solo le foto-catalogo (488 PNG/JPG) per ridurre lag prodotti.html.
- Le card del catalog sono renderizzate a ~165px wide su mobile, ~250px desktop
- PNG con alpha (foto isolate prodotti): resize max 600px + palette quantize
- WebP companion ricreato con qualita' 75
NON tocca altre immagini (hero/officina/storia restano alta qualita').
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
CAT = ROOT / 'assets' / 'img' / 'prodotti' / 'foto-catalogo'

MAX_DIM = 700      # le card sono ~165-250px wide, 700px e' gia' generoso per retina
PNG_THRESH = 80_000  # comprimi solo PNG > 80KB
WEBP_QUALITY = 75
processed = 0
saved = 0
errors = 0

def safe_print(*a, **kw):
    try:
        print(*a, **kw)
    except UnicodeEncodeError:
        msg = ' '.join(str(x) for x in a)
        sys.stdout.buffer.write(msg.encode('utf-8', 'replace') + b'\n')

for p in CAT.rglob('*.*'):
    if p.suffix.lower() not in {'.png', '.jpg', '.jpeg'}:
        continue
    size_before = p.stat().st_size
    if size_before < PNG_THRESH:
        continue
    try:
        img = Image.open(p)
        img = ImageOps.exif_transpose(img)
        is_png_alpha = (p.suffix.lower() == '.png' and img.mode in ('RGBA', 'LA', 'P'))

        # Resize a max 700px
        w, h = img.size
        m = max(w, h)
        if m > MAX_DIM:
            scale = MAX_DIM / m
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

        if is_png_alpha:
            # Mantieni PNG ma quantize per ridurre dimensione
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode == 'LA':
                img = img.convert('RGBA')
            # Quantize a 256 colori mantenendo alpha
            # Per i prodotti isolati su sfondo trasparente, 128 colori sono sufficienti
            try:
                # Pillow >= 9: quantize with alpha
                img_q = img.quantize(colors=192, method=Image.MEDIANCUT)
                img_q.save(p, 'PNG', optimize=True, compress_level=9)
                # Genera anche WebP companion
                webp_path = p.with_suffix('.webp')
                img.save(webp_path, 'WEBP', quality=WEBP_QUALITY, method=4)
            except Exception:
                # Fallback: salva con palette
                img.save(p, 'PNG', optimize=True, compress_level=9)
        else:
            # JPG: ricomprimi q=82
            img = img.convert('RGB')
            img.save(p, 'JPEG', quality=82, optimize=True, progressive=True)
            webp_path = p.with_suffix('.webp')
            img.save(webp_path, 'WEBP', quality=WEBP_QUALITY, method=4)

        size_after = p.stat().st_size
        diff = size_before - size_after
        saved += diff
        processed += 1
        safe_print(f'  [OK] {p.name:30s} {size_before/1000:5.0f}KB -> {size_after/1000:5.0f}KB ({diff/1000:+.0f})')
    except Exception as e:
        errors += 1
        safe_print(f'  [ERR] {p.name}: {e}')

safe_print(f'\n=== Done ===')
safe_print(f'Processed: {processed}, Errors: {errors}')
safe_print(f'Saved: {saved/1_000_000:.1f} MB')
