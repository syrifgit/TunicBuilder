"""Trace the heraldic eagle into src/afa_bird_{sil,ink,aspect}.txt.

    python3 trace_bird.py eagle.png

The source is RGB with the transparency checkerboard baked in, so the
background is keyed off saturation rather than alpha. The black outlines are
as unsaturated as the checker, so they need the luminance clause as well:

    bird = (saturation > 40) OR (luminance < 140)

Two masks come out of that. The silhouette is the largest connected component
with holes filled. The ink is the dark line work inside it, dilated 3 px first
because the feather lines are 1 to 3 px in the source and would not survive
the roughly 4x downscale to medal size.

NOTE: potrace.Bitmap treats LOW values as foreground, so both masks are
inverted going in. Tracing them the obvious way returns the complement, which
renders as a solid field with the artwork knocked out of it.
"""
import sys
import numpy as np
import potrace
from PIL import Image
from scipy import ndimage as ndi

src = sys.argv[1] if len(sys.argv) > 1 else "eagle.png"
a = np.array(Image.open(src).convert("RGB")).astype(int)
sat = a.max(2) - a.min(2)
lum = a.mean(2)

badge = (sat > 40) | (lum < 140)
lab, n = ndi.label(badge)
big = int(np.argmax(ndi.sum(badge, lab, range(1, n + 1)))) + 1
sil = ndi.binary_fill_holes(lab == big)
ink = (lum < 110) & sil

ys, xs = np.nonzero(sil)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
W, H = x1 - x0 + 1, y1 - y0 + 1
sil = sil[y0:y1 + 1, x0:x1 + 1]
ink = ndi.binary_dilation(ink[y0:y1 + 1, x0:x1 + 1], np.ones((3, 3), bool))


def trace(mask, turdsize):
    path = potrace.Bitmap(~mask.astype(bool)).trace(
        turdsize=turdsize, alphamax=1.0, opttolerance=0.2)
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


open("src/afa_bird_sil.txt", "w").write(trace(sil, 24))
open("src/afa_bird_ink.txt", "w").write(trace(ink, 10))
open("src/afa_bird_aspect.txt", "w").write("%.5f" % (H / W))
print("traced %d x %d px, aspect %.5f" % (W, H, H / W))
