# Air cadet artwork request

From the session that maintains `demo/tunic.template.html`. You did the medals pack;
this is the same job for Air Cadets, from the air equivalent of A-CR-CCP-750/DA-003.

The tool already models Air placement in full (rank on both arms, training level on the
left, the six-badge cuff block). What it lacks is pictures: every Air badge currently
draws **army artwork**. A Flight Sergeant renders as an army warrant officer crown.

---

## Do this first, before extracting anything

**Send an inventory, not artwork.** One line per badge family on the poster: family
name, how many badges, and whether it's vector or raster. Ten minutes of your time
saves a round trip, because §4 below is my best guess at what the poster contains and
I have not seen it.

Then extract. If the inventory and §4 disagree, the poster wins and I'll adjust.

## Two things that cost us badly on the army poster

**1. The extractor sees vector objects only.** Ours clustered vector drawings and
silently dropped every raster region: the whole physical fitness block, all the
competition pins, and seven medals. Nobody noticed until the badges were missing from
the page. If you're reusing that approach, **render each region and segment on the
alpha channel instead** - the poster background is unpainted, so alpha is a clean mask.
`src/recut_pins.py` in this repo is the working pattern.

Before you finish, count what you extracted against your own inventory and tell me
about any gap. A missing badge that nobody flags becomes a badge drawn as a grey box
three weeks later.

**2. Artwork identifies badges. It does not dimension them.** We inferred a
marksmanship badge width from poster proportions once and it was 8% wrong. The army
poster isn't even drawn to a single scale - 13 to 24 points per cm depending which
family you measure.

So: give me the trimmed **aspect** (that's real, it comes from the image) and never a
width or height in cm unless the *publication states it in words*. If it does, quote
the paragraph separately - don't bake it into the artwork.

## Format

Same as the medal pack, one file, `air_art_pack.js`:

```js
const AIR_ART = {"<key>": {"d": "<base64>", "aspect": <w/h>, "m": "image/webp"}, ...};
```

**WebP quality 90, not PNG.** We switched: these are photographic scans and PNG stored
them at ~2.3 bytes per pixel. WebP q90 is a third of the size and visually identical at
the size the tool draws. `Image.save(buf, "WEBP", quality=90, method=4)`.

Trim to the alpha bounding box before measuring the aspect, and cap the long edge at
about 420 px - the tool never draws a badge larger than that.

Keep a manifest alongside it, same shape as `medal_art_manifest.json`: per key, the
source page or region, and a `fidelity` flag. That's what becomes the citation.

## The keys

Exactly these names. They're what the tool looks up, so anything else needs a mapping
layer and will get one wrong eventually.

**Rank** - 7 badges. Cadet wears none.

```
air_rank_LAC    Leading Air Cadet          air_rank_FSgt   Flight Sergeant
air_rank_Cpl    Corporal                   air_rank_WO2    Warrant Officer 2nd Class
air_rank_FCpl   Flight Corporal            air_rank_WO1    Warrant Officer 1st Class
air_rank_Sgt    Sergeant
```

**Training level** - 5 badges, `air_level_1` to `air_level_5`. Air's equivalent of the
army star. Note Air carries a level 5 badge where the army has none, so all five exist.

**Squadron shoulder insignia** - `air_squadron_title`. If it's a blank plate that gets
a squadron number added, send the blank and say so; that's how the army corps title
works here and there's already a kit for generating them.

**Summer training** - 10 badges. These keys are already in the tool:

```
air_surv_1      Survival, Basic            air_avtech_am   Adv Aviation Tech, Aircraft Maintenance
air_surv_2      Survival, Instructor       air_avtech_ao   Adv Aviation Tech, Airport Operations
air_avn_1       Aviation, Basic            air_glider      Glider Pilot Scholarship
air_avn_2       Aviation, Advanced         air_power       Power Pilot Scholarship
air_aero_1      Aviation Technology and Aerospace, Basic
air_aero_2      Aerospace, Advanced
```

**Pilot wings** - `air_wings_glider`, `air_wings_power`. These are the sewn wings worn
above the left breast pocket, which are a different badge from the two CTC badges
above. If the poster shows the silver and gold wire-thread variants as well, send them
as `air_wings_glider_silver` / `_gold` and so on, but the issued nylon ones are what we
need first.

**Participation** - `air_staff` (Staff Cadet), `air_exchange` (International Exchange).

**Effective Speaking** - Air's equivalent of the army National Rifle Team, and I'm told
it follows the biathlon pattern. Best guess at the keys:
`air_es_zone`, `air_es_prov`, `air_es_nat`, and `air_es_winner` if a national-winner
badge exists. Tell me the real levels and I'll match them.

**Proficiency** - **this is the one I can't name.** Air wears up to six proficiency
insignia above the left cuff. The tool currently offers the army's three families
(fitness, first aid, music) because that's all it knows. Please list what the poster
actually shows and propose keys as `air_prof_<family>_<level>`. If fitness, first aid
and music are common across elements with identical artwork, say so and send nothing -
we'll reuse `fit_*`, `fa_*`, `mus_*`.

## Do not send

- medals, ribbons or commendation pins - done, and they're tri-service
- anything army - we have it
- `group_*` / `rack_*` style composites - the tool lays out its own rows
- marketing or heraldry artwork that never goes on a uniform

## What to tell me at the end

1. inventory vs extracted, and any gap
2. anything on the poster that doesn't fit the keys above
3. anything above that isn't on the poster
4. any dimension the publication states **in words**, quoted with its paragraph
5. fidelity per badge, the way you did for the medals - measured, estimated, or stylised

That last one matters more than it sounds. Half the value of the medal pack was
`NOTES.md` telling us which colours were sampled and which were eyeballed.
