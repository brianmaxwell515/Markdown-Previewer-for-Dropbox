"""Generate store/promo/small-tile.png (440x280) from icons/icon.png.

Run from the repo root:  python store/promo/make_small_tile.py
Requires Pillow and the Segoe UI fonts that ship with Windows.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FONTS = Path('C:/Windows/Fonts')
S = 2  # draw at 2x, then downscale for crisp edges
W, H = 440 * S, 280 * S

BLUE = (0, 104, 239)
INK = (22, 27, 34)
MUTED = (87, 96, 106)

# Background: soft vertical gradient from white to light blue.
tile = Image.new('RGB', (W, H))
top, bottom = (255, 255, 255), (228, 238, 255)
draw = ImageDraw.Draw(tile)
for y in range(H):
    t = y / (H - 1)
    draw.line([(0, y), (W, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))

# Icon: crop to its visible artwork and place it on the left.
icon = Image.open(ROOT / 'icons/icon.png').convert('RGBA')
icon = icon.crop(icon.getchannel('A').getbbox())
icon_h = 190 * S
icon = icon.resize((round(icon.width * icon_h / icon.height), icon_h), Image.LANCZOS)
icon_x = 36 * S
tile.paste(icon, (icon_x, (H - icon_h) // 2), icon)

# Text block on the right.
bold = ImageFont.truetype(str(FONTS / 'segoeuib.ttf'), 36 * S)
semi = ImageFont.truetype(str(FONTS / 'seguisb.ttf'), 21 * S)
btn_font = ImageFont.truetype(str(FONTS / 'seguisb.ttf'), 15 * S)

x = icon_x + icon.width + 30 * S
lines = [('Markdown', bold, INK), ('Previewer', bold, INK), ('for Dropbox', semi, MUTED)]
gaps = [2 * S, 10 * S, 0]
heights = [d.getbbox(t)[3] - d.getbbox(t)[1] for t, d, _ in lines]

# Badge under the title.
btn_text = 'Free & open source'
tb = btn_font.getbbox(btn_text)
btn_w, btn_h = tb[2] - tb[0] + 28 * S, 34 * S
btn_gap = 18 * S

block_h = sum(heights) + sum(gaps) + btn_gap + btn_h
y = (H - block_h) // 2
for (text, font, color), h, gap in zip(lines, heights, gaps):
    draw.text((x, y - font.getbbox(text)[1]), text, font=font, fill=color)
    y += h + gap

y += btn_gap
draw.rounded_rectangle((x, y, x + btn_w, y + btn_h), radius=btn_h // 2, fill=BLUE)
draw.text(
    (x + (btn_w - (tb[2] - tb[0])) / 2 - tb[0], y + (btn_h - (tb[3] - tb[1])) / 2 - tb[1]),
    btn_text, font=btn_font, fill='white',
)

out = ROOT / 'store/promo/small-tile.png'
tile.resize((440, 280), Image.LANCZOS).save(out, optimize=True)
print(f'Saved {out.relative_to(ROOT)} (440x280)')
