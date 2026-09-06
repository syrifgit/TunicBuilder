#!/usr/bin/env python3
"""Regenerate everything: artwork packs, badge map, and both HTML pages.

Run from the repo root. Needs ACRCCP750DA003.pdf and rcac_badges.zip present -
see the README. Safe to re-run; every step overwrites its own output.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
NEEDED = ["rcac_badges.zip", "ACRCCP750DA003.pdf"]

STEPS = [
    ("src/recut_music.py",        "recover music levels 2-4 from a merged crop"),
    ("src/recut_shoulder.py",     "split corps title from RCAC badge"),
    ("src/recut_marksmanship.py", "split rifles from numeral"),
    ("src/recut_fitness.py",      "pull fitness badges off the source PDF"),
    ("src/build_art.py",          "pack artwork for the layout tool"),
    ("src/build_plate.py",        "pack artwork for the identification sheet"),
    ("src/build_badge_map.py",    "labels.py -> data/badge_map.csv"),
    ("demo/build.py",             "build demo/tunic.html"),
    ("demo/build_plate_html.py",  "build demo/plate.html"),
]


def main():
    os.chdir(ROOT)
    missing = [f for f in NEEDED if not os.path.exists(f)]
    if missing:
        print("Missing source files, see the README:")
        for f in missing:
            print("   ", f)
        return 1

    width = max(len(s) for s, _ in STEPS)
    for script, what in STEPS:
        print(f"\n\033[1m{script:<{width}}\033[0m  {what}")
        r = subprocess.run([sys.executable, os.path.basename(script)],
                           cwd=os.path.join(ROOT, os.path.dirname(script)),
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        for line in (r.stdout or "").splitlines()[:4]:
            print("   ", line)
        if r.returncode != 0:
            print("FAILED:")
            print((r.stderr or "").strip()[-1500:])
            return r.returncode

    print("\nDone. Open demo/tunic.html or demo/plate.html.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
