"""
Install Weibang photos from zip -> assets/img/prodotti/weibang/
+ optimize size (resize 1400px max, q=82) + WebP companion
+ update HTML schede prodotto Weibang
"""
import zipfile, os, shutil, re
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print('PIL non disponibile: salto resize/webp')

ROOT = Path(__file__).resolve().parent.parent
ZIP = Path(r'C:\Users\ilbug\Downloads\weibang.zip')
DEST = ROOT / 'assets' / 'img' / 'prodotti' / 'weibang'
DEST.mkdir(parents=True, exist_ok=True)

mapping = {
    'WB 452 HE.webp': ('weibang-wb-452-he', 'webp'),
    'WB 456 SCVE3.jpg': ('weibang-wb-456-scve3', 'jpg'),
    'WB 462 SEM.jpg': ('weibang-wb-462-sem', 'jpg'),
    'WB 466 SCM.jpg': ('weibang-wb-466-scm', 'jpg'),
    'WB 537 SC3.jpg': ('weibang-wb-537-sc3', 'jpg'),
    'WB 537 SCVAL.jpg': ('weibang-wb-537-scval', 'jpg'),
    'WB 537 SCVALB.jpg': ('weibang-wb-537-scvalb', 'jpg'),
    'WB 537 SCVM.jpg': ('weibang-wb-537-scvm', 'jpg'),
    'WB 778 SCV3.jpg': ('weibang-wb-778-scv3', 'jpg'),
    'WB506SC.jpg': ('weibang-wb-506-sc', 'jpg'),
    'WB506SC3.jpg': ('weibang-wb-506-sc3', 'jpg'),
}

extracted = {}
with zipfile.ZipFile(ZIP, 'r') as z:
    for arcname in z.namelist():
        if arcname.endswith('/'):
            continue
        basename = os.path.basename(arcname)
        if basename not in mapping:
            continue
        slug, fmt = mapping[basename]
        # Estrai sempre in tmp poi processa
        tmp = DEST / f'_tmp_{slug}.{fmt}'
        with z.open(arcname) as src, open(tmp, 'wb') as dst:
            shutil.copyfileobj(src, dst)

        outpath_jpg = DEST / f'{slug}.jpg'
        outpath_webp = DEST / f'{slug}.webp'

        if HAS_PIL:
            try:
                img = Image.open(tmp)
                img = img.convert('RGB') if img.mode != 'RGB' else img
                # Resize se più grande di 1400px sul lato lungo
                w, h = img.size
                m = max(w, h)
                if m > 1400:
                    scale = 1400 / m
                    img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
                # Salva JPG (q=82) e WebP (q=82)
                img.save(outpath_jpg, 'JPEG', quality=82, optimize=True, progressive=True)
                img.save(outpath_webp, 'WEBP', quality=82, method=5)
                tmp.unlink()
                extracted[slug] = (outpath_jpg, outpath_webp, img.size)
                print(f'  [OK]{basename:25s} -> {slug}.jpg + .webp  {img.size}')
            except Exception as e:
                print(f'  [!]PIL fail {basename}: {e}, copio raw')
                shutil.move(tmp, outpath_jpg)
                extracted[slug] = (outpath_jpg, None, None)
        else:
            # Senza PIL: copia raw e basta
            shutil.move(tmp, outpath_jpg)
            extracted[slug] = (outpath_jpg, None, None)

print(f'\n{len(extracted)} foto installate in {DEST.relative_to(ROOT)}')

# === Aggiorna ogni scheda HTML ===
prodotti_dir = ROOT / 'prodotti'
updated_count = 0

for slug, (jpg_path, webp_path, size) in extracted.items():
    html_path = prodotti_dir / f'{slug}.html'
    if not html_path.exists():
        print(f'  [!]HTML mancante: {html_path.name}')
        continue
    with open(html_path, 'r', encoding='utf-8') as f:
        s = f.read()
    orig = s
    rel_img = f'assets/img/prodotti/weibang/{slug}.jpg'
    rel_img_from_prodotti = f'../{rel_img}'  # path relativo da prodotti/
    abs_img_url = f'https://www.motorgardenbazzana.it/{rel_img}'

    # 1. Sostituisci <img src="placeholder..."> nel product__media
    s = re.sub(
        r'<div class="product__media reveal in"><img src="[^"]+" alt="[^"]*"[^/>]*/></div>',
        f'<div class="product__media reveal in"><img src="{rel_img_from_prodotti}" alt="Weibang {slug.replace("weibang-wb-", "WB ").upper()} - foto prodotto" loading="eager" decoding="async" /></div>',
        s, count=1
    )

    # 2. Sostituisci data-img attributo su main.product
    s = re.sub(
        r'(data-img=")assets/img/[^"]+(")',
        rf'\1{rel_img}\2',
        s, count=1
    )

    # 3. Sostituisci og:image
    s = re.sub(
        r'(<meta property="og:image" content=")[^"]+(")',
        rf'\g<1>{abs_img_url}\g<2>',
        s, count=1
    )

    # 4. Sostituisci JSON-LD image
    s = re.sub(
        r'("image":\s*")[^"]+(")',
        rf'\1{abs_img_url}\2',
        s, count=1
    )

    if s != orig:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(s)
        updated_count += 1
        print(f'  [OK]{html_path.name}')
    else:
        print(f'  [SKIP]{html_path.name} (no changes)')

print(f'\nUpdated {updated_count} HTML schede.')
