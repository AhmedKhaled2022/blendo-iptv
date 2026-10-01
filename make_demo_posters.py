# صور غلاف للأفلام المفتوحة في القائمة التجريبية (review-demo.m3u) — من لقطات الأفلام نفسها.
# Big Buck Bunny و Tears of Steel: (c) Blender Foundation، رخصة CC BY 3.0 — النسبة مكتوبة على الغلاف.
# التشغيل: python store/site/make_demo_posters.py <مجلد اللقطات>
import os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', '..', 'assets', 'google_fonts')
FRAMES = sys.argv[1]
W, H = 600, 900

POSTERS = [
    # (ملف اللقطة، صندوق القص (x0, y0, x1, y1)، العنوان، الاسم الناتج)
    ('bbb_000230.png', (620, 0, 1340, 1080), 'Big Buck Bunny', 'bbb.jpg'),
    ('tos_000630.png', (817, 50, 1284, 750), 'Tears of Steel', 'tos.jpg'),
]

title_font = ImageFont.truetype(os.path.join(FONTS, 'Changa-Bold.ttf'), 64)
credit_font = ImageFont.truetype(os.path.join(FONTS, 'Tajawal-Medium.ttf'), 26)
os.makedirs(os.path.join(HERE, 'demo'), exist_ok=True)

for frame, box, title, out in POSTERS:
    im = Image.open(os.path.join(FRAMES, frame)).convert('RGB').crop(box).resize((W, H), Image.LANCZOS)
    # تدرّج غامق تحت عشان العنوان يتقري
    shade = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(shade)
    for y in range(H // 2, H):
        d.line([(0, y), (W, y)], fill=int(235 * ((y - H / 2) / (H / 2)) ** 1.6))
    im = Image.composite(Image.new('RGB', (W, H), (8, 4, 24)), im, shade)
    d = ImageDraw.Draw(im)
    tw = d.textlength(title, font=title_font)
    d.text(((W - tw) / 2, H - 175), title, font=title_font, fill=(255, 255, 255))
    credit = 'Blender Foundation · CC BY 3.0'
    cw = d.textlength(credit, font=credit_font)
    d.text(((W - cw) / 2, H - 82), credit, font=credit_font, fill=(205, 196, 230))
    path = os.path.join(HERE, 'demo', out)
    im.save(path, 'JPEG', quality=86, optimize=True, progressive=True)
    print(out, os.path.getsize(path) // 1024, 'KB')
