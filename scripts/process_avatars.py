"""Crop/resize the user-provided headshots into small square avatars
for the feed-card creator byline (displayed at ~13-20px, so a 96x96
source gives plenty of headroom for retina without bloating the repo)."""
from PIL import Image, ImageOps
import os

SRC_DIR = r"C:\Users\vyomv\Downloads\images"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "avatars")
os.makedirs(OUT_DIR, exist_ok=True)

SIZE = 96

jobs = [
    ("priya.jpg", "priya.jpg", (0.5, 0.32)),
    ("rahul.avif", "rahul.jpg", (0.5, 0.26)),
]

for src_name, out_name, centering in jobs:
    src_path = os.path.join(SRC_DIR, src_name)
    im = Image.open(src_path)
    im = ImageOps.exif_transpose(im)
    im = im.convert("RGB")
    im = ImageOps.fit(im, (SIZE, SIZE), method=Image.LANCZOS, centering=centering)
    out_path = os.path.join(OUT_DIR, out_name)
    im.save(out_path, "JPEG", quality=82, optimize=True, progressive=True)
    print(out_name, os.path.getsize(out_path), "bytes")
