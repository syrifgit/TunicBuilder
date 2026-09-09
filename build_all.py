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
NEEDED = ["rcac_badges.zip"]
RULES = os.path.join(ROOT, "rules", "army_tunic_placement_rules_2.json")

# Two steps render regions straight out of the poster PDF, because the extractor only
# sees vector objects and these are photographs. Their output is 16 PNGs in art/recut,
# which are gitignored like the rest of the artwork - so if the PDF goes and those PNGs
# go, these badges cannot be regenerated from anything in the repo.
#
# The PDF is a national publication and can be fetched again, so it does not have to
# live here. Keep the artwork and these steps skip themselves; lose both and the build
# stops rather than quietly producing pages missing sixteen badges.
PDF = "ACRCCP750DA003.pdf"
PDF_STEPS = {
    "src/recut_fitness.py": ["fit_bronze", "fit_silver", "fit_gold", "fit_excellence"],
    "src/recut_pins.py": ["comp_mk_zone", "comp_mk_prov", "comp_mk_nat", "comp_mk_winner",
                          "comp_bi_zone", "comp_bi_prov", "comp_bi_nat", "comp_bi_winner",
                          "pin_rifle_team", "pin_belzile",
                          "exped_regional", "exped_national"],
}

STEPS = [
    ("src/recut_music.py",        "recover music levels 2-4 from a merged crop"),
    ("src/recut_shoulder.py",     "split corps title from RCAC badge"),
    ("src/recut_marksmanship.py", "split rifles from numeral"),
    ("src/recut_fitness.py",      "pull fitness badges off the source PDF"),
    ("src/recut_pins.py",         "pull competition and expedition pins off the PDF"),
    ("src/repack_medals.py",      "medal pack PNG -> WebP"),
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

    have_pdf = os.path.exists(PDF)
    width = max(len(s) for s, _ in STEPS)
    for script, what in STEPS:
        if script in PDF_STEPS and not have_pdf:
            missing = [n for n in PDF_STEPS[script]
                       if not os.path.exists(os.path.join(ROOT, "art", "recut", n + ".png"))]
            if missing:
                print(f"\n\033[1m{script:<{width}}\033[0m  {what}")
                print(f"    {PDF} is gone and so is its output: "
                      f"{', '.join(missing[:4])}{' ...' if len(missing) > 4 else ''}")
                print(f"    {len(missing)} badge(s) cannot be regenerated. Restore the PDF "
                      f"(a national publication) and re-run.")
                return 1
            print(f"\n\033[2m{script:<{width}}\033[0m  skipped, no PDF; "
                  f"{len(PDF_STEPS[script])} existing crops kept")
            continue
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
