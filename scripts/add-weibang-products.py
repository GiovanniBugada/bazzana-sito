#!/usr/bin/env python3
"""Genera pagine prodotto Weibang con SVG placeholder per categoria,
aggiorna marquee marchi nei file esistenti, sostituisce la sezione brand
Weibang in prodotti.html (delimitata da marker WEIBANG:START / WEIBANG:END)
e aggiunge entry sitemap.xml.

Pattern derivato da scripts/add-ligier-products.py / add-stihl-products.py,
ma esteso: lo script e' completamente idempotente — genera tutto, basta
rilanciarlo dopo aver modificato MODELS.
"""
from __future__ import annotations

import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODOTTI = ROOT / "prodotti"
PRODOTTI_HTML = ROOT / "prodotti.html"
SITEMAP = ROOT / "sitemap.xml"

# Mapping: slug -> (id_catalogo, sottocategoria_catalogo, svg_categoria)
# - id_catalogo: data-product-id univoco per la card
# - sottocategoria_catalogo: nome leggibile del <details data-cat="...">
# - svg_categoria: filename in assets/img/placeholder-categoria/
CATALOG_MAP = {
    "weibang-wb-506-scv":     ("weib1",  "Rasaerba - Semoventi",          "rasaerba-semovente"),
    "weibang-wb-506-hcv":     ("weib2",  "Rasaerba - Semoventi",          "rasaerba-semovente"),
    "weibang-wb-456-scv":     ("weib7",  "Rasaerba - Semoventi",          "rasaerba-semovente"),
    "weibang-wb-537-scv":     ("weib8",  "Rasaerba - Semoventi",          "rasaerba-semovente"),
    "weibang-wb-506-sc":      ("weib9",  "Rasaerba - A spinta",           "rasaerba-spinta"),
    "weibang-wb-484-sbv-pro": ("weib10", "Rasaerba - Professionali",      "rasaerba-pro"),
    "weibang-wb-537-scv-bbc": ("weib3",  "Rasaerba - Professionali BBC",  "rasaerba-pro"),
    "weibang-wb-656-slcv-bbc":("weib4",  "Rasaerba - Professionali BBC",  "rasaerba-pro"),
    "weibang-p40-bull":       ("weib5",  "Rasaerba - Batteria",           "rasaerba-batteria"),
    "weibang-wb-1100-pro":    ("weib6",  "Trattorini - Rasaerba",         "trattorino"),
    "weibang-wb-384-rb":      ("weib11", "Robot tagliaerba",              "robot"),
}

# Ordine di display delle sottocategorie nel catalogo Weibang
CATALOG_ORDER = [
    "Rasaerba - Semoventi",
    "Rasaerba - A spinta",
    "Rasaerba - Professionali",
    "Rasaerba - Professionali BBC",
    "Rasaerba - Batteria",
    "Trattorini - Rasaerba",
    "Robot tagliaerba",
]

PLACEHOLDER_DIR = "assets/img/placeholder-categoria"


def page_img_path(svg_basename: str) -> str:
    """Path immagine dal punto di vista delle pagine in prodotti/ (relativo)."""
    return f"../{PLACEHOLDER_DIR}/{svg_basename}.svg"


def catalog_img_path(svg_basename: str) -> str:
    """Path immagine dal punto di vista di prodotti.html (root)."""
    return f"{PLACEHOLDER_DIR}/{svg_basename}.svg"


def cat_slug(cat_label: str) -> str:
    """es. 'Rasaerba - A spinta' -> 'rasaerba-a-spinta'"""
    s = cat_label.lower()
    s = s.replace(" - ", "-").replace(" ", "-").replace("·", "-")
    s = re.sub(r"-+", "-", s).strip("-")
    return s

# (slug, model_label, category, lead, description, specs[list of (label, value)], tagline)
MODELS = [
    (
        "weibang-wb-506-scv",
        "WB 506 SCV",
        "Rasaerba semovente",
        "Rasaerba semovente da 51 cm di taglio, telaio robusto e trasmissione progressiva. Foto del modello in arrivo.",
        "Pensato per giardini medio-grandi e uso intensivo. Per scheda "
        "tecnica completa, prezzo aggiornato e disponibilita', chiamaci o "
        "passa in negozio a Cene (BG).",
        [
            ("Larghezza taglio", "51 cm"),
            ("Trazione", "Semovente"),
            ("Categoria", "Professionale"),
            ("Disponibilita'", "Chiamaci per info"),
            ("Assistenza", "Officina interna Bazzana"),
            ("Garanzia", "Standard produttore"),
        ],
        "spinta facile, taglio pulito.",
    ),
    (
        "weibang-wb-506-hcv",
        "WB 506 HCV",
        "Rasaerba semovente",
        "Rasaerba semovente da 51 cm con motore Honda. Foto del modello in arrivo.",
        "Versione con motore a 4 tempi Honda, per giardini medio-grandi e uso frequente. "
        "Per scheda tecnica completa, prezzo aggiornato e disponibilita', chiamaci o "
        "passa in negozio a Cene (BG).",
        [
            ("Larghezza taglio", "51 cm"),
            ("Trazione", "Semovente"),
            ("Motore", "Honda 4 tempi"),
            ("Disponibilita'", "Chiamaci per info"),
            ("Assistenza", "Officina interna Bazzana"),
            ("Garanzia", "Standard produttore"),
        ],
        "spinta facile, motore Honda.",
    ),
    (
        "weibang-wb-537-scv-bbc",
        "WB 537 SCV BBC",
        "Rasaerba professionale BBC",
        "Rasaerba professionale 53 cm con freno lama BBC. Foto del modello in arrivo.",
        "Sistema BBC (Blade Brake Clutch): il motore resta acceso anche quando la "
        "lama e' ferma, ideale per chi sposta spesso la macchina o svuota il cesto. "
        "Per scheda tecnica completa e disponibilita', chiamaci.",
        [
            ("Larghezza taglio", "53 cm"),
            ("Trazione", "Semovente"),
            ("Freno lama", "BBC (Blade Brake Clutch)"),
            ("Categoria", "Professionale"),
            ("Disponibilita'", "Chiamaci per info"),
            ("Assistenza", "Officina interna Bazzana"),
        ],
        "il professionale per giardinieri.",
    ),
    (
        "weibang-wb-656-slcv-bbc",
        "WB 656 SLCV BBC",
        "Rasaerba professionale BBC",
        "Rasaerba professionale 65 cm con freno lama BBC. Foto del modello in arrivo.",
        "Larghezza di taglio 65 cm per coprire piu' superficie con meno passate. "
        "Sistema BBC (Blade Brake Clutch) per sicurezza in uso intensivo. "
        "Per scheda tecnica completa e disponibilita', chiamaci.",
        [
            ("Larghezza taglio", "65 cm"),
            ("Trazione", "Semovente"),
            ("Freno lama", "BBC (Blade Brake Clutch)"),
            ("Categoria", "Professionale"),
            ("Disponibilita'", "Chiamaci per info"),
            ("Assistenza", "Officina interna Bazzana"),
        ],
        "il top di gamma a spinta.",
    ),
    (
        "weibang-p40-bull",
        "P40 BULL",
        "Rasaerba a batteria",
        "Rasaerba professionale a batteria. Foto del modello in arrivo.",
        "Tagliaerba elettrico a batteria, silenzioso e senza emissioni. "
        "Per modello, autonomia e accessori disponibili, chiamaci o passa in negozio.",
        [
            ("Alimentazione", "Batteria"),
            ("Categoria", "Professionale silenzioso"),
            ("Disponibilita'", "Chiamaci per info"),
            ("Assistenza", "Officina interna Bazzana"),
            ("Garanzia", "Standard produttore"),
            ("Vantaggio", "Zero emissioni, basso rumore"),
        ],
        "silenzioso, zero emissioni.",
    ),
    (
        "weibang-wb-1100-pro",
        "WB 1100 PRO",
        "Trattorino tagliaerba",
        "Trattorino tagliaerba Weibang serie 1100. Foto del modello in arrivo.",
        "Trattorino tagliaerba per giardini medio-grandi. "
        "Per cilindrata, larghezza di taglio e disponibilita', chiamaci o passa "
        "in negozio a Cene (BG).",
        [
            ("Tipologia", "Trattorino tagliaerba"),
            ("Categoria", "Hobby / semi-pro"),
            ("Disponibilita'", "Chiamaci per info"),
            ("Assistenza", "Officina interna Bazzana"),
            ("Garanzia", "Standard produttore"),
            ("Consegna", "Su appuntamento"),
        ],
        "trattorino comodo per il tuo giardino.",
    ),
    (
        "weibang-wb-456-scv",
        "WB 456 SCV",
        "Rasaerba semovente compatto",
        "Rasaerba semovente compatto 46 cm. Foto del modello in arrivo.",
        "Versione compatta da 46 cm di taglio, ideale per giardini fino a "
        "800 m². Trasmissione semovente, leggero e maneggevole. Per scheda "
        "tecnica e disponibilita', chiamaci o passa in negozio.",
        [
            ("Larghezza taglio", "46 cm"),
            ("Trazione", "Semovente"),
            ("Categoria", "Hobby evoluto"),
            ("Area consigliata", "Fino a 800 m²"),
            ("Disponibilita'", "Chiamaci per info"),
            ("Assistenza", "Officina interna Bazzana"),
        ],
        "compatto, agile, semovente.",
    ),
    (
        "weibang-wb-537-scv",
        "WB 537 SCV",
        "Rasaerba semovente",
        "Rasaerba semovente 53 cm versione standard. Foto del modello in arrivo.",
        "Versione standard della famiglia 537 (senza freno lama BBC), pensata "
        "per chi cerca un semovente serio senza il sovrapprezzo del sistema "
        "professionale. Per disponibilita' e prezzo, chiamaci.",
        [
            ("Larghezza taglio", "53 cm"),
            ("Trazione", "Semovente"),
            ("Categoria", "Semi-pro"),
            ("Area consigliata", "1000 - 2000 m²"),
            ("Disponibilita'", "Chiamaci per info"),
            ("Assistenza", "Officina interna Bazzana"),
        ],
        "il semovente serio, senza fronzoli.",
    ),
    (
        "weibang-wb-506-sc",
        "WB 506 SC",
        "Rasaerba a spinta",
        "Rasaerba a spinta 51 cm versione economica. Foto del modello in arrivo.",
        "Versione a spinta (non semovente) del WB 506, indicata per giardini "
        "piccoli e medi e per chi preferisce avere controllo manuale del "
        "ritmo di taglio. Per disponibilita', chiamaci.",
        [
            ("Larghezza taglio", "51 cm"),
            ("Trazione", "Spinta manuale"),
            ("Categoria", "Hobby"),
            ("Area consigliata", "Fino a 1000 m²"),
            ("Disponibilita'", "Chiamaci per info"),
            ("Assistenza", "Officina interna Bazzana"),
        ],
        "il classico a spinta, fatto bene.",
    ),
    (
        "weibang-wb-484-sbv-pro",
        "WB 484 SBV PRO",
        "Rasaerba professionale",
        "Rasaerba professionale 48 cm con telaio in acciaio. Foto del modello in arrivo.",
        "Telaio in acciaio rinforzato e trasmissione professionale, pensato "
        "per giardinieri che cercano un 48 cm capace di lavorare ore senza "
        "scaldarsi. Per scheda completa e disponibilita', chiamaci.",
        [
            ("Larghezza taglio", "48 cm"),
            ("Telaio", "Acciaio rinforzato"),
            ("Trazione", "Semovente variabile"),
            ("Categoria", "Professionale"),
            ("Disponibilita'", "Chiamaci per info"),
            ("Assistenza", "Officina interna Bazzana"),
        ],
        "telaio in acciaio, lavoro continuo.",
    ),
    (
        "weibang-wb-384-rb",
        "WB 384 RB",
        "Robot tagliaerba",
        "Robot tagliaerba Weibang. Foto del modello in arrivo.",
        "Robot tagliaerba con perimetrale, programmazione automatica e ritorno "
        "in base. Per area massima coperta, autonomia e disponibilita', "
        "chiamaci o passa in negozio.",
        [
            ("Tipologia", "Robot tagliaerba"),
            ("Alimentazione", "Batteria + base ricarica"),
            ("Installazione", "Inclusa, dal nostro tecnico"),
            ("Disponibilita'", "Chiamaci per info"),
            ("Assistenza", "Officina interna Bazzana"),
            ("Garanzia", "Standard produttore"),
        ],
        "il prato si fa da solo.",
    ),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Weibang {model} — {category} · Motor Garden Bazzana</title>
<meta name="description" content="Weibang {model}: {category_lower}. Foto in arrivo. Cene (BG)." />
<meta name="theme-color" content="#0E0F0E" />
<meta property="og:type" content="product" />
<meta property="og:title" content="Weibang {model} — {category} · Motor Garden Bazzana" />
<meta property="og:description" content="Weibang {model}: {category_lower}. Foto in arrivo. Cene (BG)." />
<meta property="og:image" content="https://www.motorgardenbazzana.it/assets/brand/logo-bazzana.png" />
<meta property="og:locale" content="it_IT" />
<link rel="canonical" href="https://www.motorgardenbazzana.it/prodotti/{slug}.html" />

<link rel="icon" type="image/svg+xml" href="../assets/favicon/favicon.svg" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="image" href="../assets/brand/logo-bazzana.png" />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="../css/main.css?v=85" />
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Weibang {model}",
  "brand": {{ "@type": "Brand", "name": "Weibang" }},
  "category": "{category}",
  "image": "https://www.motorgardenbazzana.it/{img_rel}",
  "offers": {{
    "@type": "Offer",
    "availability": "https://schema.org/InStock",
    "priceCurrency": "EUR",
    "seller": {{ "@type": "LocalBusiness", "name": "Motor Garden Bazzana" }}
  }}
}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Vai al contenuto</a>
<div class="loader" aria-hidden="true">
  <div class="loader__inner">
    <div class="loader__logo">
      <div class="loader__logo-stage">
        <img src="../assets/brand/logo-bazzana.png" alt="" width="460" height="160" loading="eager" fetchpriority="high">
      </div>
    </div>
    <div class="loader__progress">
      <div class="loader__bar"></div>
      <div class="loader__meta">
        <span class="loader__brand">MOTOR GARDEN BAZZANA</span>
        <span class="loader__pct" aria-live="polite">000%</span>
      </div>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="site-header__inner">
    <a class="brand" href="../index.html" aria-label="Motor Garden Bazzana — Home"><img class="brand__logo" src="../assets/brand/logo-bazzana.png" alt="Motor Garden Bazzana" width="240" height="80"></a>
    <nav class="nav"><a href="../officina.html">Officina</a><a href="../prodotti.html" aria-current="page">Prodotti</a>
      <a href="../foto.html">Foto</a>
      <a href="../note.html">Blog</a>
      <a href="../storia.html">Storia</a><a href="../contatti.html">Contatti</a></nav>
    <div class="header-actions"><a class="tel-link" href="tel:+393464156981">346 4156981</a><button class="menu-toggle"><span></span></button></div>
  </div>
</header>
<div class="menu-overlay" aria-hidden="true"><div class="menu-overlay__top"><span class="mono">Menu</span><button class="menu-overlay__close">×</button></div><button type="button" class="menu-overlay__search" onclick="this.closest('.menu-overlay').classList.remove('is-open');document.body.style.overflow='';setTimeout(()=>{{var b=document.getElementById('nav-search-mobile');if(b)b.click();else{{var i=document.querySelector('.nav-search__input');if(i)i.focus();}}}},150);">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" width="18" height="18"><circle cx="11" cy="11" r="7.5"/><line x1="20.5" y1="20.5" x2="16.65" y2="16.65"/></svg>
    <span>Cerca prodotti</span>
  </button>
  <nav class="menu-overlay__list"><a href="../officina.html">Officina</a><a href="../prodotti.html">Prodotti</a>
      <a href="../foto.html">Foto</a>
      <a href="../note.html">Blog</a>
      <a href="../storia.html">Storia</a><a href="../contatti.html">Contatti</a></nav></div>
<main id="main" class="product" data-bzn-product data-brand="Weibang" data-model="{model}" data-category="{category}" data-description="{description_attr}" data-img="{img_rel}" data-specs="{specs_attr}">
  <p class="product__crumbs"><a href="../index.html">Home</a> / <a href="../prodotti.html">Prodotti</a> / Weibang {model}</p>
  <div class="product__grid">
    <div class="product__media reveal in"><img src="../{img_rel}" alt="Foto in arrivo — Weibang {model}" style="background:#f4f1ea; padding:1.5rem;" /></div>
    <div>
      <p class="product__brand reveal">Weibang · {category}</p>
      <h1 class="product__title reveal" data-delay="1">{model}<br/><em class="serif-italic">{tagline}</em></h1>
      <p class="product__lead reveal" data-delay="2">{lead}</p>
      <p class="product__desc reveal" data-delay="3">{description}</p>
      <dl class="spec reveal" data-delay="4">
{specs_html}      </dl>
      <div class="product__ctas reveal" data-delay="5">
        <a class="btn" href="https://wa.me/393464156981?text=Buongiorno%2C%20vorrei%20info%20sul%20Weibang%20{model_url}" target="_blank" rel="noopener">Chiedi info</a>
        <a class="btn btn--outline" href="../prodotti.html">Torna al catalogo</a>
      </div>
    </div>
  </div>
</main>
<footer class="site-footer">

  <!-- 1 · KINETIC TAGLINE STRIP -->
  <div class="site-footer__strip" aria-hidden="true">
    <div class="site-footer__strip-track">
      <span>Stihl official dealer</span><span class="site-footer__strip-dot"></span>
      <span>Officina autorizzata</span><span class="site-footer__strip-dot"></span>
      <span>Ricambi originali in 48h</span><span class="site-footer__strip-dot"></span>
      <span>Cene · Val Seriana</span><span class="site-footer__strip-dot"></span>
      <span>Aperti 2026 · esperienza decennale</span><span class="site-footer__strip-dot"></span>
      <span>Stihl · Active · Oleo-Mac · Kress · Shindaiwa · Ligier · Weibang · motori Honda</span><span class="site-footer__strip-dot"></span>
      <span>Stihl official dealer</span><span class="site-footer__strip-dot"></span>
      <span>Officina autorizzata</span><span class="site-footer__strip-dot"></span>
      <span>Ricambi originali in 48h</span><span class="site-footer__strip-dot"></span>
      <span>Cene · Val Seriana</span><span class="site-footer__strip-dot"></span>
      <span>Aperti 2026 · esperienza decennale</span><span class="site-footer__strip-dot"></span>
      <span>Stihl · Active · Oleo-Mac · Kress · Shindaiwa · Ligier · Weibang · motori Honda</span><span class="site-footer__strip-dot"></span>
    </div>
  </div>

  <div class="site-footer__inner">

    <!-- 2 · MAIN GRID -->
    <div class="site-footer__main">
      <div class="site-footer__brand">
        <a class="site-footer__brand-mark" href="../index.html" aria-label="Motor Garden Bazzana — Home">
          <img src="../assets/brand/logo-bazzana.png" alt="Motor Garden Bazzana" width="200" height="68" loading="lazy">
        </a>
        <p class="site-footer__motto">
          Cene, valle Seriana.<br>
          <em>Aperti 2026 — esperienza decennale.</em>
        </p>
        <ul class="site-footer__social" aria-label="Social e contatti rapidi">
          <li><a href="https://wa.me/393464156981?text=Ciao%21%20Vorrei%20info%20su%20Motor%20Garden%20Bazzana" target="_blank" rel="noopener" aria-label="WhatsApp">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19.05 4.91A9.82 9.82 0 0 0 12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01zM12.04 20.15c-1.48 0-2.93-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.26 8.26 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.24-8.24 2.2 0 4.27.86 5.82 2.42a8.18 8.18 0 0 1 2.41 5.83c.02 4.54-3.68 8.23-8.22 8.23z"/></svg>
          </a></li>
          <li><a href="https://www.instagram.com/bazzanamotorgarden/" target="_blank" rel="noopener" aria-label="Instagram">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
          </a></li>
          <li><a href="tel:+393464156981" aria-label="Telefono">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          </a></li>
          <li><a href="mailto:bazzanamotorgarden@gmail.com" aria-label="Email">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="2 6 12 13 22 6"/></svg>
          </a></li>
        </ul>
      </div>

      <nav class="site-footer__col" aria-label="Naviga">
        <h4 class="site-footer__h">Naviga</h4>
        <ul>
          <li><a href="../officina.html">Officina<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
          <li><a href="../prodotti.html">Prodotti<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
          <li><a href="../storia.html">Storia<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
          <li><a href="../contatti.html">Contatti<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
        </ul>
      </nav>

      <div class="site-footer__col">
        <h4 class="site-footer__h">Contatti</h4>
        <ul>
          <li><a href="tel:+393464156981">+39 346 4156981</a></li>
          <li><a href="https://wa.me/393464156981" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="mailto:bazzanamotorgarden@gmail.com">bazzanamotorgarden@gmail.com</a></li>
          <li><a href="https://www.instagram.com/bazzanamotorgarden/" target="_blank" rel="noopener">@bazzanamotorgarden</a></li>
        </ul>
      </div>

      <div class="site-footer__col site-footer__col--find">
        <h4 class="site-footer__h">Trovaci</h4>
        <address class="site-footer__addr">
          Via U. Bellora, 73<br>
          24020 Cene (BG)<br>
          Italia
        </address>
        <dl class="site-footer__hours">
          <dt>Lun-Ven</dt><dd>07:45-12:00 · 13:30-19:15</dd>
          <dt>Sabato</dt><dd>07:45-16:00</dd>
          <dt>Domenica</dt><dd>Chiuso</dd>
        </dl>
      </div>
    </div>

    <!-- 3 · KINETIC WORDMARK -->
    <div class="site-footer__kinetic" aria-hidden="true">
      <div class="site-footer__kinetic-track">
        <span class="site-footer__kinetic-word">{model}</span>
        <span class="site-footer__kinetic-sep">·</span>
        <span class="site-footer__kinetic-sub">Motor Garden</span>
        <span class="site-footer__kinetic-sep">·</span>
        <span class="site-footer__kinetic-word">{model}</span>
        <span class="site-footer__kinetic-sep">·</span>
        <span class="site-footer__kinetic-sub">Cene · Val Seriana</span>
        <span class="site-footer__kinetic-sep">·</span>
        <span class="site-footer__kinetic-word">{model}</span>
        <span class="site-footer__kinetic-sep">·</span>
        <span class="site-footer__kinetic-sub">Bazzana</span>
        <span class="site-footer__kinetic-sep">·</span>
      </div>
    </div>

    <!-- 4 · BOTTOM STRIP -->
    <div class="site-footer__bottom">
      <div class="site-footer__bottom-left">
        <span class="site-footer__copy">© <span data-year>2026</span> Motor Garden Bazzana</span><span class="site-footer__piva">P.IVA 04897880169</span>
      </div>
      <nav class="site-footer__legal" aria-label="Legal">
        <a href="../privacy.html">Privacy</a>
        <a href="../index.html">Home</a>
      </nav>
      <span class="site-footer__credit">Cene · BG · Italia</span>
    </div>
  </div>
</footer>
<div class="fab-stack" id="fab-stack" aria-label="Azioni rapide">
  <a class="fab-stack__btn fab-stack__btn--wa" href="https://wa.me/393464156981?text=Ciao%21%20Vorrei%20info%20su%20Motor%20Garden%20Bazzana" target="_blank" rel="noopener" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19.05 4.91A9.82 9.82 0 0 0 12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01zM12.04 20.15c-1.48 0-2.93-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.26 8.26 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.24-8.24 2.2 0 4.27.86 5.82 2.42a8.18 8.18 0 0 1 2.41 5.83c.02 4.54-3.68 8.23-8.22 8.23z"/></svg>
  </a>
  <a class="fab-stack__btn fab-stack__btn--phone" href="tel:+393464156981" aria-label="Chiama 346 4156981">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>
  <button class="fab-stack__btn fab-stack__btn--top" id="fab-top" aria-label="Torna su">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>
  </button>
</div>


<script src="../js/webp-upgrade.js?v=1" defer></script>
<script src="../js/main.js?v=45"></script>
<script src="../js/search-index.js?v=5" defer></script>
<script src="../js/search.js?v=4" defer></script>
<script src="../js/site-fx.js?v=53" defer></script>
<script src="../js/awwwards.js?v=35" defer></script>
<script src="../js/wow-fx.js?v=40" defer></script>
<script src="../js/photo-rich.js?v=39" defer></script>
<script src="../js/extras.js?v=41" defer></script>
<script src="../js/product-data.js?v=35" defer></script>
<script src="../js/product-pro.js?v=27" defer></script>
<script src="../js/pdf-scheda.js?v=2" defer></script>
<script src="../js/product-rotate-admin.js?v=1" defer></script>
</body>
</html>
"""


def build_specs_attr(specs):
    parts = []
    for label, value in specs:
        parts.append(
            '{&quot;label&quot;: &quot;' + label + '&quot;, '
            '&quot;value&quot;: &quot;' + value + '&quot;}'
        )
    return "[" + ", ".join(parts) + "]"


def build_specs_html(specs):
    rows = []
    for label, value in specs:
        rows.append(f"        <dt>{label}</dt><dd>{value}</dd>")
    return "\n".join(rows) + "\n"


def render_page(slug, model, category, lead, description, specs, tagline):
    svg_cat = CATALOG_MAP[slug][2]
    return TEMPLATE.format(
        slug=slug,
        model=model,
        category=category,
        category_lower=category.lower(),
        description_attr=description.replace('"', "&quot;"),
        description=description,
        lead=lead,
        tagline=tagline,
        model_url=model.replace(" ", "%20"),
        specs_attr=build_specs_attr(specs),
        specs_html=build_specs_html(specs),
        img_rel=catalog_img_path(svg_cat),
    )


def write_pages():
    for (slug, model, category, lead, description, specs, tagline) in MODELS:
        out = PRODOTTI / f"{slug}.html"
        out.write_text(
            render_page(slug, model, category, lead, description, specs, tagline),
            encoding="utf-8",
        )
        print(f"  scritto {out.relative_to(ROOT)}")


# ----------------------------------------------------------------------
# CATALOGO: sezione brand Weibang in prodotti.html
# ----------------------------------------------------------------------

CATALOG_CARD_TPL = """        <article class="depth-card" data-product-id="{pid}" data-product-name="{model}" data-product-brand="Weibang" data-product-cat="{cat}" data-product-img="{img}">
          <div class="depth-card__base">
            <img src="{img}" alt="Weibang {model} - {cat}" loading="lazy" decoding="async">
          </div>
          <div class="depth-card__overlay">
            <h4 class="depth-card__title">Weibang {model}</h4>
          </div>
          <div class="depth-card__info">
            <span class="depth-card__brand-tag">Weibang</span>
            <span class="depth-card__name">{model}</span>
            <span class="depth-card__hint">{cat}</span>
          </div>
        </article>"""


def build_catalog_section():
    """Genera l'HTML completo della sezione brand Weibang del catalogo.
    Organizza i prodotti per sottocategoria nell'ordine definito da CATALOG_ORDER.
    """
    # Mappa slug -> tupla MODELS
    by_slug = {m[0]: m for m in MODELS}

    # Raggruppa per sottocategoria di catalogo (NON la 'category' del modello,
    # ma la 'sottocategoria_catalogo' di CATALOG_MAP)
    groups = OrderedDict()
    for cat_label in CATALOG_ORDER:
        groups[cat_label] = []
    for slug, (pid, cat_label, svg_cat) in CATALOG_MAP.items():
        if slug not in by_slug:
            continue
        model = by_slug[slug][1]
        groups.setdefault(cat_label, []).append((pid, model, cat_label, svg_cat))

    lines = []
    lines.append('      <!-- WEIBANG:START -->')
    lines.append('      <!-- Sezione Weibang rasaerba professionali (placeholder per categoria, foto reali in arrivo) -->')
    lines.append('      <div class="brand-section" data-brand="weibang">')
    lines.append('        <h3 class="brand-section__title">Weibang</h3>')

    for cat_label, items in groups.items():
        if not items:
            continue
        slug = cat_slug(cat_label)
        lines.append(f'        <details class="cat-group" data-cat="{cat_label}" data-cat-slug="{slug}" open>')
        lines.append(f'          <summary class="cat-group__title">{cat_label}</summary>')
        lines.append('          <div class="cat-group__grid">')
        for pid, model, cat, svg_cat in items:
            card = CATALOG_CARD_TPL.format(
                pid=pid,
                model=model,
                cat=cat,
                img=catalog_img_path(svg_cat),
            )
            lines.append(card)
        lines.append('          </div>')
        lines.append('        </details>')

    lines.append('      </div>')
    lines.append('      <!-- WEIBANG:END -->')
    return "\n".join(lines)


def update_prodotti_html_section():
    """Sostituisce idempotentemente la sezione Weibang in prodotti.html.
    La sezione e' delimitata dai marker <!-- WEIBANG:START --> ... <!-- WEIBANG:END -->.
    Se i marker non esistono, li inserisce sostituendo la sezione corrente.
    """
    if not PRODOTTI_HTML.exists():
        print("  prodotti.html non trovato, salto")
        return
    text = PRODOTTI_HTML.read_text(encoding="utf-8")
    new_section = build_catalog_section()

    # Caso 1: marker presenti -> sostituisci tutto fra di loro
    marker_re = re.compile(
        r"      <!-- WEIBANG:START -->.*?      <!-- WEIBANG:END -->",
        re.DOTALL,
    )
    if marker_re.search(text):
        text = marker_re.sub(new_section, text)
        PRODOTTI_HTML.write_text(text, encoding="utf-8")
        print("  sezione Weibang rigenerata (via marker WEIBANG:START/END)")
        return

    # Caso 2: marker assenti -> trova la sezione attuale e sostituisci
    legacy_re = re.compile(
        r'      <!--[^\n]*Sezione Weibang[^\n]*-->\s*\n\s*<div class="brand-section" data-brand="weibang">.*?</div>\s*\n(?=</section>)',
        re.DOTALL,
    )
    m = legacy_re.search(text)
    if m:
        text = text[: m.start()] + new_section + "\n" + text[m.end():]
        PRODOTTI_HTML.write_text(text, encoding="utf-8")
        print("  sezione Weibang sostituita (legacy senza marker -> con marker)")
        return

    print("  ATTENZIONE: nessuna sezione Weibang trovata in prodotti.html, salto")


def update_marquee_in_existing_files():
    """Aggiunge ' Weibang ·' alla stringa marquee marchi se non gia' presente."""
    old = "Stihl · Active · Oleo-Mac · Kress · Shindaiwa · Ligier · motori Honda"
    new = "Stihl · Active · Oleo-Mac · Kress · Shindaiwa · Ligier · Weibang · motori Honda"

    targets = list(ROOT.glob("*.html")) + list((ROOT / "prodotti").glob("*.html")) + list((ROOT / "note").glob("*.html"))
    touched = 0
    for fp in targets:
        try:
            text = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if old in text and new not in text:
            text = text.replace(old, new)
            fp.write_text(text, encoding="utf-8")
            touched += 1
            print(f"  marquee aggiornato in {fp.relative_to(ROOT)}")
        elif new in text and fp.name.startswith("weibang-"):
            pass
    print(f"  totale file con marquee aggiornato: {touched}")


def update_sitemap():
    if not SITEMAP.exists():
        print("  sitemap.xml non trovato, salto")
        return
    text = SITEMAP.read_text(encoding="utf-8")
    today = "2026-05-27"
    base = "https://www.motorgardenbazzana.it/prodotti/"
    new_entries = []
    for (slug, *_rest) in MODELS:
        url = f"{base}{slug}.html"
        if url in text:
            continue
        new_entries.append(
            f"  <url><loc>{url}</loc><lastmod>{today}</lastmod><priority>0.6</priority></url>"
        )
    if not new_entries:
        print("  sitemap gia' contiene tutte le pagine Weibang")
        return
    inj = "\n".join(new_entries) + "\n"
    text = re.sub(r"(</urlset>\s*)$", inj + r"\1", text)
    SITEMAP.write_text(text, encoding="utf-8")
    print(f"  aggiunte {len(new_entries)} entry a sitemap.xml")


def main():
    print("Genero pagine Weibang...")
    write_pages()
    print()
    print("Aggiorno sezione catalogo Weibang in prodotti.html...")
    update_prodotti_html_section()
    print()
    print("Aggiorno marquee marchi nei file esistenti...")
    update_marquee_in_existing_files()
    print()
    print("Aggiorno sitemap.xml...")
    update_sitemap()
    print()
    print("Fatto.")


if __name__ == "__main__":
    main()
