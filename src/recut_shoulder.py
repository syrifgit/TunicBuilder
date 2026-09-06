"""Items 15 and 17 are the same bad-crop problem as unnamed_7: each merges a corps
name title with the RCAC sleeve badge below it. Split them, and compare the two
worked examples against each other."""
import _paths  # noqa: F401  - chdir to repo root, expose data/
import zipfile, io, os, sys, unicodedata, re
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
z = zipfile.ZipFile("rcac_badges.zip")
Z = {unicodedata.normalize("NFC", n): n for n in z.namelist()}
def get(s):
    n = unicodedata.normalize("NFC", s + ".png")
    k = Z.get(n) or next(v for kk, v in Z.items()
        if re.sub(r"[^a-z0-9_]","",kk.lower()) == re.sub(r"[^a-z0-9_]","",n.lower()))
    im = Image.open(io.BytesIO(z.read(k))).convert("RGBA"); return im.crop(im.getbbox())

def runs(mask, gap):
    out, start = [], None
    for i, v in enumerate(mask + [False]):
        if v and start is None: start = i
        elif not v and start is not None:
            if out and start - out[-1][1] <= gap: out[-1] = (out[-1][0], i)
            else: out.append((start, i))
            start = None
    return out

PT = lambda p, dpi=600: p / dpi * 72
os.makedirs("art/recut", exist_ok=True)
res = {}
for slug, corps in [("da_vi_d_d_e_f_al_ar_de","Lord Westminster 2990"),
                    ("unnamed_5","St-David-de-Falardeau 2864")]:
    im = get(slug); a = im.split()[3].load(); W, H = im.size
    rowfull = [any(a[x, y] > 24 for x in range(0, W, 2)) for y in range(H)]
    bands = [b for b in runs(rowfull, H // 40) if b[1]-b[0] > H*0.08]
    print(f"\n{corps}   crop {W}x{H}px = {PT(W):.1f}x{PT(H):.1f} pt   bands {bands}")
    parts = []
    for bi, (y0, y1) in enumerate(bands):
        sub = im.crop((0, y0, W, y1)); sub = sub.crop(sub.getbbox())
        name = ["corps_name_title","rcac_badge"][bi] if len(bands) == 2 else f"part{bi}"
        sub.save(f"art/recut/{name}__{slug}.png")
        parts.append((name, sub.width, sub.height))
        print(f"   {name:18} {sub.width:4} x {sub.height:4} px   "
              f"{PT(sub.width):6.2f} x {PT(sub.height):6.2f} pt   aspect {sub.width/sub.height:.3f}")
    res[corps] = dict(parts=parts, W=W)

print("\n--- proportional relationship (both examples) ---")
for corps, d in res.items():
    p = dict((n,(w,h)) for n,w,h in d["parts"])
    if "corps_name_title" in p and "rcac_badge" in p:
        tw, th = p["corps_name_title"]; cw, ch = p["rcac_badge"]
        print(f"{corps:30} title {tw/ch:5.3f} x circle dia wide, {th/ch:5.3f} x tall; "
              f"circle aspect {cw/ch:.3f}")

print("\n--- if you measure the RCAC circle diameter D (cm), everything follows ---")
p = dict((n,(w,h)) for n,w,h in res["Lord Westminster 2990"]["parts"])
tw, th = p["corps_name_title"]; cw, ch = p["rcac_badge"]
for D in (5.0, 5.5, 6.0, 6.5, 7.0):
    print(f"   D = {D:.1f} cm  ->  title {tw/ch*D:5.2f} x {th/ch*D:4.2f} cm")
