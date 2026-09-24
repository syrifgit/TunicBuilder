#!/usr/bin/env python3
"""Generate ribbon and full-medal artwork for cadet honours.

Everything is authored as SVG in millimetre units, so it scales to any output
size. PNGs are rasterised from the same SVG with cairosvg.

    python3 make_medals.py --dpi 300 --out ./out

Sizes follow the brief: ribbons 35 x 10 mm, full medals 35 x 100 mm. The one
exception is the Cadet Award for Bravery, whose ribbon is 38 mm per CATO
13-16 Annex B; pass --true-width to render it at its real width instead of
being squeezed into 35 mm.
"""
import argparse
import json
import math
import os

import cairosvg
from PIL import ImageFont

from medal_specs import MEDALS, PINS, METALS, UNSOURCED, acmm_states

_HERE = os.path.dirname(os.path.abspath(__file__))
# Bundled first so the script runs off a checkout on any OS; the system copy
# is only a fallback. TeX Gyre Heros is GUST Font License (LPPL 1.3c), which
# permits redistribution - see fonts/GUST-FONT-LICENSE.txt.
_BUNDLED = os.path.join(_HERE, "fonts", "texgyreheros-bold.otf")
FONT_PATH = _BUNDLED if os.path.exists(_BUNDLED) else (
    "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheros-bold.otf")
FONT_FAMILY = "TeX Gyre Heros"
_SERIF = os.path.join(_HERE, "fonts", "texgyretermes-bold.otf")
SERIF_PATH = _SERIF if os.path.exists(_SERIF) else (
    "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-bold.otf")
SERIF_FAMILY = "TeX Gyre Termes"
def _asset(name):
    return open(os.path.join(_HERE, "src", name)).read().strip()


LEAF_PATH = _asset("maple_leaf_path.txt")
LEAF_ASPECT = 0.9856          # height / width of the traced leaf
BIRD_PATH = _asset("afa_bird_sil.txt")
BIRD_INK = _asset("afa_bird_ink.txt")
BIRD_ASPECT = float(_asset("afa_bird_aspect.txt"))
BIRD_DRAWN = _asset("bird_path.txt")        # superseded, kept for older specs
EMBLEM_SIL = _asset("rcac_air_emblem_sil.txt")
EMBLEM_INK = _asset("rcac_air_emblem_ink.txt")
EMBLEM_ASPECT = float(_asset("rcac_air_emblem_aspect.txt"))
ARMY_SIL = _asset("rcac_army_emblem_sil.txt")
ARMY_INK = _asset("rcac_army_emblem_ink.txt")
ARMY_ASPECT = float(_asset("rcac_army_emblem_aspect.txt"))
LEGION_SIL = _asset("legion_emblem_sil.txt")
LEGION_INK = _asset("legion_emblem_ink.txt")
LEGION_ASPECT = float(_asset("legion_emblem_aspect.txt"))
AFA_EAGLE = _asset("afa_eagle_path.txt")
AFA_EAGLE_ASPECT = float(_asset("afa_eagle_aspect.txt"))
CROWN_SIL = _asset("st_edwards_crown_sil.txt")
CROWN_INK = _asset("st_edwards_crown_ink.txt")
CROWN_ASPECT = float(_asset("st_edwards_crown_aspect.txt"))
STRATH_INK = _asset("strathcona_ink.txt")
STRATH_LIT = _asset("strathcona_lit.txt")
STRATH_ASPECT = float(_asset("strathcona_aspect.txt"))
GEORGE_SIL = _asset("stgeorge_sil.txt")
GEORGE_INK = _asset("stgeorge_ink.txt")
GEORGE_ASPECT = float(_asset("stgeorge_aspect.txt"))
BUSTS_PATH = _asset("bravery_busts.txt")
BUSTS_ASPECT = float(_asset("bravery_busts_aspect.txt"))
ANV_METAL = _asset("anavets_metal.txt")
ANV_WHITE = _asset("anavets_white.txt")
ANV_RED = _asset("anavets_red.txt")
ANV_BLUE = _asset("anavets_blue.txt")
ANV_INK = _asset("anavets_ink.txt")
ANV_ASPECT = float(_asset("anavets_aspect.txt"))

# --- full medal layout, millimetres ----------------------------------------
# The ribbon is always 35 mm. The CANVAS is wider, so suspension bars, claws
# and their returns can overhang the ribbon the way they do on a worn group
# without running off the render. Medals are mounted at a 35 mm pitch with no
# interval (CJCR DI ch 5 para 5.c), so the overhang is meant to land on the
# neighbouring medal: the tool centres each canvas on its 35 mm slot.
RIBBON_W = 35.0             # rendered ribbon width, every medal
H = 100.0                   # CJCR DI ch5 para 7: top of suspender to bottom
TOP_BAR_H = 6.0             # of the medal is 10 cm

# The binding overhang is the squared return on a bar-and-claw suspension: it
# is as thick as the bar is tall and turns up OUTSIDE the ribbon edge. Sizing
# the canvas off that keeps ret = min(bh, (width_mm - rw)/2 - 0.25) from ever
# clamping. The extra 0.5 rather than the 0.25 the formula reserves leaves the
# return's own 0.24 mm stroke somewhere to go. Everything else overhangs less:
# the ANAVETS MERITUM bar flares to 1.15x the ribbon (40.25 mm), the Bravery
# and ACMM bars to 1.10x (38.5 mm).
CLAW_BAR_H = RIBBON_W / 7.0                       # 5.0
CANVAS_W = RIBBON_W + 2.0 * (CLAW_BAR_H + 0.5)    # 46.0
W = CANVAS_W                                      # kept: older call sites
DISC_R = 16.5
CAP_FRAC = 0.729            # TeX Gyre Heros cap height, 729/1000 em
LEGEND_CLEAR = 0.55         # mm the legend keeps clear of the inner ring
LEGEND_LEAD = 0.45          # mm between two stacked legend lines
DEVICE_CLEAR = 0.9          # mm the centre device keeps off the legend
DISC_CY = H - DISC_R - 0.3  # medal bottoms out at 100 mm, less the rim stroke
SUSP_BOT = DISC_CY - DISC_R
SUSP_TOP = SUSP_BOT - 6.0
RIBBON_BOTTOM = SUSP_TOP
PANEL_BOTTOM = DISC_CY      # para 7: panel lower edge in line with medal centres
BROOCH_H = 2.2              # pin bar across the top of a court mount


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def grad(name, metal, vertical=False):
    a, b, c, d = METALS[metal]
    coords = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    return (f'<linearGradient id="{name}" {coords}>'
            f'<stop offset="0" stop-color="{a}"/>'
            f'<stop offset="0.30" stop-color="{b}"/>'
            f'<stop offset="0.62" stop-color="{c}"/>'
            f'<stop offset="1" stop-color="{d}"/></linearGradient>')


def stripes_svg(spec, x, y, w, h):
    """Vertical ribbon stripes, normalised to w."""
    total = sum(wt for _, wt in spec["stripes"])
    out, cur = [], x
    for i, (col, wt) in enumerate(spec["stripes"]):
        seg = w * wt / total
        # overlap by a hair so cairo does not leave seams between stripes
        x0 = cur - (0.02 if i else 0)
        out.append(f'<rect x="{x0:.3f}" y="{y:.3f}" width="{seg + (0.02 if i else 0):.3f}" '
                   f'height="{h:.3f}" fill="{col}"/>')
        cur += seg
    return "".join(out)


def arc_text(text, cx, cy, r, size, fill, position="top", max_sweep=142.0,
             serif=False):
    """Lay glyphs on a circle, one rotated <text> per glyph.

    Shrinks the type if the legend would otherwise wrap past max_sweep degrees
    and collide with the other legend or run off the rim.
    """
    if not text:
        return ""
    ss = 64
    fpath = SERIF_PATH if serif else FONT_PATH
    fam = SERIF_FAMILY if serif else FONT_FAMILY
    font = ImageFont.truetype(fpath, size * ss)
    adv = [font.getlength(ch) / ss for ch in text]
    span = sum(adv)
    sweep = math.degrees(span / r)
    if sweep > max_sweep:                       # too long, scale it down
        size *= max_sweep / sweep
        font = ImageFont.truetype(fpath, max(1, int(size * ss)))
        adv = [font.getlength(ch) / ss for ch in text]
        span = sum(adv)
    out, run = [], -span / 2.0
    for ch, a in zip(text, adv):
        th = math.degrees((run + a / 2.0) / r)
        run += a
        if position == "top":
            ang = th
            rot = th
        else:                                   # bottom arc, reads left to right
            ang = 180.0 - th
            rot = ang + 180.0
        px = cx + r * math.sin(math.radians(ang))
        py = cy - r * math.cos(math.radians(ang))
        out.append(f'<text x="{px:.3f}" y="{py:.3f}" font-family="{fam}" '
                   f'font-weight="bold" font-size="{size:.3f}" fill="{fill}" '
                   f'text-anchor="middle" '
                   f'transform="rotate({rot:.3f} {px:.3f} {py:.3f})">{esc(ch)}</text>')
    return "".join(out)


def leaf_svg(cx, cy, width, fill, opacity=1.0, outline=True, weight=0.18):
    """Maple leaf with a black hairline. LOCAL DECISION: the outline is not on
    the issued artwork, but without it the WALSH red leaf vanishes on the red
    half of the ACMM ribbon and the ACSM gold leaf vanishes on its gold disc.
    weight is the stroke width in mm, held constant as the leaf scales."""
    h = width * LEAF_ASPECT
    stroke = (f' stroke="{OUTLINE}" stroke-width="{weight/width:.5f}"'
              if outline else '')
    return (f'<g transform="translate({cx - width/2:.3f},{cy - h/2:.3f}) '
            f'scale({width:.4f},{width:.4f})" fill="{fill}" opacity="{opacity}"{stroke}>'
            f'<path d="{LEAF_PATH}"/></g>')


ANCHOR = ("M0.455,0.20 L0.545,0.20 L0.545,0.80 L0.455,0.80 Z"
          "M0.20,0.255 L0.80,0.255 L0.80,0.325 L0.20,0.325 Z"
          "M0.115,0.575 C0.135,0.815 0.30,0.905 0.50,0.925 "
          "C0.70,0.905 0.865,0.815 0.885,0.575 "
          "L0.795,0.545 C0.775,0.735 0.66,0.815 0.50,0.835 "
          "C0.34,0.815 0.225,0.735 0.205,0.545 Z"
          "M0.055,0.545 L0.235,0.505 L0.145,0.665 Z"
          "M0.945,0.545 L0.765,0.505 L0.855,0.665 Z")


def anchor_svg(cx, cy, height, fill, weight=0.18):
    """Fouled anchor: ring, shank, stock and arms with flukes."""
    w = height * 0.78
    sw = weight / w
    r = 0.075
    return (f'<g transform="translate({cx - w/2:.3f},{cy - height/2:.3f}) '
            f'scale({w:.4f},{height:.4f})" fill="{fill}" stroke="{OUTLINE}" '
            f'stroke-width="{sw:.5f}">'
            f'<circle cx="0.5" cy="0.115" r="{r}" fill="none" '
            f'stroke-width="{sw*2.2:.5f}"/>'
            f'<path d="{ANCHOR}"/></g>')


def bird_svg(cx, cy, width, fill, weight=0.18, ink=False):
    """Spread-wing eagle, traced from the supplied heraldic artwork.

    On a service bar the device is only a couple of millimetres tall, so the
    default is the silhouette alone - filled AND stroked in the outline colour,
    then filled again with no stroke, which outlines the union rather than
    every subpath. Set ink=True on a medal face, where there is room for the
    traced feather line work.
    """
    h = width * BIRD_ASPECT
    g = (f'<g transform="translate({cx - width/2:.3f},{cy - h/2:.3f}) '
         f'scale({width:.4f},{width:.4f})">')
    sw = weight / width
    out = (g + f'<path d="{BIRD_PATH}" fill="{OUTLINE}" stroke="{OUTLINE}" '
               f'stroke-width="{sw*2:.5f}" stroke-linejoin="round"/>'
             + f'<path d="{BIRD_PATH}" fill="{fill}"/>')
    if ink:
        out += f'<path d="{BIRD_INK}" fill="{OUTLINE}" opacity="0.85"/>'
    return out + "</g>"


def rosette_svg(cx, cy, size, fill, weight=0.18):
    """Ribbon rosette: scalloped disc, recessed ring, raised centre."""
    lobes, r_out, r_in = 13, 0.5, 0.40
    pts = []
    for i in range(lobes * 12):
        t = i / (lobes * 12) * 2 * math.pi
        r = r_in + (r_out - r_in) * (0.5 + 0.5 * math.cos(lobes * t))
        pts.append((0.5 + r * math.cos(t), 0.5 + r * math.sin(t)))
    d = "M%.4f,%.4f " % pts[0] + " ".join("L%.4f,%.4f" % q for q in pts[1:]) + "Z"
    sw = weight / size
    return (f'<g transform="translate({cx - size/2:.3f},{cy - size/2:.3f}) '
            f'scale({size:.4f},{size:.4f})">'
            f'<path d="{d}" fill="{fill}" stroke="{OUTLINE}" stroke-width="{sw:.5f}"/>'
            f'<circle cx="0.5" cy="0.5" r="0.30" fill="none" stroke="{OUTLINE}" '
            f'stroke-width="{sw*1.4:.5f}" opacity="0.85"/>'
            f'<circle cx="0.5" cy="0.5" r="0.13" fill="{fill}" stroke="{OUTLINE}" '
            f'stroke-width="{sw:.5f}"/></g>')


def _emblem(sil, ink, aspect, cx, cy, width, fill):
    h = width * aspect
    return (f'<g transform="translate({cx - width/2:.3f},{cy - h/2:.3f}) '
            f'scale({width:.4f},{width:.4f})">'
            f'<path d="{sil}" fill="{fill}" opacity="0.22"/>'
            f'<path d="{ink}" fill="{fill}"/></g>')


def army_emblem_svg(cx, cy, width, fill, weight=0.18):
    """RCAC emblem - crowned maple leaf, RCAC monogram, ACER ACERPORI scroll.
    Traced from the corps' own artwork, drawn as gold relief."""
    return _emblem(ARMY_SIL, ARMY_INK, ARMY_ASPECT, cx, cy, width, fill)


def legion_emblem_svg(cx, cy, width, fill, weight=0.18):
    """Royal Canadian Legion badge - crown over a MEMORIAM EORUM RETINEBIMUS
    annulus, maple leaf centre, LEGION banner and poppies. Traced from the
    Legion's own artwork, drawn as relief."""
    return _emblem(LEGION_SIL, LEGION_INK, LEGION_ASPECT, cx, cy, width, fill)


def air_emblem_svg(cx, cy, width, fill, weight=0.18):
    """RCAC Air Cadets emblem as gold relief: silhouette in the light shade,
    line work in the dark shade. Traced from the League's own artwork."""
    h = width * EMBLEM_ASPECT
    return (f'<g transform="translate({cx - width/2:.3f},{cy - h/2:.3f}) '
            f'scale({width:.4f},{width:.4f})">'
            f'<path d="{EMBLEM_SIL}" fill="{fill}" opacity="0.22"/>'
            f'<path d="{EMBLEM_INK}" fill="{fill}"/></g>')


def crown_svg(cx, cy, w, fill, weight=0.14):
    """St Edward's Crown, traced from heraldic artwork: jewelled band with
    ermine, fleurs-de-lis and crosses, arches, monde and cross patee.
    `w` is the crown's width."""
    h = w * CROWN_ASPECT
    return (f'<g transform="translate({cx-w/2:.3f},{cy-h/2:.3f}) '
            f'scale({w:.4f},{w:.4f})">'
            f'<path d="{CROWN_SIL}" fill="{fill}" opacity="0.20"/>'
            f'<path d="{CROWN_INK}" fill="{fill}"/></g>')


def laurel_sprig_svg(x, y, length, fill, sign=1, weight=0.16):
    """Laurel sprig: a stem angled down and out with leaflets along it."""
    dx, dy = sign * length * 0.52, length
    out = [f'<path d="M{x:.3f},{y:.3f} Q{x+dx*0.75:.3f},{y+dy*0.35:.3f} '
           f'{x+dx:.3f},{y+dy:.3f}" fill="none" stroke="{fill}" '
           f'stroke-width="{weight:.3f}" stroke-linecap="round"/>']
    for i in range(4):
        t = 0.18 + i * 0.24
        px = x + dx * (0.75 * 2 * t * (1 - t) + t * t)
        py = y + dy * (0.35 * 2 * t * (1 - t) + t * t)
        for s2 in (-1, 1):
            out.append(f'<ellipse cx="{px + s2*sign*length*0.11:.3f}" '
                       f'cy="{py + length*0.03:.3f}" rx="{length*0.115:.3f}" '
                       f'ry="{length*0.050:.3f}" fill="{fill}" '
                       f'transform="rotate({sign*s2*42 + sign*30:.0f} '
                       f'{px + s2*sign*length*0.11:.3f} {py + length*0.03:.3f})"/>')
    return "".join(out)


def fouled_anchor_svg(cx, cy, size, fill, weight=0.18, slim=False):
    """Fouled anchor: ring, capped stock, shank, curved crown with arrowhead
    flukes, and a rope threaded through the ring winding round the shank."""
    w = size * (0.62 if slim else 0.72)
    h = size
    sw = weight / w
    sh = 0.030 if slim else 0.038          # half-width of the shank
    g = (f'<g transform="translate({cx-w/2:.3f},{cy-h/2:.3f}) '
         f'scale({w:.4f},{h:.4f})" fill="{fill}" stroke="{fill}" '
         f'stroke-width="{sw:.5f}" stroke-linejoin="round">')
    parts = [
        # ring at the head of the shank
        f'<circle cx="0.5" cy="0.075" r="0.062" fill="none" '
        f'stroke-width="{sw*2.6:.5f}"/>',
        # shank
        f'<rect x="{0.5-sh:.3f}" y="0.12" width="{2*sh:.3f}" height="0.66"/>',
        # stock, with banded caps
        '<rect x="0.20" y="0.185" width="0.60" height="0.045" rx="0.02"/>',
        '<rect x="0.175" y="0.165" width="0.055" height="0.085" rx="0.022"/>',
        '<rect x="0.770" y="0.165" width="0.055" height="0.085" rx="0.022"/>',
        # crown and arms
        f'<path d="M0.150,0.690 C0.180,0.862 0.320,0.930 0.50,0.930 '
        f'C0.680,0.930 0.820,0.862 0.850,0.690" fill="none" '
        f'stroke-width="{sw*2.7:.5f}" stroke-linecap="round"/>',
        # spade / arrowhead flukes at the tips of the arms
        '<path d="M0.150,0.712 C0.085,0.690 0.045,0.628 0.062,0.566 '
        'C0.130,0.586 0.196,0.620 0.236,0.648 Z"/>',
        '<path d="M0.850,0.712 C0.915,0.690 0.955,0.628 0.938,0.566 '
        'C0.870,0.586 0.804,0.620 0.764,0.648 Z"/>',
        # rope: through the ring, then an S around the shank
        f'<path d="M0.415,0.085 C0.255,0.175 0.300,0.330 0.560,0.400 '
        f'C0.790,0.470 0.760,0.610 0.545,0.690" fill="none" '
        f'stroke-width="{sw*2.0:.5f}" stroke-linecap="round" opacity="0.95"/>',
    ]
    return g + "".join(parts) + "</g>"


def st_george_svg(cx, cy, size, fill, weight=0.18):
    """St George and the dragon, traced from the supplied silver render.

    Bright silhouette with the engraving over it, which is how the figure
    reads on a mirror-polished field. Replaces the drawn version - the
    rotate-about-the-hip rearing pose, the stick rider and the hand-built
    dragon are all gone. See trace_stgeorge.py for the extraction.
    """
    w = size
    h = w * GEORGE_ASPECT
    return (f'<g transform="translate({cx-w/2:.3f},{cy-h/2:.3f}) '
            f'scale({w:.4f},{w:.4f})">'
            f'<path d="{GEORGE_SIL}" fill="{fill}"/>'
            f'<path d="{GEORGE_INK}" fill="#2A2F33" opacity="0.90"/></g>')


def roundel_svg(cx, cy, size, fill, weight=0.18):
    """Superseded by the traced legion_emblem; kept so older specs still run."""
    r = size * 0.36
    return (f'<circle cx="{cx:.3f}" cy="{cy + size*0.06:.3f}" r="{r:.3f}" '
            f'fill="none" stroke="{fill}" stroke-width="{size*0.055:.3f}"/>'
            + leaf_svg(cx, cy + size * 0.03, size * 0.40, fill, weight=weight)
            + crown_svg(cx, cy - size * 0.40, size * 0.34, fill))


def maple_spray_svg(x, y, length, fill, sign=1, n=5):
    """Spray of small maple leaves on a curving stem, running from the
    shield's point up to its shoulder."""
    out = [f'<path d="M{x:.3f},{y:.3f} Q{x + sign*length*0.42:.3f},'
           f'{y - length*0.44:.3f} {x + sign*length*0.30:.3f},{y - length:.3f}" '
           f'fill="none" stroke="{fill}" stroke-width="{length*0.055:.3f}" '
           f'stroke-linecap="round"/>']
    for k in range(n):
        t = 0.12 + k * (0.80 / max(1, n - 1))
        px = x + sign*length*(0.42*2*t*(1-t) + 0.30*t*t)
        py = y - length*(0.44*2*t*(1-t) + t*t)
        out.append(leaf_svg(px + sign*length*0.10, py, length*0.26, fill,
                            1.0, outline=False))
    return "".join(out)


def shield_svg(cx, cy, size, fill, weight=0.18):
    """The ANAVETS centre - crown, enamelled shield and maple sprays - traced
    from the supplied silver render.

    The only coloured face in the set, so it is five passes rather than two:
    silver for the crown and sprays, the shield's white areas, the red and
    blue enamel, and the engraved line work over the lot. See
    trace_anavets.py.
    """
    METAL, WHITE = "#C6CCD0", "#EDEFF1"
    RED, BLUE, LINE = "#C81E2D", "#1E2D82", "#3D4145"
    w = size
    h = w * ANV_ASPECT
    g = (f'<g transform="translate({cx-w/2:.3f},{cy-h/2:.3f}) '
         f'scale({w:.4f},{w:.4f})">')
    return (g + f'<path d="{ANV_METAL}" fill="{METAL}"/>'
              + f'<path d="{ANV_WHITE}" fill="{WHITE}"/>'
              + f'<path d="{ANV_RED}" fill="{RED}"/>'
              + f'<path d="{ANV_BLUE}" fill="{BLUE}"/>'
              + f'<path d="{ANV_INK}" fill="{LINE}"/></g>')


INK_DARK = "#1F2427"     # the render strikes the busts near-black


def busts_svg(cx, cy, size, fill, weight=0.18):
    """The three Cadet Award for Bravery cadets - sea, army, air - traced from
    the supplied silver render.

    Line work only. The busts are drawn as outlines and solid dark hair over
    fills that are the same silver as the field behind them, so there is no
    silhouette to separate: measured, the face interiors and the surrounding
    field both sit at mean luminance ~194. See trace_bravery.py.

    device_scale and device_offset on the spec come from the tracer, which
    reports the width as a fraction of the disc diameter and the box centre in
    disc-radius units, so the busts land where they sit on the render.
    """
    w = size
    h = w * BUSTS_ASPECT
    return (f'<g transform="translate({cx-w/2:.3f},{cy-h/2:.3f}) '
            f'scale({w:.4f},{w:.4f})">'
            f'<path d="{BUSTS_PATH}" fill="{INK_DARK}"/></g>')


def bust_svg(cx, cy, size, fill, weight=0.18):
    """Lord Strathcona in profile, traced from the supplied bronze render.

    Two passes rather than a silhouette: the highlight mask in a light bronze
    and the shadow mask in a dark one, which is how the relief reads on the
    struck medal. A silhouette pass was tried and dropped - closing the
    highlight fragments into one bust leaves a ragged edge down the profile.
    See trace_strathcona.py for the extraction.
    """
    SHADOW, HIGH = "#4E280F", "#EFC79A"
    w = size
    h = w * STRATH_ASPECT
    g = (f'<g transform="translate({cx-w/2:.3f},{cy-h/2:.3f}) '
         f'scale({w:.4f},{w:.4f})">')
    return (g + f'<path d="{STRATH_LIT}" fill="{HIGH}" opacity="0.82"/>'
              + f'<path d="{STRATH_INK}" fill="{SHADOW}" opacity="0.88"/></g>')


def afa_eagle_path(w=1.0):
    """RCAF-style eagle drawn parametrically: wings spread wide and slightly
    raised, scalloped trailing edge, head turned to the viewer's right, fanned
    tail. Drawn rather than traced - the badge source is 139 px and auto-tracing
    it gave a blobby outline."""
    ROOT, TIP = 0.505, 0.985
    Y_ROOT, Y_TIP = 0.185, 0.090          # leading edge rises toward the tip
    C_ROOT, C_TIP = 0.175, 0.030          # chord
    N = 6

    def lead(t):
        x = ROOT + t * (TIP - ROOT)
        return x, Y_ROOT + (Y_TIP - Y_ROOT) * (1 - (1 - t) ** 1.8)

    def trail(t):
        x, y = lead(t)
        chord = C_ROOT + (C_TIP - C_ROOT) * (t ** 0.55)
        scallop = 0.030 * (1 - t) ** 0.35 * max(0.0, math.sin(N * math.pi * t))
        return x, y + chord + scallop

    def wing(mirror):
        pts = [lead(k / 72) for k in range(73)]
        pts += [trail(1 - k / 72) for k in range(73)]
        if mirror:
            pts = [(1 - x, y) for x, y in pts][::-1]
        return ("M%.4f,%.4f " % pts[0]
                + " ".join("L%.4f,%.4f" % q for q in pts[1:]) + "Z")

    body = ("M0.500,0.086 C0.530,0.086 0.546,0.108 0.543,0.132 "
            "C0.562,0.140 0.571,0.158 0.569,0.180 "
            "C0.566,0.214 0.548,0.246 0.527,0.268 "
            "L0.556,0.320 L0.500,0.296 L0.444,0.320 L0.473,0.268 "
            "C0.452,0.246 0.434,0.214 0.431,0.180 "
            "C0.429,0.158 0.438,0.140 0.457,0.132 "
            "C0.454,0.108 0.470,0.086 0.500,0.086 Z")
    # head, turned to the viewer's right
    head = ("M0.500,0.092 C0.500,0.062 0.520,0.044 0.543,0.046 "
            "C0.560,0.047 0.572,0.058 0.575,0.072 "
            "L0.598,0.078 L0.574,0.090 "
            "C0.568,0.102 0.556,0.110 0.541,0.110 "
            "C0.518,0.110 0.500,0.100 0.500,0.092 Z")
    return wing(False) + wing(True) + body + head


AFA_EAGLE_DRAWN = afa_eagle_path()
AFA_DRAWN_ASPECT = 0.33


def eagle_on_leaf_svg(cx, cy, size, fill, weight=0.18):
    """Upright maple leaf with the traced eagle spread across it.

    Both pieces are struck in relief rather than outlined: a dropped shadow,
    a solid body and a highlight catching the upper-left edge. No dark
    outlines anywhere. The wings pass outside the leaf's side points, the
    leaf's top point shows above the bird, and its lower lobes show below.
    """
    SHADOW, BODY, HIGH, LINE = "#6B5010", "#F0DA93", "#FDF4D2", "#8C6C1B"
    lw = size * 0.64
    lh = lw * LEAF_ASPECT
    ly = cy + size * 0.05
    ew = size * 0.92
    eh = ew * BIRD_ASPECT
    ey = ly - eh / 2 - size * 0.06
    d = size * 0.022                          # relief offset

    def plate(path, w, x, y):
        def g(dx, dy, col, op):
            return (f'<g transform="translate({x+dx:.3f},{y+dy:.3f}) '
                    f'scale({w:.4f},{w:.4f})"><path d="{path}" fill="{col}" '
                    f'opacity="{op}"/></g>')
        return (g(d, d, SHADOW, 0.80) + g(-d * 0.6, -d * 0.6, HIGH, 0.85)
                + g(0, 0, BODY, 0.98))

    # the traced leaf stops at the lobes, so the stem is its own little plate
    stem = "M0.470,0.878 L0.530,0.878 L0.521,1.082 L0.479,1.082 Z"
    return (plate(LEAF_PATH, lw, cx - lw / 2, ly - lh / 2)
            + plate(stem, lw, cx - lw / 2, ly - lh / 2)
            + plate(BIRD_PATH, ew, cx - ew / 2, ey)
            + f'<g transform="translate({cx-ew/2:.3f},{ey:.3f}) '
              f'scale({ew:.4f},{ew:.4f})"><path d="{BIRD_INK}" fill="{LINE}" '
              f'opacity="0.62"/></g>')


def _emblems():
    return {"air_emblem":    (air_emblem_svg, EMBLEM_ASPECT, 1.55),
            "army_emblem":   (army_emblem_svg, ARMY_ASPECT, 0.92),
            "legion_emblem": (legion_emblem_svg, LEGION_ASPECT, 0.72)}


def device_svg(kind, cx, cy, size, fill, weight=0.18, spec=None, max_r=None):
    emb = _emblems()
    if kind in emb:
        fn, aspect, k = emb[kind]
        w = size * k
        if max_r:
            # keep the whole bounding box inside max_r, so a bumped
            # device_scale can never push an emblem across the legend again
            w = min(w, 2.0 * max_r, 2.0 * max_r / aspect)
        return fn(cx, cy, w, fill, weight)
    if kind == "anchor":
        return anchor_svg(cx, cy, size, fill, weight)
    if kind == "fouled_anchor":
        sc = (spec or {}).get("anchor_scale", 1.0)
        return fouled_anchor_svg(cx, cy, size * sc, fill, weight,
                                 slim=bool(spec and spec.get("anchor_slim")))
    if kind == "st_george":
        return st_george_svg(cx, cy, size, fill, weight)
    if kind == "bird":
        return bird_svg(cx, cy, size, fill, weight)
    if kind == "rosette":
        return rosette_svg(cx, cy, size, fill, weight)
    if kind == "roundel":
        return roundel_svg(cx, cy, size, fill, weight)
    if kind == "shield":
        return shield_svg(cx, cy, size, fill, weight)
    if kind == "busts":
        return busts_svg(cx, cy, size, fill, weight)
    if kind == "bust":
        return bust_svg(cx, cy, size, fill, weight)
    if kind == "eagle_on_leaf":
        return eagle_on_leaf_svg(cx, cy, size, fill, weight)
    return leaf_svg(cx, cy, size, fill, 1.0, weight=weight)


def fishtail_path(x, y, w, h):
    """Bar whose ends flare out with a concave sweep top and bottom."""
    cy, f, e = y + h / 2, w * 0.16, h * 0.20
    return (f"M{x:.3f},{cy-h/2-e:.3f} "
            f"Q{x+f*0.55:.3f},{cy-h/2-e*0.15:.3f} {x+f:.3f},{cy-h/2:.3f} "
            f"L{x+w-f:.3f},{cy-h/2:.3f} "
            f"Q{x+w-f*0.55:.3f},{cy-h/2-e*0.15:.3f} {x+w:.3f},{cy-h/2-e:.3f} "
            f"L{x+w:.3f},{cy+h/2+e:.3f} "
            f"Q{x+w-f*0.55:.3f},{cy+h/2+e*0.15:.3f} {x+w-f:.3f},{cy+h/2:.3f} "
            f"L{x+f:.3f},{cy+h/2:.3f} "
            f"Q{x+f*0.55:.3f},{cy+h/2+e*0.15:.3f} {x:.3f},{cy+h/2+e:.3f} Z")


def metal_bar(x, y, w, h, metal, text=None, gid="m", fs=2.6, radius=None,
              ink=None, end_leaves=False, shape=None, serif=False,
              w2=None, antiqued=False):
    r = min(h * 0.28, 0.9) if radius is None else radius
    ink = ink or METALS[metal][0]
    fam = SERIF_FAMILY if serif else FONT_FAMILY
    if w2 is not None:
        # trapezoid: w is the top edge, w2 the bottom, both centred on x + w/2
        mx = x + w / 2.0
        s = (f'<path d="M{x:.3f},{y:.3f} L{x+w:.3f},{y:.3f} '
             f'L{mx+w2/2:.3f},{y+h:.3f} L{mx-w2/2:.3f},{y+h:.3f} Z" '
             f'fill="url(#{gid})" stroke="{OUTLINE}" stroke-width="0.3"/>')
        if antiqued:
            # thin raised border, recessed darker field inside it
            i_, j_ = w - h * 0.5, w2 - h * 0.5
            s += (f'<path d="M{x+h*0.25:.3f},{y+h*0.22:.3f} '
                  f'L{x+w-h*0.25:.3f},{y+h*0.22:.3f} '
                  f'L{mx+j_/2:.3f},{y+h*0.78:.3f} L{mx-j_/2:.3f},{y+h*0.78:.3f} Z" '
                  f'fill="{METALS[metal][0]}" opacity="0.38"/>')
    elif shape == "fishtail":
        s = (f'<path d="{fishtail_path(x, y, w, h)}" fill="url(#{gid})" '
             f'stroke="{OUTLINE}" stroke-width="0.3"/>')
    elif shape == "bevel":          # flat plate with angled ends
        b = h * 0.55
        s = (f'<path d="M{x+b:.3f},{y:.3f} L{x+w-b:.3f},{y:.3f} L{x+w:.3f},{y+h/2:.3f} '
             f'L{x+w-b:.3f},{y+h:.3f} L{x+b:.3f},{y+h:.3f} L{x:.3f},{y+h/2:.3f} Z" '
             f'fill="url(#{gid})" stroke="{OUTLINE}" stroke-width="0.3"/>')
    else:
        s = (f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{r:.2f}" '
             f'fill="url(#{gid})" stroke="{OUTLINE}" stroke-width="0.3"/>')
        if antiqued:
            s += (f'<rect x="{x+h*0.22:.3f}" y="{y+h*0.22:.3f}" '
                  f'width="{w-h*0.44:.3f}" height="{h*0.56:.3f}" rx="{r*0.5:.2f}" '
                  f'fill="{METALS[metal][0]}" opacity="0.38"/>')
    if text:
        parts = text.split("\u2020")            # dagger marks a leaf separator
        if len(parts) == 2:
            s += (f'<text x="{x + w*0.30:.3f}" y="{y + h*0.70:.3f}" '
                  f'font-family="{FONT_FAMILY}" font-weight="bold" font-size="{fs}" '
                  f'fill="{ink}" text-anchor="middle">{esc(parts[0].strip())}</text>')
            s += leaf_svg(x + w * 0.5, y + h * 0.5, h * 0.62, METALS[metal][0], 0.85)
            s += (f'<text x="{x + w*0.72:.3f}" y="{y + h*0.70:.3f}" '
                  f'font-family="{FONT_FAMILY}" font-weight="bold" font-size="{fs}" '
                  f'fill="{ink}" text-anchor="middle">{esc(parts[1].strip())}</text>')
        else:
            s += (f'<text x="{x + w/2:.3f}" y="{y + h*0.70:.3f}" '
                  f'font-family="{fam}" font-weight="bold" font-size="{fs}" '
                  f'fill="{ink}" text-anchor="middle" '
                  f'letter-spacing="0.25">{esc(text)}</text>')
            if end_leaves:
                lf = METALS[metal][1] if antiqued else ink
                for lx in (x + w * 0.12, x + w * 0.88):
                    s += leaf_svg(lx, y + h * 0.5, h * 0.55, lf, 1.0,
                                  outline=not antiqued)
    return s


# ---------------------------------------------------------------- ribbons --
def ribbon_svg(spec, devices=0, width_mm=35.0, height_mm=10.0,
               device_colours=None, device_kind=None):
    body = stripes_svg(spec, 0, 0, width_mm, height_mm)
    if devices:
        # keep service devices on the central field, clear of the edge stripes
        field = width_mm * 0.60
        gap = field / devices
        size = min(height_mm * 0.62, gap * 0.86)
        x0 = (width_mm - field) / 2 + gap / 2
        cols = device_colours or [METALS["gold"][2]] * devices
        kind = device_kind or spec.get("service_ribbon_device", "leaf")
        for i in range(devices):
            body += device_svg(kind, x0 + gap * i, height_mm / 2, size,
                               cols[i % len(cols)])
    body += (f'<rect x="0.15" y="0.15" width="{width_mm-0.3:.3f}" '
             f'height="{height_mm-0.3:.3f}" fill="none" stroke="#00000055" '
             f'stroke-width="0.3"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_mm}mm" '
            f'height="{height_mm}mm" viewBox="0 0 {width_mm} {height_mm}">'
            f'{body}</svg>')


def pin_svg(spec):
    """Commendation / award pin at its own published size."""
    metal, w, h = spec["metal"], spec["w_mm"], spec["h_mm"]
    n = spec.get("count", 1)
    body = f'<defs>{grad("pm", metal, vertical=True)}</defs>'
    body += metal_bar(0.25, 0.25, w - 0.5, h - 0.5, metal, gid="pm",
                      radius=min(h * 0.22, 0.7))
    size = min(h * 0.74, (w * 0.72) / n * 0.92)
    gap = (w * 0.62) / n
    x0 = w / 2 - gap * (n - 1) / 2
    for i in range(n):
        body += device_svg(spec.get("device", "leaf"), x0 + gap * i, h / 2,
                           size, METALS[metal][0], weight=0.13)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" '
            f'height="{h}mm" viewBox="0 0 {w} {h}">{body}</svg>')


OUTLINE = "#141414"         # hairline on bars and devices, for legibility
DISC_INK = "#141414"         # LOCAL DECISION: black legends on every disc face

BAR_BAND_CENTRE = 0.40      # stack centre, as a fraction of ribbon height
BAR_BAND_FRAC = 0.48        # band the stack is distributed across
BAR_MAX_PITCH = 2.0         # cap spacing at this multiple of bar height


def bar_positions(n, top, bottom, bh, band_frac=None, max_pitch=None):
    """Top-y for each bar, evenly distributed and centred on the ribbon.

    Spacing tightens as bars are added rather than the stack growing
    downward, which is how they sit on an issued medal.
    """
    h = bottom - top
    pitch = min(h * (band_frac or BAR_BAND_FRAC) / n,
                bh * (max_pitch or BAR_MAX_PITCH))
    cy = top + h * BAR_BAND_CENTRE
    span = pitch * (n - 1)
    return [cy - span / 2 + i * pitch - bh / 2 for i in range(n)]


# ------------------------------------------------------------ full medals --
def medal_body(spec, bars=None, width_mm=W, service_bars=0, uid="", court=False):
    """Inner SVG for one medal, id-namespaced so a group can hold several."""
    metal = spec["metal"]
    u = f"_{uid}" if uid else ""
    d = [f'<defs>{grad("mg"+u, metal)}{grad("mgv"+u, metal, vertical=True)}']
    mets = {b[1] for b in spec.get("award_bars", [])}
    if service_bars:
        mets.add(spec.get("service_bar_metal", "gold"))
    for extra in sorted(mets):        # a set iterates in hash order, which
        # changes between processes and made the SVG defs block
        # non-reproducible even though the PNGs were identical
        d.append(grad(f"bg_{extra}{u}", extra, vertical=True))
    d.append("</defs>")
    body = "".join(d)

    top = TOP_BAR_H if spec.get("top_bar") else 0.0
    # The ribbon is 35 mm on a wider canvas, so bars, returns and trapezoid
    # flares overhang it without running off the render.
    rw = RIBBON_W
    rx = (width_mm - rw) / 2.0
    cx = width_mm / 2.0
    susp = spec["suspension"]
    # A medal that dangles on jump rings, or hangs off a bar-and-claw with a
    # proper stem, needs more room between the ribbon and the rim than the
    # 6 mm a plain loop wants. susp_gap buys it by shortening the ribbon.
    gap_h = spec.get("susp_gap", SUSP_BOT - SUSP_TOP)
    s_top = SUSP_BOT - gap_h
    dark, bright, mid = METALS[metal][0], METALS[metal][1], METALS[metal][2]
    ly = DISC_CY - DISC_R                      # top of the medallion rim
    loop = susp == "ring"

    # ---- ring first, so the ribbon's folded sleeve covers its top arc ----
    if loop:
        flat = rw / 3.0                        # flat bottom edge of the fold
        rr = min(flat * 0.43, 4.3)
        heavy = spec.get("ring_style") == "ball" and spec.get("beaded_border")
        ring_cy = ly - 0.9 - rr                # bottom of the ring meets the mount
        style = spec.get("ring_style", "tab")
        # mount on the rim: the ring passes through it, so draw it underneath
        if style == "ball":
            body += (f'<circle cx="{cx}" cy="{ly - 1.15:.2f}" '
                     f'r="{1.5 if heavy else 1.3}" fill="url(#mg{u})" '
                     f'stroke="{dark}" stroke-width="0.22"/>')
        elif style == "lug":
            body += (f'<path d="M{cx-1.1:.2f},{ly+0.4:.2f} L{cx-1.1:.2f},{ly-1.1:.2f} '
                     f'A1.1,1.1 0 0 1 {cx+1.1:.2f},{ly-1.1:.2f} '
                     f'L{cx+1.1:.2f},{ly+0.4:.2f} Z" fill="url(#mgv{u})" '
                     f'stroke="{dark}" stroke-width="0.22"/>')
        else:
            body += (f'<rect x="{cx-1.15:.2f}" y="{ly-2.4:.2f}" width="2.3" '
                     f'height="3.0" rx="0.3" fill="url(#mgv{u})" stroke="{dark}" '
                     f'stroke-width="0.22"/>')
        sw = 1.5 if heavy else 1.1
        body += (f'<circle cx="{cx}" cy="{ring_cy:.2f}" r="{rr:.2f}" fill="none" '
                 f'stroke="url(#mg{u})" stroke-width="{sw}"/>'
                 f'<circle cx="{cx}" cy="{ring_cy:.2f}" r="{rr:.2f}" fill="none" '
                 f'stroke="{dark}" stroke-width="0.18" opacity="0.75"/>')

    # ---- ribbon ---------------------------------------------------------
    # a bar-and-claw or trapezoid suspension has the ribbon looping round it,
    # so the ribbon runs on behind the metal and never shows a bottom edge
    # Only the bar-and-claw medals loop the ribbon round the bar, so only they
    # run it on behind the metal. Everywhere else the ribbon stops inside the
    # bar or claw strip above it and no bottom edge shows.
    rib_bot = s_top
    if susp == "claw_bar":
        # the ribbon loops round the plate, so it stops inside it
        rib_bot = s_top + 1.0 + (rw / 7.0) * 0.6
    elif susp == "trapezoid":
        rib_bot = s_top + 0.6            # tucked inside the claw's top strip
    elif susp == "scroll":
        rib_bot = s_top + gap_h * 0.28
    elif susp == "bar":
        rib_bot = s_top + gap_h * 0.30
    if loop:
        fold = (rw - flat) / 2.0               # 45 degrees, so run == rise
        yf = s_top - fold
        outline = (f"M{rx:.2f},{top:.2f} L{rx+rw:.2f},{top:.2f} L{rx+rw:.2f},{yf:.2f} "
                   f"L{cx+flat/2:.2f},{s_top:.2f} "
                   f"L{cx-flat/2:.2f},{s_top:.2f} L{rx:.2f},{yf:.2f} Z")
        cid = f"rib{u or '0'}"
        body += (f'<clipPath id="{cid}"><path d="{outline}"/></clipPath>'
                 f'<g clip-path="url(#{cid})">'
                 + stripes_svg(spec, rx, top, rw, s_top - top) + '</g>')
        body += f'<path d="{outline}" fill="none" stroke="#00000055" stroke-width="0.3"/>'
    else:
        body += stripes_svg(spec, rx, top, rw, rib_bot - top)
        body += (f'<rect x="{rx:.2f}" y="{top}" width="{rw:.2f}" '
                 f'height="{rib_bot-top:.2f}" fill="none" stroke="#00000055" '
                 f'stroke-width="0.3"/>')

    # ---- top bar --------------------------------------------------------
    if spec.get("top_bar"):
        shp = spec.get("bar_shape")
        if shp == "trap_down":              # ANAVETS CADET: wider at the top
            body += metal_bar(rx, 0.3, rw, TOP_BAR_H - 0.6, metal, spec["top_bar"],
                              gid="mgv"+u, fs=2.6, w2=rw * 0.86, antiqued=True,
                              end_leaves=spec.get("bar_end_leaves", False),
                              ink=METALS[metal][1])
        else:                               # Bravery CANADA: overhangs 5% a side
            ov = rw * 0.05
            body += metal_bar(rx - ov, 0.4, rw + 2 * ov, TOP_BAR_H - 0.8, metal,
                              spec["top_bar"], gid="mgv"+u,
                              end_leaves=spec.get("bar_end_leaves", False),
                              shape=shp, serif=bool(spec.get("serif")),
                              ink=("#101010" if spec.get("serif") else None))

    # ---- service bars (ACLC Policy 13.1 para 12) ------------------------
    if service_bars:
        m = spec.get("service_bar_metal", "gold")
        n = min(service_bars, spec.get("max_service_bars", 3))
        bh = 5.0 if spec.get("service_bar_device") == "bird" else 3.6
        for yb in bar_positions(n, top, s_top, bh):
            body += metal_bar(rx + 1.2, yb, rw - 2.4, bh, m,
                              gid=f"bg_{m}{u}", radius=0.25)
            dev = spec.get("service_bar_device")
            if dev:
                kind = dev if isinstance(dev, str) else "leaf"
                span = (bh * 0.88 / BIRD_ASPECT) if kind == "bird" else bh * 0.66
                body += device_svg(kind, cx, yb + bh / 2, span,
                                   METALS[m][2], weight=0.16)

    # ---- award bars: square ends, overhanging the ribbon ----------------
    want = bars if bars is not None else [b[0] for b in spec.get("award_bars", [])]
    if want:
        lookup = dict(spec.get("award_bars", []))
        order = [b[0] for b in spec.get("award_bars", [])]
        want = sorted(want, key=lambda l: order.index(l) if l in order else 0,
                      reverse=True)                     # senior bar on top
        bh = 5.2
        ov = rw * 0.05 if spec.get("bars_overhang") else 0.0
        for label, yb in zip(want, bar_positions(
                len(want), top, s_top, bh,
                spec.get("bar_band_frac"), spec.get("bar_max_pitch"))):
            m = lookup.get(label, "gold")
            body += metal_bar(rx - ov, yb, rw + 2 * ov, bh, m, label,
                              gid=f"bg_{m}{u}", fs=3.1, radius=0.0,
                              ink=spec.get("bar_ink", {}).get(label, "#1F1F1F"))

    # ---- suspensions -----------------------------------------------------
    if susp == "claw_bar":
        # Flat plate the ribbon loops around, squared returns turning up
        # OUTSIDE the ribbon edges, a leaf straddling the plate's top edge,
        # a thick stem, and a broad shoulder-claw merging into the rim.
        bh = rw / 7.0
        # the return wants to be as thick as the bar is tall, but the canvas
        # is fixed at 35 mm, so take whatever fits outside the ribbon
        ret = min(bh, (width_mm - rw) / 2.0 - 0.25)
        by = s_top + 1.0
        body += (f'<rect x="{rx-ret:.2f}" y="{by:.2f}" width="{rw+2*ret:.2f}" '
                 f'height="{bh:.2f}" fill="url(#mgv{u})" stroke="{OUTLINE}" '
                 f'stroke-width="0.26"/>')
        body += (f'<rect x="{rx-ret:.2f}" y="{by:.2f}" width="{rw+2*ret:.2f}" '
                 f'height="{bh*0.34:.2f}" fill="{bright}" opacity="0.35"/>')
        for ex in (rx - ret, rx + rw):             # squared returns, outside
            body += (f'<rect x="{ex:.2f}" y="{by-bh:.2f}" width="{ret:.2f}" '
                     f'height="{bh*2:.2f}" fill="url(#mgv{u})" stroke="{OUTLINE}" '
                     f'stroke-width="0.24"/>')
        stem_w = rw / 7.0
        body += (f'<path d="M{cx-stem_w/2:.2f},{by+bh:.2f} '
                 f'L{cx+stem_w/2:.2f},{by+bh:.2f} L{cx+stem_w/2:.2f},{ly-1.6:.2f} '
                 f'C{cx+width_mm*0.10:.2f},{ly-1.0:.2f} '
                 f'{cx+width_mm*0.18:.2f},{ly-0.3:.2f} '
                 f'{cx+width_mm*0.20:.2f},{ly+1.1:.2f} '
                 f'L{cx-width_mm*0.20:.2f},{ly+1.1:.2f} '
                 f'C{cx-width_mm*0.18:.2f},{ly-0.3:.2f} '
                 f'{cx-width_mm*0.10:.2f},{ly-1.0:.2f} '
                 f'{cx-stem_w/2:.2f},{ly-1.6:.2f} Z" fill="url(#mgv{u})" '
                 f'stroke="{dark}" stroke-width="0.22"/>')
        body += leaf_svg(cx, by, bh * 1.3, f"url(#mgv{u})", 1.0, weight=0.16)
    elif susp == "trapezoid":
        st = rw * 0.25
        y0, y1 = s_top, s_top + 0.9
        y2 = min(y1 + 2.6, ly - 1.2)
        body += (f'<path d="M{rx:.2f},{y0:.2f} L{rx+rw:.2f},{y0:.2f} '
                 f'L{rx+rw:.2f},{y1:.2f} L{cx+st/2:.2f},{y2:.2f} '
                 f'L{cx+st/2:.2f},{ly+0.4:.2f} L{cx-st/2:.2f},{ly+0.4:.2f} '
                 f'L{cx-st/2:.2f},{y2:.2f} L{rx:.2f},{y1:.2f} Z" '
                 f'fill="url(#mgv{u})" stroke="{dark}" stroke-width="0.25"/>')
    elif susp != "ring":
        txt = spec.get("suspension_text")
        if spec.get("bottom_bar_flare"):
            # ANAVETS MERITUM: trapezoid flaring wider going down, and the
            # tallest, widest piece on the medal
            bh = TOP_BAR_H * 0.92
            body += metal_bar(rx, s_top, rw, bh, metal, txt, gid="mgv"+u,
                              fs=2.6, w2=rw * 1.15, antiqued=True,
                              end_leaves=spec.get("bar_end_leaves", False),
                              ink=METALS[metal][1])
        else:
            bh = 3.12 if susp == "scroll" else gap_h
            ov = rw * 0.05 if susp == "scroll" else 0.0
            body += metal_bar(rx - ov, s_top, rw + 2 * ov, bh, metal, txt,
                              gid="mgv"+u, fs=2.5,
                              end_leaves=spec.get("bar_end_leaves", False),
                              shape=spec.get("bar_shape"),
                              serif=bool(spec.get("serif")),
                              ink=("#101010" if spec.get("serif") else None))
        if spec.get("hanging_rings"):
            # pierced lug under the bar, two jump rings, an eye on the rim
            y1 = s_top + bh
            gap = ly - y1
            body += (f'<rect x="{cx-0.9:.2f}" y="{y1-0.2:.2f}" width="1.8" '
                     f'height="{gap*0.30:.2f}" rx="0.5" fill="url(#mgv{u})" '
                     f'stroke="{dark}" stroke-width="0.18"/>')
            body += (f'<circle cx="{cx}" cy="{ly-0.5:.2f}" r="0.85" '
                     f'fill="url(#mg{u})" stroke="{dark}" stroke-width="0.18"/>')
            for fy, fr in ((0.34, 0.26), (0.72, 0.24)):
                body += (f'<circle cx="{cx}" cy="{y1 + gap*fy:.2f}" '
                         f'r="{gap*fr:.2f}" fill="none" stroke="url(#mg{u})" '
                         f'stroke-width="0.5"/>'
                         f'<circle cx="{cx}" cy="{y1 + gap*fy:.2f}" '
                         f'r="{gap*fr:.2f}" fill="none" stroke="{dark}" '
                         f'stroke-width="0.14" opacity="0.8"/>')
        if susp == "scroll":
            # One rigid ornament: a solid body merging into the bar above and
            # the rim below, with a tight volute at each end and a flame
            # finial up the middle.
            sb = s_top + bh
            hw = rw * 0.70 / 2.0
            mid = (sb + ly) / 2.0
            body += (f'<path d="M{cx-hw:.2f},{sb-0.3:.2f} '
                     f'C{cx-hw:.2f},{mid+0.4:.2f} {cx-hw*0.34:.2f},{mid+0.9:.2f} '
                     f'{cx-1.9:.2f},{ly+1.0:.2f} '
                     f'L{cx+1.9:.2f},{ly+1.0:.2f} '
                     f'C{cx+hw*0.34:.2f},{mid+0.9:.2f} {cx+hw:.2f},{mid+0.4:.2f} '
                     f'{cx+hw:.2f},{sb-0.3:.2f} '
                     f'L{cx+hw*0.62:.2f},{sb-0.3:.2f} '
                     f'C{cx+hw*0.60:.2f},{mid:.2f} {cx+hw*0.20:.2f},{mid+0.5:.2f} '
                     f'{cx:.2f},{ly-0.4:.2f} '
                     f'C{cx-hw*0.20:.2f},{mid+0.5:.2f} {cx-hw*0.60:.2f},{mid:.2f} '
                     f'{cx-hw*0.62:.2f},{sb-0.3:.2f} Z" fill="url(#mgv{u})" '
                     f'stroke="{dark}" stroke-width="0.22"/>')
            for sgn in (-1, 1):                    # tight volute at each end
                vx, vy = cx + sgn * hw * 0.78, sb + (ly - sb) * 0.30
                body += (f'<circle cx="{vx:.2f}" cy="{vy:.2f}" r="1.65" '
                         f'fill="url(#mg{u})" stroke="{dark}" stroke-width="0.2"/>')
                body += (f'<path d="M{vx + sgn*1.42:.2f},{vy-0.85:.2f} '
                         f'A1.65,1.65 0 1 {0 if sgn>0 else 1} '
                         f'{vx - sgn*0.40:.2f},{vy+1.05:.2f} '
                         f'A0.86,0.86 0 1 {1 if sgn>0 else 0} '
                         f'{vx + sgn*0.62:.2f},{vy-0.12:.2f} '
                         f'A0.34,0.34 0 1 {0 if sgn>0 else 1} '
                         f'{vx - sgn*0.10:.2f},{vy+0.22:.2f}" fill="none" '
                         f'stroke="{dark}" stroke-width="0.30" opacity="0.8"/>')
            # tall acanthus finial: point up under the bar, a swelling belly,
            # a waist, then a flare into a small claw merging with the rim
            hi = sb - 0.4
            body += (f'<path d="M{cx:.2f},{hi:.2f} '
                     f'C{cx+0.42:.2f},{hi+1.0:.2f} {cx+1.60:.2f},{mid-0.2:.2f} '
                     f'{cx+1.32:.2f},{mid+0.9:.2f} '
                     f'C{cx+1.12:.2f},{mid+1.7:.2f} {cx+1.40:.2f},{ly-0.8:.2f} '
                     f'{cx+2.35:.2f},{ly+1.2:.2f} '
                     f'L{cx-2.35:.2f},{ly+1.2:.2f} '
                     f'C{cx-1.40:.2f},{ly-0.8:.2f} {cx-1.12:.2f},{mid+1.7:.2f} '
                     f'{cx-1.32:.2f},{mid+0.9:.2f} '
                     f'C{cx-1.60:.2f},{mid-0.2:.2f} {cx-0.42:.2f},{hi+1.0:.2f} '
                     f'{cx:.2f},{hi:.2f} Z" fill="url(#mgv{u})" '
                     f'stroke="{dark}" stroke-width="0.2"/>')
            for sgn in (-1, 1):                    # acanthus side lobes
                body += (f'<path d="M{cx + sgn*0.35:.2f},{mid-0.9:.2f} '
                         f'C{cx + sgn*1.75:.2f},{mid-0.7:.2f} '
                         f'{cx + sgn*1.95:.2f},{mid+0.5:.2f} '
                         f'{cx + sgn*1.25:.2f},{mid+1.2:.2f} '
                         f'C{cx + sgn*1.35:.2f},{mid+0.3:.2f} '
                         f'{cx + sgn*0.95:.2f},{mid-0.4:.2f} '
                         f'{cx + sgn*0.35:.2f},{mid-0.9:.2f} Z" '
                         f'fill="url(#mg{u})" stroke="{dark}" '
                         f'stroke-width="0.18"/>')
            body += (f'<path d="M{cx:.2f},{hi+1.0:.2f} L{cx:.2f},{ly+0.4:.2f}" '
                     f'stroke="{dark}" stroke-width="0.22" opacity="0.45"/>')

    if susp == "ring":
        pass                                   # ring and mount already drawn
    elif susp == "bar" and not spec.get("hanging_rings"):
        body += (f'<rect x="{cx-1.5:.2f}" y="{SUSP_BOT-0.6:.2f}" width="3" '
                 f'height="{max(0.4, ly - SUSP_BOT + 1.4):.2f}" '
                 f'fill="url(#mgv{u})" stroke="{dark}" stroke-width="0.22"/>')

    # medallion
    body += (f'<circle cx="{cx}" cy="{DISC_CY}" r="{DISC_R}" fill="url(#mg{u})" '
             f'stroke="{METALS[metal][0]}" stroke-width="0.45"/>')
    if spec.get("disc_checker"):
        cols = spec["disc_checker"]
        rr, segs = DISC_R * 0.90, 8
        circ = 2 * math.pi * rr
        seg = circ / (segs * len(cols))
        for i, col in enumerate(cols):
            body += (f'<circle cx="{cx}" cy="{DISC_CY}" r="{rr:.2f}" fill="none" '
                     f'stroke="{col}" stroke-width="{DISC_R*0.16:.2f}" '
                     f'stroke-dasharray="{seg:.3f} {seg*(len(cols)-1):.3f}" '
                     f'stroke-dashoffset="{-seg*i:.3f}"/>')
        body += (f'<circle cx="{cx}" cy="{DISC_CY}" r="{DISC_R*0.82:.2f}" '
                 f'fill="url(#mg{u})" stroke="{METALS[metal][0]}" stroke-width="0.3"/>')
    field = spec.get("disc_field")
    if spec.get("finish") == "mirror":
        field = field or "#2A2E31"
    if field:
        body += (f'<circle cx="{cx}" cy="{DISC_CY}" r="{DISC_R*0.90:.2f}" fill="{field}" '
                 f'stroke="{METALS[metal][0]}" stroke-width="0.3"/>')
        # a polished face reflects dark, so the raised work reads bright
        ink = "#F2F5F6" if spec.get("finish") == "mirror" else DISC_INK
    else:
        body += (f'<circle cx="{cx}" cy="{DISC_CY}" r="{DISC_R*0.86:.2f}" fill="none" '
                 f'stroke="{METALS[metal][0]}" stroke-width="0.3" opacity="0.75"/>')
        ink = DISC_INK
    if spec.get("beaded_border"):
        # ring of small raised dots just inside the rim
        rb, n = DISC_R * 0.925, 64
        for i in range(n):
            th = 2 * math.pi * i / n
            body += (f'<circle cx="{cx + rb*math.sin(th):.3f}" '
                     f'cy="{DISC_CY - rb*math.cos(th):.3f}" r="0.42" '
                     f'fill="{METALS[metal][0]}" opacity="0.85"/>')
    if spec.get("dot_ornaments"):
        # a square of four dots each side of IN CANADA
        rdot = DISC_R * 0.70
        for sgn in (-1, 1):
            bx = cx + sgn * rdot * 0.62
            by = DISC_CY + rdot * 0.70
            for ddx in (-0.42, 0.42):
                for ddy in (-0.42, 0.42):
                    body += (f'<circle cx="{bx + ddx:.2f}" cy="{by + ddy:.2f}" '
                             f'r="0.28" fill="{DISC_INK}" opacity="0.9"/>')
    if spec.get("side_dashes"):
        # short dashes at 9 and 3 o'clock, parting the top and bottom legends
        for sgn in (-1, 1):
            body += (f'<rect x="{cx + sgn*DISC_R*0.80 - 1.1:.2f}" '
                     f'y="{DISC_CY - 0.28:.2f}" width="2.2" height="0.56" rx="0.2" '
                     f'fill="{DISC_INK}" opacity="0.9"/>')
    if spec.get("crown_laurels"):
        cyc = DISC_CY - DISC_R * 0.585
        dk = METALS[metal][1] if spec.get("finish") == "mirror" else METALS[metal][0]
        body += crown_svg(cx, cyc, DISC_R * 0.50, dk)
        # two sprigs floating free at about 10 and 2 o'clock, top near the
        # crown and bottom out toward the rim, touching nothing
        for sgn in (-1, 1):
            body += laurel_sprig_svg(cx + sgn * DISC_R * 0.44,
                                     DISC_CY - DISC_R * 0.50,
                                     DISC_R * 0.40, dk, sign=sgn, weight=0.40)
    # Legends hang off the INNER RING, both anchored by the edge that faces it.
    # arc_text puts the baseline at the radius it is given; a top arc grows
    # outward from there and a bottom arc grows inward. So the bottom legend
    # takes the ring radius directly (its baseline IS its outer edge) while the
    # top legend has a cap height subtracted, putting the TOP of its glyphs on
    # the ring instead of its baseline. Passing both the same radius is what
    # used to push SERVICE - CADETS out across the ring.
    ring_r = DISC_R * (0.82 if spec.get("disc_checker") else 0.86)
    fs = 2.3 * (0.82 if spec.get("disc_checker") else 1.0)
    cap = fs * CAP_FRAC
    edge = ring_r - LEGEND_CLEAR

    lines = []
    if spec.get("legend_top"):
        lines.append((spec["legend_top"], "top", edge - cap))
    inner_k = spec.get("inner_arc_k", 1.0)
    if spec.get("legend_top2"):                 # second line, inboard of the first
        lines.append((spec["legend_top2"], "top",
                      (edge - 2 * cap - LEGEND_LEAD) * inner_k))
    if spec.get("legend_bottom"):
        lines.append((spec["legend_bottom"], "bottom", edge))
        bs = spec.get("legend_bottom_size")
        if bs and bs > fs:                  # keep its cap inside the ring
            lines[-1] = (spec["legend_bottom"], "bottom", edge)
    if spec.get("legend_bottom2"):              # inner bottom arc, above the outer
        lines.append((spec["legend_bottom2"], "bottom",
                      (edge - cap - LEGEND_LEAD) * inner_k))
    # The device is drawn before the legends but has to clear them, so the
    # innermost legend ink sets the room it gets. A top arc's baseline is its
    # inner edge; a bottom arc's cap top is, one cap height further in.
    inner = [r if pos == "top" else r - cap for _, pos, r in lines]
    legend_min_r = min(inner) if inner else DISC_R * 0.86

    dev_ink = "#EDF1F3" if spec.get("finish") == "mirror" else METALS[metal][0]
    if spec.get("device"):
        # dark shade of the medal's own metal: reads as engraved and keeps
        # contrast on both light (silver) and dark (gold) faces
        off = spec.get("device_offset",
                       0.22 if spec.get("legend_lines_top") else 0.0)
        dev_cy = DISC_CY + DISC_R * off
        body += device_svg(spec["device"], cx, dev_cy,
                           DISC_R * 0.92 * spec.get("device_scale", 1.0),
                           dev_ink, weight=0.3, spec=spec,
                           max_r=legend_min_r - DEVICE_CLEAR)

    serif = bool(spec.get("serif"))
    for line, pos, r in lines:
        size_ = fs
        if pos == "bottom" and line == spec.get("legend_bottom"):
            size_ = spec.get("legend_bottom_size", fs)
        body += arc_text(line, cx, DISC_CY, r, size_, ink, pos,
                         max_sweep=spec.get("legend_bottom_sweep", 134.0),
                         serif=serif)

    # straight horizontal legend lines in the top third (Cadet Award for
    # Bravery: FOR BRAVERY over POUR BRAVOURE, not arcs)
    flat = spec.get("legend_lines_top", [])
    if flat:
        fam = SERIF_FAMILY if serif else FONT_FAMILY
        y = DISC_CY - DISC_R * 0.52
        for line in flat:
            body += (f'<text x="{cx}" y="{y:.2f}" font-family="{fam}" '
                     f'font-weight="bold" font-size="2.7" fill="{ink}" '
                     f'text-anchor="middle" letter-spacing="0.1">{esc(line)}</text>')
            y += 3.3

    for i, line in enumerate(spec.get("centre_lines", [])):
        y = DISC_CY - 5.0 + i * 10.5
        body += (f'<text x="{cx}" y="{y:.2f}" font-family="{FONT_FAMILY}" '
                 f'font-weight="bold" font-size="3.0" fill="{ink}" '
                 f'text-anchor="middle" opacity="0.9">{esc(line)}</text>')

    return body


def medal_svg(spec, bars=None, width_mm=W, service_bars=0, court=False):
    body = medal_body(spec, bars, width_mm, service_bars, court=court)
    top = -BROOCH_H if court else 0.0
    h = H - top
    if court:
        body = brooch_svg(0, top, width_mm) + body
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_mm}mm" '
            f'height="{h}mm" viewBox="0 {top} {width_mm} {h}">{body}</svg>')


def brooch_svg(x, y, w):
    """Pin bar across the top of a court mount."""
    return (f'<defs><linearGradient id="br{abs(hash((x,w)))%9999}" x1="0" y1="0" '
            f'x2="0" y2="1"><stop offset="0" stop-color="#C9CFD2"/>'
            f'<stop offset="0.5" stop-color="#EDF1F3"/>'
            f'<stop offset="1" stop-color="#8A9094"/></linearGradient></defs>'
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{BROOCH_H:.2f}" '
            f'rx="0.5" fill="url(#br{abs(hash((x,w)))%9999})" stroke="{OUTLINE}" '
            f'stroke-width="0.3"/>')


def group_svg(keys, court=True, overlap_from=5):
    """Court-mounted group. CJCR DI ch5 para 5.c: medals in order of
    precedence without interval, highest priority closest to the centre of the
    chest. Medals sit above the RIGHT breast, so the centre of the chest is on
    the wearer's left, which is the viewer's right. Senior therefore renders
    rightmost. Overlap only once five or more are worn."""
    specs = [(k, MEDALS[k]) for k in keys]
    specs.sort(key=lambda kv: (kv[1].get("precedence") or 99), reverse=True)
    widths = [s.get("ribbon_width_mm", W) for _, s in specs]
    n = len(specs)
    pitch = [w for w in widths]
    if n >= overlap_from:                       # squeeze, senior stays full
        shown = 0.72
        pitch = [w * shown for w in widths]
        pitch[-1] = widths[-1]
    total = sum(pitch[:-1]) + widths[-1]
    top = -BROOCH_H if court else 0.0
    parts, x = [], 0.0
    for i, (k, sp) in enumerate(specs):
        parts.append(f'<g transform="translate({x:.3f},0)">'
                     + medal_body(sp, width_mm=widths[i], uid=k, court=court)
                     + '</g>')
        x += pitch[i]
    head = brooch_svg(0, top, total) if court else ""
    h = H - top
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{total}mm" '
            f'height="{h}mm" viewBox="0 {top} {total} {h}">'
            f'{head}{"".join(parts)}</svg>'), total, h


def rack_svg(keys, per_row=3, rw=W, rh=10.0):
    """Undress ribbon rack. CJCR DI ch5 para 6.c: max three per row, no
    interval, each new row centred on the one below, senior closest to the
    centre of the chest (viewer's right) on the top row."""
    specs = [(k, MEDALS[k]) for k in keys]
    specs.sort(key=lambda kv: (kv[1].get("precedence") or 99))
    # Fill rows from the bottom with the most junior, so the senior ends up on
    # the top row (para 6.c: highest priority on the top row; a single ribbon
    # forming a row is centred above the row below).
    junior_first = specs[::-1]
    rows = [junior_first[i:i + per_row] for i in range(0, len(junior_first), per_row)]
    rows = rows[::-1]                           # render top row first
    width = max(len(r) for r in rows) * rw
    height = len(rows) * rh
    parts = []
    for ri, row in enumerate(rows):
        # rows are already junior-to-senior left to right, which puts the
        # senior of each row closest to the centre of the chest
        x0 = (width - len(row) * rw) / 2
        for ci, (k, sp) in enumerate(row):
            parts.append(f'<g transform="translate({x0+ci*rw:.3f},{ri*rh:.3f})">'
                         + stripes_svg(sp, 0, 0, rw, rh)
                         + f'<rect x="0.15" y="0.15" width="{rw-0.3:.2f}" '
                           f'height="{rh-0.3:.2f}" fill="none" stroke="{OUTLINE}" '
                           f'stroke-width="0.3"/></g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" '
            f'height="{height}mm" viewBox="0 0 {width} {height}">'
            f'{"".join(parts)}</svg>'), width, height


# ------------------------------------------------------------------ main --
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    px = a.dpi / 25.4
    os.makedirs(f"{a.out}/svg", exist_ok=True)
    os.makedirs(f"{a.out}/png", exist_ok=True)
    manifest = {}

    def emit(key, svg, w_mm, h_mm, meta, ribbon_w=None):
        open(f"{a.out}/svg/{key}.svg", "w").write(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=f"{a.out}/png/{key}.png",
                         output_width=round(w_mm * px), output_height=round(h_mm * px))
        entry = {"w_mm": round(w_mm, 2), "h_mm": round(h_mm, 2),
                 "aspect": round(w_mm / h_mm, 4),
                 "png": f"png/{key}.png", "svg": f"svg/{key}.svg"}
        if ribbon_w is not None:
            # w_mm is the CANVAS. The ribbon inside it is always this wide,
            # centred, so the tool does not have to infer it.
            entry["ribbon_w_mm"] = round(ribbon_w, 2)
        entry.update(meta)
        manifest[key] = entry

    def meta_for(key, spec, extra=None):
        m = {k: spec.get(k) for k in
             ("name", "authority", "precedence", "fidelity", "source")}
        m["true_ribbon_width_mm"] = spec.get("ribbon_width_mm")
        if spec.get("ribbon_width_mm") not in (None, RIBBON_W):
            m["width_note"] = (
                f"Issued ribbon is {spec['ribbon_width_mm']} mm. Rendered at "
                f"{RIBBON_W:.0f} mm: LOCAL DECISION so ribbon rows stay "
                f"aligned.")
        if extra:
            m.update(extra)
        return m

    # ---- ribbons at 35 mm; medals on the wider canvas --------------------
    for key, spec in MEDALS.items():
        if key == "acmm":
            continue                       # never worn bare, see below
        emit(f"ribbon_{key}", ribbon_svg(spec, width_mm=RIBBON_W),
             RIBBON_W, 10.0, meta_for(key, spec))
        emit(f"medal_{key}", medal_svg(spec, width_mm=CANVAS_W), CANVAS_W, H,
             meta_for(key, spec), ribbon_w=RIBBON_W)

    # ---- service medals: four years earns the medal, each further year a
    # bar. Army per ACLC Policy 13.1 para 12; Air the same system with its own
    # devices. Any spec carrying max_service_bars gets its variants here.
    for key, spec in MEDALS.items():
        cap = spec.get("max_service_bars")
        if not cap:
            continue
        for years in range(5, 5 + cap):
            n = years - 4
            note = {"variant": f"{years} years of service, {n} bar"
                               f"{'s' if n > 1 else ''}"}
            emit(f"ribbon_{key}_{years}yr",
                 ribbon_svg(spec, devices=n, width_mm=RIBBON_W),
                 RIBBON_W, 10.0, meta_for(key, spec, note))
            emit(f"medal_{key}_{years}yr",
                 medal_svg(spec, width_mm=CANVAS_W, service_bars=n),
                 CANVAS_W, H, meta_for(key, spec, note), ribbon_w=RIBBON_W)

    # ---- ACMM, the 11 wearable bar states --------------------------------
    acmm = MEDALS["acmm"]
    dev = acmm["bar_devices"]
    for code, bars in acmm_states():
        note = {"variant": "bars: " + ", ".join(bars)}
        emit(f"medal_acmm_{code}",
             medal_svg(acmm, bars=bars, width_mm=CANVAS_W), CANVAS_W, H,
             meta_for("acmm", acmm, note), ribbon_w=RIBBON_W)
        emit(f"ribbon_acmm_{code}",
             ribbon_svg(acmm, devices=len(bars), width_mm=RIBBON_W,
                        device_colours=[dev[b] for b in bars]),
             RIBBON_W, 10.0, meta_for("acmm", acmm, note))

    # ---- commendation and award pins, at their own published sizes -------
    for key, spec in PINS.items():
        emit(key, pin_svg(spec), spec["w_mm"], spec["h_mm"],
             {k: spec.get(k) for k in
              ("name", "authority", "fidelity", "source")})

    manifest["_unsourced"] = UNSOURCED
    json.dump(manifest, open(f"{a.out}/medal_art_manifest.json", "w"), indent=2)
    print(f"wrote {len(manifest)-1} items to {a.out} at {a.dpi} dpi")


if __name__ == "__main__":
    main()
