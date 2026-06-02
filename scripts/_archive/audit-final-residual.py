#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDIT FINALE RESIDUO — Motor Garden Bazzana
============================================
Cerca problemi non ancora visti su:
 1. Schede prodotto (prodotti/*.html, esclusa dettaglio.html)
 2. Pagine minori (privacy, 404, admin-rotate)
 3. JavaScript (sintassi grezza, riferimenti rotti, debug residui)
 4. CSS (import esistenti, versionamento)
 5. Accessibilità di base (alt, aria-label)
 6. Robots / Sitemap / SEO
 7. Footer consistency (anno, P.IVA, layout, strip marchi)

Output: lista CRITICAL / HIGH / MEDIUM / LOW con file:linea + fix consigliato.
"""

from __future__ import annotations
import html
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS_DIR = ROOT / "prodotti"
NOTES_DIR = ROOT / "note"
JS_DIR = ROOT / "js"
CSS_DIR = ROOT / "css"

EXCLUDE_PRODUCT_FILES = {"dettaglio.html"}

# ---------------------------------------------------------------------------
# Findings collector
# ---------------------------------------------------------------------------

SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
findings: list[dict] = []


def report(severity: str, fpath: Path | str, line: int | None, desc: str, fix: str) -> None:
    rel = str(fpath)
    try:
        rel = str(Path(fpath).resolve().relative_to(ROOT)).replace("\\", "/")
    except Exception:
        pass
    findings.append({
        "severity": severity,
        "file": rel,
        "line": line or 0,
        "desc": desc,
        "fix": fix,
    })


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def line_of(src: str, idx: int) -> int:
    return src.count("\n", 0, idx) + 1


def asset_exists(rel_from_html: str, base_dir: Path) -> bool:
    """rel_from_html is an href relative to the HTML's folder."""
    # Strip query strings, fragments
    rel_from_html = rel_from_html.split("#", 1)[0].split("?", 1)[0]
    if not rel_from_html:
        return True
    candidate = (base_dir / rel_from_html).resolve()
    return candidate.exists()


# ---------------------------------------------------------------------------
# 1. PRODUCT DETAIL PAGES
# ---------------------------------------------------------------------------

LEGACY_RESIDUES = [
    # token: regex flags
    ("MZ CM", r"\bMZ\s*CM\b"),
    ("4860 SH", r"\b4860\s*SH\b"),
    ("Honda GP", r"\bHonda\s*GP\b"),
    ("lorem ipsum", r"\blorem\s+ipsum\b"),
    ("TODO", r"\bTODO\b"),
    ("FIXME", r"\bFIXME\b"),
]


def audit_product_pages() -> None:
    product_files = [
        p for p in sorted(PRODUCTS_DIR.glob("*.html"))
        if p.name not in EXCLUDE_PRODUCT_FILES
    ]
    if len(product_files) != 22:
        report(
            "MEDIUM",
            PRODUCTS_DIR,
            None,
            f"Atteso 22 schede prodotto, trovate {len(product_files)}",
            "Verifica se ne è stata aggiunta/rimossa una senza aggiornare il count atteso.",
        )

    for f in product_files:
        src = read_text(f)

        # Title
        m_title = re.search(r"<title[^>]*>(.*?)</title>", src, re.I | re.S)
        if not m_title or not m_title.group(1).strip():
            report("HIGH", f, line_of(src, m_title.start()) if m_title else 1,
                   "Title vuoto o assente",
                   "Aggiungi <title>NomeProdotto · Motor Garden Bazzana</title>")

        # H1
        m_h1 = re.search(r"<h1[^>]*>(.*?)</h1>", src, re.I | re.S)
        if not m_h1:
            report("HIGH", f, 1, "Nessun <h1> nella scheda prodotto",
                   "Aggiungi <h1 class=\"product__title\">…</h1>")
        else:
            text = re.sub(r"<[^>]+>", "", m_h1.group(1)).strip()
            if not text:
                report("HIGH", f, line_of(src, m_h1.start()),
                       "<h1> presente ma vuoto",
                       "Inserisci il modello del prodotto come testo dell'H1.")

        # data attributes on <main>
        m_main = re.search(r"<main\b([^>]*)>", src, re.I)
        if not m_main:
            report("CRITICAL", f, 1, "Nessun <main> trovato",
                   "Aggiungi <main id=\"main\" class=\"product\" data-bzn-product …>")
        else:
            attrs = m_main.group(1)
            mline = line_of(src, m_main.start())
            for attr in ("data-bzn-product", "data-brand", "data-model"):
                if attr not in attrs:
                    report("HIGH", f, mline,
                           f"<main> manca attributo {attr}",
                           f"Aggiungi {attr}=\"…\" sull'elemento <main>.")

            # data-img → file esiste?
            m_img = re.search(r'data-img="([^"]+)"', attrs)
            if not m_img:
                report("MEDIUM", f, mline, "data-img assente",
                       "Aggiungi data-img=\"assets/img/prodotti/<file>.jpg\" su <main>.")
            else:
                img_rel = m_img.group(1)
                # data-img è espresso dalla root, non dalla cartella prodotti
                candidate = (ROOT / img_rel).resolve()
                if not candidate.exists() and "placeholder" not in img_rel.lower():
                    report("HIGH", f, mline,
                           f"data-img punta a file inesistente: {img_rel}",
                           f"Verifica path. Atteso: {candidate}")

            # data-specs JSON valido?
            m_specs = re.search(r'data-specs="([^"]*)"', attrs)
            if not m_specs:
                report("MEDIUM", f, mline, "data-specs assente",
                       "Aggiungi data-specs='[…]' (JSON) su <main>.")
            else:
                raw = html.unescape(m_specs.group(1))
                try:
                    parsed = json.loads(raw)
                    if not isinstance(parsed, list) or not parsed:
                        report("MEDIUM", f, mline,
                               "data-specs JSON valido ma non lista non vuota",
                               "Deve essere lista di oggetti {label,value}.")
                except json.JSONDecodeError as e:
                    report("HIGH", f, mline,
                           f"data-specs JSON INVALIDO: {e.msg}",
                           "Correggi escaping HTML / virgole / sintassi JSON.")

            # JSON-LD name vs data-model
            m_model = re.search(r'data-model="([^"]+)"', attrs)
            data_model = m_model.group(1) if m_model else None

            m_ldjson = re.search(
                r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                src, re.I | re.S,
            )
            if not m_ldjson:
                report("HIGH", f, 1,
                       "Manca <script type=\"application/ld+json\"> Schema.org Product",
                       "Inserisci JSON-LD con Product, brand, image, offers.")
            else:
                ld_raw = m_ldjson.group(1).strip()
                try:
                    ld = json.loads(ld_raw)
                    if ld.get("@type") != "Product":
                        report("MEDIUM", f, line_of(src, m_ldjson.start()),
                               f"JSON-LD @type={ld.get('@type')!r}, atteso 'Product'",
                               "Imposta \"@type\":\"Product\".")
                    ld_name = ld.get("name", "")
                    if data_model and ld_name and ld_name.strip() != data_model.strip():
                        # Allow JSON-LD name to be richer (include brand)
                        if data_model not in ld_name:
                            report("MEDIUM", f, line_of(src, m_ldjson.start()),
                                   f"JSON-LD name={ld_name!r} ≠ data-model={data_model!r}",
                                   "Allinea il name del Product al modello reale.")
                except json.JSONDecodeError as e:
                    report("HIGH", f, line_of(src, m_ldjson.start()),
                           f"JSON-LD non parseabile: {e.msg}",
                           "Correggi sintassi JSON dentro <script type=ld+json>.")

        # Link al catalogo
        if "../prodotti.html" not in src:
            report("MEDIUM", f, 1,
                   "Manca link \"../prodotti.html\" (torna al catalogo)",
                   "Aggiungi <a href=\"../prodotti.html\">Torna al catalogo</a>.")

        # WhatsApp con text=
        if "wa.me/" not in src:
            report("HIGH", f, 1, "Nessun link WhatsApp (wa.me)",
                   "Aggiungi CTA <a href=\"https://wa.me/393464156981?text=…\">.")
        else:
            # WA con parametro text= almeno una volta
            if not re.search(r"wa\.me/393464156981\?text=", src):
                report("MEDIUM", f, 1,
                       "Link wa.me senza ?text= precompilato",
                       "Aggiungi ?text=Buongiorno%2C%20vorrei%20info%20su… .")

        # Residui legacy
        for token, pat in LEGACY_RESIDUES:
            # Esclude active-mz-cm.html — è proprio quel modello (corpo testo lecito).
            if f.name == "active-mz-cm.html" and token == "MZ CM":
                continue
            for m in re.finditer(pat, src, re.I):
                report("HIGH", f, line_of(src, m.start()),
                       f"Residuo testuale \"{token}\"",
                       f"Sostituisci/rimuovi \"{token}\".")


# ---------------------------------------------------------------------------
# 2. MINOR PAGES
# ---------------------------------------------------------------------------

def audit_minor_pages() -> None:
    # privacy.html
    p = ROOT / "privacy.html"
    if not p.exists():
        report("HIGH", "privacy.html", 1, "privacy.html mancante", "Crea pagina privacy GDPR.")
    else:
        src = read_text(p)
        if not re.search(r"<title[^>]*>.+?</title>", src, re.I | re.S):
            report("MEDIUM", p, 1, "privacy.html senza <title>",
                   "Aggiungi <title>Privacy Policy · Motor Garden Bazzana</title>")
        # Contenuto minimo
        text = re.sub(r"<[^>]+>", " ", src)
        if len(text.strip()) < 800:
            report("MEDIUM", p, 1,
                   f"privacy.html sembra troppo corto ({len(text.strip())} char di testo)",
                   "Espandi informativa GDPR (titolare, dati, base giuridica, diritti).")
        if "motorgardenbazzana.it" not in src and "index.html" not in src:
            report("LOW", p, 1, "privacy.html senza link al sito principale",
                   "Aggiungi link a Home o canonical.")

    # 404.html
    p404 = ROOT / "404.html"
    src = read_text(p404)
    if not re.search(r"<h1[^>]*>.*?</h1>", src, re.I | re.S):
        report("HIGH", p404, 1, "404.html senza <h1>",
               "Aggiungi <h1>404 — Pagina in officina</h1>.")
    if "index.html" not in src and 'href="/"' not in src:
        report("MEDIUM", p404, 1, "404.html senza link a home",
               "Aggiungi <a href=\"index.html\">Torna alla home</a>.")
    if "contatti" not in src.lower():
        report("LOW", p404, 1, "404.html senza link a contatti",
               "Suggerisci <a href=\"contatti.html\">Contattaci</a>.")
    if not re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', src, re.I):
        report("MEDIUM", p404, 1, "404.html senza <meta name=robots noindex>",
               "Aggiungi <meta name=\"robots\" content=\"noindex\">.")

    # admin-rotate.html
    padm = ROOT / "admin-rotate.html"
    if not padm.exists():
        report("LOW", "admin-rotate.html", 1,
               "admin-rotate.html mancante (admin tool atteso)",
               "Crea pagina admin con noindex.")
    else:
        src = read_text(padm)
        if not re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', src, re.I):
            report("HIGH", padm, 1,
                   "admin-rotate.html NON ha <meta name=robots noindex>",
                   "Aggiungi <meta name=\"robots\" content=\"noindex,nofollow\">.")


# ---------------------------------------------------------------------------
# 3. JAVASCRIPT
# ---------------------------------------------------------------------------

JS_PATH_HINTS = re.compile(
    r"""(?:["'`])(?P<path>(?:\.\./|/|)(?:assets|css|js|prodotti|note|favicon|sitemap)[^"'`?#]+?\.(?:jpg|jpeg|png|webp|svg|gif|css|js|html|ico|xml|json|pdf))["'`]""",
    re.I,
)


def strip_js_strings_and_comments(src: str) -> str:
    """Best effort: rimuove stringhe ' " ` e commenti // /* */."""
    out = []
    i = 0
    n = len(src)
    while i < n:
        c = src[i]
        # block comment
        if c == "/" and i + 1 < n and src[i + 1] == "*":
            j = src.find("*/", i + 2)
            if j == -1:
                break
            out.append(" " * (j + 2 - i))
            i = j + 2
            continue
        # line comment
        if c == "/" and i + 1 < n and src[i + 1] == "/":
            j = src.find("\n", i + 2)
            if j == -1:
                break
            out.append(" " * (j - i))
            i = j
            continue
        # string
        if c in ("'", '"', "`"):
            quote = c
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == quote:
                    j += 1
                    break
                j += 1
            out.append(" " * (j - i))
            i = j
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _node_check(path: Path) -> tuple[bool, str]:
    """Tenta `node --check`. Ritorna (ok, stderr). Se node manca, ok=True."""
    import shutil, subprocess
    node = shutil.which("node")
    if not node:
        return True, ""
    try:
        r = subprocess.run([node, "--check", str(path)],
                           capture_output=True, text=True, timeout=10)
        return (r.returncode == 0), r.stderr
    except Exception as e:
        return True, str(e)


def audit_javascript() -> None:
    for f in sorted(JS_DIR.glob("*.js")):
        src = read_text(f)

        # Sintassi: preferisci node --check se disponibile (parser vero).
        # Il counter di graffe su JS è troppo rumoroso (regex / template strings).
        ok, stderr = _node_check(f)
        if not ok:
            report("CRITICAL", f, 1,
                   f"`node --check` segnala sintassi NON valida",
                   "Correggi sintassi. Stderr: " + (stderr.strip().splitlines() or [""])[0][:200])

        # Debug residui

        # Debug residui
        for pat, label, sev in [
            (r"\bdebugger\b", "debugger", "HIGH"),
            (r"\bconsole\.error\(", "console.error(", "LOW"),
            (r"\bTODO\b", "TODO", "LOW"),
            (r"\bFIXME\b", "FIXME", "MEDIUM"),
            (r"\bXXX\b", "XXX", "LOW"),
        ]:
            for m in re.finditer(pat, src):
                report(sev, f, line_of(src, m.start()),
                       f"Residuo {label} in JS",
                       "Rimuovi o sostituisci con logging strutturato/feature flag.")

        # Riferimenti a file
        for m in JS_PATH_HINTS.finditer(src):
            p = m.group("path")
            # Salta CDN e path con templating
            if "${" in p or "{" in p:
                continue
            # I path JS possono essere usati da pagine in / o /prodotti o /note.
            # Verifichiamo come "esiste se almeno una di queste interpretazioni
            # corrisponde ad un file reale dentro ROOT":
            candidates = []
            # 1) interpretazione root-relative (es. "/assets/..", "assets/..")
            rel = p.lstrip("/")
            candidates.append((ROOT / rel))
            # 2) interpretazione da una pagina che vive nella root (../foo)
            #    Quando p inizia con ../ va risolto contro una sottocartella ipotetica.
            if p.startswith("../"):
                # Da /prodotti/<page>.html → ../assets/... = /assets/...
                candidates.append((ROOT / "prodotti" / p).resolve())
                candidates.append((ROOT / "note" / p).resolve())
            exists = any(c.resolve().exists() for c in candidates)
            if not exists:
                report("MEDIUM", f, line_of(src, m.start()),
                       f"Riferimento a file inesistente: {p}",
                       f"Verifica path (tentate: {[str(c) for c in candidates]}).")


# ---------------------------------------------------------------------------
# 4. CSS
# ---------------------------------------------------------------------------

CSS_IMPORT = re.compile(r'@import\s+url\(\s*["\']?([^"\')\s]+)["\']?\s*\)\s*;', re.I)
HTML_CSS_LINK = re.compile(
    r'<link[^>]+href="(?P<href>[^"]*main\.css[^"]*)"', re.I
)
QUERY_V = re.compile(r"\?v=(\d+)")


def audit_css() -> None:
    main_css = CSS_DIR / "main.css"
    src = read_text(main_css)
    for m in CSS_IMPORT.finditer(src):
        rel = m.group(1)
        # rel è espresso rispetto alla cartella css/
        candidate = (CSS_DIR / rel.split("?", 1)[0]).resolve()
        if not candidate.exists():
            report("HIGH", main_css, line_of(src, m.start()),
                   f"@import punta a file CSS inesistente: {rel}",
                   f"Crea/rinomina file. Atteso: {candidate}")

    # main.css versione vs versionamento HTML
    # Estrai versioni richiamate da tutte le pagine HTML
    html_versions = set()
    for html_file in [
        ROOT / "index.html", ROOT / "officina.html", ROOT / "prodotti.html",
        ROOT / "storia.html", ROOT / "foto.html", ROOT / "contatti.html",
        ROOT / "note.html", ROOT / "privacy.html", ROOT / "404.html",
    ]:
        if not html_file.exists():
            continue
        s = read_text(html_file)
        m = HTML_CSS_LINK.search(s)
        if not m:
            continue
        href = m.group("href")
        vm = QUERY_V.search(href)
        if vm:
            html_versions.add(vm.group(1))
    if len(html_versions) > 1:
        report("MEDIUM", "css/main.css", 1,
               f"Versioni main.css disallineate tra pagine: {sorted(html_versions)}",
               "Allinea tutti i ?v=N su main.css alla stessa versione (cache busting).")


# ---------------------------------------------------------------------------
# 5. ACCESSIBILITY (lightweight)
# ---------------------------------------------------------------------------

IMG_TAG = re.compile(r"<img\b([^>]*?)/?>", re.I | re.S)
BUTTON_TAG = re.compile(r"<button\b([^>]*?)>(.*?)</button>", re.I | re.S)
A_TAG = re.compile(r"<a\b([^>]*?)>(.*?)</a>", re.I | re.S)


def has_attr(attrs: str, name: str) -> bool:
    return re.search(rf'\b{name}\s*=', attrs, re.I) is not None


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def audit_a11y() -> None:
    html_files = sorted(ROOT.glob("*.html")) + sorted(PRODUCTS_DIR.glob("*.html")) + \
                 sorted(NOTES_DIR.glob("*.html"))
    for f in html_files:
        if f.name == "dettaglio.html":
            continue
        src = read_text(f)
        for m in IMG_TAG.finditer(src):
            attrs = m.group(1)
            if not has_attr(attrs, "alt"):
                report("MEDIUM", f, line_of(src, m.start()),
                       "<img> senza attributo alt=",
                       "Aggiungi alt=\"\" (decorativa) o alt=\"descrizione\" (contenuto).")
        for m in BUTTON_TAG.finditer(src):
            attrs, inner = m.group(1), m.group(2)
            text = strip_tags(inner)
            if not text and not has_attr(attrs, "aria-label") and not has_attr(attrs, "aria-labelledby") and not has_attr(attrs, "title"):
                report("MEDIUM", f, line_of(src, m.start()),
                       "<button> senza testo né aria-label",
                       "Aggiungi aria-label=\"…\" descrittivo.")
        for m in A_TAG.finditer(src):
            attrs, inner = m.group(1), m.group(2)
            text = strip_tags(inner)
            has_svg = "<svg" in inner.lower()
            has_img_alt = re.search(r"<img\b[^>]*\balt\s*=\s*\"([^\"]+)\"", inner, re.I)
            if not text and has_svg and not has_attr(attrs, "aria-label") and not has_attr(attrs, "aria-labelledby") and not has_attr(attrs, "title") and not has_img_alt:
                report("MEDIUM", f, line_of(src, m.start()),
                       "<a> con solo icona SVG senza aria-label",
                       "Aggiungi aria-label=\"…\" sull'<a>.")


# ---------------------------------------------------------------------------
# 6. ROBOTS / SEO / SITEMAP
# ---------------------------------------------------------------------------

def audit_seo() -> None:
    robots = ROOT / "robots.txt"
    sitemap = ROOT / "sitemap.xml"

    if not robots.exists():
        report("HIGH", "robots.txt", 1, "robots.txt mancante",
               "Crea robots.txt con Sitemap: e Disallow: pertinenti.")
    if not sitemap.exists():
        report("HIGH", "sitemap.xml", 1, "sitemap.xml mancante",
               "Crea sitemap.xml con tutte le URL pubbliche.")
        return

    sm = read_text(sitemap)
    sitemap_urls = set(re.findall(r"<loc>([^<]+)</loc>", sm))

    # Calcola URL attese
    expected: set[str] = set()
    base = "https://www.motorgardenbazzana.it"

    # Root pages: tutte tranne admin-rotate, 404, dettaglio
    for f in ROOT.glob("*.html"):
        if f.name in {"404.html", "admin-rotate.html"}:
            continue
        if f.name == "index.html":
            expected.add(base + "/")
        else:
            expected.add(f"{base}/{f.name}")
    # Note articles
    for f in NOTES_DIR.glob("*.html"):
        expected.add(f"{base}/note/{f.name}")
    # Product details (esclusa dettaglio.html)
    for f in PRODUCTS_DIR.glob("*.html"):
        if f.name in EXCLUDE_PRODUCT_FILES:
            continue
        expected.add(f"{base}/prodotti/{f.name}")

    missing = expected - sitemap_urls
    extra = sitemap_urls - expected

    if missing:
        for url in sorted(missing):
            report("HIGH", "sitemap.xml", 1,
                   f"URL mancante in sitemap: {url}",
                   "Aggiungi <url><loc>…</loc>…</url>.")
    if extra:
        for url in sorted(extra):
            report("MEDIUM", "sitemap.xml", 1,
                   f"URL in sitemap che non corrisponde a file locale: {url}",
                   "Rimuovi entry oppure crea la pagina mancante.")


# ---------------------------------------------------------------------------
# 7. FOOTER CONSISTENCY
# ---------------------------------------------------------------------------

FOOTER_EXPECTED_BRANDS = [
    "Stihl", "Active", "Oleo-Mac", "Kress", "Shindaiwa", "Ligier", "Weibang", "Honda",
]


def audit_footer_consistency() -> None:
    # Pagine pubbliche con footer atteso
    targets: list[Path] = []
    for f in ROOT.glob("*.html"):
        if f.name == "admin-rotate.html":
            continue
        targets.append(f)
    for f in PRODUCTS_DIR.glob("*.html"):
        if f.name in EXCLUDE_PRODUCT_FILES:
            continue
        targets.append(f)
    for f in NOTES_DIR.glob("*.html"):
        targets.append(f)

    for f in targets:
        src = read_text(f)
        if not re.search(r"site-footer__copy[^>]*>[\s\S]*?2026", src):
            # tolleranza: data-year="2026" presente sul tag
            if not re.search(r'data-year[^>]*>2026', src):
                report("HIGH", f, 1,
                       "Footer senza \"© 2026\" o data-year=\"2026\"",
                       "Allinea anno copyright a 2026.")
        if "04897880169" not in src:
            report("HIGH", f, 1,
                   "P.IVA 04897880169 assente nel footer",
                   "Inserisci P.IVA nel blocco bottom del footer.")
        # Strip marchi
        missing = [b for b in FOOTER_EXPECTED_BRANDS if b not in src]
        if missing:
            sev = "HIGH" if len(missing) >= 2 else "MEDIUM"
            report(sev, f, 1,
                   f"Strip marchi footer manca: {', '.join(missing)}",
                   "Aggiungi tutti i brand nella tagline: " + " · ".join(FOOTER_EXPECTED_BRANDS))
        # Layout footer minimo
        if 'class="site-footer"' not in src:
            report("HIGH", f, 1,
                   "Manca <footer class=\"site-footer\">",
                   "Inserisci footer standard del sito.")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def write_report(out_path: Path) -> None:
    findings.sort(key=lambda r: (SEVERITY_ORDER.index(r["severity"]),
                                  r["file"], r["line"]))
    grouped = defaultdict(list)
    for r in findings:
        grouped[r["severity"]].append(r)

    lines: list[str] = []
    lines.append("# AUDIT FINALE RESIDUO — Motor Garden Bazzana")
    lines.append("")
    lines.append(f"Totale finding: **{len(findings)}**")
    counts = {s: len(grouped[s]) for s in SEVERITY_ORDER}
    lines.append("- CRITICAL: " + str(counts["CRITICAL"]))
    lines.append("- HIGH:     " + str(counts["HIGH"]))
    lines.append("- MEDIUM:   " + str(counts["MEDIUM"]))
    lines.append("- LOW:      " + str(counts["LOW"]))
    lines.append("")
    for sev in SEVERITY_ORDER:
        if not grouped[sev]:
            continue
        lines.append(f"## {sev} ({len(grouped[sev])})")
        for r in grouped[sev]:
            lines.append(f"- `{r['file']}:{r['line']}` — {r['desc']}")
            lines.append(f"  - **Fix:** {r['fix']}")
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def print_summary() -> None:
    counts = {s: 0 for s in SEVERITY_ORDER}
    for r in findings:
        counts[r["severity"]] += 1
    print("===== AUDIT FINALE RESIDUO =====")
    for s in SEVERITY_ORDER:
        print(f"  {s:9s} {counts[s]}")
    print(f"  TOTAL     {len(findings)}")
    print()
    # Top 30 worst
    findings.sort(key=lambda r: (SEVERITY_ORDER.index(r["severity"]),
                                  r["file"], r["line"]))
    shown = 0
    for r in findings:
        if shown >= 30:
            break
        print(f"[{r['severity']:8s}] {r['file']}:{r['line']} — {r['desc']}")
        shown += 1
    if len(findings) > shown:
        print(f"… (+{len(findings)-shown} altre, vedi report file)")


def main() -> int:
    audit_product_pages()
    audit_minor_pages()
    audit_javascript()
    audit_css()
    audit_a11y()
    audit_seo()
    audit_footer_consistency()

    report_path = ROOT / "scripts" / "audit-final-residual.report.md"
    write_report(report_path)
    print_summary()
    print(f"\nReport completo salvato in: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
