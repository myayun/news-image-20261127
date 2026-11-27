#!/usr/bin/env python3
"""Build the news-image-20261127 entry image (1024x1024 PNG).

Facts come ONLY from NEWS_BRIEF.md in this directory. Deterministic:
fixed fonts, no timestamps, no randomness. Pillow only, no network.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ILLUS = os.path.join(BASE, "assets", "illustrations")
OUT = os.path.join(BASE, "entry_v1.png")

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SANS = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")

W = H = 1024
NAVY = (11, 36, 71)
NAVY_LIGHT = (159, 193, 232)
RED = (176, 58, 46)
GREEN = (30, 132, 73)
INK = (26, 26, 26)
GRAY = (68, 68, 68)
PANEL = (244, 246, 249)
STAT_BG = (253, 236, 234)
RULE = (213, 219, 219)
WHITE = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def crop_to(img, tw, th, fx=0.5, fy=0.5):
    """Crop img to aspect tw:th around focus point (fx, fy), resize to (tw, th)."""
    iw, ih = img.size
    target = tw / th
    if iw / ih > target:  # too wide -> crop width
        cw = int(ih * target)
        x0 = int((iw - cw) * fx)
        box = (x0, 0, x0 + cw, ih)
    else:  # too tall -> crop height
        ch = int(iw / target)
        y0 = int((ih - ch) * fy)
        box = (0, y0, iw, y0 + ch)
    return img.crop(box).resize((tw, th), Image.LANCZOS)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading, align="left", width=None):
    for ln in lines:
        if align == "center" and width:
            tw = draw.textlength(ln, font=fnt)
            draw.text((x + (width - tw) / 2, y), ln, font=fnt, fill=fill)
        elif align == "right" and width:
            tw = draw.textlength(ln, font=fnt)
            draw.text((x + width - tw, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---------- Masthead ----------
    d.rectangle([0, 0, W, 94], fill=NAVY)
    d.rectangle([0, 94, W, 98], fill=RED)
    f_date = font(SANS_B, 42)
    d.text((24, 24), "Friday 27 November 2026", font=f_date, fill=WHITE)
    f_tag = font(SANS_B, 20)
    tag = "WORLD NEWS IN ONE IMAGE"
    tw = d.textlength(tag, font=f_tag)
    d.text((1000 - tw, 36), tag, font=f_tag, fill=NAVY_LIGHT)

    # ---------- Lead image ----------
    lead = Image.open(os.path.join(ILLUS, "lead.png")).convert("RGB")
    lead_c = crop_to(lead, 676, 250, fx=0.18, fy=0.5)
    img.paste(lead_c, (24, 110))

    # ---------- Lead headline ----------
    f_head = font(SANS_B, 39)
    y = 368
    for ln in ["NVIDIA FREEZES AI CHIPS", "TO SOUTHEAST ASIA"]:
        d.text((24, y), ln, font=f_head, fill=INK)
        y += 46

    # ---------- Deck ----------
    f_deck = font(SANS, 17)
    deck = ("Nvidia told Dell and Supermicro to stop shipping AI servers to "
            "Malaysia, Singapore, Thailand and Indonesia under new US export "
            "controls. (FT \u2014 26 NOV)")
    lines = wrap(d, deck, f_deck, 676)
    y = draw_lines(d, lines, 24, 462, f_deck, GRAY, 22)

    # ---------- Stat blocks ----------
    stats = [("4", "COUNTRIES HALTED"), ("19 NOV", "RULE LIVE"),
             ("90 DAYS", "TO LICENCE"), ("RM123.5B", "AT STAKE")]
    f_num = font(SANS_B, 29)
    f_lab = font(SANS_B, 13)
    sy, sh, sw, gap = 540, 78, 160, 12
    for i, (num, lab) in enumerate(stats):
        x = 24 + i * (sw + gap)
        d.rectangle([x, sy, x + sw, sy + sh], fill=STAT_BG)
        d.rectangle([x, sy, x + sw, sy + 4], fill=RED)
        nw = d.textlength(num, font=f_num)
        d.text((x + (sw - nw) / 2, sy + 10), num, font=f_num, fill=RED)
        lab_lines = wrap(d, lab, f_lab, sw - 8)
        draw_lines(d, lab_lines, x, sy + 46, f_lab, INK, 15,
                   align="center", width=sw)

    # ---------- Sidebar: THE DAY IN BRIEF ----------
    sx, swd = 712, 288
    d.rectangle([sx, 110, sx + swd, 624], fill=PANEL)
    d.rectangle([sx, 110, sx + swd, 144], fill=NAVY)
    f_side_t = font(SANS_B, 17)
    t = "THE DAY IN BRIEF"
    tw = d.textlength(t, font=f_side_t)
    d.text((sx + (swd - tw) / 2, 118), t, font=f_side_t, fill=WHITE)

    briefs = [
        "China and Brazil lead the pushback against Trump's tariffs; "
        "Beijing signals retaliation.",
        "EU leaders fail to agree a \u20ac45 billion Ukraine loan for 2027; "
        "decision pushed to 17\u201318 Dec.",
        "UK net migration falls to 77,000 \u2014 the lowest in three decades.",
        "Saudi-led coalition destroys a Houthi missile platform after an "
        "attack on an Aramco facility.",
        "Storms snarl US Thanksgiving travel: 6,000+ flights delayed, "
        "Macy's parade postponed.",
        "Bank of Korea raises rates and lifts its GDP growth forecast.",
        "Russia sends a humanoid robot to the ISS to assist astronauts.",
        "Trump says he pressed Putin to pull back \"all military "
        "aggression\" in Europe.",
    ]
    f_brief = font(SANS, 13.5)
    by = 154
    for i, b in enumerate(briefs):
        bl = wrap(d, b, f_brief, swd - 20)
        by = draw_lines(d, bl, sx + 10, by, f_brief, INK, 16.5)
        by += 5
        if i < len(briefs) - 1:
            d.line([sx + 10, by, sx + swd - 10, by], fill=RULE, width=1)
            by += 6
    assert by <= 624, f"sidebar overflow: ends at {by}"

    # ---------- Hero cards ----------
    heroes = [
        ("hero-ukraine.png", "KYIV BRACES FOR NEW MASS STRIKE",
         "Zelenskyy warns of a new mass strike 'in the coming days'; "
         "missiles hit Kyiv, 7 wounded. Ukraine says a laser downed a "
         "drone \u2014 a world first.",
         "REUTERS \u2014 27 NOV", 0.42),
        ("hero-mine.png", "13 DEAD IN FLOODED GOLD MINE",
         "Unauthorised gold mine floods in Pongkor, West Java: 13 dead, "
         "13 missing. 325 rescuers search two waterlogged shafts; "
         "rescue continues.",
         "BBC \u2014 27 NOV", 0.62),
        ("hero-markets.png", "CHIPS LEAD BLACK FRIDAY REBOUND",
         "Chip stocks rally over Thanksgiving as tariff fears ease; US "
         "futures higher into Friday's shortened session (NYSE closes "
         "1pm ET).",
         "MARKETS \u2014 27 NOV", 0.30),
    ]
    f_hh = font(SANS_B, 19)
    f_hs = font(SANS, 13.5)
    f_src = font(SANS_B, 11)
    hy, cw, ch_img = 636, 320, 124
    for i, (fn, head, summ, src, fy) in enumerate(heroes):
        x = 24 + i * (cw + 8)
        him = Image.open(os.path.join(ILLUS, fn)).convert("RGB")
        img.paste(crop_to(him, cw, ch_img, fx=0.5, fy=fy), (x, hy))
        yy = hy + ch_img + 8
        hl = wrap(d, head, f_hh, cw - 4)
        yy = draw_lines(d, hl, x + 2, yy, f_hh, INK, 22)
        yy += 2
        sl = wrap(d, summ, f_hs, cw - 4)
        yy = draw_lines(d, sl, x + 2, yy, f_hs, GRAY, 16.5)
        yy += 3
        d.text((x + 2, yy), src, font=f_src, fill=RED)

    # ---------- Markets strip ----------
    my = 900
    d.rectangle([0, my, W, my + 68], fill=NAVY)
    f_mt = font(SANS_B, 15)
    d.text((24, my + 7), "FRIDAY \u2014 FUTURES & OVERSEAS", font=f_mt, fill=WHITE)
    figures = [
        ("S&P 500 FUT", "+0.7%"), ("NASDAQ FUT", "+0.7%"),
        ("TAIWAN", "+2.5%"), ("STOXX 600", "+1.8%"),
        ("BRENT $96.57", "+2.1%"), ("WTI $84.91", "+1.5%"),
        ("GOLD $3,642", "+3.0%"), ("BITCOIN $61,502", "+1.9%"),
    ]
    f_fn = font(SANS_B, 13.5)
    f_fv = font(SANS_B, 13.5)
    cell_w = 976 // 4
    for i, (name, val) in enumerate(figures):
        cx = 24 + (i % 4) * cell_w
        cy = my + 30 + (i // 4) * 19
        d.text((cx, cy), name, font=f_fn, fill=NAVY_LIGHT)
        nw = d.textlength(name + " ", font=f_fn)
        d.text((cx + nw, cy), val, font=f_fv, fill=(110, 231, 160))

    # ---------- Footer ----------
    f_foot = font(SANS, 14)
    foot = "The world's news of Friday 27 November 2026."
    tw = d.textlength(foot, font=f_foot)
    d.text(((W - tw) / 2, 978), foot, font=f_foot, fill=GRAY)

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
