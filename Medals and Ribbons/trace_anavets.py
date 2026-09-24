"""Trace the ANAVETS centre into src/anavets_{metal,white,red,blue,ink}.txt.

    python3 trace_anavets.py anavets_render.png

Five passes, because this is the only coloured face in the set: the crown and
maple sprays in silver, the shield's white areas, the red and blue enamel, and
the engraved line work over all of it.

The disc is fitted by least squares on the medal's own outline below the
suspension ring (residual ~1.6 px), not from a bounding box - the ring would
drag the centre up by 20 px.

Three things this had to work around:

1. **The silver field is stippled.** A high-pass picks up the matte texture
   everywhere, so a relief mask is not selective on its own. The line work
   survives as long connected curves while the stipple breaks into hundreds of
   specks, so components under 120 px are dropped.
2. **The inner ring closes the fill.** The circle at 0.58R that separates the
   centre from the legend band is part of the outline, so filling the outline
   encloses the whole face and returns one 212k px blob. Cutting at 0.572R -
   a radius histogram puts the ring at 0.58 and the sprays end by 0.55 - lets
   the crown and each spray leaf fill separately.
3. **The shield cannot be filled from its enamel.** Its white areas are open
   to the shield's silver border rather than enclosed by red and blue, so
   filling holes in the enamel leaves them out. A heater shield is convex, so
   the convex hull of the enamel recovers the whole shield, and the white
   areas are the hull minus the enamel.

The ink excludes the shield's interior, eroded 4 px, because the enamel is
darker than the field and would otherwise trace as line work and paint over
itself.
"""
import sys
import numpy as np
import potrace
from PIL import Image
from scipy import ndimage as ndi
from skimage.morphology import convex_hull_image

src = sys.argv[1] if len(sys.argv) > 1 else "anavets_render.png"
a = np.array(Image.open(src).convert("RGB")).astype(float)
L = a.mean(2)
Rr, G, B = a[..., 0], a[..., 1], a[..., 2]


def disk(r):
    y, x = np.mgrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r


# --- fit the disc: least squares on the outline, ignoring the ring ---------
med = ndi.binary_fill_holes(~((L > 238) & ((a.max(2) - a.min(2)) < 18)))
lab, n = ndi.label(med)
med = ndi.binary_fill_holes(lab == int(np.argmax(ndi.sum(med, lab, range(1, n + 1)))) + 1)
med[:120, :] = False
edge = med & ~ndi.binary_erosion(med, np.ones((3, 3), bool))
ys, xs = np.nonzero(edge)
k = ys > 150
x, y = xs[k].astype(float), ys[k].astype(float)
sol, *_ = np.linalg.lstsq(np.c_[2 * x, 2 * y, np.ones(len(x))],
                          x ** 2 + y ** 2, rcond=None)
cx, cy = sol[0], sol[1]
R = np.sqrt(sol[2] + cx * cx + cy * cy)
rms = (np.hypot(x - cx, y - cy) - R).std()

Y, X = np.mgrid[0:L.shape[0], 0:L.shape[1]]
rad = np.hypot(X - cx, Y - cy) / R
reg = rad < 0.572                      # inside the ring at 0.58R

# --- the five masks --------------------------------------------------------
red = (Rr > 110) & (Rr - G > 45) & (Rr - B > 35) & reg
blue = (B > 75) & (B - Rr > 25) & (B - G > 20) & reg
shield = convex_hull_image(red | blue)          # a heater shield is convex
white = shield & ~red & ~blue

outline = ((L - ndi.gaussian_filter(L, 26)) < -16) & reg
filled = ndi.binary_fill_holes(ndi.binary_closing(outline, disk(4)))
lab, n = ndi.label(filled)
sz = ndi.sum(filled, lab, range(1, n + 1))
metal = np.isin(lab, [i + 1 for i in range(n) if sz[i] >= 400]) & ~shield

ink = outline & ~ndi.binary_erosion(shield, disk(4))
lab, n = ndi.label(ink)
sz = ndi.sum(ink, lab, range(1, n + 1))
ink = np.isin(lab, [i + 1 for i in range(n) if sz[i] >= 120])   # drop stipple

# --- trace -----------------------------------------------------------------
allm = metal | white | red | blue | ink
ys, xs = np.nonzero(allm)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
W, H = x1 - x0 + 1, y1 - y0 + 1
crop = lambda m: m[y0:y1 + 1, x0:x1 + 1]


def trace(mask, turdsize):
    # potrace.Bitmap treats LOW values as foreground, hence the invert
    path = potrace.Bitmap(~crop(mask).astype(bool)).trace(
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


for name, mask, turd in (("metal", metal, 30), ("white", white, 30),
                         ("red", red, 20), ("blue", blue, 20),
                         ("ink", ink, 12)):
    open("src/anavets_%s.txt" % name, "w").write(trace(mask, turd))
open("src/anavets_aspect.txt", "w").write("%.5f" % (H / W))

w_frac = W / (2.0 * R)
cy_k = ((y0 + y1) / 2.0 - cy) / R
open("src/anavets_place.txt", "w").write("%.5f %.5f" % (w_frac, cy_k))
print("disc fit: centre (%.1f, %.1f) R %.1f, residual rms %.2f px"
      % (cx, cy, R, rms))
print("traced %d x %d px, aspect %.5f" % (W, H, H / W))
print("placement: width %.4f of the disc diameter, centre %+.4f R"
      % (w_frac, cy_k))
print("  -> device_scale %.3f, device_offset %.3f"
      % (w_frac * 2.0 / 0.92, cy_k))
