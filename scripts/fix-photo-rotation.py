"""
Forza la corretta orientazione EXIF per tutte le foto-XXX.jpg in
assets/img/bazzana/. Ri-salva applicando ImageOps.exif_transpose() che
risolve il caso in cui il browser ignora l'header Orientation.

USO: python scripts/fix-photo-rotation.py
"""
import os
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
PHOTOS_DIR = ROOT / "assets" / "img" / "bazzana"

if not PHOTOS_DIR.exists():
    print(f"  Cartella mancante: {PHOTOS_DIR}")
    sys.exit(1)

files = sorted(PHOTOS_DIR.glob("foto-*.jpg"))
print(f"Totale foto: {len(files)}")

fixed = 0
skipped_no_exif = 0
errors = 0

for f in files:
    try:
        img = Image.open(f)
        exif = img.getexif() if hasattr(img, "getexif") else None
        # Codice tag Orientation = 274
        orientation = exif.get(274) if exif else None

        if orientation in (3, 6, 8):
            transposed = ImageOps.exif_transpose(img)
            # Rimuovi l'header EXIF dopo la trasposizione (altrimenti
            # alcuni browser ri-applicano la rotazione)
            if transposed.mode != "RGB":
                transposed = transposed.convert("RGB")
            transposed.save(f, "JPEG", quality=82, optimize=True, progressive=True)
            fixed += 1
            print(f"  fixed (orient={orientation}): {f.name}")
        else:
            skipped_no_exif += 1
    except Exception as e:
        errors += 1
        print(f"  ERROR {f.name}: {e}")

print(f"\nFatto. Fissate: {fixed}  Saltate: {skipped_no_exif}  Errori: {errors}")
