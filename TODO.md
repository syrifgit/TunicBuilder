# TODO

Ordered by what it unblocks, not by effort. Every geometric item is also recorded in
`rules/army_tunic_placement_rules_2.json` under `open_questions`, which is the
authoritative list — this file is the working view of it.

Status as of rules **v0.14-draft**: 22 slots, 26 open questions, 6 recorded conflicts.

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
- [ ] **Wire the medal precedence into the tool.** CJCR Gp O 10050 para 7.4 supplies
  the ordered list (see below); the tool still takes a medal *count*, so it draws the
  right number in the right place with no identity and no order.
- [ ] **`Date Awarded` is placeholder data** in the workbook. It drives CTC grid fill
  order, so grid *order* is not sewing-safe even though grid *geometry* is.
- [ ] **Confirm the precedence lists against CATO 13-16.** No longer blocking —
  10050 fills the gap — but 10050 is a *JCR* order and CATO 13-16 is the
  cadet-programme authority. Confirm before a printed guide relies on it.
- [ ] **Resolve "Command" vs "VCDS" vs "Comd CJCR".** 10050 contradicts itself: its
  availability list (5.1) offers a Comd CJCR Commendation, its precedence list (7.5)
  ranks a VCDS Commendation. Held as "Command Commendation" per Chapter 5.
- [ ] **Chapter 7 or Chapter 5?** 10050 para 4.4 sends the reader to *Chapter 7* of the
  Cadet and JCR Dress Instructions for wearing medals and ribbons; every cadet figure
  here is cited from Chapter 5. Establish whether Chapter 7 is the JCR chapter or a
  renumbering that supersedes our citations.

### Medal order of precedence — CJCR Gp O 10050 para 7.4

The full CJCR list is 11. Seven are reachable by an army cadet; the rest are Sea or
Air awards, which a cadet who transferred in retains. Sort by seq rather than storing
the army seven. Precedence 1 is worn inboard, nearest the centre of the chest.

| # | Medal | Army |
|---|---|:--:|
| 1 | Cadet Award for Bravery | ● |
| 2 | Lord Strathcona Medal | ● |
| 3 | Royal Canadian Legion Cadet Medal of Excellence | ● |
| 4 | Navy League of Canada Medal of Excellence | |
| 5 | The Major-General W.A. Howard Award | ● |
| 6 | Air Force Association Medal | |
| 7 | Army, Navy and Air Force Veterans in Canada Cadet Medal of Merit | ● |
| 8 | Order of St. George Medal | ● |
| 9 | Sea Cadet Service Medal | |
| 10 | Army Cadet Service Medal | ● |
| 11 | Air Cadet Service Medal | |

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
