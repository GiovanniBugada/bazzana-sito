# AUDIT FINALE RESIDUO — Motor Garden Bazzana

Totale finding: **25**
- CRITICAL: 0
- HIGH:     1
- MEDIUM:   24
- LOW:      0

## HIGH (1)
- `admin-rotate.html:1` — admin-rotate.html NON ha <meta name=robots noindex>
  - **Fix:** Aggiungi <meta name="robots" content="noindex,nofollow">.

## MEDIUM (24)
- `js/search-index.js:3` — Riferimento a file inesistente: assets/img/prodotti/microcar-ligier-jsbluepass-frontale.jpg
  - **Fix:** Verifica path (tentate: ['C:\\Users\\ilbug\\Desktop\\bazzana_v2\\assets\\img\\prodotti\\microcar-ligier-jsbluepass-frontale.jpg']).
- `prodotti.html:63` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/active-4860.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/active-mz-cm.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/cippatore-tritone.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/honda-eu22i.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/honda-hrn.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/honda-hrx-476.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/ligier-myli.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/stihl-bg-86.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/stihl-fs-131.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/stihl-imow.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/stihl-ms-251.html:76` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/weibang-wb-452-he.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/weibang-wb-456-scve3.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/weibang-wb-462-sem.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/weibang-wb-466-scm.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/weibang-wb-506-sc.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/weibang-wb-506-sc3.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/weibang-wb-537-sc3.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/weibang-wb-537-scval.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/weibang-wb-537-scvalb.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/weibang-wb-537-scvm.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
- `prodotti/weibang-wb-778-scv3.html:69` — <button> senza testo né aria-label
  - **Fix:** Aggiungi aria-label="…" descrittivo.
