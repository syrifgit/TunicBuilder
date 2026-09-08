#!/usr/bin/env python3
"""Assemble a static site: site/index.html plus the badge plate.

Both pages are already single self-contained files with the artwork inlined, so a
static host needs nothing but the files themselves - no server, no build step, no
runtime dependency beyond the Google Fonts stylesheet.

BEFORE PUBLISHING ANYWHERE PUBLIC, read the copyright note this prints. The pages
carry Crown copyright badge artwork inlined, and GitHub Pages on a free account
serves from a PUBLIC repository.
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
PAGES = [("demo/tunic.local.html", "index.html", "the layout tool"),
         ("demo/plate.local.html", "plate.html", "the badge identification sheet")]

# GitHub Pages runs Jekyll by default, which skips files and folders starting with
# an underscore. Nothing here does, but the marker costs nothing and removes a
# whole class of surprise.
NOJEKYLL = ""


def main():
    os.makedirs(SITE, exist_ok=True)
    open(os.path.join(SITE, ".nojekyll"), "w").write(NOJEKYLL)

    total = 0
    for src, dest, what in PAGES:
        s = os.path.join(ROOT, src)
        if not os.path.exists(s):
            print(f"missing {src} - run build_all.py first")
            return 1
        d = os.path.join(SITE, dest)
        shutil.copyfile(s, d)
        size = os.path.getsize(d)
        total += size
        print(f"  {dest:12} {size/1e6:5.2f} MB  {what}")

    print(f"\nsite/ ready, {total/1e6:.2f} MB total. Serve the folder as-is.")
    print("\n" + "!" * 72)
    print("COPYRIGHT: both pages carry Crown copyright badge artwork inlined, from")
    print("A-CR-CCP-750/DA-003. That is fine for internal corps use. Publishing to a")
    print("PUBLIC host redistributes it. GitHub Pages on a free account serves from a")
    print("public repository, so that route publishes the artwork. Settle this before")
    print("pushing anywhere public - see README.")
    print("!" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
