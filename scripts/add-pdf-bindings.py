"""
Per ogni pagina prodotto dedicata (prodotti/*.html), aggiunge:
  - data-bzn-product, data-brand, data-model, data-category, data-description,
    data-img, data-specs (JSON) sul <main class="product"> per fornire i metadati
    al generatore PDF.
  - data-product-cta="pdf" sul bottone "Chiedi disponibilita" cosi il binding JS
    intercetta il click.

Lettura dei dati prodotto: dal DOM stesso (h1, dl.spec, img, brand, lead).
"""
import re
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "prodotti"

processed = 0
for p in sorted(DIR.glob("*.html")):
    if p.name == "dettaglio.html":
        continue
    s = p.read_text(encoding="utf-8")

    # 1) Brand + categoria dal <p class="product__brand">Brand · Categoria</p>
    brand, category = "", ""
    m = re.search(r'<p class="product__brand[^"]*">([^<]+)</p>', s)
    if m:
        text = re.sub(r'\s+', ' ', m.group(1)).strip()
        if " · " in text:
            brand, category = text.split(" · ", 1)
        else:
            parts = text.split(maxsplit=1)
            brand = parts[0] if parts else ""
            category = parts[1] if len(parts) > 1 else ""

    # 2) Model dal <h1 class="product__title">MODEL<br/><em>tagline</em></h1>
    model = ""
    m = re.search(r'<h1 class="product__title[^"]*"[^>]*>([^<]+)', s)
    if m:
        model = re.sub(r'\s+', ' ', m.group(1)).strip()

    # 3) Description dal <p class="product__desc">...
    desc = ""
    m = re.search(r'<p class="product__desc[^"]*"[^>]*>(.*?)</p>', s, re.DOTALL)
    if m:
        desc = re.sub(r'<[^>]+>', '', m.group(1))
        desc = re.sub(r'\s+', ' ', desc).strip()

    # 4) Img path dal <img src="..." dentro product__media
    img = ""
    m = re.search(
        r'<div class="product__media[^"]*"[^>]*>\s*<img\s+src="([^"]+)"',
        s,
    )
    if m:
        img_raw = m.group(1)
        # Da "../assets/..." a "assets/..."
        img = re.sub(r'^(\.\./)+', '', img_raw)

    # 5) Specs dal <dl class="spec">
    specs = []
    m = re.search(r'<dl class="spec[^"]*"[^>]*>(.*?)</dl>', s, re.DOTALL)
    if m:
        dl = m.group(1)
        for dt_m, dd_m in re.findall(
            r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', dl, re.DOTALL
        ):
            label = re.sub(r'<[^>]+>', '', dt_m).strip()
            value = re.sub(r'<[^>]+>', '', dd_m).strip()
            if label:
                specs.append({"label": label, "value": value})

    if not (brand and model):
        print(f"  SKIP {p.name}: no brand/model")
        continue

    # Costruisci attributi data-* (escape virgolette)
    def esc(v):
        return v.replace('"', '&quot;').replace("\n", " ")
    specs_json = json.dumps(specs, ensure_ascii=False).replace('"', '&quot;')

    # 6) Aggiungi data-* sul <main class="product"
    main_attrs = (
        ' data-bzn-product'
        f' data-brand="{esc(brand)}"'
        f' data-model="{esc(model)}"'
        f' data-category="{esc(category)}"'
        f' data-description="{esc(desc)}"'
        f' data-img="{esc(img)}"'
        f' data-specs="{specs_json}"'
    )
    s_new = re.sub(
        r'(<main\s+id="main"\s+class="product")(>)',
        lambda mm: mm.group(1) + main_attrs + mm.group(2),
        s,
        count=1,
    )

    # 7) Aggiungi data-product-cta="pdf" al primo bottone "Chiedi disponibilita"
    s_new = re.sub(
        r'(<a class="btn"\s+href="https://wa\.me/393464156981[^"]*"[^>]*?)(>Chiedi disponibilit[aà])',
        r'\1 data-product-cta="pdf"\2',
        s_new,
        count=1,
    )
    # Variante "Chiedi sopralluogo"
    s_new = re.sub(
        r'(<a class="btn"\s+href="https://wa\.me/393464156981[^"]*"[^>]*?)(>Chiedi sopralluogo)',
        r'\1 data-product-cta="pdf"\2',
        s_new,
        count=1,
    )

    if s_new != s:
        p.write_text(s_new, encoding="utf-8")
        processed += 1
        print(f"  bound {p.name}: {brand} {model} ({len(specs)} specs)")
    else:
        print(f"  skip {p.name}: no change")

print(f"\nProcessate {processed} pagine prodotto")
