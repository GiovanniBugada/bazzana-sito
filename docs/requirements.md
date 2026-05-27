# 📋 Requirements

> Risorse e link funzionali al progetto **Motor Garden Bazzana — sito v2**.

---

## 🔗 Form / Risorse esterne

### Modulo di raccolta dati progetto
📝 **Google Form** (compilazione iniziale del progetto):
[Apri il form](https://docs.google.com/forms/d/e/1FAIpQLScbpqQfSt4yNVsdMwV4-WVgkqRoQ7IGkOF9zfJupDG4fQyOVQ/viewform?usp=dialog)

---

## 🧱 Dipendenze tecniche del sito

Il sito è **vanilla HTML/CSS/JS** — non ha dipendenze runtime installabili
(`npm install` non serve, `package.json` non esiste).

### Strumenti di sviluppo
| Tool | Versione | Uso |
|------|----------|-----|
| Python 3 | ≥ 3.10 | Script in `scripts/` (import foto, build search index, ecc.) |
| Git | ≥ 2.30 | Versioning + push GitHub |
| GitHub CLI (`gh`) | opzionale | Creazione repo e gestione PR via shell |
| Browser moderno | Chrome / Edge / Firefox / Safari ultime 2 major | Test e preview locale |
| Server locale | `python -m http.server 8790` | Preview durante sviluppo |

### Servizi esterni utilizzati a runtime
| Servizio | Scopo | Costo |
|----------|-------|-------|
| Google Fonts | Fraunces · Inter · JetBrains Mono | 0 € |
| FormSubmit | Gestione form contatti senza backend | 0 € (free tier) |
| OpenStreetMap | Mappa embed in contatti | 0 € |
| GitHub Pages / Netlify | Hosting statico in produzione | 0 € (free tier) |

---

## 🐍 Eventuali pip install (solo per script Python)

Nessun pacchetto pip esterno è strettamente richiesto: gli script in `scripts/`
usano solo standard library (`os`, `pathlib`, `re`, `json`, `xml`).

Se servono ottimizzazioni immagini avanzate:
```powershell
pip install pillow      # per resize/conversione formati
pip install pillow-avif # per output AVIF (opzionale)
```

---

## 📚 Documentazione di riferimento

- 🌿 [`../README.md`](../README.md) — guida tecnica completa
- 🚀 [`deploy.md`](deploy.md) — come pubblicare il sito
- 💡 [`idea-progetto.md`](idea-progetto.md) — idea del progetto ed evoluzione
- 💰 [`economy_finance/spese-progetto.md`](economy_finance/spese-progetto.md) — stima economica
