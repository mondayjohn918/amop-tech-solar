"""Web-ready photos (webp, two widths) from the Google listing originals, plus og.jpg."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "originals", ROOT / "img"
OUT.mkdir(exist_ok=True)

# name: (source, crop as fractions or None)
JOBS = {
    "roof-wide": ("g01.jpg", None),
    "after": ("g02.jpg", (0, .05, 1, .75)),
    "wall": ("g04.jpg", None),
    "inverters": ("g05.jpg", None),
    "ladder": ("g06.jpg", None),
    "tech": ("g07.jpg", None),
    "frame": ("g08.jpg", None),
    "cctv": ("g09.jpg", (0, .1, 1, .85)),
    "roof-close": ("g10.jpg", None),
    "bungalow": ("g11.jpg", (0, 0, 1, .9)),
    "before": ("geo.jpg", (0, .05, 1, .75)),
}

def prep(src, crop):
    im = Image.open(SRC / src).convert("RGB")
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0]*w), int(crop[1]*h), int(crop[2]*w), int(crop[3]*h)))
    return ImageEnhance.Contrast(im).enhance(1.05)

for name, (src, crop) in JOBS.items():
    im = prep(src, crop)
    for w in (640, 1200):
        if w > im.width * 1.05 and w != 640:
            continue
        r = im.copy(); r.thumbnail((w, w * 2))
        r = r.filter(ImageFilter.UnsharpMask(radius=1, percent=40, threshold=2))
        r.save(OUT / f"{name}-{w}.webp", quality=78, method=6)
    print(name, im.size)

# og.jpg 1200x630: paper background, mark, headline, technician photo
W, H = 1200, 630
og = Image.new("RGB", (W, H), "#EEF1EA")
d = ImageDraw.Draw(og)
from PIL import ImageOps
photo = ImageOps.fit(prep("g07.jpg", None), (470, 630), centering=(0.5, 0.35))
og.paste(photo, (W - photo.width, 0))
F = "C:/Windows/Fonts/"
big = ImageFont.truetype(F + "seguibl.ttf", 66)
mid = ImageFont.truetype(F + "segoeui.ttf", 28)
sb = ImageFont.truetype(F + "seguisb.ttf", 28)
# mark: sun over earth bars
d.ellipse((64, 52, 104, 92), fill="#F2B01E")
for i, (x, w) in enumerate([(56, 56), (66, 36), (76, 16)]):
    d.rectangle((x, 104 + i * 12, x + w, 110 + i * 12), fill="#13221E")
d.text((132, 70), "AMO-P TECH SOLAR", font=sb, fill="#13221E")
d.multiline_text((64, 190), "Let your\ngenerator rest.", font=big, fill="#13221E", spacing=6)
d.text((64, 370), "Solar, hybrid inverters, lithium batteries\nand proper earthing in Benin City.", font=mid, fill="#33433E", spacing=6)
d.rounded_rectangle((64, 480, 452, 540), radius=30, fill="#F2B01E")
d.text((92, 492), "WhatsApp 0908 285 9581", font=sb, fill="#13221E")
og.save(ROOT / "og.jpg", quality=84, optimize=True)
print("og", (ROOT / "og.jpg").stat().st_size // 1024, "KB")
