#!/usr/bin/env python3
"""Assemble the static site into docs/, ready for GitHub Pages.

Both pages are already single self-contained files with the artwork inlined, so a
static host needs nothing but the files themselves - no server, no build step, no
runtime dependency beyond the Google Fonts stylesheet.

docs/ rather than site/ because GitHub Pages will only publish from a branch root or
from /docs. Pages serves master -> /docs, and the layout tool is the site root.

The built pages are tracked: the artwork they carry is cleared for publication as part
of the tool. The poster PDF and the raw badge library are not, and stay ignored.
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "docs")
PAGES = [("demo/tunic.local.html", "index.html", "the layout tool"),
         ("demo/plate.local.html", "plate.html", "the badge identification sheet"),
         # The artwork the two pages load. Kept out of the HTML on purpose: the pages
         # change often and are small, these change almost never and are large, so a
         # normal commit no longer rewrites megabytes of base64.
         ("demo/tunic_art.js", "tunic_art.js", "artwork for the layout tool"),
         ("demo/plate_art.js", "plate_art.js", "artwork for the identification sheet")]

# GitHub Pages runs Jekyll by default, which skips files and folders starting with
# an underscore. Nothing here does, but the marker costs nothing and removes a
# whole class of surprise.
NOJEKYLL = ""

# The publication clearance on record named A-CR-CCP-750/DA-003, the army poster. Air
# artwork comes from its sibling, A-CR-CCP-850/DA-003. Lt Beal, 2026-09-24: "they are
# basically the same poster", and it went public with the 2026-09-24 release on Lt
# Beal's direction. So it ships.
# Set this back to False if that changes; a release carrying Air art then stops here.
AIR_ART_CLEARED = True


def main():
    art = os.path.join(ROOT, "demo", "tunic_art.js")
    has_air = os.path.exists(art) and "AIR_ART" in open(art, encoding="utf-8").read()
    if has_air and not AIR_ART_CLEARED:
        print("demo/tunic_art.js carries Air artwork from A-CR-CCP-850/DA-003, and the")
        print("clearance on record covers A-CR-CCP-750/DA-003 only. Confirm it extends")
        print("to the Air poster, set AIR_ART_CLEARED in build_site.py, and re-run.")
        return 1

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

    print(f"\ndocs/ ready, {total/1e6:.2f} MB total. Serve the folder as-is, or:")
    print("  python -m http.server -d docs 8000     # check it over HTTP first")
    print("\nTo publish on GitHub Pages:")
    print("  1. commit these files - they are tracked")
    print("  2. push: the repo is syrifgit/TunicBuilder, and the local clone has no")
    print("     remote on purpose, so push to its URL (ask first)")
    print("  3. Pages serves master -> /docs")
    print("The layout tool lands at the site root; the plate at /plate.html.")
    print("\nBoth pages carry Crown copyright artwork from A-CR-CCP-750/DA-003,")
    print("cleared for publication as part of the tool, and both attribute it. The")
    print("poster itself and the raw badge library are NOT cleared and stay ignored.")
    if has_air:
        print("The layout tool also carries Air artwork from A-CR-CCP-850/DA-003.")
    print("And the medal artwork, faces traced from supplied emblem artwork: published")
    print("as rendered in the tool; the pack and its traced sources stay local.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
