"""Recover the Physical Fitness badges from the source poster.

extract_badges.py missed the whole PHYSICAL FITNESS block. The badges sit on the
bottom row of the middle/right section, immediately left of the music circles.
Render that strip at the same 600 dpi the original pipeline used, then segment on
alpha (the poster background is unpainted, so alpha is a clean mask).

The four crops and their order - bronze, silver, gold, excellence - are
confirmed correct by Lt Beal. Excellence was the one in doubt, since it is the
last in the strip and a mis-segmentation would show up there first."""
import _paths  # noqa: F401  - chdir to repo root, expose data/
import pymupdf, io, os, sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")

PDF   = "ACRCCP750DA003.pdf"
DPI   = 600
STRIP = pymupdf.Rect(700, 2290, 1190, 2385)     # circles only, above the captions
NAMES = ["fit_bronze", "fit_silver", "fit_gold", "fit_excellence"]
OUT   = "art/recut"


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
pix = page.get_pixmap(clip=STRIP, dpi=DPI, alpha=True)
im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")
W, H = im.size
a = im.split()[3].load()
scale = DPI / 72.0
print(f"strip {STRIP}  ->  {W} x {H} px at {DPI} dpi")

colfull = [any(a[x, y] > 24 for y in range(0, H, 3)) for x in range(W)]
cols = [c for c in runs(colfull, int(W * 0.01)) if c[1] - c[0] > W * 0.04]
print(f"{len(cols)} columns found\n")

os.makedirs(OUT, exist_ok=True)
print(f"{'name':16} {'px':>11} {'pt':>13} {'aspect':>7}   at 3.0 cm the art is")
for i, (x0, x1) in enumerate(cols):
    sub = im.crop((x0, 0, x1, H))
    bb = sub.getbbox()
    if not bb:
        continue
    sub = sub.crop(bb)
    name = NAMES[i] if i < len(NAMES) else f"fit_extra{i}"
    sub.save(f"{OUT}/{name}.png")
    wpt, hpt = sub.width / scale, sub.height / scale
    asp = sub.width / sub.height
    print(f"{name:16} {sub.width:4}x{sub.height:<4} {wpt:6.2f}x{hpt:<6.2f} {asp:7.3f}"
          f"   {3.0:.2f} x {3.0/asp:.2f} cm")

if len(cols) != 4:
    print(f"\nWARNING: expected 4 fitness badges, segmented {len(cols)}. Check STRIP.")
