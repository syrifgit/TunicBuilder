# Ribbon back to 35 mm, on a 46 mm canvas

`RIBBON_FRAC = 0.80` is gone. It solved the overhang problem the wrong way
round: shrinking the ribbon to 28.2 mm inside a 35 mm canvas opened a 7 mm gap
between every mounted pair and left each ribbon reading narrower than its own
33 mm disc.

Now the ribbon is 35 mm on a canvas wide enough for the metal:

```python
RIBBON_W   = 35.0
CLAW_BAR_H = RIBBON_W / 7.0                       # 5.0
CANVAS_W   = RIBBON_W + 2.0 * (CLAW_BAR_H + 0.5)  # 46.0
```

The canvas is derived, not chosen. The binding overhang is the squared return
on a bar-and-claw suspension - as thick as the bar is tall, turning up outside
the ribbon edge - so sizing off that keeps
`ret = min(bh, (width_mm - rw)/2 - 0.25)` from ever clamping, and St. George
and the AFA get their full 5 mm returns. The extra 0.5 rather than the 0.25
the formula reserves leaves the return's own 0.24 mm stroke somewhere to go;
at 0.25 the outer edge landed 0.1 mm inside the canvas, which is not margin.

Everything else overhangs less and was never the constraint: the ANAVETS
MERITUM bar flares to 1.15x the ribbon (40.25 mm), the Bravery and ACMM bars
to 1.10x (38.5 mm).

**Nothing else moved.** The disc, suspensions, bars, legends and `susp_gap`
are unchanged in millimetres. Measured on the 300 dpi output: all 27 ribbons
come out 35.3 mm (35 plus the 0.3 mm outline stroke), the widest overhang in
the set is 45.30 mm on the 46 mm canvas, and ink runs y=0.00 to 99.91 mm as
before.

Manifest: `w_mm` is now the canvas (46.0, aspect 0.46) and every medal key
carries `ribbon_w_mm: 35`. The 27 `ribbon_*` keys are untouched at 35 x 10,
aspect 3.5.

1200 dpi renders are now 2173 x 4724 px. `renders_1200dpi/README.txt` says
explicitly to mount at a 35 mm pitch rather than tiling at 46.

## A bug this turned up in the clearance test

`clearance.py` hard-coded `PX = 600.0 / 35.0` while rendering at
`output_width=600`. Once the canvas went to 46 mm that scaled every gap by
0.76, and the first run after the change reported Legion at 0.37 mm and
Bravery at 1.17 mm - it read as though widening the canvas had tightened every
clearance, which is geometrically impossible. It now derives px/mm from
`M.CANVAS_W`. Real numbers, unchanged within rasterisation noise:

| | gap | | | gap |
|---|---|---|---|---|
| `bravery` | 1.61 mm | | `anavets` | 2.17 mm |
| `strathcona` | 0.92 mm | | `stgeorge` | 0.85 mm |
| `legion` | 0.48 mm | | `seaservice` | 2.20 mm |
| `navyleague` | 3.97 mm | | `armyservice` | 1.63 mm |
| `acmm` | 0.89 mm | | `airservice` | 0.92 mm |
| `afa` | 2.76 mm | | | |

## AFA provenance rewritten

The note was stale on both counts. It now reads:

> Stripe PATTERN scanlined at 9x off the full-colour medal image on
> A-CR-CCP-850/DA-003: seven stripes. WIDTHS 9/9/9/46/9/9/9 and COLOURS navy
> #1B2350, light aqua #7EC3C8, maroon #6B1D2E are both read off the close-up
> reference photo, per the round-4 corrections; the 46% centre replaces an
> earlier 41% taken from the poster. An earlier note here recorded the ANAVETS
> palette per Lt Beal on the theory that the poster print had shifted - that is
> superseded: Lt Beal confirms the photo. …

`fidelity` goes from `MEASURED pattern / STATED colour` to
`MEASURED pattern / MEASURED colour`, since the colours now come from a
measured photo rather than a verbal instruction.

## ANAVETS comma

Unchanged. ARMY, NAVY & AIR FORCE VETERANS.

---

# Reproducibility fix found while packaging

Smoke-testing the download - unzip into an empty directory, rebuild, compare -
turned up two things worth recording.

**The published `png/` and `svg/` trees were stale.** The pack was current and
correct, but the loose renders beside it were from an earlier round. Re-copied
and verified file by file against the build.

**The SVGs were not byte-reproducible.** The PNGs, manifest and pack matched
exactly, but 11 SVGs - every ACMM bar state - differed between runs. Cause:

```python
mets = {b[1] for b in spec.get("award_bars", [])}
for extra in mets:                 # a SET
```

Set iteration order for strings depends on the hash seed, which changes
between processes, so the `<defs>` gradients came out in a different order
each run. It never affected rendering, which is why the PNGs were identical
and the earlier clean-room checks - which compared the manifest, the PNGs and
the pack - passed. Now `sorted(mets)`, and the SVGs reproduce byte for byte
too.

Worth being precise about: the earlier rounds' "byte-identical" claims covered
the manifest, all 58 PNGs and the pack. They did not cover the SVGs, because
the test did not look at them. It does now.

---

# ANAVETS centre - traced. Nothing stylised left.

Your render closes the set. The crown, enamelled shield and maple sprays are
traced; the hand-built asymmetric shield, the drawn crown and the drawn sprays
are all gone.

The only coloured face in the set, so this is **five passes** rather than two:
silver for the crown and sprays, the shield's white areas, the red enamel, the
blue enamel, and the engraved line work over the lot.

Three things had to be worked around, and all three were dead ends first:

1. **The silver field is stippled.** A high-pass picks up the matte texture
   everywhere, so a relief mask is not selective on its own - the first
   silhouette attempt returned the entire face. The line work survives as long
   connected curves while the stipple breaks into hundreds of specks, so
   components under 120 px go.
2. **The inner ring closes the fill.** The circle at 0.58R between the centre
   and the legend band is part of the outline, so filling the outline encloses
   the whole face and hands back one 212,000 px blob. A radius histogram puts
   the ring at 0.58 and the sprays ending by 0.55, so cutting at 0.572R lets
   the crown and each spray leaf fill separately.
3. **The shield cannot be filled from its enamel.** Its white areas open onto
   the shield's silver border rather than being enclosed by red and blue, so
   filling holes in the enamel leaves them out - the first attempt lost the
   entire lower-left quarter. A heater shield is convex, so the convex hull of
   the enamel recovers the whole shield and the white areas are the hull minus
   the enamel.

The ink also had to exclude the shield's interior, eroded 4 px: the enamel is
darker than the silver field, so it traces as line work and paints over itself.

The disc is fitted by least squares on the medal's own outline below the
suspension ring, residual 1.59 px. A bounding box would have put the centre
20 px high, because the ring counts.

Placement comes from the tracer as before: width 0.5725 of the disc diameter,
centre -0.002R, so `device_scale` 1.245 and no offset. Clearance to the legend
**2.15 mm**. Clean-room rebuild verified.

**One thing I did not change.** Your render reads ARMY NAVY & AIR FORCE
VETERANS with no comma; the medal has ARMY, NAVY & AIR FORCE VETERANS. Text in
generated renders garbles often enough that I would rather not take punctuation
from one, and the comma came from the descriptions file. Say the word and it
goes.

---

## Fidelity, final

**Traced** from supplied artwork, all of it: the RCAC army and air emblems, the
Legion badge, St Edward's Crown, the eagle, the Strathcona portrait, the St
George figure, the Bravery busts, and the ANAVETS centre.

**Stylised**: nothing on a medal face. What remains drawn is furniture - the
fouled anchor on the two navy medals, the laurel sprigs on the AFA, the
suspension bars, claws, scrolls and rings. Send a render for any of those and
the same pipeline applies.

---

# Bravery busts - traced

Three faces down. Your render replaces the drawn busts, which you had ruled
out of scope for hand-detailing back in round 4 - tracing sidesteps that
entirely.

This one has no silhouette to extract, and the numbers say so rather than my
eye: the busts are line work and solid dark hair over fills that are the
**same silver as the field behind them**. Labelling the free space inside the
face puts the three face interiors at mean luminance 194, 193 and 196, and the
surrounding field at 194. Flooding the background and keeping the rest just
returns the whole disc. So this traces the line work only, which is what the
render actually is.

Two cuts, and both needed care:

1. **The legend is flat, not an arc.** FOR BRAVERY / POUR BRAVOURE sits in two
   straight lines across the top of the face, so it is cut by y. The band
   between it and the busts is *not* empty - the rim arc and JPEG ringing
   leave about 12 px on every row - so "quiet" has to be a low count rather
   than zero. And the band above the legend is quiet too, so it is the LAST
   quiet row above the centre, not the longest run.
2. **The rim circle.** A radius histogram puts it at 0.84 to 0.86 of the disc
   radius, while the shoulders fade out by 0.80, so cutting at 0.828 drops the
   rim and leaves the busts whole.

**The tracer now emits its own placement.** It reports the width as a fraction
of the disc diameter (0.8017) and the box centre in disc-radius units
(+0.2991), which become `device_scale` 1.743 and a new `device_offset` on the
spec. The busts land where they sit on your render rather than where they look
about right. `device_offset` replaces the hard-coded 0.22 nudge that any
`legend_lines_top` medal used to get.

Struck near-black (`#1F2427`) rather than the medal's dark-metal tone, matching
the render and your standing rule about legibility on the faces.

Clearance to the legend measured at **1.46 mm**. The clearance script now
suppresses `legend_lines_top` as well, so Bravery is measured rather than
skipped - it was the one medal the test could not see.

---

## Fidelity, after four traces

**Traced** from supplied artwork: the RCAC army and air emblems, the Legion
badge, St Edward's Crown, the eagle, the Strathcona portrait, the St George
figure, and the Bravery busts.

**Stylised** - the last one standing: the ANAVETS shield, plus the fouled
anchor and the laurel and maple sprays, which are small enough that it hardly
matters.

---

# St George figure - traced

The drawn figure is gone. The rotate-about-the-hip rearing pose, the
counter-rotated rider and the hand-built dragon were all scaffolding for not
having a reference; the render you sent on 2026-09-24 replaces the lot.

This one was far easier than the Strathcona portrait: bright silver on a dark
mirror field keys straight off luminance. The work was in two cuts.

1. **The legend is the same metal as the figure.** PRO MERITO and ORDER OF ST.
   GEORGE are struck in the same bright silver, so a plain luminance key picks
   them up with the horse. They sit at about 0.80 of the field radius and the
   figure inside 0.72, so a cut at 0.76R separates them with room to spare.
   The disc is fitted from the dark field itself - largest mid-luminance
   component, holes filled - because the render is cropped and the rim is not
   fully in frame.
2. **Keep everything, not just the largest component.** At a threshold that
   holds the figure's shaded areas it is all one piece, but the raised sword,
   the cape tip and the dragon's wing sit close to breaking off. Anything at
   or above 120 px inside the radius cut is kept, so a tighter threshold
   cannot silently drop them.

The ink is a high-pass inside the figure, dilated 3 px, and it carries the
engraving: the bridle and reins, the armour plates, the mane, the sword driven
down into the dragon, and the dragon's scales and wing membrane. Drawn as a
bright silhouette with the engraving over it, which is how relief reads on a
mirror-polished field.

Scaled to `device_scale` 1.26. Clearance measured at **0.86 mm**, in line with
the ACMM (0.91 mm) and Strathcona (0.93 mm). Clean-room rebuild verified:
manifest identical, all 58 PNGs byte-identical, pack byte-identical.

The extraction is `trace_stgeorge.py`.

**Two of the three stylised holdouts are now closed.** Only the ANAVETS shield
is left, plus the Bravery busts, which are out of scope.

---

# Strathcona portrait - traced

The bust is no longer stylised. It is traced from the bronze render you sent
on 2026-09-24, which changes its fidelity flag from STYLISED to TRACED.

That render cannot be keyed the way the eagle was: the portrait is the same
colour as the field, so there is no silhouette to segment. What separates it
is **relief** - the struck areas carry local highlights and shadows and the
field does not. So the field is estimated with a wide Gaussian and subtracted,
and the high-pass falls out as a shadow mask and a highlight mask.

Three things were worth writing down:

1. **Sigma matters.** At sigma 26 the portrait's own large light areas bias
   the background estimate and the face partly cancels itself out. Sigma 70
   estimates the disc's radial gradient and nothing else.
2. **AGMINA DUCENS touches the hair.** The legend cannot be split off by
   connected components - the left-hand letters are joined to the head through
   the hair. It is cut by radius instead, but only *above* the centre: the
   shoulders run out to 0.75R and a global cut beheads the bust.
3. **The render is lit from the left**, so the field beside the profile reads
   as highlight and traces as a slab down the left of the face. It is the
   largest single component of the highlight mask, and dropping it by size
   and position removes it cleanly.

No silhouette pass. One was built and thrown away: closing the highlight
fragments into a single bust leaves a lumpy outline that shows as a ragged
edge down the profile. The highlight and shadow passes alone carry the
portrait.

Scaled to `device_scale` 1.24, the portrait fills the field. Clearance to
AGMINA DUCENS measured at **0.93 mm**, in line with the ACMM (0.91 mm) and the
Air Cadet Service Medal (0.94 mm). Re-verified: manifest identical, all 58
PNGs byte-identical, pack byte-identical from a clean-room rebuild.

The extraction is `trace_strathcona.py`, alongside `trace_bird.py`.

---

# Round 5 - what changed

Everything in `medal-art-corrections.md` (round 5) is applied. 58 keys,
unchanged. Rebuild:

```
python3 make_medals.py --dpi 300 --out out
python3 make_pack.py --src out --out medal_art_pack.js
```

Clean-room check passed again: sources copied to an empty directory, both
steps re-run, manifest identical, all 58 PNGs byte-identical,
`medal_art_pack.js` byte-identical.

---

## The regressions

You were right that round 4's "extend the ribbon behind the bar" leaked onto
medals that should not have it. It was one branch covering four suspension
types at once:

```python
if susp in ("claw_bar", "trapezoid", "bar", "scroll"):
    rib_bot = SUSP_TOP + (SUSP_BOT - SUSP_TOP) * 0.75
```

Now each type stops where its own metal starts. Only `claw_bar` (St. George
and AFA) runs the ribbon on behind the plate, and even there it stops inside
the plate rather than below it:

| suspension | ribbon ends |
|---|---|
| `claw_bar` (St. George, AFA) | inside the bar plate, 60% down |
| `trapezoid` (Army Cadet Medal of Merit) | 0.6 mm in, inside the claw's top gold strip |
| `scroll` (Bravery) | inside the CADET bar |
| `bar` (ANAVETS) | inside the MERITUM bar |

## The ANAVETS rings, and why they vanished

Round 4 made the MERITUM bar taller (you asked for "a little taller than the
CADET bar"), which took it to 5.52 mm. The suspension gap was a fixed 6 mm
constant, so the bar ate all but 0.48 mm of it and the two jump rings had
nowhere to go. They were still being drawn, just squeezed to nothing.

The fix is structural rather than a nudged number. The gap is now a per-medal
value instead of a constant:

```python
gap_h = spec.get("susp_gap", SUSP_BOT - SUSP_TOP)
s_top = SUSP_BOT - gap_h
```

`susp_gap` shortens the ribbon and buys room between it and the rim, with the
total medal height untouched at 100 mm. Set on four medals:

| medal | gap | why |
|---|---|---|
| ANAVETS | 10.5 mm | lug, two jump rings, eye |
| St. George | 10.5 mm | bar, stem, claw |
| AFA | 10.5 mm | bar, stem, claw |
| Bravery | 8.6 mm | a taller scroll |

Bravery's CADET bar is pinned to 3.12 mm rather than a fraction of the gap, so
widening the gap gives the scroll room without inflating the bar.

## St. George and AFA: the missing stem

Both bars sat straight on the claw. There is now a short thick stem between
them: `rw / 7` wide, about one bar height tall, running from the centre
underside of the bar into the shoulder-claw, which stays at 40% of the medal's
width. The medal hangs about a bar height lower as a result.

The maple leaf on the St. George bar was flat white (`METALS["silver"][1]`,
a fixed near-white). It now takes the bar's own gradient, so it shades with
the metal instead of sitting on top of it as a sticker.

## St. George: the horse now rears

The horse was anatomically fine but standing. Rather than redraw it, the front
assembly is rotated:

- The body, head, raised forelegs and rider spin **32 degrees about the hip**
  at `(0.72, 0.58)`, scaled to 0.80 so the raised head stays on the disc.
- The hind legs and tail are laid out in world space **after** the rotation,
  so they stay planted vertically under the weight instead of tipping with
  the body.
- The rider gets a second, opposite rotation of **-17 degrees about his own
  seat**, so he does not tip backwards with the horse, plus a small offset
  back along the spine. Without that he ended up sitting on the neck.
- The lance is drawn in world space too, from his hand down to the dragon,
  so it keeps its own angle rather than inheriting the tilt.

The cape now reads, streaming out to the right behind him.

The dragon was still a coil with bits floating near it, so it was rebuilt as
one creature: skull and neck, body, open jaws where the lance lands, a bat
wing off the shoulder, two forelegs, spine spikes and a barbed tail.

## AFA: leaf and eagle in relief

The leaf was a hollow dark outline and the wingtips stopped inside the leaf's
side points. Both are now struck in relief with no outlines anywhere - three
passes per piece:

1. a dropped shadow, offset `0.022 * size` down and right,
2. a highlight, offset back up and left,
3. the solid body on top.

The leaf is a solid gold plate with its top point under the crown and its
lower lobes below the bird, plus a short stem pointing down into
`ASSOCIATION` (the traced leaf ends at the lobes, so the stem is its own small
plate on the same transform). The eagle is at `0.92 * size` against the leaf's
`0.64`, so the wingtips clear the leaf's side points by a wide margin and
still stay clear of the laurel sprigs. Its feather line work is kept, in a mid
gold at 62% rather than the dark tone, so it reads as shading and not as an
outline.

## Bravery: the scroll

Volutes up from r 1.35 to 1.65, with a three-arc spiral instead of two so the
coil is tighter. The finial is now a tall acanthus: a point merging into the
underside of the CADET bar, a swelling belly, a waist, then a flare into the
claw on the rim, with two side lobes and a centre vein.

---

## Verification

Device clearance, measured the same way (render each medal three times, diff
the ink masks, measure closest approach):

| | closest gap | | | closest gap |
|---|---|---|---|---|
| `strathcona` | 5.62 mm | | `anavets` | 3.92 mm |
| `legion` | 0.50 mm | | `stgeorge` | 2.41 mm |
| `navyleague` | 3.97 mm | | `seaservice` | 2.17 mm |
| `acmm` | 0.91 mm | | `armyservice` | 1.64 mm |
| `afa` | 2.74 mm | | `airservice` | 0.94 mm |

Nothing touches. AFA came down from 3.51 mm and St. George from 2.68 mm, both
because their centres grew; both still have millimetres in hand. All 27 medals
remain exactly 35 x 100 mm.

## Still stylised

Unchanged from round 4: the fouled anchor, St George and the dragon, the
ANAVETS shield, the laurel and maple sprays, the cadet busts and the
Strathcona portrait are all drawn from written descriptions. Traced from
supplied artwork: the RCAC army and air emblems, the Legion badge, St
Edward's Crown, and the eagle.

---
---

# Round 4 - what changed

Worked through `medal-art-corrections.md` (round 4) against the V2
`cadet-medal-descriptions.md`. Where the two disagreed, the descriptions file
won, as instructed. Out of scope and untouched: the Cadet Award for Bravery
busts and the Lord Strathcona portrait.

58 keys, same as before. Rebuild:

```
python3 make_medals.py --dpi 300 --out out
python3 make_pack.py --src out --out medal_art_pack.js
```

Clean-room check: copied `make_medals.py`, `medal_specs.py`, `make_pack.py`,
`fonts/` and `src/` into an empty directory, ran both steps, and compared.
Manifest entries identical, all 58 PNGs byte-identical, `medal_art_pack.js`
byte-identical. Nothing in the build depends on leftover state.

`make_pack.py` is new. The pack used to be assembled by hand, which is why
there was no way to reproduce it.

---

## The traced eagle (your 16:16 artwork)

The heraldic bird you sent replaced two separate stand-ins, and it is by far
the biggest visible change in this round.

Segmented off the baked-in checkerboard rather than an alpha channel: the file
is RGB, so background is anything near-greyscale, and the bird is
`saturation > 40 OR luminance < 140` - the second clause keeps the black
outlines, which are as unsaturated as the checker but much darker. Largest
component, holes filled. That lands the silhouette cleanly at 1021 x 423 px,
aspect 0.4143.

Traced twice, the same two-path treatment as the RCAC, Legion and Crown
emblems: silhouette as a soft fill, ink line work over it. The ink is dilated
3 px before tracing, because the feather lines are 1 to 3 px in the source and
would otherwise vanish under the roughly 4x downscale to medal size.

Worth writing down: `potrace.Bitmap` treats **low** values as foreground, so
both masks have to be inverted going in. Tracing them the obvious way returns
the complement, which renders as a solid field with the artwork knocked out of
it - it looks like a fill-rule problem and is not one.

Used in two places:

- **Air Cadet Service Medal service bars.** Silhouette only. The device is
  about 2 mm tall there, so the line work would just muddy it. `bird_svg` now
  takes `ink=True` for the cases with room.
- **Air Force Association face.** Silhouette plus full line work, over the
  upright maple leaf.

`BIRD_ASPECT` moved from 0.31 to 0.4143, so the bar device is now correctly
shorter and wider. The old drawn bird is still in `src/bird_path.txt` as
`BIRD_DRAWN`, unused.

---

## Applied this round

### Global fixes

**A. Canvas width no longer blocks overhanging bars.** `RIBBON_FRAC = 0.80` -
the ribbon is 80% of the canvas, centred, and the canvas stays 35 mm. First
attempt used 0.85, which put the St. George claw-bar returns at
`rw * 9/7 = 38.25 mm` on a 35 mm canvas, off the edge. The returns are now
also capped at the available margin:
`ret = min(bh, (width_mm - rw)/2 - 0.25)`.

**B. Loop rings are drawn under the ribbon.** Draw order is now mount, then
ring, then ribbon, so the ribbon's flat bottom hides the ring's top arc. First
visible part of the ring is where it emerges below the fold.

**C. Mounts differentiated.** Rounded lug on Air and Army Service, ball knob
on Sea Service, Navy League and Strathcona, rectangular tab on RCL. The ring
passes through the mount in every case.

**D. Nothing floats.** Gaps closed on St. George, AFA, ANAVETS and Bravery.

### Order of St. George

- **Centre figure redrawn.** The old one read as a dog. It is now built as an
  anatomical silhouette: head and arched neck high on the left, barrel and
  haunch right, hind legs planted, forelegs raised and bent, tail as a filled
  plume rather than a stroke (which had been reading as a third hind leg).
  Rider enlarged and moved up so his torso clears the horse's back, with a
  sunburst halo, crested helm, cape streaming right, and the lance running
  from his hand down to the lower left.
- **Dragon redrawn.** Coiled body with spine spikes, a bat wing, an open jaw
  where the lance lands, and a barbed tail. The previous version read as a
  horseshoe.
- Mirror finish kept: dark reflective field, bright metal (`#F2F5F6`) rim,
  lettering and figure.
- Claw bar: flat plate, squared returns outside the ribbon edges, straddling
  maple leaf, thick stem flaring into a broad shoulder-claw.

### Air Force Association

- Centre is the traced eagle across an upright maple leaf, both in gold relief.
  Sized so the wings pass outside the leaf but stay clear of the laurel
  sprigs, and positioned so the leaf's top point shows below the crown and its
  lower lobes show below the bird.
- Crown is the traced St Edward's Crown, enlarged.
- Laurels float free at 10 and 2, touching nothing.
- `ASSOCIATION` large, arcing roughly 7 to 5 o'clock
  (`legend_bottom_size` 3.5, `legend_bottom_sweep` 150).
- Same claw-bar template as St. George, in gold.

### ANAVETS

- Asymmetric shield per the descriptions file, not a symmetrical Union Jack.
- Maple-leaf sprays beside the shield, not laurel.
- Trapezoid bars: CADET wider at the top, MERITUM wider at the bottom and
  taller, overhanging both the ribbon and the CADET bar.
- Antiqued finish on both bars - recessed darker field at 0.38 opacity inside a
  raised border, with bright raised lettering and solid bright leaves.
- Pierced lug under MERITUM, eye on the rim, two jump rings, and the rigid lug
  suppressed so the medal actually dangles.
- Serif lettering, four-dot ornaments either side of IN CANADA, raised silver
  crown, navy border blocks.

### Sea Cadet Service

- **Side bands to royal blue `#2350A8`.** This reverses the round-3 change to
  navy; you were right that every photo shows royal blue.
- Fouled anchor: thinner curved crown with spade flukes, capped stock, rope
  threaded through the ring and wound round the shank in an S. Scaled up 25%
  (`anchor_scale` 1.25).
- Ball knob, serif FOR SERVICE / POUR SERVICE.

### Navy League of Excellence

Back in scope this round after you said to skip it in round 3. Now has the
same fouled anchor, slimmed (`anchor_slim`), serif lettering, navy centre
pinstripe `#1B2350`, ball knob and ring layering.

### Cadet Award for Bravery

- Ghost ring deleted. Solid scroll suspender: volutes at each end coiling down
  and inward, arms sweeping to the centre, flame finial widening into a claw
  on the rim. One rigid piece, merged into the bar above and the rim below.
- Both bars overhang the ribbon, fishtail ends sharpened.

### Army Cadet Medal of Merit

Name bars overhang the ribbon on both edges, square ends.

### Others

- RCL: CADET and EXCELLENCE pulled inboard so they read as arcs.
- Army and Air Service: rounded lug mounts, ring under ribbon.

---

## Two things I decided rather than asked

**AFA ribbon colours.** The corrections file said the reference photo showed
navy, light blue and maroon. `AIR_ARTWORK_FOLLOWUP_2.md` §3 had you saying the
AFA ribbon uses the ANAVETS palette and the poster print had shifted. The V2
descriptions file sides with the corrections, and you said the descriptions
file wins, so the ribbon is now navy `#1B2350` / aqua `#7EC3C8` / maroon
`#6B1D2E`. Flagging it because it does reverse your earlier call - say the word
and it goes back.

**Bravery stays light.** The corrections offered the dark-mirror treatment to
match St. George, and allowed keeping it light for readability. Kept light. At
ribbon-rack size a dark Bravery loses the busts entirely, and it is the medal
most likely to be shown small.

---

## Verification

**Device clearance.** Each medal rendered three times - full, device
suppressed, device and legends suppressed - then the ink masks differenced so
the device pixels and legend pixels are isolated exactly, and the closest
approach measured.

| | closest gap | | | closest gap |
|---|---|---|---|---|
| `strathcona` | 5.62 mm | | `anavets` | 3.92 mm |
| `legion` | 0.50 mm | | `stgeorge` | 2.68 mm |
| `navyleague` | 3.97 mm | | `seaservice` | 2.17 mm |
| `acmm` | 0.91 mm | | `armyservice` | 1.64 mm |
| `afa` | 3.51 mm | | `airservice` | 0.94 mm |

Nothing touches. The clamp is geometric, not a tuned number: legends are laid
out first, the innermost legend ink sets `legend_min_r`, and any emblem device
is bounded in both width and height to fit inside that minus `DEVICE_CLEAR`
(0.9 mm). Bravery is not in the table - it uses `legend_lines_top` rather than
arc legends, so the diff has nothing to measure against; its busts are
unchanged from the round-3 measurement of 6.27 mm.

The test script is `clearance.py` in the notes. Two earlier versions of it were
wrong and both are worth remembering: a radius-only check is too strict once
the AFA eagle goes in, because the bird spans wide at mid-height where there is
no lettering; and suppressing the legends also relaxes the device clamp, so the
device must be isolated against the **full** render, never the legend-free one.

**Canvas.** All 27 medals are now exactly 35 x 100 mm, aspect 0.35. They used
to be 100.1 mm because the disc rim stroke overhung the bottom edge; the round-4
mount and ring rework pulled it back inside. 1200 dpi renders are 1654 x 4724 px
either way.

---

## Fidelity

**Traced** from supplied artwork: `army_emblem` (RCAC), `legion_emblem`,
`air_emblem` (RCAC Air), `st_edwards_crown`, and now the AFA / Air Service
eagle.

**Stylised** - built from written descriptions, no reference image: the fouled
anchor, St George and the dragon, the ANAVETS shield, the laurel and maple
sprays, the three cadet busts and the Strathcona bust.

Send artwork for St George, the ANAVETS shield or the Strathcona portrait the
way you sent the eagle and each one moves into the traced column in about ten
minutes.
