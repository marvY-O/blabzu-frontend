"""Generate assets/og-image.png (1200x630) for social sharing previews."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1200, 630

# ---- Colors (match site brand tokens) ----
BG_TOP = (253, 251, 249)      # --bg
GLOW = (255, 232, 225)        # --primary-light
TEXT = (26, 21, 18)           # --text
MUTED = (107, 98, 92)         # --text-muted
PRIMARY = (255, 90, 60)       # --primary
DOT = (255, 182, 72)
SPARK_BIG = (247, 212, 136)
SPARK_SMALL = (232, 84, 46)

img = Image.new("RGB", (W, H), BG_TOP)
draw = ImageDraw.Draw(img, "RGBA")

# Radial-ish glow in the top-right using concentric circles
cx, cy = W - 120, 60
max_r = 650
steps = 80
for i in range(steps, 0, -1):
    r = int(max_r * i / steps)
    alpha = int(70 * (1 - i / steps) ** 1.6)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GLOW + (alpha,))

# ---- Fonts ----
import os
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
f_word = ImageFont.truetype(os.path.join(FONT_DIR, "poppins-extrabold.ttf"), 110)
f_tag = ImageFont.truetype(os.path.join(FONT_DIR, "poppins-medium.ttf"), 34)
f_head = ImageFont.truetype(os.path.join(FONT_DIR, "poppins-extrabold.ttf"), 54)
f_sub = ImageFont.truetype(os.path.join(FONT_DIR, "poppins-medium.ttf"), 26)

margin = 90
y = 100

# ---- Wordmark "blabzu" with colored z ----
x = margin
parts = [("blab", TEXT), ("z", PRIMARY), ("u", TEXT)]
for text, color in parts:
    draw.text((x, y), text, font=f_word, fill=color)
    w = draw.textlength(text, font=f_word)
    x += w

word_end_x = x
word_bbox = draw.textbbox((margin, y), "blabzu", font=f_word)

# Decorative dot + sparkles near top-right of wordmark
def sparkle(draw, cx, cy, size, fill, rotation=0):
    pts = []
    n = 4
    for i in range(n * 2):
        angle = math.pi / n * i + rotation
        r = size if i % 2 == 0 else size * 0.32
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=fill)

draw.ellipse([word_end_x - 230, y - 46, word_end_x - 230 + 26, y - 46 + 26], fill=DOT)
sparkle(draw, word_end_x - 110, y - 10, 30, SPARK_BIG, rotation=0.4)
sparkle(draw, word_end_x - 40, y + 55, 18, SPARK_SMALL, rotation=-0.3)

# ---- Tagline ----
tag_y = word_bbox[3] + 18
draw.text((margin, tag_y), "No filter. Just finds.", font=f_tag, fill=MUTED)

# ---- Headline ----
head_y = tag_y + 90
line1 = "India's place to decide,"
line2 = "not just scroll."

# line1 with colored "decide"
hx = margin
pre, word, post = "India's place to ", "decide", ","
draw.text((hx, head_y), pre, font=f_head, fill=TEXT)
hx += draw.textlength(pre, font=f_head)
draw.text((hx, head_y), word, font=f_head, fill=PRIMARY)
hx += draw.textlength(word, font=f_head)
draw.text((hx, head_y), post, font=f_head, fill=TEXT)

draw.text((margin, head_y + 70), line2, font=f_head, fill=TEXT)

# ---- Subheading ----
sub_y = head_y + 160
draw.text((margin, sub_y),
          "Real, save-worthy recommendations from real people, in your language.",
          font=f_sub, fill=MUTED)
draw.text((margin, sub_y + 42),
          "Launching soon on Android, iOS and Web.",
          font=f_sub, fill=MUTED)

# ---- Bottom accent bar ----
draw.rectangle([0, H - 10, W, H], fill=PRIMARY)

out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "og-image.png")
img.save(out_path, "PNG", optimize=True)
print("saved", img.size, out_path)
