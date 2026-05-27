"""
Import foto reali Stihl: prende le foto dalla cartella

    assets/img/prodotti/stihl-foto-reali/

e le abbina automaticamente ai prodotti Stihl del catalogo per somiglianza
del nome file con il nome del modello.

REGOLA DI MATCHING:
  - Per ciascun file foto, estraggo i "model tokens" significativi
    (es. "ms-251.jpg" → ["ms", "251"]; "fs131-c.png" → ["fs", "131"])
  - Per ciascun prodotto Stihl, estraggo i model tokens dal nome
    (es. "MS 251" → ["MS", "251"]; "FS 131" → ["FS", "131"])
  - Matchano se TUTTI i token del prodotto compaiono nel filename (case-insensitive)
  - Es. "MS 251" matcha "ms-251.jpg", "Stihl_MS251.png", "scheda_ms_251_fronte.jpg"

PROCESSING DELLE FOTO:
  - EXIF auto-rotate (i pixel ruotati correttamente)
  - Resize a max 1200px lato lungo
  - Salva come JPG q=85 + WebP q=85
  - Output: assets/img/prodotti/stihl-foto/{slug}.jpg + .webp

POI:
  - Aggiorna prodotti.html cambiando data-product-img e <img src> per il modello
  - Mantiene il placeholder per i modelli senza foto

USO:
  1. Crea la cartella: assets/img/prodotti/stihl-foto-reali/
  2. Metti dentro le foto Stihl (qualsiasi formato/risoluzione, qualsiasi nome
     purche' contenga il codice modello: "MS 251.jpg", "ms251.png", "FS131-bianco.jpg")
  3. Lancia: python scripts/import-stihl-photos.py
  4. La console ti mostra cosa è stato matchato e cosa no
"""
import re
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
PRODOTTI = ROOT / "prodotti.html"
SRC_DIR = ROOT / "assets" / "img" / "prodotti" / "stihl-foto-reali"
OUT_DIR = ROOT / "assets" / "img" / "prodotti" / "stihl-foto"

OUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_SIDE = 1200
JPG_Q = 85
WEBP_Q = 85


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s


def tokens(s):
    """Estrai token alfanumerici significativi (lower, >=2 char)."""
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return [t for t in s.split() if len(t) >= 2 or t.isdigit()]


def model_tokens(model):
    """I token del nome modello (es. 'MS 251 C-BE' -> ['ms','251','c','be'])."""
    return tokens(model)


def filename_tokens(filename):
    """Token dal filename (senza estensione)."""
    name = Path(filename).stem
    return tokens(name)


def card_matches_file(model, filename):
    """True se TUTTI i token significativi del modello sono nel filename."""
    mt = model_tokens(model)
    if not mt:
        return False
    ft = set(filename_tokens(filename))
    # Tutti i token del modello devono essere presenti nel filename
    for t in mt:
        if t in {"a", "c", "be", "ef", "tc", "efm", "ce", "z"}:
            # token troppo generici: skip dal vincolo (matchiamo lo stesso)
            continue
        if t not in ft:
            return False
    return True


def best_match_for_model(model, photo_files):
    """Trova la foto migliore per un modello (la prima che matcha)."""
    candidates = [p for p in photo_files if card_matches_file(model, p.name)]
    if not candidates:
        return None
    # Preferisci quella con MENO token extra (piu' specifica)
    def extra_count(p):
        return len(set(filename_tokens(p.name)) - set(model_tokens(model)))
    candidates.sort(key=extra_count)
    return candidates[0]


def process_photo(src_path, out_jpg, out_webp):
    """Ridimensiona + EXIF transpose + salva JPG/WebP."""
    img = Image.open(src_path)
    img = ImageOps.exif_transpose(img)
    w, h = img.size
    if max(w, h) > MAX_SIDE:
        if w >= h:
            nw, nh = MAX_SIDE, int(h * MAX_SIDE / w)
        else:
            nh, nw = MAX_SIDE, int(w * MAX_SIDE / h)
        img = img.resize((nw, nh), Image.LANCZOS)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(out_jpg, "JPEG", quality=JPG_Q, optimize=True, progressive=True, exif=b"")
    img.save(out_webp, "WEBP", quality=WEBP_Q, method=6)


def main():
    if not SRC_DIR.exists() or not any(SRC_DIR.iterdir()):
        print(f"\nCartella vuota o inesistente: {SRC_DIR}")
        print("Crea la cartella e metti dentro le foto Stihl, poi rilancia.")
        SRC_DIR.mkdir(parents=True, exist_ok=True)
        return

    # 1) Trova tutte le foto sorgente
    exts = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".bmp", ".tif", ".tiff"}
    photo_files = sorted([p for p in SRC_DIR.iterdir() if p.is_file() and p.suffix.lower() in exts])
    print(f"Foto sorgente: {len(photo_files)} in {SRC_DIR}")

    # 2) Carica prodotti Stihl dal catalogo
    html = PRODOTTI.read_text(encoding="utf-8")
    card_re = re.compile(
        r'<article\s+class="depth-card"[^>]*data-product-name="([^"]+)"[^>]*data-product-brand="Stihl"[^>]*data-product-cat="([^"]+)"',
        re.IGNORECASE,
    )
    stihl_models = []
    for m in card_re.finditer(html):
        stihl_models.append((m.group(1), m.group(2)))
    print(f"Prodotti Stihl nel catalogo: {len(stihl_models)}")

    # 3) Matcha foto -> prodotti
    matches = {}  # model_name -> Path source
    used_files = set()
    for model, cat in stihl_models:
        candidates = [p for p in photo_files if p not in used_files and card_matches_file(model, p.name)]
        if not candidates:
            continue
        # Piu' specifica = meno token extra
        def specificity(p):
            return len(set(filename_tokens(p.name)) - set(model_tokens(model)))
        candidates.sort(key=specificity)
        matches[model] = candidates[0]
        used_files.add(candidates[0])

    print(f"\nMatch trovati: {len(matches)} / {len(stihl_models)}")

    # 4) Processa le foto matchate
    new_paths = {}  # model -> path rel da root
    for model, src in matches.items():
        slug = slugify(model)
        out_jpg = OUT_DIR / f"{slug}.jpg"
        out_webp = OUT_DIR / f"{slug}.webp"
        try:
            process_photo(src, out_jpg, out_webp)
            new_paths[model] = f"assets/img/prodotti/stihl-foto/{slug}.jpg"
            print(f"  OK  {model:20} <- {src.name}")
        except Exception as e:
            print(f"  ERR {model:20} <- {src.name}: {e}")

    # 5) Aggiorna prodotti.html
    if new_paths:
        update_re = re.compile(
            r'(<article\s+class="depth-card"[^>]*data-product-name=")([^"]+)("[^>]*data-product-brand="Stihl"[^>]*data-product-img=")([^"]+)("[^>]*>)(.*?)(</article>)',
            re.DOTALL | re.IGNORECASE,
        )
        updated = 0

        def replace_card(m):
            nonlocal updated
            head1, name, head2, old_img, head3, body, tail = m.groups()
            if name in new_paths:
                new_img = new_paths[name]
                # Sostituisci data-product-img
                new_head = head1 + name + head2 + new_img + head3
                # Sostituisci anche src dell'img
                new_body = re.sub(
                    r'(<img[^>]*src=")[^"]+(")',
                    lambda mm: mm.group(1) + new_img + mm.group(2),
                    body,
                    count=1,
                )
                updated += 1
                return new_head + new_body + tail
            return m.group(0)

        html_new = update_re.sub(replace_card, html)
        PRODOTTI.write_text(html_new, encoding="utf-8")
        print(f"\nCard catalogo aggiornate: {updated}")

    # 6) Report finale
    unmatched_models = [m for m, _ in stihl_models if m not in matches]
    unused_files = [f for f in photo_files if f not in used_files]

    if unmatched_models:
        print(f"\nModelli SENZA foto ({len(unmatched_models)}):")
        for m in unmatched_models[:20]:
            print(f"  - Stihl {m}")
        if len(unmatched_models) > 20:
            print(f"  ... e altri {len(unmatched_models) - 20}")

    if unused_files:
        print(f"\nFoto NON MATCHATE ({len(unused_files)}):")
        for f in unused_files[:15]:
            print(f"  - {f.name}")
        if len(unused_files) > 15:
            print(f"  ... e altre {len(unused_files) - 15}")
        print("\nPer queste foto, rinomina il file aggiungendo il codice modello")
        print("(es. 'MS 251.jpg' o 'stihl_ms251_fronte.jpg') e rilancia lo script.")


if __name__ == "__main__":
    main()
