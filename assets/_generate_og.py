"""Generate PNG OG image (1200x630) for the Korea IPO brief.

WeChat link cards don't render SVG — this script produces a PNG version
that maximizes compatibility across WeChat / Telegram / Slack / Twitter / Slack.

Run: python3 assets/_generate_og.py
Output: assets/og-image.png
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
INK = (11, 23, 51)
INK_LIGHT = (30, 49, 104)
PAPER = (250, 250, 247)
CORAL = (249, 115, 87)
CORAL_SOFT = (249, 115, 87, 90)

img = Image.new("RGB", (W, H), INK)
draw = ImageDraw.Draw(img, "RGBA")

# Diagonal gradient feel via two big soft circles
def soft_disc(cx, cy, r, color):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for i in range(r, 0, -8):
        alpha = int(color[3] * (1 - i / r))
        ld.ellipse((cx - i, cy - i, cx + i, cy + i), fill=(*color[:3], alpha))
    img.paste(layer, (0, 0), layer)

soft_disc(int(W * 0.85), int(H * 0.18), 320, (*CORAL, 80))
soft_disc(int(W * 0.10), int(H * 0.85), 260, (*INK_LIGHT, 120))

# Subtle grid
for x in range(0, W, 48):
    draw.line([(x, 0), (x, H)], fill=(250, 250, 247, 12), width=1)
for y in range(0, H, 48):
    draw.line([(0, y), (W, y)], fill=(250, 250, 247, 12), width=1)

# Fonts (macOS system Chinese fonts)
def font(size, bold=False):
    paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc" if bold else "/System/Library/Fonts/STHeiti Light.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

f_tag = font(20, bold=True)
f_h1 = font(78, bold=True)
f_sub = font(22, bold=True)
f_corner = font(36, bold=True)

# Top tag pill
tag_x, tag_y = 80, 80
tag_text = "  韩国市场观察 · 2025–2026"
tw = int(draw.textlength(tag_text, font=f_tag))
draw.rounded_rectangle((tag_x, tag_y, tag_x + tw + 60, tag_y + 44), radius=22, fill=(250, 250, 247, 28))
draw.ellipse((tag_x + 18, tag_y + 16, tag_x + 30, tag_y + 28), fill=CORAL)
draw.text((tag_x + 38, tag_y + 11), tag_text, font=f_tag, fill=PAPER)

# Headline (3 lines)
h_x, h_y = 80, 180
draw.text((h_x, h_y), "韩国对中国 ", font=f_h1, fill=PAPER)
left_w = draw.textlength("韩国对中国 ", font=f_h1)
draw.text((h_x + left_w, h_y), "AI 公司，", font=f_h1, fill=CORAL)
draw.text((h_x, h_y + 100), "既是收入市场，", font=f_h1, fill=PAPER)
draw.text((h_x, h_y + 200), "也是资本市场。", font=f_h1, fill=PAPER)

# Sub stats line
sub_y = 540
sub_parts = [
    ("ChatGPT 付费用户全球 #2", CORAL),
    ("  ·  ", (250, 250, 247, 200)),
    ("KOSDAQ 2025 公募收益 82.6%", CORAL),
    ("（历史第二）", (250, 250, 247, 200)),
]
sx = 80
for txt, color in sub_parts:
    draw.text((sx, sub_y), txt, font=f_sub, fill=color)
    sx += int(draw.textlength(txt, font=f_sub))

# Right corner mark "IPO"
cx, cy = 1020, 80
draw.rounded_rectangle((cx, cy, cx + 100, cy + 100), radius=20, fill=CORAL)
ipo_w = draw.textlength("IPO", font=f_corner)
draw.text((cx + (100 - ipo_w) / 2, cy + 32), "IPO", font=f_corner, fill=PAPER)

out_path = os.path.join(os.path.dirname(__file__), "og-image.png")
img.save(out_path, "PNG", optimize=True)
print(f"Wrote {out_path}  ({os.path.getsize(out_path) // 1024} KB)")
