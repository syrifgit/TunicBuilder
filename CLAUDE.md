# Working on this project

Context for a fresh session. Read this, then `rules/army_tunic_placement_rules_2.json`,
then `TODO.md`. `README.md` is written for a human picking the repo up; this file is
about how to *change* it without breaking it.

## What it is

A tool that works out where every badge goes on a Royal Canadian Army Cadet tunic and
states each position as a measurement someone can take with a ruler. One cadet at a
time, entered by hand. Output is a dimensioned check drawing, printing on two sheets.

`demo/tunic.template.html` is the tool. Everything else exists to feed it artwork or
to justify a number in it.

## The prime directive

**Flag discrepancies. Never reconcile them silently.**

The sources contradict each other, repeatedly. When they do, the fix is to record the
conflict in the rules pack — the field, the alternative value, the source of each, and
the reasoning for what was adopted — and to surface it in the validator. It is never to
quietly pick one and move on.

Six conflicts are recorded so far. Where an illustration argued with an instruction,
the illustration lost every time:

| Slot | Conflict | Adopted |
|---|---|---|
| `proficiency_stack` | Annex H says 12 cm | CH3S1 3.b.(5) → 20 cm |
| `marksmanship` | poster draws ~0.73–0.86 cm | CH3S1 3.b.(6) → 0.5 cm |
| `ctc_grid` | Annex H text describes a 5-badge stagger | CH3S1 3.b.(9) → aligned 2×3 |
| `front_right_expedition` | workbook says left pocket | CH5-B figure → right pocket |
| `right_commendation_stack` | 5D-1 says national goes left | Ch5 → one right-hand stack |
| `right_commendation_stack` | 10050 ranks a VCDS Commendation | Ch5 → "Command Commendation" |

**The commendation split needs a decision before anyone prints a guide.** The stack was
adopted as one right-hand run against Figure 5D-1. CJCR Gp O 10050 para 7.5 now
corroborates 5D-1 — CDS and VCDS marked "(to be worn on the left side)" — so two
independent sources say national goes left and the renderer is drawing it right. That
puts a CDS Commendation on the wrong side of a cadet. See `TODO.md` §1.

Note that the two sources disagreeing here are a cadet instruction and a *JCR* order.
10050 is used for **order, not geometry**: its precedence lists are CJCR-wide (para 4.2,
and 7.4 spans all three elements), but every figure it gives is for the JCR sweatshirt.

## Three rules learned the hard way

1. **Artwork identifies badges. It does not dimension them.** Poster aspect ratios were
   used to infer a marksmanship rifle width of 5.5 cm. The real badge is 6.0 cm — 8%
   out. The poster is not drawn to a single scale either: 13 to 24 points per cm
   depending on which family you measure. Within one band the comparison is fair;
   across bands it is not.
2. **Poster captions are a hint, not an identity.** The extractor reads whatever text
   sits under a badge, which produced "Canadian Armed Forces" for the parachutist wings
   and "Maple Leaf" for the Maple Leaf Exchange. `data/labels.py` is authoritative and
   was confirmed visually, badge by badge.
3. **Where the instruction and the illustration disagree, the instruction governs.**

## The coordinate model

One axis per surface. Nothing measures in two directions at once.

- **Sleeves** — `y` in cm upward from the cuff bottom edge, `x` front-positive from the
  sleeve centre. The shoulder seam is simply `y = sleeve length`, so nothing ever
  measures downward internally.
- **Front** — `y` in cm upward from each pocket's top edge, `x` inboard-positive.
  Negative `y` is on the pocket, where the pinned insignia go.

Front/rear and inboard/outboard become image-left/right **exactly once**, at draw time,
in `drawSleeve` and `drawPocket`. Get that wrong and the whole block mirrors.

**Two datum families, and it matters.** On the sleeve, the corps title, the RCAC badge
and the LCpl–Sgt chevrons measure *down from the shoulder seam*; everything else
measures *up from the cuff*. The distance between the families is the sleeve length, so
the gap between a shoulder-referenced badge and a cuff-referenced one changes with tunic
size. A Sgt who is also Drum Major has 2.00 cm clearance at 57 cm and an overlap below
55 cm. Never quote a cross-family figure as if it were fixed.

**Absolute or relative.** A badge is quoted absolutely only where the regulation gives a
fixed anchor. Everything else is a gap from what it hangs off, because that is the
measurement actually taken: *"bottom edge 1.00 cm above the training level star"*, not
"9.71 cm from the cuff".

## How to make a change

```bash
python build_all.py      # regenerates artwork, both pages, and smoke-tests them
```

- **Edit `demo/*.template.html`, never the built `.html`.** The built files are
  generated and gitignored.
- `build_all.py` runs the whole pipeline and finishes with `demo/check.js`, which
  executes the built pages against a stub DOM.
- **`check.js` cannot see CSS.** No layout, no cascade, no specificity. A page that
  builds a perfect SVG and then hides it behind a losing CSS rule passes clean. That
  has happened. For any CSS change, verify in a real browser:
  ```
  chrome --headless=new --disable-gpu --dump-dom <file>          # did it render
  chrome --headless=new --no-pdf-header-footer --print-to-pdf=x.pdf <file>   # pagination
  ```
- **Assert every string replacement.** Patching the template with
  `s.replace(old, new)` and no check has silently missed twice in this project, both
  times reported as success. If you script an edit, `assert old in s` per replacement,
  and probe for the *declaration* afterwards, not merely the string.
- **Delete one-time scripts once applied.** Their effect lives in the template or the
  rules pack; leaving them around invites someone to run one twice. 27 have been
  deleted this way.
- **Sleeve slot ids are semantic, never positional.** `marksmanship`, not
  `left_marksmanship`. Which arm a slot lands on is the element's business and lives in
  `ELEMENTS[...].sleeves`, because that is exactly what differs between elements: Army
  wears rank right, Sea left, Air both. `put(slot, box)` in `resolve()` is the only
  place a slot meets a side. Breast slots keep their side, which is anatomical.
- **`docs/` is a release, not a build step.** `build_all.py` writes `demo/` and does
  not touch `docs/`; only `build_site.py` does. Run it and commit when you want to
  publish, not on every rebuild. The pages are ~7 MB of base64 that compresses to 74%
  and cannot be delta'd, so every committed rebuild is ~5 MB of permanent history.
- **Two build outputs per page.** `tunic.html` is artifact-shaped — page content with no
  doctype, html, head or body, because the Artifact tool supplies that skeleton.
  `tunic.local.html` is a complete document for local work. A fragment is not a
  document: Live Server injects its live-reload client by looking for `</body>`, and
  with none to find, the page's own scripts stop running. Symptom is correct styling,
  no console errors, and nothing populated.

## Constraints

- **No cadet data lives here, and none should arrive.** `242 Qualifications Data.xlsx`
  is Protected A — cadet names, ranks, qualifications — and has been moved out of this
  directory. Nothing tracked reads it and `.gitignore` still excludes `*.xlsx` so a
  stray copy cannot be committed. The workbook notes in `TODO.md` §4 describe it from
  memory; go to wherever it now lives to act on them. Synthesise test data, never
  borrow real.
- **Badge artwork is Crown copyright** (A-CR-CCP-750/DA-003), and is **cleared for
  publication as part of the tool**. `docs/` is tracked and both pages attribute it.
  The clearance stops there: the poster PDF, `rcac_badges.zip` and `art/*` are the
  artwork as a *library* rather than as a tool, and stay out of the repo. Do not
  commit them, and do not add the raw crops to a page just to make them downloadable.
- **Git: commit locally, freely. Never push, never add a remote, never
  `gh repo create`** without being asked. There is deliberately no remote configured.
  Use the repo's configured identity, do not override it with `-c user.name=...`.
- **Every geometric claim needs a citation.** A drawing someone sews from has to be
  defensible when they ask why a badge is at 20 cm.

## Layout

```
rules/    army_tunic_placement_rules_2.json   source of truth. Start here.
data/     labels.py       slug -> confirmed identity. Beats manifest.csv captions.
          badge_map.csv   generated from labels.py
          manifest.csv    output of extract_badges.py
src/      extract_badges.py   poster PDF -> badge artwork
          recut_*.py          recover badges the extractor merged or skipped
          build_art.py        pack artwork for the tool
          build_plate.py      pack artwork for the identification sheet
          build_badge_map.py  labels.py -> badge_map.csv
          poster_scale.py     one-off: is the poster to one scale (no)
demo/     tunic.template.html   the tool
          plate.template.html   the identification sheet
          check.js              executes a built page against a stub DOM
notes/    CLAUDE_1.md     the original brief. Partly superseded — see below.
docs/     build_site.py output. Gitignored; GitHub Pages would serve it.
```

`notes/CLAUDE_1.md` is the founding brief and still useful for background, but its
*Settled decisions* list has been corrected in at least one place (ALP cadets wear the
Gold Star; they were previously recorded as wearing none). Treat the rules pack as
current and the brief as history.

## The extractor's two failure modes

`extract_badges.py` clusters **vector** drawing objects. Both failures follow from that:

1. **It merges adjacent artwork into one crop.** Music levels 2–4, the corps title with
   the RCAC badge, the marksmanship numeral with its rifles. Fixed by
   `recut_music.py`, `recut_shoulder.py`, `recut_marksmanship.py`.
2. **It drops whole regions.** Anything raster is invisible to it — the entire Physical
   Fitness block, all the competition and expedition pins, and the seven medals which
   are *still* missing. Fixed by `recut_fitness.py` and `recut_pins.py`, which render a
   strip from the PDF and segment on alpha.

Both are the same repair: render the region, segment on the alpha channel, trim to the
true bounding box. Copy `recut_pins.py` for anything else that turns up missing.

A proper fix — folding alpha segmentation into `extract_badges.py` and re-running the
whole poster — has not been done. The `recut_*.py` scripts are the accumulated
workaround, and they are all in the pipeline.

## Where things stand

Rules **v0.21-draft**: 20 slots, 31 open questions, 6 conflicts, sources CH3S1,
ANNEX-H, CH5-A–D, CH5-S7, CH4-A, CJCRGPO-10050 and CATO 13-16 (para 19 now sourced
verbatim, confirming the precedence for every medal but the Order of St. George).

Sleeves are complete: every badge has artwork and a resolved position. The front is
modelled and placed but several sizes are placeholders. `TODO.md` has the full list,
ordered by what it unblocks.
