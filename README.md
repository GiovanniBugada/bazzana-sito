# Motor Garden Bazzana — v2

Sito vetrina di Motor Garden Bazzana (Cene, BG), rivenditore ufficiale Stihl e officina autorizzata dal 1998.

Versione 2 — completamente indipendente dal sito precedente. Si affianca al sito esistente come opzione alternativa.

## Stack

- HTML5 statico
- CSS3 vanilla (custom properties, grid, container queries)
- JavaScript vanilla (no framework)
- Font: Fraunces (display), Inter (UI), JetBrains Mono (mono) — Google Fonts
- Zero build step. Si serve con qualsiasi server statico.

## Avvio locale

```bash
cd bazzana_v2
python -m http.server 8000
# o
npx serve .
```

Apri `http://localhost:8000`.

## Struttura

```
bazzana_v2/
├── index.html               Home
├── officina.html
├── prodotti.html            Catalogo
├── prodotti/                Schede prodotto (15)
├── storia.html
├── contatti.html
├── 404.html
├── sitemap.xml
├── robots.txt
├── assets/
│   ├── img/{hero,prodotti,officina,ambiente,brand,storia}/
│   └── favicon/
├── css/
│   ├── main.css             Entry (importa tutti)
│   ├── tokens.css           Custom properties (palette, font, spacing)
│   ├── reset.css
│   ├── typography.css
│   ├── layout.css
│   ├── components.css
│   ├── motion.css           Loader, cursor, reveal, page transitions
│   ├── shell.css            Header, footer, menu
│   └── pages/{home,interior}.css
└── js/
    └── main.js
```

## Direzione creativa

Riferimenti Awwwards: sondaven.com, floema.com, weirdfolders.com. Direzione: "officina cinematografica". Palette scura, tipografia Fraunces grande, accenti arancio Stihl.

## Foto

Tutte le foto principali sono scatti reali del negozio (selezionati dalla cartella `foto bazzana` del proprietario). Trattate con leggera desaturazione + warm tone per coerenza visiva. Le foto della valle Seriana sullo sfondo della vetrina danno il senso del luogo.

## Contatti

- Sede: Via U. Bellora 73, 24020 Cene (BG)
- Telefono: +39 035 719411
- Email: info@motorgardenbazzana.it
- Instagram: @bazzanamotorgarden
