# 📜 Changelog

Tutte le modifiche notevoli al progetto **Motor Garden Bazzana — sito v2** sono documentate qui.
Il formato segue [Keep a Changelog](https://keepachangelog.com/it/1.1.0/) e il versionamento segue [SemVer](https://semver.org/lang/it/).

---

## [Unreleased]

### 🚀 In arrivo
- Foto reali dei modelli Weibang (sostituiranno il placeholder `placeholder-foto-arrivo.svg`)
- Integrazione Behold.so per il feed Instagram nella sezione "Live dal banco"
- Critical CSS inline (build step Python)

---

## [2.1.0] — 2026-05-27

### ✨ Aggiunto
- 🏷️ **Nuovo marchio Weibang** con 6 modelli (rasaerba semoventi, professionali BBC, batteria, trattorino)
  - `prodotti.html`: chip filtro + sezione brand dedicata
  - 6 pagine dettaglio `prodotti/weibang-*.html` con placeholder "foto in arrivo"
  - 6 entry in `js/product-data.js` per scheda completa con highlights
  - Indicizzazione automatica in `js/search-index.js` (ora 650 prodotti totali)
- 🖼️ **Griglia "Otto marche"** in `index.html` (`h3-brands`) — Weibang aggiunto alla griglia 4×2
- 📑 **Documentazione progetto**: cartella `docs/` con `business-brief`, `studio-fattibilita`, `roadmap`, `deploy`, `aggiungere-un-marchio`, `idea-progetto`
- 📜 `CHANGELOG.md` esteso + `LICENSE.txt` (MIT)
- 🐍 `scripts/add-weibang-products.py`: script replicabile per generare pagine + aggiornare marquee + sitemap

### 🔧 Modificato
- `index.html` + `storia.html`: aggiornati riferimenti "sette marche/marchi/filosofie" → "otto"
- Marquee marchi nel footer di **32 file HTML** aggiornato con "Weibang"
- `README.md`: riscritto coerente con stato attuale (17 schede detail, 650 SKU, 8 marchi, emoji nei titoli)
- `.gitignore`: aggiunti `.claude/`, `bazzana-sito/`, `__pycache__/`, `*.pyc`, pattern editor/secrets
- Integrati documenti scolastici originali (`docs/economy_finance/`, `docs/feasibility_study/`, `docs/idea-progetto.md`, `requirements`)

### 🐛 Bug fix
- **CRITICO**: `js/product-data.js` riga 262 aveva `},,` (doppia virgola) seguito da specs orfane di un prodotto Ligier cancellato male. Causava parse-error JS che rompeva `window.BAZZANA_PRODUCTS` → search e schede prodotto non funzionavano. Risolto rimuovendo le righe orfane.

### 📦 Repo
- Creato repository pubblico [GiovanniBugada/bazzana-sito](https://github.com/GiovanniBugada/bazzana-sito)
- Configurato `http.version HTTP/1.1` + `http.postBuffer 1GB` per superare il timeout del push iniziale (~1400 file)

---

## [2.0.0] — 2026-05-26

### ✨ Aggiunto
- 🎬 **Loader cinematografico ricco** con gradient typography
- 🎨 **Palette ricca** + animazioni dinamiche eleganti
- 📄 Pagine prodotto Stihl (iMow, MS 251, FS 131, BG 86)
- 📄 Pagine prodotto Ligier (Myli)
- 📄 Pagine prodotto Honda (HRX 476, HRN 536, EU22i)
- 📄 Pagine prodotto Active (4860 SH, MZ CM)
- 📄 Pagina prodotto Geotech (Cippatore Tritone)

### 🗑️ Rimosso
- `img-marquee` con foto prodotti che scorrono in home (sostituito con design più calmo)
- Pulsante audio toggle (non utile)
- Pagine `prodotti/echo-*.html` (Echo non più trattato)
- File prompt obsoleti (`PROMPT_ANIMAZIONI_SONDAVEN.md`, `PROMPT_VISUAL_MASTER.md`)

### 🔧 Modificato
- Refactor visivo: rimossi elementi "rumorosi" — design più calmo e premium

---

## [1.0.0] — primavera 2026

### 🎉 Prima release pubblica
- Struttura sito base: index, prodotti, officina, storia, contatti, foto, note, privacy, 404
- Sistema design: 11 sezioni cinematic in home
- Catalogo prodotti con modal scheda
- Galleria foto con lightbox (245 immagini)
- Form contatti GDPR + mappa OpenStreetMap
- Blog (12 articoli manutenzione/scelta)
- Easter eggs: Konami code, cursor custom

---

## 📚 Preistoria (versioni scolastiche)

> Le versioni iniziali risalgono al lavoro scolastico, prima della trasformazione nel sito v2 attuale.

### [0.0.5] — 2026-02-15
- 🍪 Cookie funzionanti

### [0.0.4] — 2026-02-15
- 🖼️ Aggiunta immagini
- 🍪 Cookie (non ancora funzionanti)

### [0.0.3] — 2026-02-09
- 🔧 Modifica del codice del sito

### [0.0.2] — 2025-11-19
- 🎉 Creazione iniziale della struttura del progetto
- 📄 Aggiunto file **README.md** con descrizione del sito
- 📄 Aggiunto file **LICENSE** (Licenza MIT)
- 📄 Aggiunto file **requirements** per le dipendenze
- 📄 Aggiunto file **CHANGELOG.md** per tracciare le modifiche future
- 🔒 Impostate le linee guida base per l'uso del codice (tramite Licenza MIT)

---

<sub>Per dettagli completi: `git log --oneline` sul repository.</sub>
