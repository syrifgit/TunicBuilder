# TODO

Ordered by what it unblocks, not by effort. Every geometric item is also recorded in
`rules/army_tunic_placement_rules_2.json` under `open_questions`, which is the
authoritative list — this file is the working view of it.

Status as of rules **v0.12-draft**: 22 slots, 15 open questions, 5 recorded conflicts.

---

## 1. Blocks correct output

Things the tool currently gets *wrong* or cannot answer, not merely gaps.

- [ ] **Source CATO 13-16.** It holds the order of precedence for every medal and
  undress ribbon. Without it the right breast can be correctly *placed* but not
  correctly *ordered* — the numbering in the tool is your click order, not authority.
  Raised as a `crit` in the validator whenever medals or ribbons are worn.
- [ ] **Resolve the 5D-1 contradiction.** Figure 5D-1 says National Commendations go
  on the **left** breast pocket; the rest of Chapter 5 puts everything on the right in
  one stack, and 5B-1's precedence list runs CDS → Command → Cadet → Navy League →
  DofE as a single 0.5 cm stack. Adopted **right**, logged as a conflict. Getting this
  backwards puts a CDS Commendation on the wrong side of a cadet.
- [ ] **`Date Awarded` is placeholder data** in the workbook. It drives CTC grid fill
  order, so grid *order* is not sewing-safe even though grid *geometry* is.
- [ ] **Confirm medal precedence order** once CATO 13-16 is in hand.

## 2. Measurements — one ruler each

Everything here is a placeholder or an estimate the tool draws and flags.

- [ ] **Breast pocket flap height.** Unmeasured, and *every* pocket-mounted pin is
  centred between the flap's lower edge and the pocket's lower seam. Highest-value
  single measurement on the list.
- [ ] **Sgt chevron height.** Settles the standing disagreement: measured
  6.5 / 8.0 / 9.5 / 11.0 cm at 10 cm wide against the poster's implied
  7.28 / 8.91 / 10.04 / 12.05. Measure Sgt and the other three follow.
- [ ] **NRT and Bisley Series pins.** RCAC National Rifle Team and LGen C.H. Belzile
  Trophy. Both non-standard: the artwork trims to aspect 2.47 and 1.42, so neither is
  a 1 in square. Drawn 2.54 cm wide with height from the artwork.
- [ ] **National-winner award pins.** Vamplew & Clément Tremblay (marksmanship) and
  Bédard / Keddie / Le Guellec (biathlon). Confirmed non-standard; aspect 1.07 and
  about a third larger than the championship pins beside them.
- [ ] **Duke of Edinburgh pin.** Oval, so it needs *both* dimensions. Annex D gives
  none.
- [ ] **Expedition pin.** Circular. Poster draws it ~1.5× the championship pins in the
  same block — a within-band comparison, so 1 in is probably low.
- [ ] **Anniversary pin**, **medal width**, **commendation pin** (Annex D gives
  2.0 × 0.5 cm, and 2.0 × 0.75 for Navy League — confirm against real pins).
- [ ] **CWO rank.** Still an estimate at 7.62 × 10.16 cm, though the poster corroborates
  it to 2%.
- [ ] **Smallest tunic in stores: sleeve length.** Only size 6436 (57 cm) is measured.
  A Sgt who is also Drum Major has 2.00 cm of clearance at 57 cm, 0.00 cm at 55 cm and
  an overlap below. This is a real wearability question, not a drawing nicety.
- [ ] **Corps name title**, ideally against a real title rather than derived. Currently
  12.21 × 3.85 cm, derived from the poster template and the measured 6.35 cm RCAC badge.

## 3. Artwork still missing

- [ ] **Seven medals.** Army Cadet Service (plus its bar), Order of St George, ANAVETS,
  Howard, Legion, Lord Strathcona, Bravery. On the poster but never extracted —
  they are photographs, and `extract_badges.py` clusters vector objects only. Same
  failure that hid the fitness block and the pins; `src/recut_pins.py` shows the fix.
- [ ] **Commendation and award insignia.** CDS, Command, Cadet, Navy League. Annex D
  illustrates all four; they are currently drawn as plain bars at the right size.
- [ ] **Fitness Excellence** exists in the workbook and on the poster — check the
  recovered `fit_excellence.png` is the right badge and not a mis-crop.

## 4. Workbook corrections

The tool is right and `D - Qual Info` is wrong in each of these.

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
  element-specific.
- [ ] **Bulk data entry.** Deliberately out of scope for the first release. The
  resolver already takes a plain object, so wiring it to `D - Master Calc` is a
  data-loading job, not a modelling one.
- [ ] **Shirt layouts.** Only the jacket is modelled. The DofE pin is jacket-only and
  the poppy figure is drawn for the shirt.
- [ ] **Canadian Honours System medals** (Queen's Jubilee and similar). A cadet may
  hold one but the CO must seek wear instructions through the chain of command.

## 6. Housekeeping

- [ ] **Settle the copyright question** before publishing anywhere public. See
  *Publishing* in the README — GitHub Pages on a free account serves from a public
  repository, so that route redistributes Crown copyright artwork.
- [ ] **`docs/CLAUDE_1.md` names a real cadet surname** (line 49). Fine in a private
  repo, not for a public one. Rewording to "some cadets share a surname" keeps the
  point.
- [ ] **`make_corps_title.py` has a hardcoded Linux font path.** Fine as-is since the
  PNGs are generated, but retitling for another corps from Windows will fail.
- [ ] **Sleeve print page: break line.** Badges live at 0–13 cm and 33–57 cm from the
  cuff with a deliberately empty 20 cm band between. A standard drafting break would
  render the sleeves roughly 40% larger on paper, at the cost of a discontinuous scale.
- [ ] **Report Annex H 3H-3 upward.** Its 12 cm proficiency dimension is wrong and
  geometrically impossible. Worth correcting nationally.
- [ ] **Record the source of the photograph** that confirmed the 20 cm proficiency
  anchor, so the conflict resolution is auditable.
- [ ] **Confirm appointment insignia against Annex E** — Drum Major and Pipe Major only,
  currently established from the poster's APPOINTMENT section alone.
