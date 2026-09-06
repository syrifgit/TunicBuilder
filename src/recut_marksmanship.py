"""Split the marksmanship assembly into its two sewn pieces.

Levels 1-3 are crossed rifles with a separate numeral tab 0.5 cm below them - two
pieces, sewn separately, so the guide needs two rows and the drawing needs the gap
shown. Distinguished is a single piece (rifles fused with a crown) and is left alone."""
import _paths  # noqa: F401  - chdir to repo root, expose data/
import zipfile, io, os, sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")

OUT = "art/recut"
LEVELS = {"marksman": "mk_1", "first_class_marksman": "mk_2", "expert_marksman": "mk_3"}


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


z = zipfile.ZipFile("rcac_badges.zip")
os.makedirs(OUT, exist_ok=True)
print(f"{'level':10} {'piece':9} {'px':>11} {'aspect':>7}   measured aspect")
for slug, key in LEVELS.items():
    im = Image.open(io.BytesIO(z.read(slug + ".png"))).convert("RGBA")
    im = im.crop(im.getbbox())
    a = im.split()[3].load()
    W, H = im.size
    rowfull = [any(a[x, y] > 24 for x in range(0, W, 2)) for y in range(H)]
    bands = [b for b in runs(rowfull, 2) if b[1] - b[0] > H * 0.04]
    if len(bands) != 2:
        print(f"{slug:10} WARNING: {len(bands)} bands, expected 2 -> {bands}")
        continue
    # top band is the rifles, bottom band the numeral tab
    for (y0, y1), piece, want in zip(bands, ("rifles", "numeral"), (5.5/5.08, 3.81/1.905)):
        sub = im.crop((0, y0, W, y1))
        sub = sub.crop(sub.getbbox())
        sub.save(f"{OUT}/{key}_{piece}.png")
        print(f"{key:10} {piece:9} {sub.width:4}x{sub.height:<4} "
              f"{sub.width/sub.height:7.3f}   {want:.3f}")
    gap_px = bands[1][0] - bands[0][1]
    rifles_h = bands[0][1] - bands[0][0]
    # rifles are 5.08 cm tall, so the drawn gap converts through that
    print(f"{'':10} gap between them: {gap_px} px = "
          f"{gap_px / rifles_h * 5.08:.2f} cm (rules say 0.50)")
