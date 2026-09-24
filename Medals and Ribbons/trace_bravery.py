"""Trace the three Cadet Award for Bravery busts into src/bravery_busts.txt.

    python3 trace_bravery.py bravery_render.png

The busts are line art: dark outlines and solid dark hair over fills that are
the same silver as the field behind them. Component analysis confirms it - the
face interiors and the surrounding field both sit at mean luminance ~194, so
there is no silhouette to separate. Trying to flood the background and keep
the rest just returns the whole disc.

So this traces the line work only, which is what the render actually is. Two
cuts:

1. The legend. FOR BRAVERY / POUR BRAVOURE is flat text across the top of the
   face, not an arc, so it is cut by y - everything above the sea cadet's cap.
2. The rim. Cutting at 0.828 of the disc radius drops the rim circle - a radius
   histogram puts it at 0.84 to 0.86, clear of the shoulders, which fade out
   by 0.80 - and leaves the busts whole.

The disc is fitted from the widest bright row in the lower half of the frame,
below the scroll suspender.
"""
import sys
import numpy as np
import potrace
from PIL import Image
from scipy import ndimage as ndi

src = sys.argv[1] if len(sys.argv) > 1 else "bravery_render.png"
L = np.array(Image.open(src).convert("RGB")).astype(float).mean(2)

# the disc is the big bright blob in the lower half, below the suspender
sub = L[L.shape[0] // 2:, :]
bright = sub > 100
lab, n = ndi.label(bright)
d = ndi.binary_fill_holes(lab == int(np.argmax(ndi.sum(bright, lab, range(1, n + 1)))) + 1)
r = int(np.argmax(d.sum(1)))
row = np.nonzero(d[r])[0]
cx = (row.min() + row.max()) / 2.0
R = (row.max() - row.min()) / 2.0
cy = r + L.shape[0] // 2
Y, X = np.mgrid[0:L.shape[0], 0:L.shape[1]]
rad = np.hypot(X - cx, Y - cy) / R

# The legend and the busts are separated by a band of bare metal. It is not
# perfectly empty - the rim arc and JPEG ringing leave ~12 px on every row -
# so "quiet" is a low count, not zero. The band above the legend is quiet too,
# hence the LAST quiet row above the centre rather than the longest run.
ink_all = (L < 135) & (rad < 0.828)
rows = ink_all.sum(1)
lo = cy - int(R * 0.62)
quiet = [y for y in range(lo, cy) if rows[y] <= 25]
assert quiet, "no clear band between the legend and the busts"
top = max(quiet)
ink = ink_all & (Y > top)

ys, xs = np.nonzero(ink)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
W, H = x1 - x0 + 1, y1 - y0 + 1
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


open("src/bravery_busts.txt", "w").write(trace(ink, 8))
open("src/bravery_busts_aspect.txt", "w").write("%.5f" % (H / W))

# Placement, so the busts land on our disc exactly where they sit on the
# render: width as a fraction of the disc DIAMETER, and the box centre in
# disc-radius units below the centre. These feed device_scale and
# device_offset in medal_specs.py rather than being eyeballed.
w_frac = W / (2.0 * R)
cy_k = ((y0 + y1) / 2.0 - cy) / R
open("src/bravery_busts_place.txt", "w").write("%.5f %.5f" % (w_frac, cy_k))
print("placement: width %.4f of the disc diameter, centre %+.4f R"
      % (w_frac, cy_k))
print("  -> device_scale %.3f, device_offset %.3f"
      % (w_frac * 2.0 / 0.92, cy_k))
print("disc centre (%.0f, %d) R %.0f, legend ends at y=%d" % (cx, cy, R, top))
print("traced %d x %d px, aspect %.5f" % (W, H, H / W))
