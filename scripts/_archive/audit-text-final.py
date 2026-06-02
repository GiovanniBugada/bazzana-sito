"""
audit-text-final.py
Perfectionist textual audit of all HTML pages in bazzana_v2.

Extracts only visible text (no tags, scripts, styles) and checks:
  A. Italian typos / accent errors
  B. Suspicious sentences / placeholder leftovers
  C. Numeric & nominative consistency (products, brands, phone, email)
  D. Missing/empty/duplicate <h1>, <meta description>, <title>
  E. Missing or generic img alt attributes

Outputs issues grouped by severity: CRITICAL > HIGH > MEDIUM > LOW.
"""

from __future__ import annotations

import io
import os
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

# Force UTF-8 stdout on Windows (cp1252 chokes on Italian accents / arrows)
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(r"C:\Users\ilbug\Desktop\bazzana_v2")

# ---------------------------------------------------------------------------
# HTML extraction
# ---------------------------------------------------------------------------


class VisibleTextExtractor(HTMLParser):
    """Collects (text, line_in_file) tuples for visible text only."""

    SKIP_TAGS = {"script", "style", "noscript", "template", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.in_title = False
        self.title_text: list[str] = []
        # text fragments with their source line in the file
        self.fragments: list[tuple[str, int]] = []
        # meta tags
        self.meta_description: str | None = None
        self.meta_description_line: int | None = None
        # h1 collection
        self.h1_depth = 0
        self.h1_buffer: list[str] = []
        self.h1_start_line: int | None = None
        self.h1s: list[tuple[str, int]] = []
        # img alts
        self.imgs: list[tuple[str, int, str]] = []  # (alt, line, src)
        # title
        self.title_line: int | None = None

    # -- tag handling -------------------------------------------------------

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if tag == "title":
            self.in_title = True
            line, _ = self.getpos()
            self.title_line = line
        if tag == "meta":
            name = (attr_dict.get("name") or "").lower()
            if name == "description":
                line, _ = self.getpos()
                self.meta_description = (attr_dict.get("content") or "").strip()
                self.meta_description_line = line
        if tag == "h1":
            self.h1_depth += 1
            if self.h1_depth == 1:
                line, _ = self.getpos()
                self.h1_start_line = line
                self.h1_buffer = []
        if tag == "img":
            line, _ = self.getpos()
            alt = attr_dict.get("alt")
            src = attr_dict.get("src") or ""
            self.imgs.append((alt if alt is not None else "<MISSING>", line, src))

    def handle_startendtag(self, tag, attrs):
        # treat self-closing img/meta exactly like a start tag
        if tag in {"img", "meta"}:
            self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS:
            if self.skip_depth > 0:
                self.skip_depth -= 1
            return
        if tag == "title":
            self.in_title = False
        if tag == "h1":
            if self.h1_depth > 0:
                self.h1_depth -= 1
            if self.h1_depth == 0:
                text = " ".join(self.h1_buffer).strip()
                self.h1s.append((text, self.h1_start_line or 0))
                self.h1_buffer = []
                self.h1_start_line = None

    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        line, _ = self.getpos()
        if self.in_title:
            self.title_text.append(data)
        if self.h1_depth > 0:
            self.h1_buffer.append(data)
        if data.strip():
            self.fragments.append((data, line))


# ---------------------------------------------------------------------------
# Issue collection
# ---------------------------------------------------------------------------

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


class IssueLog:
    def __init__(self) -> None:
        self.items: list[tuple[str, str, int, str, str]] = []
        # (severity, rel_path, line, category, message)

    def add(self, severity: str, path: Path, line: int, category: str, msg: str) -> None:
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        self.items.append((severity, rel, line, category, msg))

    def render(self) -> str:
        self.items.sort(key=lambda it: (SEVERITY_ORDER[it[0]], it[1], it[2]))
        by_sev: dict[str, list[tuple[str, int, str, str]]] = defaultdict(list)
        for sev, rel, line, cat, msg in self.items:
            by_sev[sev].append((rel, line, cat, msg))

        out: list[str] = []
        out.append("=" * 78)
        out.append("AUDIT TESTUALE — bazzana_v2 — 44 pagine HTML")
        out.append("=" * 78)

        total = len(self.items)
        counts = {s: len(v) for s, v in by_sev.items()}
        out.append(
            f"Totale issue: {total}  |  CRITICAL={counts.get('CRITICAL',0)}  "
            f"HIGH={counts.get('HIGH',0)}  MEDIUM={counts.get('MEDIUM',0)}  "
            f"LOW={counts.get('LOW',0)}"
        )
        out.append("")

        for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            rows = by_sev.get(sev, [])
            if not rows:
                continue
            out.append("-" * 78)
            out.append(f"[{sev}]  {len(rows)} issue")
            out.append("-" * 78)
            for rel, line, cat, msg in rows:
                out.append(f"  {rel}:{line}  ({cat})  {msg}")
            out.append("")
        return "\n".join(out)


# ---------------------------------------------------------------------------
# Italian typo patterns (A)
# ---------------------------------------------------------------------------

WORD_CHARS_BEFORE = r"(?<![A-Za-zÀ-ÿ])"
WORD_CHARS_AFTER = r"(?![A-Za-zÀ-ÿ])"


def w(p: str) -> re.Pattern:
    return re.compile(WORD_CHARS_BEFORE + p + WORD_CHARS_AFTER, re.IGNORECASE)


# Pattern definitions:  (regex, severity, message)
TYPO_PATTERNS: list[tuple[re.Pattern, str, str]] = [
    (re.compile(r"qual'è", re.IGNORECASE), "HIGH", "Refuso: 'qual'è' senza apostrofo — corretto 'qual è'"),
    (re.compile(r"\bperchè\b", re.IGNORECASE), "HIGH", "Accento errato: 'perchè' — corretto 'perché'"),
    (re.compile(r"\bnonche\b", re.IGNORECASE), "HIGH", "Accento mancante: 'nonche' — corretto 'nonché'"),
    (re.compile(r"\bnonchè\b", re.IGNORECASE), "HIGH", "Accento grave errato: 'nonchè' — corretto 'nonché'"),
    (re.compile(r"\baffinche\b", re.IGNORECASE), "HIGH", "Accento mancante: 'affinche' — corretto 'affinché'"),
    (re.compile(r"\baffinchè\b", re.IGNORECASE), "HIGH", "Accento grave errato: 'affinchè' — corretto 'affinché'"),
    (re.compile(r"\bpoichè\b", re.IGNORECASE), "HIGH", "Accento errato: 'poichè' — corretto 'poiché'"),
    (re.compile(r"\bpoiche\b", re.IGNORECASE), "HIGH", "Accento mancante: 'poiche' — corretto 'poiché'"),
    (re.compile(r"\bgiache\b", re.IGNORECASE), "MEDIUM", "Accento mancante: 'giache' — corretto 'giacché'"),
    (re.compile(r"\bsicche\b", re.IGNORECASE), "MEDIUM", "Accento mancante: 'sicche' — corretto 'sicché'"),
    (re.compile(r"\bbenche\b", re.IGNORECASE), "HIGH", "Accento mancante: 'benche' — corretto 'benché'"),
    (re.compile(r"\bdaccordo\b", re.IGNORECASE), "HIGH", "Refuso: 'daccordo' — corretto 'd'accordo'"),
    (re.compile(r"\bapartire\b", re.IGNORECASE), "HIGH", "Refuso: 'apartire' — corretto 'a partire'"),
    (re.compile(r"\bdapertutto\b", re.IGNORECASE), "HIGH", "Refuso: 'dapertutto' — corretto 'dappertutto'"),
    (re.compile(r"\bcosi\b"), "MEDIUM", "Accento mancante: 'cosi' — corretto 'così'"),
    (re.compile(r"\bgia\b"), "MEDIUM", "Accento mancante: 'gia' — corretto 'già'"),
    (re.compile(r"\bpiu\b"), "MEDIUM", "Accento mancante: 'piu' — corretto 'più'"),
    (re.compile(r"\bpero\b"), "LOW", "Accento mancante possibile: 'pero' (albero) vs 'però' — verificare"),
    (re.compile(r"\bun altra\b", re.IGNORECASE), "HIGH", "Refuso: 'un altra' — corretto 'un'altra'"),
    (re.compile(r"\bun'altro\b", re.IGNORECASE), "HIGH", "Refuso: 'un'altro' — corretto 'un altro' (maschile)"),
    (re.compile(r"\bun'amico\b", re.IGNORECASE), "MEDIUM", "Refuso: 'un'amico' — corretto 'un amico' (maschile)"),
    (re.compile(r"\bun ora\b", re.IGNORECASE), "MEDIUM", "Refuso: 'un ora' — corretto 'un'ora'"),
    (re.compile(r"\bun anno\b", re.IGNORECASE), "LOW", "Possibile refuso: 'un anno' va bene (maschile), conferma"),
    (re.compile(r"\be' "), "CRITICAL", "Encoding/refuso: \"e' \" — corretto \"è \""),
    (re.compile(r"\bE' "), "CRITICAL", "Encoding/refuso: \"E' \" — corretto \"È \""),
    (re.compile(r" {3,}"), "LOW", "Tripli (o più) spazi consecutivi"),
    (re.compile(r"&nbsp;&nbsp;"), "MEDIUM", "Doppio &nbsp; consecutivo (entità HTML non risolte)"),
    (re.compile(r"&amp;amp;"), "HIGH", "Doppia codifica HTML &amp;amp;"),
    (re.compile(r"\bufficina\b", re.IGNORECASE), "CRITICAL", "Refuso grave: 'ufficina' — corretto 'officina'"),
    (re.compile(r"\bpoò\b", re.IGNORECASE), "CRITICAL", "Refuso: 'poò'"),
    (re.compile(r"\ba fatto\b"), "MEDIUM",
     "Possibile verbo 'avere' senza h: 'a fatto' → 'ha fatto' (verificare contesto)"),
    (re.compile(r"\ba detto\b"), "MEDIUM",
     "Possibile verbo 'avere' senza h: 'a detto' → 'ha detto' (verificare contesto)"),
    (re.compile(r"\ba avuto\b"), "MEDIUM",
     "Possibile verbo 'avere' senza h: 'a avuto' → 'ha avuto'"),
]

# pò standalone (without apostrophe) is wrong — match exactly "pò" surrounded by non-letters
PO_PATTERN = re.compile(r"(?<![A-Za-zÀ-ÿ])pò(?![A-Za-zÀ-ÿ'])", re.IGNORECASE)

# ASCII apostrophe used as accent (è → e', à → a', ì → i', ù → u', ò → o')
# Common Italian words written wrong this way: "velocita'", "capacita'", "e' ", "qualita'", etc.
APOSTROPHE_ACCENT_PATTERNS: list[tuple[re.Pattern, str, str]] = [
    (re.compile(r"\b(velocita|capacita|qualita|attivita|verita|liberta|citta|universita|comunita|societa|necessita|possibilita|maesta|eta|meta)'", re.IGNORECASE),
     "CRITICAL", "Apostrofo ASCII al posto di 'à' su parola tronca (es. 'velocita\\'' → 'velocità')"),
    (re.compile(r"\bSi'(?=[\s,.;:!?])"), "CRITICAL", "Apostrofo ASCII al posto di 'ì' in 'Si\\'' → 'Sì'"),
    (re.compile(r"\b(?:cosi|cos[ií])'\B"), "MEDIUM", "Apostrofo ASCII su 'cosi\\'' — verificare"),
    (re.compile(r"\bgia'(?=\W)"), "CRITICAL", "Apostrofo ASCII al posto di 'à' in 'gia\\'' → 'già'"),
    (re.compile(r"\bpiu'(?=\W)"), "CRITICAL", "Apostrofo ASCII al posto di 'ù' in 'piu\\'' → 'più'"),
    (re.compile(r"\bpoi'(?=\W)"), "MEDIUM", "Apostrofo sospetto in 'poi\\'' (verifica contesto)"),
    (re.compile(r"\bperche'(?=\W)"), "CRITICAL", "Apostrofo ASCII su 'perche\\'' → 'perché'"),
    (re.compile(r"\bcosi'(?=\W)"), "CRITICAL", "Apostrofo ASCII su 'cosi\\'' → 'così'"),
]

PLACEHOLDER_PATTERNS: list[tuple[re.Pattern, str, str]] = [
    (re.compile(r"\blorem\s+ipsum\b", re.IGNORECASE), "CRITICAL", "Lorem ipsum placeholder dimenticato"),
    (re.compile(r"\bTODO\b"), "CRITICAL", "TODO placeholder dimenticato"),
    (re.compile(r"\bFIXME\b"), "CRITICAL", "FIXME placeholder dimenticato"),
    (re.compile(r"\bPLACEHOLDER\b", re.IGNORECASE), "CRITICAL", "PLACEHOLDER testuale dimenticato"),
    (re.compile(r"\bTBD\b"), "HIGH", "TBD ('to be done') dimenticato"),
    (re.compile(r"\b(xxx|XXX)\b"), "HIGH", "XXX placeholder testuale"),
    (re.compile(r"\b(asdf|qwerty)\b", re.IGNORECASE), "CRITICAL", "Testo di prova (asdf/qwerty)"),
]

# Mojibake & encoding glitches: typical UTF-8 mis-decoded sequences
MOJIBAKE_PATTERNS: list[tuple[re.Pattern, str, str]] = [
    (re.compile(r"Ã[©¨¬²Ãa-z]"), "HIGH", "Possibile mojibake (UTF-8 letto come Latin-1)"),
    (re.compile(r"â€™"), "HIGH", "Mojibake apostrofo curly â€™"),
    (re.compile(r"â€œ|â€"), "HIGH", "Mojibake virgolette curly"),
    (re.compile(r"�"), "CRITICAL", "Carattere di replacement U+FFFD (encoding rotto)"),
]

# Sanity reference for brand names
BRAND_CANONICAL = ["Stihl", "Active", "Oleo-Mac", "Kress", "Shindaiwa", "Ligier", "Weibang", "Honda"]
BRAND_VARIANTS: dict[str, list[str]] = {
    "Stihl": [r"\bSTIHL\b", r"\bsthil\b", r"\bsthil\b"],
    "Oleo-Mac": [r"\bOleomac\b", r"\bOleo Mac\b", r"\bOLEO-MAC\b", r"\bOleo\-mac\b"],
    "Weibang": [r"\bWEI\s?BANG\b", r"\bWei Bang\b", r"\bwei\-bang\b"],
    "Shindaiwa": [r"\bshindaiva\b", r"\bShin Daiwa\b"],
    "Ligier": [r"\bLIGIER\b"],
    "Kress": [r"\bKRESS\b", r"\bkress\b"],
}

PHONE_CANONICAL = "346 4156981"
PHONE_NORMALIZED = re.compile(r"3\s?4\s?6\s*4\s?1\s?5\s?6\s?9\s?8\s?1")
PHONE_ANY = re.compile(r"\b(?:\+39\s*)?(?:0\d{1,3}[\s.\-]?\d{6,8}|3\d{2}[\s.\-]?\d{6,7})\b")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")


# ---------------------------------------------------------------------------
# Sentence-level checks (B)
# ---------------------------------------------------------------------------


def check_sentences(text: str) -> list[tuple[str, str]]:
    """Returns list of (severity, message) for sentence-level issues in a chunk."""
    issues: list[tuple[str, str]] = []

    # Lowercase start after period inside same chunk (allow proper nouns: skip if next word starts with caps elsewhere)
    # Pattern: ". word" where word starts with lowercase Italian letter, and is followed by another word (avoid file extensions, urls).
    for m in re.finditer(r"\.\s+([a-zà-ÿ])([a-zà-ÿ]{2,})\b", text):
        # Skip URLs, file extensions, abbreviations like "e.g."
        ctx_start = max(0, m.start() - 25)
        ctx = text[ctx_start: m.end() + 10]
        if any(tok in ctx.lower() for tok in ("http", "www.", ".html", ".com", ".it", "p.iva", "p. iva", "n.", "art.", "fig.", "es.", "vol.", "v.", "etc.")):
            continue
        if m.group(1) + m.group(2) in {"www", "html", "com", "it"}:
            continue
        issues.append(("LOW", f"Possibile frase che inizia con minuscola dopo punto: '...{m.group(0).strip()}...'"))

    return issues


# ---------------------------------------------------------------------------
# Audit single file
# ---------------------------------------------------------------------------


def audit_file(path: Path, log: IssueLog,
               titles: dict[str, list[Path]],
               descriptions: dict[str, list[Path]],
               brand_hits: dict[str, set[Path]]) -> None:
    raw = path.read_text(encoding="utf-8", errors="replace")
    parser = VisibleTextExtractor()
    try:
        parser.feed(raw)
        parser.close()
    except Exception as e:
        log.add("HIGH", path, 0, "PARSE", f"Errore parser HTML: {e}")
        return

    # -- A. typos / encoding -----------------------------------------------
    for text, line in parser.fragments:
        # Skip text fragments that are 100% inside what looks like a code block tag content
        for pat, sev, msg in TYPO_PATTERNS:
            if pat.search(text):
                # tripli spazi: la maggior parte è indent HTML tra nodi di testo (\n+spaces),
                # non veri tripli spazi nel testo finale renderizzato. Ignora se il match
                # è puramente whitespace o se il testo contiene newline (indent HTML).
                if pat.pattern == r" {3,}":
                    if text.strip() == "":
                        continue
                    # se il blocco di spazi è preceduto/seguito da newline → indent HTML, non visibile
                    triple_match = re.search(r" {3,}", text)
                    if triple_match:
                        m_start, m_end = triple_match.span()
                        before = text[:m_start]
                        after = text[m_end:]
                        if before.endswith("\n") or after.startswith("\n") or "\n" in before[-5:] or "\n" in after[:5]:
                            continue
                        # se subito prima/dopo non c'è testo significativo, skip
                        if before.strip() == "" or after.strip() == "":
                            continue
                log.add(sev, path, line, "TYPO", f"{msg} — frammento: '{text.strip()[:80]}'")

        if PO_PATTERN.search(text):
            log.add("HIGH", path, line, "TYPO",
                    "Refuso: 'pò' senza apostrofo — corretto \"po'\" — frammento: '"
                    + text.strip()[:80] + "'")

        for pat, sev, msg in APOSTROPHE_ACCENT_PATTERNS:
            if pat.search(text):
                log.add(sev, path, line, "TYPO",
                        f"{msg} — frammento: '{text.strip()[:80]}'")

        for pat, sev, msg in PLACEHOLDER_PATTERNS:
            if pat.search(text):
                log.add(sev, path, line, "PLACEHOLDER",
                        f"{msg} — frammento: '{text.strip()[:80]}'")

        for pat, sev, msg in MOJIBAKE_PATTERNS:
            if pat.search(text):
                log.add(sev, path, line, "ENCODING",
                        f"{msg} — frammento: '{text.strip()[:80]}'")

        for sev, msg in check_sentences(text):
            log.add(sev, path, line, "PROSE", msg)

    # also check raw HTML (not just visible text) for &amp;amp; / &nbsp;&nbsp;
    if "&amp;amp;" in raw:
        log.add("HIGH", path, 0, "ENCODING", "&amp;amp; (doppia codifica) presente nel sorgente")
    if re.search(r"&nbsp;\s*&nbsp;\s*&nbsp;", raw):
        log.add("MEDIUM", path, 0, "ENCODING", "Tripli &nbsp; consecutivi nel sorgente")

    # -- B. brand variants ---------------------------------------------------
    full_text = " ".join(t for t, _ in parser.fragments)
    for canon, variants in BRAND_VARIANTS.items():
        for v in variants:
            for m in re.finditer(v, full_text):
                # Find approximate line
                snippet = m.group(0)
                # Search for first fragment containing snippet
                for text, line in parser.fragments:
                    if snippet in text:
                        log.add("MEDIUM", path, line, "BRAND",
                                f"Variante non canonica '{snippet}' del marchio '{canon}' "
                                f"— uniformare a '{canon}'")
                        break

    # -- C. brand presence (only for officina/prodotti/index)
    for canon in BRAND_CANONICAL:
        if re.search(r"\b" + re.escape(canon) + r"\b", full_text):
            brand_hits[canon].add(path)

    # -- D. title / description / h1 ----------------------------------------
    title_text = "".join(parser.title_text).strip()
    if not title_text:
        log.add("CRITICAL", path, parser.title_line or 0, "META",
                "<title> vuoto o assente")
    else:
        if len(title_text) > 70:
            log.add("MEDIUM", path, parser.title_line or 0, "META",
                    f"<title> > 70 char ({len(title_text)}): '{title_text[:80]}'")
        if title_text.lower() in {"titolo", "title", "untitled", "document"}:
            log.add("CRITICAL", path, parser.title_line or 0, "META",
                    f"<title> generico: '{title_text}'")
        titles[title_text].append(path)

    if parser.meta_description is None:
        log.add("HIGH", path, 0, "META", "<meta name=\"description\"> assente")
    elif not parser.meta_description.strip():
        log.add("HIGH", path, parser.meta_description_line or 0, "META",
                "<meta description> vuota")
    else:
        descriptions[parser.meta_description.strip()].append(path)

    if not parser.h1s:
        log.add("HIGH", path, 0, "STRUCT", "Nessun <h1> trovato nella pagina")
    else:
        for h1_text, h1_line in parser.h1s:
            if not h1_text:
                log.add("CRITICAL", path, h1_line, "STRUCT", "<h1> vuoto")
            elif h1_text.lower() in {"titolo", "title", "h1"}:
                log.add("CRITICAL", path, h1_line, "STRUCT",
                        f"<h1> generico: '{h1_text}'")
        if len(parser.h1s) > 1:
            log.add("MEDIUM", path, parser.h1s[0][1], "STRUCT",
                    f"Pagina con {len(parser.h1s)} <h1> (consigliato uno solo)")

    # -- E. img alt ----------------------------------------------------------
    for alt, line, src in parser.imgs:
        # Decide if image is decorative: aria-hidden? Not tracked here, so treat alt="" as accepted
        if alt == "<MISSING>":
            log.add("HIGH", path, line, "ALT", f"<img> senza attributo alt — src='{src}'")
            continue
        stripped = alt.strip()
        if alt == "":
            # alt vuoto esplicito = decorativa, ok
            continue
        if stripped == "" and alt != "":
            log.add("HIGH", path, line, "ALT",
                    f"alt con soli spazi vuoti — src='{src}'")
            continue
        low = stripped.lower()
        if low in {"img", "image", "foto", "picture", "immagine", "photo", "logo", "icon"}:
            log.add("MEDIUM", path, line, "ALT",
                    f"alt generico '{stripped}' — src='{src}'")
            continue
        # alt that simply repeats the filename
        filename = os.path.basename(src).lower()
        filename_no_ext = re.sub(r"\.[a-z0-9]+$", "", filename)
        if filename_no_ext and (low == filename or low == filename_no_ext):
            log.add("MEDIUM", path, line, "ALT",
                    f"alt ripete il filename: '{stripped}' src='{src}'")

    # -- F. phone / email consistency in raw text ---------------------------
    # Build a "context-aware" search: exclude matches that are clearly P.IVA / VAT numbers.
    phones_found: set[str] = set()
    for m in PHONE_ANY.finditer(full_text):
        match_start = m.start()
        ctx_before = full_text[max(0, match_start - 30): match_start].lower()
        if "p.iva" in ctx_before or "p. iva" in ctx_before or \
           "partita iva" in ctx_before or "vat" in ctx_before or "cf:" in ctx_before:
            continue
        phones_found.add(m.group(0))
    for p in phones_found:
        digits = re.sub(r"[^\d]", "", p)
        if digits.startswith("39"):
            digits = digits[2:]
        # The canonical mobile is 3464156981; also accept the P.IVA digits as harmless
        if digits == "04897880169" or digits == "4897880169":
            continue  # P.IVA digits picked up by phone regex — false positive
        if digits != "3464156981" and len(digits) >= 9:
            log.add("MEDIUM", path, 0, "CONSISTENCY",
                    f"Telefono non canonico '{p}' (atteso '346 4156981')")

    emails = set(EMAIL_RE.findall(full_text))
    for em in emails:
        if em.lower() not in {"bazzanamotorgarden@gmail.com",
                              "info@bazzanamotorgarden.it",
                              "scuolaclaude@gmail.com"}:
            # Just record extra emails as LOW (could be intentional, e.g., link to suppliers)
            log.add("LOW", path, 0, "CONSISTENCY",
                    f"Email non standard rilevata: '{em}' (verificare se intenzionale)")


# ---------------------------------------------------------------------------
# Cross-file consistency
# ---------------------------------------------------------------------------


def cross_file_checks(log: IssueLog,
                      titles: dict[str, list[Path]],
                      descriptions: dict[str, list[Path]],
                      brand_hits: dict[str, set[Path]],
                      files: list[Path]) -> None:
    # Duplicate titles
    for title, paths in titles.items():
        if len(paths) > 1 and len(title) > 8:
            for p in paths:
                log.add("MEDIUM", p, 0, "META",
                        f"<title> duplicato in {len(paths)} pagine: '{title[:70]}'")

    # Duplicate descriptions
    for desc, paths in descriptions.items():
        if len(paths) > 1 and len(desc) > 30:
            for p in paths:
                log.add("HIGH", p, 0, "META",
                        f"<meta description> duplicata in {len(paths)} pagine: '{desc[:70]}...'")

    # Brand presence across site (informative)
    expected_brands_on = ["officina.html", "index.html", "prodotti.html"]
    site_dir = ROOT
    for canon in BRAND_CANONICAL:
        present_in = brand_hits.get(canon, set())
        # only warn if a canonical brand is *never* mentioned anywhere
        if not present_in:
            log.add("HIGH", site_dir / "officina.html", 0, "CONSISTENCY",
                    f"Marchio canonico '{canon}' non rilevato in nessuna pagina")


def numeric_consistency(log: IssueLog, files: list[Path]) -> None:
    """Check the claim that the site has 650 prodotti, 8 marchi, 10+ anni, 129 foto."""
    targets = {
        "prodotti": [re.compile(r"\b(\d{2,4})\s*\+?\s*prodott", re.IGNORECASE),
                     re.compile(r"\b(\d{2,4})\s*prodott", re.IGNORECASE)],
        "marchi":   [re.compile(r"\b(\d{1,3})\s*\+?\s*march", re.IGNORECASE),
                     re.compile(r"\b(\d{1,3})\s*march", re.IGNORECASE)],
        "anni":     [re.compile(r"\b(\d{1,3})\s*\+?\s*anni", re.IGNORECASE)],
        "foto":     [re.compile(r"\b(\d{1,4})\s*\+?\s*foto", re.IGNORECASE)],
    }
    expected = {"prodotti": 650, "marchi": 8, "anni_min": 10, "foto": 129}

    findings: dict[str, set[tuple[Path, int, str]]] = defaultdict(set)
    for p in files:
        raw = p.read_text(encoding="utf-8", errors="replace")
        # strip tags for safer matching
        text_only = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
        text_only = re.sub(r"<style.*?</style>", " ", text_only, flags=re.S | re.I)
        text_only = re.sub(r"<[^>]+>", " ", text_only)
        for key, pats in targets.items():
            for pat in pats:
                for m in pat.finditer(text_only):
                    findings[key].add((p, 0, m.group(0).strip()))

    for key, hits in findings.items():
        for p, line, snippet in hits:
            digits = re.findall(r"\d+", snippet)
            if not digits:
                continue
            n = int(digits[0])
            if key == "prodotti" and n not in (expected["prodotti"],):
                if 50 <= n <= 9999:  # filter noise
                    log.add("MEDIUM", p, line, "CONSISTENCY",
                            f"Numero prodotti '{snippet}' incoerente con atteso {expected['prodotti']}")
            elif key == "marchi" and n not in (expected["marchi"],):
                if 1 <= n <= 100:
                    log.add("MEDIUM", p, line, "CONSISTENCY",
                            f"Numero marchi '{snippet}' incoerente con atteso {expected['marchi']}")
            elif key == "anni" and n < expected["anni_min"]:
                # Skip 0 (animated counter starting value) and small values in blog articles
                # describing time periods (es. "5 anni di garanzia").
                if n == 0:
                    continue
                if p.name == "index.html" or "officina" in p.name or "storia" in p.name:
                    log.add("LOW", p, line, "CONSISTENCY",
                            f"Numero anni '{snippet}' < {expected['anni_min']} attesi (verificare contesto)")
            elif key == "foto" and n != expected["foto"]:
                if 10 <= n <= 9999:
                    log.add("LOW", p, line, "CONSISTENCY",
                            f"Numero foto '{snippet}' diverso da atteso {expected['foto']}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    html_files = sorted(ROOT.glob("*.html")) + \
                 sorted((ROOT / "prodotti").glob("*.html")) + \
                 sorted((ROOT / "note").glob("*.html"))

    # filter out admin/utility pages that don't need linguistic audit
    excluded = {"admin-rotate.html"}
    html_files = [p for p in html_files if p.name not in excluded]

    log = IssueLog()
    titles: dict[str, list[Path]] = defaultdict(list)
    descriptions: dict[str, list[Path]] = defaultdict(list)
    brand_hits: dict[str, set[Path]] = defaultdict(set)

    for p in html_files:
        audit_file(p, log, titles, descriptions, brand_hits)

    cross_file_checks(log, titles, descriptions, brand_hits, html_files)
    numeric_consistency(log, html_files)

    report = log.render()
    print(f"Pagine analizzate: {len(html_files)}\n")
    print(report)

    out_path = ROOT / "scripts" / "audit-text-final.report.txt"
    out_path.write_text(report, encoding="utf-8")
    print(f"\nReport scritto in: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
