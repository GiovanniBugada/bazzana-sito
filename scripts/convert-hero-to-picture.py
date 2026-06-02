"""
Converte le <img> hero e principali in <picture> con <source type="image/webp">
e fallback JPG. Il browser sceglie WebP dal parse HTML, senza attendere JS.
Più veloce del runtime upgrade.
"""
import re, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Target: trasformare img specifiche in <picture> con source webp
# Pattern: <img ... src="path.jpg" alt="..." ...>
# Mantiene tutti gli attributi originali + crea source webp.

def img_to_picture(match):
    full = match.group(0)
    src = match.group('src')
    # Ricostruisci webp src
    if not re.search(r'\.(jpe?g|png)$', src, re.I):
        return full
    webp_src = re.sub(r'\.(jpe?g|png)$', '.webp', src, flags=re.I)
    # Verifica se webp esiste su disco
    # path relativo dal file html — assumiamo path relativi dalla root del sito
    abs_jpg = ROOT / src
    abs_webp = ROOT / webp_src
    # Per percorsi con ../ (subfolder), non possiamo verificare facilmente
    # quindi accettiamo se esiste senza ../ oppure se non possiamo verificare
    if '../' in src:
        # Subfolder: rimuovi ../ per verificare path assoluto
        check_path = src.replace('../', '')
        abs_webp_check = ROOT / re.sub(r'\.(jpe?g|png)$', '.webp', check_path, flags=re.I)
        if not abs_webp_check.exists():
            return full
    else:
        if not abs_webp.exists():
            return full
    # Build picture
    return f'<picture><source type="image/webp" srcset="{webp_src}">{full}</picture>'

# Applichiamo solo a img hero / immagini grandi (>500 KB JPG)
HERO_IMG_PATTERNS = [
    # Hero homepage / pagine
    re.compile(r'<img(?P<attrs>[^>]*?)src="(?P<src>[^"]*hero/[^"]+\.(?:jpe?g|png))"(?P<rest>[^>]*?)/?>', re.I),
    # Bazzana scena/storia
    re.compile(r'<img(?P<attrs>[^>]*?)src="(?P<src>[^"]*bazzana/scena[^"]+\.(?:jpe?g|png))"(?P<rest>[^>]*?)/?>', re.I),
    re.compile(r'<img(?P<attrs>[^>]*?)src="(?P<src>[^"]*ambiente/[^"]+\.(?:jpe?g|png))"(?P<rest>[^>]*?)/?>', re.I),
    re.compile(r'<img(?P<attrs>[^>]*?)src="(?P<src>[^"]*officina/[^"]+\.(?:jpe?g|png))"(?P<rest>[^>]*?)/?>', re.I),
    re.compile(r'<img(?P<attrs>[^>]*?)src="(?P<src>[^"]*storia/[^"]+\.(?:jpe?g|png))"(?P<rest>[^>]*?)/?>', re.I),
    # Schede prodotto hero (foto reali)
    re.compile(r'<img(?P<attrs>[^>]*?)src="(?P<src>[^"]*prodotti/(?:weibang|active|honda|rasaerba|cippatore|microcar|generatore|tagliasiepi|motozappa|motosega|soffiatore|decespugliatore)[^"]+\.(?:jpe?g|png))"(?P<rest>[^>]*?)/?>', re.I),
    # Articolo blog hero
    re.compile(r'<img(?P<attrs>[^>]*?)src="(?P<src>[^"]*img/note/[^"]+\.(?:jpe?g|png))"(?P<rest>[^>]*?)/?>', re.I),
]

files = list(ROOT.glob('*.html')) + list((ROOT / 'prodotti').glob('*.html')) + list((ROOT / 'note').glob('*.html'))
total = 0

# Counter container per workaround nonlocal
class Counter:
    def __init__(self): self.n = 0

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        s = f.read()
    orig = s
    cnt = Counter()
    s_ref = [s]  # mutable ref so closure may read latest
    for pat in HERO_IMG_PATTERNS:
        def replace_if_not_in_picture(m):
            full = m.group(0)
            start = m.start()
            context = s_ref[0][max(0, start - 200):start]
            if '<picture' in context and '</picture>' not in context[context.rfind('<picture'):]:
                return full
            cnt.n += 1
            src = m.group('src')
            webp_src = re.sub(r'\.(jpe?g|png)$', '.webp', src, flags=re.I)
            return f'<picture><source type="image/webp" srcset="{webp_src}">{full}</picture>'
        s = pat.sub(replace_if_not_in_picture, s)
        s_ref[0] = s
    if s != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(s)
        total += cnt.n
        print(f'  [OK] {fp.relative_to(ROOT)}: {cnt.n} img -> picture')

print(f'\nTotale: {total} img convertite in <picture>')
