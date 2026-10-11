"""Generate store/promo/marquee.png (1400x560) from the icon and screenshots.

Run from the repo root:  python store/promo/make_marquee.py
Requires Pillow and the Segoe UI fonts that ship with Windows.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FONTS = Path('C:/Windows/Fonts')
W, H = 1400, 560

BLUE = (0, 104, 239)
INK = (22, 27, 34)
MUTED = (87, 96, 106)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def gradient(size, top, bottom):
    img = Image.new('RGB', size)
    d = ImageDraw.Draw(img)
    for y in range(size[1]):
        t = y / (size[1] - 1)
        d.line([(0, y), (size[0], y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    return img


def pill(draw, xy, text, fnt, fill, color, pad_x, height, radius):
    tb = fnt.getbbox(text)
    w = tb[2] - tb[0] + 2 * pad_x
    x, y = xy
    draw.rounded_rectangle((x, y, x + w, y + height), radius=radius, fill=fill)
    draw.text((x + pad_x - tb[0], y + (height - (tb[3] - tb[1])) / 2 - tb[1]), text, font=fnt, fill=color)
    return w


def card(shot, width, label, label_fill, label_color):
    """A browser-like card: title bar with a label, then the screenshot."""
    bar = 40
    shot = shot.resize((width, round(shot.height * width / shot.width)), Image.LANCZOS)
    c = Image.new('RGB', (width, bar + shot.height), 'white')
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, width, bar), fill=(242, 244, 247))
    d.line((0, bar - 1, width, bar - 1), fill=(222, 226, 231))
    for i, col in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse((16 + i * 20, 14, 28 + i * 20, 26), fill=col)
    d.text((86, 9), 'demo.md', font=font('segoeui.ttf', 16), fill=MUTED)
    lf = font('seguisb.ttf', 14)
    lw = lf.getbbox(label)[2] + 24
    pill(d, (width - lw - 12, 8), label, lf, label_fill, label_color, 12, 24, 12)
    c.paste(shot, (0, bar))
    return c


def place(canvas, img, xy, radius=14):
    """Paste with rounded corners and a soft drop shadow."""
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=radius, fill=255)
    shadow = Image.new('L', canvas.size, 0)
    x, y = xy
    ImageDraw.Draw(shadow).rounded_rectangle((x, y + 10, x + img.width, y + img.height + 10), radius=radius, fill=70)
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.paste((40, 60, 110), (0, 0), shadow)
    border = Image.new('RGB', (img.width + 2, img.height + 2), (214, 222, 235))
    bmask = Image.new('L', border.size, 0)
    ImageDraw.Draw(bmask).rounded_rectangle((0, 0, border.width - 1, border.height - 1), radius=radius + 1, fill=255)
    canvas.paste(border, (x - 1, y - 1), bmask)
    canvas.paste(img, xy, mask)


canvas = gradient((W, H), (255, 255, 255), (226, 236, 255))
draw = ImageDraw.Draw(canvas)

# Right: raw Markdown behind, rendered preview in front.
src = Image.open(ROOT / 'store/screenshots/03-full-page-source.png').crop((15, 215, 700, 640))
pre = Image.open(ROOT / 'store/screenshots/04-full-page-preview.png').crop((225, 250, 830, 715))
back = card(src, 450, 'Source', (229, 231, 235), MUTED)
front = card(pre, 470, 'Preview', BLUE, 'white')
place(canvas, back, (690, 44))
place(canvas, front, (W - 470 - 50, H - front.height - 34))

# Left: icon, title, tagline and the Preview button.
icon = Image.open(ROOT / 'icons/icon.png').convert('RGBA')
icon = icon.crop(icon.getchannel('A').getbbox())
icon = icon.resize((round(icon.width * 100 / icon.height), 100), Image.LANCZOS)

x = 80
title = font('segoeuib.ttf', 54)
sub = font('seguisb.ttf', 30)
body = font('segoeui.ttf', 23)
items = [
    ('icon', None, None, 100, 26),
    ('Markdown Previewer', title, INK, None, 16),
    ('for Dropbox', sub, MUTED, None, 22),
    ('Read .md files fully formatted —', body, MUTED, None, 4),
    ('right inside the Dropbox web viewer.', body, MUTED, None, 30),
    ('button', None, None, 50, 0),
]
heights = [h if h else f.getbbox(t)[3] - f.getbbox(t)[1] for t, f, _, h, _ in items]
y = (H - sum(heights) - sum(i[4] for i in items)) // 2
for (text, fnt, color, _, gap), h in zip(items, heights):
    if text == 'icon':
        canvas.paste(icon, (x, y), icon)
    elif text == 'button':
        pill(draw, (x, y), 'Preview', font('seguisb.ttf', 22), BLUE, 'white', 30, 50, 10)
    else:
        draw.text((x, y - fnt.getbbox(text)[1]), text, font=fnt, fill=color)
    y += h + gap

out = ROOT / 'store/promo/marquee.png'
canvas.convert('RGB').save(out, optimize=True)  # 24-bit PNG, no alpha
print(f'Saved {out.relative_to(ROOT)} ({W}x{H})')
