# 🏍️ Motor Garden Bazzana — Sito ufficiale

Sito vetrina **Awwwards-tier** per **Motor Garden Bazzana**
Rivenditore ufficiale **Stihl** + officina autorizzata a **Cene (BG)** — Apertura 2026

🌐 **Live:** [www.motorgardenbazzana.it](https://www.motorgardenbazzana.it)
📦 **Repo:** [GitHub.com/GiovanniBugada/bazzana-sito](https://github.com/GiovanniBugada/bazzana-sito)

---

## 📞 Contatti business

| | |
|---|---|
| **Indirizzo** | Via U. Bellora 73, 24020 Cene (BG) |
| **Telefono** | [+39 346 4156981](tel:+393464156981) |
| **WhatsApp** | [wa.me/393464156981](https://wa.me/393464156981) |
| **Email** | bazzanamotorgarden@gmail.com |
| **Instagram** | [@bazzanamotorgarden](https://www.instagram.com/bazzanamotorgarden/) |
| **P.IVA** | 04897880169 |
| **Orari** | Lun–Ven 07:45–12:00 · 13:30–19:15 · Sab 07:45–16:00 · Dom chiuso |

---

## 🏷️ Gli 8 marchi trattati

| Marchio | Tipologia | Schede detail |
|---|---|---|
| **Stihl** | Rivenditore ufficiale | 4 |
| **Honda** | Motori GCV / GXV, generatori, rasaerba | 3 |
| **Active** | Decespugliatori + rasaerba Made in Italy | 2 |
| **Oleo-Mac** | Emak Group | catalogo |
| **Kress** | Robot & batteria | catalogo |
| **Shindaiwa** | Forestry pro made in Giappone | catalogo |
| **Ligier** | Microcar L6e | 1 |
| **Weibang** | Rasaerba professionali | 11 |
| **Geotech** | Biotrituratore | 1 |

**Totale schede detail prodotto:** 22

---

## 📂 Struttura cartelle

```
bazzana_v2/
│
├── 🏠 PAGINE PUBBLICHE (URL del sito)
│   ├── index.html              Home cinematic (11 sezioni)
│   ├── officina.html           Timeline 4 step + brand grid + 3 stats
│   ├── prodotti.html           Catalogo 650 SKU con modal scheda
│   ├── foto.html               Gallery 129 foto + lightbox
│   ├── storia.html             6 chapter sticky scroll
│   ├── contatti.html           Form GDPR + mappa OSM
│   ├── note.html               Blog (12 articoli manutenzione)
│   ├── privacy.html            Privacy policy GDPR
│   └── 404.html                Pagina errore
│
├── 🔍 SEO / CRAWLER (root obbligatorio)
│   ├── robots.txt              Direttive crawler (blocca admin/scripts/docs)
│   ├── sitemap.xml             Sitemap pubblico
│   └── favicon.ico             Favicon multi-res 16/32/48
│
├── 📋 DOCUMENTAZIONE (in root, standard GitHub)
│   ├── README.md               Questo file
│   └── LICENSE.txt             Licenza MIT
│
├── 🔐 admin/
│   └── admin-rotate.html       Tool admin per ruotare foto galleria
│
├── prodotti/               🏷️  22 schede detail (MSI-style)
│   ├── stihl-*.html        (4: MS 251, FS 131, BG 86, iMow)
│   ├── honda-*.html        (3: EU22i, HRN 536, HRX 476)
│   ├── active-*.html       (2: 4860 SA, AC900)
│   ├── ligier-myli.html    (1)
│   ├── weibang-*.html      (11: gamma rasaerba)
│   ├── cippatore-tritone.html
│   └── dettaglio.html      (template generico)
│
├── note/                   📝 12 articoli blog
│
├── assets/
│   ├── brand/              Logo Motor Garden Bazzana
│   ├── favicon/            favicon.ico + PNG + SVG + Apple touch icon
│   ├── img/
│   │   ├── hero/           Foto facciata + insegne
│   │   ├── bazzana/        129 foto showroom + 31 scene
│   │   ├── ambiente/       Showroom + scenari
│   │   ├── officina/       Banco + attrezzi
│   │   ├── storia/         Hero capitoli storia
│   │   ├── note/           Foto articoli blog
│   │   └── prodotti/
│   │       ├── foto-catalogo/   PNG isolate ~500 prodotti
│   │       ├── weibang/         11 foto Weibang reali
│   │       └── *.jpg            Foto schede dettaglio
│
├── css/
│   ├── main.css            Entry — importa 38 moduli
│   ├── tokens.css reset.css typography.css …
│   └── pages/
│       ├── awwwards.css         Design layer definitivo
│       ├── mobile-perf.css      Fix mobile + perf
│       ├── search.css           Search overlay
│       ├── catalog-pro.css      Catalog + modal
│       ├── foto-gallery.css     Gallery 129 foto
│       ├── storia-pro.css       Storia chapter
│       └── …
│
├── js/
│   ├── main.js              Page transition + filters
│   ├── search.js            Live search (~650 prodotti)
│   ├── search-index.js      Indice generato da Python
│   ├── catalog-pro.js       Modal scheda
│   ├── foto-gallery.js      Gallery + lightbox + swipe
│   ├── product-pro.js       Scheda detail MSI-style
│   ├── webp-upgrade.js      Runtime WebP swap
│   ├── awwwards.js photo-rich.js storia-pro.js …
│   └── site-fx.js extras.js wow-fx.js
│
├── scripts/                🐍 Tool Python attivi
│   ├── build-search-index.py        Rigenera search-index.js
│   ├── compress-heavy-images.py     Comprime foto > 500KB
│   ├── compress-catalog-images.py   Comprime PNG catalog
│   ├── reencode-quality.py          Re-encode q=88 + WebP
│   ├── install-weibang-photos.py    Pattern per installare foto fornitore
│   ├── generate-favicon.py          Genera set favicon da logo
│   ├── import-all-photos.py         Import iniziale foto bazzana
│   ├── add-*-products.py            Pattern aggiunta nuovo marchio
│   ├── build-blog.py                Build articoli blog
│   ├── rewrite-footer.py            Sync footer su tutte le pagine
│   ├── convert-to-webp.py           Genera WebP companion
│   ├── webp-rebuild-bazzana.py
│   └── _archive/                    Script audit one-off già usati
│
└── docs/
    ├── README.md                Index documentazione
    ├── CHANGELOG.md             Cronologia rilasci
    ├── foto-da-fornire.txt      📋 LISTA 138 FOTO da fornire
    ├── idea-progetto.md         Brainstorm iniziale
    ├── business-brief.md        Obiettivi, target, KPI
    ├── studio-fattibilita.md    Studio fattibilità
    ├── roadmap.md               Roadmap future features
    ├── deploy.md                Come pubblicare il sito
    ├── aggiungere-un-marchio.md Pattern aggiunta brand
    ├── requirements.md          Requisiti tecnici
    ├── economy_finance/         Budget + Gantt
    └── fattibilità/             Studio di fattibilità .docx
```

---

## 🚀 Come ci lavoro / Come modificarlo

### A) Aggiungere un prodotto al catalogo (`prodotti.html`)

1. Copia un `<article class="depth-card">` esistente
2. Modifica:
   - `data-product-id` univoco
   - `data-product-name` nome modello
   - `data-product-brand` brand
   - `data-product-cat` "Categoria - Sottocategoria"
   - `data-product-img` path foto (o `placeholder-foto-arrivo.svg`)
3. `python scripts/build-search-index.py` per aggiornare la search

### B) Aggiungere scheda detail completa

1. Copia un file in `prodotti/` (es. `weibang-wb-506-scv.html`)
2. Aggiungi entry in `js/product-data.js`
3. Aggiungi mapping in `scripts/build-search-index.py` (`DB_SLUGS`)
4. `python scripts/build-search-index.py`
5. Aggiungi URL a `sitemap.xml`

### C) Aggiungere foto galleria (`foto.html`)

1. Copia JPG originali in `C:/Users/ilbug/Desktop/scuola/gestione/foto bazzana/`
2. `python scripts/import-all-photos.py` (ottimizza 1400px q=80 + WebP)

### D) Aggiungere foto scheda detail

1. Salva la foto in `assets/img/prodotti/`
2. Aggiorna `data-img` nella scheda HTML
3. Aggiorna `og:image` e JSON-LD `image`

---

## ⚙️ Modifiche comuni rapide

| Cosa | Dove |
|---|---|
| Title hero home | `index.html` ~linea 153 |
| Grid 8 marchi | `index.html` ~linea 305 (`h3-brands`) |
| Footer motto / marquee | tutte le pagine — rilancia `python scripts/rewrite-footer.py` |
| Orari | tutte le pagine, cerca `.site-footer__hours` |
| Tel/email/indirizzo | hardcoded ovunque |
| Nav menu | tutte le pagine, oppure `python scripts/add-foto-nav.py` |
| P.IVA | hardcoded — è `04897880169` |

---

## 🔢 Versioning cache

Tutti CSS+JS hanno `?v=N`. Quando modifichi un file, bumpa la versione in tutti gli HTML.

**Versioni attuali (Maggio 2026):**
- `css/main.css?v=99`
- `js/main.js?v=48`
- `js/awwwards.js?v=46`, `wow-fx.js?v=46`, `extras.js?v=46`
- `favicon.ico?v=2`

---

## ✨ Animazioni / Interazioni

- 🎬 **Loader cinematic** — SVG mask reveal + count-up + gradient typography
- 🎢 **Hero scroll-driven** — foto entra a destra al primo scroll
- 📌 **Sticky feature pin** — foto sticky + 3 step crossfade
- ↔️ **Horizontal scroll showcase** — pinning + 5 panel orizzontali
- 🖱️ **Cursor custom** — dot + ring lerp inerziale (solo desktop)
- 🎮 **Konami code** `↑↑↓↓←→←→BA` → modal easter egg
- 🎉 **Confetti** su submit form contatti
- 🧲 **Magnetic CTA** — bottoni seguono il cursore
- 🌀 **3D tilt** su card dual-focus
- 🎭 **Image clip-path reveal** — mask animation su entrata viewport
- 🔄 **Page transition** dark curtain + bfcache safe
- 🖼️ **Lightbox foto** — swipe touch + keyboard arrows
- 🔍 **Search live** con fuzzy + Levenshtein (~650 prodotti)

---

## 🧱 Stack

- **HTML5** puro + **CSS3** (clamp, grid, sticky, clip-path, backdrop-filter)
- **JS vanilla ES6+** — no framework
- **Form**: FormSubmit
- **Mappa**: OpenStreetMap embed
- **Font**: Fraunces + Inter + JetBrains Mono (Google Fonts, display=swap)
- **Build tool**: Python (script import foto + indici)

---

## 🌐 Browser support

Chrome / Edge / Safari / Firefox **ultime 2 major**
iOS Safari **14+**, Android Chrome **108+**
Mobile-first 320px → 1920px+
Touch + mouse + tastiera supportati
`prefers-reduced-motion` rispettato

---

## 🎯 Performance attuale

| Metric | Valore |
|---|---|
| Peso totale `assets/img/` | **131 MB** (era 280 MB, -150 MB) |
| Foto hero (facciata) | **250 KB JPG / 154 KB WebP** (era 3.8 MB) |
| DOMContentLoaded home (375px) | **157 ms** |
| FPS scroll catalogo 650 card | **63 fps medio / 32 min** |
| Frame slow (<30fps) | **0** |
| Lighthouse target | Performance 90+ |
| Accessibility | 100 |
| SEO | 100 |
| Best Practices | 95+ |

---

## 🔧 Ottimizzazioni applicate

- ✅ **`<picture>` con `<source webp>`** — 44 immagini hero servono WebP direttamente dal parse HTML
- ✅ **WebP companion** generato per **ogni** JPG/PNG (q=85)
- ✅ **JPG q=88 + chroma 4:4:4** — niente artefatti su rossi/verdi
- ✅ **`content-visibility: auto`** sulle 650 card del catalogo → skip render off-screen
- ✅ **`fetchpriority="low"`** sulle img catalogo → no blocco rete
- ✅ **`loading="lazy"` + `decoding="async"`** ovunque
- ✅ **`defer`** su `main.js` → no blocco parsing HTML
- ✅ **`mix-blend-mode: normal` + isolation** su search → no trasparenza
- ✅ **`backdrop-filter: blur(6px)`** ridotto solo su header sticky (era blur 20px)
- ✅ **`format-detection: telephone=no`** → P.IVA non parte come chiamata su iOS
- ✅ **`pageshow` listener** in main.js → bfcache funziona, back button OK
- ✅ **Foto Honda HRN/HRX** ruotate correttamente (EXIF + auto-rotate)

---

## 🛠️ Quality assurance

- ✅ **0 refusi italiani** (audit completo)
- ✅ **0 immagini rotte** (audit programmatico)
- ✅ **0 link interni rotti** (verificato via Python su 44 file HTML)
- ✅ **Schema.org JSON-LD** su 22 schede prodotto + LocalBusiness
- ✅ **Cross-device** verificato 320/360/375/414/768/1024/1280/1440/1920 px
- ✅ **Touch + click + keyboard** tutte interazioni funzionanti
- ✅ **Contatti coerenti** (tel/email/IG/P.IVA/indirizzo) in tutte le 44 pagine

---

## 📑 Documentazione estesa

| Documento | Contenuto |
|---|---|
| [`docs/foto-da-fornire.txt`](docs/foto-da-fornire.txt) | **Lista 138 foto da fornire** (8 schede + 130 catalog) |
| [`docs/idea-progetto.md`](docs/idea-progetto.md) | Idea originale (brainstorm iniziale) |
| [`docs/business-brief.md`](docs/business-brief.md) | Obiettivi, target, KPI |
| [`docs/studio-fattibilita.md`](docs/studio-fattibilita.md) | Studio fattibilità tecnica e business |
| [`docs/roadmap.md`](docs/roadmap.md) | Roadmap funzionalità future |
| [`docs/deploy.md`](docs/deploy.md) | Come pubblicare il sito |
| [`docs/aggiungere-un-marchio.md`](docs/aggiungere-un-marchio.md) | Pattern aggiunta nuovo brand (es. Weibang) |
| [`CHANGELOG.md`](CHANGELOG.md) | Cronologia rilasci |
| [`LICENSE.txt`](LICENSE.txt) | Licenza MIT |

---

## 📝 Lista foto mancanti (TOP priority)

Le **8 foto schede detail** da fornire al collaboratore per primo:

1. **Active AC900** (motozappa)
2. **Honda EU22i** (generatore inverter)
3. **Honda HRN 536** (rasaerba mulching)
4. **Ligier Myli** (microcar elettrica)
5. **Stihl BG 86** (soffiatore)
6. **Stihl FS 131** (decespugliatore)
7. **Stihl iMow 6 EVO** (robot tagliaerba)
8. **Stihl MS 251** (motosega)

> Lista completa con 130 foto catalog: [`docs/foto-da-fornire.txt`](docs/foto-da-fornire.txt)

---

<sub>© Motor Garden Bazzana — Cene (BG) · Val Seriana · Italia · 2026
Progetto sviluppato da **Giovanni Bugada** e **Bruno Baldassarri**</sub>
