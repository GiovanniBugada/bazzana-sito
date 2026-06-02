"""
Comprime tutte le immagini > 500KB:
- JPG: resize max 1600px + q=82 + progressive + WebP companion
- PNG con grossi sfondi: convertire in JPG (perdita alpha accettata per foto prodotto)
Sovrascrive in-place.
"""
import os, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

MAX_DIM = 1600
JPG_QUALITY = 82
WEBP_QUALITY = 80
TARGET_KB = 500

savings = 0
processed = 0
errors = 0

def safe_print(*a, **kw):
    try:
        print(*a, **kw)
    except UnicodeEncodeError:
        msg = ' '.join(str(x) for x in a)
        sys.stdout.buffer.write(msg.encode('utf-8', 'replace') + b'\n')

for p in Path('assets/img').rglob('*.*'):
    if p.suffix.lower() not in {'.jpg', '.jpeg', '.png'}:
        continue
    size_before = p.stat().st_size
    if size_before < TARGET_KB * 1024:
        continue

    try:
        img = Image.open(p)
        # Rotazione EXIF se serve
        img = ImageOps.exif_transpose(img)
        is_png_with_alpha = (p.suffix.lower() == '.png' and img.mode in ('RGBA', 'LA'))
        # PNG nelle foto-catalogo: hanno alpha (PNG isolate) -> manteniamo PNG con compress, NO conversione
        # PNG altrove: convertiamo in JPG perché sono foto
        keep_png = is_png_with_alpha and 'foto-catalogo' in str(p)

        if img.mode == 'RGBA' and not keep_png:
            # Flatten su bianco
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        elif img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')

        # Resize se necessario
        w, h = img.size
        m = max(w, h)
        if m > MAX_DIM:
            scale = MAX_DIM / m
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

        if keep_png:
            # PNG con alpha: ricomprimi PNG (compress_level 9)
            img.save(p, 'PNG', optimize=True, compress_level=9)
        else:
            # Sostituisci eventuale .png con .jpg
            if p.suffix.lower() == '.png':
                new_path = p.with_suffix('.jpg')
                img.save(new_path, 'JPEG', quality=JPG_QUALITY, optimize=True, progressive=True)
                # NON cancello l'originale .png perché potrebbe essere referenziato
                # Lo lascio (verrà sovrascritto dal browser preferendo .webp comunque)
                p_after = new_path
            else:
                img.save(p, 'JPEG', quality=JPG_QUALITY, optimize=True, progressive=True)
                p_after = p
            # WebP companion
            webp_path = p_after.with_suffix('.webp')
            try:
                img.save(webp_path, 'WEBP', quality=WEBP_QUALITY, method=4)
            except Exception:
                pass

        size_after = p.stat().st_size if p.exists() else 0
        if 'foto-catalogo' not in str(p) and p.suffix.lower() == '.png':
            # Convertito a jpg, size after dal jpg
            jpg_p = p.with_suffix('.jpg')
            if jpg_p.exists():
                size_after = jpg_p.stat().st_size
        savings += (size_before - size_after) if size_after > 0 else 0
        processed += 1
        safe_print(f'  [OK] {p.name:45s} {size_before/1000:6.0f}KB -> {size_after/1000:6.0f}KB')
    except Exception as e:
        errors += 1
        safe_print(f'  [ERR] {p.name}: {e}')

safe_print(f'\n=== Done ===')
safe_print(f'Processed: {processed}, Errors: {errors}')
safe_print(f'Saved: {savings/1_000_000:.1f} MB')
