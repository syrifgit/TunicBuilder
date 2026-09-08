#!/usr/bin/env python3
"""Assemble the static site into docs/, ready for GitHub Pages.

Both pages are already single self-contained files with the artwork inlined, so a
static host needs nothing but the files themselves - no server, no build step, no
runtime dependency beyond the Google Fonts stylesheet.

docs/ rather than site/ because GitHub Pages will only publish from a branch root or
from /docs. Point Pages at main -> /docs and the layout tool is the site root.

The built pages are gitignored by default, because publishing them is a decision
rather than a build step - see the copyright note this prints.
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "docs")
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

    print(f"\ndocs/ ready, {total/1e6:.2f} MB total. Serve the folder as-is, or:")
    print("  python -m http.server -d docs 8000     # check it over HTTP first")
    print("\nTo publish on GitHub Pages, in order:")
    print("  1. settle the copyright question below")
    print("  2. drop the docs/ lines from .gitignore and commit the built pages")
    print("  3. add a remote and push - neither is set up, deliberately")
    print("  4. repo Settings > Pages > Source: main, folder /docs")
    print("The layout tool lands at the site root; the plate at /plate.html.")

    print("\n" + "!" * 72)
    print("COPYRIGHT: both pages carry Crown copyright badge artwork inlined, from")
    print("A-CR-CCP-750/DA-003. That is fine for internal corps use. Publishing to a")
    print("PUBLIC host redistributes it. GitHub Pages on a free account serves from a")
    print("public repository, so that route publishes the artwork - and committing")
    print("these files puts it in the repo whether or not Pages is ever switched on.")
    print("Settle this before either step. See README.")
    print("!" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
