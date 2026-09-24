#!/usr/bin/env python3
"""Generate src/bird_path.txt - the spread-wing eagle for the Air service bar.

STYLISED. The real bar IS printed on A-CR-CCP-850/DA-003 but the embedded
image is 422x98 px of gold relief on a gold face; both a luminance threshold
and a local-variance segmentation produced unusable blobs. Drawn to the
proportions of that image (wingspan:height about 3.1:1, wings swept slightly
up from the shoulder, four primary feather notches) rather than traced.
"""
import math

W_ROOT_X, W_TIP_X = 0.502, 0.990
ROOT_Y, TIP_Y = 0.082, 0.026
CHORD_ROOT, CHORD_TIP = 0.128, 0.004
NOTCHES = 5
N = 96


def lead(t):
    x = W_ROOT_X + t * (W_TIP_X - W_ROOT_X)
    y = ROOT_Y + (TIP_Y - ROOT_Y) * (1 - (1 - t) ** 1.7)
    return x, y


def trail(t):
    x, y = lead(t)
    chord = CHORD_ROOT + (CHORD_TIP - CHORD_ROOT) * (t ** 0.62)
    ripple = 0.017 * (1 - t) ** 0.6 * max(0.0, math.sin(NOTCHES * math.pi * t))
    return x, y + chord + ripple


def wing(mirror=False):
    pts = [lead(i / N) for i in range(N + 1)]
    pts += [trail(1 - i / N) for i in range(N + 1)]
    if mirror:
        # mirroring flips the winding; reverse so every subpath stays
        # clockwise, or nonzero fill cancels where wings cross the body
        pts = [(1.0 - x, y) for x, y in pts][::-1]
    d = "M%.4f,%.4f " % pts[0] + " ".join("L%.4f,%.4f" % p for p in pts[1:]) + "Z"
    return d


def body():
    # head, shoulders, breast and a notched tail, symmetric about x = 0.5
    return ("M0.500,0.018 C0.528,0.018 0.543,0.040 0.540,0.064 "
            "C0.560,0.072 0.571,0.090 0.573,0.114 "
            "C0.570,0.160 0.552,0.210 0.530,0.244 "
            "L0.552,0.302 L0.500,0.276 L0.448,0.302 L0.470,0.244 "
            "C0.448,0.210 0.430,0.160 0.427,0.114 "
            "C0.429,0.090 0.440,0.072 0.460,0.064 "
            "C0.457,0.040 0.472,0.018 0.500,0.018 Z")


if __name__ == "__main__":
    d = wing() + wing(mirror=True) + body()
    open("src/bird_path.txt", "w").write(d)
    print("bird path chars", len(d))
