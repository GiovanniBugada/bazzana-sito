"""
Audit foto-vs-nome: per ogni card del catalogo, confronta
data-product-name con il filename dell'immagine. Se non c'e' una
buona corrispondenza, sostituisce la foto con il placeholder.

Strategia di matching:
  - Estrai i "token" alfanumerici dal nome del prodotto (es. "51.51" -> ["51", "51"]; "BC241D" -> ["BC241D", "241"])
  - Estrai i token dal filename (es. "51.51-300x300.png" -> ["51", "51", "300", "300"])
  - C'e' match se almeno un token significativo del nome appare nel filename
  - Token "significativi" = quelli che non sono dimensioni (300x300, 1-1, thumb, etc)

USO: python scripts/audit-photo-name-match.py
"""
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
PRODOTTI = ROOT / "prodotti.html"
PLACEHOLDER = "assets/img/placeholder-foto-arrivo.svg"

# Token nel filename da IGNORARE (non sono il model code)
IGNORE_TOKENS = {
    "300x300", "300", "thumb", "1-1", "1", "sx", "dx", "sp",
    "standard", "sinistra", "destra", "fronte", "laterale", "retro",
    "alto", "basso", "logo", "kit", "con", "batteria",
    # parole italiane comuni nei filename descrittivi
    "motosega", "decespugliatore", "tagliasiepi", "tagliasiepe", "soffiatore",
    "rasaerba", "robot", "trattorino", "generatore", "motozappa",
    "potatura", "abbattimento", "forestale", "professionale",
    "da", "a", "di", "il", "la", "le", "lo", "per", "con",
    "om", "oleo", "mac", "active", "kress", "krees", "stihl", "shindaiwa",
    "honda", "ligier", "geotech",
    "scoppio", "elettrico", "benzina", "tempi", "multiuso", "multifunzione",
    "evolution", "frontale", "posteriore", "interno", "esterno",
    "camera", "cruscotto", "bagagliaio", "completo", "pannello",
    "myli", "yashi", "jsbluepass", "nera", "tritone", "sprint",
    "3", "4", "quarti", "vista", "dall", "anteriore",
}


def tokenize(s):
    """Estrai token alfanumerici da una stringa, in minuscolo."""
    s = s.lower()
    # Sostituisci punti con spazi (es. "51.51" -> "51 51" che e' ok)
    s = re.sub(r'[._\-\s/(),]+', ' ', s)
    raw = [t for t in s.split() if t]
    return raw


def significant_tokens(tokens):
    """Filtra i token che sembrano model code (almeno 2 caratteri, non in IGNORE)."""
    out = []
    for t in tokens:
        if t in IGNORE_TOKENS:
            continue
        if len(t) < 2:
            continue
        if t.isdigit() and len(t) < 2:
            continue
        out.append(t)
    return out


def basename_no_ext(path):
    name = Path(path).name
    return re.sub(r'\.(png|jpg|jpeg|webp|svg)$', '', name, flags=re.I)


def main():
    html = PRODOTTI.read_text(encoding="utf-8")
    article_re = re.compile(
        r'<article\s+class="depth-card"[^>]*data-product-name="([^"]*)"[^>]*data-product-brand="([^"]*)"[^>]*data-product-cat="([^"]*)"[^>]*data-product-img="([^"]*)"[^>]*>',
        re.IGNORECASE,
    )

    cards = []
    for m in article_re.finditer(html):
        name, brand, cat, img = m.group(1), m.group(2), m.group(3), m.group(4)
        cards.append({"name": name, "brand": brand, "cat": cat, "img": img})

    print(f"Totale card analizzate: {len(cards)}\n")

    matched = 0
    placeholders = 0
    mismatches = []
    no_token_in_name = []

    for c in cards:
        if c["img"].endswith("placeholder-foto-arrivo.svg"):
            placeholders += 1
            continue
        name_tokens = significant_tokens(tokenize(c["name"]))
        img_base = basename_no_ext(c["img"])
        img_tokens = tokenize(img_base)

        # Match se almeno un token significativo del nome appare nel filename
        is_match = False
        if not name_tokens:
            # Nome senza token significativi (es. solo "Standard")
            no_token_in_name.append(c)
            is_match = True  # non possiamo verificare, lo consideriamo OK
        else:
            for nt in name_tokens:
                if nt in img_tokens:
                    is_match = True
                    break
                # Match parziale: token del nome contenuto in un token dell'img (e' un superset)
                for it in img_tokens:
                    if nt in it or it in nt:
                        if len(nt) >= 3 or len(it) >= 3:
                            is_match = True
                            break
                if is_match:
                    break

        if is_match:
            matched += 1
        else:
            mismatches.append({
                "name": c["name"],
                "img": c["img"],
                "name_tokens": name_tokens,
                "img_base": img_base,
                "img_tokens": img_tokens,
            })

    print(f"OK (foto e nome coerenti):       {matched}")
    print(f"Gia placeholder:                 {placeholders}")
    print(f"MISMATCH (foto != nome):         {len(mismatches)}")
    print(f"Nome senza token (non valutati): {len(no_token_in_name)}")
    print()

    if mismatches:
        print("=" * 70)
        print("Primi 30 mismatch (foto non corrisponde al nome):")
        print("=" * 70)
        for m in mismatches[:30]:
            print(f"\n  Nome:     {m['name']}")
            print(f"  Tokens:   {m['name_tokens']}")
            print(f"  Img file: {m['img_base']}")
            print(f"  Img tok:  {m['img_tokens'][:6]}")

    # Scrivi report dei mismatch in JSON
    import json
    out = ROOT / "mismatch-report.json"
    out.write_text(
        json.dumps(mismatches, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n\nReport completo salvato in {out}")

    return mismatches


if __name__ == "__main__":
    main()
