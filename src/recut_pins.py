"""Recover the competition and expedition pins from the source poster.

extract_badges.py clusters VECTOR drawing objects. These pins are photographs of
metal, so they are rasters and the extractor never saw them. Same fix as the fitness
block: render the strip and segment on alpha, because the page background is unpainted.

Three rows:
  MARKSMANSHIP CHAMPIONSHIPS  Zone / Provincial / National / Vamplew & Clement Tremblay
  BIATHLON CHAMPIONSHIPS      Zone / Provincial / National / Myriam Bedard, Nikki Keddie
                              & Jean-Philippe Le Guellec
  EXPEDITIONS                 Regional / National-International
  (summer training row)       RCAC National Rifle Team / LGen C.H. Belzile Trophy

The workbook calls the fourth item in each championship row "National Winners"; the
poster names the actual award. Both names are recorded in data/labels.py.
"""
import io
import os
import sys

import _paths  # noqa: F401  - chdir to repo root, expose data/
import pymupdf
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

PDF = "ACRCCP750DA003.pdf"
DPI = 600
OUT = "art/recut"

ROWS = [
    ("marksmanship", pymupdf.Rect(80, 2032, 650, 2098),
     ["comp_mk_zone", "comp_mk_prov", "comp_mk_nat", "comp_mk_winner"]),
    ("biathlon", pymupdf.Rect(80, 2196, 650, 2262),
     ["comp_bi_zone", "comp_bi_prov", "comp_bi_nat", "comp_bi_winner"]),
    # the caption text sits on the same line as these two, so take each one alone
    # National Rifle Team pins sit in the summer-training bottom row, not with the
    # other pins, so they need their own strips
    ("rifle team", pymupdf.Rect(392, 1828, 545, 1886), ["pin_rifle_team"]),
    ("belzile trophy", pymupdf.Rect(578, 1820, 684, 1896), ["pin_belzile"]),
    ("expedition regional", pymupdf.Rect(112, 2358, 188, 2426), ["exped_regional"]),
    ("expedition national", pymupdf.Rect(356, 2358, 432, 2426), ["exped_national"]),
]


def runs(mask, gap):
    out, start = [], None
    for i, v in enumerate(mask + [False]):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if out and start - out[-1][1] <= gap:
                out[-1] = (out[-1][0], i)
            else:
                out.append((start, i))
            start = None
    return out


doc = pymupdf.open(PDF)
page = doc[0]
os.makedirs(OUT, exist_ok=True)
scale = DPI / 72.0

print(f"{'name':16} {'px':>11} {'pt':>13} {'aspect':>7}   at 2.54 cm")
for label, strip, names in ROWS:
    pix = page.get_pixmap(clip=strip, dpi=DPI, alpha=True)
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")
    W, H = im.size
    a = im.split()[3].load()
    colfull = [any(a[x, y] > 24 for y in range(0, H, 3)) for x in range(W)]
    cols = runs(colfull, int(W * 0.012))
    # drop slivers: a stray caption glyph clipping into the strip is far narrower
    # than a pin, so keep only columns at least 40% as wide as the widest one
    widest = max((c[1] - c[0] for c in cols), default=0)
    cols = [c for c in cols if c[1] - c[0] >= widest * 0.4]
    print(f"\n-- {label}: {len(cols)} of {len(names)} expected --")
    for i, (x0, x1) in enumerate(cols):
        sub = im.crop((x0, 0, x1, H))
        bb = sub.getbbox()
        if not bb:
            continue
        sub = sub.crop(bb)
        name = names[i] if i < len(names) else f"{label}_extra{i}"
        sub.save(f"{OUT}/{name}.png")
        asp = sub.width / sub.height
        print(f"{name:16} {sub.width:4}x{sub.height:<4} "
              f"{sub.width/scale:6.2f}x{sub.height/scale:<6.2f} {asp:7.3f}"
              f"   {2.54:.2f} x {2.54/asp:.2f} cm")
    if len(cols) != len(names):
        print(f"   WARNING: expected {len(names)} pins, segmented {len(cols)}. Check the strip.")
