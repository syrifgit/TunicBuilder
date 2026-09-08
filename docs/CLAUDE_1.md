# Army Cadet Tunic Builder - project brief

## What this is

242 RCACC (Royal Canadian Army Cadet Corps, Fredericton NB) runs about 88 cadets. This
project takes cadet qualification data out of an Excel workbook and produces a per-cadet
tunic layout: which badges and pins a cadet wears, and exactly where each one goes on the
jacket, in centimetres.

Two outputs are wanted eventually:

1. A visual render of the left and right sleeves (SVG, on screen or printed).
2. A sewing guide - a per-cadet printout listing each badge with its measurement from a
   named datum, so someone can lay a ruler on a sleeve and place it.

Right now the sleeves are fully specified. The front of the tunic is not.

## Files here

| File | What it is |
|---|---|
| `242 Qualifications Data.xlsx` | The data source. Star-schema workbook, see below. **Protected A, since moved out of this directory.** |
| `army_tunic_placement_rules_2.json` | The placement rules pack. Every slot, anchor, offset, citation and conflict. Read this first. |
| `extract_badges.py` | Pulls badge artwork out of the national symbols poster as SVG + PNG. Already run. |
| `rcac_badges.zip` | 77 extracted badges. SVG (vector) and 600 dpi transparent PNG each, plus `manifest.csv`. |
| `manifest.csv` | Badge inventory with source coordinates and aspect ratios. Four blank columns at the end are for mapping badges onto the workbook's `QualMap`. |

## The workbook

Star schema. Sheet prefixes mean something: `I -` input, `D -` derived, `O -` output.

- `I - Raw Fortress Nominal Roll` - immutable import from Fortress, the national cadet
  management system. Never edited by hand.
- `I - Config` - lookup tables (`ProgMap`, `LevelMap`, `RankMap`, `GroupMap`, `ApptSecMap`,
  `SectComdMap`, `AccelMap`).
- `I - Overrides` - manual layer for anything Fortress can't hold.
- `I - Cadet Qualifications` (`CadetQuals`) - long format, one row per cadet per
  qualification. `Key | Type | Category | Qualification Name | Status | Date Awarded | Notes`.
- `D - Qual Info` (`QualMap`) - the qualification dictionary. Carries `Badge`, `Pin`,
  `Highest Only?`, `Max Worn`, `Slot`, `Stack Order`.
- `D - Master Calc` - the joined fact table. One row per cadet, all derived fields resolved
  with a coalesce pattern (override wins, else derived, else blank).
- `O - Tunic Builder` - human-readable check view. Shows what each cadet wears per slot.

**Read `Master Calc` + `CadetQuals` + `QualMap` directly.** Do not parse `Tunic Builder`
strings - that sheet is for a human to eyeball, not a machine contract.

The join key is `LastName|FirstName`. CIN exists as a column but is empty in the Fortress
export, so names are load-bearing. Several cadets share a surname - three of them in one
case. Never match on surname alone.

### The `Slot` column is what maps data to geometry

`Type` and `Category` are a data taxonomy and do **not** map to positions. Three cases prove
it: Marksmanship is `Type = Proficiency` but has its own anchor; Training Level is
`Type = Proficiency` but is the star on the other sleeve; Parachutist is
`Type = Summer Training` like the CTC quals but goes on the chest. Always route by `Slot`.

Slot values: `right_star_level`, `right_ctc_grid`, `left_proficiency_stack`,
`left_marksmanship`, `not_worn`, `out_of_scope_left_pocket`, `out_of_scope_left_breast`,
`out_of_scope_medals`.

## Settled decisions - do not relitigate

All of these are already recorded in the rules JSON with citations and reasoning. They took
work to establish. If you think one is wrong, say so and show the evidence, but don't
silently change it.

- **Two datums**: `shoulder_seam` (offsets measured down) and `cuff_bottom` (the bottom edge
  of the cuff, not the top cuff seam - offsets measured up).
- **Proficiency stack anchors at 20 cm, not 12.** Annex H figure 3H-3 says 12 cm and is
  wrong. The marksmanship assembly already occupies 6 to ~13.5 cm, so 12 cm would overlap
  it. Chapter 3 Section 1 governs; the annex is illustrative. Confirmed against a photo of a
  worn tunic.
- **The proficiency stack and marksmanship are independent.** The stack holds at 20 cm
  whether or not marksmanship is worn. A cadet with proficiency badges and no marksmanship
  wears a visible empty band. That is correct. Do not close the gap.
- **Stack order bottom to top: Fitness, First Aid, Music.** Collapses - the lowest worn badge
  takes the 20 cm slot, the rest chain upward 1 cm apart. Policy gives no order; this is a
  local decision.
- **Circle badges are 3 cm.** Proven, not assumed: the CTC grid is three circles wide, so at
  3 cm it is 9 cm on a 12.26 cm flat sleeve (1.63 cm each side), and at 4 cm it would be
  12 cm on the same 12.26 cm, which cannot be sewn.
- **CTC grid is an aligned 2 row x 3 column grid**, max six. Fill order: bottom-centre,
  bottom-front, bottom-rear, top-centre, top-front, top-rear. Sequence by date awarded
  ascending. Annex H's text describes only five in a stagger and is wrong; Ch3 3.b.(9) and
  the drawn figures agree on the aligned grid.
- **"Front" means toward the chest, "rear" toward the back.** On the right sleeve viewed flat
  from outside, front is image-right. Output sewing guides in front/rear terms or the block
  gets mirrored.
- **Chevrons point down.** Confirmed from the extracted poster art. This is why the
  appointment badge builds *upward* from 20 cm: "chevron points at 20 cm" means the bottom
  apex. Note Annex H uses "tips" for the Sgt rule meaning the *top* arm ends, and "points"
  for the appointment meaning the *bottom* apex. Same shape, opposite edges, neither defined.
- **Only Drum Major and Pipe Major have appointment insignia.** The national symbols poster's
  APPOINTMENT section contains exactly those two. Pl WO, CSM, RSM, Sect Comd, Sr Stds Cdt,
  Cdt Trg A and D&C A have no sleeve badge.
- **Distinguished marksmanship swaps the numeral for a crown.** Same 6 cm bottom anchor, but
  the assembly is a single 6 x 8 cm piece rather than rifles + numeral. Heights are close but
  not equal (7.485 vs 8.0 cm) - use real values.
- **ALP cadets wear the Gold Star.** ALP has no insignia of its own yet, so the cadet keeps
  the highest level they hold that carries a badge. This falls out of a general rule - within
  any "highest only" category, skip levels that have no badge and wear the next one down -
  which also covers Fitness "Participated". No special case, no phantom box. Corrected by
  Lt Beal; supersedes the earlier "no star, hold the position" decision.
- **Master Cadet and the National Star of Excellence are terminated programs.** Their slot
  (left sleeve, 1 cm below the RCAC badge) stays vacant. Nothing reflows into it.

## Open questions

Ranked by how much they block work.

1. **Chevron heights disagree with the poster art.** Measured 6.5 / 8.0 / 9.5 / 11.0 cm for
   LCpl / Cpl / MCpl / Sgt at 10 cm wide. Poster aspects imply 7.41 / 8.98 / 10.13 / 12.02.
   Probably embroidered field vs merrowed edge. Remeasure Sgt first. This shifts the whole
   rank block and squeezes the Sgt-plus-drum-major case from a 2 cm gap to 1 cm.
2. **`RankMap` has no geometry class.** It maps abbreviation to full name only. Needs three
   columns: badge class (`none` / `chevron` / `crown`), width, height. Cdt wears nothing.
3. **No `ApptBadgeMap`.** `O - Tunic Builder` currently echoes the appointment string
   straight through, so it would render badges for appointments that have none. Two rows are
   real (Drum Major, Pipe Major); everything else is N.
4. **`Date Awarded` is placeholder data.** 17 of 31 rows have dates derived from course level,
   14 have none. There is a warning in `O - Tunic Builder!A2`. The CTC grid fill order depends
   on this, so grid output is not sewing-safe yet.
5. **Test fixtures missing for the hard paths.** No cadet has 4-6 CTC quals (max is 3), none
   has a 3-high proficiency stack (max is 2), none is a WO/MWO with an appointment. The
   two-row grid is the whole reason fill order matters and nothing exercises it. Suggest fake
   rows under a `TEST|Alpha` style key, filtered out of real printouts.
6. **MWO and Distinguished aspects also disagree with the poster** (1.26 vs 1.50, 0.842 vs
   0.750). Remeasure.
7. **Corps name title and RCAC badge dimensions unmeasured.** The RCAC height is needed to
   confirm the 1 cm gap down to junior rank.
8. **Only tunic size 6436 measured.** The taper profile in the JSON is that one size. The CTC
   grid at 1.63 cm clearance is the tightest fit on the tunic, so a small cadet with a full
   grid may not fit. Measuring the smallest tunic in stores would bracket it.
9. **Annex E not sourced.** Should confirm the two-appointment finding.
10. **Front of tunic entirely out of scope.** Parachutist (0.5 cm above the left breast
    pocket), participation pins (left pocket strip, max 3 combined), commemorative pin (max
    1), medals and undress ribbons. Needs Ch3 4.a/4.b, Annex E, Annex G and Chapter 5.

## Suggested first tasks

1. Read `army_tunic_placement_rules_2.json` end to end before writing any code.
2. Write the extract script: read the workbook, resolve each cadet against `QualMap` and the
   rules pack, emit per-cadet JSON of resolved slots with cm coordinates. Stub rank and
   appointment behind a flag until items 2 and 3 above are done.
3. Validate the extract against `O - Tunic Builder` for a handful of cadets - that sheet is
   the human-readable answer key.
4. Then render. SVG sleeve outline from the taper profile, badges placed from the resolved
   coordinates, artwork from `rcac_badges.zip`.

## Constraints

- **The data is Protected A.** Cadet names, ranks and qualifications. Keep it in this
  directory. No uploading to third-party services, no committing real data to a public repo.
  If you need sample data for tests, synthesise it.
- **Every geometric claim needs a citation.** The rules JSON carries `citation` on each slot
  and a `conflicts` block where policy contradicts itself. Maintain that. A printed sewing
  guide has to be defensible when someone asks why a badge is at 20 cm.
- **Flag discrepancies, don't reconcile them silently.** If a source disagrees with another
  source or with local practice, surface it.
- **Local decisions are tagged `LOCAL DECISION`** in the JSON. Keep them distinguishable from
  the actual regulation.
- The badge artwork is Crown copyright. Fine for internal corps use. If this ever becomes a
  public web tool, that changes.

## Writing style for anything user-facing

Direct and plain. Short sentences. Contractions. Hyphens, never em-dashes. No hedging, no
filler politeness, no formal connectors. Lead with the conclusion.

## Source documents

- CJCR Dress Instructions Chapter 3 Section 1 - the governing instruction for insignia.
- CJCR Dress Instructions Chapter 3 Annex H - placement figures 3H-3 (left sleeve) and
  3H-4-1/2/3 (right sleeve, three rank variants). Illustrative only, and figure 3H-3 carries
  a known wrong dimension.
- A-CR-CCP-750/DA-003, *Symbols of the Royal Canadian Army Cadets*, dated March 2018. The
  badge art source. Still shows terminated programs, so treat it as artwork, not currency.
