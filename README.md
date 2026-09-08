# Cadet Tunic Layout

Works out where every badge goes on a Royal Canadian Army Cadet tunic, and how far
that is from something you can put a ruler on.

Give it one cadet's insignia and it draws both sleeves and the front to scale,
dimensioned: each badge carries the measurement you actually take - from the cuff,
from the shoulder seam, from the pocket top, or as a gap from the badge it hangs
off. It prints on two landscape sheets, sleeves then pockets.

Built for 242 RCACC (Fredericton) but the placement rules are national, so it should
work for any army cadet corps.

## Why it exists

The dress instructions state placement in prose, spread across Chapter 3 Section 1,
Chapter 3 Annex H, Chapter 4 Annex A and Chapter 5 Annexes A-D. Some of it is
contradictory. Turning "the chevron tips shall be 1 cm below the RCAC badge" into
"top edge 13.00 cm down from the shoulder seam" by hand, for 88 cadets, is where
mistakes come from.

Every geometric claim in `rules/army_tunic_placement_rules_2.json` carries a
citation. Where the sources disagree, the file records the conflict, the alternative
value, and the reasoning for what was adopted - rather than silently picking one.
There are six such conflicts so far.

## Just want to use it

Open **`docs/index.html`**. Double-click it - there is nothing to install, build or
serve. It is a complete self-contained page with every badge inlined, and it is
committed, so a clone or a ZIP download runs straight away.

`docs/plate.html` is the badge identification sheet, same deal.

The only network request either page makes is the webfont; both work offline without
it, just in a fallback face.

## Want to change it

The built pages are generated. Edit `demo/tunic.template.html`, never the built HTML,
then rebuild:

```bash
pip install -r requirements.txt
python build_all.py           # regenerate artwork + build the pages
python build_site.py          # copy the built pages into docs/
```

`build_all.py` needs two files that are **not in the repo**, because they are the
artwork as a library rather than as a tool - see *What you need to provide*. Without
them it will not run, and you cannot rebuild the pages. Everything needed to *read*
the geometry is here: `rules/army_tunic_placement_rules_2.json` is the source of truth
and carries a citation for every number.

## What you need to provide

Nothing in this repo is Crown copyright artwork or cadet data, and nothing that is
should ever be committed to it. `.gitignore` is set up to keep it that way.

| File | What it is | Where to get it |
|---|---|---|
| `ACRCCP750DA003.pdf` | A-CR-CCP-750/DA-003, *Symbols of the Royal Canadian Army Cadets*, March 2018 | National publication |
| `rcac_badges.zip` | Badge artwork extracted from that poster | `python src/extract_badges.py ACRCCP750DA003.pdf out_dir` |

The badge artwork is **Crown copyright**. Fine for internal corps use. If this ever
becomes a public web tool that changes, and the artwork would have to come out.

The PDF is only read by `recut_fitness.py` and `recut_pins.py`, which recover 16
badges the extractor cannot see because they are photographs. Once `art/recut/` holds
those crops the PDF can be deleted: `build_all.py` skips both steps and keeps the
existing crops. If the crops go too it stops and says which badges are unrecoverable,
rather than building pages quietly missing them. Everything else derives from
`rcac_badges.zip`, which is needed on every build.

## Layout

```
rules/    army_tunic_placement_rules_2.json   the source of truth. Start here.
data/     labels.py       slug -> confirmed badge identity (beats poster captions)
          badge_map.csv   generated from labels.py; hand-maintained, not regenerated
          manifest.csv    output of extract_badges.py
src/      extract_badges.py   pull badge artwork out of the poster PDF
          recut_*.py          recover badges the extractor merged or skipped
          build_art.py        pack artwork for the layout tool
          build_plate.py      pack artwork for the identification sheet
          build_badge_map.py  labels.py -> badge_map.csv
          poster_scale.py     check whether the poster is drawn to scale (it is not)
demo/     tunic.template.html   the layout tool, source
          plate.template.html   the identification sheet, source
          build.py, build_plate_html.py   inline the artwork -> *.html
notes/    CLAUDE_1.md     project brief and settled decisions
docs/     build_site.py output: index.html + plate.html. Gitignored - see Publishing
```

Edit a `.template.html`, run its build script, and the `.html` next to it is
regenerated with the artwork inlined. Never edit the built `.html` directly.

## The coordinate model

One axis per surface, and nothing ever measures in two directions at once.

- **Sleeves** - `y` in cm upward from the cuff bottom edge, `x` front-positive from
  the sleeve centre. The shoulder seam is simply `y = sleeve length`.
- **Front** - `y` in cm upward from each pocket's top edge, `x` inboard-positive.
  Negative `y` is on the pocket itself, where the pinned insignia go.

Front/rear and inboard/outboard become image-left/right exactly once, at draw time.
Get that wrong and the whole block mirrors.

### Two datum families, and why it matters

On the sleeve, the corps name title, the RCAC badge and the LCpl-Sgt chevrons are
measured **down from the shoulder seam**. Everything else is measured **up from the
cuff**. The distance between those two families is the sleeve length, so the gap
between a shoulder-referenced badge and a cuff-referenced one **changes with tunic
size**.

That is not academic. A Sergeant who is also Drum Major has 2.00 cm between the
chevron and the appointment badge on a 57 cm sleeve, 0.00 cm at 55 cm, and an
overlap below that. The tool has a sleeve-length control so you can see it.

### Absolute or relative

A badge is quoted absolutely only where the regulation gives it a fixed anchor.
Everything else is quoted as a gap from what it hangs off, because that is the
measurement a person actually takes:

> CTC grid, bottom row - bottom edge **1.00 cm above the training level star**

not "9.71 cm from the cuff".

## Publishing

`python build_site.py` assembles `docs/` - `index.html` (the layout tool) and
`plate.html` (the identification sheet), plus a `.nojekyll` marker. Both are single
self-contained files, so any static host serves the folder as-is. Check it first with
`python -m http.server -d docs 8000`; both pages are verified rendering over HTTP in
headless Chrome.

`docs/` rather than `site/` because GitHub Pages publishes only from a branch root or
from `/docs`. The layout tool becomes the site root and the plate lands at
`/plate.html`. To go live:

1. commit `docs/` - it is tracked
2. add a remote and push - neither is configured; ask before doing either
3. repo *Settings > Pages > Source: main, folder /docs*

### Copyright

The badge artwork is Crown copyright, from A-CR-CCP-750/DA-003. **Publishing it as
part of the tool is cleared** (Lt Beal, Sep 2026), and both pages carry an
attribution naming the publication and stating that this is not an official one.

That decision covers the artwork **as rendered in the tool**. It does not cover the
poster itself or the raw badge library, so `ACRCCP750DA003.pdf`, `rcac_badges.zip`
and `art/*` stay out of the repo. Someone wanting the badge files should go to the
publication, not to this repo.

Two things follow from publishing that did not matter internally. The tool becomes
reachable by other corps, so the pages say plainly that some figures rest on local
measurement and that open questions remain - see *Known gaps*. And GitHub Pages on a
free account serves from a **public** repository, so pushing is what actually
publishes; the repo being new and remote-less is the only thing holding it back.

One behaviour differs off the artifact: `plate.html` stores its label corrections in
the artifact database. Anywhere else that is unavailable, so it shows a banner and
falls back to browser-local storage - corrections survive a reload but stay in that
one browser, and cannot be read back. The layout tool has no such dependency and
behaves identically everywhere.

## Known gaps

`rules/army_tunic_placement_rules_2.json` carries the full list in
`open_questions`. The ones that would change output:

- **Which pocket the national commendations go on.** Figure 5D-1 says left; the tool
  draws one right-hand stack. CJCR Gp O 10050 para 7.5 now corroborates 5D-1, so the
  balance of evidence has moved and the tool has not. This is the one open question
  that puts a badge on the wrong side of a cadet.
- **Cadet Service Medal bars** are offered and named but not drawn, and the whole
  scheme - qualifying periods, whether bars accumulate, the ceiling - is unsourced.
- **Medal, anniversary pin and commendation pin dimensions** are unmeasured, so the
  front places them by rule but sizes them by placeholder.
- **Only tunic size 6436 is measured.** The taper profile is stretched
  proportionally for other lengths, which is an approximation.
- **`Date Awarded` drives CTC grid fill order** and is placeholder data upstream, so
  grid *order* is not yet sewing-safe even though grid *geometry* is.

## Working rules

Three of these were learned the hard way.

- **Artwork identifies badges. It does not dimension them.** Poster aspect ratios
  were used to infer a marksmanship rifle width of 5.5 cm; the real badge is 6.0 cm.
  The poster is also not drawn to a single scale - it runs 13 to 24 points per cm
  depending on which family you measure.
- **Poster captions are a hint, not an identity.** The extractor reads whatever text
  sits under a badge, which produced "Canadian Armed Forces" for the parachutist
  wings and "Maple Leaf" for the Maple Leaf Exchange. `data/labels.py` is
  authoritative.
- **Where the instruction and the illustration disagree, the instruction governs.**
  Annex H's 12 cm proficiency anchor, its five-badge stagger, and the poster's wider
  marksmanship gap were all wrong.
- **Flag discrepancies, never reconcile them silently.** The validator reports
  overlaps, tight clearances and anything resting on an estimate. It never adjusts a
  position to make a problem go away.

## Sources

- CJCR Dress Instructions, Chapter 3 Section 1 - the governing instruction
- CJCR Dress Instructions, Chapter 3 Annex H - sleeve placement figures
- CJCR Dress Instructions, Chapter 4 Annex A - poppy
- CJCR Dress Instructions, Chapter 5 Annexes A-D - medals, ribbons, commendations
- CJCR Gp O 10050, *JCR National Honours and Awards*, 2021-03-19 - order of
  precedence for medals and commendation pins. A JCR order, so it is used for order
  and not for geometry; the precedence itself is CJCR-wide.
- A-CR-CCP-750/DA-003, *Symbols of the Royal Canadian Army Cadets*, March 2018 -
  artwork only. Still shows terminated programmes, so treat it as art, not currency.
