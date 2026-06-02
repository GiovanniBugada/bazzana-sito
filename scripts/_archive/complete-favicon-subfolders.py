"""Aggiunge il set completo di favicon ai subfolder HTML (prodotti/, note/)
che ora hanno solo favicon.svg."""
import re, glob

files = list(glob.glob('prodotti/*.html')) + list(glob.glob('note/*.html'))
count = 0

ICONS_BLOCK = (
    '<link rel="icon" href="../favicon.ico?v=2" sizes="any" />\n'
    '<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon/favicon-32x32.png?v=2" />\n'
    '<link rel="icon" type="image/png" sizes="16x16" href="../assets/favicon/favicon-16x16.png?v=2" />\n'
    '<link rel="apple-touch-icon" sizes="180x180" href="../assets/favicon/apple-touch-icon.png?v=2" />\n'
)

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        s = f.read()
    orig = s
    # Trova il link favicon.svg esistente
    m = re.search(r'(<link rel="icon" type="image/svg\+xml"[^>]*?/>)', s)
    if m and 'favicon.ico' not in s:
        # Inserisci block subito PRIMA del favicon.svg
        s = s[:m.start()] + ICONS_BLOCK + s[m.start():]
    if s != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(s)
        count += 1

print(f'Subfolder HTML aggiornati con favicon set: {count}')
