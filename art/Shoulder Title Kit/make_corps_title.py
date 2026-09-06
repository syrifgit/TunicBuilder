#!/usr/bin/env python3
"""Generate a CJCR army cadet corps shoulder title matching the national artwork.

Geometry, colours and type size were reverse-engineered from the issued
1721x542 corps_name_title artwork (St-David-de-Falardeau 2864 / Lord
Westminster 2990). Digits fit the source to ~14% edge residual, letters ~31%
(all of it antialiasing on glyph edges), so output is visually indistinguishable.

Usage:
    python3 make_corps_title.py "Fredericton" 242 out.png
"""
import math
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ---- constants measured off the issued artwork -----------------------------
CANVAS = (1721, 542)
FONT = "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheros-bold.otf"
GOLD = (247, 183, 44)
TEAL = (8, 68, 61)

CX, CY = 859.73, 1880.4     # common arc centre for plate and both text lines
XOFF = -16.0                # text block sits 16 px left of the plate axis
TOP = dict(size=146.96, R=1691.28)   # baseline radius, top line
BOT = dict(size=148.29, R=1526.65)   # baseline radius, number line
MAXW = 1400.0               # max advance width on the top arc before shrinking
# ---------------------------------------------------------------------------


def render_arc(text, size, R, ss=6):
    """Rotate each glyph about (CX, CY) so its baseline sits tangent to R."""
    W, H = CANVAS
    font = ImageFont.truetype(FONT, int(round(size * ss)))
    adv = [font.getlength(c) / ss for c in text]
    total = sum(adv)
    ang, run = [], -total / 2.0 + XOFF
    for a in adv:
        ang.append(math.degrees((run + a / 2.0) / R))
        run += a

    big = Image.new("L", (W * ss, H * ss), 0)
    tile = int(size * ss * 3)
    for ch, th in zip(text, ang):
        if ch == " ":
            continue
        t = Image.new("L", (tile, tile), 0)
        ImageDraw.Draw(t).text((tile / 2, tile / 2), ch, font=font,
                               fill=255, anchor="ms")
        t = t.rotate(-th, resample=Image.BICUBIC)
        r = math.radians(th)
        ox = int(round((CX + R * math.sin(r)) * ss - tile / 2))
        oy = int(round((CY - R * math.cos(r)) * ss - tile / 2))
        big.paste(t, (ox, oy), t)

    a = np.zeros((H, W, 4), np.uint8)
    a[:, :, 0], a[:, :, 1], a[:, :, 2] = GOLD
    a[:, :, 3] = np.array(big.resize((W, H), Image.LANCZOS))
    return Image.fromarray(a)


def fit_size(text, size, R, ss=6):
    """Shrink the top line if it would run past the plate shoulders."""
    font = ImageFont.truetype(FONT, int(round(size * ss)))
    w = sum(font.getlength(c) for c in text) / ss
    return size * MAXW / w if w > MAXW else size


def build(name, number, plate_path="blank_plate.png"):
    out = Image.open(plate_path).convert("RGBA")
    top = dict(TOP)
    top["size"] = fit_size(name, **TOP)
    out.alpha_composite(render_arc(name, **top))
    out.alpha_composite(render_arc(str(number), **BOT))
    return out


if __name__ == "__main__":
    name, number, dest = sys.argv[1], sys.argv[2], sys.argv[3]
    build(name, number).save(dest)
    print("wrote", dest)
