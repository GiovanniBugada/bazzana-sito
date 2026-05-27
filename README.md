# 🌿 Motor Garden Bazzana — sito v2

Sito **Awwwards-tier** per Motor Garden Bazzana, rivenditore ufficiale **Stihl** + officina autorizzata a **Cene (BG)**. Apertura **2026**.

> Otto marchi sotto un tetto: Stihl · Active · Oleo-Mac · Kress · Shindaiwa · Ligier · Weibang · motori Honda.

[![Status](https://img.shields.io/badge/status-WIP%202026-orange)]() [![Stack](https://img.shields.io/badge/stack-HTML%20%2B%20CSS%20%2B%20vanilla%20JS-blue)]() [![License](https://img.shields.io/badge/license-Proprietary-red)](LICENSE.txt)

---

## 📂 Struttura

```
bazzana_v2/
├── index.html              # 🏠 home con 11 sezioni cinematic
├── officina.html           # 🔧 timeline 4 step + brand grid + stats
├── prodotti.html           # 🛒 catalogo ~650 SKU con modal scheda
├── foto.html               # 📸 gallery 245 foto + lightbox
├── storia.html             # 📖 6 chapter sticky scroll storytelling
├── contatti.html           # ✉️  form GDPR + mappa OSM
├── note.html               # 📝 blog (12 articoli manutenzione)
├── privacy.html · 404.html
├── prodotti/*.html         # 🏷️  17 schede detail prodotto (MSI-style)
│                           #     Stihl × 4 · Honda × 3 · Active × 2 · Ligier × 1
│                           #     Weibang × 6 · Geotech × 1
├── assets/
│   ├── brand/              # logo Bazzana
│   ├── img/bazzana/        # 245 foto showroom + 31 scene
│   ├── img/prodotti/       # foto catalog isolate (PNG/WEBP/AVIF)
│   ├── img/hero/           # immagini hero esterne/insegne
│   ├── img/officina/       # foto officina e attrezzi
│   ├── img/ambiente/       # showroom e scenari
│   └── favicon/
├── css/
│   ├── main.css            # entry — importa tutti i moduli
│   ├── tokens.css reset.css typography.css layout.css components.css motion.css shell.css
│   └── pages/
│       ├── awwwards.css           # design override definitivo
│       ├── photo-rich.css         # feature pin + hscroll + featured
│       ├── product-pro.css        # detail page MSI-style
│       ├── storia-pro.css         # storia sticky chapter
│       ├── officina-pro.css       # officina redesign
│       ├── foto-gallery.css       # gallery 245 foto
│       ├── catalog-pro.css        # catalog + modal scheda
│       ├── loader-pro.css         # caricamento cinematografico ricco
│       ├── loader-cinematic.css   # SVG mask reveal loader
│       ├── wow-moments.css        # hero scene, konami
│       ├── mobile-fixes.css       # 320px + reduced-motion
│       ├── newsletter.css         # footer mini-form
│       ├── cinematic.css          # palette ricca + animazioni
│       ├── interior.css           # rifiniture
│       └── polish-final.css
├── js/
│   ├── main.js                    # loader, header, base reveal
│   ├── site-fx.js                 # cursor, scroll bar, newsletter auto-inject
│   ├── awwwards.js                # parallax, magnetic, tilt, reveal
│   ├── wow-fx.js                  # hero scene, konami, confetti
│   ├── photo-rich.js              # feature pin, hscroll, image zoom
│   ├── product-pro.js             # scheda prodotto MSI-style
│   ├── product-data.js            # database 17 prodotti dettagliati
│   ├── catalog-pro.js             # modal scheda ~650 prodotti
│   ├── storia-pro.js              # storia chapter animations
│   ├── foto-gallery.js            # gallery + lightbox
│   ├── foto-manifest.js           # 245 foto manifest auto-generato
│   ├── search.js + search-index.js # ricerca live (~650 prodotti)
│   ├── extras.js                  # toast, search, fab
│   ├── webp-upgrade.js            # upgrade JPG → WEBP runtime
│   ├── pdf-scheda.js              # generatore PDF scheda
│   ├── product-rotate-admin.js    # admin rotazione foto
│   └── compare.js                 # confronto prodotti
├── scripts/                # 🐍 tool Python per import foto, build index, ecc.
└── docs/                   # 📑 documentazione progetto (brief, deploy, roadmap)
```

---

## 🏷️ Marchi trattati (8)

| Marchio    | Specializzazione           | Schede detail |
|------------|----------------------------|---------------|
| Stihl      | Rivenditore ufficiale      | 4             |
| Honda      | Motori GCV / GXV           | 3             |
| Active     | Made in Italy              | 2             |
| Oleo-Mac   | Emak Group                 | catalogo      |
| Kress      | Robot & batteria           | catalogo      |
| Shindaiwa  | Forestry pro               | catalogo      |
| Ligier     | Microcar L6e               | 1             |
| **Weibang**| **Rasaerba pro** (nuovo)   | **6**         |

---

## ➕ Come aggiungere un prodotto

### A) Aggiungere al catalogo (`prodotti.html`)
Apri `prodotti.html`, copia un blocco `<article class="depth-card">` esistente. Modifica:
- `data-product-id` univoco (es. `weib7`)
- `data-product-name="Nome modello"`
- `data-product-brand="Brand"`
- `data-product-cat="Categoria - Sottocategoria"`
- `data-product-img="assets/img/prodotti/foto/path.png"` (o `placeholder-foto-arrivo.svg` se foto in arrivo)

Il modal scheda + descrizione fallback si generano automaticamente da `catalog-pro.js`.
Poi rilancia `python scripts/build-search-index.py` per aggiornare la search.

### B) Aggiungere scheda detail completa
1. Copia un file in `prodotti/` (es. `weibang-wb-506-scv.html` per un placeholder)
2. Aggiungi entry in `js/product-data.js`:
```js
{
  slug: 'nuovo-prodotto',
  brand: 'Brand',
  model: 'Modello',
  modelFull: 'Brand Modello completo',
  category: 'Categoria',
  tagline: 'Tagline breve',
  lead: 'Sub-titolo 25 parole',
  description: 'Descrizione tecnica 80-120 parole',
  specs: [ { label: 'Cilindrata', value: '45.6 cc' } /* ... */ ],
  highlights: [ { title: 'Sistema X', value: '...' } /* ... */ ]
}
```
3. Aggiungi mapping in `scripts/build-search-index.py` (`DB_SLUGS`)
4. Rilancia `python scripts/build-search-index.py`
5. Aggiungi URL a `sitemap.xml`

### C) Aggiungere un intero marchio nuovo (pattern Weibang)
Riferimento: [`docs/aggiungere-un-marchio.md`](docs/aggiungere-un-marchio.md)

---

## 📸 Come aggiungere foto

### Foto galleria (`foto.html` — 245 attuali)
1. Copia i JPG originali in `C:/Users/ilbug/Desktop/scuola/gestione/foto bazzana/`
2. Esegui `python scripts/import-all-photos.py`
3. Le foto vengono ottimizzate (1400px, q=80) in `assets/img/bazzana/foto-XXX.jpg` e `js/foto-manifest.js` viene rigenerato

### Foto-scena (sezioni home / storia / officina)
Aggiungi a `assets/img/bazzana/scena-XX.jpg`, poi modifica `<img src>` nelle pagine specifiche.

### Foto prodotto in arrivo
Usa `assets/img/placeholder-foto-arrivo.svg` come `data-img` finché la foto reale non arriva
(pattern usato per **Stihl iMow**, **Ligier**, **Weibang**).

---

## ⚙️ Come modificare contenuti rapidi

| Cosa | Dove |
|------|------|
| Hero home title | `index.html` ~linea 134 |
| Griglia marchi | `index.html` ~linea 296 (sezione `h3-brands`) |
| Footer motto / marquee marchi | tutte le pagine — rilancia `python scripts/rewrite-footer.py` |
| Orari | tutte le pagine, cerca `.site-footer__hours` |
| Telefono / email / indirizzo | tutte le pagine — sono hard-coded |
| Nav menu | tutte le pagine, oppure rilancia `python scripts/add-foto-nav.py` |

---

## 🔢 Versioning cache

Tutti CSS+JS hanno `?v=N`. Quando modifichi un file, bumpa la versione in tutti gli HTML con uno script Python.

---

## ✨ Animazioni implementate

- 🎬 **Loader cinematic**: SVG mask reveal + count-up + tagline + gradient typography
- 🎢 **Hero scroll-driven scene change**: foto entra a destra al primo scroll
- 📌 **Sticky feature pin**: foto sticky + 3 step crossfade
- ↔️ **Horizontal scroll showcase**: pinning + 5 panel orizzontali
- 🖱️ **Cursor custom**: dot 5px + ring 30px fluido lerp + easter eggs (🔧🌿📍)
- 🎮 **Konami code** `↑↑↓↓←→←→BA` → modal easter egg
- 🎉 **Confetti** su submit form contatti
- 🧲 **Magnetic CTA**: bottoni seguono il cursore
- 🌀 **3D tilt** su dual-focus + featured strip
- 🎭 **Image clip-path reveal**: mask animation su entrata viewport
- 🔄 **Page transition** fade tra pagine
- 📰 **Newsletter footer** auto-inject su tutte le pagine
- 🖼️ **Lightbox foto** click → fullscreen con frecce keyboard

---

## 🧱 Stack

- HTML5 puro + CSS3 (`clamp`, `grid`, `sticky`, `clip-path`, `backdrop-filter`)
- JS vanilla ES6+ — **no framework**
- Form: FormSubmit
- Mappa: OpenStreetMap embed
- Fonts: **Fraunces** + **Inter** + **JetBrains Mono** (Google Fonts)
- Build/tool: Python (script di import foto + indici)

---

## 🌐 Browser support

Chrome / Edge / Safari / Firefox ultime 2 major. iOS Safari 14+.
Mobile-first 320px → 1920px+. Touch + mouse + tastiera.
`prefers-reduced-motion` rispettato.

---

## 🎯 Performance target

- ⚡ Lighthouse Performance 90+
- ♿ Accessibility 100 / 🔍 SEO 100 / ✅ Best Practices 95+
- 🖼️ Images: lazy + EXIF + JPEG q=80 (+ upgrade runtime a WEBP)
- 📦 Critical CSS inline: TODO (build step futuro)

---

## 📑 Documentazione estesa

| Documento | Contenuto |
|-----------|-----------|
| [`docs/business-brief.md`](docs/business-brief.md) | Obiettivi del progetto, target audience, KPI |
| [`docs/studio-fattibilita.md`](docs/studio-fattibilita.md) | Studio fattibilità tecnica e business |
| [`docs/roadmap.md`](docs/roadmap.md) | Roadmap funzionalità future |
| [`docs/deploy.md`](docs/deploy.md) | Come pubblicare il sito |
| [`docs/aggiungere-un-marchio.md`](docs/aggiungere-un-marchio.md) | Procedura aggiunta nuovo brand (es. Weibang) |
| [`CHANGELOG.md`](CHANGELOG.md) | Cronologia rilasci |
| [`LICENSE.txt`](LICENSE.txt) | Licenza proprietaria |

---

## ☎️ Contatti business

- **Tel**: +39 346 4156981
- **Email**: bazzanamotorgarden@gmail.com
- **Instagram**: [@bazzanamotorgarden](https://www.instagram.com/bazzanamotorgarden/)
- **WhatsApp**: [wa.me/393464156981](https://wa.me/393464156981)
- **Indirizzo**: Via U. Bellora 73, 24020 Cene (BG)
- **Orari**: Lun-Ven 07:45-12:00 · 13:30-19:15 · Sab 07:45-16:00 · Dom chiuso
- **P.IVA**: 02234180169

---

<sub>© Motor Garden Bazzana — Cene (BG) · Val Seriana · Italia · 2026</sub>
