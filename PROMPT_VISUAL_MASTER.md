# PROMPT MASTER — Visual + Motion Polish bazzana_v2

> Documento operativo: tutto quello che serve fare graficamente, in
> animazioni, in UX e in responsive sul sito Motor Garden Bazzana per
> portarlo a livello Awwwards / sondaven.com / msi.com.

---

## 0. VISIONE D'INSIEME

**Cosa deve essere il sito**: un negozio fisico digitale di alta gamma.
Un sito che, aperto, comunichi immediatamente:

- **Mestiere** — l'officina autorizzata Stihl, le mani che riparano, il banco
- **Catalogo curato** — 420+ prodotti reali, navigabili senza fatica
- **Affidabilita'** — 10+ anni di esperienza decennale, marchi seri, riferimento territoriale Val Seriana
- **Premium ma caldo** — design cinematografico ma non freddo. Italiano, artigianale

**Riferimenti estetici**:
- sondaven.com → preloader %, parallax, hero immersivo, FAQ accordion, color invert reveal
- floema.com → page transitions, smooth scroll, sticky narrative
- msi.com / apple.com → pinned showcase con prodotto che ruota su scroll
- awwwards.com SoTD → micro-interazioni, cursor variants, marquee infiniti

**Stack vincolato**: HTML/CSS/JS vanilla. Zero framework, zero build. Tutto nei `<link>`/`<script>` standard.

---

## 1. AUDIT STATO ATTUALE

### Ottimo (gia' implementato)
- Loader cinematografico con logo + counter % + tendine
- Logo PNG ufficiale Bazzana Motor Garden (scudo + tricolore)
- 420 prodotti reali in catalogo con foto vere (Active, Kress, Oleo-Mac)
- Naming intelligente foto (no piu' "tagliasiepi.png" ambiguo)
- Wishlist localStorage + toast notifications
- Cookie banner GDPR
- Search istantanea catalogo
- Lightbox immagini
- WhatsApp smart links
- Custom cursor con label
- Spotlight cursor sezioni
- Color invert reveal
- Pinned MSI showcase
- Marquee brand + image marquee
- Stats counter num-ticker
- FAQ accordion
- Filter chip brand
- Reveal-clip / Word-reveal / Letter-up
- Magnetic CTA buttons
- 3D tilt cards
- Cursor trail dot
- Film grain overlay
- Scroll progress bar tricolore
- Sticky narrative
- Custom scrollbar arancione brand
- Page transition mask

### Da migliorare graficamente
- **Hero**: poco impatto visivo al primo schermo. Manca un elemento "wow"
- **Card prodotto**: foto su sfondo grigio piatto, poca personalita'
- **Categorie BENTO**: 6 card belle ma poca differenziazione hover
- **Spaziatura** tra sezioni: a volte troppo densa, a volte troppo larga
- **Tipografia titoli**: alcuni h2 mancano peso emotivo
- **Footer**: wordmark "BAZZANA" gigante presente ma sembra isolato
- **Navbar**: scroll-state poco percepibile

### Animazioni che mancano
- **Hero**: nessuna animazione di sfondo (manca particelle/ondeggiare gentle)
- **Categorie**: hover OK ma ingresso scroll piatto
- **Transizioni di pagina**: c'e' un mask base, ma non e' "wow"
- **Card flip 3D** su prodotti speciali
- **Cursor che cambia** in base alla sezione
- **Marquee verticale** decorativo
- **Hover su link "in vista"** con underline animato che cresce da centro
- **Counter incrementale** anche su sezione officina (clienti serviti, riparazioni, ecc.)
- **Animazioni di entrata sezione** con clip-path obliquo
- **Sticky FAB** WhatsApp + call con animazione bounce
- **Mouse-following spotlight** su intere sezioni hero
- **Custom scroll behavior** con momentum smussato (tipo Lenis)

### Responsive da rivedere
- Mobile portrait (375): hero text troppo grande
- Tablet (768-1024): scroll-showcase si stacca male
- Wide (>1440): contenuto si centra troppo, lascia bordi vuoti
- Touch device: alcune hover effect non danno feedback su tap

### Performance da migliorare
- Le 420 immagini del catalogo: 55 MB totali. Da convertire in WebP (-50%)
- Lazy-load aggressivo gia' parziale, da estendere a TUTTE le sezioni below-the-fold
- Preload solo dell'hero image, basta
- CSS critical inline nei head (top 4 KB)

---

## 2. MIGLIORIE GRAFICHE DA FARE

### 2.A Colore + atmosfera
- **Background gradient** dinamico nella hero (mesh gradient sottile arancione/verde/nero, statico ma morbido)
- **Box-shadow** dei prodotti: piu' definite con bordo arancione luminoso al hover
- **Border-radius** delle card: ridurre a 4-6px (piu' "scolpito") da 12px attuali
- **Bordi sezione**: usare separatori `border-block` 1px con `var(--c-line)` ovunque
- **Selection color** brand (gia' fatto)

### 2.B Tipografia
- **Hero title**: aumentare letter-spacing negativo a `-0.04em`, line-height 0.92 (piu' compatto, piu' cinema)
- **H2 sezione**: usare `font-style: italic` selettivo su parole chiave (es. "Le facciamo *durare*")
- **Eyebrow** mono uppercase con bullet arancione "●" all'inizio
- **Body text**: line-height 1.7 per leggibilita' italiana

### 2.C Immagini
- **Hero**: aggiungere overlay `gradient bottom: rgba(14,15,14,0.4) -> rgba(14,15,14,0.85)` per leggibilita' testo
- **Card prodotto catalogo**: sfondo `--c-ivory-soft` con sottile gradient diagonale, no piatto
- **Foto officina**: filter `saturate(0.95) contrast(1.04)` per look piu' cinematografico
- **Hover image**: scale 1.05 + filter brightness(1.08) per "accendere" la foto

### 2.D Decorazioni visive
- **Blob arancione** background dinamico nella hero (gia' fatto)
- **Dots grid** pattern sottile in alcune sezioni
- **SVG corner accents** angoli L che crescono on hover
- **Numeri sezione**: "01 / 06" mono uppercase in alto a destra di ogni section
- **Marquee verticale** sui lati dei trattorini (decoration)
- **Linea SVG che si traccia** come divider animato tra sezioni
- **Bollino circolare** rotante che dice "MOTOR GARDEN BAZZANA · CENE BG · 2026 ·" che gira lentamente in fondo

### 2.E Layout
- **Container** `--container: min(1400px, 92vw)` (gia' fatto)
- **Aspect-ratio** standardizzato: card 4/5, hero 16/9, foto officina 3/4
- **Sticky FAB** WhatsApp in basso destra (sempre visibile)

---

## 3. ANIMAZIONI MOZZAFIATO DA AGGIUNGERE

### 3.A Hero (impact immediato)
1. **Mesh gradient animato** sotto la facciata negozio (3 blob radial che si muovono lentamente)
2. **Titolo letter-by-letter** con `clip-path` da bottom (gia' fatto) + sottile **glitch** una volta al load
3. **Subtitle** che entra in mascheratura clip-path 1.2s dopo il titolo
4. **CTA magnetic** che si attraggono al cursore (gia' fatto) + ripple click (gia' fatto)
5. **Scroll cue** in basso che pulsa + freccia che oscilla
6. **Hero image zoom-in** lento (10s ease-out) on initial load — sensazione che la facciata "ti accolga"

### 3.B Scroll-driven
7. **Reveal con clip-path obliquo** invece del solito fade-in (taglio diagonale 45deg)
8. **Sticky narrative** officina: testo sticky a sinistra, foto che scorrono a destra (gia' fatto)
9. **Pinned MSI showcase** motosega che ruota -10 a +10deg + scala + glow (gia' fatto)
10. **Parallax** multi-layer su grandi immagini (gia' fatto)
11. **Color invert reveal** sezione brands (gia' fatto)
12. **Scale-in dell'immagine** che entra in viewport da 0.86 a 1.0 (gia' fatto)
13. **Numbers count-up** quando i KPI entrano in viewport (gia' fatto)
14. **Sticky scale-out** elementi che si rimpiccoliscono uscendo (gia' fatto)
15. **Headline shift** h2 che si sposta -20px quando entra in viewport

### 3.C Categorie BENTO
16. **Tilt 3D** su mouse (gia' fatto, perfezionare)
17. **Image swap** crossfade tra 2 foto (gia' CSS, da applicare)
18. **Numero categoria** "01 / 06" che si anima su hover
19. **CTA card** con sottolineato arancione che cresce da sinistra

### 3.D Catalogo prodotti
20. **Stagger cascade** entrata cards (gia' fatto)
21. **Filter chips** ripple click + fluida transizione brand-section (gia' fatto)
22. **Wishlist heart bounce** quando aggiungi (gia' fatto)
23. **Search input** con focus che cambia bordo arancione (gia' fatto)
24. **Card hover**: depth-card translateY -3px + overlay scuro + CTA WhatsApp slide-in

### 3.E Micro-interazioni
25. **Custom cursor** con label dinamica (gia' fatto)
26. **Cursor trail dot** arancione (gia' fatto)
27. **Toast** slide-in dalla destra (gia' fatto)
28. **Loader cinematic** con counter % e tendine (gia' fatto)
29. **Ripple click** sui btn (gia' fatto)
30. **Magnetic CTA** (gia' fatto)
31. **Page transition** mask al click di link interno (base presente, perfezionare con curtain orizzontale)

### 3.F Mancano (alta priorita')
32. **Smooth scroll lerp** custom (no library, ~120 righe vanilla). Override wheel/touchmove. Inertia 0.08.
33. **Cursor variants** per sezione: nel catalogo = "lente", in officina = "chiave inglese", su CTA = "freccia"
34. **Animated SVG line** che si traccia come divider tra ogni section (gia' fatto, applicare ovunque)
35. **Rotating badge** circolare "MOTOR GARDEN BAZZANA · CENE BG ·" che gira a fondo pagina
36. **Section number** "01" "02" "03" che si rivela on scroll in alto a sinistra di ogni section
37. **Eye-catcher** orange dot pulsante nelle CTA primarie
38. **Hover preview card** sulle categorie: micro-thumbnail flottante in basso a destra
39. **Page transition curtain** verticale arancione che scopre la prossima pagina
40. **Sticky FAB stack** in basso destra: WhatsApp + Call + Top con stagger fade-in on scroll

### 3.G Polish accessibility motion
41. **Prefers-reduced-motion**: TUTTE le animazioni disabilitate o ridotte a fade
42. **Focus visible** ring arancione (gia' fatto)
43. **Skip link** "Vai al contenuto" (gia' presente)

---

## 4. RESPONSIVE A TUTTI I DISPOSITIVI

### Breakpoint strategy
- **<480px** — mobile portrait (testo compatto, 1 colonna)
- **480-768** — mobile landscape / tablet portrait (2 colonne dove serve)
- **768-1024** — tablet (3 colonne, no parallax aggressivi)
- **1024-1440** — desktop (4-5 colonne catalogo, anim complete)
- **>1440** — wide screen (max-width 1400, centratura)

### Da rivedere
- Hero title `clamp(2rem, 7vw, 5rem)` invece di sole rem
- Scroll-showcase: stack verticale completo sotto 768 con flow normale (no sticky)
- Card grid: 1 col <480, 2 col 480-768, 3-4 col >768
- Padding section: `clamp(2rem, 6vw, 6rem)` verticale, `clamp(1rem, 4vw, 2rem)` orizzontale
- Footer: stack verticale completo sotto 600
- Cursor custom: nascosto su touch (hover: none, pointer: coarse) — gia' fatto
- Splash loader: logo width `min(420px, 80vw)` invece di fixed

### Touch device specials
- Tap targets minimo 44x44px (gia' fatto)
- Magnetic/tilt/spotlight disabilitati (gia' fatto)
- Image marquee piu' lenta su mobile per leggibilita'
- Active-state piu' visibile (background change + scale 0.97)

---

## 5. PERFORMANCE OTTIMIZZAZIONI

- [ ] Convertire le 420 PNG catalogo in WebP (-50% size, ~25 MB invece di 55)
- [ ] Aggiungere `<picture>` con fallback PNG per browser vecchi
- [ ] Lazy load di TUTTI gli elementi below-the-fold (gia' parziale)
- [ ] `<link rel="preload">` solo per la hero image + Inter font woff2
- [ ] Critical CSS (top 4 KB) inline nel `<head>` di ogni HTML
- [ ] Defer caricamento `js/extras.js` (gia' fatto)
- [ ] Compress SVG assets (cinematic-extras grain overlay e' 1 KB, gia' OK)
- [ ] `fetchpriority="high"` solo sulla hero image
- [ ] `loading="lazy"` su TUTTE le altre immagini (gia' fatto)
- [ ] Service Worker minimo per cache (opzionale, no PWA full)
- [ ] Sitemap.xml + robots.txt completi (gia' presente sitemap base)

---

## 6. ACCESSIBILITY + SEO

- [ ] `aria-label` su ogni bottone icona-only
- [ ] `role="status"` sui toast
- [ ] `role="dialog"` sul lightbox + focus trap
- [ ] `alt` descrittivo su ogni `<img>` (gia' migliorato in catalog v2)
- [ ] Schema.org Product per ogni prodotto (esistono come `<details>`, valutare se vale generare data)
- [ ] Schema.org LocalBusiness (gia' presente in index.html)
- [ ] OpenGraph immagini dedicate per ogni pagina (gia' presente in index)
- [ ] Robots.txt + sitemap.xml curati (gia' presente, verificare contenuto)
- [ ] Lang attr `it` (gia' presente)
- [ ] Canonical URL su ogni pagina (gia' presente)

---

## 7. UX FUNZIONALITA'

### Da aggiungere
- [ ] **Sticky FAB stack** in basso a destra: WhatsApp + Phone + Back-to-top
- [ ] **Pagina prodotto template** click su una card del catalogo apre `prodotto.html?slug=XXX` con dettaglio
- [ ] **Comparatore prodotti**: spunta su 2-3 card, modal che mostra le foto affiancate
- [ ] **Newsletter signup** in footer (semplice mailto temporaneo o Formspree)
- [ ] **Bottone "Salva come PDF"** sulla wishlist
- [ ] **Configuratore robot** (wizard 3 step: m²/terreno/budget → 3 modelli consigliati)
- [ ] **Calendar booking** assistenza (slot disponibili week corrente)
- [ ] **Testimonial slider** clienti reali (per ora fakes plausibili)
- [ ] **Live availability badge** "IN STOCK" "ORDINABILE" "SOLO ASSISTENZA" sui prodotti (gia' CSS pronto)

### Gia' presente
- Wishlist localStorage + toast
- Search istantanea catalogo
- Cookie banner GDPR
- Lightbox immagini
- WhatsApp smart links
- Cursor custom

---

## 8. PIANO DI ESECUZIONE

Ordine sequenziale, ogni step e' commit separato sul branch `try-all-extras`:

### FASE 1 — Hero piu' impattante (priorita' top)
1. Mesh gradient blob dietro la facciata
2. Hero image zoom-in lento on load
3. Overlay gradient piu' definito per leggibilita'
4. CTA pulse soft + scroll cue piu' visibile
5. Section number "01 / 06" in alto

### FASE 2 — Card categorie premium
6. Image swap su hover (CSS gia', applicare alle 6 cat-card)
7. Numero "01 — Taglio" che si anima al hover
8. CTA underline grow

### FASE 3 — Catalogo perfezione
9. Card hover: depth piu' marcato, overlay piu' rapido
10. Search con dropdown suggestion (top 5 risultati live)
11. Live availability badge applicato a top 20 prodotti

### FASE 4 — Sticky FAB stack
12. WhatsApp + Phone + Back-to-top in basso destra con stagger fade-in on scroll

### FASE 5 — Page transition curtain
13. Click su link interno → curtain arancione verticale + navigazione + reveal

### FASE 6 — Section numbers + dividers SVG
14. "01" "02" "03"... in alto a sinistra di ogni section
15. SVG line draw divider tra ogni section

### FASE 7 — Rotating badge circolare
16. "MOTOR GARDEN BAZZANA · CENE BG · 2026 ·" che gira lentamente prima del footer

### FASE 8 — Responsive fine-tuning
17. Hero text clamp() rivisto
18. Scroll-showcase mobile no-sticky
19. Card grid breakpoint review
20. Padding sections clamp() review

### FASE 9 — Performance
21. Conversione PNG -> WebP top 50 prodotti hero/featured
22. Critical CSS inline top of head
23. Lazy load review esaustivo

### FASE 10 — Polish finale
24. Rifinitura easing/timing (cubic-bezier consistency)
25. Test prefers-reduced-motion su tutte le pagine
26. Test mobile 375 / tablet 768 / desktop 1440
27. Lighthouse score >= 90 su perf/a11y/best-practices

---

## 9. CRITERI "FATTO"

Il sito e' "pronto" quando, aprendolo da zero in incognito:

- Loader nero con logo che si compone + counter 000% → 100% + linea tricolore
- Hero: facciata negozio con zoom lento, blob arancioni che si muovono, titolo che si rivela letter-by-letter, 2 CTA magnetic
- Scroll: progress bar in alto, ogni sezione entra con reveal-clip diagonal
- Categorie: 6 card che si inclinano 3D, numero che cresce on hover
- Pinned showcase: motosega che ruota mentre scorri, 3 step di testo si avvicendano
- Stats: counter che incrementano da 0 al numero in 1.4s
- Brand grid: scrolla e diventa avorio chiaro
- FAQ: domande accordion con + che ruota a x
- H-scroll: 6 citta' scroll-snap orizzontale
- Catalogo: 420 prodotti con foto, search filtra istantaneo, wishlist cuoricino, CTA arancione "Chiedi info"
- Sticky FAB: WhatsApp/phone/top in basso destra
- Rotating badge sopra footer
- Cookie banner al primo accesso
- Custom cursor desktop, normale touch
- Tutto smooth, no jank, no flash di stile non caricato
- Mobile portrait: navigazione hamburger, layout 1 colonna, no parallax, tap targets corretti
- prefers-reduced-motion: animazioni ridotte/disabilitate

---

## 10. ESEGUI SU `try-all-extras`

Tutti i commit di questo lavoro sul branch `try-all-extras`. Master rimane
stato stabile precedente. Al termine, utente decide:
- `git checkout master && git merge try-all-extras` se piace
- `git checkout master` se non piace (torna allo stato attuale)
