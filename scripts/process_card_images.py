"""Resize/crop the user-provided photos into small, optimized square
thumbnails for the hero feed-card mockup (object-fit: cover handles the
final aspect per card, so a consistent square source is enough)."""
from PIL import Image, ImageOps
import os

SRC_DIR = r"C:\Users\vyomv\Downloads\images"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "cards")
os.makedirs(OUT_DIR, exist_ok=True)

SIZE = 480  # square output, object-fit:cover crops to each card's shape

jobs = [
    ("makeup.jpg", "skincare.jpg"),
    ("earphones.webp", "earphones.jpg"),
    ("cafe.jpg", "cafe.jpg"),
    ("filter_coffee.jpg", "filter-coffee.jpg"),
]

for src_name, out_name in jobs:
    src_path = os.path.join(SRC_DIR, src_name)
    im = Image.open(src_path)
    im = ImageOps.exif_transpose(im)  # respect camera orientation
    im = im.convert("RGB")
    im = ImageOps.fit(im, (SIZE, SIZE), method=Image.LANCZOS, centering=(0.5, 0.4))
    out_path = os.path.join(OUT_DIR, out_name)
    im.save(out_path, "JPEG", quality=80, optimize=True, progressive=True)
    print(out_name, os.path.getsize(out_path), "bytes")
