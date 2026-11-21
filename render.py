"""Render the front page (stories.json) to entry.png, 1024x1024, deterministic.

Build-time tooling for the news-image-20261121 entry. The entry program
(main.py) only copies the rendered entry.png to /output/entry.png.
Layout follows the top-10 DNA of this campaign: the DATE is the hero,
3 big illustrated leads, 10 numbered mid stories with source + verification
label each, a numbered list to 35, a WHERE IT HAPPENED map with pins, and
an explicit DATE CHECK box naming what was left out and why.
"""
import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (253, 246, 227)
INK = (26, 26, 26)
RED = (185, 28, 28)
GREY = (110, 105, 95)
DARKGREY = (60, 58, 52)
RULE = (26, 26, 26)
LABEL_COLORS = {
    "OFFICIAL": (15, 118, 110),
    "CONFIRMED": (30, 64, 175),
    "REPORTED": (120, 53, 15),
    "CLAIMED": (153, 27, 27),
}

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-75, 62),
     (-80, 45), (-75, 35), (-80, 25), (-90, 20), (-97, 16), (-105, 20),
     (-115, 30), (-125, 40), (-125, 50), (-140, 60), (-160, 58)],
    [(-80, 10), (-75, 5), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-50, -30), (-60, -40), (-70, -55), (-75, -40), (-80, -20),
     (-80, -5)],
    [(-10, 36), (-10, 45), (-5, 50), (0, 52), (5, 58), (10, 60), (20, 70),
     (30, 70), (40, 68), (35, 60), (30, 55), (25, 45), (20, 40), (15, 38),
     (10, 38), (0, 36)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 10), (45, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (12, -5), (9, 4), (-8, 4)],
    [(40, 68), (60, 70), (90, 75), (120, 77), (150, 72), (170, 66), (180, 65),
     (170, 60), (160, 55), (140, 45), (130, 40), (127, 35), (120, 30),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (80, 20), (75, 10),
     (70, 20), (60, 25), (55, 28), (48, 30), (42, 35), (40, 40)],
    [(113, -22), (125, -15), (135, -12), (142, -11), (150, -22), (150, -37),
     (140, -38), (130, -32), (120, -34), (113, -25)],
]


def font(name, size):
    paths = {
        "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "mono_b": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    }
    return ImageFont.truetype(paths[name], size)


def wrap(draw, text, fnt, max_w, max_lines=None):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "\u2026", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1] + "\u2026"
    return lines


def text_block(d, x, y, lines, fnt, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def label_chip(d, x, y, label):
    """Small coloured verification chip; returns width used."""
    col = LABEL_COLORS[label]
    w = d.textlength(label, font=font("sans_b", 9)) + 10
    d.rectangle([x, y, x + w, y + 14], fill=col)
    d.text((x + 5, y + 7), label, font=font("sans_b", 9),
           fill=(255, 255, 255), anchor="lm")
    return w


def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    d.ellipse([x + w - 78, y + 8, x + w - 18, y + 68], fill=(240, 200, 90))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(120, 140, 110))
    d.rectangle([x + 24, y + h - 62, x + w - 24, y + h - 34], fill=(90, 70, 55))
    for i, fx in enumerate([x + 40, x + w // 2, x + w - 52]):
        d.line([(fx, y + 14), (fx, y + h - 62)], fill=INK, width=2)
        d.polygon([(fx, y + 14), (fx + 26, y + 22), (fx, y + 30)],
                  fill=[(30, 64, 175), (185, 28, 28), (15, 118, 110)][i])
    d.text((x + 10, y + 6), "ANTALYA", font=font("sans_b", 11), fill=INK)


def art_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 28, 58))
    d.ellipse([x + 18, y + 10, x + 46, y + 38], fill=(240, 230, 180))
    d.ellipse([x + 26, y + 8, x + 52, y + 36], fill=(18, 28, 58))
    for bx, bh in [(x + 20, 46), (x + 62, 66), (x + 112, 54), (x + 158, 74),
                   (x + 206, 58), (x + 248, 40)]:
        d.rectangle([bx, y + h - bh, bx + 34, y + h], fill=(45, 60, 100))
        for wy in range(y + h - bh + 8, y + h - 6, 12):
            d.rectangle([bx + 6, wy, bx + 12, wy + 5], fill=(250, 210, 90))
            d.rectangle([bx + 20, wy, bx + 26, wy + 5], fill=(250, 210, 90))
    for cx in (x + 90, x + 170, x + 250):
        d.arc([cx - 34, y + 6, cx + 34, y + 74], 200, 340, fill=(250, 210, 90), width=3)
        for dx, dy in [(0, -6), (5, 3), (-5, 3), (0, 6)]:
            d.line([(cx + dx, y + 22 + dy), (cx - dx, y + 22 - dy)],
                   fill=(255, 255, 255), width=2)


def art_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    d.ellipse([x + w - 66, y + 8, x + w - 22, y + 52], fill=(240, 190, 80))
    d.polygon([(x, y + h), (x + 90, y + 18), (x + 180, y + h)], fill=(120, 85, 50))
    d.polygon([(x + 120, y + h), (x + 220, y + 30), (x + w, y + h)], fill=(90, 60, 35))
    d.polygon([(x + 76, y + 34), (x + 90, y + 18), (x + 104, y + 34), (x + 90, y + 30)],
              fill=(255, 255, 255))
    pts = []
    px, py = x + 8, y + h - 22
    pts.append((px, py))
    for i, (dx, dy) in enumerate([(28, -14), (14, 16), (20, -22), (16, 20),
                                  (22, -10), (18, 12), (24, -18), (20, 14),
                                  (26, -6), (30, 0)]):
        px += dx
        py += dy
        pts.append((px, py))
    d.line(pts, fill=RED, width=2, joint="curve")
    d.text((x + 10, y + 6), "JUNIN  M6.7", font=font("sans_b", 11), fill=INK)


ARTS = {"cop31": art_cop31, "riyadh": art_riyadh, "peru": art_peru}


def main():
    with open(os.path.join(HERE, "stories.json")) as f:
        data = json.load(f)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    x0, x1 = M, W - M

    # ---- Masthead: small brand line, DATE as hero ----
    d.text((W // 2, 16), data["masthead"], font=font("sans_b", 13), fill=GREY, anchor="mt")
    d.text((W // 2, 52), data["date"], font=font("serif_b", 50), fill=INK, anchor="mm")
    d.text((W // 2, 92), data["counts"], font=font("sans_b", 14), fill=RED, anchor="mm")
    d.line([(x0, 108), (x1, 108)], fill=RULE, width=2)

    # ---- Data strip ----
    sy = 116
    d.rectangle([x0, sy, x1, sy + 30], fill=INK)
    strip = "  \u2022  ".join(data["strip"])
    fsize = 13
    while d.textlength(strip, font=font("mono_b", fsize)) > (x1 - x0 - 16) and fsize > 9:
        fsize -= 1
    d.text((W // 2, sy + 15), strip, font=font("mono_b", fsize),
           fill=(253, 246, 227), anchor="mm")

    # ---- 3 illustrated leads ----
    ly, lh = 156, 232
    cw = (x1 - x0 - 2 * 12) // 3
    for i, s in enumerate(data["leads"]):
        bx = x0 + i * (cw + 12)
        ARTS[s["art"]](d, bx, ly, cw, 96)
        y = ly + 104
        d.text((bx, y), f"0{i + 1}", font=font("mono_b", 12), fill=RED)
        d.text((bx + 26, y), s["kicker"], font=font("sans_b", 11), fill=RED)
        y += 16
        y = text_block(d, bx, y, wrap(d, s["headline"], font("serif_b", 18), cw, 2),
                       font("serif_b", 18), INK, 22)
        y = text_block(d, bx, y + 2, wrap(d, s["summary"], font("sans", 11), cw, 2),
                       font("sans", 11), DARKGREY, 14)
        d.text((bx, y + 4), s["figures"], font=font("mono_b", 10), fill=RED)
        y += 21
        d.text((bx, y), s["source"], font=font("sans_b", 9), fill=GREY)
        sw = d.textlength(s["source"], font=font("sans_b", 9))
        label_chip(d, bx + sw + 8, y - 2, s["label"])
        if i < 2:
            d.line([(bx + cw + 6, ly), (bx + cw + 6, ly + lh)], fill=(200, 190, 170), width=1)

    # ---- 10 numbered mid stories, 2 columns x 5 ----
    my = 402
    d.line([(x0, my - 8), (x1, my - 8)], fill=RULE, width=1)
    mid = data["mid"]
    colw = (x1 - x0 - 16) // 2
    rowh = 47
    for i, s in enumerate(mid):
        col, row = i % 2, i // 2
        bx = x0 + col * (colw + 16)
        by = my + row * rowh
        n = i + 4
        d.text((bx, by), f"{n:02d}", font=font("mono_b", 12), fill=RED)
        d.text((bx + 30, by), s["h"], font=font("sans_b", 12), fill=INK)
        sy2 = text_block(d, bx + 30, by + 16,
                         wrap(d, s["s"], font("sans", 10), colw - 30, 1),
                         font("sans", 10), DARKGREY, 13)
        d.text((bx + 30, sy2 + 1), s["src"], font=font("sans_b", 9), fill=GREY)
        sw = d.textlength(s["src"], font=font("sans_b", 9))
        label_chip(d, bx + 30 + sw + 8, sy2 - 1, s["label"])

    # ---- Numbered list 14-35 ----
    ly2 = 646
    d.line([(x0, ly2 - 6), (x1, ly2 - 6)], fill=RULE, width=1)
    d.text((x0, ly2 + 2), "THE REST OF THE DAY  \u2014  14 TO 35",
           font=font("sans_b", 12), fill=RED)
    lst = data["list"]
    assert len(lst) == 22, len(lst)
    colw2 = (x1 - x0 - 16) // 2
    for i, s in enumerate(lst):
        col, row = i % 2, i // 2
        bx = x0 + col * (colw2 + 16)
        by = ly2 + 22 + row * 20
        n = i + 14
        d.text((bx, by), f"{n:02d}", font=font("mono_b", 10), fill=RED)
        head = s["h"]
        tail = f"  \u00b7  {s['src']}  \u00b7  {s['label']}"
        maxw = colw2 - 30 - d.textlength(tail, font=font("sans", 9))
        while head and d.textlength(head, font=font("sans_b", 10)) > maxw:
            head = head[:-1]
        if head != s["h"]:
            head = head.rstrip() + "\u2026"
        d.text((bx + 28, by), head, font=font("sans_b", 10), fill=INK)
        tw = d.textlength(head, font=font("sans_b", 10))
        d.text((bx + 28 + tw, by), tail, font=font("sans", 9), fill=GREY)

    # ---- Map + DATE CHECK band ----
    by = 898
    d.line([(x0, by - 6), (x1, by - 6)], fill=RULE, width=2)
    map_x, map_y, map_w, map_h = x0, by + 2, 600, 104
    d.text((map_x, by + 2), "WHERE IT HAPPENED",
           font=font("sans_b", 11), fill=RED)
    mx0, my0 = map_x, by + 18
    d.rectangle([mx0, my0, mx0 + map_w, my0 + map_h - 16], fill=(226, 232, 238))
    for poly in CONTINENTS:
        pts = [(mx0 + (lon + 180) / 360 * map_w,
                my0 + (90 - lat) / 150 * (map_h - 16)) for lon, lat in poly]
        d.polygon(pts, fill=(190, 200, 185), outline=(150, 160, 150))
    for p in data["pins"]:
        lon, lat = p.get("dx", p["lon"]), p.get("dy", p["lat"])
        px = mx0 + (lon + 180) / 360 * map_w
        py = my0 + (90 - lat) / 150 * (map_h - 16)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py), str(p["n"]), font=font("sans_b", 8),
               fill=(255, 255, 255), anchor="mm")

    dx0 = map_x + map_w + 16
    dx1 = x1
    d.rectangle([dx0, by + 2, dx1, by + 106], outline=RED, width=2)
    d.text((dx0 + 8, by + 10), "DATE CHECK  \u2713  21 NOV 2026",
           font=font("sans_b", 11), fill=RED)
    cy = by + 28
    for ln in data["datecheck"]:
        cy = text_block(d, dx0 + 8, cy, wrap(d, ln, font("sans", 9), dx1 - dx0 - 16, 2),
                        font("sans", 9), DARKGREY, 12)
        cy += 3

    # ---- Footer sources ----
    d.text((x0, 1012), "Sources: " + data["sources"],
           font=font("sans", 9), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
