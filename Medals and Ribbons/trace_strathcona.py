"""Trace the Lord Strathcona portrait into src/strathcona_{ink,lit,aspect}.txt.

    python3 trace_strathcona.py strathcona_render.png

The source is a shaded bronze render, so the portrait is the same colour as
the field and cannot be keyed. What separates it is RELIEF: the struck areas
carry local highlights and shadows, the field does not. So the field is
estimated with a wide Gaussian (sigma 70 - a narrow one lets the portrait's
own large light areas bias it) and subtracted, leaving a high-pass where
shadow and highlight fall out as two masks.

Two things have to be cut out of those masks:

1. The legend. AGMINA DUCENS arcs across the top and touches the hair, so it
   cannot be split off by connected components. It is cut by radius, but only
   ABOVE the centre - the shoulders run out to 0.75R and must be left alone.
2. The lit field to the LEFT of the profile. The render lights the medal from
   that side, so the field there reads as highlight. It is the largest single
   component of the highlight mask and is dropped by size and position.

Nothing is traced as a silhouette. Closing the highlight fragments into one
bust gives a lumpy outline that shows as a ragged edge down the profile; the
highlight and shadow passes alone carry the portrait.
"""
import sys
import numpy as np
import potrace
from PIL import Image
from scipy import ndimage as ndi

src = sys.argv[1] if len(sys.argv) > 1 else "strathcona_render.png"
L = np.array(Image.open(src).convert("RGB")).astype(float).mean(2)

# fit the disc off the black surround: the widest bright row gives the centre
disc = L > 40
cy = int(np.argmax(disc.sum(1)))
row = np.nonzero(disc[cy])[0]
cx, R = (row.min() + row.max()) / 2.0, (row.max() - row.min()) / 2.0
Y, X = np.mgrid[0:L.shape[0], 0:L.shape[1]]
rad = np.hypot(X - cx, Y - cy) / R

hp = L - ndi.gaussian_filter(L, 70)
keep = rad < 0.76                              # inside the legend ring
cut = (Y < cy) & (rad > 0.605)                 # the legend arc, top only
dark = (hp < -14) & keep & ~cut
light = (hp > 18) & keep & ~cut

# drop the lit field left of the profile - the largest highlight component
lab, n = ndi.label(light)
sz = ndi.sum(light, lab, range(1, n + 1))
band = int(np.argmax(sz)) + 1
ys, xs = np.nonzero(lab == band)
if xs.mean() < cx and sz.max() > 20000:        # left of centre and large
    light = light & (lab != band)
else:
    print("WARNING: the largest highlight component does not look like the "
          "lit field; nothing dropped")

ys, xs = np.nonzero(dark | light)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
W, H = x1 - x0 + 1, y1 - y0 + 1
dark = dark[y0:y1 + 1, x0:x1 + 1]
light = light[y0:y1 + 1, x0:x1 + 1]


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


open("src/strathcona_ink.txt", "w").write(trace(dark, 16))
open("src/strathcona_lit.txt", "w").write(trace(light, 16))
open("src/strathcona_aspect.txt", "w").write("%.5f" % (H / W))
print("disc centre (%.0f, %d) R %.0f" % (cx, cy, R))
print("traced %d x %d px, aspect %.5f" % (W, H, H / W))
