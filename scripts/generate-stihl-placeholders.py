"""
Genera un placeholder SVG personalizzato per ogni modello Stihl del catalogo,
con il nome del modello scritto sopra, in stile catalogo Bazzana.

Output: assets/img/prodotti/stihl-placeholder/{slug-modello}.svg

Poi aggiorna prodotti.html sostituendo il placeholder generico con quello
specifico per ogni card Stihl.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODOTTI = ROOT / "prodotti.html"
OUT_DIR = ROOT / "assets" / "img" / "prodotti" / "stihl-placeholder"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def slugify(s):
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()
    return s


SVG_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" role="img" aria-labelledby="ph-title">
  <title id="ph-title">Stihl {model}</title>
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f4f1ea"/>
      <stop offset="100%" stop-color="#e8e3d4"/>
    </linearGradient>
    <pattern id="grain" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="4" fill="transparent"/>
      <circle cx="1" cy="1" r="0.3" fill="rgba(14, 15, 14, 0.04)"/>
      <circle cx="3" cy="3" r="0.3" fill="rgba(14, 15, 14, 0.03)"/>
    </pattern>
  </defs>

  <!-- Background -->
  <rect width="600" height="600" fill="url(#bg)"/>
  <rect width="600" height="600" fill="url(#grain)"/>

  <!-- Cornice dashed -->
  <rect x="80" y="80" width="440" height="440" fill="none" stroke="rgba(14, 15, 14, 0.10)" stroke-width="1" stroke-dasharray="4 6"/>

  <!-- Stihl badge in alto -->
  <rect x="180" y="125" width="240" height="42" rx="3" fill="#ee5e1f"/>
  <text x="300" y="153" text-anchor="middle"
        font-family="Inter, system-ui, sans-serif"
        font-size="22" font-weight="700" letter-spacing="4"
        fill="#ffffff">
    STIHL
  </text>

  <!-- Icona macchina (silhouette stilizzata) -->
  <g transform="translate(300 280)" fill="none" stroke="#0E0F0E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity="0.4">
    {icon}
  </g>

  <!-- Nome modello (grande) -->
  <text x="300" y="430" text-anchor="middle"
        font-family="Fraunces, Georgia, serif"
        font-size="{model_size}" font-weight="500"
        fill="#0E0F0E">
    {model}
  </text>

  <!-- Categoria (piccola) -->
  <text x="300" y="465" text-anchor="middle"
        font-family="JetBrains Mono, ui-monospace, monospace"
        font-size="11" letter-spacing="2.5"
        fill="#0E0F0E" opacity="0.6"
        font-weight="500">
    {category_upper}
  </text>

  <!-- Eyebrow in basso -->
  <text x="300" y="510" text-anchor="middle"
        font-family="Fraunces, Georgia, serif"
        font-size="14" font-weight="300" font-style="italic"
        fill="#0E0F0E" opacity="0.5">
    Foto in arrivo a breve
  </text>

  <!-- Brand dot -->
  <circle cx="300" cy="540" r="3" fill="#ee5e1f"/>
</svg>
'''


# Icone per categoria (silhouette semplificate)
ICONS = {
    "Motoseghe": '<path d="M -60 -10 L -10 -10 L -10 -25 L 30 -25 L 50 -10 L 60 -10 L 55 5 L 50 -5 L 30 -5 L 25 -15 L -10 -15 L -10 5 L -60 5 Z"/><circle cx="-30" cy="-5" r="3"/><line x1="50" y1="-10" x2="58" y2="-15"/>',
    "Decespugliatori": '<line x1="0" y1="-50" x2="-30" y2="40"/><line x1="-50" y1="40" x2="-10" y2="40"/><circle cx="-30" cy="40" r="20" fill="none"/><circle cx="-30" cy="40" r="3"/><rect x="-12" y="-55" width="24" height="14" rx="2"/>',
    "Tagliasiepi": '<rect x="-50" y="-8" width="80" height="16" rx="2"/><polygon points="30,-8 60,-8 50,0 60,8 30,8"/><circle cx="-40" cy="0" r="3"/><line x1="-50" y1="-15" x2="30" y2="-15" stroke-dasharray="3 3"/>',
    "Soffiatori": '<rect x="-40" y="-10" width="50" height="20" rx="4"/><polygon points="10,-12 35,-25 35,25 10,12"/><circle cx="-25" cy="0" r="3"/><path d="M 40 -8 L 55 -15 M 40 0 L 60 0 M 40 8 L 55 15"/>',
    "Rasaerba": '<rect x="-50" y="-15" width="100" height="30" rx="4"/><circle cx="-35" cy="20" r="10"/><circle cx="35" cy="20" r="10"/><line x1="0" y1="-15" x2="-25" y2="-40"/><circle cx="-30" cy="-45" r="5" fill="none"/>',
    "Robot": '<rect x="-45" y="-25" width="90" height="50" rx="20"/><circle cx="-25" cy="20" r="8"/><circle cx="25" cy="20" r="8"/><circle cx="0" cy="-10" r="4"/><circle cx="-20" cy="-15" r="2"/><circle cx="20" cy="-15" r="2"/>',
    "Trattorini": '<rect x="-40" y="-20" width="60" height="30" rx="4"/><circle cx="-30" cy="15" r="10"/><circle cx="35" cy="15" r="14"/><polygon points="20,-20 40,-20 35,-10 25,-10"/><line x1="-30" y1="-25" x2="-10" y2="-25"/>',
    "Potatori": '<line x1="-50" y1="40" x2="50" y2="-40" stroke-width="3"/><polygon points="40,-50 60,-30 50,-30 50,-20 40,-30 30,-30"/><circle cx="-45" cy="42" r="4"/>',
    "Idropulitrici": '<rect x="-40" y="-15" width="50" height="30" rx="3"/><polygon points="10,-10 35,-20 35,20 10,10"/><path d="M 35 -10 L 50 -10 L 50 -3 M 35 0 L 55 0 M 35 10 L 50 10 L 50 3"/>',
}


def get_icon(category):
    for key, icon in ICONS.items():
        if key in category:
            return icon
    return '<rect x="-50" y="-25" width="100" height="50" rx="4"/><circle cx="0" cy="0" r="12" fill="none"/>'


def main():
    html = PRODOTTI.read_text(encoding="utf-8")

    # Trova tutte le card Stihl
    stihl_card_re = re.compile(
        r'(<article\s+class="depth-card"[^>]*data-product-name="([^"]+)"[^>]*data-product-brand="Stihl"[^>]*data-product-cat="([^"]+)"[^>]*data-product-img=")([^"]+)("[^>]*>.*?</article>)',
        re.DOTALL | re.IGNORECASE,
    )

    generated = 0
    cards_updated = 0
    html_out = html

    seen_models = set()
    for m in stihl_card_re.finditer(html):
        model = m.group(2)
        category = m.group(3)
        if model in seen_models:
            continue
        seen_models.add(model)

        # Genera SVG personalizzato
        slug = slugify(model)
        # Dimensione testo modello in base a lunghezza
        model_size = 42 if len(model) <= 8 else (34 if len(model) <= 14 else 26)
        # Categoria pulita (prima parte prima del trattino)
        cat_short = category.split(' - ')[0]
        category_upper = cat_short.upper()
        icon = get_icon(cat_short)

        svg = SVG_TEMPLATE.format(
            model=model.replace('&', '&amp;'),
            category_upper=category_upper,
            icon=icon,
            model_size=model_size,
        )

        out_path = OUT_DIR / f'{slug}.svg'
        out_path.write_text(svg, encoding='utf-8')
        generated += 1

    # Ora aggiorna prodotti.html: per ogni card Stihl, sostituisci il path placeholder
    # con il nuovo placeholder specifico
    def repl(m):
        nonlocal cards_updated
        head = m.group(1)
        model = m.group(2)
        category = m.group(3)
        old_path = m.group(4)
        tail = m.group(5)
        slug = slugify(model)
        new_path = f'assets/img/prodotti/stihl-placeholder/{slug}.svg'
        # Aggiorna anche il src dell'<img> dentro la card
        tail_new = re.sub(
            r'(<img[^>]*src=")[^"]+(")',
            lambda mm: mm.group(1) + new_path + mm.group(2),
            tail,
            count=1,
        )
        # Aggiorna anche alt: deve riflettere brand + model + categoria
        new_alt = f'Stihl {model} - {category}'.replace('"', '&quot;')
        tail_new = re.sub(
            r'(<img[^>]*alt=")[^"]+(")',
            lambda mm: mm.group(1) + new_alt + mm.group(2),
            tail_new,
            count=1,
        )
        cards_updated += 1
        return head + new_path + tail_new

    html_out = stihl_card_re.sub(repl, html_out)
    PRODOTTI.write_text(html_out, encoding='utf-8')

    print(f"  SVG placeholder Stihl generati: {generated}")
    print(f"  Card Stihl aggiornate:           {cards_updated}")
    print(f"  Output in {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
