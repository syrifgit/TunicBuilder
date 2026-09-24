# Air artwork: decisions

Answers to `AIR_INVENTORY.md`. **Go ahead and extract.** Everything is settled below,
including the championship diff, which I've already run.

The inventory was worth the round trip. Eleven of the badges I asked for by name are
raster, so a vector-clustering run would have dropped exactly those and still looked
like a clean pass. That's the army failure, caught before it cost anything.

---

## 1. The naming rule

One rule for every key: **`air_` + the key the tool already uses for that badge's row.**

- **The row is shared with Army** (a tri-service CTC course, a proficiency, an
  appointment): `air_` + the army key. `ctc_dc_1` → `air_ctc_dc_1`, `fit_2` →
  `air_fit_2`, `appt_drum_major` → `air_appt_drum_major`. The tool tries the prefixed
  key first and falls back to the army one, the way it already does for the CTC grid,
  so there's no lookup table to get wrong.
- **The row is Air's own** (rank, training level, Air-only courses): Air's own name.
  `air_rank_FSgt`, `air_level_3`, `air_surv_1`.

That supersedes your proposed `air_summer_*`, `air_pipe_*`, `air_band_*`, `air_prof_*`,
`air_appt_drum` / `air_appt_pipe` and `air_marks_*` / `air_biath_*`. Same badges, with
names the tool can resolve without a mapping layer.

## 2. The keys, all 63

Exactly these names. Match each one by its poster caption, not by the number in the
key (see the fitness note below).

**Rank - 7**

| Key | Poster caption |
|---|---|
| `air_rank_LAC` | Leading Air Cadet |
| `air_rank_Cpl` | Corporal |
| `air_rank_FCpl` | Flight Corporal |
| `air_rank_Sgt` | Sergeant |
| `air_rank_FSgt` | Flight Sergeant |
| `air_rank_WO2` | Warrant Officer Second Class |
| `air_rank_WO1` | Warrant Officer First Class |

**Training level - 5** (the poster's "Proficiency Levels")

| Key | Poster caption |
|---|---|
| `air_level_1` to `air_level_5` | Level 1 to Level 5 |

**Appointment - 2**

| Key | Poster caption |
|---|---|
| `air_appt_drum_major` | Drum Major |
| `air_appt_pipe_major` | Pipe Major |

**Squadron shoulder insignia - 2**

| Key | Poster caption |
|---|---|
| `air_squadron_title_en` | ROYAL CANADIAN AIR CADETS / 89 / PACIFIC |
| `air_squadron_title_fr` | CADETS DE L'AVIATION ROYALE DU CANADA / 96 / ALOUETTE |

**Pilot wings - 2**

| Key | Poster caption |
|---|---|
| `air_wings_power` | Power Pilot Wings |
| `air_wings_glider` | Glider Pilot Wings |

**Summer training, Air-only - 11**

| Key | Poster caption |
|---|---|
| `air_aero_1` | Basic Aviation Technology and Aerospace |
| `air_aero_2` | Advanced Aerospace |
| `air_avtech_am` | Advanced Aviation Technology - Aircraft Maintenance |
| `air_avtech_ao` | Advanced Aviation Technology - Airport Operations |
| `air_avn_1` | Basic Aviation |
| `air_avn_2` | Advanced Aviation |
| `air_glider` | Glider Pilot Scholarship |
| `air_surv_1` | Basic Survival |
| `air_surv_2` | Survival Instructor |
| `air_oshkosh` | Oshkosh Trip |
| `air_exchange` | International Air Cadet Exchange |

**Summer training, tri-service - 13**

| Key | Poster caption |
|---|---|
| `air_ctc_gen` | General Training |
| `air_ctc_arm_2` | Air Rifle Marksmanship Instructor |
| `air_ctc_fit_1` | Basic Fitness and Sports |
| `air_ctc_fit_2` | Fitness and Sports Instructor |
| `air_ctc_dc_1` | Basic Drill and Ceremonial |
| `air_ctc_dc_2` | Drill and Ceremonial Instructor |
| `air_ctc_staff` | Staff Cadet |
| `air_ctc_pb_1`, `_2`, `_3` | Pipe Band Basic, Intermediate, Advanced Musician |
| `air_ctc_mb_1`, `_2`, `_3` | Military Band Basic, Intermediate, Advanced Musician |

**Proficiency - 18**

| Key | Poster caption |
|---|---|
| `air_fit_2` | Physical Fitness - Bronze (numeral I) |
| `air_fit_3` | Physical Fitness - Silver (II) |
| `air_fit_4` | Physical Fitness - Gold (III) |
| `air_fit_5` | Physical Fitness - Excellence (maple leaf) |
| `air_fa_1` | First Aid - Emergency |
| `air_fa_2` | First Aid - Standard |
| `air_mus_basic` | Music - Basic Qualification |
| `air_mus_1` to `air_mus_5` | Music - Level 1 to Level 5 |
| `air_mk_1` | Marksmanship Classification - Marksman |
| `air_mk_2` | Marksmanship Classification - First Class Marksman |
| `air_mk_3` | Marksmanship Classification - Expert Marksman |
| `air_mk_4` | Marksmanship Classification - Distinguished Marksman |
| `air_glider_fam_1` | Glider Pilot Front Seat Familiarization |
| `air_glider_fam_2` | Glider Pilot Back Seat Familiarization |

**Effective Speaking - 3**

| Key | Poster caption |
|---|---|
| `air_es_zone` | Zone Championship |
| `air_es_prov` | Provincial Championship |
| `air_es_nat` | National Championship |

### Three things to watch while extracting

- **Fitness is off by one on purpose.** `air_fit_2` is Bronze, and Bronze carries
  numeral **I**. The tool's fitness level 1 is "Participated", which has no badge, so
  the keys start at 2 to match the army pack. Go by the caption. Every other family's
  key number matches the numeral on the badge.
- **Marksmanship is one piece.** Each Air badge is a single octagon with the rifles and
  the numeral inside it. Army's is a numeral tab and a pair of rifles sewn separately,
  which is why the army pack has `mk_1_num` and `mk_1_rifles`. Send `air_mk_1` to
  `air_mk_4` whole, no split.
- **The music numerals are live text.** The I to V on Music Levels 1-5 are text runs in
  the PDF, not paths. I stripped the text layer and re-rendered: all five Level badges
  come out identical. A normal render picks them up, but anything that drops text
  won't, so check the six music crops are distinct before packing. No other family has
  this. Their numerals are outlined and survive text removal.

## 3. Send nothing for these

- **Championships, all 8.** I diffed them against the army poster. Seven of the eight
  embedded JPEGs are byte-identical, same MD5. The eighth, Biathlon Zone, is the same
  photograph cropped about 5% tighter (163 × 160 px against 172 × 169). They're the
  pins we already hold as `comp_mk_*` and `comp_bi_*`, named awards included, so no
  `air_marks_*` or `air_biath_*`.
- **Duke of Edinburgh, 3.** Same insignia as `dofe_bronze`, `dofe_silver` and
  `dofe_gold`, as you said.
- **Headdress badge.** The tool draws sleeves and breast pockets only. Noted as existing
  so nobody re-discovers it.

## 4. The rest

- **`air_power`: you're right, it's dropped.** The Power Pilot Scholarship gives wings
  only. The Glider Pilot Scholarship gives wings and a CTC badge, and the Glider CTC
  badge only goes on once the cadet upgrades to Power wings, because the Glider wings
  come off then. So one CTC badge and two sets of wings is right. It's gone from the
  tool.
- **Appointments are in scope.** Air wears them on the right sleeve.
- **Effective Speaking is three levels.** No `air_es_winner`. Thanks for tracking down
  where the named-award pattern actually lives.
- **Proficiency: all five families.** You were right that "send nothing" was wrong, and
  the artwork is the reason: navy octagons with pale-blue devices, where Army's are
  green circles with gold. The level counts aren't a reason, though. They match in
  every shared family. Army Music is Basic plus Levels 1-5 as well, and `mus_basic` is
  already in the army pack.
- **Marksmanship Classification is an Air proficiency badge.** I had Air down as wearing
  no marksmanship badge at all. That's a correction to the tool, and it came out of
  your inventory, not out of any instruction I had.
- **Terminology: agreed.** The poster's "Proficiency Levels" are our `air_level_*`, and
  our "proficiency" is the poster's five cuff families. It's noted in the rules pack so
  nobody reconciles the two later.
- **Squadron title: send both samples.** Fitting a generator is a separate job for
  later. Two real patches let the tool draw something honest in the meantime.
- **Pilot wings: nylon only**, as you found.
- **Staff Cadet is `air_ctc_staff`.** It's a tri-service row. The tool was carrying it
  twice by mistake, and that's fixed.

## 5. Medal pack: yes to the Air Force Association Medal

That closes an open question rather than adding a badge. The tool omitted it because
nothing described its ribbon, and slot 6 was left as a deliberate gap in the precedence
numbering. A full-colour ribbon and disc settles it. Please add it to
`medal_art_pack.js` as `medal_afa` / `ribbon_afa`, and I'll unhide slot 6.

**Look at the Air Cadet Service Medal disc again.** The poster shows bronze, Blatherwick
says gold, and you built it gold. Record whichever you adopt and why in the manifest. A
photograph disagreeing with a text description should be written down, not quietly
settled. The ribbon confirmation is good news either way.

## 6. Format

Unchanged from the request: WebP q90, trim to the alpha bounding box, long edge capped
around 420 px, `{"d","aspect","m"}`, and a manifest with the source region and fidelity
per key. No dimensions in cm. Your regex finding none in the poster text matches the
Army one, where every number we trusted came from a ruler or a written instruction.

## 7. Expected count

| Group | Keys |
|---|---|
| Rank | 7 |
| Training level | 5 |
| Appointment | 2 |
| Squadron title | 2 |
| Pilot wings | 2 |
| Summer training | 24 |
| Proficiency | 18 |
| Effective Speaking | 3 |
| **Total** | **63** |

Against your 75 in scope, the other 12 are the 8 championships, the 3 DofE and the
headdress. Plus `medal_afa` / `ribbon_afa` into the medal pack separately. If your
extracted count lands anywhere else, tell me about the gap before reconciling it.
