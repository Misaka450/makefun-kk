#!/usr/bin/env python3
"""Build entry.png v4 for make.fun bounty news-image-20261123.

Run:  python3 build_image.py
Writes: entry.png  (1024x1024, PNG)

Design v4: bright colourful infographic (user's choice; the
newspaper front-page look of v1-v3 was rejected wholesale).
  - White page, vivid saturated colour per story, rounded
    colourful cards, big white number chips, modern sans-serif
    type only. No serif, no navy masthead, no beige paper,
    no hairline rules.
  - Bright violet header band with big white WORLD NEWS and a
    yellow date chip naming MONDAY 23 NOVEMBER 2026.
  - Lead story (COP31) as the biggest block, teal, with the
    model-generated serious hero (cracked teal/green globe,
    plain gold sun with straight rays and NO face, coral
    mountains, turquoise sea, no text, no faces anywhere).
  - Five colourful blocks in a 2 + 3 grid, each with a big
    headline and a flat icon in a white circle. Planet and
    scales icons are model-generated (bright, no text); pin,
    chart and building are clean white-on-card code icons,
    kept because they read perfectly at 58px.
  - Markets block carries a small white bar chart with the
    exact numbers Nikkei -5.06% and S&P 500 -3.7%.
Every headline and number comes from the verified list in
README.md -- nothing was invented or changed. Text is wrapped
by measured pixel width so nothing is cut off or overlaps.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO_PATH = os.path.join(
    HERE, "assets",
    "media-generation-cop31-hero-serious-0-b200ad05-dca8-477f-bce5-1be5b0e9a494.png")
ICON_PLANET = os.path.join(
    HERE, "assets",
    "media-generation-v4-icon-planet-0-8f65fea6-b401-48d0-967a-ce23230d7f19.webp")
ICON_SCALES = os.path.join(
    HERE, "assets",
    "media-generation-v4-icon-scales-0-53985519-b168-4348-b290-faa294315781.webp")

W, H = 1024, 1024
WHITE = (255, 255, 255)
INK = (24, 28, 38)
MUTED_D = (90, 98, 112)          # footer grey on white
VIOLET = (109, 40, 217)          # header band
YELLOW = (255, 217, 61)          # date chip
TEAL = (0, 178, 160)             # lead: climate
TEAL_D = (0, 138, 124)           # lead darker teal
ORANGE = (255, 107, 53)          # Dymer
GREEN = (22, 163, 74)            # markets
RED = (239, 68, 68)              # Khartoum
PURPLE = (124, 58, 237)          # Sinaloa
BLUE = (37, 99, 235)             # Mercury

SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, text, fnt, x, y, max_w, fill, lh, max_lines=None):
    lines = wrap(d, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def paste_cover(img, path, x0, y0, x1, y1, radius=18, border=None):
    """Cover-crop an image into a rounded box (no text added)."""
    src = Image.open(path).convert("RGB")
    bw, bh = x1 - x0, y1 - y0
    sw, sh = src.size
    scale = max(bw / sw, bh / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    src = src.resize((nw, nh), Image.LANCZOS)
    ox, oy = (nw - bw) // 2, (nh - bh) // 2
    crop = src.crop((ox, oy, ox + bw, oy + bh))
    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=radius, fill=255)
    img.paste(crop, (x0, y0), mask)
    if border:
        ImageDraw.Draw(img).rounded_rectangle(
            [x0, y0, x1, y1], radius=radius, outline=border, width=3)


def paste_model_icon(img, path, cx, cy, size=52):
    """Paste a model-generated icon on a white background, centred.

    Auto-crop to the symbol, then knock near-white pixels out to
    transparent so no square patch shows on the white circle.
    """
    ic = Image.open(path).convert("RGB")
    w, h = ic.size
    bg = ic.getpixel((2, 2))
    px = ic.load()
    minx, miny, maxx, maxy = w, h, -1, -1
    for yy in range(0, h, 2):
        for xx in range(0, w, 2):
            r, g, b = px[xx, yy]
            if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > 60:
                minx, miny = min(minx, xx), min(miny, yy)
                maxx, maxy = max(maxx, xx), max(maxy, yy)
    pad = 10
    minx, miny = max(0, minx - pad), max(0, miny - pad)
    maxx, maxy = min(w - 1, maxx + pad), min(h - 1, maxy + pad)
    ic = ic.crop((minx, miny, maxx + 1, maxy + 1))
    scale = min(size / ic.width, size / ic.height)
    ic = ic.resize((max(1, int(ic.width * scale)), max(1, int(ic.height * scale))),
                   Image.LANCZOS)
    rgba = ic.convert("RGBA")
    out = []
    for p in rgba.getdata():
        if abs(p[0] - bg[0]) + abs(p[1] - bg[1]) + abs(p[2] - bg[2]) < 50:
            out.append((p[0], p[1], p[2], 0))
        else:
            out.append(p)
    rgba.putdata(out)
    img.paste(rgba, (cx - rgba.width // 2, cy - rgba.height // 2), rgba)


# ------------------------------------------------- white code-drawn icons
def icon_pin(d, cx, cy, col):
    d.ellipse([cx - 13, cy - 17, cx + 13, cy + 8], fill=col)
    d.polygon([(cx - 11, cy + 1), (cx + 11, cy + 1), (cx, cy + 19)], fill=col)
    d.ellipse([cx - 5, cy - 9, cx + 5, cy + 1], fill=WHITE)


def icon_chart(d, cx, cy, col):
    for bx, bh in [(-16, 20), (-5, 15), (6, 10), (17, 5)]:
        d.rectangle([cx + bx - 4, cy + 12 - bh, cx + bx + 4, cy + 12], fill=col)
    d.line([(cx - 20, cy - 12), (cx + 21, cy + 6)], fill=col, width=3)


def icon_building(d, cx, cy, col):
    d.polygon([(cx - 16, cy - 12), (cx + 16, cy - 12), (cx, cy - 20)], fill=col)
    d.rectangle([cx - 16, cy - 12, cx + 16, cy + 17], fill=col)
    for dx in (-11, -3, 5):
        d.rectangle([cx + dx, cy - 7, cx + dx + 4, cy + 12], fill=WHITE)
    d.rectangle([cx - 19, cy + 17, cx + 19, cy + 20], fill=col)


# ------------------------------------------------- story card
def card(d, img, x, y, w, h, bg, num, tag, place, head, body,
         icon=None, model_icon=None, markets=False):
    d.rounded_rectangle([x, y, x + w, y + h], radius=22, fill=bg)
    # top row: big white number, tag + place, icon in a white circle
    d.text((x + 22, y + 16), num, font=font(SANS_B, 30), fill=WHITE)
    d.text((x + 68, y + 20), tag, font=font(SANS_B, 15), fill=WHITE)
    d.text((x + 68, y + 42), place, font=font(SANS_R, 14), fill=(255, 255, 255))
    icx, icy = x + w - 48, y + 48
    d.ellipse([icx - 32, icy - 32, icx + 32, icy + 32], fill=WHITE)
    if model_icon:
        paste_model_icon(img, model_icon, icx, icy, size=50)
    elif icon:
        icon(d, icx, icy, bg)
    # headline + body, wrapped to the card width
    tx, tw = x + 22, w - 44
    hf = font(SANS_B, 25 if w > 400 else 22)
    while d.textlength(head, font=hf) > tw * 2 and hf.size > 19:
        hf = font(SANS_B, hf.size - 1)
    hy = y + 82
    hy = draw_wrapped(d, head, hf, tx, hy, tw, WHITE,
                      30 if w > 400 else 27, max_lines=3)
    if markets:
        # white bar chart, exact numbers, at the card bottom
        by = y + h - 78
        for j, (name, val, frac) in enumerate(
                [("NIKKEI", "-5.06%", 1.0), ("S&P 500", "-3.7%", 3.7 / 5.06)]):
            cy = by + j * 36
            d.text((tx, cy), name, font=font(SANS_B, 15), fill=WHITE)
            vw = d.textlength(val, font=font(SANS_B, 17))
            d.text((tx + tw - vw, cy - 2), val, font=font(SANS_B, 17), fill=WHITE)
            d.rectangle([tx, cy + 21, tx + tw, cy + 29], fill=(255, 255, 255))
            d.rectangle([tx, cy + 21, tx + int(tw * frac), cy + 29], fill=YELLOW)
    else:
        bf = font(SANS_R, 17 if w > 400 else 16)
        draw_wrapped(d, body, bf, tx, hy + 6, tw, (255, 255, 255), 22, max_lines=2)


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---- bright header band ----
    d.rounded_rectangle([28, 24, 996, 150], radius=24, fill=VIOLET)
    d.text((56, 42), "WORLD NEWS", font=font(SANS_B, 62), fill=WHITE)
    # yellow date chip
    chip = "MONDAY  23  NOVEMBER  2026"
    cf = font(SANS_B, 22)
    cw = d.textlength(chip, font=cf) + 36
    d.rounded_rectangle([56, 108, 56 + cw, 108 + 30], radius=15, fill=YELLOW)
    d.text((56 + 18, 113), chip, font=cf, fill=(60, 20, 120))
    d.text((700, 52), "6 STORIES", font=font(SANS_B, 26), fill=WHITE)
    d.text((700, 86), "ONE DAY", font=font(SANS_B, 26), fill=(255, 255, 255))

    # ---- lead story: big teal block ----
    lx, ly, lw, lh = 28, 166, 968, 300
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=24, fill=TEAL)
    d.rounded_rectangle([56, 188, 56 + 300, 188 + 30], radius=15, fill=TEAL_D)
    d.text((56 + 16, 193), "01  •  CLIMATE  •  ANTALYA", font=font(SANS_B, 15), fill=WHITE)
    draw_wrapped(d, "COP31 ends without a deal", font(SANS_B, 46), 56, 228, 500,
                 WHITE, 52, max_lines=2)
    draw_wrapped(d, "EU and about 130 parties reject a text omitting fossil fuels.",
                 font(SANS_R, 22), 56, 340, 500, WHITE, 30, max_lines=2)
    # white stat chip with the verified number
    d.rounded_rectangle([56, 408, 56 + 500, 408 + 44], radius=14, fill=WHITE)
    d.text((56 + 18, 414), "130", font=font(SANS_B, 30), fill=TEAL_D)
    d.text((56 + 118, 420), "parties rejected the text", font=font(SANS_B, 20),
           fill=(0, 90, 82))
    paste_cover(img, HERO_PATH, 592, 182, 980, 450, radius=18, border=WHITE)

    # ---- grid: 2 wide cards, then 3 narrower cards ----
    card(d, img, 28, 482, 472, 232, ORANGE, "02", "CONFLICT", "DYMER, UKRAINE",
         "Russian strike kills at least 10",
         "A 7-year-old boy is pulled alive from the rubble in Dymer, north of Kyiv.",
         icon=icon_pin)
    card(d, img, 524, 482, 472, 232, GREEN, "03", "MARKETS", "TOKYO  /  NEW YORK",
         "AI sell-off rattles markets",
         "Nikkei falls 5.06%; S&P 500 falls 3.7%.",
         icon=icon_chart, markets=True)
    card(d, img, 28, 730, 304, 232, RED, "04", "CONFLICT", "KHARTOUM, SUDAN",
         "Drone strikes kill five children",
         "Strikes hit homes and a UN building in Khartoum.",
         icon=icon_building)
    card(d, img, 360, 730, 304, 232, PURPLE, "05", "JUSTICE", "SINALOA, MEXICO",
         "‘El Chapo Isidro’ captured",
         "FBI most-wanted fugitive seized; 11 killed in violence during the capture.",
         model_icon=ICON_SCALES)
    card(d, img, 692, 730, 304, 232, BLUE, "06", "SPACE", "MERCURY",
         "BepiColombo reaches Mercury",
         "Probe enters Mercury orbit after an eight-year journey.",
         model_icon=ICON_PLANET)

    # ---- footer ----
    foot = "All six stories were reported on Monday 23 November 2026."
    ff = font(SANS_R, 15)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 982), foot, font=ff, fill=MUTED_D)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
