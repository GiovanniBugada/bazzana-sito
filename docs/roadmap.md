# 🗺️ Roadmap

> Funzionalità pianificate per **Motor Garden Bazzana v2** dopo l'apertura 2026.
> Versione: 2.1.0 · Aggiornato: 2026-05-27

---

## 🟢 Done (v2.1.0 — 2026-05-27)

- ✅ Marchio **Weibang** completo (6 modelli con placeholder foto)
- ✅ Griglia "Otto marche" in home aggiornata
- ✅ Bug fix `js/product-data.js` (`,,` orfano risolto)
- ✅ Documentazione progetto (`docs/`, `CHANGELOG.md`, `LICENSE.txt`)
- ✅ Repository pubblico [GiovanniBugada/bazzana-sito](https://github.com/GiovanniBugada/bazzana-sito)

---

## 🟡 In progress (sprint 2026-Q2)

| Priorità | Voce | Stato |
|----------|------|-------|
| 🔴 alta  | Foto reali modelli Weibang (sostituiscono placeholder) | in attesa fornitore |
| 🔴 alta  | Pubblicazione su dominio `motorgardenbazzana.it` | DNS in corso |
| 🟠 media | Integrazione Behold.so per feed Instagram (sezione "Live dal banco") | in attesa account |
| 🟠 media | Google Business Profile + Maps | apre con negozio |
| 🟡 bassa | Critical CSS inline (build step Python) | backlog |

---

## 🔮 Backlog (post-apertura 2026)

### 📦 Prodotti
- Aggiunta schede detail per **Oleo-Mac**, **Kress**, **Shindaiwa** (oggi solo catalogo)
- Sistema **confronto prodotti** (`compare.js` già a livello base — UI da finalizzare)
- **Filtro avanzato** nel catalogo (per cilindrata, prezzo, peso)
- Pagina **"Promozioni"** stagionali

### 🛎️ Servizi
- **Booking appuntamento officina** (slot da calendar Google)
- **Preventivatore manutenzione** (categoria + macchina → fascia di prezzo)
- **Newsletter** stagionale (primavera/autunno) — gia' slot footer

### 📊 Analytics e SEO
- Setup **Plausible Analytics** (privacy-first, no cookie banner)
- **Schema.org Review** quando arrivano le recensioni Google
- **Local SEO**: 20+ menzioni su directory locali (Pagine Gialle, Yelp BG, ProntoPro)
- **Blog**: 1 articolo/mese (manutenzione stagionale, scelta macchina, casi reali)

### 🌍 Espansione
- Versione **🇬🇧 EN** (solo se richiesta — basso ROI nel target Val Seriana)
- **App PWA** installabile (offline catalogo + scheda salvata)

### 🎨 Design
- **Dark mode** dedicato (oggi sito sempre dark)
- Pagine **"Tecnici"** (foto staff, qualifiche, anni esperienza)
- **Video** breve dell'officina al lavoro (loop muto in home hero)

---

## 📅 Milestone

| Data target | Milestone |
|-------------|-----------|
| 2026-Q2     | 🏪 **Apertura negozio** + pubblicazione sito su dominio |
| 2026-Q3     | 📸 Foto reali Weibang + restanti brand su pagine detail |
| 2026-Q4     | 📊 Prime metriche annuali, ottimizzazioni SEO based on dati |
| 2027-Q1     | 🛎️ Booking officina + preventivatore |
| 2027-Q2     | 🌱 Newsletter primavera + 6 articoli blog stagionali |

---

## 🧭 Principi guida

1. **Vanilla > framework**: ogni nuova feature deve poter essere scritta in HTML/CSS/JS puro.
2. **Performance prima del wow**: nessuna feature può portare Lighthouse < 85.
3. **Mobile-first**: ogni feature deve avere senso a 320px prima che a 1920px.
4. **No tracking invasivo**: solo analytics privacy-first, no cookie banner imposti.
5. **Aggiornabile in casa**: ogni feature deve avere uno "script Python" per modificarla in batch.
6. **Local-first**: il target è Val Seriana — ogni decisione SEO/copy guarda lì.

---

## 🚫 Out of scope (esplicitamente)

- ❌ E-commerce con pagamento online (le macchine vanno viste, provate, montate)
- ❌ Chatbot AI (preferiamo WhatsApp umano con risposta < 2h)
- ❌ Account utente / area riservata
- ❌ Recensioni nel sito (vanno su Google, è il loro posto)
- ❌ App nativa iOS/Android (PWA basta e avanza)
