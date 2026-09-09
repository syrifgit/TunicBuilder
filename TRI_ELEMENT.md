# Making the tool tri-element

**The framework is built. Sea and Air are stubs waiting on source material.**

The blocker was that slot names encoded which sleeve they were on, baked into the rules
pack, the resolver and the validator. That is fixed: slot ids are semantic and an
`ELEMENTS` table assigns them to arms. Army output was verified byte-identical through
the whole refactor.

What is left is entirely data: the placement instruction, sizes and artwork for Sea and
Air. No more surgery.

The rest of this file is the reasoning, kept because the next person will want to know
why it is shaped this way.

---

## What already works

Worth knowing before scoping, because it's more than you'd expect.

- **The coordinate model is element-neutral.** `y` up from the cuff, `x` front-positive,
  one mirror applied once in `drawSleeve`. Nothing about it is army-specific.
- **The medals layer is already tri-element.** `MEDALS` carries `element` tags, the
  service medal is already an element choice resolving to seq 9 / 10 / 11, and the
  artwork covers all three. A sea cadet's medals would render correctly today.
- **`state.unit`** already proves the pattern: a dropdown that swaps artwork.
- **The renderer doesn't care.** `drawSleeve(g, items, side, ...)` takes whatever boxes
  it's given. It never asks what element they are.

## What the blockers were

### 1. Slot ids were positional, not semantic

This is the real problem. **Twelve of the 22 rules-pack slots are sleeve slots named
for a side**, and eight of those twelve are one logical slot written twice:

```
left_corps_name    right_corps_name           right_rank_junior
left_rcac_badge    right_rcac_badge           right_rank_senior_no_appointment
left_marksmanship  right_appointment          right_rank_senior_with_appointment
left_proficiency_stack  right_ctc_grid        right_star_level
```

In the template it's six ids to rename. The other ten positional ids are breast slots
(`front_left_poppy`, `right_medals` and so on), and those are anatomical rather than
element-varying, so they stay exactly as they are.

Sea puts rank on the **left** arm. Air puts it on **both**. So `right_rank_junior` is
wrong for two of three elements, and it's not just a label: that string is a key.

It's used in the rules pack, in `resolve()` as literal `push(L, ...)` and `push(R, ...)`
calls, and in six literal string comparisons in `validate()`, which exempts overlaps by
matching the id:

```js
if (A.slot==="left_proficiency_stack" && B.slot==="left_proficiency_stack") continue;
```

**Fix:** rename to semantic ids (`proficiency_stack`, `rank_junior`, `star_level`) and
make the sleeve an attribute set from an element table. Pure refactor, no behaviour
change, and it's safely testable: army output has to come out byte-identical.

Do this first and on its own. It touches everything and it's the one step with a
perfect test.

### 2. A slot can only appear once

Air wears rank on both arms. Right now every slot resolves to at most one box, so
"both" has no representation. Either the resolver emits one box per assigned sleeve, or
the element table says `sleeve: "both"` and `resolve()` loops. The corps title and RCAC
badge already do the second thing:

```js
for (const [arr,side] of [[L,"left"],[R,"right"]]) { ... }
```

so the pattern exists. It just needs to be general rather than hardcoded for those two.

### 3. Page weight is not actually a problem

I assumed it was and was wrong, so here are the numbers. Measured in headless Chrome
including full render, off local disk:

| Page | Load |
|---|---|
| 6.79 MB, today | 1.03 s |
| 15.85 MB, synthetic | 1.63 s |

Sub-linear and not painful. GitHub Pages caps at 100 MB per file, so 20 MB is not close.
**Put all three elements in one page.** A real in-page dropdown beats navigating between
sibling pages.

The cost that *is* real is git, not the browser. Base64 PNG compresses to 74% and cannot
be stored as a delta, so every committed rebuild of `docs/index.html` is roughly 5 MB of
permanent history. Hence the standing rule: `docs/` is a release, run `build_site.py` and
commit when you mean to publish, not on every rebuild.

---

## The element table

One object, everything element-specific in it. Sketch:

```js
const ELEMENTS = {
  army: {
    label: "Army",
    cloth: {fill:"#123D2C", edge:"#0A2A1E"},   // rifle green
    nametag: "black",
    sleeves: {                                  // semantic slot -> sleeve
      corps_name:"both", element_badge:"both",
      marksmanship:"left", proficiency_stack:"left",
      rank:"right", appointment:"right", star_level:"right", ctc_grid:"right"
    },
    ranks: RANKS_ARMY,          // names, art keys, sizes
    levels: STARS,              // training level badges
    proficiencies: [FITNESS, FIRSTAID, MUSIC],
    art: "army"
  },
  sea: { ..., sleeves:{ rank:"left", ... }, cloth:{fill:"#1A1A1A", ...} },
  air: { ..., sleeves:{ rank:"both", ... }, cloth:{fill:"#3A4A5C", ...} }
};
```

Everything you listed maps onto a field here:

- different rank names and graphics: `ranks`
- rank placement: `sleeves.rank`
- tunic colour: `cloth`
- same proficiencies, different badge: same categories in `proficiencies`, different art
  keys inside them
- extra proficiencies for sea/air: `proficiencies` is a list, so add entries
- different proficiency size or placement: goes in the rules pack, see below

## Rules pack

Keep **one pack** with per-element overrides, not three packs. Most geometry is shared,
and three packs means fixing a shared bug three times and maintaining three copies of
every citation and conflict.

Shape: each slot keeps its base geometry and gains an optional `elements` block for the
deltas.

```json
{
  "id": "proficiency_stack",
  "anchor": "cuff_bottom",
  "offset_cm": 20,
  "citation": "CH3S1 3.b.(5)",
  "elements": {
    "sea": {"offset_cm": 18, "citation": "<sea instruction, para>"},
    "air": {"sleeve": "left"}
  }
}
```

Rules that follow from the project's existing discipline:

- **Every override needs its own citation.** An army figure doesn't become a sea figure
  by being nearby. If you can't cite it for that element, it stays an open question and
  the validator says so.
- **Absent override means shared, and that's a claim.** Add a per-element
  `confirmed_shared: true` so "we checked and it's the same" is distinguishable from
  "nobody looked yet". Without that you can't tell.
- **Conflicts stay in one place.** The six recorded conflicts are army-sourced. Sea and
  air will grow their own; same `conflicts` block, tagged with element.

## Validator

Two things break quietly.

**Slot-id exemptions** become semantic ids. Easy, but must not be missed or you'll get
clash boxes over correct output. That already happened once with the medals.

**Clearance checks are element-specific.** The Sgt-plus-Drum-Major collision at 55 cm is
an army fact about army badge sizes on an army sleeve. Sea and air get their own
collisions and their own tunic sizes, and only 6436 army is measured. Every clearance
warning needs to say which element and which size it's checking, or it'll assert army
geometry about a sea cadet.

## Artwork

Split into a shared pack and three element packs:

```
art/art_shared.js    medals, ribbons, commendation pins, DofE   (2.2 MB)
art/art_army.js      ranks, stars, proficiencies, RCAC badge    (4.5 MB)
art/art_sea.js
art/art_air.js
```

Keys stay flat and namespaced by element where they differ (`rank_army_Cpl`,
`rank_sea_PO2`). Flat keys with a merge is what the tool already does with
`Object.assign(BADGE_ART, MEDAL_ART)`, so no lookup changes.

`build.py` splices the shared pack plus all three element packs into the one page,
since page weight turned out not to matter. It already merges two packs this way.

## UI

Element dropdown at the top of the Cadet group, above name. It's the widest-reaching
control on the page, so it goes first.

Everything downstream rebuilds from the element table: rank options, proficiency
dropdowns, level badges, and the cloth colour, which is four CSS variable definitions
today (light, dark, print) and should become one `body[data-element]` block per element.

The rest of the rail doesn't change shape. Summer training, pins and medals are already
collapsible and mostly element-neutral.

---

## Order of work

1. ~~**Rename slots to semantic ids.**~~ **Done.** Rules pack, resolver, validator.
   Verified byte-identical: same md5 on all three SVGs, with every slot exercised.
2. ~~**Add the element table.**~~ **Done.** `ELEMENTS` holds cloth, nametag colour and
   the slot-to-sleeve map. Army drives current behaviour through it, still identical.
3. ~~**Multi-sleeve slots.**~~ **Done.** `put()` emits one box per assigned sleeve.
   Tested: army draws 18 sleeve images, sea 18 with rank moved left, air 19 with rank
   on both arms.
4. ~~**Element selector.**~~ **Done.** Dropdown at the top of the rail, cloth colour
   follows it, and an unmodelled element raises a `crit` saying so.
5. **Add sea**, once you have sources. Then air. Data entry plus artwork, not surgery.

Steps 1 to 4 are complete and needed no source material. Step 5 is the part gated on
documents.

## What is stubbed and what that means

`ELEMENTS.sea` and `ELEMENTS.air` exist and carry only what you stated: rank on the left
arm for sea, both arms for air, and a tunic colour. Everything else is deliberately still
the army ruleset, and the tool says so rather than pretending:

> Sea cadets are not modelled yet. The sleeve assignment is in place, but every badge,
> size and placement below is still the ARMY ruleset, and the artwork is army artwork.

The two cloth colours are unsourced placeholders. They look right and they are not cited,
which is why `cite` is `null` on both stubs.

## What to source

For each of sea and air:

- placement instruction equivalent to CJCR Dress Instructions Ch 3 Sect 1, with the
  figures. This is the one that actually blocks work.
- rank insignia names, sizes and artwork
- training level and proficiency badge names, sizes, artwork
- whether the proficiency stack order and anchor match army
- tunic colour reference, and nametag colour (air force blue for air is already noted)
- one measured tunic per element, the way 6436 was measured for army

The medals are already done for all three.
