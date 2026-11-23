#!/usr/bin/env python3
"""Build entry.png for make.fun bounty news-image-20261123.

Run:  python3 build_image.py
Writes: entry.png  (1024x1024, PNG)

Design: dark-navy newspaper header naming the day, then six panels
(2 columns x 3 rows), one per verified story of 23 November 2026.
Every headline and number below comes from the verified list in
README.md -- nothing else was invented. Text is wrapped by measured
pixel width so nothing is cut off or overlaps.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 232)          # warm paper
HEADER = (15, 42, 68)         # dark navy
PANEL = (255, 255, 255)
INK = (18, 24, 32)
MUTED = (74, 85, 99)
RULE = (203, 213, 225)

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to lines that fit max_w pixels (measured, not guessed)."""
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


PANELS = [
    dict(num="01", tag="CLIMATE", place="ANTALYA, TURKEY",
         accent=(14, 122, 107),
         head="COP31 ends without a deal",
         body="EU and about 130 parties reject a text omitting fossil fuels."),
    dict(num="02", tag="CONFLICT", place="DYMER, UKRAINE",
         accent=(180, 35, 24),
         head="Russian strike kills at least 10",
         body="A 7-year-old boy is pulled alive from the rubble in Dymer, north of Kyiv."),
    dict(num="03", tag="MARKETS", place="TOKYO  /  NEW YORK",
         accent=(154, 106, 0),
         head="AI sell-off rattles markets",
         body="Nikkei falls 5.06%; S&P 500 falls 3.7%."),
    dict(num="04", tag="CONFLICT", place="KHARTOUM, SUDAN",
         accent=(107, 63, 160),
         head="Drone strikes kill five children",
         body="Strikes hit homes and a UN building in Khartoum."),
    dict(num="05", tag="JUSTICE", place="SINALOA, MEXICO",
         accent=(36, 86, 166),
         head="\u2018El Chapo Isidro\u2019 captured",
         body="FBI most-wanted fugitive seized; 11 killed in violence during the capture."),
    dict(num="06", tag="SPACE", place="MERCURY",
         accent=(46, 125, 50),
         head="BepiColombo reaches Mercury",
         body="Probe enters Mercury orbit after an eight-year journey."),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 168], fill=HEADER)
    d.rectangle([0, 168, W, 174], fill=(198, 160, 60))  # gold rule
    title_f = font(BOLD, 74)
    date_f = font(BOLD, 36)
    sub_f = font(REG, 22)
    d.text((32, 18), "WORLD NEWS", font=title_f, fill=(255, 255, 255))
    d.text((32, 100), "MONDAY  23  NOVEMBER  2026", font=date_f,
           fill=(255, 214, 110))
    d.text((640, 112), "Six stories that\ndefined the day", font=sub_f,
           fill=(214, 226, 238))

    # ---- panels: 2 cols x 3 rows ----
    margin, gutter = 24, 16
    pw = (W - 2 * margin - gutter) // 2          # 480
    ph = (H - 174 - margin - 2 * gutter - 8) // 3  # ~262
    head_f = font(BOLD, 32)
    body_f = font(REG, 22)
    tag_f = font(BOLD, 18)
    num_f = font(BOLD, 26)

    for i, p in enumerate(PANELS):
        col, row = i % 2, i // 2
        x0 = margin + col * (pw + gutter)
        y0 = 174 + 8 + row * (ph + gutter)
        x1, y1 = x0 + pw, y0 + ph
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=PANEL,
                            outline=RULE, width=2)
        d.rectangle([x0, y0 + 10, x0 + 8, y1 - 10], fill=p["accent"])
        # number badge, top right
        cx, cy, r = x1 - 38, y0 + 36, 24
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=p["accent"])
        tw = d.textlength(p["num"], font=num_f)
        d.text((cx - tw / 2, cy - 17), p["num"], font=num_f, fill=(255, 255, 255))
        # tag + place
        tx = x0 + 26
        d.text((tx, y0 + 18), p["tag"], font=tag_f, fill=p["accent"])
        d.text((tx, y0 + 44), p["place"], font=tag_f, fill=MUTED)
        # headline, wrapped to 2 lines max
        lines = wrap(d, p["head"], head_f, pw - 52)
        hy = y0 + 78
        for ln in lines[:2]:
            d.text((tx, hy), ln, font=head_f, fill=INK)
            hy += 38
        # body, wrapped
        blines = wrap(d, p["body"], body_f, pw - 52)
        by = hy + 12
        for ln in blines[:3]:
            d.text((tx, by), ln, font=body_f, fill=(38, 48, 62))
            by += 29

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
