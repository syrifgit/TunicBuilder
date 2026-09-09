# Air poster inventory — A-CR-CCP-850/DA-003

Sent before extraction, per your §"Do this first". Nothing extracted yet.

Source: `ACRCCP850DA003.pdf`, one page, 1728 x 2592 pt (24 x 36 in), Adobe
Illustrator CC 22.0, created 2018-03-04. Title metadata `16115_Air_24x36`.

**88 items on the poster. 66 vector, 22 raster.**

---

## 1. Inventory

Vector/raster determined from `page.get_image_rects()` placements, not by eye.
The 22 raster placements account for exactly the 22 embedded JPEGs.

| # | Family | Count | Kind | In scope? |
|---|---|---|---|---|
| 1 | Emblem | 1 | vector | no — heraldry |
| 2 | Flags and banners | 3 | **raster** | no — heraldry |
| 3 | Headdress badge | 1 | vector | **not in §4** |
| 4 | Shoulder badges (squadron title) | 2 | vector | yes |
| 5 | Commander's Cadet Commendation Pin | 1 | vector | no — pins done |
| 6 | Medals | 7 | **raster** | no — done |
| 7 | Additional years of service bar | 1 | **raster** | no — done |
| 8 | Ranks | 7 | vector | yes |
| 9 | Appointment (Drum Major, Pipe Major) | 2 | vector | **not in §4** |
| 10 | Proficiency Levels (Level 1–5) | 5 | vector | yes — your `air_level_*` |
| 11 | Pilot Wings | 2 | vector | yes |
| 12 | Duke of Edinburgh Award | 3 | vector | you already have it |
| 13 | Summer Training | **24** | vector | yes — §4 names 10 |
| 14 | Marksmanship Championships | 4 | **raster** | yes |
| 15 | Biathlon Championships | 4 | **raster** | yes |
| 16 | Effective Speaking | 3 | **raster** | yes |
| 17 | First Aid | 2 | vector | yes |
| 18 | Glider Pilot Familiarization | 2 | vector | yes |
| 19 | Marksmanship Classification | 4 | vector | yes |
| 20 | Physical Fitness | 4 | vector | yes |
| 21 | Music | 6 | vector | yes |

Uniform-worn items in scope for this pack, excluding medals, pins, flags and
the emblem: **75**.

## 2. The raster trap — you were right to warn me

The 22 raster items are: 3 flags, 7 medals, the service bar, and then

- **all 4 Marksmanship Championship badges**
- **all 4 Biathlon Championship badges**
- **all 3 Effective Speaking badges**

Those last eleven are badges you asked for by name. A vector-clustering
extractor drops every one of them and keeps everything else, which is the
army failure in miniature — and worse, because it would look like a clean run.

**Alpha segmentation will work here.** Verified rather than assumed: rendered
the page with `alpha=True` and probed it. The page corner, the section
gutters and the space between summer-training badges are all alpha 0, and only
**23.4%** of the page is fully opaque. The background is genuinely unpainted,
so alpha is a clean mask across the whole sheet. I'll use `recut_pins.py`'s
pattern and reconcile the count against this table before sending anything.

## 3. Dimensions stated in words: none

Regex over the full page text for any number followed by cm / mm / in / inch /
pouce returns nothing. The poster is labels only — every caption is a bilingual
badge name. So there is no paragraph to quote for §4 of your "what to tell me"
list, and every number I send will be a trimmed aspect.

## 4. Where §4 and the poster disagree

### 4.1 `air_power` does not exist on this poster

Summer Training shows **Glider Pilot Scholarship** and no Power Pilot
Scholarship badge. Power Pilot **Wings** exist under Pilot Wings, which is the
other badge you correctly separated. Suggest dropping `air_power`, or telling
me it comes from a source other than the poster.

### 4.2 Summer Training is 24 badges, not 10

Nine of your ten map cleanly. Fifteen badges have no key. Proposed, following
your existing patterns — all open to renaming:

| Poster badge | Existing key | Proposed |
|---|---|---|
| General Training | | `air_summer_general` |
| Air Rifle Marksmanship Instructor | | `air_summer_rifle_instr` |
| Basic Aviation Technology and Aerospace | `air_aero_1` | |
| Advanced Aerospace | `air_aero_2` | |
| Adv Aviation Tech – Aircraft Maintenance | `air_avtech_am` | |
| Adv Aviation Tech – Airport Operations | `air_avtech_ao` | |
| Basic Aviation | `air_avn_1` | |
| Advanced Aviation | `air_avn_2` | |
| Glider Pilot Scholarship | `air_glider` | |
| Pipe Band Basic / Intermediate / Advanced Musician | | `air_pipe_1/2/3` |
| Staff Cadet | `air_staff` | |
| Oshkosh Trip | | `air_summer_oshkosh` |
| International Air Cadet Exchange | `air_exchange` | |
| Basic Fitness and Sports | | `air_summer_fitness` |
| Fitness and Sports Instructor | | `air_summer_fitness_instr` |
| Basic Survival | `air_surv_1` | |
| Survival Instructor | `air_surv_2` | |
| Basic Drill and Ceremonial | | `air_summer_drill` |
| Drill and Ceremonial Instructor | | `air_summer_drill_instr` |
| Military Band Basic / Intermediate / Advanced Musician | | `air_band_1/2/3` |

### 4.3 Appointment badges have no keys

Drum Major and Pipe Major, worn as chevron-and-device rank-style badges.
Proposed `air_appt_drum`, `air_appt_pipe`. Tell me if the tool has no slot for
these and I'll leave them out.

### 4.4 Headdress badge has no key

Worn on the wedge. Proposed `air_headdress`. Out of scope if the tool doesn't
model headdress.

### 4.5 Terminology collision worth knowing about

The poster calls Level 1–5 the **"Proficiency Levels"**. Your §"Proficiency"
means the six cuff insignia, which the poster splits across five differently
named sections. Your `air_level_*` keys are the poster's *Proficiency Levels*
— correct badge, different word. Worth a comment in the tool so nobody
reconciles the two later.

## 5. Answers to your open questions

### Effective Speaking: three levels, no winner badge

Zone, Provincial, National. Nothing above National. So `air_es_zone`,
`air_es_prov`, `air_es_nat` — **drop `air_es_winner`**.

The named-award badge you were thinking of does exist, just not here:
Marksmanship Championships carries a fourth badge, the **Vamplew & Clément
Tremblay Awards**, and Biathlon carries the **Myriam Bédard, Nikki Keddie &
Jean-Philippe Le Guellec Awards**. That's the biathlon pattern — it applies to
marksmanship and biathlon, not to effective speaking.

Proposed: `air_marks_zone/_prov/_nat/_vamplew`,
`air_biath_zone/_prov/_nat/_bedard`.

### Proficiency: five families, and no, you cannot reuse the army art

| Family | Count | Levels |
|---|---|---|
| Physical Fitness | 4 | Bronze, Silver, Gold, Excellence |
| First Aid | 2 | Emergency, Standard |
| Music | 6 | Basic Qualification, Level 1–5 |
| Marksmanship Classification | 4 | Marksman, First Class, Expert, Distinguished |
| Glider Pilot Familiarization | 2 | Front Seat, Back Seat |

**Send nothing is the wrong call.** Two reasons:

1. The artwork is Air-specific — dark navy octagons with pale blue devices,
   nothing like the army versions.
2. The **level counts differ**. Air Music is six badges (Basic Qualification
   plus five levels). If `mus_*` in the tool assumes the army's set, reuse
   silently mismatches. Same risk on fitness.

Proposed `air_prof_fitness_bronze/_silver/_gold/_excellence`,
`air_prof_firstaid_emergency/_standard`,
`air_prof_music_basic/_1/_2/_3/_4/_5`,
`air_prof_marks_marksman/_first/_expert/_distinguished`,
`air_prof_glider_front/_back`.

Glider Pilot Familiarization is a sixth family you didn't list — it fits the
cuff block and is probably one of the six.

### Squadron title: not a blank, two filled samples

The poster shows two finished patches, not a blank plate:
**ROYAL CANADIAN AIR CADETS / 89 / PACIFIC** and **CADETS DE L'AVIATION
ROYALE DU CANADA / 96 / ALOUETTE**. English and French versions of the same
badge.

It is also a **different shape from the army corps title** — a half-round dome
with the arched element name around the top edge, squadron number large in the
centre, squadron name on a straight line below. The army title is a scrolled
banner. The existing corps-title generator will not produce these; it would
need new geometry fitted the same way.

Also note the squadron name is part of the badge, so a generator needs two
text fields, not one. Say the word and I'll fit it, but it's a separate job
from this extraction.

### Pilot wings: two, nylon only

Power Pilot Wings and Glider Pilot Wings. **No silver or gold wire-thread
variants on the poster**, so `air_wings_glider` / `air_wings_power` only.

### Duke of Edinburgh: you already have it

Three levels, and `art_pack.js` already in the tool carries `dofe_bronze`,
`dofe_silver` and `dofe_gold` at aspect 1.197. The poster's are the same oval
cypher insignia. Don't re-extract — point the slot at the existing art.

## 6. One thing for the medal pack, not this one

**The Air Force Association Medal is on this poster.** Full colour, ribbon and
disc, as one of the seven raster medal images.

That is the medal I sent back as unsourced last round, with slot 6 asked to be
hidden. Blatherwick's chapter had the award terms but no ribbon description,
and nothing else described it. This poster shows it.

I have not touched it — it's outside this request's scope and the medal pack
is a different file. But `afa` is now buildable. Say the word and I'll add it
to `medal_art_pack.js` and unhide slot 6.

Two smaller notes from the same row, both worth checking against what I
already sent you:

- The Air Cadet Service Medal ribbon here reads royal blue / gold / light blue
  / gold / royal blue, which **confirms** the Blatherwick description I built
  `airservice` from.
- Its disc renders **bronze on this poster**, where Blatherwick says "a round
  gold coloured medal". I built it gold. Worth a second look before anyone
  trusts that one.

---

## Ready to extract

On your go I'll pull all 75 in-scope items by alpha segmentation, trim to the
alpha bounding box, cap the long edge at 420 px, encode WebP q90, and ship
`air_art_pack.js` plus a manifest with per-key source region and fidelity.
I'll reconcile extracted count against the table in §1 and report any gap.

What I need from you first: confirm or rename the proposed keys in §4.2, 4.3,
4.4 and §5, and tell me whether appointment badges and the headdress badge are
in scope at all.
