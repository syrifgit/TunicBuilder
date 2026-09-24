"""Device / legend clearance check.

Renders each medal three times - full, with the device suppressed, and with
neither device nor legend - and diffs the ink masks so the device pixels and
the legend pixels are isolated exactly. Then measures the closest approach
between the two.

Suppressing the legends also relaxes the device clamp, so the device must be
isolated against the FULL render, never against the legend-free one.
"""
import sys, os, copy, cairosvg, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy import ndimage as ndi
from PIL import Image
import io
import make_medals as M, medal_specs as ms

# Derive px/mm from the canvas rather than hard-coding it. When the canvas
# widened from 35 to 46 mm a fixed 600/35 quietly scaled every gap by 0.76 and
# made it look as though the clearances had shrunk.
WIDE = 600
PX = WIDE / M.CANVAS_W


def render(spec):
    svg = M.medal_svg(spec)
    buf = io.BytesIO()
    cairosvg.svg2png(bytestring=svg.encode(), write_to=buf,
                     output_width=WIDE,
                     output_height=round(WIDE * M.H / M.CANVAS_W))
    return np.array(Image.open(buf).convert('RGB')).astype(int)


def diff(a, b):
    return (np.abs(a - b).max(2) > 18)


rows = []
for key, spec in ms.MEDALS.items():
    full = render(spec)
    no_dev = copy.deepcopy(spec); no_dev['device'] = None
    nd = render(no_dev)
    bare = copy.deepcopy(no_dev)
    bare['legend_top'] = None; bare['legend_bottom'] = None
    bare['legend_mid'] = None; bare['legend_bottom2'] = None
    bare['legend_lines_top'] = None
    br = render(bare)

    dev = diff(full, nd)            # pixels the device contributes
    leg = diff(nd, br)              # pixels the legends contribute
    if not dev.any() or not leg.any():
        rows.append((key, None)); continue
    d = ndi.distance_transform_edt(~leg)
    gap = d[dev].min() / PX
    rows.append((key, gap))

w = max(len(k) for k, _ in rows)
for k, g in rows:
    print(f"{k:<{w}}  " + ("no device/legend" if g is None
                           else f"{g:6.2f} mm  " + ("OK" if g > 0.25 else "TOUCHING")))
