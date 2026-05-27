#!/usr/bin/env python3
"""Ottimizza foto Bazzana per il web.
- Selezione: prende ~30 foto distanziate (1 ogni 8 per ridurre duplicati visivi)
- Resize: max 1800px lato lungo
- EXIF orientation: corregge la rotazione del telefono
- Compress: JPEG q=82
- Output: assets/img/bazzana/scena-NN.jpg
"""
import os
from pathlib import Path
from PIL import Image, ImageOps

SOURCE = Path("C:/Users/ilbug/Desktop/scuola/gestione/foto bazzana")
DEST = Path(os.path.dirname(__file__)).parent / "assets" / "img" / "bazzana"
DEST.mkdir(parents=True, exist_ok=True)

# Prendi tutte le JPG e seleziona con step
files = sorted([f for f in SOURCE.iterdir() if f.suffix.lower() in {".jpg", ".jpeg"}])
print(f"Totale source: {len(files)}")

# Step ~8 → ~30 immagini
STEP = max(1, len(files) // 30)
selected = files[::STEP][:32]
print(f"Selezionate: {len(selected)}")

MAX_SIDE = 1800
QUALITY = 82

for i, src in enumerate(selected, start=1):
    try:
        img = Image.open(src)
        # Applica orientation EXIF
        img = ImageOps.exif_transpose(img)
        # Resize
        w, h = img.size
        if max(w, h) > MAX_SIDE:
            if w >= h:
                new_w = MAX_SIDE
                new_h = int(h * MAX_SIDE / w)
            else:
                new_h = MAX_SIDE
                new_w = int(w * MAX_SIDE / h)
            img = img.resize((new_w, new_h), Image.LANCZOS)
        # RGB only (no alpha)
        if img.mode != "RGB":
            img = img.convert("RGB")
        # Save
        out = DEST / f"scena-{i:02d}.jpg"
        img.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        print(f"  {out.name}  {img.size}  {out.stat().st_size // 1024} KB")
    except Exception as e:
        print(f"  ERROR {src.name}: {e}")

print(f"\nDone. Output: {DEST}")
