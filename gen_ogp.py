"""Generate OGP image matching LP hero (1200x630)"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1200, 630

BLUE   = (53, 103, 245)
WHITE  = (255, 255, 255)
YELLOW = (255, 214, 61)
PINK   = (255, 126, 168)
INK    = (29, 34, 51)

FONT_DIR = "C:/Windows/Fonts/"
def font(path, size):
    return ImageFont.truetype(FONT_DIR + path, size)

f_h1    = font("BIZ-UDGothicB.ttc", 100)
f_h1_em = font("BIZ-UDGothicB.ttc", 100)
f_badge = font("BIZ-UDGothicB.ttc", 14)
f_sub   = font("BIZ-UDGothicB.ttc", 20)
f_hint  = font("BIZ-UDGothicB.ttc", 15)
f_logo  = font("BIZ-UDGothicB.ttc", 16)

img  = Image.new("RGB", (W, H), BLUE)
draw = ImageDraw.Draw(img, "RGBA")

# ---- 背景の薄いグリッド（LPのドットっぽさ）----
for x in range(0, W, 60):
    for y in range(0, H, 60):
        draw.ellipse([x-1, y-1, x+1, y+1], fill=(255,255,255,18))

# ==============================
# 幾何学デコレーション（LPと同じ配置イメージ）
# ==============================

def plus(cx, cy, size, color, alpha=200, width=4):
    a = (*color, alpha)
    half = size // 2
    thin = width // 2
    draw.rectangle([cx-thin, cy-half, cx+thin, cy+half], fill=a)
    draw.rectangle([cx-half, cy-thin, cx+half, cy+thin], fill=a)

def circle_outline(cx, cy, r, color, alpha=160, width=3):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r],
                 outline=(*color, alpha), width=width)

def circle_filled(cx, cy, r, color, alpha=220):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*color, alpha))

def diamond(cx, cy, size, color, alpha=220):
    s = size // 2
    draw.polygon([(cx, cy-s), (cx+s, cy), (cx, cy+s), (cx-s, cy)],
                 fill=(*color, alpha))

def striped_circle(cx, cy, r, color, alpha=160):
    """斜線入り円（LPの左上のやつ）"""
    bbox = [cx-r, cy-r, cx+r, cy+r]
    mask = Image.new("RGBA", (W, H), (0,0,0,0))
    md = ImageDraw.Draw(mask)
    md.ellipse(bbox, fill=(*color, alpha))
    # 斜線を上から重ねる
    for i in range(-r*2, r*2, 12):
        md.line([(cx-r+i, cy-r), (cx+i, cy+r)],
                fill=(BLUE[0], BLUE[1], BLUE[2], alpha), width=3)
    img.paste(mask, mask=mask)

# 左上：斜線円
striped_circle(90, 160, 62, WHITE)

# 左上：+ 大
plus(46, 100, 32, WHITE, alpha=180, width=5)

# 左中：空白円
circle_outline(68, 340, 46, WHITE, alpha=130, width=3)

# 左下：- ダッシュ
draw.rectangle([56, 500, 100, 508], fill=(*YELLOW, 200))

# 右上：黄色ダイヤ
diamond(1080, 110, 68, YELLOW, alpha=230)

# 右上：+
plus(1140, 200, 28, WHITE, alpha=160, width=4)

# 右中：塗り円
circle_filled(1130, 310, 28, YELLOW, alpha=200)

# 右下：ピンク四角
draw.rectangle([1060, 480, 1110, 530], fill=(*PINK, 210))

# 右下：+
plus(1155, 520, 30, WHITE, alpha=150, width=4)

# 中央下あたり：+
plus(580, 560, 24, WHITE, alpha=120, width=3)

# 上中央あたりの点
circle_filled(400, 95, 8, WHITE, alpha=150)
circle_filled(820, 85, 6, WHITE, alpha=130)

# ==============================
# バッジ（上部）
# ==============================
badge_text = "freee  /  SOKUSHU ACCOUNTING  /  2026"
bw = draw.textlength(badge_text, font=f_badge) + 48
bx = (W - bw) // 2
by = 52
draw.rounded_rectangle([bx, by, bx+bw, by+34], radius=17,
                        fill=(255,255,255,30), outline=(255,255,255,80), width=1)
# freee ロゴ風の小さい丸
draw.ellipse([bx+14, by+10, bx+28, by+24], fill=(255,255,255,200))
draw.text((bx+18, by+8), "f", font=font("BIZ-UDGothicB.ttc", 13), fill=BLUE)
draw.text((bx+34, by+8), badge_text, font=f_badge, fill=(255,255,255,220))

# ==============================
# メインタイトル
# ==============================
line1 = "経理の現場に、"
line2_w = "10日"
line2_r = "で入る。"

# line1
l1w = draw.textlength(line1, font=f_h1)
draw.text(((W - l1w) // 2, 108), line1, font=f_h1, fill=WHITE)

# line2: "10日" を黄色、残りを白
l2w_yellow = draw.textlength(line2_w, font=f_h1_em)
l2w_white  = draw.textlength(line2_r, font=f_h1)
l2_total   = l2w_yellow + l2w_white
l2x = (W - l2_total) // 2
draw.text((l2x, 218), line2_w, font=f_h1_em, fill=YELLOW)
draw.text((l2x + l2w_yellow, 218), line2_r, font=f_h1, fill=WHITE)

# ==============================
# サブテキスト
# ==============================
sub = "動画8時間と実地2日間のプログラム。修了者全員に就労先を複数ご紹介。"
sw = draw.textlength(sub, font=f_sub)
draw.text(((W - sw) // 2, 346), sub, font=f_sub, fill=(255,255,255,210))

# ==============================
# ロゴ strip（中段）
# ==============================
logo_y = 398
sep_color = (255,255,255,80)

logos = ["Hatenabase", "|", "← freee", "|", "Digital Base"]
total_lw = sum(draw.textlength(t, font=f_logo) for t in logos) + 40 * (len(logos)-1)
lx = (W - total_lw) // 2
for t in logos:
    tw = draw.textlength(t, font=f_logo)
    color = (255,255,255,160) if t == "|" else (255,255,255,210)
    draw.text((lx, logo_y), t, font=f_logo, fill=color)
    lx += tw + 40

# ==============================
# ヒントライン（下部）
# ==============================
hint = "8h E-learning  /  2 days 実地研修  /  ¥50,000 受講料（税抜）"
hw = draw.textlength(hint, font=f_hint)
hx = (W - hw) // 2
hy = H - 52
# 左右の線
line_len = 50
draw.line([(hx - line_len - 16, hy+10), (hx - 16, hy+10)],
          fill=(255,255,255,100), width=1)
draw.line([(hx + hw + 16, hy+10), (hx + hw + 16 + line_len, hy+10)],
          fill=(255,255,255,100), width=1)
draw.text((hx, hy), hint, font=f_hint, fill=(255,255,255,180))

# 保存
out = "C:/Users/fumik/hatenabase-freee-training/images/ogp.png"
img.save(out, "PNG", optimize=True)
print(f"Saved: {out}")
