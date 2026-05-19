"""Generate OGP image - editorial split layout (1200x630)"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1200, 630
SPLIT = 760  # 左パネルの幅

# --- Colors ---
CREAM    = (255, 252, 249)   # --paper
CREAM2   = (242, 235, 224)   # --paper-2
BLUE     = (53, 103, 245)    # --freee
BLUE_D   = (23, 68, 199)     # --freee-deep
INK      = (29, 34, 51)      # --ink
INK_SOFT = (58, 68, 102)     # --ink-soft
MUTED    = (122, 132, 154)
YELLOW   = (255, 214, 61)    # --accent
WHITE    = (255, 255, 255)

FONT_DIR = "C:/Windows/Fonts/"
def font(path, size):
    return ImageFont.truetype(FONT_DIR + path, size)

f_h1     = font("BIZ-UDGothicB.ttc", 68)
f_h1_sm  = font("BIZ-UDGothicB.ttc", 62)
f_tag    = font("BIZ-UDGothicB.ttc", 14)
f_sub    = font("YuGothM.ttc", 21)
f_stat_n = font("BIZ-UDGothicB.ttc", 44)
f_stat_u = font("BIZ-UDGothicB.ttc", 18)
f_stat_l = font("YuGothM.ttc", 13)
f_feat   = font("BIZ-UDGothicB.ttc", 16)
f_feat_s = font("YuGothM.ttc", 13)
f_price  = font("BIZ-UDGothicB.ttc", 42)
f_price_l= font("BIZ-UDGothicB.ttc", 14)
f_cta    = font("BIZ-UDGothicB.ttc", 18)
f_foot   = font("YuGothM.ttc", 13)

img  = Image.new("RGB", (W, H), CREAM)
draw = ImageDraw.Draw(img, "RGBA")

# ==============================
# 左パネル（クリーム）
# ==============================

# 薄いグリッド線（紙っぽさ）
for y in range(0, H, 40):
    draw.line([(0, y), (SPLIT, y)], fill=(*CREAM2, 120))

# 上部アクセントバー
draw.rectangle([0, 0, SPLIT, 6], fill=BLUE)

# タグ
TAG_X, TAG_Y = 56, 36
tag_text = "はてなベース × freee 公認"
tw = draw.textlength(tag_text, font=f_tag)
draw.rectangle([TAG_X-1, TAG_Y-1, TAG_X+tw+20, TAG_Y+26], fill=BLUE)
draw.text((TAG_X+10, TAG_Y+4), tag_text, font=f_tag, fill=WHITE)

# メインタイトル
TX, TY = 56, 82
# "速習" 行
draw.text((TX, TY), "速習", font=f_h1, fill=INK)
sw = draw.textlength("速習", font=f_h1)
# "freee" をブルーで inline
draw.text((TX + sw + 10, TY), "freee", font=f_h1, fill=BLUE)
fw = draw.textlength("freee", font=f_h1)
# "会計研修" 行
draw.text((TX, TY + 78), "会計研修", font=f_h1, fill=INK)

# サブタイトル
draw.text((TX, TY + 168), "経理の現場に、10日で入る。", font=f_sub, fill=INK_SOFT)

# 区切り線
draw.line([(TX, TY+210), (TX+560, TY+210)], fill=(*CREAM2, 255), width=2)

# 数字バッジ（stats row）
stats = [
    ("10", "日",  "修了期間"),
    ("8",  "h",   "動画学習"),
    ("2",  "日",  "現場研修"),
]
BX = TX
BY = TY + 228
BW = 150
BH = 96
for i, (num, unit, label) in enumerate(stats):
    bx = BX + i * (BW + 12)
    draw.rounded_rectangle([bx, BY, bx+BW, BY+BH], radius=10,
                            fill=WHITE, outline=(*CREAM2, 255), width=2)
    nw = draw.textlength(num, font=f_stat_n)
    uw = draw.textlength(unit, font=f_stat_u)
    total = nw + uw + 2
    nx = bx + (BW - total) // 2
    draw.text((nx, BY+10), num, font=f_stat_n, fill=INK)
    draw.text((nx+nw+2, BY+26), unit, font=f_stat_u, fill=BLUE)
    lw = draw.textlength(label, font=f_stat_l)
    draw.text((bx + (BW-lw)//2, BY+66), label, font=f_stat_l, fill=MUTED)

# フッター（左下）
draw.text((TX, H-36), "hatenabase.com", font=f_foot, fill=(*MUTED, 180))

# ==============================
# 右パネル（ブルー）
# ==============================

# 右パネル背景
draw.rectangle([SPLIT, 0, W, H], fill=BLUE)

# 右パネル内の斜めストライプ（さりげない）
for i in range(-10, 30):
    x0 = SPLIT + i * 30
    draw.line([(x0, 0), (x0 + H, H)], fill=(255,255,255, 8), width=12)

# 右上角の三角アクセント
draw.polygon([(W-120, 0), (W, 0), (W, 120)], fill=(255,255,255, 20))
# 左下角アクセント
draw.polygon([(SPLIT, H-100), (SPLIT+100, H), (SPLIT, H)], fill=(23,68,199, 180))

# 右パネルコンテンツ
RX = SPLIT + 40
RW = W - SPLIT - 40

# 受講料ブロック
ry = 70
draw.text((RX, ry), "受講料", font=f_price_l, fill=(255,255,255,160))
ry += 22
pw = draw.textlength("¥50,000", font=f_price)
draw.text((RX, ry), "¥50,000", font=f_price, fill=WHITE)
draw.text((RX+pw+6, ry+18), "（税抜）", font=f_foot, fill=(255,255,255,140))
ry += 58

# 区切り
draw.line([(RX, ry), (W-40, ry)], fill=(255,255,255,40), width=1)
ry += 20

# 特徴リスト
features = [
    ("✓", "修了者全員に就労先を紹介"),
    ("✓", "完全オンライン対応"),
    ("✓", "freee認定アドバイザー監修"),
    ("✓", "税理士事務所が直接運営"),
]
for icon, text in features:
    draw.text((RX, ry), icon, font=f_feat, fill=YELLOW)
    draw.text((RX+22, ry), text, font=f_feat, fill=WHITE)
    ry += 34

# 区切り
ry += 8
draw.line([(RX, ry), (W-40, ry)], fill=(255,255,255,40), width=1)
ry += 20

# CTA テキスト
cta = "無料相談受付中"
draw.rounded_rectangle([RX, ry, W-40, ry+44], radius=8,
                        fill=(255,255,255,25), outline=(255,255,255,60), width=1)
cw = draw.textlength(cta, font=f_cta)
draw.text((RX + (RW - cw)//2, ry+10), cta, font=f_cta, fill=WHITE)

# 右パネル下部 ブランド
draw.text((RX, H-36), "はてなベース株式会社", font=f_foot, fill=(255,255,255,120))

# ==============================
# 左右の境界線シャドウ
# ==============================
for i in range(8):
    alpha = int(60 * (1 - i/8))
    draw.line([(SPLIT+i, 0), (SPLIT+i, H)], fill=(0,0,0,alpha))

# 保存
out = "C:/Users/fumik/hatenabase-freee-training/images/ogp.png"
img.save(out, "PNG", optimize=True)
print(f"Saved: {out}")
