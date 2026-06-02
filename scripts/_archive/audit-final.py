#!/usr/bin/env python3
"""
Audit finale: consistenza contatti, SEO, schema.org, refusi IT, nav, footer,
numeri, prodotti.html, note. Output classificato CRITICAL/HIGH/MEDIUM/LOW.
"""
from pathlib import Path
import re
import json
import sys
from collections import defaultdict, Counter

ROOT = Path(r"C:\Users\ilbug\Desktop\bazzana_v2")
PRODUCTS_DIR = ROOT / "prodotti"
NOTES_DIR = ROOT / "note"

# Collect all HTML files (exclude admin-rotate.html as it's a tool page)
HTML_FILES = sorted(
    [p for p in ROOT.glob("*.html")] +
    [p for p in PRODUCTS_DIR.glob("*.html")] +
    [p for p in NOTES_DIR.glob("*.html")]
)
HTML_FILES = [p for p in HTML_FILES if p.name != "admin-rotate.html"]

issues = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": []}


def add(level, msg):
    issues[level].append(msg)


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


# -----------------------------------------------------------------------------
# 1. CONTATTI - consistenza
# -----------------------------------------------------------------------------
# Pattern accettati
TEL_OK = [
    r"\+39\s*346\s*4156981",
    r"\+39\s*346[\s\.-]*415[\s\.-]*6981",
    r"346\s*4156981",
    r"346[\s\.-]*415[\s\.-]*6981",
    r"\+393464156981",
]
EMAIL_OK = "bazzanamotorgarden@gmail.com"
IG_OK = "instagram.com/bazzanamotorgarden"
WA_OK = "wa.me/393464156981"
INDIRIZZO_OK = re.compile(r"Via\s+U\.?\s*Bellora,?\s*73", re.I)
CAP_OK = re.compile(r"24020\s+Cene", re.I)
PIVA_OK = "04897880169"

tel_pattern_any = re.compile(r"(?:\+?39[\s\.-]*)?(\d{3})[\s\.-]*(\d{3})[\s\.-]*(\d{4})")
email_pattern = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
ig_pattern = re.compile(r"instagram\.com/([\w\.\-/]+)", re.I)
wa_pattern = re.compile(r"wa\.me/(\d+)", re.I)

# Strict matches expected
TEL_CANON_DIGITS = "3464156981"

contacts_summary = {
    "tel_files_with_wrong": [],
    "email_files_with_wrong": [],
    "ig_files_with_wrong": [],
    "wa_files_with_wrong": [],
    "address_files_missing_or_wrong": [],
    "piva_files_with_wrong": [],
}

# We only check pages that surface contacts (most pages have footer).
for f in HTML_FILES:
    html = f.read_text(encoding="utf-8", errors="ignore")
    # Telefoni
    for m in tel_pattern_any.finditer(html):
        digits = m.group(1) + m.group(2) + m.group(3)
        # Filter: only flag plausible IT mobile numbers (start with 3) or landlines starting with 0
        if digits.startswith("3") and len(digits) == 10 and digits != TEL_CANON_DIGITS:
            # Skip if it's just embedded inside a longer non-tel string
            context = html[max(0, m.start()-40):m.end()+40]
            if any(k in context.lower() for k in ["tel", "whatsapp", "phone", "wa.me", "ico-phone", "contact"]):
                contacts_summary["tel_files_with_wrong"].append((rel(f), digits))
                break
    # Emails (cerca email che non sia quella canonica ma che assomigli a bazzana)
    emails = set(email_pattern.findall(html))
    for e in emails:
        e_lower = e.lower()
        if "bazzana" in e_lower and e_lower != EMAIL_OK:
            contacts_summary["email_files_with_wrong"].append((rel(f), e))
        # email gmail diverse (legit per contatti? no, dovrebbe essere solo bazzanamotorgarden)
        if e_lower.endswith("@gmail.com") and "bazzana" not in e_lower and "@example" not in e_lower:
            contacts_summary["email_files_with_wrong"].append((rel(f), e))
    # Instagram
    for m in ig_pattern.finditer(html):
        handle = m.group(1).strip("/").lower()
        if handle and handle != "bazzanamotorgarden":
            # ignora link a generici tipo instagram.com/p/... ma flag se è un handle diverso
            if "/" not in handle and handle != "bazzanamotorgarden":
                contacts_summary["ig_files_with_wrong"].append((rel(f), handle))
    # WhatsApp
    for m in wa_pattern.finditer(html):
        num = m.group(1)
        if num != "393464156981":
            contacts_summary["wa_files_with_wrong"].append((rel(f), num))
    # Indirizzo & P.IVA: check only on contatti.html and pages that mention "Via" near Bellora
    if "Bellora" in html:
        if not INDIRIZZO_OK.search(html):
            contacts_summary["address_files_missing_or_wrong"].append(rel(f))
        if not CAP_OK.search(html):
            contacts_summary["address_files_missing_or_wrong"].append(rel(f) + " (CAP)")
    if "P.IVA" in html or "P. IVA" in html or "Partita IVA" in html.lower():
        if PIVA_OK not in html:
            contacts_summary["piva_files_with_wrong"].append(rel(f))


def emit_contacts():
    if contacts_summary["tel_files_with_wrong"]:
        for f, d in contacts_summary["tel_files_with_wrong"][:10]:
            add("CRITICAL", f"Telefono divergente in {f}: trovato {d}, atteso 346 4156981")
    if contacts_summary["email_files_with_wrong"]:
        seen = set()
        for f, e in contacts_summary["email_files_with_wrong"]:
            if (f, e) in seen:
                continue
            seen.add((f, e))
            add("CRITICAL", f"Email anomala in {f}: '{e}' (atteso bazzanamotorgarden@gmail.com)")
    if contacts_summary["ig_files_with_wrong"]:
        for f, h in contacts_summary["ig_files_with_wrong"][:10]:
            add("HIGH", f"IG handle diverso in {f}: '{h}' (atteso bazzanamotorgarden)")
    if contacts_summary["wa_files_with_wrong"]:
        for f, n in contacts_summary["wa_files_with_wrong"][:10]:
            add("CRITICAL", f"WhatsApp numero diverso in {f}: '{n}' (atteso 393464156981)")
    if contacts_summary["address_files_missing_or_wrong"]:
        uniq = list(dict.fromkeys(contacts_summary["address_files_missing_or_wrong"]))
        for f in uniq[:10]:
            add("HIGH", f"Indirizzo formato anomalo o CAP mancante: {f}")
    if contacts_summary["piva_files_with_wrong"]:
        for f in contacts_summary["piva_files_with_wrong"]:
            add("CRITICAL", f"P.IVA diversa da {PIVA_OK} in {f}")


emit_contacts()

# -----------------------------------------------------------------------------
# 2. TITLE + META DESCRIPTION
# -----------------------------------------------------------------------------
title_re = re.compile(r"<title>(.*?)</title>", re.I | re.S)
meta_desc_re_dq = re.compile(
    r'<meta\s+name="description"\s+content="(.*?)"', re.I | re.S
)
meta_desc_re_sq = re.compile(
    r"<meta\s+name='description'\s+content='(.*?)'", re.I | re.S
)


def find_meta_desc(html: str):
    m = meta_desc_re_dq.search(html)
    if m:
        return m
    return meta_desc_re_sq.search(html)


meta_desc_re = type("MD", (), {"search": staticmethod(find_meta_desc)})

for f in HTML_FILES:
    html = f.read_text(encoding="utf-8", errors="ignore")
    tm = title_re.search(html)
    if not tm:
        add("HIGH", f"<title> mancante: {rel(f)}")
    else:
        t = tm.group(1).strip()
        if not t:
            add("HIGH", f"<title> vuoto: {rel(f)}")
        elif len(t) < 10:
            add("MEDIUM", f"<title> troppo corto ({len(t)} char) in {rel(f)}: '{t}'")
        elif len(t) > 70:
            add("LOW", f"<title> lungo ({len(t)} char) in {rel(f)}")
    mm = meta_desc_re.search(html)
    if not mm:
        add("HIGH", f"meta description mancante: {rel(f)}")
    else:
        d = mm.group(1).strip()
        if len(d) < 50:
            add("MEDIUM", f"meta description corta ({len(d)} char): {rel(f)}")
        elif len(d) > 200:
            add("LOW", f"meta description lunga ({len(d)} char): {rel(f)}")

# -----------------------------------------------------------------------------
# 3. SCHEMA.ORG JSON-LD
# -----------------------------------------------------------------------------
jsonld_re = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)

idx_html = (ROOT / "index.html").read_text(encoding="utf-8", errors="ignore")
idx_ld = jsonld_re.findall(idx_html)
has_localbiz_idx = False
for blk in idx_ld:
    if "LocalBusiness" in blk or "AutomotiveBusiness" in blk or '"@type"' in blk and "Business" in blk:
        has_localbiz_idx = True
        break
if not has_localbiz_idx:
    add("CRITICAL", "index.html: LocalBusiness JSON-LD non trovato")

product_pages = sorted(PRODUCTS_DIR.glob("*.html"))
schema_count = 0
no_schema = []
for f in product_pages:
    if f.name == "dettaglio.html":
        continue
    html = f.read_text(encoding="utf-8", errors="ignore")
    blocks = jsonld_re.findall(html)
    has_product = any('"Product"' in b or "'Product'" in b for b in blocks)
    if has_product:
        schema_count += 1
    else:
        no_schema.append(rel(f))

total_products = len([f for f in product_pages if f.name != "dettaglio.html"])
if no_schema:
    add("HIGH", f"Schede prodotto senza schema Product: {len(no_schema)}/{total_products}")
    for f in no_schema[:5]:
        add("HIGH", f"  -> manca Product schema: {f}")

# -----------------------------------------------------------------------------
# 4. REFUSI ITALIANI
# -----------------------------------------------------------------------------
text_only_re = re.compile(r"<[^>]+>")
script_style_re = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.I | re.S)
comment_re = re.compile(r"<!--.*?-->", re.S)


def get_text(html: str) -> str:
    h = script_style_re.sub("", html)
    h = comment_re.sub("", h)
    return text_only_re.sub(" ", h)


refusi_patterns = [
    (re.compile(r"\bqual'è\b", re.I), "qual'è (corretto: qual è)"),
    (re.compile(r"\bpò\b"), "pò senza apostrofo (corretto: po')"),
    (re.compile(r"\bperchè\b", re.I), "perchè senza accento (corretto: perché)"),
    (re.compile(r"\bun\saltra\b", re.I), "un altra (corretto: un'altra)"),
    (re.compile(r"\s{2,}"), "doppio spazio"),
    (re.compile(r"\s+[,\.;:](?=\s|$)"), "spazio prima di punteggiatura"),
    (re.compile(r"\s+[?!](?=\s|$)"), "spazio prima di ?/!"),
    # brand wrong case (only flag the wrong ones)
    (re.compile(r"\bSTIHL\b"), "STIHL maiuscolo (corretto: Stihl)"),
    (re.compile(r"\bstihl\b"), "stihl minuscolo (corretto: Stihl)"),
    (re.compile(r"\bACTIVE\b"), "ACTIVE maiuscolo (corretto: Active)"),
    (re.compile(r"\bOLEO[-\s]?MAC\b"), "OLEO-MAC maiuscolo (corretto: Oleo-Mac)"),
    (re.compile(r"\bKRESS\b"), "KRESS maiuscolo (corretto: Kress)"),
    (re.compile(r"\bSHINDAIWA\b"), "SHINDAIWA maiuscolo (corretto: Shindaiwa)"),
    (re.compile(r"\bLIGIER\b"), "LIGIER maiuscolo (corretto: Ligier)"),
    (re.compile(r"\bWEIBANG\b"), "WEIBANG maiuscolo (corretto: Weibang)"),
    (re.compile(r"\bHONDA\b"), "HONDA maiuscolo (corretto: Honda)"),
]

refusi_counts = defaultdict(list)
for f in HTML_FILES:
    html = f.read_text(encoding="utf-8", errors="ignore")
    text = get_text(html)
    for rx, name in refusi_patterns:
        m = rx.search(text)
        if m:
            # exception: "stihl" inside URLs/paths is ok but text mode strips tags
            # so any hit in visible text is real
            refusi_counts[name].append((rel(f), m.group(0)[:30]))

for name, hits in refusi_counts.items():
    if "doppio spazio" in name or "punteggiatura" in name or "?/!" in name:
        level = "LOW"
    elif "maiuscolo" in name:
        level = "MEDIUM"
    else:
        level = "MEDIUM"
    # Don't spam: aggregate
    add(level, f"Refuso '{name}' in {len(hits)} file (es: {hits[0][0]})")

# -----------------------------------------------------------------------------
# 5. NAV-BAR consistenza
# -----------------------------------------------------------------------------
nav_re = re.compile(r"<nav[^>]*>(.*?)</nav>", re.I | re.S)
nav_link_re = re.compile(r'<a[^>]+href=["\'][^"\']*["\'][^>]*>(.*?)</a>', re.I | re.S)

EXPECTED_NAV = ["Officina", "Prodotti", "Foto", "Blog", "Storia", "Contatti"]

nav_signatures = defaultdict(list)
for f in HTML_FILES:
    html = f.read_text(encoding="utf-8", errors="ignore")
    nav_blocks = nav_re.findall(html)
    # Pick the first nav containing site links
    found_links = []
    for nb in nav_blocks:
        link_texts = [re.sub(r"\s+", " ", text_only_re.sub("", t)).strip() for t in nav_link_re.findall(nb)]
        # filter out brand logo / skip-link
        link_texts = [t for t in link_texts if t and t.lower() not in ("bazzana", "salta al contenuto", "menu")]
        if any(t in link_texts for t in ("Prodotti", "Officina")):
            found_links = link_texts
            break
    sig = "|".join(found_links)
    nav_signatures[sig].append(rel(f))

if len(nav_signatures) == 0:
    add("HIGH", "Nessuna nav trovata in alcun file")
else:
    # Look at the most common nav
    sorted_navs = sorted(nav_signatures.items(), key=lambda x: -len(x[1]))
    main_sig, main_files = sorted_navs[0]
    main_links = main_sig.split("|") if main_sig else []
    # Check if main nav matches expected
    missing = [e for e in EXPECTED_NAV if e not in main_links]
    extra = [l for l in main_links if l not in EXPECTED_NAV and l]
    if "Note" in main_links and "Blog" not in main_links:
        add("HIGH", f"Nav principale usa 'Note' invece di 'Blog' (in {len(main_files)} file)")
    if missing:
        add("HIGH", f"Nav principale manca voci: {missing} (in {len(main_files)} file)")
    if extra:
        add("MEDIUM", f"Nav principale voci extra: {extra}")
    # Check files with divergent nav
    for sig, files in sorted_navs[1:]:
        if not sig:
            for f in files:
                add("HIGH", f"Nav assente o vuota: {f}")
            continue
        links = sig.split("|")
        diff_miss = [e for e in EXPECTED_NAV if e not in links]
        diff_extra = [l for l in links if l not in EXPECTED_NAV and l]
        if "Note" in links and "Blog" not in links:
            add("MEDIUM", f"Nav usa 'Note' invece di 'Blog' in: {files}")
        elif diff_miss or diff_extra:
            add("MEDIUM", f"Nav diverge in {files}: missing={diff_miss}, extra={diff_extra}")

# -----------------------------------------------------------------------------
# 6. FOOTER MARQUEE consistenza
# -----------------------------------------------------------------------------
strip_re = re.compile(
    r'<[^>]+class=["\'][^"\']*site-footer__strip[^"\']*["\'][^>]*>(.*?)</', re.I | re.S
)
marquee_re = re.compile(
    r'<[^>]+class=["\'][^"\']*marquee[^"\']*["\'][^>]*>(.*?)</', re.I | re.S
)

strip_sigs = defaultdict(list)
marquee_sigs = defaultdict(list)
for f in HTML_FILES:
    html = f.read_text(encoding="utf-8", errors="ignore")
    sm = strip_re.search(html)
    mm = marquee_re.search(html)
    s_sig = ""
    m_sig = ""
    if sm:
        s_text = re.sub(r"\s+", " ", text_only_re.sub(" ", sm.group(1))).strip()
        s_sig = s_text[:200]
    if mm:
        m_text = re.sub(r"\s+", " ", text_only_re.sub(" ", mm.group(1))).strip()
        m_sig = m_text[:200]
    strip_sigs[s_sig].append(rel(f))
    if m_sig:
        marquee_sigs[m_sig].append(rel(f))

if len(strip_sigs) > 1:
    # If many pages share the canonical one but few diverge, flag the divergent
    sorted_strips = sorted(strip_sigs.items(), key=lambda x: -len(x[1]))
    canonical_count = len(sorted_strips[0][1])
    for sig, files in sorted_strips[1:]:
        if not sig:
            add("HIGH", f"site-footer__strip mancante in {len(files)} file: {files[:3]}")
        else:
            add("MEDIUM", f"site-footer__strip diverge in {len(files)} file (canonical in {canonical_count}): {files[:3]}")

if len(marquee_sigs) > 1:
    sorted_m = sorted(marquee_sigs.items(), key=lambda x: -len(x[1]))
    for sig, files in sorted_m[1:]:
        add("LOW", f"Marquee divergente in {len(files)} file: {files[:3]}")

# -----------------------------------------------------------------------------
# 7. CONTEGGI NUMERICI
# -----------------------------------------------------------------------------
def count_strings(strings):
    counts = Counter()
    where = defaultdict(list)
    for f in HTML_FILES:
        html = f.read_text(encoding="utf-8", errors="ignore")
        text = get_text(html).lower()
        for s in strings:
            n = text.count(s.lower())
            if n:
                counts[s] += n
                where[s].append(rel(f))
    return counts, where

# 650
counts_650, where_650 = count_strings(["650+", "650 prodotti", "650 sku", "650 referenze"])
# Alternate: numero scritto a parola
counts_650b, where_650b = count_strings(["seicento", "650 catalogo"])
# 8 marchi
counts_8, where_8 = count_strings(["8 marchi", "otto marchi", "8 brand", "otto brand"])
# 10+ anni / decennale
counts_10, where_10 = count_strings(["10+ anni", "dieci anni", "decennale", "decennio"])
# 2026
counts_2026, where_2026 = count_strings(["2026"])
# 48h ricambi
counts_48, where_48 = count_strings(["48h", "48 h", "48 ore"])

# Sanity: count "650" raw vs "8 marchi" raw to find divergent numbers (es. 700, 9 marchi)
suspicious_nums = re.compile(r"\b(\d{3,4})\s*(?:prodotti|sku|articoli|referenze)\b", re.I)
suspicious_marchi = re.compile(r"\b(\d+)\s*(?:marchi|brand)\b", re.I)
suspicious_anni = re.compile(r"\b(\d+)\+?\s*anni\b", re.I)
num_findings = defaultdict(list)
for f in HTML_FILES:
    text = get_text(f.read_text(encoding="utf-8", errors="ignore"))
    for m in suspicious_nums.finditer(text):
        n = int(m.group(1))
        if n != 650:
            num_findings["prodotti!=650"].append((rel(f), m.group(0)))
    for m in suspicious_marchi.finditer(text):
        n = int(m.group(1))
        if n != 8:
            num_findings["marchi!=8"].append((rel(f), m.group(0)))
    for m in suspicious_anni.finditer(text):
        n = int(m.group(1))
        if n < 10 or n > 20:
            num_findings["anni!=10"].append((rel(f), m.group(0)))

for k, hits in num_findings.items():
    add("MEDIUM", f"Numero divergente {k}: {len(hits)} occorrenze (es: {hits[0]})")

# -----------------------------------------------------------------------------
# 8. PRODOTTI.HTML HEALTH
# -----------------------------------------------------------------------------
prodotti_html = (ROOT / "prodotti.html").read_text(encoding="utf-8", errors="ignore")
# Conta article.depth-card
depth_card_re = re.compile(r'<article[^>]*class=["\'][^"\']*depth-card[^"\']*["\']', re.I)
card_count = len(depth_card_re.findall(prodotti_html))
if card_count < 600:
    add("CRITICAL", f"prodotti.html: solo {card_count} article.depth-card (atteso ~650)")
elif card_count != 650:
    add("MEDIUM", f"prodotti.html: {card_count} article.depth-card (atteso 650)")
else:
    pass  # OK

# Data attributes obbligatori
required_attrs = ["data-product-id", "data-product-name", "data-product-brand",
                  "data-product-cat", "data-product-img"]
# Estrai tutti gli <article ...> tag dei depth-card
article_open_re = re.compile(r"<article\b[^>]*class=[\"'][^\"']*depth-card[^\"']*[\"'][^>]*>", re.I)
articles = article_open_re.findall(prodotti_html)
missing_attr_count = defaultdict(int)
for art in articles:
    for attr in required_attrs:
        if attr not in art:
            missing_attr_count[attr] += 1

for attr, n in missing_attr_count.items():
    if n > 0:
        level = "HIGH" if n > 10 else "MEDIUM"
        add(level, f"prodotti.html: {n} card senza attributo {attr}")

# Duplicati id
id_re = re.compile(r'data-product-id=["\']([^"\']+)["\']')
ids = id_re.findall(prodotti_html)
dup_ids = [i for i, c in Counter(ids).items() if c > 1]
if dup_ids:
    add("CRITICAL", f"prodotti.html: {len(dup_ids)} data-product-id duplicati (es: {dup_ids[:5]})")

# -----------------------------------------------------------------------------
# 9. NOTE/BLOG 12 ARTICOLI
# -----------------------------------------------------------------------------
note_files = sorted(NOTES_DIR.glob("*.html"))
# Atteso 12
if len(note_files) != 12:
    add("MEDIUM", f"note/: {len(note_files)} articoli (atteso 12)")

h1_re = re.compile(r"<h1[^>]*>(.*?)</h1>", re.I | re.S)
for f in note_files:
    html = f.read_text(encoding="utf-8", errors="ignore")
    if not title_re.search(html):
        add("HIGH", f"Articolo blog senza <title>: {rel(f)}")
    if not h1_re.search(html):
        add("MEDIUM", f"Articolo blog senza <h1>: {rel(f)}")
    if not meta_desc_re.search(html):
        add("MEDIUM", f"Articolo blog senza meta description: {rel(f)}")

# Cross-link check: cerca "Articoli correlati" o "Continua a leggere" o link tra articoli
cross_link_present = 0
for f in note_files:
    html = f.read_text(encoding="utf-8", errors="ignore")
    # Almeno un link ad altro articolo nella stessa cartella
    other_note_links = re.findall(r'href=["\'](?:\.?/)?note/[^"\']+\.html', html)
    other_note_links_rel = re.findall(r'href=["\']\.?/?([\w\-]+\.html)["\']', html)
    has_correlati = ("Articoli correlati" in html or
                     "Continua a leggere" in html or
                     "Leggi anche" in html or
                     "Articoli simili" in html)
    has_internal_link = any(l != f.name for l in other_note_links_rel)
    if has_correlati or has_internal_link or other_note_links:
        cross_link_present += 1

if cross_link_present < len(note_files) / 2:
    add("MEDIUM", f"Solo {cross_link_present}/{len(note_files)} articoli blog hanno cross-link interni")

# -----------------------------------------------------------------------------
# REPORT
# -----------------------------------------------------------------------------
print("=" * 70)
print(f"AUDIT FINALE - {len(HTML_FILES)} file HTML scansionati")
print(f"  - {len([p for p in HTML_FILES if p.parent == ROOT])} top-level")
print(f"  - {len(product_pages)} schede prodotto ({total_products} con schema atteso)")
print(f"  - {len(note_files)} articoli blog")
print("=" * 70)
print()
print(f"SUMMARY: CRITICAL={len(issues['CRITICAL'])} HIGH={len(issues['HIGH'])} "
      f"MEDIUM={len(issues['MEDIUM'])} LOW={len(issues['LOW'])}")
print()

for level in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
    if not issues[level]:
        continue
    print(f"\n=== {level} ({len(issues[level])}) ===")
    for msg in issues[level]:
        print(f"  - {msg}")

print()
print("=" * 70)
print(f"Schede prodotto con Product schema: {schema_count}/{total_products}")
print(f"prodotti.html article.depth-card count: {card_count}")
print(f"note/ articoli: {len(note_files)} (cross-link in {cross_link_present})")
print("=" * 70)
