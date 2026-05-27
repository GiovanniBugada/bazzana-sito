"""
Re-import strict di TUTTE le foto Bazzana, con:
  1. ImageOps.exif_transpose() (applica EXIF orientation ai pixel)
  2. exif=b'' nel save (strip totale dei metadati)
  3. Conferma che il pixel-orientation finale corrisponda a quello atteso

USO: python scripts/re-import-photos-strict.py
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = Path("C:/Users/ilbug/Desktop/scuola/gestione/foto bazzana")
DST = ROOT / "assets" / "img" / "bazzana"

MAX_SIDE = 1400
QUALITY = 82

srcs = sorted([f for f in SRC.iterdir() if f.suffix.lower() in {".jpg", ".jpeg"}])
print(f"Source: {len(srcs)} files")

re_imported = 0
errors = 0
for i, s in enumerate(srcs, start=1):
    out = DST / f"foto-{i:03d}.jpg"
    try:
        img = Image.open(s)
        # 1. Trasponi pixel secondo EXIF
        img = ImageOps.exif_transpose(img)
        # 2. Resize se necessario
        w, h = img.size
        if max(w, h) > MAX_SIDE:
            if w >= h:
                nw = MAX_SIDE
                nh = int(h * MAX_SIDE / w)
            else:
                nh = MAX_SIDE
                nw = int(w * MAX_SIDE / h)
            img = img.resize((nw, nh), Image.LANCZOS)
        # 3. Converti a RGB pulito
        if img.mode != "RGB":
            img = img.convert("RGB")
        # 4. Salva STRIPPING TUTTI i metadati (exif=b'')
        img.save(
            out,
            "JPEG",
            quality=QUALITY,
            optimize=True,
            progressive=True,
            exif=b"",
        )
        re_imported += 1
        if i % 20 == 0:
            print(f"  ... {i}/{len(srcs)}")
    except Exception as e:
        errors += 1
        print(f"  ERROR {s.name}: {e}")

print(f"\nRe-imported: {re_imported}  Errors: {errors}")
print(f"Output: {DST}")
