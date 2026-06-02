import os, re, glob, sys
from pathlib import Path

ROOT = Path(r"C:\Users\ilbug\Desktop\bazzana_v2")
os.chdir(ROOT)

html_files = list(glob.glob('*.html')) + list(glob.glob('prodotti/*.html')) + list(glob.glob('note/*.html'))

missing_imgs = []  # (file, line, src)
missing_links = []  # (file, line, href)
placeholder_count = 0
real_img_count = 0

for hf in html_files:
    folder = Path(hf).parent
    with open(hf, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        # img src
        for m in re.finditer(r'<img[^>]*\ssrc="([^"]+)"', line):
            src = m.group(1)
            if src.startswith(('http://', 'https://', 'data:', '//')):
                continue
            # Skip template literals (JS strings con ${...})
            if '${' in src or '`' in src:
                continue
            # Risolvi path relativo al file html
            if src.startswith('/'):
                full = (ROOT / src.lstrip('/')).resolve()
            else:
                # Path relativo al file HTML corrente
                full = (ROOT / folder / src).resolve()
            if not full.exists():
                missing_imgs.append((hf, i, src))
        # href
        for m in re.finditer(r'href="([^"]+)"', line):
            href = m.group(1)
            if href.startswith(('http://', 'https://', '#', 'mailto:', 'tel:', 'javascript:', 'data:')):
                continue
            # Skip template literals
            if '${' in href or '`' in href:
                continue
            # Strip query/hash
            clean = href.split('?')[0].split('#')[0]
            if not clean: continue
            if clean.startswith('/'):
                full = (ROOT / clean.lstrip('/')).resolve()
            else:
                # Path relativo al file HTML corrente
                full = (ROOT / folder / clean).resolve()
            if not full.exists():
                missing_links.append((hf, i, href))
        # data-product-img
        for m in re.finditer(r'data-product-img="([^"]+)"', line):
            src = m.group(1)
            if 'placeholder' in src:
                placeholder_count += 1
            else:
                full = (ROOT / src).resolve()
                if full.exists():
                    real_img_count += 1
                else:
                    missing_imgs.append((hf, i, 'data-product-img:' + src))

print(f"=== MISSING IMG ({len(missing_imgs)}) ===")
for f, l, s in missing_imgs[:30]:
    print(f"{f}:{l} -> {s}")
if len(missing_imgs) > 30: print(f"... e altri {len(missing_imgs)-30}")
print()
print(f"=== MISSING HREF ({len(missing_links)}) ===")
for f, l, h in missing_links[:30]:
    print(f"{f}:{l} -> {h}")
if len(missing_links) > 30: print(f"... e altri {len(missing_links)-30}")
print()
print(f"=== PRODOTTI ===")
print(f"data-product-img placeholder: {placeholder_count}")
print(f"data-product-img reali (esistono): {real_img_count}")

# Scene
print(f"\n=== SCENE BAZZANA ===")
for i in range(1, 35):
    p = ROOT / f'assets/img/bazzana/scena-{i:02d}.jpg'
    if not p.exists():
        print(f"  MISSING: scena-{i:02d}.jpg")
