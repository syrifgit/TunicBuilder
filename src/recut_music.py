"""unnamed_7 is a bad crop: the extractor merged several music level badges, their
captions and the Canada wordmark into one box. The badges sit in a left-to-right
line, so segment on alpha - split into horizontal bands, then split the badge band
into columns - and write each one out on its own."""
import _paths  # noqa: F401  - chdir to repo root, expose data/
import zipfile, io, os, sys, csv
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")

def runs(mask, gap):
    """Contiguous True runs in a 1-D bool list, merging gaps under `gap`."""
    out, start = [], None
    for i, v in enumerate(mask + [False]):
        if v and start is None: start = i
        elif not v and start is not None:
            if out and start - out[-1][1] <= gap: out[-1] = (out[-1][0], i)
            else: out.append((start, i))
            start = None
    return out

z = zipfile.ZipFile("rcac_badges.zip")
im = Image.open(io.BytesIO(z.read("unnamed_7.png"))).convert("RGBA")
a = im.split()[3].load()
W, H = im.size
print(f"unnamed_7.png  {W} x {H}")

rowfull = [any(a[x, y] > 24 for x in range(0, W, 3)) for y in range(H)]
bands = [b for b in runs(rowfull, H // 60) if b[1] - b[0] > H * 0.06]
print("horizontal bands:", [(y0, y1, y1 - y0) for y0, y1 in bands])

os.makedirs("art/recut", exist_ok=True)
found = []
for bi, (y0, y1) in enumerate(bands):
    colfull = [any(a[x, y] > 24 for y in range(y0, y1, 3)) for x in range(W)]
    cols = [c for c in runs(colfull, W // 90) if c[1] - c[0] > W * 0.02]
    for ci, (x0, x1) in enumerate(cols):
        sub = im.crop((x0, y0, x1, y1))
        bb = sub.getbbox()
        if not bb: continue
        sub = sub.crop(bb)
        asp = sub.width / sub.height
        square = 0.85 < asp < 1.18 and sub.width > W * 0.05
        found.append((bi, ci, x0, sub.width, sub.height, round(asp, 3), square))
        if square:
            sub.save(f"art/recut/band{bi}_col{ci}.png")

print(f"\n{'band':>4} {'col':>4} {'x0':>6} {'w':>5} {'h':>5} {'aspect':>7}  square?")
for r in found:
    print(f"{r[0]:>4} {r[1]:>4} {r[2]:>6} {r[3]:>5} {r[4]:>5} {r[5]:>7}  {'YES' if r[6] else '-'}")
print("\nsquare crops written:", sorted(os.listdir("art/recut")))
