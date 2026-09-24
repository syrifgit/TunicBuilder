# TODO

Ordered by what it unblocks, not by effort. Every geometric item is also recorded in
`rules/army_tunic_placement_rules_2.json` under `open_questions`, which is the
authoritative list — this file is the working view of it.

Status as of rules **v0.31-draft**: 21 slots, 48 open questions, 10 recorded conflicts.

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
- [x] ~~**Cadet Service Medal bars are unsourced.**~~ The **army** scheme is sourced:
  ACLC Policy 13.1 paras 5 and 12 — four years earns the medal, each further year adds
  a gold bar and a ribbon leaf, **accumulating** rather than replacing. Drawn, not just
  named. Blatherwick puts the ceiling at three bars (seven years) by arithmetic. Still
  open: **Sea's scheme** is undescribed (reportedly anchor devices rather than a stack).
  **Air** uses the Army's system with its own devices, a gold bar with a bird on the
  medal and rosettes on the ribbon (Lt Beal). The artwork's built and arrives with the
  resized medal pack (§3).
- [ ] **`Date Awarded` is placeholder data** in the workbook. It drives CTC grid fill
  order, so grid *order* is not sewing-safe even though grid *geometry* is.
- [ ] **Resolve "Command" vs "VCDS" vs "Comd CJCR".** 10050 contradicts itself: its
  availability list (5.1) offers a Comd CJCR Commendation, its precedence list (7.5)
  ranks a VCDS Commendation. Held as "Command Commendation" per Chapter 5.
- [ ] **Confirm a transferring cadet keeps awards earned in another element.** Stated
  for JCR at 10050 para 6.2. It is what makes the Sea and Air entries in the medal list
  reachable on an army tunic, and the tool models it that way.
- [x] ~~**Air rank height: which edge is "mid-way"?**~~ The top edge, per Figures 3H-5 /
  3H-6. Every Air rank now clears the squadron insignia by 7.3 cm. The same figures
  settled the CTC arm (right), the appointment (whichever right-sleeve anchor the rank
  leaves free) and the six-badge blocks.
- [x] ~~**Check Figure 3D-6 for the wing gap.**~~ Sewn wings sit directly on the pocket
  edge. Para 3's 0.5 cm is the gap for the metal pin on the collared shirt (Lt Beal).
- [ ] **CTC supersession is unclear for every element.** The Army texts (CH3S1 3.b.(9),
  Figure 3D-3) say "advanced qualification supersedes basic qualification"; the Air
  texts don't. Which badges count as advanced and basic is open, so the tool applies
  nothing and draws every badge selected.
- [ ] **Commendation pins against competition pins.** How the two rank against each
  other is unclear for every element. Air follows Army for now.
- [ ] **Which CTC badges come off past six?** The tool drops the most recently awarded,
  on no source, for every element.

Medals are done. **CATO 13-16 para 19 is now sourced verbatim** and confirms the order
for every medal except the Order of St. George, which is absent from it — that one still
rests on CJCR Gp O 10050 alone. Seq 5 is the **Army Cadet Medal of Merit** (four award
bars, at least one worn, Walsh requires President — 11 states, all drawn). Seq 6, the
**Air Force Association Medal**, is drawn now too: no text describes its ribbon, but the
air poster shows it in full colour, so its colour is measured and its geometry estimated.

## 2. Measurements — one ruler each

Everything here is a placeholder or an estimate the tool draws and flags.

- [ ] **NRT and Bisley Series pins.** RCAC National Rifle Team and LGen C.H. Belzile
  Trophy. Both non-standard: the artwork trims to aspect 2.47 and 1.42, so neither is
  a 1 in square. Drawn 2.54 cm wide with height from the artwork.
- [ ] **National-winner award pins.** Vamplew & Clément Tremblay (marksmanship) and
  Bédard / Keddie / Le Guellec (biathlon). Confirmed non-standard; aspect 1.07 and
  about a third larger than the championship pins beside them.
- [ ] **Duke of Edinburgh pin — size only.** The *aspect* was never unknown: the issued
  artwork is 1.197 for all three levels, so it is now drawn 2.0 × 1.671 rather than
  2.0 × 1.6, which had been stretching it 4.4%. Annex D still gives no millimetres.
- [ ] **Expedition pin.** Circular. Poster draws it ~1.5× the championship pins in the
  same block — a within-band comparison, so the 2.54 cm drawn is probably low.
- [ ] **Anniversary pin** (drawn 2.0 cm), **medal width** (drawn 3.5 cm; the 10 cm
  court-mount length is regulation and confirmed), **commendation pin** (Annex D gives
  2.0 × 0.5 cm, and 2.0 × 0.75 for Navy League — confirm against real pins),
  **parachutist badge** (drawn 9.0 × 3.87 cm from poster aspect at a guessed width),
  and the **service medal bar**, which has no dimensions at all.
- [ ] **CWO rank.** Still an estimate at 7.62 × 10.16 cm, though the poster corroborates
  it to 2%.
- [x] ~~**Air: the unmeasured badges.**~~ Settled by adopting army sizes (Lt Beal): WO2
  = MWO 7.62 × 5.08, WO1 = CWO 7.62 × 10.16, wings = parachutist 9.0 × 3.87, and
  Effective Speaking = the championship pins' 1 in square. WO1 and the wings inherit
  the CWO and parachutist items above, so measuring those settles both elements.
  The Air Drum Major and Pipe Major still sit in the army 10 × 11 cm box on no
  recorded decision, though the Air art fits it to within 1%.
- [ ] **The elbow.** Air and Sea both place ranks "mid-way between the elbow and the
  shoulder seam", and the elbow is still assumed at mid-sleeve (28 cm on 57). One
  measurement on any tunic settles it for both.
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

## 3. Artwork

- [x] ~~**Medals and ribbons.**~~ Authored as SVG in `Medals and Ribbons/` and wired in:
  ribbons 35 × 10 mm, medals 35 × 100 mm, matching the tool's geometry exactly. Every
  award draws as itself. Not extracted from the poster — it never carried them.
- [x] ~~**Commendation and award insignia.**~~ CDS, Command, Cadet and Navy League now
  draw as real insignia at the Chapter 5 sizes. The DofE slot already had artwork.
- [ ] **Fidelity is mixed and worth knowing.** Strathcona, RCL Excellence, St. George
  and the Army Cadet Service Medal are sampled from source images. **Bravery and ANAVETS
  stripe widths are still eyeballed**, and every medallion obverse is stylised — the
  central relief is not reproducible from the sources to hand. Per-item detail is in
  `Medals and Ribbons/medal_art_manifest.json`. The full delivery traces every face, so
  this closes when it's merged.
- [x] ~~**Air Force Association Medal has no artwork.**~~ `medal_afa` / `ribbon_afa`
  arrived with the air delivery and seq 6 is drawn. The Air Cadet Service Medal disc
  is **gold** (Lt Beal). It was built bronze for a while off the poster, which prints it
  brown, and that's been reverted.
- [x] ~~**Send `AIR_ARTWORK_FOLLOWUP_2.md`.**~~ Answered in the full medal delivery
  (`cadet_medal_art_full/`): the Air service bars, `src/maple_leaf_path.txt` and bundled
  fonts all came back. The ANAVETS recolour for the AFA was overtaken by a reference
  photo, so navy / light blue / maroon stands (Lt Beal). Still to come: the **Air
  squadron title generator**.
- [ ] **Merge the full medal delivery once it's resized.** It traces every medal face and
  adds the Air bars, but shrank each medal ribbon to 28 mm on the 35 mm canvas so the
  bars could overhang, which opens a 7 mm gap between ribbons in the tool. Sent back:
  ribbon at 35 mm, canvas widened for the overhang, AFA manifest note corrected. The
  tool already draws a wider canvas centred on its slot. When it lands, replace
  `Medals and Ribbons/`, decide which of the traced emblem sources get committed, and
  rebuild.
- [ ] **Court-mounted medals.** Every medal is drawn swing-mounted, its ribbon ending at
  the suspender, at the 10 cm court-mount length, and the front note calls that "Court
  mounted". The request is written: 27 `medal_<key>_court` twins on the same 35 × 100 mm
  canvas, the ribbon carried down behind the disc to its centre line. Send it with or
  after the follow-up, and the tool gets a swing / court choice once the art lands.
  First check whether Chapter 5 gives swing-mounted medals their own length, since the
  10 cm comes from the court-mounting section.
- [x] ~~**Get the updated `medal_specs.py` and `make_medals.py`.**~~ Arrived with the
  air follow-up. Only `medal_specs.py` changed, and the manifest regenerates from it
  identically.
- [ ] **`make_medals.py` can't run from this repo.** The full delivery bundles the leaf
  path and the fonts, so once it's merged only cairo is missing. The pack is fine as
  delivered.
- [x] ~~**Air badge artwork.**~~ 63 badges from `air badges/air_art_pack.js`, wired in
  at hand-measured sizes. Still to do:
  - [x] ~~**Effective Speaking re-cut.**~~ Revision 2 keys the white paper out of all
    three; the other 60 badges are byte-identical.
  - [x] ~~**Families with art but no control.**~~ Air marksmanship, glider
    familiarization and Music Basic are in the cuff block, one per family, in the order
    the dropdowns are set.
  - [x] ~~**Pilot wings and Effective Speaking.**~~ Wings on the left breast with the
    Glider CTC exclusion; Effective Speaking tops the Air pin strip.
  - [x] ~~**Publication.**~~ Lt Beal: same poster family, individual tool for now.
    `AIR_ART_CLEARED` is set in `build_site.py`.
  - [x] ~~**Silver and gold wire wings.**~~ Authorized on the jacket in lieu of the
    issued ones (3D-6), but not needed: the tool draws the issued nylon wings (Lt Beal).

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
- [ ] **No QualMap level for Music Basic.** It's worn until Level 1 replaces it (Lt
  Beal), and the tool now offers it for every element.
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
- [ ] **Sea artwork and the Sea corps badge.** Air is done: placement sourced from para
  3 and its figures, and its own artwork at measured sizes. Sea is placed from para 3
  but still draws army artwork, and its corps badge, worn on the right breast, isn't
  drawn. The coordinate model and the resolver carried over unchanged, as expected:
  it's the rules pack and the art that are element-specific.
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
