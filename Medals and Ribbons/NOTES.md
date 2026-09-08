# Cadet honours artwork - reply to ARTWORK_REQUEST.md

50 keys. Format, sizes and key names are as specified. `group_*`, `rack_*`,
`court_*`, the three unwearable ACMM states and the old ribbon-sized
`pin_commendation` are all gone.

```
python3 make_medals.py --dpi 300 --out out
```

Verified on output: `ribbon_armyservice` 413 x 118 px, aspect 3.5;
`medal_armyservice` 413 x 1181 px, aspect 0.3497 (35 / 100.1, the 0.1 mm being
the medal rim stroke). All PNGs RGBA on transparent ground.

---

## §9 first - CATO 13-16 para 19, verbatim

> 19. The order of precedence of medals/ribbons is:
>
> 1. Cadet Award for Bravery;
> 2. Lord Strathcona Medal;
> 3. Royal Canadian Legion Cadet Medal of Excellence;
> 4. Navy League of Canada Medal of Excellence;
> 5. The Major-General W.A. Howard Award;
> 6. Air Force Association Medal;
> 7. Army, Navy and Air Force Veterans in Canada Cadet Medal of Merit;
> 8. Sea Cadet Service Medal;
> 9. Army Cadet Service Medal; and
> 10. Air Cadet Service Medal.

Source: CATO 13-16, *National Cadet Honours and Awards*, canada.ca, page
modified 2022-03-14.

**Your reading is correct.** That is your eleven minus the Order of St. George,
in the same order. Your list is confirmed against the cadet authority and you
can stop qualifying it — for the ten medals that appear in it.

**St. George is genuinely absent.** Not in para 19, not in the annex list
(Annexes A to G, with Annex D cancelled), not anywhere in the order. It is also
absent from Blatherwick's chapter on cadet medals. Placing it 8th rests on
CJCR Gp O 10050 alone, which is a JCR order. That stays an open question and
the page should say so.

Two other things para 11 settles: it lists the Army Cadet Service Medal as
"the Army Cadet League of Canada Policy No 13.1", so CATO delegates the bar
scheme rather than setting one, and the Major-General W.A. Howard Award at
para 19.e is the slot the ACMM now occupies.

**Maximum number of bars — now sourced.** Not from CATO, but Blatherwick ch40
states that a cadet enrolling on their 12th birthday and leaving the day before
their 19th could receive a **third bar**. That is the ceiling by arithmetic, so
the 3-bar cap is no longer an unsourced local decision. Policy 13.1 para 12
itself still sets no explicit limit.

---

## §5 ACMM - all 11 states

Generated from the two rules rather than hand-listed, so the set cannot drift:
15 non-empty subsets of RHPW, less the 4 carrying Walsh without President.
See `acmm_states()` in `medal_specs.py`.

```
medal_acmm_r   medal_acmm_rh   medal_acmm_rhp   medal_acmm_rhpw
medal_acmm_h   medal_acmm_rp   medal_acmm_rpw
medal_acmm_p   medal_acmm_hp   medal_acmm_hpw
               medal_acmm_pw
```

Plus `ribbon_acmm_*`, one leaf per bar in the bar's own colour: RODGER tan
`#A8906C`, HOWARD grey `#9DA3A6`, PRESIDENT orange `#F0A526`, WALSH red
`#C1272D`. No bare `medal_acmm` or `ribbon_acmm` exists.

Blatherwick ch40 confirms the ribbon is **scarlet on the left half, green on
the right**, and notes a pre-2019 edition had it reversed. Ours is scarlet
left.

---

## §7 Four missing medals - three built, one not

| Key | Built | Basis |
|---|---|---|
| `navyleague` | yes | 38 mm red, central white 17 mm, single 2 mm blue in the centre of the white |
| `seaservice` | yes | 38 mm blue, central white 17 mm, 2 mm yellow at each edge of the white, 2 mm dark green in the middle |
| `airservice` | yes | 35 mm: 10 mm royal blue borders, two 4 mm gold stripes, 7 mm light blue centre |
| `afa` | **no** | see below |

All three come from Blatherwick, *Canadian Orders, Decorations and Medals*,
ch 40, 11 Jan 2019, which gives dimensioned ribbon descriptions. `seaservice`
is independently corroborated by the Wikipedia blazon (azure, or, argent,
vert, argent, or, azure) — same seven stripes, same order.

**Stripe geometry is measured; colours are estimated.** No source publishes
hex values, so the blues, golds and greens were chosen to sit with the rest of
the set. Flagged as `MEASURED geometry / ESTIMATED colour` per key.

`navyleague` and `seaservice` both carry a large fouled anchor, drawn as a
vector device. Legends are as published: CADET / EXCELLENCE and FOR SERVICE /
POUR SERVICE. `airservice` should carry the RCAirC crest; it has a maple leaf
standing in, since I have no RCAirC artwork.

### afa — please hide it

Blatherwick's entry for the Air Force Association Medal carries the terms of
the award and the selection criteria, then stops. There is no DESCRIPTION or
RIBBON section. A separate search returned only US Air Force Association
JROTC awards, which are a different thing entirely. Nothing else describes it.

Drawing a ribbon for it would be invention, so nothing was produced. It is
recorded under `_unsourced` in the manifest with the reason. **Hide slot 6.**

---

## §6 Service medal year bars - the three schemes differ

`armyservice` is unchanged in scheme, just renamed: 4 / 5 / 6 / 7 years,
one gold bar with a flat maple leaf per additional year, one gold maple leaf
per bar on the undress ribbon. Blatherwick confirms all of that and sources
the 3-bar ceiling.

**Sea and Air do not simply copy it, so no variants were generated.**

- **Sea** is a different scheme. Wikipedia describes a silver bar with a
  fouled anchor for one additional year and a bar with **two anchors** for two
  additional years — devices, not an accumulating stack. Blatherwick's Sea
  entry does not mention bars at all. One moderate-quality source and a
  silence is not enough to build from.
- **Air** bars exist — commercial medal suppliers list "Bar, Air Cadet Service
  Medal" — but no source found describes the scheme or the device. Blatherwick
  covers the Air medal's ribbon in full and says nothing about bars.

Both are shipped **base state only**. If you can get the Navy League and Air
Cadet League dress instructions, both are a few lines each in
`medal_specs.py`.

---

## §8 Pins

`pin_cds`, `pin_command`, `pin_cadet` and `pin_navy` are drawn as real
insignia at the Chapter 5 sizes: bars with maple leaves, and a fouled anchor
for the Navy League one. `pin_commendation` is gone.

| Key | Size | Aspect | Device |
|---|---|---|---|
| `pin_cds` | 20 x 5 mm | 4.0 | gold bar, three maple leaves |
| `pin_command` | 20 x 5 mm | 4.0 | silver bar, three maple leaves |
| `pin_cadet` | 20 x 5 mm | 4.0 | silver bar, one maple leaf |
| `pin_navy` | 20 x 7.5 mm | 2.667 | silver bar, one anchor |

Para 11 describes the Navy League pin as "a bar with a single **anchor leaf**"
— quirk preserved verbatim in the manifest. Read as an anchor.

### pin_dofe - you already have it

Do not draw one. `art_pack.js`, already in the tool, contains `dofe_bronze`,
`dofe_silver` and `dofe_gold` at aspect 1.197 — the oval cypher insignia, all
three levels, correct artwork. Point the DofE slot at those.

That also resolves the dimensions question the wrong way round: Annex D gives
no millimetres for the oval, but you do not need them, because the existing
art already carries the true aspect. What you cannot do is represent the award
with a single `pin_dofe` key, since it is issued at three levels.

---

## Corrections carried in from Blatherwick

Worth recording, since two of these reverse things I sent earlier.

1. **ANAVETS is seven stripes, not nine.** Blatherwick: 35 mm, "blue, red and
   white edges and a wide blue centre". That matches my original scanline of
   the Annex D thumbnail. The nine-stripe version I sent last round came from
   eyeballing a photo and was **wrong**. Reverted.
2. **ACSM stripe ratio corrected.** Blatherwick: green ribbon, edges of yellow
   and red, red outermost, **red twice as wide as the yellow**. My measured
   ratio was 2.6 because JPEG bleed had eaten part of the yellow. Now 17 / 8.5
   / 49 / 8.5 / 17.
3. **Strathcona ribbon is 32 mm**, five *equal* stripes — confirms the equal
   fifths I had, and matches the ruler photo.
4. **Bravery ribbon width is contested.** CATO Annex B says 1.5 in / 3.8 cm.
   Blatherwick says 36 mm. Unresolved; both recorded. Rendered at 35 per §2.
5. Blatherwick also confirms the ANAVETS outer annulus is **24 equal areas**
   enamelled alternately red, white and blue — the checker ring is 8 x 3, so
   exactly right by luck.

## Width overrides

Three ribbons are not really 35 mm. All are rendered at 35 per §2, with the
true width in the manifest as `true_ribbon_width_mm` plus a `width_note`:

| Key | True width | Source |
|---|---|---|
| `bravery` | 38 mm (CATO) / 36 mm (Blatherwick) | contested |
| `strathcona` | 32 mm | Blatherwick |
| `navyleague` | 38 mm | Blatherwick |
| `seaservice` | 38 mm | Blatherwick |

## Legibility overrides, unchanged

Black hairline on every bar and device; black legends on every disc face;
ACSM and St. George discs solid rather than dark-fielded; WALSH bar solid red
with gold lettering. All deliberate departures from the issued artwork, all
one-line reverts in `make_medals.py`.

## Still stylised

Medallion obverses. Ribbons, suspenders, bars, engraved legends, the anchor
and the ANAVETS checker ring are right. The central relief — three cadet
heads, Strathcona's profile, St George and the dragon, the ANAVETS Union Jack
shield, the RCAirC crest — is not reproducible from the sources available.
