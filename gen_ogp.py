"""Generate OGP image for freee training LP (1200x630)"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1200, 630

# --- Colors ---
BG       = (29, 34, 51)
BLUE     = (53, 103, 245)
BLUE_DIM = (53, 103, 245, 60)
YELLOW   = (255, 214, 61)
WHITE    = (255, 255, 255)
GRAY     = (122, 132, 154)
SOFT     = (58, 68, 102)
CARD_BG  = (255, 255, 255, 16)

# --- Fonts ---
FONT_DIR = "C:/Windows/Fonts/"
def font(path, size):
    return ImageFont.truetype(FONT_DIR + path, size)

f_heavy   = font("BIZ-UDGothicB.ttc", 72)
f_title   = font("BIZ-UDGothicB.ttc", 60)
f_sub     = font("YuGothM.ttc", 22)
f_label   = font("BIZ-UDGothicB.ttc", 16)
f_badge_n = font("BIZ-UDGothicB.ttc", 34)
f_badge_u = font("BIZ-UDGothicB.ttc", 17)
f_badge_l = font("YuGothM.ttc", 13)
f_feat_m  = font("BIZ-UDGothicB.ttc", 17)
f_feat_s  = font("YuGothM.ttc", 13)
f_footer  = font("YuGothM.ttc", 14)

# --- Canvas ---
img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

# ---- Background dots ----
DOT_STEP = 30
for x in range(0, W, DOT_STEP):
    for y in range(0, H, DOT_STEP):
        draw.ellipse([x-1, y-1, x+1, y+1], fill=(255,255,255,10))

# ---- Background glow circles ----
def radial_glow(cx, cy, r, color_rgb, steps=60, max_alpha=40):
    for i in range(steps, 0, -1):
        alpha = int(max_alpha * (i / steps) ** 2.5)
        rr = int(r * i / steps)
        draw.ellipse([cx-rr, cy-rr, cx+rr, cy+rr],
                     fill=(*color_rgb, alpha))

radial_glow(1050, -30, 260, (53, 103, 245), steps=50, max_alpha=22)
radial_glow(280, 600, 200, (53, 103, 245), steps=40, max_alpha=18)

# ---- Top-right corner triangle ----
draw.polygon([(W, 0), (W-120, 0), (W, 120)], fill=(53,103,245, 30))

# ---- Left accent bar (gradient blue → yellow) ----
BAR_W = 8
for y in range(H):
    t = y / H
    r = int(53  + (255-53)  * t)
    g = int(103 + (214-103) * t)
    b = int(245 + (61-245)  * t)
    draw.line([(0, y), (BAR_W-1, y)], fill=(r, g, b))

# ---- Helper: rounded rectangle ----
def rrect(xy, r, fill, outline=None, width=1):
    x0,y0,x1,y1 = xy
    draw.rounded_rectangle([x0,y0,x1,y1], radius=r, fill=fill,
                            outline=outline, width=width)

# ---- Label badge ----
label_text = " はてなベース × freee 公認研修"
lx, ly = 80, 62
lw = draw.textlength(label_text, font=f_label) + 40
rrect([lx, ly, lx+lw, ly+36], 18,
      fill=(53,103,245, 45), outline=(53,103,245,130), width=2)
# dot
draw.ellipse([lx+14, ly+14, lx+22, ly+22], fill=BLUE)
draw.text((lx+28, ly+8), label_text.strip(), font=f_label, fill=(130,168,255))

# ---- Main title ----
# "速習 " in white, "freee" in yellow, " 会計研修" in white
tx, ty = 80, 112
title_parts = [("速習 ", WHITE), ("freee", YELLOW), (" 会計研修", WHITE)]
cx = tx
for txt, color in title_parts:
    draw.text((cx, ty), txt, font=f_heavy, fill=color)
    cx += draw.textlength(txt, font=f_heavy)

# ---- Subtitle ----
draw.text((80, 197), "経理の現場に、10日で入る。", font=f_sub,
          fill=(255,255,255,165))

# ---- Stat badges ----
badges = [
    ("10", "日",  "最短修了期間"),
    ("8",  "時間", "動画学習"),
    ("¥50","K",   "受講料（税抜）"),
    ("100","%",   "修了者就労紹介"),
]
bx_start = 80
by = 248
bw, bh = 132, 76
gap = 14
for i, (num, unit, lbl) in enumerate(badges):
    bx = bx_start + i * (bw + gap)
    rrect([bx, by, bx+bw, by+bh], 14,
          fill=(255,255,255,15), outline=(255,255,255,30), width=1)
    # number + unit
    nw = draw.textlength(num, font=f_badge_n)
    uw = draw.textlength(unit, font=f_badge_u)
    total_w = nw + uw
    nx = bx + (bw - total_w) // 2
    draw.text((nx, by+10), num, font=f_badge_n, fill=WHITE)
    draw.text((nx+nw, by+22), unit, font=f_badge_u, fill=YELLOW)
    # label
    lw2 = draw.textlength(lbl, font=f_badge_l)
    draw.text((bx + (bw - lw2)//2, by+52), lbl, font=f_badge_l,
              fill=(255,255,255,128))

# ---- Right panel: feature cards ----
PANEL_X = 820
features = [
    ("🎬", "動画＋実地で習得",   "e-learning 8h ＋ 現場研修 2日"),
    ("📊", "freee 実務に直結",   "記帳・仕訳・決算補助まで"),
    ("💼", "修了後に就労先紹介", "経理事務所・企業へ複数紹介"),
]
card_w = 330
card_h = 92
card_gap = 18
card_total = len(features)*card_h + (len(features)-1)*card_gap
card_y_start = (H - card_total) // 2

for i, (icon, main, sub) in enumerate(features):
    cx2 = PANEL_X
    cy = card_y_start + i * (card_h + card_gap)
    rrect([cx2, cy, cx2+card_w, cy+card_h], 16,
          fill=(53,103,245,35), outline=(53,103,245, 80), width=2)
    # icon
    try:
        icon_font = font("seguiemj.ttf", 30)
    except:
        icon_font = f_sub
    draw.text((cx2+18, cy+28), icon, font=icon_font, fill=WHITE,
              embedded_color=True)
    # text
    draw.text((cx2+68, cy+18), main, font=f_feat_m, fill=WHITE)
    draw.text((cx2+68, cy+46), sub,  font=f_feat_s, fill=(255,255,255,128))

# ---- Divider line between main and right ----
for y in range(80, H-80):
    alpha = int(60 * math.sin(math.pi * (y-80) / (H-160)))
    draw.point((PANEL_X - 30, y), fill=(255,255,255,alpha))

# ---- Footer ----
draw.text((88, H-42), "はてなベース株式会社", font=f_footer,
          fill=(255,255,255,100))
draw.ellipse([88+draw.textlength("はてなベース株式会社", font=f_footer)+8, H-36,
              88+draw.textlength("はてなベース株式会社", font=f_footer)+14, H-30],
             fill=(255,255,255,50))
draw.text((88+draw.textlength("はてなベース株式会社", font=f_footer)+20, H-42),
          "hatenabase.com", font=f_footer, fill=(255,255,255,100))

# ---- Bottom accent line ----
for x in range(W):
    t = x / W
    r = int(53  + (255-53)  * t)
    g = int(103 + (214-103) * t)
    b = int(245 + (61-245)  * t)
    draw.line([(x, H-4), (x, H-1)], fill=(r,g,b))

# ---- Save ----
out = "C:/Users/fumik/hatenabase-freee-training/images/ogp.png"
img.save(out, "PNG", optimize=True)
print(f"Saved: {out}")
print(f"Size: {img.size}")
