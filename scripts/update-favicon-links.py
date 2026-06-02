import re, glob, os

files = list(glob.glob('*.html')) + list(glob.glob('prodotti/*.html')) + list(glob.glob('note/*.html'))
count_fav = 0
count_v = 0

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        s = f.read()
    orig = s
    # Determina prefix: root o subfolder
    norm = fp.replace('\\', '/')
    is_sub = '/' in norm
    prefix = '../' if is_sub else ''

    # 1. Aggiungi fallback favicon.ico nella root del sito se manca
    if 'favicon.ico' not in s:
        m = re.search(r'(<link rel="icon"[^>]*sizes="32x32"[^>]*/>)', s)
        if m:
            ico_tag = '<link rel="icon" href="' + prefix + 'favicon.ico?v=2" sizes="any" />'
            s = s[:m.start()] + ico_tag + '\n' + s[m.start():]
            count_fav += 1

    # 2. Bumpa versione cache su favicon
    s = re.sub(r'(favicon[a-zA-Z0-9\-]*\.png)(?:\?v=\d+)?(")', r'\1?v=2\2', s)
    s = re.sub(r'(favicon\.svg)(?:\?v=\d+)?(")', r'\1?v=2\2', s)
    s = re.sub(r'(apple-touch-icon\.png)(?:\?v=\d+)?(")', r'\1?v=2\2', s)

    if s != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(s)
        count_v += 1

print('Fallback favicon.ico aggiunto in', count_fav, 'file')
print('Cache bumped in', count_v, 'file')
