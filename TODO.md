# TODO

Ordered by what it unblocks, not by effort. Every geometric item is also recorded in
`rules/army_tunic_placement_rules_2.json` under `open_questions`, which is the
authoritative list — this file is the working view of it.

Status as of rules **v0.18-draft**: 22 slots, 21 open questions, 6 recorded conflicts.

---

## 1. Blocks correct output

Things the tool currently gets *wrong* or cannot answer, not merely gaps.

- [ ] **Decide the commendation split, then flip the renderer.** Figure 5D-1 puts
  National Commendations on the **left** pocket. That was adopted as *right* because
  the rest of Chapter 5 is right-breast and 5B-1 lists CDS → Command → Cadet → Navy
  League → DofE as one 0.5 cm stack. **CJCR Gp O 10050 para 7.5 now corroborates
  5D-1**, marking CDS and VCDS "(to be worn on the left side)" while 7.2 puts
  commendation and DofE pins generally on the right. Two independent sources for
  national-left / cadet-right against one reading of Chapter 5. The renderer still
  draws a single right-hand stack, so a cadet holding a CDS Commendation currently
  gets it on the wrong side.
- [ ] **Left-pocket stack geometry**, if the split goes ahead. 5D-1 gives the
  single-pin case only, and CDS + VCDS together is possible.
- [ ] **Cadet Service Medal bars are unsourced.** The tool offers None / 5-year /
  6-year / 7-year and names the bar on the award without drawing it. Nothing to hand
  gives the qualifying period for the medal or for each bar, whether a cadet wears
  every bar earned or only the highest, where the ceiling is, or how a bar shows on an
  undress ribbon. Labels and the 7-year ceiling follow Lt Beal; the "highest only"
  reading follows the convention used everywhere else here, and is a guess.
- [ ] **`Date Awarded` is placeholder data** in the workbook. It drives CTC grid fill
  order, so grid *order* is not sewing-safe even though grid *geometry* is.
- [ ] **Resolve "Command" vs "VCDS" vs "Comd CJCR".** 10050 contradicts itself: its
  availability list (5.1) offers a Comd CJCR Commendation, its precedence list (7.5)
  ranks a VCDS Commendation. Held as "Command Commendation" per Chapter 5.
- [ ] **Confirm a transferring cadet keeps awards earned in another element.** Stated
  for JCR at 10050 para 6.2. It is what makes the Sea and Air entries in the medal list
  reachable on an army tunic, and the tool models it that way.

Medal precedence is implemented: all 11 in order from CJCR Gp O 10050 para 7.4, the
three service medals collapsed to one element choice resolving back to seq 9 / 10 / 11,
and the undress ribbons built from the same selection. The full list lives in the rules
pack under `right_medals.order_of_precedence`. Only the artwork is outstanding.

## 2. Measurements — one ruler each

Everything here is a placeholder or an estimate the tool draws and flags.

- [ ] **NRT and Bisley Series pins.** RCAC National Rifle Team and LGen C.H. Belzile
  Trophy. Both non-standard: the artwork trims to aspect 2.47 and 1.42, so neither is
  a 1 in square. Drawn 2.54 cm wide with height from the artwork.
- [ ] **National-winner award pins.** Vamplew & Clément Tremblay (marksmanship) and
  Bédard / Keddie / Le Guellec (biathlon). Confirmed non-standard; aspect 1.07 and
  about a third larger than the championship pins beside them.
- [ ] **Duke of Edinburgh pin.** Oval, so it needs *both* dimensions. Annex D gives
  none. Drawn 2.0 × 1.6 cm.
- [ ] **Expedition pin.** Circular. Poster draws it ~1.5× the championship pins in the
  same block — a within-band comparison, so the 2.54 cm drawn is probably low.
- [ ] **Anniversary pin** (drawn 2.0 cm), **medal width** (drawn 3.5 cm; the 10 cm
  court-mount length is regulation and confirmed), **commendation pin** (Annex D gives
  2.0 × 0.5 cm, and 2.0 × 0.75 for Navy League — confirm against real pins),
  **parachutist badge** (drawn 9.0 × 3.87 cm from poster aspect at a guessed width),
  and the **service medal bar**, which has no dimensions at all.
- [ ] **CWO rank.** Still an estimate at 7.62 × 10.16 cm, though the poster corroborates
  it to 2%.
- [ ] **Smallest tunic in stores: sleeve length.** Only size 6436 (57 cm) is measured.
  A Sgt who is also Drum Major has 2.00 cm of clearance at 57 cm, 0.00 cm at 55 cm and
  an overlap below. This is a real wearability question, not a drawing nicety.
- [ ] **Corps name title**, ideally against a real title rather than derived. Currently
  12.21 × 3.85 cm, derived from the poster template and the measured 6.35 cm RCAC badge.
- [x] ~~**Breast pocket flap height.**~~ Measured at **6.0 cm**. Three independent
  measurements now agree: a 15 cm pocket less a 6 cm flap leaves exactly the 9 cm of
  the measured competition pin strip, so the strip fills the pin band with no
  remainder. The 4.0 cm placeholder left 2 cm unaccounted for.
- [x] ~~**Chevron heights**~~ and ~~**MWO aspect**~~. Settled on the hand
  measurements: chevrons 6.5 / 8.0 / 9.5 / 11.0 cm at 10 cm wide, MWO 7.62 × 5.08 cm.
  The poster implied 7.41 / 8.98 / 10.13 / 12.02 and an MWO aspect of 1.50, and loses
  on the standing rule that artwork identifies badges without dimensioning them — its
  art carries an embroidered field the finished badge does not. Reasoning is recorded
  on the constants in the rules pack, not just deleted.

**Not a ruler question:** the maximum medal bar width is set by the wearer's physique —
the bar must not run past the jacket arm seam — so it stays a per-cadet flag rather
than a number the rules pack can carry.

## 3. Artwork still missing

- [ ] **Seven medals.** Army Cadet Service (plus its bar), Order of St George, ANAVETS,
  Howard, Legion, Lord Strathcona, Bravery. On the poster but never extracted —
  they are photographs, and `extract_badges.py` clusters vector objects only. Same
  failure that hid the fitness block and the pins; `src/recut_pins.py` shows the fix.
  The tool now names and orders all 11 and draws each as a plain bar, so artwork is
  the only thing outstanding. The other four are Sea and Air and are not on this
  poster at all.
- [ ] **Commendation and award insignia.** CDS, Command, Cadet, Navy League. Annex D
  illustrates all four; they are currently drawn as plain bars at the right size.

## 4. Workbook corrections

The tool is right and `D - Qual Info` is wrong in each of these. `242 Qualifications
Data.xlsx` is Protected A and has been moved out of this directory, so these are
described from notes — go to wherever it now lives to act on them.

- [ ] **Expedition slot is wrong.** Four `Participation | Expedition` rows say
  `out_of_scope_left_pocket`, following the general CH3S1 4.b rule. The Chapter 5
  Annex B figure is specific and puts expedition insignia over the **right** pocket,
  0.5 cm above the nametag. Specific beats general.
- [ ] **Add the Order of St George** as a 7th medal. The poster carries it; the
  workbook has only six.
- [ ] **Typo:** "Army, Navy, and Air Force Veterans in **Canda** Cadet Medal of Merit".
- [ ] **No rows for three CTC badges** that exist on the poster: General Training,
  Army Cadet Voyage, Maple Leaf Exchange. 21 CTC badges against 18 rows.
- [ ] **`RankMap` has no geometry columns.** Needs badge class
  (`none` / `chevron` / `crown`), width, height. The tool hardcodes this and is
  effectively the working spec.
- [ ] **No `ApptBadgeMap`.** Only Drum Major and Pipe Major have appointment insignia;
  `O - Tunic Builder` echoes the appointment string straight through and would render
  a badge for ranks that have none.

## 5. Scope the tool does not yet cover

- [ ] **Sashes and lanyards.** Not modelled at all. Needs a source — neither Chapter 3
  Section 1 nor Chapter 5 covers them.
- [ ] **Full tunic render.** Currently four flat panels (two sleeves, two breast
  pockets). A whole-garment view would show how the pieces relate and make the
  shoulder-to-pocket relationship real rather than presentational.
- [ ] **Sea and Air elements.** Most of the above repeats for each: their own
  placement rules, their own artwork, their own nametag colour (air cadet name tags
  are air force blue; army and sea are black). The coordinate model and the resolver
  should carry over unchanged — it is the rules pack and the art that are
  element-specific. The unit dropdown and the service-medal element selection are the
  first two places that already anticipate it.
- [ ] **A written sewing guide.** The tool produced one until it was removed as
  screen clutter: a table of every badge sorted so that anything a later badge hangs
  off was already placed. The drawing's callouts carry the same measurements, but
  there is no longer a list to work down while sewing. If it comes back it should be a
  third print page rather than an on-screen panel. `resolve()` still returns
  everything it needs; `fmtMeasure()` and `datumOf()` were the formatters and are in
  git history.
- [ ] **Bulk data entry.** Deliberately out of scope for the first release. `state` is
  a plain object that the resolvers read directly, so loading a cadet is assigning to
  it — wiring this to `D - Master Calc` is a data-loading job, not a modelling one.
- [ ] **Shirt layouts.** Only the jacket is modelled. The DofE pin is jacket-only and
  the poppy figure is drawn for the shirt.
- [ ] **Canadian Honours System medals** (Queen's Jubilee and similar). A cadet may
  hold one but the CO must seek wear instructions through the chain of command. One
  data point: 10050 para 7.3 wears these on the **left**, opposite the cadet awards.

## 6. Housekeeping

- [x] ~~**Settle the copyright question.**~~ Cleared: the badge artwork may be
  published as part of the tool. `docs/` is tracked and both pages attribute the
  artwork. The clearance covers the artwork *as rendered in the tool* only — the
  poster and the raw badge library stay out of the repo.
- [x] ~~**`notes/CLAUDE_1.md` names a real cadet surname.**~~ Reworded; the point it was
  making — never match on surname alone — survives without the name. No cadet name
  appears anywhere in the repo now.
- [ ] **`make_corps_title.py` has a hardcoded Linux font path.** More pressing now
  that the rail has a unit dropdown: adding a corps means generating a plate, and that
  will fail from Windows.
- [ ] **Sleeve print page: break line.** Badges live at 0–13 cm and 33–57 cm from the
  cuff with a deliberately empty 20 cm band between. A standard drafting break would
  render the sleeves roughly 40% larger on paper, at the cost of a discontinuous scale.
- [ ] **Report Annex H 3H-3 upward.** Its 12 cm proficiency dimension is wrong and
  geometrically impossible. Worth correcting nationally.
