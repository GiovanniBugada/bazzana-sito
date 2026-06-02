"""
Audit: per ogni scheda prodotto detail, elenca brand/modello/categoria + foto.
Permette di verificare a colpo d'occhio se la foto corrisponde al prodotto.
"""
import re, glob, os

files = sorted(glob.glob('prodotti/*.html'))
print('=== AUDIT FOTO vs PRODOTTI ===\n')
for fp in files:
    if 'dettaglio' in fp:
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        s = f.read()
    name = os.path.basename(fp).replace('.html', '')
    img_m = re.search(r'data-img="([^"]+)"', s)
    brand_m = re.search(r'data-brand="([^"]+)"', s)
    model_m = re.search(r'data-model="([^"]+)"', s)
    cat_m = re.search(r'data-category="([^"]+)"', s)
    img = img_m.group(1) if img_m else '-'
    brand = brand_m.group(1) if brand_m else '-'
    model = model_m.group(1) if model_m else '-'
    cat = cat_m.group(1) if cat_m else '-'
    img_short = img.split('/')[-1]
    # Esiste file?
    exists = os.path.exists(img) if not img.startswith('http') else '(remote)'
    flag = ''
    if 'placeholder' in img.lower():
        flag = ' [PLACEHOLDER]'
    elif 'foto-arrivo' in img.lower():
        flag = ' [FOTO IN ARRIVO]'
    print(f'{name}')
    print(f'  brand={brand} model={model} cat={cat}')
    print(f'  img={img_short}{flag} exists={exists}')
    print()
