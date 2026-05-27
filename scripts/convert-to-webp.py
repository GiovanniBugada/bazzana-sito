"""
Converte tutte le PNG/JPG sotto assets/img/ in formato WebP parallelo.
Salva il file .webp accanto all'originale (es. foto.jpg → foto.webp).
Non tocca l'originale (resta come fallback per browser vecchi).

Lanciare ogni volta che aggiungi nuove immagini al catalogo.
"""
from pathlib import Path
from PIL import Image
import sys

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "img"

# Qualità: 82 è un buon equilibrio (visivamente identico, 50-70% più piccolo)
QUALITY = 82

# Estensioni da convertire
EXTS = {".png", ".jpg", ".jpeg"}

def file_size_kb(p):
    return p.stat().st_size / 1024

def main():
    if not ASSETS.exists():
        print(f"Non trovata: {ASSETS}")
        sys.exit(1)

    total = 0
    converted = 0
    skipped = 0
    saved_orig = 0
    saved_webp = 0

    for src in ASSETS.rglob("*"):
        if src.suffix.lower() not in EXTS:
            continue
        # Salta i file dentro _archive
        if "_archive" in src.parts:
            continue
        total += 1
        dst = src.with_suffix(".webp")
        # Skip se già esistente e più recente
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            skipped += 1
            saved_orig += src.stat().st_size
            saved_webp += dst.stat().st_size
            continue
        try:
            im = Image.open(src)
            # Per PNG con trasparenza, mantieni l'alpha
            save_kwargs = {"quality": QUALITY, "method": 6}
            if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
                im.save(dst, "WEBP", lossless=False, **save_kwargs)
            else:
                if im.mode != "RGB":
                    im = im.convert("RGB")
                im.save(dst, "WEBP", **save_kwargs)
            converted += 1
            saved_orig += src.stat().st_size
            saved_webp += dst.stat().st_size
            if converted % 50 == 0:
                print(f"  {converted}/{total} convertite…")
        except Exception as e:
            print(f"  ERR su {src.name}: {e}")

    print()
    print(f"=== RISULTATO ===")
    print(f"Totale immagini scannerizzate: {total}")
    print(f"Convertite ora:                {converted}")
    print(f"Skip (già aggiornate):         {skipped}")
    print(f"Dimensione originale:          {saved_orig/1024/1024:.1f} MB")
    print(f"Dimensione WebP:               {saved_webp/1024/1024:.1f} MB")
    if saved_orig:
        risparmio = (1 - saved_webp/saved_orig) * 100
        print(f"Risparmio:                     {risparmio:.1f}%")

if __name__ == "__main__":
    main()
