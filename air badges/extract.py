#!/usr/bin/env python3
"""Extract Air cadet badges from A-CR-CCP-850/DA-003 into air_art_pack.js.

Regions come from alpha segmentation of the rendered page, not from vector
object clustering, so raster-backed badges survive (see NOTES: 11 of the
badges requested by name are raster).
"""
import base64
import io
import json

import numpy as np
import pymupdf
from PIL import Image
from scipy import ndimage

from keymap import ROWS, RASTER_PPI

WHITE_T = 222      # min-channel at or above this counts as paper


def key_white_ground(im):
    """Key the white paper out of a scanned badge.

    The three Effective Speaking badges are photographs on white. Their PDF
    smask is a plain rectangle, so page alpha leaves the corners opaque and the
    badge draws as a white square.

    Paper is flood-filled inward from the frame, so the badge's own cream
    interior is kept. The frame itself is the clip's transparent bleed, so the
    fill has to treat already-transparent pixels as passable or it never
    reaches the paper. Fringe pixels then get the white divided back out so no
    pale halo is left behind.
    """
    arr = np.array(im.convert("RGBA"))
    rgb = arr[:, :, :3].astype(float)
    a0 = arr[:, :, 3].astype(float) / 255.0
    minch = rgb.min(axis=2)

    passable = (minch >= WHITE_T) | (a0 < 0.03)
    seed = np.zeros_like(passable)
    seed[0, :] = seed[-1, :] = seed[:, 0] = seed[:, -1] = True
    bg = ndimage.binary_propagation(seed & passable, mask=passable)

    soft = np.clip((255.0 - minch) / (255.0 - WHITE_T), 0, 1)
    alpha = np.where(bg, soft, 1.0)
    ring = ndimage.binary_dilation(bg, np.ones((3, 3))) & ~bg
    alpha[ring] = np.minimum(alpha[ring], 0.5 + 0.5 * soft[ring])
    alpha *= a0

    part = (alpha > 0.02) & (alpha < 0.98)
    out = rgb.copy()
    out[part] = np.clip((rgb[part] - (1 - alpha[part])[:, None] * 255.0)
                        / alpha[part][:, None], 0, 255)
    return Image.fromarray(np.dstack([out, alpha * 255]).astype(np.uint8), "RGBA")


PDF = "/mnt/user-data/uploads/ACRCCP850DA003.pdf"
LONG_EDGE = 420
PAD = 1.0          # pt of bleed around the blob before trimming

doc = pymupdf.open(PDF)
page = doc[0]
words = [pymupdf.Rect(w[:4]) for w in page.get_text("words")]
mapping = json.load(open("mapping.json"))

pack, manifest, report = {}, {}, []

for key, (bx0, by0, bx1, by1, _px) in mapping.items():
    blob = pymupdf.Rect(bx0, by0, bx1, by1)
    clip = pymupdf.Rect(bx0 - PAD, by0 - PAD, bx1 + PAD, by1 + PAD)

    # Caption guard: a text run that pokes into the clip but is not part of the
    # badge would be baked in. Music numerals ARE live text inside the blob, so
    # only text outside the blob counts as contamination.
    bleed = [w for w in words if w.intersects(clip) and not blob.contains(w)]
    if bleed:
        report.append(f"{key}: {len(bleed)} text run(s) in bleed, padding dropped")
        clip = pymupdf.Rect(blob)

    long_pt = max(clip.width, clip.height)
    zoom = LONG_EDGE / long_pt
    if key in RASTER_PPI:                      # do not upsample scanned art
        zoom = min(zoom, RASTER_PPI[key] / 72.0)

    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip, alpha=True)
    im = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)

    if key in RASTER_PPI:
        im = key_white_ground(im)

    a = np.array(im)[:, :, 3]
    ys, xs = np.nonzero(a > 8)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))   # trim to alpha

    if max(im.size) > LONG_EDGE:
        s = LONG_EDGE / max(im.size)
        im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))),
                       Image.LANCZOS)

    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=90, method=4)
    pack[key] = {"d": base64.b64encode(buf.getvalue()).decode(),
                 "aspect": round(im.width / im.height, 4),
                 "m": "image/webp"}
    manifest[key] = {
        "px": [im.width, im.height],
        "aspect": round(im.width / im.height, 4),
        "source": "A-CR-CCP-850/DA-003 p1",
        "region_pt": [round(v, 1) for v in (bx0, by0, bx1, by1)],
        "art": "raster" if key in RASTER_PPI else "vector",
        "bytes": buf.tell(),
    }
    im.save(f"out_png/{key}.png")

print(f"extracted {len(pack)}")
for r in report:
    print("  note:", r)
json.dump(pack, open("pack.json", "w"))
json.dump(manifest, open("manifest.json", "w"))
