# 🚀 Deploy guide

> Come pubblicare e aggiornare **Motor Garden Bazzana v2**.
> Versione: 2.1.0 · Aggiornato: 2026-05-27

---

## 🌐 Opzioni di hosting

Il sito è **statico** (solo HTML/CSS/JS/immagini), quindi puoi pubblicarlo
ovunque accetti file statici. Tre opzioni consigliate, dalla più semplice
alla più professionale:

### 🥇 Opzione 1 — GitHub Pages (consigliata, 0 €)

**Pro**: gratis, deploy automatico al push, HTTPS incluso, no setup.
**Contro**: dominio `.github.io` (a meno di custom domain con DNS).

```powershell
# 1. Sul repo GitHub, vai in Settings → Pages
# 2. Source: Deploy from a branch
# 3. Branch: master, folder: / (root)
# 4. Save

# Il sito sarà online in ~2 minuti su:
# https://giovannibugada.github.io/bazzana-sito/
```

Per usare `motorgardenbazzana.it`:
1. Aggiungi un file `CNAME` nella root con `motorgardenbazzana.it`
2. Sul registrar (es. Aruba, Register.it), punta il DNS:
   - `A` record → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` (www) → `giovannibugada.github.io`

---

### 🥈 Opzione 2 — Netlify (drag-and-drop, 0 €)

**Pro**: deploy preview per ogni branch, form serverless gratuiti, CDN globale.

```powershell
# 1. Vai su https://app.netlify.com/
# 2. "Add new site" → "Import an existing project"
# 3. Collega il repo GitHub
# 4. Build command: (vuoto)
# 5. Publish directory: (vuoto, è la root)
# 6. Deploy

# Custom domain: Settings → Domain management → Add custom domain
```

---

### 🥉 Opzione 3 — Hosting tradizionale (es. Aruba)

**Pro**: dominio Aruba + hosting già pagato dall'attività.
**Contro**: deploy manuale via FTP, niente preview branch, niente HTTPS automatico (a meno di Let's Encrypt manuale).

```powershell
# 1. FileZilla → connetti FTP Aruba
# 2. Carica tutta la cartella bazzana_v2/ (esclusi .git/, .claude/, scripts/, bazzana-sito/)
# 3. Verifica HTTPS attivo nel pannello Aruba
```

**File/cartelle da NON caricare**:
- `.git/` `.claude/` `bazzana-sito/`
- `scripts/__pycache__/` `*.pyc`
- `scripts/` (sono solo tool dev, non servono in produzione)
- `docs/` `CHANGELOG.md` `LICENSE.txt` `README.md` (non danneggiano ma occupano spazio)

---

## 🔄 Workflow di aggiornamento

### Per modifiche al codice
```powershell
# 1. Modifica file
# 2. Test locale
python -m http.server 8790
# Apri http://localhost:8790

# 3. Commit + push
git add -A
git commit -m "feat(area): descrizione modifica"
git push

# 4. GitHub Pages / Netlify deploya automaticamente in 1-2 minuti
```

### Per aggiungere foto
```powershell
# 1. Copia foto originali in C:/Users/ilbug/Desktop/scuola/gestione/foto bazzana/
# 2. Esegui import
python scripts/import-all-photos.py
# 3. Le foto vengono ottimizzate in assets/img/bazzana/
# 4. js/foto-manifest.js viene rigenerato
# 5. Commit + push come sopra
```

### Per aggiungere un nuovo prodotto al catalogo
Vedi [`aggiungere-un-marchio.md`](aggiungere-un-marchio.md) o sezione "Come aggiungere un prodotto" nel [README](../README.md).

### Per bumpare versioning cache (`?v=N`)
Dopo modifiche pesanti a CSS/JS, bumpa la versione per forzare il refresh browser:
```powershell
# (opzionale, esiste script per bump batch)
python scripts/bump-cache-version.py
```

---

## 🔐 Configurazioni produzione

### `robots.txt`
Già configurato correttamente per consentire crawl:
```
User-agent: *
Allow: /
Sitemap: https://www.motorgardenbazzana.it/sitemap.xml
```

### `sitemap.xml`
Aggiornato automaticamente quando aggiungi pagine prodotto via script Python.
Verifica che le URL puntino al dominio finale (cerca `motorgardenbazzana.it`).

### Form contatti (FormSubmit)
- Endpoint: `https://formsubmit.co/bazzanamotorgarden@gmail.com`
- **Prima volta**: invia un test, ricevi mail di conferma da FormSubmit, conferma → da quel momento i form arrivano in mail.

### Google Search Console
1. Aggiungi proprietà per `motorgardenbazzana.it`
2. Verifica con meta tag (basta aggiungerlo a `index.html` `<head>`)
3. Sottometti `sitemap.xml`
4. Richiedi indicizzazione delle pagine principali

---

## 🧪 Test pre-deploy

Checklist prima di pubblicare in produzione:

- [ ] `python -m http.server 8790` → tutte le pagine principali si aprono
- [ ] Console browser: 0 errori JS
- [ ] Network: 0 risorse 404
- [ ] Form contatti funziona (invia test)
- [ ] Mappa contatti carica
- [ ] WhatsApp link apre wa.me
- [ ] Telefono link apre dialer
- [ ] Mobile (DevTools → 375px): tutto leggibile
- [ ] `python scripts/build-search-index.py` rigenerato dopo modifiche al catalogo
- [ ] `sitemap.xml` aggiornato

---

## 🆘 Rollback

Se un deploy rompe il sito:

```powershell
# Trova il commit funzionante (es. aeaa171)
git log --oneline -10

# Crea un nuovo commit che inverte gli ultimi
git revert HEAD --no-edit
git push

# Oppure (più drastico) reset sul commit buono — DA USARE CON CAUTELA
git reset --hard aeaa171
git push --force-with-lease   # NB: --force-with-lease, mai --force secco
```

---

## 📞 Supporto

In caso di problemi tecnici durante il deploy, contattare lo sviluppatore che
mantiene il repo. Per richieste di modifica contenuti: [`README.md`](../README.md) sezione
"Come modificare contenuti rapidi".
