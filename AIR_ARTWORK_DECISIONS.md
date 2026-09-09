# Air artwork: decisions

Answers to `AIR_INVENTORY.md`. **Go ahead and extract.** Every open question is
settled below; nothing else needs asking first.

The inventory was worth the round trip on its own. Eleven of the badges I asked for by
name are raster, so a vector-clustering run would have dropped exactly the ones I care
about while looking like a clean pass. That is the army failure, caught before it cost
anything.

---

## 1. The naming rule, because it drives most of the answers

Some Air badges are Air's own course; others are a **tri-service course with Air
artwork**. The tool already knows which is which - it tags each summer-training row
`army` or tri-service, and Air and Army genuinely share thirteen of them.

So the tool needs both, and the key tells them apart:

- **Air-only course** → `air_<name>`, the key it already uses
- **Tri-service course, Air artwork** → `air_ctc_<army key>`

The tool will look up `air_ctc_dc_1` for an Air cadet and `ctc_dc_1` for an Army one,
same course, different picture. Your thirteen non-Air-specific summer badges line up
one-to-one with our thirteen tri-service rows, which is a good independent check that
both lists are right.

## 2. Summer training: 24 badges, here are all 24 keys

**Air-only, 11:**

```
air_aero_1      Basic Aviation Technology and Aerospace
air_aero_2      Advanced Aerospace
air_avtech_am   Adv Aviation Technology - Aircraft Maintenance
air_avtech_ao   Adv Aviation Technology - Airport Operations
air_avn_1       Basic Aviation
air_avn_2       Advanced Aviation
air_glider      Glider Pilot Scholarship
air_surv_1      Basic Survival
air_surv_2      Survival Instructor
air_oshkosh     Oshkosh Trip
air_exchange    International Air Cadet Exchange
```

**Tri-service, Air artwork, 13:**

```
air_ctc_gen     General Training           air_ctc_pb_1/2/3  Pipe Band basic/int/adv
air_ctc_arm_2   Air Rifle Marksmanship Instructor
air_ctc_fit_1   Basic Fitness and Sports   air_ctc_mb_1/2/3  Military Band basic/int/adv
air_ctc_fit_2   Fitness and Sports Instructor
air_ctc_dc_1    Basic Drill and Ceremonial
air_ctc_dc_2    Drill and Ceremonial Instructor
air_ctc_staff   Staff Cadet
```

This supersedes your proposed `air_summer_*`, `air_pipe_*` and `air_band_*`. Same
badges, names that match what the tool already calls the shared rows.

Note `air_ctc_staff` rather than `air_staff`: Staff Cadet is a tri-service row, and the
tool currently carries it twice by mistake. I'll fix that end.

## 3. `air_power`: you're right, drop it

Confirmed from the dress instruction, not just the poster. The Power Pilot Scholarship
produces **wings only**; the Glider Pilot Scholarship produces wings *and* a CTC badge,
and the rule is that the Glider CTC badge is worn only once a cadet upgrades to Power
wings - because the Glider wings themselves come off at that point.

So one CTC badge and two wings is exactly right, and `air_power` is my error. Removing
it from the tool.

## 4. Everything else, in order

**Appointments - in scope.** `air_appt_drum`, `air_appt_pipe`. The tool models
appointment insignia for Air on the right sleeve.

**Headdress - out of scope.** The tool draws sleeves and breast pockets only, no
headdress. Please skip it rather than extract something nothing can display. Noted as
existing so nobody re-discovers it.

**Effective Speaking - three keys**, `air_es_zone`, `air_es_prov`, `air_es_nat`. Drop
`air_es_winner`, and thank you for chasing where the named-award pattern actually
lives.

**Proficiency - accepted in full, all five families, all your proposed keys.** You were
right that "send nothing" was wrong, and the level-count argument is the stronger half:
silently reusing `mus_*` when Air has six badges and Army has five would misdraw and
never announce itself.

One thing your list told me that I did not know: **Marksmanship Classification is an
Air proficiency badge.** I had Air marked as wearing no marksmanship badge at all,
because Army wears it in a dedicated slot anchored at 6 cm and nothing said Air did.
It turns out Air has the same four classifications, worn in the six-badge cuff block
instead. That is a correction to the tool, and it came out of your inventory rather
than any instruction I had. Send `air_prof_marks_*` as proposed.

**Terminology - agreed and worth the flag.** The poster's "Proficiency Levels" are our
`air_level_*`, and our "proficiency" is the poster's five separate cuff families. I'll
put that note in the tool so nobody reconciles the two later.

**Squadron title - send both samples**, English and French, as
`air_squadron_title_en` and `air_squadron_title_fr`. Your point that it needs two text
fields and different geometry is well taken; fitting a generator is a separate job and
not now. Two real patches let the tool draw something honest in the meantime.

**Pilot wings** - `air_wings_glider`, `air_wings_power`. Nylon only, as you found.

**Duke of Edinburgh** - agreed, don't re-extract.

## 5. Championships: diff before you extract

Marksmanship and Biathlon Championships are **Canadian Cadet Movement** awards, not
element ones, and the tool already carries the Army poster's versions as
`comp_mk_zone/_prov/_nat/_winner` and `comp_bi_*`.

Before extracting eight more, compare them against `art/art_pack.js`. If they are the
same badges, say so and send nothing - we should not carry two copies of one award.
If they differ, send them as `air_marks_*` / `air_biath_*` per your proposal.

Same question for the two named-award badges, which we hold as `comp_mk_winner` and
`comp_bi_winner`.

## 6. Yes to the Air Force Association Medal

That closes an open question rather than adding a badge. It went into the rules pack as
"no source describes this medal's ribbon, so it is omitted rather than invented", and
slot 6 was left as a deliberate gap in the precedence numbering. A full-colour ribbon
and disc settles it.

Please add it to `medal_art_pack.js` as `medal_afa` / `ribbon_afa`, and I'll unhide
slot 6 and rewrite that open question as resolved.

**The Air Cadet Service Medal disc is the more valuable note.** Poster says bronze,
Blatherwick says gold, you built gold. Please look again and record whichever you
adopt with its reason - a disagreement between a photograph and a text description is
exactly the kind of thing that should end up in the manifest rather than being quietly
settled. The ribbon confirmation is good news either way.

## 7. Format reminders

Unchanged from the request: WebP q90, trim to the alpha bounding box, long edge capped
around 420 px, `{"d","aspect","m"}`, manifest with source region and fidelity per key.

No dimensions in cm - your regex finding none in the poster text matches the Army one,
where every number we trusted came from a ruler or a written instruction.

## 8. Expected count

| Group | Keys |
|---|---|
| Rank | 7 |
| Training level | 5 |
| Squadron title | 2 |
| Summer training | 24 |
| Proficiency | 18 |
| Effective Speaking | 3 |
| Pilot wings | 2 |
| Appointment | 2 |
| **Total** | **63** |

Plus up to 8 championship badges if §5 finds they differ, and `medal_afa` /
`ribbon_afa` into the medal pack separately.

Against your 75 in-scope: the difference is the 3 DofE we already have, the headdress,
and the 8 championships pending the diff. If your extracted count lands anywhere else,
that gap is the interesting part - tell me before reconciling it.
