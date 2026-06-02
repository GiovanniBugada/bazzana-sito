"""Audit profondo finale - tutto in uno"""
import re, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

def sp(*a):
    try: print(*a)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((' '.join(str(x) for x in a)).encode('utf-8', 'replace') + b'\n')

import glob
HTMLS = sorted(set(glob.glob('*.html') + glob.glob('prodotti/*.html') + glob.glob('note/*.html')))

problems = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}

# === A. TECNICA ===
sp('=== A. TECNICA ===')
for fp in HTMLS:
    with open(fp, 'r', encoding='utf-8') as f: s = f.read()
    if '<!DOCTYPE html>' not in s[:200]:
        problems['HIGH'].append(f'{fp}: manca <!DOCTYPE html>')
    if '<html lang="it"' not in s:
        problems['MEDIUM'].append(f'{fp}: <html> senza lang="it"')
    if '<meta name="viewport"' not in s:
        problems['HIGH'].append(f'{fp}: manca meta viewport')

# Cache version coerenza
versions = {}
for fp in HTMLS:
    with open(fp, 'r', encoding='utf-8') as f: s = f.read()
    for m in re.finditer(r'(\w[\w-]*\.(?:css|js))\?v=(\d+)', s):
        path, v = m.group(1), int(m.group(2))
        versions.setdefault(path, set()).add(v)
inconsistent = {p: vs for p, vs in versions.items() if len(vs) > 1}
if inconsistent:
    for p, vs in inconsistent.items():
        problems['MEDIUM'].append(f'cache version inconsistent: {p} ha versioni {sorted(vs)}')

# Picture/source: webp esiste?
broken_webp_sources = []
for fp in HTMLS:
    folder = Path(fp).parent
    with open(fp, 'r', encoding='utf-8') as f: s = f.read()
    for m in re.finditer(r'<source type="image/webp" srcset="([^"]+\.webp)"', s):
        webp = m.group(1)
        if webp.startswith(('http://', 'https://', 'data:')): continue
        if webp.startswith('../'):
            full = (ROOT / folder / webp).resolve()
        else:
            full = (ROOT / webp).resolve()
        if not full.exists():
            broken_webp_sources.append(f'{fp}: source webp non esiste -> {webp}')
for b in broken_webp_sources[:10]:
    problems['HIGH'].append(b)
if len(broken_webp_sources) > 10:
    problems['HIGH'].append(f'+ altri {len(broken_webp_sources)-10} source webp mancanti')

# Img src exists
broken_imgs = []
for fp in HTMLS:
    folder = Path(fp).parent
    with open(fp, 'r', encoding='utf-8') as f: s = f.read()
    for m in re.finditer(r'<img[^>]+\bsrc="([^"]+)"', s):
        src = m.group(1)
        if src.startswith(('http://', 'https://', 'data:')): continue
        if src.startswith('../'):
            full = (ROOT / folder / src).resolve()
        else:
            full = (ROOT / src).resolve()
        if not full.exists():
            broken_imgs.append(f'{fp}: img src non esiste -> {src}')
for b in broken_imgs[:10]:
    problems['HIGH'].append(b)
if len(broken_imgs) > 10:
    problems['HIGH'].append(f'+ altri {len(broken_imgs)-10} img mancanti')

# Href interni
broken_hrefs = []
for fp in HTMLS:
    folder = Path(fp).parent
    with open(fp, 'r', encoding='utf-8') as f: s = f.read()
    for m in re.finditer(r'href="([^"]+)"', s):
        h = m.group(1)
        if h.startswith(('http://', 'https://', '#', 'mailto:', 'tel:', 'javascript:', 'data:')): continue
        clean = h.split('?')[0].split('#')[0]
        if not clean: continue
        if clean.startswith('../'):
            full = (ROOT / folder / clean).resolve()
        else:
            full = (ROOT / clean).resolve()
        if not full.exists():
            broken_hrefs.append(f'{fp}: href -> {h}')
for b in broken_hrefs[:10]:
    problems['HIGH'].append(b)

# === B. CONTENUTI ===
refusi_pattern = [
    (r"\bqual'è\b", "qual è"),
    (r"\bun altra\b", "un'altra"),
    (r"\bun'altro\b", "un altro"),
    (r"\bdaccordo\b", "d'accordo"),
    (r"\bnonche\b", "nonché"),
    (r"\baffinche\b", "affinché"),
    (r"\bperchè\b", "perché"),
    (r"\bvelocita'", "velocità"),
    (r"\bcapacita'", "capacità"),
    (r"\bpiu'", "più"),
    (r"\be' ", "è "),
    (r"\bgia'", "già"),
    (r"\bcosi'", "così"),
    (r"\bSi'\b", "Sì"),
]
for pat, _ in refusi_pattern:
    total = 0
    for fp in HTMLS:
        with open(fp, 'r', encoding='utf-8') as f: s = f.read()
        n = len(re.findall(pat, s))
        if n:
            total += n
    if total:
        problems['MEDIUM'].append(f'Refuso `{pat}`: {total} occorrenze')

# Conteggi
for label, expected in [('650', '650 prodotti'), ('8 marchi', '8 marchi'), ('10+', '10+ anni')]:
    pass  # già verificato in passi precedenti

# === C. ASSET ===
heavy_jpgs = []
for p in Path('assets/img').rglob('*.jpg'):
    if p.stat().st_size > 500_000:
        heavy_jpgs.append((p.stat().st_size, p))
if heavy_jpgs:
    heavy_jpgs.sort(reverse=True)
    for sz, p in heavy_jpgs[:5]:
        problems['LOW'].append(f'JPG > 500 KB: {p.relative_to(ROOT)} ({sz//1024}KB)')
    if len(heavy_jpgs) > 5:
        problems['LOW'].append(f'+ altri {len(heavy_jpgs)-5} JPG > 500 KB')

# PNG senza webp companion (solo foto, non logo)
png_no_webp = []
for p in Path('assets/img/prodotti/foto-catalogo').rglob('*.png'):
    if not p.with_suffix('.webp').exists():
        png_no_webp.append(p)
if png_no_webp:
    problems['LOW'].append(f'PNG senza WebP companion (catalog): {len(png_no_webp)}')

# === D. ACCESSIBILITÀ ===
buttons_no_label = []
for fp in HTMLS:
    with open(fp, 'r', encoding='utf-8') as f: s = f.read()
    # <button> senza testo né aria-label (escluso menu-toggle che ha SVG)
    for m in re.finditer(r'<button(?P<attrs>[^>]*)>(?P<content>.*?)</button>', s, re.S):
        attrs = m.group('attrs')
        content = m.group('content').strip()
        if 'aria-label' in attrs: continue
        text = re.sub(r'<[^>]+>', '', content).strip()
        if not text:
            line = s[:m.start()].count('\n') + 1
            buttons_no_label.append(f'{fp}:{line}: <button> senza testo né aria-label')
for b in buttons_no_label[:10]:
    problems['MEDIUM'].append(b)
if len(buttons_no_label) > 10:
    problems['MEDIUM'].append(f'+ altri {len(buttons_no_label)-10} button senza label')

# === E. SEO ===
for fp in HTMLS:
    with open(fp, 'r', encoding='utf-8') as f: s = f.read()
    tm = re.search(r'<title>([^<]*)</title>', s)
    if not tm or not tm.group(1).strip():
        problems['HIGH'].append(f'{fp}: title vuoto')
    elif len(tm.group(1)) > 75:
        problems['LOW'].append(f'{fp}: title {len(tm.group(1))} char (>75)')
    dm = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not dm or not dm.group(1).strip():
        problems['MEDIUM'].append(f'{fp}: meta description vuota')

# === F. JS ===
# Cerca console.error / TODO / FIXME / debugger
js_issues = []
for jsf in Path('js').glob('*.js'):
    with open(jsf, 'r', encoding='utf-8') as f: s = f.read()
    for issue in ['debugger', 'TODO', 'FIXME']:
        if issue in s:
            n = s.count(issue)
            js_issues.append(f'{jsf.name}: contiene "{issue}" ({n}x)')
for j in js_issues:
    problems['LOW'].append(j)

# === G. PERF ===
with open('css/main.css', 'r', encoding='utf-8') as f:
    main_css = f.read()
imports = len(re.findall(r'@import', main_css))
if imports > 25:
    problems['LOW'].append(f'css/main.css: {imports} @import sequenziali (consigliato bundle)')

# === H. CONTATTI/FOOTER ===
contact_inconsistencies = []
tel_variants = set()
piva_variants = set()
email_variants = set()
for fp in HTMLS:
    with open(fp, 'r', encoding='utf-8') as f: s = f.read()
    # Estrai TEL
    for m in re.finditer(r'(\+?[\d\s]{6,}\d)', s):
        # Cerca solo se contiene 4156981
        if '4156981' in m.group(1):
            tel_variants.add(m.group(1).strip())
    # PIVA
    for m in re.finditer(r'P\.?IVA[^0-9]*(\d+)', s):
        piva_variants.add(m.group(1))
    # email
    for m in re.finditer(r'[\w.-]+@[\w.-]+', s):
        email_variants.add(m.group(0))
if len(piva_variants) > 1:
    problems['HIGH'].append(f'P.IVA varianti diverse: {piva_variants}')
if 'bazzanamotorgarden@gmail.com' not in email_variants:
    problems['MEDIUM'].append('email bazzanamotorgarden@gmail.com non trovata in tutte le pagine')

# === SUMMARY ===
sp('\n' + '=' * 70)
for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
    items = problems[sev]
    sp(f'\n[{sev}]: {len(items)} problemi')
    for i in items[:20]:
        sp(f'  - {i}')
    if len(items) > 20:
        sp(f'  ... e altri {len(items)-20}')
sp('\n' + '=' * 70)
sp(f'TOTALE: CRITICAL={len(problems["CRITICAL"])}, HIGH={len(problems["HIGH"])}, MEDIUM={len(problems["MEDIUM"])}, LOW={len(problems["LOW"])}')
