# PROMPT — Replicare le animazioni di sondaven.com su `bazzana_v2`

> Riferimento per replicare RIGOROSAMENTE le interazioni di [sondaven.com/en](https://sondaven.com/en) sul nostro sito Motor Garden Bazzana. Stack: HTML/CSS/JS vanilla, zero librerie. Tutto coerente con `tokens.css` esistente.

---

## 0. PRINCIPI DI sondaven

1. **Preloader 0%→100%** con tipografia ampia + barra fine.
2. **Hero immersivo full-screen** con titolo poetico + immagine architettonica.
3. **Scroll-driven**: ogni sezione ha la propria animazione legata alla posizione di scroll, non a timer.
4. **Pinned sections**: il contenuto resta fisso mentre il testo a fianco continua a scrollare ("storytelling").
5. **Reveal con clip-path**: testi e immagini emergono con mascheratura (`inset(100% 0 0 0) → inset(0)`).
6. **Carousel infiniti** su brand/sezioni partner.
7. **Parallax sottile** sulle immagini paesaggistiche (background scroll più lento del foreground).
8. **Number counters** che incrementano on viewport entry.
9. **Apartments SVG**: layout interattivo dove al click si cambia floorplan (per noi: scheda prodotto con immagine alternativa).
10. **Footer compatto** a 4 colonne con FAQ accordion.

---

## 1. ANIMAZIONI DA IMPLEMENTARE (ordine di esecuzione)

### A. Preloader con counter % ✅ GIA' FATTO
Implementazione: `js/main.js` linea 11 + `css/motion.css` `.loader`.
Tre tendine si aprono dal centro rivelando il logo, barra `scaleX(0→1)` 2200ms, counter `000% → 100%` con `cubic-out`. Skip a `window.load`.

### B. Hero "valley of peace" style 🔲 DA FARE
- Markup: `<section class="cinema-hero">` con `<img>` di sfondo (`facciata-esterna-rossa.jpg`) + overlay scuro 40-70% + titolo poetico + frase secondaria + scroll cue.
- Animazione: bg-zoom infinito 18s alternate (`scale 1.05 ↔ 1.15`).
- Titolo entra letter-by-letter con `.reveal-mask` (mask reveal verticale `translateY(110% → 0)`, stagger 80ms).
- Sub-titolo in `<em>` corsivo Fraunces (font display) `opacity 0 → 1` delay 1.4s.

### C. Sticky narrative "Officina" 🔲 DA FARE
- Markup: `<section class="sticky-narrative">` con `<aside class="sticky-narrative__text">` (testo principale a sinistra) + `<div class="sticky-narrative__items">` (5 immagini a destra che scrollano).
- Comportamento: testo sticky `top: 14vh`, immagini in flow normale. Mentre scrolli, il testo resta fisso al lato e le foto si succedono.
- CSS gia' presente in `css/pages/cinematic.css`.

### D. Stats counter 🔲 DA FARE
- Markup: `<div class="stat-block">` con `<p class="stat-block__value"><span class="num-ticker" data-target="10" data-suffix="+">0</span></p>` + label.
- JS in `main.js` `IntersectionObserver` count-up con `cubic-out` 1400ms (gia' presente).
- 4 stats: `10+ anni esperienza`, `200+ prodotti`, `7 marchi`, `48h ricambi`.

### E. Parallax sottile su immagini 🔲 DA FARE
- Markup: aggiungere `data-parallax-speed="0.3"` a `<img>` o `<div class="parallax">`.
- JS in `main.js`: scroll handler che applica `translateY(scrollY * -speed)` con `requestAnimationFrame`.
- Solo desktop (skip su touch device e reduced-motion).

### F. Pinned tech showcase con elemento che ruota 🔲 DA FARE
- Markup: `<section class="scroll-showcase">` con `<div class="scroll-showcase__sticky">` (sticky top:0 height:100vh) + img motosega che ruota mentre scrolli.
- JS: scroll listener calcola progress (0..1) della sezione e setta `--showcase-rot` (`rotate(progress * 360deg)`).
- 3 step di testo che si avvicendano (step 0: motore, step 1: catena, step 2: ergonomia).

### G. Brand marquee infinito 🔲 DA FARE
- Markup: `<div class="brand-marquee"><div class="brand-marquee__track">` + 8 `.brand-marquee__item` ripetuti 2 volte per loop seamless.
- CSS gia' presente: `animation: brand-marquee-scroll 34s linear infinite`.
- Items: STIHL, OLEO-MAC, SHINDAIWA, WEIBANG, LIGIER MICROCAR, KRESS, ACTIVE, OFFICINA AUTORIZZATA.

### H. Reveal clip-path su sezioni 🔲 DA FARE
- Markup: aggiungere `class="reveal-clip"` a h2, paragrafi e immagini chiave.
- JS IntersectionObserver applica `.is-revealed` (gia' presente).
- Effetto: `clip-path: inset(100% 0 0 0)` → `inset(0)` con stagger.

### I. Color invert section 🔲 DA FARE
- Markup: `<section class="color-invert-reveal">` su sezione narrative.
- CSS: pseudo-element nero che si scala da 0 a 1 cambiando sfondo.
- JS: IO applica `.is-inverted` al viewport entry.

### J. Spotlight section 🔲 DA FARE
- Markup: `<section class="spotlight-section">` su CTA finale.
- CSS: `radial-gradient` 520px che segue `--mouse-x`, `--mouse-y` (gia' presente).
- JS: mousemove handler (gia' presente).

### K. Footer wordmark gigante 🔲 GIA' PRESENTE
- `.site-footer__wordmark` con "MOTOR GARDEN BAZZANA" in font display 18rem (gia' in shell.css).

---

## 2. PALETTE E TIPOGRAFIA (gia' in `tokens.css`)

- **Primary dark**: `--c-ink: #0E0F0E` (sfondo principale, simile a sondaven nero-verde notte)
- **Ivory**: `--c-ivory: #F4F1EA` (testo su scuro, alternato avorio carta)
- **Accent Stihl**: `--c-stihl: #F26522` (CTA, dot, accent)
- **Forest**: `--c-forest: #1F3A2E` (riserva, sezioni "verde")
- **Display**: `Fraunces` (serif moderno per titoli H1/H2, mimica del display elegante di sondaven)
- **Body**: `Inter` (sans-serif neutro)
- **Mono**: `JetBrains Mono` (eyebrow, labels, num counter)

---

## 3. EASING E TIMING

- `--ease-out: cubic-bezier(0.22, 1, 0.36, 1)` — entrate (reveal, fade-up)
- `--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1)` — page transitions, sezioni grandi
- `--dur-fast: 240ms` — micro-interactions (hover, button)
- `--dur: 480ms` — transitions standard
- `--dur-slow: 900ms` — reveal, parallax inertia
- `--dur-page: 1200ms` — page mask, color invert

---

## 4. ACCESSIBILITA' (sondaven la rispetta)

- `prefers-reduced-motion: reduce` → tutti gli `animation: none`, `transform: none`, `opacity: 1`
- Skip su touch device (`hover: none, pointer: coarse`) per custom cursor e parallax
- IntersectionObserver con `safety net` 1500ms: se non scatta, forza `.is-in/.is-revealed/.is-inverted`
- `aria-hidden="true"` sugli elementi decorativi (loader, marquee, spotlight)

---

## 5. ESECUZIONE STEP-BY-STEP

1. **Hero cinema** (B) — modifica `index.html` sezione hero.
2. **Brand marquee** (G) — aggiungi `<div class="brand-marquee">` subito sotto la hero.
3. **Stats counter** (D) — sezione `<section class="stats-section">` con 4 stat blocks.
4. **Sticky narrative officina** (C) — sezione officina con testo sticky + 5 immagini.
5. **Pinned showcase** (F) — sezione con motosega che ruota.
6. **Color invert** (I) — wrap della sezione "I nostri marchi".
7. **Reveal clip-path** (H) — applicare `class="reveal-clip"` ai titoli h2 + immagini hero.
8. **Spotlight CTA** (J) — sezione contatti finale in `<section class="spotlight-section">`.
9. **Parallax** (E) — applicare `data-parallax-speed` alle immagini grandi.

Esegui ogni step, salva, ricarica nel browser, verifica visivamente. Commit dopo ogni step completato.

---

## 6. FILE COINVOLTI

- `index.html` — markup nuovo
- `css/pages/cinematic.css` — gia' creato con tutte le classi
- `css/motion.css` — loader cinema gia' presente
- `js/main.js` — observers + count-up + spotlight + parallax (parzialmente presente, completare parallax)
- `assets/img/hero/facciata-esterna-rossa.jpg` — hero bg
- `assets/img/officina/*.jpg` — sticky narrative items
- `assets/img/storia/*.jpg` — sezione narrative

---

## 7. SUCCESSO = "FATTO" QUANDO

- Apri `index.html` → splash con logo + 0% → 100% smooth → hero immersivo
- Scroll → marquee brand infinito sotto hero
- Continui scroll → stats counter animati 10/200/7/48
- Sezione officina sticky: testo fisso, foto scrollano
- Pinned section motosega: rotazione 360 mentre scrolli
- Color invert: la sezione brand passa da nero a avorio scrollando
- Spotlight CTA: muovendo il mouse vedi alone arancione che segue
- Footer marquee "MOTOR GARDEN BAZZANA" gia' presente
- Tutto rispetta `prefers-reduced-motion`

Nessun blocco scroll, nessun jank, mai elementi invisibili.
