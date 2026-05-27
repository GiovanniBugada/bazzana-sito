# ➕ Aggiungere un nuovo marchio al sito

> Procedura passo-passo per inserire un **brand completo** nel sito Bazzana.
> Riferimento operativo: come è stato fatto **Weibang** in v2.1.0.

---

## 🎯 Quando usare questa procedura

Usa questa procedura se vuoi aggiungere un marchio **come ottavo brand ufficiale**, cioè:
- ✅ Compare nella **griglia marchi** in home (`h3-brands`)
- ✅ Compare nel **marquee scrolling** in footer e header su tutte le pagine
- ✅ Ha una **chip filtro** e una **sezione brand dedicata** nel catalogo prodotti
- ✅ Ha 1+ **pagina dettaglio prodotto** stile MSI
- ✅ Ha entry in **search-index** e **sitemap.xml**

Se vuoi solo aggiungere **un prodotto a un brand esistente**, leggi invece la
sezione "Come aggiungere un prodotto" del [README](../README.md).

---

## 🪜 Steps (pattern Weibang)

### 1️⃣ Griglia marchi in home

📂 File: `index.html` (sezione `<section class="h3-brands">`, ~linea 296)

- Aggiungi un `<li class="h3-brand">` con nome e ruolo del brand
- Aggiorna numero marchi in `<h2>` (`Otto marche` → `Nove marche`, ecc.)
- Aggiorna la lead `<p>` con stesso numero

📂 File: `storia.html` (capitolo 03, ~linea 194)

- Stesso aggiornamento del numero ("otto filosofie", lista `<ul>` tag)
- Capitolo 05 (~linea 265): aggiorna "otto marchi in catalogo"

---

### 2️⃣ Marquee marchi (32 file HTML)

Aggiungi il nome del brand alla stringa marchi nei marquee footer e h3-marquee.

📂 Stringa da cercare:
```
Stihl · Active · Oleo-Mac · Kress · Shindaiwa · Ligier · Weibang · motori Honda
```

➡️ Aggiungi il nuovo brand (es. `· NuovoBrand`) prima di `· motori Honda`.

Usa lo script per applicare in batch:
```python
# scripts/aggiungi-brand-marquee.py (adatta da scripts/add-weibang-products.py)
old = "... · Weibang · motori Honda"
new = "... · Weibang · NuovoBrand · motori Honda"
# Sostituisci in tutti gli .html in root, prodotti/, note/
```

---

### 3️⃣ Catalogo prodotti

📂 File: `prodotti.html`

**A) Chip filtro** (~linea 130)
```html
<button class="chip" data-filter="nuovobrand">NuovoBrand</button>
```

**B) Sezione brand** (prima del `</section>` ~ ultima riga del main)
```html
<div class="brand-section" data-brand="nuovobrand">
  <h3 class="brand-section__title">NuovoBrand</h3>
  <details class="cat-group" data-cat="Categoria - Sottocategoria" data-cat-slug="categoria-sottocategoria" open>
    <summary class="cat-group__title">Categoria - Sottocategoria</summary>
    <div class="cat-group__grid">
      <article class="depth-card"
        data-product-id="nb1"
        data-product-name="Modello"
        data-product-brand="NuovoBrand"
        data-product-cat="Categoria - Sottocategoria"
        data-product-img="assets/img/placeholder-foto-arrivo.svg">
        <!-- ...card content... -->
      </article>
      <!-- altre card -->
    </div>
  </details>
</div>
```

⚠️ Lascia `placeholder-foto-arrivo.svg` finché le foto reali non arrivano (pattern Stihl iMow / Ligier / Weibang).

---

### 4️⃣ Pagine dettaglio prodotto

📂 File: `prodotti/nuovobrand-<modello>.html`

Modo veloce: **clona** una pagina Weibang esistente e modifica:
```powershell
copy prodotti/weibang-wb-506-scv.html prodotti/nuovobrand-modello-x.html
```

Poi sostituisci con find-replace:
- Titolo `<title>` e meta description
- `data-brand="NuovoBrand"` (capitalized) e `data-model="Modello X"`
- `data-description`, `data-specs` (JSON encoded con `&quot;`)
- Breadcrumb (linea ~76)
- Hero, lead, descrizione, tabella `<dl class="spec">`
- WhatsApp URL (`?text=...sul%20NuovoBrand%20Modello%20X`)
- Wordmark kinetic footer (3 occorrenze)
- Canonical URL

**Tip**: scrivi uno script Python `scripts/add-<brand>-products.py` (copia da `add-weibang-products.py`) per generare in batch.

---

### 5️⃣ Database prodotti `product-data.js`

📂 File: `js/product-data.js`

Aggiungi un oggetto per ogni modello, **prima** del `];` finale:

```js
{
  slug: 'nuovobrand-modello-x',
  brand: 'NuovoBrand',
  model: 'Modello X',
  modelFull: 'NuovoBrand Modello X',
  category: 'Categoria',
  tagline: 'Tagline breve.',
  lead: 'Sub-titolo descrittivo 25 parole.',
  description: 'Descrizione tecnica completa 80-120 parole...',
  specs: [
    { label: 'Specifica 1', value: 'Valore' },
    // ...
  ],
  highlights: [
    { title: 'Feature 1', value: 'Spiegazione.' },
    // ...
  ]
}
```

✅ Verifica con Python che non ci siano `,,` o squilibri di graffe:
```python
import re
text = open('js/product-data.js', encoding='utf-8').read()
print('Doppie virgole:', text.count(',,'))
print('Graffe bilanciate:', text.count('{') == text.count('}'))
```

---

### 6️⃣ Search index

📂 File: `scripts/build-search-index.py`

Aggiungi i mapping nel dict `DB_SLUGS`:
```python
("nuovobrand", "modello x"): "nuovobrand-modello-x",
```

Poi esegui:
```powershell
python scripts/build-search-index.py
```

---

### 7️⃣ Sitemap

📂 File: `sitemap.xml`

Aggiungi una `<url>` per ogni nuova pagina prodotto:
```xml
<url><loc>https://www.motorgardenbazzana.it/prodotti/nuovobrand-modello-x.html</loc><lastmod>2026-MM-DD</lastmod><priority>0.6</priority></url>
```

---

## 🧪 Verifica post-modifica

Apri il preview locale e verifica:

```powershell
python -m http.server 8790
```

Apri http://localhost:8790/prodotti.html → cerca:
- ✅ Chip "NuovoBrand" presente nel filtro
- ✅ Click sul chip → solo la sezione NuovoBrand visibile
- ✅ Le card hanno classe `has-detail` (link alla pagina prodotto)

Apri http://localhost:8790/prodotti/nuovobrand-modello-x.html → verifica:
- ✅ Hero, descrizione, specs, highlights renderizzati
- ✅ Link WhatsApp con nome brand+modello nel testo
- ✅ Console browser: 0 errori
- ✅ Network: nessun 404

Apri http://localhost:8790/index.html → verifica:
- ✅ Griglia marchi ha la nuova cella
- ✅ Marquee in footer cita NuovoBrand

---

## 📜 Checklist riassuntiva

- [ ] `index.html` — griglia marchi (`<li class="h3-brand">`) + numero "otto/nove..." aggiornato
- [ ] `index.html` — testi "sette marchi" → nuovo numero (3 occorrenze)
- [ ] `storia.html` — capitoli 03 e 05 (numero, lista tag)
- [ ] `prodotti.html` — chip filtro + sezione brand + card
- [ ] `prodotti/nuovobrand-*.html` — N pagine dettaglio
- [ ] `js/product-data.js` — N entry
- [ ] `scripts/build-search-index.py` — N mapping
- [ ] `python scripts/build-search-index.py` — rigenerato
- [ ] `sitemap.xml` — N entry
- [ ] Marquee marchi nei 32 file HTML (root + prodotti/ + note/)
- [ ] Preview locale: 0 errori console, 0 risorse 404
- [ ] Commit + push: `feat(brand): aggiungi marchio NuovoBrand`
- [ ] Aggiorna [`CHANGELOG.md`](../CHANGELOG.md) con entry `[Unreleased]` o nuova versione

---

> Pattern di riferimento: vedi commit `feat(weibang): ...` (v2.1.0, 2026-05-27).
