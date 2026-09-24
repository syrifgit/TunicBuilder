#!/usr/bin/env python3
"""Alpha-segment A-CR-CCP-850/DA-003 into badge blobs and map them to keys."""
import json
import numpy as np
import pymupdf
from scipy import ndimage
from keymap import ROWS

PDF = "/mnt/user-data/uploads/ACRCCP850DA003.pdf"
Z = 150 / 72.0

page = pymupdf.open(PDF)[0]
pix = page.get_pixmap(matrix=pymupdf.Matrix(Z, Z), alpha=True)
a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)
mask = a[:, :, -1] > 8

# blank text so captions cannot form blobs (the extraction render keeps text,
# which is what preserves the live Music numerals)
for x0, y0, x1, y1, *_ in page.get_text("words"):
    mask[max(0, int(y0*Z)-2):int(y1*Z)+3, max(0, int(x0*Z)-2):int(x1*Z)+3] = False

lab, _ = ndimage.label(ndimage.binary_dilation(mask, np.ones((11, 11))))
blobs = []
for i, sl in enumerate(ndimage.find_objects(lab)):
    ys, xs = sl
    if (xs.stop-xs.start) < 20 or (ys.stop-ys.start) < 20:
        continue
    sub = (lab[sl] == i+1) & mask[sl]
    if sub.sum() < 250:
        continue
    blobs.append([xs.start/Z, ys.start/Z, xs.stop/Z, ys.stop/Z, int(sub.sum())])

mapping, missing = {}, []
for y0, y1, x0, x1, keys in ROWS:
    sel = sorted((b for b in blobs
                  if b[1] >= y0 and b[3] <= y1 and b[0] >= x0 and b[2] <= x1),
                 key=lambda b: b[0])
    if len(sel) != len(keys):
        missing.append((y0, y1, len(sel), len(keys)))
        continue
    mapping.update(zip(keys, sel))

print(f"blobs {len(blobs)} | mapped {len(mapping)}")
for m in missing:
    print("  !! row", m)
json.dump(mapping, open("mapping.json", "w"))
