"""
Aggiunge prodotti Stihl al catalogo (prodotti.html) usando il placeholder
"foto in arrivo" come immagine. Quando arrivano le foto reali del cliente,
si sostituiscono i singoli file e l'immagine si aggiorna automaticamente.

Crea una sezione "Stihl" nel catalogo con sotto-categorie (Motoseghe,
Decespugliatori, Tagliasiepi, Soffiatori, Rasaerba, Robot, Trattorini).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODOTTI = ROOT / "prodotti.html"
PLACEHOLDER = "assets/img/placeholder-foto-arrivo.svg"

# Catalogo Stihl ufficiale (modelli principali in vendita 2024-2025)
STIHL = [
    # Motoseghe da bosco / abbattimento (benzina)
    ("MS 162",    "Motoseghe - Da Bosco"),
    ("MS 170",    "Motoseghe - Da Bosco"),
    ("MS 180",    "Motoseghe - Da Bosco"),
    ("MS 181",    "Motoseghe - Da Bosco"),
    ("MS 211",    "Motoseghe - Da Bosco"),
    ("MS 231",    "Motoseghe - Da Bosco"),
    ("MS 251",    "Motoseghe - Da Bosco"),
    ("MS 261",    "Motoseghe - Da Bosco"),
    ("MS 271",    "Motoseghe - Da Bosco"),
    ("MS 291",    "Motoseghe - Da Bosco"),
    ("MS 311",    "Motoseghe - Da Bosco"),
    ("MS 362",    "Motoseghe - Da Bosco"),
    ("MS 391",    "Motoseghe - Da Bosco"),
    ("MS 462",    "Motoseghe - Professionali"),
    ("MS 500i",   "Motoseghe - Professionali"),
    ("MS 661",    "Motoseghe - Professionali"),
    # Motoseghe da potatura
    ("MS 150 T",  "Motoseghe - Da Potatura"),
    ("MS 151 T",  "Motoseghe - Da Potatura"),
    ("MS 192 T",  "Motoseghe - Da Potatura"),
    ("MS 194 T",  "Motoseghe - Da Potatura"),
    ("MS 201 T",  "Motoseghe - Da Potatura"),
    # Motoseghe batteria (MSA)
    ("MSA 60",    "Motoseghe - A Batteria"),
    ("MSA 120 C", "Motoseghe - A Batteria"),
    ("MSA 140 C", "Motoseghe - A Batteria"),
    ("MSA 160 T", "Motoseghe - A Batteria"),
    ("MSA 200 C", "Motoseghe - A Batteria"),
    ("MSA 220 T", "Motoseghe - A Batteria"),
    ("MSA 300",   "Motoseghe - A Batteria"),
    ("MSA 300 C", "Motoseghe - A Batteria"),
    # Decespugliatori benzina (FS)
    ("FS 38",     "Decespugliatori - A Benzina"),
    ("FS 40",     "Decespugliatori - A Benzina"),
    ("FS 56",     "Decespugliatori - A Benzina"),
    ("FS 70",     "Decespugliatori - A Benzina"),
    ("FS 80",     "Decespugliatori - A Benzina"),
    ("FS 91",     "Decespugliatori - A Benzina"),
    ("FS 111",    "Decespugliatori - A Benzina"),
    ("FS 131",    "Decespugliatori - A Benzina"),
    ("FS 240",    "Decespugliatori - A Benzina"),
    ("FS 260",    "Decespugliatori - A Benzina"),
    ("FS 311",    "Decespugliatori - A Benzina"),
    ("FS 411",    "Decespugliatori - A Benzina"),
    ("FS 461",    "Decespugliatori - A Benzina"),
    ("FS 511",    "Decespugliatori - A Benzina"),
    ("FS 561",    "Decespugliatori - A Benzina"),
    # Decespugliatori batteria (FSA)
    ("FSA 30",    "Decespugliatori - A Batteria"),
    ("FSA 45",    "Decespugliatori - A Batteria"),
    ("FSA 57",    "Decespugliatori - A Batteria"),
    ("FSA 60 R",  "Decespugliatori - A Batteria"),
    ("FSA 80 R",  "Decespugliatori - A Batteria"),
    ("FSA 90 R",  "Decespugliatori - A Batteria"),
    ("FSA 135 R", "Decespugliatori - A Batteria"),
    # Decespugliatori a zaino
    ("FR 130 T",  "Decespugliatori - A Zaino"),
    ("FR 235",    "Decespugliatori - A Zaino"),
    ("FR 410 C-EF","Decespugliatori - A Zaino"),
    ("FR 460 TC-EFM","Decespugliatori - A Zaino"),
    # Tagliasiepi (HS / HSA)
    ("HS 45",     "Tagliasiepi - A Benzina"),
    ("HS 56",     "Tagliasiepi - A Benzina"),
    ("HS 82 R",   "Tagliasiepi - A Benzina"),
    ("HS 87 R",   "Tagliasiepi - A Benzina"),
    ("HSA 26",    "Tagliasiepi - A Batteria"),
    ("HSA 50",    "Tagliasiepi - A Batteria"),
    ("HSA 56",    "Tagliasiepi - A Batteria"),
    ("HSA 66",    "Tagliasiepi - A Batteria"),
    ("HSA 86",    "Tagliasiepi - A Batteria"),
    ("HSA 94 R",  "Tagliasiepi - A Batteria"),
    # Soffiatori
    ("BG 56",     "Soffiatori - A Benzina"),
    ("BG 86",     "Soffiatori - A Benzina"),
    ("BR 200",    "Soffiatori - A Zaino"),
    ("BR 350",    "Soffiatori - A Zaino"),
    ("BR 450 C-EF","Soffiatori - A Zaino"),
    ("BR 700",    "Soffiatori - A Zaino"),
    ("BR 800 C-E","Soffiatori - A Zaino"),
    ("BGA 45",    "Soffiatori - A Batteria"),
    ("BGA 57",    "Soffiatori - A Batteria"),
    ("BGA 60",    "Soffiatori - A Batteria"),
    ("BGA 86",    "Soffiatori - A Batteria"),
    ("BGA 200",   "Soffiatori - A Batteria"),
    # Aspiratori
    ("SH 86",     "Soffiatori - Aspiratori"),
    # Rasaerba (RM)
    ("RM 248",    "Rasaerba - A Benzina"),
    ("RM 253",    "Rasaerba - A Benzina"),
    ("RM 443",    "Rasaerba - A Benzina"),
    ("RM 448",    "Rasaerba - A Benzina"),
    ("RM 545",    "Rasaerba - A Benzina"),
    ("RM 655",    "Rasaerba - A Benzina"),
    ("RM 756",    "Rasaerba - A Benzina"),
    # Rasaerba batteria (RMA)
    ("RMA 235",   "Rasaerba - A Batteria"),
    ("RMA 248",   "Rasaerba - A Batteria"),
    ("RMA 339",   "Rasaerba - A Batteria"),
    ("RMA 443",   "Rasaerba - A Batteria"),
    ("RMA 448",   "Rasaerba - A Batteria"),
    ("RMA 545",   "Rasaerba - A Batteria"),
    # Robot tagliaerba
    ("iMow 5",    "Robot Tagliaerba"),
    ("iMow 6",    "Robot Tagliaerba"),
    ("iMow 6 EVO","Robot Tagliaerba"),
    ("iMow 7",    "Robot Tagliaerba"),
    # Trattorini
    ("RT 4082",   "Trattorini"),
    ("RT 5097",   "Trattorini"),
    ("RT 5112 Z", "Trattorini"),
    ("RT 6112 C", "Trattorini"),
    # Potatori asta
    ("HT 56 C-E", "Potatori - Asta"),
    ("HT 105",    "Potatori - Asta"),
    ("HT 133",    "Potatori - Asta"),
    ("HTA 50",    "Potatori - A Batteria"),
    ("HTA 86",    "Potatori - A Batteria"),
    # Idropulitrici
    ("RE 90",     "Idropulitrici"),
    ("RE 110",    "Idropulitrici"),
    ("RE 130",    "Idropulitrici"),
]


def make_card(idx, name, category):
    """Genera una card <article> Stihl per il catalogo."""
    safe_name = name.replace('"', '&quot;')
    alt = f"Stihl {safe_name} - {category}"
    return (
        f'        <article class="depth-card" data-product-id="stihl{idx}" '
        f'data-product-name="{safe_name}" '
        f'data-product-brand="Stihl" '
        f'data-product-cat="{category}" '
        f'data-product-img="{PLACEHOLDER}">\n'
        f'          <div class="depth-card__base">\n'
        f'            <img src="{PLACEHOLDER}" alt="{alt}" loading="lazy" decoding="async">\n'
        f'          </div>\n'
        f'          <div class="depth-card__overlay">\n'
        f'            <h4 class="depth-card__title">Stihl {safe_name}</h4>\n'
        f'          </div>\n'
        f'          <div class="depth-card__info">\n'
        f'            <span class="depth-card__brand-tag">Stihl</span>\n'
        f'            <span class="depth-card__name">{safe_name}</span>\n'
        f'            <span class="depth-card__hint">{category}</span>\n'
        f'          </div>\n'
        f'        </article>\n'
    )


def main():
    html = PRODOTTI.read_text(encoding="utf-8")
    if 'brand-section" data-brand="stihl"' in html:
        print("Sezione Stihl gia' presente. Skip.")
        return

    # Raggruppa per categoria
    from collections import defaultdict
    groups = defaultdict(list)
    for i, (n, c) in enumerate(STIHL, start=1):
        groups[c].append((i, n))

    # Crea sezione brand "Stihl"
    sections_html = '\n      <!-- Sezione Stihl (placeholder foto - aggiungere foto reali quando disponibili) -->\n'
    sections_html += '      <div class="brand-section" data-brand="stihl">\n'
    sections_html += '        <h3 class="brand-section__title">Stihl</h3>\n'

    for cat, items in groups.items():
        cat_slug = re.sub(r'[^a-z0-9]+', '-', cat.lower()).strip('-')
        sections_html += f'        <details class="cat-group" data-cat="{cat}" data-cat-slug="{cat_slug}" open>\n'
        sections_html += f'          <summary class="cat-group__title">{cat}</summary>\n'
        sections_html += f'          <div class="cat-group__grid">\n'
        for idx, name in items:
            sections_html += make_card(idx, name, cat)
        sections_html += '          </div>\n'
        sections_html += '        </details>\n'

    sections_html += '      </div>\n'

    # Inserisci PRIMA della chiusura di .product-catalog (cerca il primo brand-section o la fine del main)
    # Cerchiamo la sezione "accessori" e la inseriamo PRIMA. Se non c'e', alla fine.
    insertion_marker = re.search(r'(</section>\s*</main>)', html)
    if insertion_marker:
        # Inserisci prima del </section></main> finale del catalogo
        pos = insertion_marker.start()
        new_html = html[:pos] + sections_html + html[pos:]
    else:
        # Fallback: prima del </main>
        new_html = html.replace('</main>', sections_html + '</main>', 1)

    PRODOTTI.write_text(new_html, encoding="utf-8")
    total = len(STIHL)
    print(f"  {total} prodotti Stihl aggiunti in {len(groups)} categorie")
    for c, items in groups.items():
        print(f"    {c}: {len(items)} modelli")


if __name__ == "__main__":
    main()
