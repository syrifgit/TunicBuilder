# medal_specs.py — what changed

`make_medals.py` is **unchanged**, byte for byte, from the copy you already
have (md5 `9cb4d05ccd2c97ee568165fe848e8747`, 23,955 bytes). Both files are in
this folder anyway so you can drop them in together, but the only file that
actually moved is `medal_specs.py` (md5 `26a64bc06cc812c57df7e261d64d90c0`).

Three edits, all in `medal_specs.py`. Nothing else in the pack differs.

## 1. `afa` added to `MEDALS`, at precedence 6

Slots in between `acmm` (5) and `anavets` (7), so the dict order matches the
CATO 13-16 precedence the rest of the file follows.

```python
"stripes": [("#101A3D", 9), ("#70B3BD", 8), ("#101A3D", 9),
            ("#491219", 41), ("#101A3D", 9), ("#70B3BD", 8),
            ("#101A3D", 9)],
"suspension": "bar", "suspension_text": None,
"metal": "gold", "legend_bottom": "ASSOCIATION", "device": "leaf",
"ribbon_width_mm": 35,      # not published; assumed
"fidelity": "MEASURED colour / ESTIMATED geometry",
```

Stripe proportions and hexes were scanlined off the full-colour medal image on
A-CR-CCP-850/DA-003 at 9x. The 35 mm width is **assumed** — no text source
describes this ribbon, which is why it was unsourced before.

## 2. `airservice` disc metal, `"gold"` → `"bronze"`

```python
"metal": "bronze",          # see source note: poster overrides Blatherwick
```

The reasoning is appended to that entry's `source` string, so it travels with
the data rather than living only in NOTES: sampled mean `#9E7B60`, hue 26°
against gold's ~44°; poster adopted over Blatherwick because it is the issuing
authority's own current colour artwork; revert by setting `metal` back to
`"gold"`. The same entry also records that the poster **confirms** the
Blatherwick ribbon description, which did not change.

## 3. `UNSOURCED` emptied

```python
# Everything in the CATO 13-16 precedence is now built. "afa" was previously
# listed here as unsourced; A-CR-CCP-850/DA-003 supplied a full-colour image.
UNSOURCED = {}
```

The manifest still emits `_unsourced`, now an empty object. If anything in
your build asserts on it being non-empty, that is the line to look at.

## Regenerating

```
python3 make_medals.py --dpi 300 --out out
```

52 keys. Previously 50: `medal_afa` and `ribbon_afa` are the two new ones.
Every other key is byte-identical except `medal_airservice`, which is now
bronze.
