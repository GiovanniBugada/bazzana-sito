"""
Audit foto prodotti + pulizia nomi modello.

Per ogni card del catalogo (prodotti.html):
  - Verifica che data-product-img esista realmente. Se manca, sostituisce
    con il placeholder "Foto in arrivo".
  - Pulisce i nomi che sono filenames (es.
    "motosega-forestale-7310sx-sp-thumb (1)" -> "7310SX-SP").
  - Aggiorna anche src dell'<img> figlio e alt dell'<img>.

USO: python scripts/audit-product-photos.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODOTTI = ROOT / "prodotti.html"
PLACEHOLDER = "assets/img/placeholder-foto-arrivo.svg"

# Prefissi descrittivi italiani da rimuovere dai filename-nomi
DESCRIPTIVE_PREFIXES = [
    "motosega-da-abbattimento-",
    "motosega-da-potatura-",
    "motosega-forestale-",
    "motosega-a_scoppio-",
    "motosega-",
    "decespugliatore-da-zaino-",
    "decespugliatore-asta-fissa-",
    "decespugliatore-asta-snodata-",
    "decespugliatore-",
    "tagliasiepi-",
    "tagliasiepe-",
    "soffiatore-aspiratore-",
    "soffiatore-",
    "rasaerba-elettrico-",
    "rasaerba-",
    "robot-rasaerba-",
    "robot-tagliaerba-",
    "trattorino-",
    "generatore-inverter-",
    "generatore-",
    "motopompa-",
    "motozappa-",
    "motofalciatrice-",
    "potatore-",
    "trinciasarmenti-",
    "trincia-",
    "arieggiatore-",
    "spazzaneve-",
    "scuotitore-",
    "abbacchiatore-",
    "trivella-",
    "cippatore-",
    "biotrituratore-",
    "powertrack-",
    "transporter-",
    "carriola-",
    "olio-",
    "miscela-",
    "tanica-",
    "kit-",
    "catena-",
    "ricambio-",
    "accessorio-",
]

BRAND_TOKENS = [
    "oleo-mac-",
    "oleomac-",
    "shindaiwa-",
    "active-",
    "kress-",
    "krees-",
    "stihl-",
    "honda-",
    "geotech-",
]

# Suffissi cosmetici / tecnici da strippare
COSMETIC_SUFFIXES_RE = [
    re.compile(r"\s*\(\d+\)\s*$"),                        # " (1)", " (2)"
    re.compile(r"-thumb$", re.I),
    re.compile(r"-300x300$", re.I),
    re.compile(r"-1-1$"),
    re.compile(r"[-_](sx|dx|sinistra|destra)$", re.I),
    re.compile(r"[-_](sp)$", re.I),                        # 7310sx-sp
    re.compile(r"[-_](standard)$", re.I),
    re.compile(r"_thumb$", re.I),
    re.compile(r"^om(?=[a-z])", re.I),                     # "omgst..." -> "gst..." (Oleo-Mac)
]


def clean_name(raw):
    """Trasforma un filename-name in un model-code leggibile."""
    if not raw:
        return raw
    s = raw.strip()
    # Se sembra già un nome ragionevole (lettere maiuscole + spazi + cifre),
    # lascia stare.
    if re.match(r"^[A-Z0-9][A-Z0-9 \.\-/]+$", s):
        return s

    lower = s.lower()
    # Rimuovi prefissi descrittivi
    for p in DESCRIPTIVE_PREFIXES:
        if lower.startswith(p):
            lower = lower[len(p):]
            break
    # Rimuovi token brand
    for b in BRAND_TOKENS:
        if lower.startswith(b):
            lower = lower[len(b):]
            break
        # Anche nel mezzo (es "motosega-X-shindaiwa-Y")
        lower = lower.replace("-" + b.rstrip("-") + "-", "-")
    # Strippa suffissi cosmetici iterativamente
    changed = True
    while changed:
        changed = False
        for pat in COSMETIC_SUFFIXES_RE:
            new = pat.sub("", lower)
            if new != lower:
                lower = new
                changed = True

    if not lower:
        return raw  # fallback: non rovinare se la pulizia svuota

    # Sostituisci separatori con spazi e maiuscolizza i token alfanumerici
    parts = re.split(r"[\s_/-]+", lower)
    out_parts = []
    for p in parts:
        if not p:
            continue
        # Token con cifre = codice modello -> uppercase
        if re.search(r"\d", p):
            out_parts.append(p.upper())
        else:
            # Token con sole lettere = parola descrittiva -> title case
            out_parts.append(p.capitalize())
    return " ".join(out_parts)


def main():
    html = PRODOTTI.read_text(encoding="utf-8")
    original = html
    changes_img = 0
    changes_name = 0

    # 1) Trova ogni <article class="depth-card" ... > e modifica gli attributi
    article_open_re = re.compile(
        r'<article\s+class="depth-card"[^>]*>',
        re.IGNORECASE,
    )
    img_attr_re = re.compile(r'data-product-img="([^"]*)"')
    name_attr_re = re.compile(r'data-product-name="([^"]*)"')

    def repl_open(m):
        nonlocal changes_img, changes_name
        tag = m.group(0)
        # Img check
        ima = img_attr_re.search(tag)
        if ima:
            rel = ima.group(1)
            if not (ROOT / rel).exists():
                tag = img_attr_re.sub(
                    f'data-product-img="{PLACEHOLDER}"', tag, count=1
                )
                changes_img += 1
        # Name clean
        na = name_attr_re.search(tag)
        if na:
            old = na.group(1)
            new = clean_name(old)
            if new and new != old:
                safe = new.replace('"', '&quot;')
                tag = name_attr_re.sub(
                    f'data-product-name="{safe}"', tag, count=1
                )
                changes_name += 1
        return tag

    new_html = article_open_re.sub(repl_open, html)

    # 2) Per gli article con placeholder, aggiorna anche il src dell'<img> dentro.
    article_full_re = re.compile(
        r'(<article\s+class="depth-card"[^>]*data-product-img="'
        + re.escape(PLACEHOLDER)
        + r'"[^>]*>)(.*?)(</article>)',
        re.DOTALL | re.IGNORECASE,
    )

    def fix_img_src(m):
        head, body, tail = m.group(1), m.group(2), m.group(3)
        body_new = re.sub(
            r'(<img[^>]*src=")[^"]*("[^>]*>)',
            rf"\g<1>{PLACEHOLDER}\g<2>",
            body,
            count=1,
        )
        return head + body_new + tail

    new_html = article_full_re.sub(fix_img_src, new_html)

    # 3) Per ogni article, sincronizza l'alt dell'img con il name pulito.
    #    (Non rifacciamo il name cleaning, leggiamo quello attuale.)
    article_full_re2 = re.compile(
        r'(<article\s+class="depth-card"[^>]*data-product-name="([^"]*)"[^>]*data-product-brand="([^"]*)"[^>]*data-product-cat="([^"]*)"[^>]*>)(.*?)(</article>)',
        re.DOTALL | re.IGNORECASE,
    )

    def fix_alt(m):
        head, name, brand, cat, body, tail = (
            m.group(1),
            m.group(2),
            m.group(3),
            m.group(4),
            m.group(5),
            m.group(6),
        )
        new_alt = f'{brand} {name} - {cat}'.replace('"', '&quot;')
        body_new = re.sub(
            r'(<img[^>]*alt=")[^"]*("[^>]*>)',
            rf"\g<1>{new_alt}\g<2>",
            body,
            count=1,
        )
        return head + body_new + tail

    new_html = article_full_re2.sub(fix_alt, new_html)

    if new_html != original:
        PRODOTTI.write_text(new_html, encoding="utf-8")
        print(f"  IMG -> placeholder:  {changes_img}")
        print(f"  Nomi puliti:         {changes_name}")
        print(f"  Salvato {PRODOTTI}")
    else:
        print("Nessun cambio necessario.")


if __name__ == "__main__":
    main()
