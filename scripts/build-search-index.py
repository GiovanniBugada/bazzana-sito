"""
Estrae i 519 prodotti dal catalogo (prodotti.html) e li scrive in
js/search-index.js come window.BZN_SEARCH_INDEX.

Lanciare ogni volta che si modifica prodotti.html.
"""
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "prodotti.html"
DST = ROOT / "js" / "search-index.js"

html = SRC.read_text(encoding="utf-8")

# Match ogni article.depth-card e estrai gli attributi
ATTR_RE = {
    "id":    re.compile(r'data-product-id="([^"]*)"'),
    "name":  re.compile(r'data-product-name="([^"]*)"'),
    "brand": re.compile(r'data-product-brand="([^"]*)"'),
    "cat":   re.compile(r'data-product-cat="([^"]*)"'),
    "img":   re.compile(r'data-product-img="([^"]*)"'),
}

CARD_RE = re.compile(r'<article\s+class="depth-card"[^>]*>', re.IGNORECASE)

items = []
for m in CARD_RE.finditer(html):
    tag = m.group(0)
    rec = {}
    for k, r in ATTR_RE.items():
        mm = r.search(tag)
        rec[k] = mm.group(1) if mm else ""
    if not rec.get("name") or not rec.get("brand"):
        continue
    items.append(rec)

# Slug dei prodotti con scheda dedicata (matcha BAZZANA_PRODUCTS in product-data.js)
DB_SLUGS = {
    ("stihl", "ms 251"): "stihl-ms-251",
    ("stihl", "fs 131"): "stihl-fs-131",
    ("stihl", "bg 86"): "stihl-bg-86",
    ("stihl", "imow 6 evo"): "stihl-imow",
    ("honda", "hrx 476"): "honda-hrx-476",
    ("honda", "hrn 536"): "honda-hrn",
    ("honda", "eu22i"): "honda-eu22i",
    ("active", "4860 sh"): "active-4860",
    ("active", "mz cm"): "active-mz-cm",
    ("geotech", "tritone sprint"): "cippatore-tritone",
    ("ligier", "myli"): "ligier-myli",
}

# Stihl, Honda, Echo, Geotech, Ligier, Yashi NON sono nel catalogo HTML,
# li aggiungiamo direttamente da product-data.js.
# IMPORTANTE: per Stihl NON abbiamo foto reali — usiamo il placeholder
# "foto in arrivo". Honda/Ligier hanno foto reali del banco.
PH = "assets/img/placeholder-foto-arrivo.svg"
EXTRA_DB = [
    {"brand": "Stihl",  "name": "MS 251",      "cat": "Motosega da bosco",            "img": PH, "slug": "stihl-ms-251"},
    {"brand": "Stihl",  "name": "FS 131",      "cat": "Decespugliatore",              "img": PH, "slug": "stihl-fs-131"},
    {"brand": "Stihl",  "name": "BG 86",       "cat": "Soffiatore",                   "img": PH, "slug": "stihl-bg-86"},
    {"brand": "Stihl",  "name": "iMow 6 EVO",  "cat": "Robot tagliaerba",             "img": PH, "slug": "stihl-imow"},
    {"brand": "Honda",  "name": "HRX 476",     "cat": "Rasaerba semovente",           "img": "assets/img/prodotti/rasaerba-honda-hr-fronte.jpg", "slug": "honda-hrx-476"},
    {"brand": "Honda",  "name": "HRN 536",     "cat": "Rasaerba mulching",            "img": "assets/img/prodotti/rasaerba-honda-hr-fronte.jpg", "slug": "honda-hrn"},
    {"brand": "Honda",  "name": "EU22i",       "cat": "Generatore inverter portatile","img": PH, "slug": "honda-eu22i"},
    {"brand": "Geotech","name": "Tritone Sprint","cat": "Biotrituratore a benzina",   "img": PH, "slug": "cippatore-tritone"},
    {"brand": "Ligier", "name": "Myli",        "cat": "Microcar elettrica L6e",       "img": "assets/img/prodotti/microcar-ligier-jsbluepass-frontale.jpg", "slug": "ligier-myli"},
]

# Per le card del catalogo, prova a matchare uno slug per i 2 prodotti già nel DB
def resolve_slug(brand, name):
    key = (brand.lower().strip(), name.lower().strip())
    return DB_SLUGS.get(key, "")

records = []
for it in items:
    rec = {
        "brand": it["brand"],
        "name":  it["name"],
        "cat":   it["cat"].replace(" - ", " · "),
        "img":   it["img"],
        "slug":  resolve_slug(it["brand"], it["name"]),
    }
    records.append(rec)

# Aggiungi i prodotti extra (Stihl/Honda/Echo/...) non nel catalogo HTML
for x in EXTRA_DB:
    records.append({
        "brand": x["brand"],
        "name":  x["name"],
        "cat":   x["cat"],
        "img":   x["img"],
        "slug":  x["slug"],
    })

# Deduplica su brand+name (case-insensitive)
seen = set()
deduped = []
for r in records:
    key = (r["brand"].lower(), r["name"].lower())
    if key in seen:
        continue
    seen.add(key)
    deduped.append(r)

js = "/* Indice di ricerca prodotti — generato da scripts/build-search-index.py.\n"
js += "   NON modificare a mano: rieseguire lo script dopo aver toccato prodotti.html. */\n"
js += "window.BZN_SEARCH_INDEX = "
js += json.dumps(deduped, ensure_ascii=False, indent=0).replace("\n", "")
js += ";\n"

DST.write_text(js, encoding="utf-8")
print(f"OK: scritti {len(deduped)} prodotti in {DST}")
