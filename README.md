# Motor Garden Bazzana — sito v2

Sito **Awwwards-tier** per Motor Garden Bazzana, rivenditore Stihl + officina autorizzata a Cene (BG). Apertura 2026.

## Struttura

```
bazzana_v2/
├── index.html              # home con 11 sezioni cinematic
├── officina.html           # timeline 4 step + brand grid + stats
├── prodotti.html           # catalogo 519 SKU con modal scheda
├── foto.html               # gallery 245 foto + lightbox
├── storia.html             # 6 chapter sticky scroll storytelling
├── contatti.html           # form GDPR + mappa OSM
├── privacy.html · 404.html
├── prodotti/*.html         # 15 schede detail prodotto (MSI-style)
├── assets/
│   ├── brand/              # logo
│   ├── img/bazzana/        # 245 foto showroom + 31 scene
│   ├── img/prodotti/       # foto catalog isolate (PNG)
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
│       ├── loader-cinematic.css   # SVG mask reveal loader
│       ├── wow-moments.css        # hero scene, konami, audio
│       ├── mobile-fixes.css       # 320px + reduced-motion
│       ├── newsletter.css         # footer mini-form
│       └── polish-final.css
└── js/
    ├── main.js                    # loader, header, base reveal
    ├── site-fx.js                 # cursor, scroll bar, newsletter auto-inject
    ├── awwwards.js                # parallax, magnetic, tilt, reveal
    ├── wow-fx.js                  # hero scene, konami, confetti, audio toggle
    ├── photo-rich.js              # feature pin, hscroll, image zoom
    ├── product-pro.js             # scheda prodotto MSI-style
    ├── product-data.js            # database 15 prodotti
    ├── catalog-pro.js             # modal scheda 519 prodotti
    ├── storia-pro.js              # storia chapter animations
    ├── foto-gallery.js            # gallery + lightbox
    ├── foto-manifest.js           # 245 foto manifest auto-generato
    ├── extras.js                  # toast, search, fab
    └── compare.js                 # confronto prodotti
```

## Come aggiungere un prodotto

### A) Aggiungere al catalogo (prodotti.html)
Apri `prodotti.html`, copia un blocco `<article class="depth-card">` esistente. Modifica:
- `data-product-id` univoco
- `data-product-name="Nome modello"`
- `data-product-brand="Brand"`
- `data-product-cat="Categoria - Sottocategoria"`
- `data-product-img="assets/img/prodotti/foto/path.png"`

Il modal scheda + descrizione fallback si generano automaticamente da `catalog-pro.js`.

### B) Aggiungere scheda detail completa (oltre le 15 attuali)
1. Copia un file in `prodotti/` (es. `stihl-ms-251.html`)
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
  specs: [ { label: 'Cilindrata', value: '45.6 cc' }, ... ],
  highlights: [ { title: 'Sistema X', value: '...' }, ... ]
}
```
3. Aggiungi URL a `sitemap.xml`

## Come aggiungere foto

### Foto galleria (foto.html — 245 attuali)
1. Copia i JPG originali in `C:/Users/ilbug/Desktop/scuola/gestione/foto bazzana/`
2. Esegui `python scripts/import-all-photos.py`
3. Le foto vengono ottimizzate (1400px, q=80) in `assets/img/bazzana/foto-XXX.jpg` e `js/foto-manifest.js` viene rigenerato

### Foto-scena (sezioni home / storia / officina)
Aggiungi a `assets/img/bazzana/scena-XX.jpg`, poi modifica `<img src>` nelle pagine specifiche.

## Come modificare contenuti rapidi

| Cosa | Dove |
|---|---|
| Hero home title | `index.html` ~linea 134 |
| Footer motto | tutte le pagine — rilancia `python scripts/rewrite-footer.py` |
| Orari | tutte le pagine, cerca `.site-footer__hours` |
| Telefono / email / indirizzo | tutte le pagine — sono hard-coded |
| Nav menu | tutte le pagine, oppure rilancia `python scripts/add-foto-nav.py` |

## Versioning cache

Tutti CSS+JS hanno `?v=N`. Quando modifichi un file, bumpa la versione in tutti gli HTML con uno script Python.

## Animazioni implementate

- **Loader cinematic**: SVG mask reveal + count-up + tagline
- **Hero scroll-driven scene change**: foto entra a destra al primo scroll
- **Sticky feature pin**: foto sticky + 3 step crossfade
- **Horizontal scroll showcase**: pinning + 5 panel orizzontali
- **Cursor custom**: dot 5px + ring 30px fluido lerp + easter eggs (🔧🌿📍)
- **Konami code** `↑↑↓↓←→←→BA` → modal easter egg
- **Confetti** su submit form contatti
- **Magnetic CTA**: bottoni seguono il cursore
- **3D tilt** su dual-focus + featured strip
- **Image clip-path reveal**: mask animation su entrata viewport
- **Audio ambient toggle** ♪ (file `assets/audio/ambient.mp3` opzionale)
- **Page transition** fade tra pagine
- **Newsletter footer** auto-inject su tutte le pagine
- **Lightbox foto** click → fullscreen con frecce keyboard

## Stack

- HTML5 puro + CSS3 (clamp, grid, sticky, clip-path, backdrop-filter)
- JS vanilla ES6+ — no framework
- Form: FormSubmit
- Mappa: OpenStreetMap embed
- Fonts: Fraunces + Inter + JetBrains Mono (Google Fonts)

## Browser support

Chrome / Edge / Safari / Firefox ultime 2 major. iOS Safari 14+.
Mobile-first 320px → 1920px+. Touch + mouse + tastiera.
`prefers-reduced-motion` rispettato.

## Performance target

- Lighthouse Performance 90+
- Accessibility 100 / SEO 100 / Best Practices 95+
- Images: lazy + EXIF + JPEG q=80
- Critical CSS inline: TODO (build step futuro)

## Contatti business

- **Tel**: +39 346 4156981
- **Email**: bazzanamotorgarden@gmail.com
- **Instagram**: [@bazzanamotorgarden](https://www.instagram.com/bazzanamotorgarden/)
- **WhatsApp**: https://wa.me/393464156981
- **Indirizzo**: Via U. Bellora 73, 24020 Cene (BG)
- **Orari**: Lun-Ven 07:45-12:00 · 13:30-19:15 · Sab 07:45-16:00 · Dom chiuso
- **P.IVA**: 02234180169
