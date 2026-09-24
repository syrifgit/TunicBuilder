# Cadet honours artwork

Ribbon and medal art for the eleven cadet honours, plus the four commendation
and award pins. 58 keys. Everything is generated from SVG in millimetres and
rasterised, so it is resolution-independent.

## Rebuild

```
python3 make_medals.py --dpi 300 --out out     # 58 SVGs + 58 PNGs + manifest
python3 make_pack.py --src out --out medal_art_pack.js
```

Any resolution is one flag away. `--dpi 1200` gives 1654 x 4724 px medals.

Needs `cairosvg`, `pillow`, `numpy`, `scipy`. The trace scripts also need
`potracer` and, for the ANAVETS one, `scikit-image`. Fonts are bundled in
`fonts/` and found relative to the script, so there are no absolute paths to
fix.

Verified reproducible: copy `make_medals.py`, `medal_specs.py`,
`make_pack.py`, `fonts/` and `src/` into an empty directory, run both steps,
and the manifest, all 58 PNGs and the pack come out byte-identical.

## What each file is

| | |
|---|---|
| `make_medals.py` | The generator. Layout constants, devices, suspensions, legends. |
| `medal_specs.py` | One dict per medal: ribbon stripes, metal, legends, device, bars, authority, fidelity and source. Also `PINS`, `METALS` and `acmm_states()`. |
| `make_pack.py` | Bundles the rendered PNGs into `medal_art_pack.js` for the tunic tool. |
| `clearance.py` | Verification. Renders each medal three times, diffs the ink masks to isolate device and legend pixels exactly, and reports the closest approach. |
| `medal_art_pack.js` | `const MEDAL_ART = {key: {d: base64 PNG, aspect}}`. |
| `medal_art_manifest.json` | Per key: size, aspect, file paths, authority, fidelity and source. |
| `png/`, `svg/` | The 300 dpi renders and their SVG sources. |
| `src/` | Traced path data, one file per emblem. |
| `fonts/` | TeX Gyre Heros (sans) and Termes (serif), bold. |
| `CHANGES.md` | What changed each round, and why. |
| `NOTES.md` | The reply to the original artwork request, including CATO 13-16 para 19 verbatim. |

## The trace scripts

Each takes a reference image and writes path data into `src/`. They are kept
because the extraction is not obvious in any of these cases, and the
docstrings explain what failed before what worked.

```
python3 trace_bird.py eagle.png             # AFA face and Air Service bars
python3 trace_strathcona.py portrait.png    # Lord Strathcona
python3 trace_stgeorge.py figure.png        # St George and the dragon
python3 trace_bravery.py busts.png          # the three cadets
python3 trace_anavets.py centre.png         # crown, shield and sprays
```

One shared gotcha: `potrace.Bitmap` treats LOW values as foreground, so every
mask is inverted going in. Traced the obvious way it returns the complement,
which renders as a solid field with the artwork knocked out of it — it looks
exactly like a fill-rule bug and is not one.

`trace_bravery.py` and `trace_anavets.py` also print their own placement — the
width as a fraction of the disc diameter and the box centre in disc-radius
units — which become `device_scale` and `device_offset` in `medal_specs.py`.
That keeps the geometry tied to the source instead of eyeballed.

## Sizes and authority

Ribbons are 35 x 10 mm. Several are issued on 32 or 38 mm ribbon and are
rendered at 35 so ribbon rows stay aligned; the manifest records the true
width under `true_ribbon_width_mm` and flags the decision.

**Medals render 46 x 100 mm, carrying a 35 mm ribbon centred on the canvas.**
The 100 mm is suspender top to the bottom edge of the medal, per CJCR Dress
Instructions ch 5 para 7.

The canvas is wider than the ribbon on purpose. Medals mount at a 35 mm pitch
with no interval (ch 5 para 5.c), and on a worn group the suspension bars,
claws and their squared returns overhang the ribbon and sit over the
neighbouring medal. The extra width is sized off the widest of those:

```python
CLAW_BAR_H = RIBBON_W / 7.0                       # 5.0
CANVAS_W   = RIBBON_W + 2.0 * (CLAW_BAR_H + 0.5)  # 46.0
```

So **mount each medal centred on its own 35 mm slot, senior on top**, and the
overhang lands where it does on the uniform. Do not tile at 46 mm.
`previews/PREVIEW_mounted_pitch.png` shows four medals done that way.

`w_mm` in the manifest is the canvas; `ribbon_w_mm` is 35 on every medal key,
so the tool does not have to infer it. Ribbon-only keys are untouched.

Precedence follows CATO 13-16 para 19, quoted in full in `NOTES.md`. The Order
of St. George is not in it — that placement rests on CJCR Gp O 10050 alone and
the manifest says so.

Service bars follow ACLC National Policy 13.1 para 12, capped at three. A
cadet enrolling on their 12th birthday and leaving the day before their 19th
could earn a third (Blatherwick ch 40), so three is the ceiling by arithmetic.

## Fidelity

Every medal face is now **traced** from supplied artwork: the RCAC army and
air emblems, the Legion badge, St Edward's Crown, the eagle, the Strathcona
portrait, the St George figure, the Bravery busts and the ANAVETS centre.

What is still drawn is furniture — the fouled anchor on the two navy medals,
the AFA laurel sprigs, and the suspension bars, claws, scrolls and rings. Send
a reference for any of those and the same pipeline applies.

Per-key provenance is in `medal_art_manifest.json` under `fidelity` and
`source`.
