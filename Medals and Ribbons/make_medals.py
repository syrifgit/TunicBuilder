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

FONT_PATH = "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheros-bold.otf"
FONT_FAMILY = "TeX Gyre Heros"
LEAF_PATH = open(os.path.join(os.path.dirname(__file__),
                              "src/maple_leaf_path.txt")).read().strip()
LEAF_ASPECT = 0.9856          # height / width of the traced leaf

# --- full medal layout, millimetres on a 35 x 100 canvas --------------------
W = 35.0
H = 100.0                   # CJCR DI ch5 para 7: top of suspender to bottom
TOP_BAR_H = 6.0             # of the medal is 10 cm
DISC_R = 16.5
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


def arc_text(text, cx, cy, r, size, fill, position="top", max_sweep=142.0):
    """Lay glyphs on a circle, one rotated <text> per glyph.

    Shrinks the type if the legend would otherwise wrap past max_sweep degrees
    and collide with the other legend or run off the rim.
    """
    if not text:
        return ""
    ss = 64
    font = ImageFont.truetype(FONT_PATH, size * ss)
    adv = [font.getlength(ch) / ss for ch in text]
    span = sum(adv)
    sweep = math.degrees(span / r)
    if sweep > max_sweep:                       # too long, scale it down
        size *= max_sweep / sweep
        font = ImageFont.truetype(FONT_PATH, max(1, int(size * ss)))
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
        out.append(f'<text x="{px:.3f}" y="{py:.3f}" font-family="{FONT_FAMILY}" '
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


def device_svg(kind, cx, cy, size, fill, weight=0.18):
    if kind == "anchor":
        return anchor_svg(cx, cy, size, fill, weight)
    return leaf_svg(cx, cy, size, fill, 1.0, weight=weight)


def metal_bar(x, y, w, h, metal, text=None, gid="m", fs=2.6, radius=None,
              ink=None, end_leaves=False):
    r = min(h * 0.28, 0.9) if radius is None else radius
    ink = ink or METALS[metal][0]
    s = (f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{r:.2f}" '
         f'fill="url(#{gid})" stroke="{OUTLINE}" stroke-width="0.3"/>')
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
                  f'font-family="{FONT_FAMILY}" font-weight="bold" font-size="{fs}" '
                  f'fill="{ink}" text-anchor="middle" '
                  f'letter-spacing="0.25">{esc(text)}</text>')
            if end_leaves:
                for lx in (x + w * 0.12, x + w * 0.88):
                    s += leaf_svg(lx, y + h * 0.5, h * 0.55, ink, 0.9)
    return s


# ---------------------------------------------------------------- ribbons --
def ribbon_svg(spec, devices=0, width_mm=35.0, height_mm=10.0,
               device_colours=None):
    body = stripes_svg(spec, 0, 0, width_mm, height_mm)
    if devices:
        # keep service devices on the central field, clear of the edge stripes
        field = width_mm * 0.60
        gap = field / devices
        size = min(height_mm * 0.62, gap * 0.86)
        x0 = (width_mm - field) / 2 + gap / 2
        cols = device_colours or [METALS["gold"][2]] * devices
        for i in range(devices):
            body += leaf_svg(x0 + gap * i, height_mm / 2, size,
                             cols[i % len(cols)], outline=True)
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
    for extra in mets:
        d.append(grad(f"bg_{extra}{u}", extra, vertical=True))
    d.append("</defs>")
    body = "".join(d)

    top = TOP_BAR_H if spec.get("top_bar") else 0.0
    body += stripes_svg(spec, 0, top, width_mm, RIBBON_BOTTOM - top)
    body += (f'<rect x="0" y="{top}" width="{width_mm}" height="{RIBBON_BOTTOM-top}" '
             f'fill="none" stroke="#00000055" stroke-width="0.3"/>')

    if spec.get("top_bar"):
        body += metal_bar(1.0, 0.4, width_mm - 2.0, TOP_BAR_H - 0.8, metal,
                          spec["top_bar"], gid="mgv"+u,
                          end_leaves=spec.get("bar_end_leaves", False))

    # service bars: ACLC Policy 13.1 para 12, one plain gold bar per extra
    # year of service, centred, stacking upward from the suspension
    if service_bars:
        m = spec.get("service_bar_metal", "gold")
        n = min(service_bars, spec.get("max_service_bars", 3))
        bh = 3.6
        for yb in bar_positions(n, top, RIBBON_BOTTOM, bh):
            body += metal_bar(3.0, yb, width_mm - 6.0, bh, m,
                              gid=f"bg_{m}{u}", radius=0.25)
            if spec.get("service_bar_device"):
                body += leaf_svg(width_mm / 2, yb + bh / 2, bh * 0.66,
                                 METALS[m][2], 1.0, weight=0.16)

    # award bars stack upward from just above the suspension
    want = bars if bars is not None else [b[0] for b in spec.get("award_bars", [])]
    if want:
        lookup = dict(spec.get("award_bars", []))
        order = [b[0] for b in spec.get("award_bars", [])]
        want = sorted(want, key=lambda l: order.index(l) if l in order else 0,
                      reverse=True)                     # senior bar on top
        bh = 5.2
        for label, yb in zip(want, bar_positions(
                len(want), top, RIBBON_BOTTOM, bh,
                spec.get("bar_band_frac"), spec.get("bar_max_pitch"))):
            m = lookup.get(label, "gold")
            body += metal_bar(1.2, yb, width_mm - 2.4, bh, m, label,
                              gid=f"bg_{m}{u}", fs=3.1,
                              ink=spec.get("bar_ink", {}).get(label, "#1F1F1F"))

    cx = width_mm / 2.0
    if spec["suspension"] == "ring":
        body += (f'<path d="M{cx-2.6},{SUSP_TOP} L{cx-2.6},{SUSP_TOP+1.4} '
                 f'L{cx+2.6},{SUSP_TOP+1.4} L{cx+2.6},{SUSP_TOP} Z" fill="url(#mg{u})" '
                 f'stroke="{METALS[metal][0]}" stroke-width="0.25"/>')
        body += (f'<circle cx="{cx}" cy="{SUSP_TOP+3.6}" r="2.5" fill="none" '
                 f'stroke="url(#mg{u})" stroke-width="1.5"/>')
    else:
        txt = spec.get("suspension_text")
        body += metal_bar(2.5, SUSP_TOP, width_mm - 5.0, SUSP_BOT - SUSP_TOP,
                          metal, txt, gid="mgv"+u, fs=2.5,
                          end_leaves=spec.get("bar_end_leaves", False))

    # lug joining the suspension to the medallion
    body += (f'<rect x="{cx-1.5:.2f}" y="{SUSP_BOT-0.6:.2f}" width="3" '
             f'height="{DISC_CY - DISC_R - SUSP_BOT + 1.4:.2f}" fill="url(#mgv{u})" '
             f'stroke="{METALS[metal][0]}" stroke-width="0.22"/>')

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
    if field:
        body += (f'<circle cx="{cx}" cy="{DISC_CY}" r="{DISC_R*0.90:.2f}" fill="{field}" '
                 f'stroke="{METALS[metal][0]}" stroke-width="0.3"/>')
        ink = DISC_INK
    else:
        body += (f'<circle cx="{cx}" cy="{DISC_CY}" r="{DISC_R*0.86:.2f}" fill="none" '
                 f'stroke="{METALS[metal][0]}" stroke-width="0.3" opacity="0.75"/>')
        ink = DISC_INK
    if spec.get("device"):
        # dark shade of the medal's own metal: reads as engraved and keeps
        # contrast on both light (silver) and dark (gold) faces
        body += device_svg(spec["device"], cx, DISC_CY, DISC_R * 0.92,
                           METALS[metal][0], weight=0.3)
    # a checkered border eats the outer band, so pull the legends inboard
    k = 0.72 if spec.get("disc_checker") else 1.0
    fs = 2.3 * (0.82 if spec.get("disc_checker") else 1.0)
    for line, pos, rf in ((spec.get("legend_top"), "top", 0.845),
                          (spec.get("legend_top2"), "top", 0.700),
                          (spec.get("legend_bottom"), "bottom", 0.845)):
        if line:
            body += arc_text(line, cx, DISC_CY, DISC_R * rf * k, fs, ink, pos,
                             max_sweep=134.0)
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

    def emit(key, svg, w_mm, h_mm, meta):
        open(f"{a.out}/svg/{key}.svg", "w").write(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=f"{a.out}/png/{key}.png",
                         output_width=round(w_mm * px), output_height=round(h_mm * px))
        entry = {"w_mm": round(w_mm, 2), "h_mm": round(h_mm, 2),
                 "aspect": round(w_mm / h_mm, 4),
                 "png": f"png/{key}.png", "svg": f"svg/{key}.svg"}
        entry.update(meta)
        manifest[key] = entry

    def meta_for(key, spec, extra=None):
        m = {k: spec.get(k) for k in
             ("name", "authority", "precedence", "fidelity", "source")}
        m["true_ribbon_width_mm"] = spec.get("ribbon_width_mm")
        if spec.get("ribbon_width_mm") not in (None, W):
            m["width_note"] = (
                f"Issued ribbon is {spec['ribbon_width_mm']} mm. Rendered at "
                f"{W:.0f} mm: LOCAL DECISION so ribbon rows stay aligned.")
        if extra:
            m.update(extra)
        return m

    # ---- ribbons and medals, one per key, always rendered 35 mm wide ------
    for key, spec in MEDALS.items():
        if key == "acmm":
            continue                       # never worn bare, see below
        emit(f"ribbon_{key}", ribbon_svg(spec, width_mm=W), W, 10.0,
             meta_for(key, spec))
        emit(f"medal_{key}", medal_svg(spec, width_mm=W), W, H,
             meta_for(key, spec))

    # ---- Army Cadet Service Medal, years 4 to 7 (Policy 13.1 para 12) ----
    acsm = MEDALS["armyservice"]
    for years in range(5, 5 + acsm["max_service_bars"]):
        n = years - 4
        note = {"variant": f"{years} years of service, {n} bar"
                           f"{'s' if n > 1 else ''}"}
        emit(f"ribbon_armyservice_{years}yr",
             ribbon_svg(acsm, devices=n, width_mm=W), W, 10.0,
             meta_for("armyservice", acsm, note))
        emit(f"medal_armyservice_{years}yr",
             medal_svg(acsm, width_mm=W, service_bars=n), W, H,
             meta_for("armyservice", acsm, note))

    # ---- ACMM, the 11 wearable bar states --------------------------------
    acmm = MEDALS["acmm"]
    dev = acmm["bar_devices"]
    for code, bars in acmm_states():
        note = {"variant": "bars: " + ", ".join(bars)}
        emit(f"medal_acmm_{code}", medal_svg(acmm, bars=bars, width_mm=W), W, H,
             meta_for("acmm", acmm, note))
        emit(f"ribbon_acmm_{code}",
             ribbon_svg(acmm, devices=len(bars), width_mm=W,
                        device_colours=[dev[b] for b in bars]), W, 10.0,
             meta_for("acmm", acmm, note))

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
