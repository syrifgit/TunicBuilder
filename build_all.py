#!/usr/bin/env python3
"""Regenerate everything: artwork packs, badge map, and both HTML pages.

Run from the repo root. Needs ACRCCP750DA003.pdf and rcac_badges.zip present -
see the README. Safe to re-run; every step overwrites its own output.
"""
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
NEEDED = ["rcac_badges.zip", "ACRCCP750DA003.pdf"]
RULES = os.path.join(ROOT, "rules", "army_tunic_placement_rules_2.json")

STEPS = [
    ("src/recut_music.py",        "recover music levels 2-4 from a merged crop"),
    ("src/recut_shoulder.py",     "split corps title from RCAC badge"),
    ("src/recut_marksmanship.py", "split rifles from numeral"),
    ("src/recut_fitness.py",      "pull fitness badges off the source PDF"),
    ("src/recut_pins.py",         "pull competition and expedition pins off the PDF"),
    ("src/build_art.py",          "pack artwork for the layout tool"),
    ("src/build_plate.py",        "pack artwork for the identification sheet"),
    ("src/build_badge_map.py",    "labels.py -> data/badge_map.csv"),
    ("demo/build.py",             "build demo/tunic.html"),
    ("demo/build_plate_html.py",  "build demo/plate.html"),
]


def check_doc_headers(width=0):
    """TODO.md and CLAUDE.md each quote the rules pack's counts in a status line.
    Those are written by hand and have gone stale three times, every time caught by
    eye rather than by anything. Reports; does not fail the build."""
    r = json.load(open(RULES, encoding="utf-8"))
    want = (r["version"], len(r["slots"]), len(r["open_questions"]),
            sum(len(s.get("conflicts", [])) for s in r["slots"]))
    pat = re.compile(r"\*\*v?([\d.]+-draft)\*\*[:,]? (\d+) slots, (\d+) open questions?, "
                     r"(\d+)(?: recorded)? conflicts?")
    print(f"\n\033[1m{'doc headers':<{width}}\033[0m  TODO.md and CLAUDE.md vs the rules pack")
    stale = 0
    for name in ("TODO.md", "CLAUDE.md"):
        m = pat.search(open(os.path.join(ROOT, name), encoding="utf-8").read())
        if not m:
            print(f"    {name}: no status line found")
            stale += 1
        elif (m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))) != want:
            print(f"    {name}: STALE - says {m.group(1)}, "
                  f"{m.group(2)} slots, {m.group(3)} open questions, {m.group(4)} conflicts")
            stale += 1
        else:
            print(f"    {name}: current")
    if stale:
        print(f"    rules pack is v{want[0]}: {want[1]} slots, {want[2]} open questions, "
              f"{want[3]} conflicts")
    return stale


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

    # Parsing is not running. A refactor that drops a function still passes
    # `node --check`, then throws on load and leaves a blank page - so execute the
    # built pages against a stub DOM if node is available.
    node = shutil.which("node")
    if node:
        print(f"\n\033[1m{'smoke test':<{width}}\033[0m  execute both built pages")
        r = subprocess.run([node, "check.js", "tunic.html", "plate.html"],
                           cwd=os.path.join(ROOT, "demo"),
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        for line in ((r.stdout or "") + (r.stderr or "")).splitlines():
            print("   ", line)
        if r.returncode != 0:
            return r.returncode
    else:
        print("\nnode not found, skipping the smoke test. The pages are built but "
              "have not been executed.")

    check_doc_headers(width)

    print("\nDone. Open demo/tunic.html or demo/plate.html.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
