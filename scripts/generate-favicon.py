"""
Genera favicon completo dal logo Bazzana square:
- favicon.ico (multi-size 16/32/48) nella root
- favicon-16x16.png, favicon-32x32.png in assets/favicon/
- apple-touch-icon.png (180x180)
- favicon-192.png (PWA)
- favicon-512.png (PWA)
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'assets' / 'brand' / 'logo-bazzana-square.png'
FAV_DIR = ROOT / 'assets' / 'favicon'

# Apri logo + auto-rotate
src = Image.open(SRC)
src = ImageOps.exif_transpose(src)
if src.mode != 'RGBA':
    src = src.convert('RGBA')

# Crop quadrato centrato (il logo PNG è già quadrato 512x512 con padding)
w, h = src.size
side = min(w, h)
left = (w - side) // 2
top = (h - side) // 2
src = src.crop((left, top, left + side, top + side))

# Su tab Chrome dark/light bisogna che il favicon sia leggibile su entrambi.
# Il logo Bazzana ha già transparency. Per favicon piccoli (16x16) è poco leggibile
# perché c'è troppa scritta. Uso il monogramma BAZZANA cropped + bordo.
# Per le size piccole NON facciamo full logo ma uno crop dell'esagono "BAZZANA".

def make_icon(size, add_padding=True):
    """Resize logo to size with optional padding around."""
    # Calcola dimensione contenuto interno
    if add_padding:
        # 88% del frame: lascia 6% di padding per ogni lato
        inner = int(size * 0.94)
    else:
        inner = size
    img = src.resize((inner, inner), Image.LANCZOS)
    if inner == size:
        return img
    # Crea frame size con sfondo trasparente
    frame = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    pad = (size - inner) // 2
    frame.paste(img, (pad, pad), img)
    return frame

# Genera PNG di varie size
sizes_pngs = {
    16: FAV_DIR / 'favicon-16x16.png',
    32: FAV_DIR / 'favicon-32x32.png',
    48: FAV_DIR / 'favicon-48x48.png',
    180: FAV_DIR / 'apple-touch-icon.png',
    192: FAV_DIR / 'favicon-192.png',
    512: FAV_DIR / 'favicon-512.png',
}
for size, outp in sizes_pngs.items():
    img = make_icon(size, add_padding=(size >= 32))
    img.save(outp, 'PNG', optimize=True)
    print(f'  [OK] {outp.name} {img.size} ({outp.stat().st_size//1024} KB)')

# Genera favicon.ico multi-size (16/32/48) nella ROOT del sito
ico_path = ROOT / 'favicon.ico'
icons = [make_icon(s, add_padding=(s >= 32)) for s in (16, 32, 48)]
icons[0].save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
print(f'  [OK] {ico_path.name} (root, multi-size) ({ico_path.stat().st_size//1024} KB)')

# Genera nuovo favicon.svg dal PNG embeddato — più sicuro che riscrivere SVG da zero
# Su tab scuri viene reso comunque bene grazie alla trasparenza del logo originale.
# Lasciamo l'esistente solo se è già il logo Bazzana. Verifichiamo.
svg_path = FAV_DIR / 'favicon.svg'
with open(svg_path, 'r', encoding='utf-8') as f:
    svg_content = f.read()
if 'fill="#000000"' in svg_content and len(svg_content) < 800:
    # Il vecchio SVG è solo "B" su sfondo nero — sostituiamo con SVG che embedded il PNG
    # Generiamo SVG che inline il PNG 192 come base64
    import base64
    png_data = (FAV_DIR / 'favicon-192.png').read_bytes()
    b64 = base64.b64encode(png_data).decode()
    new_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192" role="img" aria-label="Motor Garden Bazzana">
  <image href="data:image/png;base64,{b64}" width="192" height="192"/>
</svg>'''
    svg_path.write_text(new_svg, encoding='utf-8')
    print(f'  [OK] favicon.svg sostituito (embedded PNG)')

print('\nFatto. Tutto in:', FAV_DIR.relative_to(ROOT))
