"""
Aggiunge la gamma completa Ligier microcar/quadricicli al catalogo
(prodotti.html) con placeholder 'foto in arrivo' come immagine.

Listino Ligier ufficiale 2024-2025:
- Myli (elettrica, L6e, 14 anni)
- JS50 (linea L6e, 14 anni) — Club, Sport, Premium, Initial, Heritage
- JS60 (linea L7e, patente B1) — Club, Sport, Lounge
- Pulse 3 (cargo L7e)
- Pulse 4 (quadriciclo L7e 4 posti)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODOTTI = ROOT / "prodotti.html"
PLACEHOLDER = "assets/img/placeholder-foto-arrivo.svg"

LIGIER = [
    # Elettriche L6e (14 anni, patente AM)
    ("Myli Active",         "Microcar - Elettrica L6e"),
    ("Myli Dynamic",        "Microcar - Elettrica L6e"),
    ("Myli Vibe",           "Microcar - Elettrica L6e"),
    # Linea JS50 (termica + elettrica, L6e)
    ("JS50 Club",           "Microcar - Termica L6e"),
    ("JS50 Sport Ultimate", "Microcar - Termica L6e"),
    ("JS50 Premium",        "Microcar - Termica L6e"),
    ("JS50 Initial",        "Microcar - Termica L6e"),
    ("JS50 Heritage",       "Microcar - Termica L6e"),
    ("JS50 L Initial",      "Microcar - Termica L6e"),
    ("JS50 L Sport",        "Microcar - Termica L6e"),
    ("JS50 Elec Club",      "Microcar - Elettrica L6e"),
    ("JS50 Elec Sport",     "Microcar - Elettrica L6e"),
    ("JS50 Elec Premium",   "Microcar - Elettrica L6e"),
    # Linea JS60 (L7e, patente B1)
    ("JS60 Club",           "Quadriciclo - Termico L7e"),
    ("JS60 Sport",          "Quadriciclo - Termico L7e"),
    ("JS60 Lounge",         "Quadriciclo - Termico L7e"),
    ("JS60 L Sport",        "Quadriciclo - Termico L7e"),
    # Pulse (commerciali)
    ("Pulse 3",             "Microcar - Cargo Van L6e"),
    ("Pulse 4",             "Quadriciclo - 4 posti L7e"),
]


def make_card(idx, name, category):
    safe = name.replace('"', '&quot;')
    alt = f'Ligier {safe} - {category}'
    return (
        f'        <article class="depth-card" data-product-id="lig{idx}" '
        f'data-product-name="{safe}" '
        f'data-product-brand="Ligier" '
        f'data-product-cat="{category}" '
        f'data-product-img="{PLACEHOLDER}">\n'
        f'          <div class="depth-card__base">\n'
        f'            <img src="{PLACEHOLDER}" alt="{alt}" loading="lazy" decoding="async">\n'
        f'          </div>\n'
        f'          <div class="depth-card__overlay">\n'
        f'            <h4 class="depth-card__title">Ligier {safe}</h4>\n'
        f'          </div>\n'
        f'          <div class="depth-card__info">\n'
        f'            <span class="depth-card__brand-tag">Ligier</span>\n'
        f'            <span class="depth-card__name">{safe}</span>\n'
        f'            <span class="depth-card__hint">{category}</span>\n'
        f'          </div>\n'
        f'        </article>\n'
    )


def main():
    html = PRODOTTI.read_text(encoding='utf-8')
    if 'data-brand="ligier"' in html.lower() and 'brand-section\' data-brand="ligier"' not in html:
        # Verifica se gia c'e' la sezione Ligier
        if 'brand-section" data-brand="ligier"' in html:
            print("Sezione Ligier gia' presente. Skip.")
            return

    from collections import defaultdict
    groups = defaultdict(list)
    for i, (n, c) in enumerate(LIGIER, start=1):
        groups[c].append((i, n))

    sections_html = '\n      <!-- Sezione Ligier microcar / quadricicli -->\n'
    sections_html += '      <div class="brand-section" data-brand="ligier">\n'
    sections_html += '        <h3 class="brand-section__title">Ligier</h3>\n'

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

    insertion = re.search(r'(</section>\s*</main>)', html)
    if insertion:
        pos = insertion.start()
        new_html = html[:pos] + sections_html + html[pos:]
    else:
        new_html = html.replace('</main>', sections_html + '</main>', 1)

    PRODOTTI.write_text(new_html, encoding='utf-8')
    print(f"  {len(LIGIER)} prodotti Ligier aggiunti in {len(groups)} categorie")
    for c, items in groups.items():
        print(f"    {c}: {len(items)} modelli")


if __name__ == "__main__":
    main()
