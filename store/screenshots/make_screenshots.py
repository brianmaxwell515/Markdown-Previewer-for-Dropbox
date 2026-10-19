"""Generate the Chrome Web Store screenshots (1280x800) in store/screenshots/.

Run from the repo root:  python store/screenshots/make_screenshots.py
Requires Pillow, NumPy and the Segoe UI fonts that ship with Windows.

Inputs live in store/screenshots/raw/:
- quickview-*.png / full-page-*.png: Dropbox captured at a 1440x900 viewport
  @2x, with Dropbox's own Markdown view (-dropbox) and with the extension
  (-extension)
- render-light.png / render-dark.png: demo.md rendered by the extension's
  renderer at 2x, in light and dark mode
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / 'store/screenshots/raw'
OUT = ROOT / 'store/screenshots'
FONTS = Path('C:/Windows/Fonts')
W, H = 1280, 800

BLUE = (0, 104, 239)
MUTED = (87, 96, 106)

# Layout of the captures, in CSS pixels (captures are 2x).
QUICKVIEW_PANEL = (865, 0, 1440, 900)
VIEW_TOGGLE = (1125, 88, 161, 32)  # Dropbox's plain-text / Markdown view toggle in quick view


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def capture(name, box=None):
    img = Image.open(RAW / f'{name}.png').convert('RGB')
    return img.crop(tuple(v * 2 for v in box)) if box else img


def background():
    """Diagonal blue gradient with two soft light blobs."""
    x = np.linspace(0, 1, W)[None, :]
    y = np.linspace(0, 1, H)[:, None]
    t = np.clip(0.55 * x + 0.45 * y, 0, 1)[..., None]
    a, b = np.array([0, 72, 196]), np.array([64, 150, 255])
    img = Image.fromarray((a + (b - a) * t).astype(np.uint8))
    glow = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(glow)
    d.ellipse((-200, 380, 420, 1000), fill=60)
    d.ellipse((900, -260, 1500, 340), fill=50)
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    img.paste((255, 255, 255), (0, 0), glow)
    return img


def heading(img, title, subtitle):
    d = ImageDraw.Draw(img)
    for text, fnt, y, fill in [
        (title, font('segoeuib.ttf', 44), 48, 'white'),
        (subtitle, font('segoeui.ttf', 22), 116, (225, 236, 255)),
    ]:
        w = d.textlength(text, font=fnt)
        d.text(((W - w) / 2, y), text, font=fnt, fill=fill)


def rounded_mask(size, radius, bottom=True, right=True):
    m = Image.new('L', size, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    # square corners on edges that run off the canvas
    if not bottom:
        d.rectangle((0, size[1] - radius, size[0], size[1]), fill=255)
    if not right:
        d.rectangle((size[0] - radius, 0, size[0], size[1]), fill=255)
    return m


def place(canvas, img, xy, radius=14, bottom=True, right=True, shadow=90):
    x, y = xy
    sh = Image.new('L', canvas.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((x, y + 14, x + img.width, y + img.height + 14), radius=radius, fill=shadow)
    canvas.paste((0, 30, 90), (0, 0), sh.filter(ImageFilter.GaussianBlur(22)))
    canvas.paste(img, (x, y), rounded_mask(img.size, radius, bottom, right))


def fit(img, width):
    return img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)


def pill(d, xy, text, fnt, fill, color, pad_x, height):
    tb = fnt.getbbox(text)
    w = tb[2] - tb[0] + 2 * pad_x
    x, y = xy
    d.rounded_rectangle((x, y, x + w, y + height), radius=height // 2, fill=fill)
    d.text((x + pad_x - tb[0], y + (height - (tb[3] - tb[1])) / 2 - tb[1]), text, font=fnt, fill=color)
    return w


def window(content, width, label=None, label_style='blue'):
    """A simple browser-like card: title bar with dots, file name and an optional label."""
    bar = 42
    content = fit(content, width)
    c = Image.new('RGB', (width, bar + content.height), 'white')
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, width, bar), fill=(241, 243, 246))
    d.line((0, bar - 1, width, bar - 1), fill=(220, 224, 230))
    for i, col in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse((16 + i * 20, 15, 28 + i * 20, 27), fill=col)
    d.text((88, 10), 'demo.md', font=font('segoeui.ttf', 16), fill=MUTED)
    if label:
        lf = font('seguisb.ttf', 14)
        lw = d.textlength(label, font=lf) + 26
        fill, color = (BLUE, 'white') if label_style == 'blue' else ((226, 229, 234), MUTED)
        pill(d, (width - lw - 12, 9), label, lf, fill, color, 13, 24)
    c.paste(content, (0, bar))
    return c


def cut_at_blank(img, top, bottom):
    """Crop rows top..bottom, moving the bottom edge up to the nearest blank row."""
    a = np.asarray(img.convert('L'), dtype=np.int16)
    for y in range(bottom, top + 1, -1):
        row = a[y - 1]
        if row.max() - row.min() < 6:
            return img.crop((0, top, img.width, y))
    return img.crop((0, top, img.width, bottom))


def save(img, name):
    img.convert('RGB').save(OUT / name, optimize=True)
    print('Saved', (OUT / name).relative_to(ROOT))


label_font = font('seguisb.ttf', 17)

# 1. Dropbox's Markdown view vs. the extension, same quick-view panel
img = background()
heading(img, "Dropbox's Markdown view, upgraded",
        'Same file, same viewer, with clean GitHub-style formatting.')
before = fit(capture('quickview-dropbox', QUICKVIEW_PANEL), 540)
after = fit(capture('quickview-extension', QUICKVIEW_PANEL), 540)
place(img, before, (70, 230), bottom=False)
place(img, after, (670, 230), bottom=False)
d = ImageDraw.Draw(img)
pill(d, (70, 186), 'Dropbox', label_font, (226, 229, 234), MUTED, 16, 32)
pill(d, (670, 186), 'With Markdown Previewer', label_font, 'white', BLUE, 16, 32)
cx, cy = 640, 470
d.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), fill='white')
d.polygon([(cx - 14, cy - 16), (cx + 18, cy), (cx - 14, cy + 16)], fill=BLUE)
save(img, '01-before-after.png')

# 2. Nothing extra to click; Dropbox's own toggle shows the source
img = background()
heading(img, 'Nothing extra to click',
        "Markdown files open fully formatted. Dropbox's view toggle still shows the source.")
shot = capture('quickview-extension')
scale = 1040 / (shot.width / 2)  # display px per CSS px
place(img, fit(shot, 1040), (120, 186), bottom=False)
# magnifier over Dropbox's view toggle
tx, ty, tw, th = VIEW_TOGGLE
cx, cy = tx + tw / 2, ty + th / 2
r, half = 120, 90  # lens radius (display px), half-size of the sampled area (CSS px)
# only the toolbar row around the toggle, magnified on a white lens
strip = capture('quickview-extension', (round(cx - half), round(cy - th / 2 - 4), round(cx + half), round(cy + th / 2 + 4)))
strip = fit(strip, 2 * r)
lens = Image.new('RGB', (2 * r, 2 * r), 'white')
lens.paste(strip, (0, r - strip.height // 2))
mask = Image.new('L', lens.size, 0)
ImageDraw.Draw(mask).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
lx, ly = round(120 + cx * scale - r), round(186 + cy * scale - r + 70)
sh = Image.new('L', img.size, 0)
ImageDraw.Draw(sh).ellipse((lx - 6, ly + 6, lx + 2 * r + 6, ly + 2 * r + 18), fill=110)
img.paste((0, 30, 90), (0, 0), sh.filter(ImageFilter.GaussianBlur(16)))
d = ImageDraw.Draw(img)
d.ellipse((lx - 7, ly - 7, lx + 2 * r + 7, ly + 2 * r + 7), fill='white', outline=BLUE, width=3)
img.paste(lens, (lx, ly), mask)
cap_w = d.textlength('Switch views anytime', font=label_font) + 32
pill(d, (round(lx + r - cap_w / 2), ly + 2 * r + 18), 'Switch views anytime', label_font, BLUE, 'white', 16, 34)
save(img, '02-nothing-to-click.png')

# 3. Quick view and full page
img = background()
heading(img, 'Works in quick view and full-page preview',
        'Preview from the file list side panel, or open the file full screen.')
full = fit(capture('full-page-extension'), 1040)
place(img, full, (330, 216), bottom=False, right=False)
panel = fit(capture('quickview-extension', QUICKVIEW_PANEL), 340)
place(img, panel, (60, H - panel.height + 60), bottom=False)
d = ImageDraw.Draw(img)
pill(d, (60, H - panel.height + 18), 'Quick view', label_font, 'white', BLUE, 16, 32)
pill(d, (330, 172), 'Full page', label_font, 'white', BLUE, 16, 32)
save(img, '03-quick-view-and-full-page.png')

# 4. Formatting and dark mode
render_light = Image.open(RAW / 'render-light.png').convert('RGB')
render_dark = Image.open(RAW / 'render-dark.png').convert('RGB')
img = background()
heading(img, 'Tables, task lists and highlighted code',
        "GitHub-style formatting that follows Dropbox's light or dark theme.")
light = window(cut_at_blank(render_light.crop((0, 0, 1360, 2338)), 0, 1040), 620, 'Light')
dark = window(cut_at_blank(render_dark.crop((0, 0, 1360, 2338)), 1100, 2000), 620, 'Dark', 'grey')
place(img, light, (70, 190))
place(img, dark, (590, 292))
save(img, '04-formatting-dark-mode.png')
