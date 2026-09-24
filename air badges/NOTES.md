# Air artwork pack — notes

63 keys, exactly the list in `AIR_ARTWORK_DECISIONS.md` §2. Extracted count
matches the expected count in §7. No gap.

`air_art_pack.js` is 1.17 MB, 874 KB of that WebP payload. Format as agreed:
`{"d","aspect","m"}`, WebP q90, trimmed to the alpha bounding box, long edge
capped at 420 px.

---

## The finding that matters most

**You told me aspect is real because it comes from the image. For 21 of the 63
badges that turns out to be false**, and your measurements are what caught it.

| Family | Badges | Image aspect vs ruler |
|---|---|---|
| Octagons (summer training + proficiency) | 42 | **0.997–1.003 vs 1.000** — exact |
| Training level | 5 | 1.170 vs 1.270 — **−7.9%** |
| Squadron title | 2 | 2.253 vs 2.076 — **+8.5%** |
| Rank, Corporal | 1 | 1.139 vs 1.272 — **−10.4%** |
| Rank, Flight Corporal | 1 | 0.953 vs 1.033 — −7.8% |
| Rank, Sergeant | 1 | 0.965 vs 1.033 − −6.6% |
| Rank, Flight Sergeant | 1 | 0.834 vs 0.870 − −4.1% |

The 42 octagons are drawn perfectly. Everything else is off, in both
directions, and by an amount that varies *within* the rank family. So the
poster is not merely at the wrong scale, it is at the wrong **shape** for
these 21 badges.

Rank widths are the one part that checks out exactly: all four chevron ranks
measure 15.0 pt/cm against your "all 10.5 cm wide". The disagreement is
entirely in the heights, and the poster draws them consistently taller than
the ruler — Corporal by about 10 mm at full size. That is too large to be
ruler error on a 3.25 in measurement, so I have not tried to reconcile it.
Worth a re-measure on Corporal specifically before anyone trusts either
number.

**What I shipped.** `aspect` in the pack is the true **image** aspect. It has
to be, or the artwork skews. The manifest carries `measured_mm`,
`measured_aspect` and `aspect_delta_pct` alongside it for the 54 keys your
measurements cover. My recommendation: **size from `measured_mm` and let the
art sit slightly off-shape**, rather than drawing a badge at the wrong
footprint. Your call, and either way it is recorded per key.

I can also letterbox the 21 mismatched badges with transparent padding so
`aspect` equals `measured_aspect` without distorting the art. Say the word.
I did not do it unasked because it moves where the ink sits inside the frame.

### Scale, for the record

Same story as the army poster, slightly wider range: **15.0 to 26.4 pt/cm**.

| Family | pt/cm |
|---|---|
| Ranks (chevrons) | 15.0 |
| Leading Air Cadet | 18.2 |
| Training level | 20.9 |
| Octagons | 21.3–22.4 |
| Squadron title | 26.4 |

Note the Leading Air Cadet is drawn 21% larger than the other ranks despite
sitting in the same row. Nothing on this poster can be sized by proportion.

## Nine badges have no physical measurement

`air_rank_WO1`, `air_rank_WO2`, `air_appt_drum_major`, `air_appt_pipe_major`,
`air_wings_power`, `air_wings_glider`, `air_es_zone`, `air_es_prov`,
`air_es_nat`.

Your list covered Corporal through Flight Sergeant and the Leading Air Cadet,
so the two Warrant Officer badges are the gap in the rank row. Each of these
nine carries `"measured_mm": null` and a note saying poster proportions are
not reliable for it. Given the numbers above, I would not infer any of them
from the poster.

Also: the Leading Air Cadet has a width (80 mm) but no height, so it has
`measured_mm: [80.0, null]` and no `measured_aspect`.

## Your three extraction warnings

**Fitness off by one.** Matched by caption, not by number. `air_fit_2` is the
Bronze badge carrying numeral I, through `air_fit_5` for Excellence with the
maple leaf.

**Marksmanship whole.** `air_mk_1` to `air_mk_4` are single octagons, numeral
and rifles together. No split.

**Music numerals are live text.** Checked as asked. All six crops are
distinct: pairwise mean absolute difference between the five Level badges is
0.9–2.9, and 13.5–14.6 between any Level and Basic Qualification, which is the
different central device. The numerals rendered. My blob detection *does*
strip the text layer, but only to stop captions forming blobs — the extraction
render is normal and keeps text. The caption guard only discards text runs
that fall outside the badge's own outline, so numerals inside the octagon were
never at risk.

## Method

Alpha segmentation, per your `recut_pins.py` pattern. Rendered the page at
150 dpi with `alpha=True`, blanked all 707 text runs so captions could not
form blobs, dilated 11 px to join badge parts (crown to chevron), then
connected-component labelled. 90 blobs, of which 63 are in scope.

Every badge was then re-rendered individually from the PDF at a zoom giving a
420 px long edge, so nothing is upsampled from the 150 dpi pass. The three
raster-backed Effective Speaking badges are capped at their source ppi
(409–415) instead, which lands them at 259–266 px rather than inventing
detail.

**Reconciliation against the §1 inventory:** 63 extracted, 63 expected. The
other 27 blobs are the emblem, 3 flags, headdress badge, 7 medals, the service
bar, the Commander's Cadet Commendation Pin, 8 championships, 3 DofE and 2
panel-outline artefacts. All accounted for, none dropped.

Caption guard fired on **zero** badges — no padding had to be reduced.

## Effective Speaking: white ground keyed (revision 2)

`air_es_zone`, `air_es_prov` and `air_es_nat` shipped opaque the first time.
They are photographs on white paper, and their PDF smask is a plain rectangle,
so page alpha never touched the paper. Fixed in `extract.py`
(`key_white_ground`), which now runs on any raster-backed badge.

Paper is flood-filled inward from the frame, so the badge's own cream and
metallic interior is kept — a plain whiteness threshold would have eaten it.
The fill has to treat already-transparent pixels as passable, because the
frame of the clip is the 1 pt transparent bleed rather than paper; that was
the bug in my first attempt at the fix. Fringe pixels then get a soft matte
from the whiteness and the white divided back out, so there is no pale halo
when the badge draws on cloth.

Result: all three RGBA with transparent corners, 3.4–6.0% of each frame keyed,
2–4% partial alpha at the rounded edge. Checked against a mid-green ground.
Aspects moved slightly with the re-trim: zone 1.027, provincial 1.000,
national 1.000.

Verified across the whole pack: **63 of 63 are RGBA, none has four opaque
corners.**

## Fidelity

Every key is `measured` in the sense that matters: the artwork is lifted
unmodified from the publication, not redrawn or recoloured. Nothing here is
stylised, unlike the medal discs. What is *not* reliable is dimension, which
is why the aspect section above exists.

---

# Medal pack update

`medal_art_pack.js` is now **52 keys**, up from 50.

## `medal_afa` / `ribbon_afa` — slot 6 can be unhidden

Built. The ribbon was sampled off the poster's full-colour image at 9x and
scanlined:

**navy `#101A3D` · pale teal `#70B3BD` · navy · dark maroon `#491219` (41% of
the width) · navy · teal · navy**

Gold disc, plain straight bar suspender with a maple leaf lug, crown and
laurel sprays above an RCAF eagle, `ASSOCIATION` around the lower edge. The
upper legend is not legible at poster resolution, so the disc carries only the
lower one.

Flagged `MEASURED colour / ESTIMATED geometry`. The stripe **proportions** come
from the image and are solid. The **35 mm ribbon width** is assumed — no text
source describes this ribbon, which is exactly why it was unsourced last
round. `UNSOURCED` in `medal_specs.py` is now empty; every medal in the CATO
13-16 precedence is built.

## Air Cadet Service Medal disc: changed to bronze

Recorded in the manifest with the reasoning, as you asked.

Sampled rather than eyeballed. The disc mean is `#9E7B60` — hue 26°, a brown —
where gold sits near hue 44°. That is bronze, not a gold medal reading warm in
print.

**Adopted the poster.** It is the issuing authority's own current colour
artwork, published by DND in 2018. Blatherwick is a third-party text
compendium, and "a round gold coloured medal" reads like it was written from
the Army medal's description, which genuinely is gold. Revert with one word:
set `metal` back to `"gold"` in `medal_specs.py`.

The same image **confirms** the Blatherwick ribbon description I built
`airservice` from — royal blue, gold, light blue, gold, royal blue — so that
part needed no change. A source being wrong about one thing and right about
another is worth having written down.
