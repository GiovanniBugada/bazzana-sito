"""
Rigenera SOLO i .webp delle foto-XXX.jpg in assets/img/bazzana/ usando i
JPG appena re-importati. Tutto il resto dei webp resta invariato.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "assets" / "img" / "bazzana"

jpgs = sorted(DIR.glob("foto-*.jpg"))
print(f"Foto JPG da convertire: {len(jpgs)}")

ok = 0
err = 0
for j in jpgs:
    webp = j.with_suffix(".webp")
    try:
        img = Image.open(j)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(webp, "WEBP", quality=82, method=6)
        ok += 1
    except Exception as e:
        err += 1
        print(f"  ERROR {j.name}: {e}")

print(f"\nOK: {ok}  Errors: {err}")
