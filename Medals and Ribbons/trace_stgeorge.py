"""Trace the St George figure into src/stgeorge_{sil,ink,aspect}.txt.

    python3 trace_stgeorge.py stgeorge_render.png

Easier than the Strathcona portrait: this render is bright silver on a dark
mirror field, so the figure keys straight off luminance. The work is in the
two cuts.

1. The legend. PRO MERITO and ORDER OF ST. GEORGE are struck in the same
   bright metal as the figure, so a plain luminance key picks them up. They
   sit at about 0.80 of the field radius, the figure inside 0.72, so a cut at
   0.76R separates them with room to spare. The disc is fitted from the dark
   field itself (largest mid-luminance component, holes filled) because the
   supplied render is cropped and the rim is not fully in frame.

2. Components. At a threshold that keeps the figure's shaded areas the whole
   thing is one component, but the raised sword, the cape tip and the dragon's
   wing sit close to breaking off. Everything at or above 120 px inside the
   radius cut is kept, rather than just the largest component, which loses
   them at tighter thresholds.

The ink is a high-pass within the figure, dilated 3 px, and it carries the
engraving: reins, armour plates, mane, the sword driven into the dragon, and
the dragon's scales and wing membrane.
"""
import sys
import numpy as np
import potrace
from PIL import Image
from scipy import ndimage as ndi

src = sys.argv[1] if len(sys.argv) > 1 else "stgeorge_render.png"
L = np.array(Image.open(src).convert("RGB")).astype(float).mean(2)

# fit the disc off the dark mirror field, not the rim, which may be cropped
field = (L > 25) & (L < 95)
lab, n = ndi.label(field)
big = int(np.argmax(ndi.sum(field, lab, range(1, n + 1)))) + 1
inner = ndi.binary_fill_holes(lab == big)
ys, xs = np.nonzero(inner)
cx, cy = (xs.min() + xs.max()) / 2.0, (ys.min() + ys.max()) / 2.0
R = (inner.sum() / np.pi) ** 0.5
Y, X = np.mgrid[0:L.shape[0], 0:L.shape[1]]
rad = np.hypot(X - cx, Y - cy) / R

bright = (L > 82) & (rad < 0.76)
lab, n = ndi.label(ndi.binary_closing(bright, np.ones((3, 3), bool)))
sz = ndi.sum(bright, lab, range(1, n + 1))
fig = np.isin(lab, [i + 1 for i in range(n) if sz[i] >= 120])

ink = ndi.binary_dilation((L - ndi.gaussian_filter(L, 14)) < -11, np.ones((3, 3), bool)) & fig

ys, xs = np.nonzero(fig)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
W, H = x1 - x0 + 1, y1 - y0 + 1
fig = fig[y0:y1 + 1, x0:x1 + 1]
ink = ink[y0:y1 + 1, x0:x1 + 1]


def trace(mask, turdsize):
    # potrace.Bitmap treats LOW values as foreground, hence the invert
    path = potrace.Bitmap(~mask.astype(bool)).trace(
        turdsize=turdsize, alphamax=1.0, opttolerance=0.22)
    out = []
    for curve in path:
        s = curve.start_point
        d = ["M%.4f,%.4f" % (s.x / W, s.y / W)]
        for seg in curve:
            if seg.is_corner:
                d.append("L%.4f,%.4f" % (seg.c.x / W, seg.c.y / W))
                d.append("L%.4f,%.4f" % (seg.end_point.x / W,
                                         seg.end_point.y / W))
            else:
                d.append("C%.4f,%.4f %.4f,%.4f %.4f,%.4f"
                         % (seg.c1.x / W, seg.c1.y / W,
                            seg.c2.x / W, seg.c2.y / W,
                            seg.end_point.x / W, seg.end_point.y / W))
        d.append("Z")
        out.append(" ".join(d))
    return " ".join(out)


open("src/stgeorge_sil.txt", "w").write(trace(fig, 24))
open("src/stgeorge_ink.txt", "w").write(trace(ink, 10))
open("src/stgeorge_aspect.txt", "w").write("%.5f" % (H / W))
print("disc centre (%.0f, %.0f) R %.0f" % (cx, cy, R))
print("traced %d x %d px, aspect %.5f" % (W, H, H / W))
