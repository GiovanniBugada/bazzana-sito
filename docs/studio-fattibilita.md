# 🔬 Studio di Fattibilità

> Analisi tecnica e business per il sito **Motor Garden Bazzana v2**.
> Versione: 2.1.0 · Aggiornato: 2026-05-27

---

## ✅ Fattibilità tecnica

### Stack scelto
| Componente | Tecnologia | Motivazione |
|------------|------------|-------------|
| Markup | HTML5 puro | Zero build, deploy istantaneo, longevità decennale |
| Styling | CSS3 moderno (`grid`, `clamp`, `clip-path`, `backdrop-filter`) | Browser support 95%+ senza polyfill |
| Logica client | JavaScript vanilla ES6+ | No framework = no aggiornamenti rotture |
| Tool catalogo | Python 3 (script offline) | Già installato, sintassi leggibile, no Node toolchain |
| Hosting | Statico (GitHub Pages / Netlify / Vercel) | 0 €, CDN globale, deploy via push |
| Form | FormSubmit | No backend, gestione GDPR inclusa |
| Mappa | OpenStreetMap embed | No API key, no tracking |

### ⚖️ Valutazione rischi

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Obsolescenza framework | 🟢 nulla | — | Vanilla stack: nessuna dipendenza che invecchia |
| Lock-in piattaforma | 🟢 nulla | — | Solo file statici, portabile ovunque |
| Browser non supportati | 🟡 bassa | basso | Fallback CSS + `prefers-reduced-motion` |
| Hosting offline | 🟡 bassa | medio | GitHub Pages uptime 99.95%, mirror su Vercel facile |
| Form spam | 🟠 media | basso | Honeypot + reCAPTCHA opzionale via FormSubmit |
| Foto prodotto mancanti | 🟠 media | medio | Placeholder "foto in arrivo" (pattern Stihl iMow / Ligier / Weibang) |

---

## 📈 Fattibilità SEO

### Punti di forza
- ✅ **HTML semantico** (header, main, section, article, nav, footer)
- ✅ **Meta description** specifica per pagina
- ✅ **Schema.org Product / LocalBusiness** su pagine prodotto e contatti
- ✅ **Sitemap.xml** + **robots.txt** corretti
- ✅ **Canonical URL** su tutte le pagine
- ✅ **OG tags** per condivisione social
- ✅ **Performance** mobile-first (Lighthouse 90+)

### Aree di lavoro post-launch
- 🟡 Inserimento Google Business Profile (negozio fisico)
- 🟡 Inserimento in directory locali Val Seriana / Bergamo
- 🟡 Link da blog locali su tematiche giardinaggio
- 🟡 Recensioni Google attive
- 🟡 Indicizzazione manuale via Google Search Console

---

## 💸 Fattibilità economica

### Costi una tantum (sviluppo)
| Voce | Costo |
|------|-------|
| Sviluppo sito (in casa) | 0 € (interno) |
| Foto showroom (245) | già fatte |
| Copywriting | interno |
| **Totale CAPEX** | **≈ 0 €** |

### Costi ricorrenti annuali
| Voce | Costo/anno |
|------|------------|
| Dominio `.it` | 12-15 € |
| Hosting (GitHub Pages free) | 0 € |
| FormSubmit (free tier) | 0 € |
| Manutenzione tecnica | interno |
| **Totale OPEX** | **< 30 €/anno** |

### Confronto con alternative

| Soluzione | CAPEX | OPEX | Controllo |
|-----------|-------|------|-----------|
| 🏆 **Sito v2 attuale** | 0 € | 30 €/a | 🟢 totale |
| Wix / Squarespace | 0 € | 200-400 €/a | 🟠 limitato |
| WordPress + theme | 500 € | 100-200 €/a | 🟡 medio |
| Agenzia "chiavi in mano" | 5-15 k€ | 500-2k €/a | 🔴 dipendenza |

**Conclusione**: il sito attuale offre **controllo totale**, **performance superiori**
e **costo recurring trascurabile** — fattibile e sostenibile in autonomia.

---

## 🧪 Fattibilità funzionale

### Funzionalità implementate (v2.1)
- ✅ Home cinematografica con 11 sezioni
- ✅ Catalogo prodotti (~650 SKU) filtrabile per brand
- ✅ 17 schede detail (MSI-style) con specs + highlights
- ✅ Galleria foto (245 immagini) con lightbox
- ✅ Storytelling "Storia" (6 capitoli sticky scroll)
- ✅ Pagina officina con timeline
- ✅ Form contatti GDPR + mappa
- ✅ Blog (12 articoli manutenzione/scelta)
- ✅ Search globale (~650 prodotti)
- ✅ Marchio Weibang con 6 modelli (foto in arrivo)
- ✅ Easter eggs (Konami, cursor)
- ✅ Mobile-first 320px → 1920px+

### Funzionalità rinviate (vedi roadmap)
- 🟡 Integrazione Behold.so per feed Instagram live
- 🟡 PDF scheda prodotto generato lato client (parziale)
- 🟡 Sistema di prenotazione appuntamenti officina
- 🟡 Multilingua IT/EN (post-apertura, se richiesto)

---

## 🚦 Decisione finale

**FATTIBILE ✅** sotto ogni profilo:
- 🟢 **Tecnico**: stack semplice, manutenibile, future-proof
- 🟢 **Economico**: CAPEX ≈ 0, OPEX < 30 €/anno
- 🟢 **Operativo**: deploy via git push, aggiornamento contenuti senza CMS
- 🟢 **Strategico**: differenzia Bazzana dai competitor "siti template anonimi"

> Il sito è **già in produzione interna**, pronto per la pubblicazione su dominio
> al momento dell'apertura fisica del negozio (2026).
