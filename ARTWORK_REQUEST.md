# What the tunic tool needs from this pack

Written by the session that maintains `demo/tunic.template.html`. The artwork here is
good and the format already matches; this is about **coverage and key names**, so the
pack drops in without anything being regenerated or renamed on the other side.

Nothing below asks for a change to how a medal or ribbon is drawn.

---

## 1. Format — already correct, do not change

```js
const MEDAL_ART = {"<key>": {"d": "<base64 PNG>", "aspect": <w/h>}, ...};
```

RGBA, transparent ground, 300 dpi (35 mm ribbon = 413 px wide). `aspect` must be the
true `w/h` of the image — it is what the tool scales by, so a wrong value skews the
badge. Keep `medal_art_manifest.json` alongside it, with `fidelity` and `source` per
key; those become the citations in the rules pack.

## 2. Sizes are load-bearing

| | Size | Tool constant |
|---|---|---|
| Ribbon | 35 × 10 mm | `RIBBON_W` 3.5 cm × `RIBBON_H` 1.0 cm |
| Medal | 35 × 100 mm | `MEDAL_W` 3.5 cm × `MEDAL_LEN` 10.0 cm |

The medal image must span **exactly** suspender top to medal bottom edge = 100 mm,
which is the `medal_*` output. **Do not send `court_*`** — its 102.2 mm includes the
pin bar, and the tool positions from the suspender line, so those 2.2 mm push every
medal down by that much.

Render the Bravery ribbon at **35 mm, not its true 38 mm**. The tool lays ribbons in
rows of three with no interval, so a single odd width breaks row alignment. That is a
deliberate local decision; please keep noting the true 38 mm in the manifest.

## 3. Do not send these

- `group_*` and `rack_*` — the tool composes its own rows and racks from single
  ribbons. This also means the "which side is senior" question in `NOTES.md` does not
  affect us; we do not use your composites.
- `court_*` — see above.
- Any ACMM state that cannot be worn — see §5.

## 4. Key names

Use these exactly. They are the tool's own medal keys, so no mapping layer is needed.

| Precedence | Key | Medal |
|---|---|---|
| 1 | `bravery` | Cadet Award for Bravery |
| 2 | `strathcona` | Lord Strathcona Medal |
| 3 | `legion` | Royal Canadian Legion Cadet Medal of Excellence |
| 4 | `navyleague` | Navy League of Canada Medal of Excellence |
| 5 | `acmm` | Army Cadet Medal of Merit (your `howard_acmm`) |
| 6 | `afa` | Air Force Association Medal |
| 7 | `anavets` | ANAVETS Cadet Medal of Merit |
| 8 | `stgeorge` | Order of St. George Medal |
| 9 | `seaservice` | Sea Cadet Service Medal |
| 10 | `armyservice` | Army Cadet Service Medal (your `acsm`) |
| 11 | `airservice` | Air Cadet Service Medal |

Every entry is `medal_<key>` and `ribbon_<key>`, plus a suffix where a medal has
variants. So: `medal_strathcona`, `ribbon_strathcona`, `medal_acmm_rhpw`, and so on.

## 5. Army Cadet Medal of Merit — 11 states, 7 of them missing

Four award bars, junior to senior: **R**odger, **H**oward, **P**resident, **W**alsh.
Two rules, both confirmed by Lt Beal:

- the medal is never worn bare — **at least one bar of any kind**
- **Walsh requires President**

That gives exactly 11 wearable states. Key them by bar initials in junior-to-senior
order, lowercase:

```
medal_acmm_r      medal_acmm_rh     medal_acmm_rhp    medal_acmm_rhpw
medal_acmm_h      medal_acmm_rp     medal_acmm_rpw
medal_acmm_p      medal_acmm_hp     medal_acmm_hpw
                  medal_acmm_pw
```

and the matching `ribbon_acmm_*`, one leaf per bar in the bar's own colour.

**Already covered** by existing output, just needing renaming: `_r`, `_h`, `_p`, and
`_rhpw` (which is the current bare `medal_howard_acmm`, since it defaults to all four
bars). **Seven are missing:** `rh rp hp pw rhp rpw hpw`.

**Please drop** `medal_/ribbon_howard_acmm_walsh` — Walsh without President is not
wearable — and the bare `ribbon_howard_acmm`, which has no leaves and so represents a
medal with no bars.

## 6. Service medals

`armyservice` is complete and correct: 4 / 5 / 6 / 7 years, bars accumulating, matching
ACLC Policy 13.1 para 12. Keep that scheme, just renamed:

```
medal_armyservice        4 yr, no bar     ribbon_armyservice
medal_armyservice_5yr    1 bar            ribbon_armyservice_5yr
medal_armyservice_6yr    2 bars           ribbon_armyservice_6yr
medal_armyservice_7yr    3 bars           ribbon_armyservice_7yr
```

**Question:** do the Sea and Air Cadet Service Medals carry the same year bars? If so
we would want the same four variants each. If you cannot source it, send the base only
and say so.

## 7. Four medals not yet built

`navyleague`, `afa`, `seaservice`, `airservice`. All four are transfer-in cases — a
cadet who served in another element keeps the award — so they are rare but reachable,
and the tool currently offers all eleven. Base state only unless §6 says otherwise.

If any of the four cannot be sourced to a usable standard, say which and we will hide
them in the tool rather than draw a placeholder.

## 8. Commendation and award pins

Currently drawn as plain coloured bars. Real insignia would be welcome, at these sizes
from Chapter 5 Annex D:

| Key | Pin | Size |
|---|---|---|
| `pin_cds` | Chief of the Defence Staff Commendation | 2.0 × 0.5 cm |
| `pin_command` | Command Commendation | 2.0 × 0.5 cm |
| `pin_cadet` | Cadet Commendation | 2.0 × 0.5 cm |
| `pin_navy` | Navy League Award of Commendation | 2.0 × 0.75 cm |
| `pin_dofe` | Duke of Edinburgh's Award | oval, **both dimensions unknown** |

The existing `pin_commendation` is drawn at ribbon size (3.5 aspect) and does not fit
any of these. If Annex D gives no dimensions for the DofE oval, say so and we will keep
it a flagged placeholder.

## 9. One thing that is not artwork

`NOTES.md` cites **CATO 13-16 para 19** and its annexes directly, so you have the
document. We do not, and it is the cadet-programme authority for precedence.

Please paste the para 19 list verbatim. Two things hang on it:

- our order comes from CJCR Gp O 10050 para 7.4, a **JCR** order. Your notes list ten
  medals in what looks like exactly 10050's eleven minus the Order of St. George, in
  the same order — if that is right, it confirms our precedence against the cadet
  authority and we can stop qualifying it.
- **Order of St. George is not in the CATO list at all.** We place it 8th on 10050's
  word alone. If CATO says nothing, that stays an open question and we need to say so
  on the page.

Anything else in CATO 13-16 giving the Cadet Service Medal bar scheme, or a maximum
number of bars, would also close a question we currently carry as unsourced.

---

## Summary of the ask

| | Count |
|---|---|
| ACMM states to generate | 7 (14 images) |
| Medals not yet built | 4 (8 images, more if they take year bars) |
| Commendation / award pins | 5, at the sizes in §8 |
| Keys to rename | all, to §4 |
| Outputs to drop | `group_*`, `rack_*`, `court_*`, 3 unwearable ACMM keys |

One `medal_art_pack.js` and one `medal_art_manifest.json`, same format as now.
