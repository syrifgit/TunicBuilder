# Air artwork: second follow-up

Revision 2 is in and drawing. The Effective Speaking cut-outs are clean, and your
`medal_specs.py` regenerates our medal manifest exactly. Thanks.

One reversal, three medal requests and a new job. **Work from the `medal_specs.py` sent
with this note**, not your own copy: ours already has item 1 in it.

---

## 1. The Air Cadet Service Medal is gold after all

Lt Beal has confirmed it: the disc is gold, as Blatherwick says. The poster prints it
brown, which is what fooled both of us. Our `medal_specs.py` has `airservice` back to
`"metal": "gold"`, with the source note rewritten to say why.

Nothing needs regenerating for the disc itself. We restored your earlier gold
`medal_airservice` image, which is what the unchanged `make_medals.py` draws with gold.
But the bars in item 2 build on it, so they need to be gold too.

## 2. Air Cadet Service Medal bars

Air uses the same system as Army: four years earns the medal, and each further year adds
a bar, accumulating. The devices differ (Lt Beal):

- **Medal:** a gold bar with a bird on it, wings spread.
- **Undress ribbon:** a rosette per bar, where Army uses a maple leaf.

Please build 5, 6 and 7 years, exactly these keys:

```
medal_airservice_5yr    medal_airservice_6yr    medal_airservice_7yr
ribbon_airservice_5yr   ribbon_airservice_6yr   ribbon_airservice_7yr
```

Same layout rules and canvases as the `armyservice` bars (35 × 100 mm and 35 × 10 mm).
The tool draws them as soon as the keys exist and falls back to the plain medal until
then. The bird and the rosette are described in words only, so flag both as stylised.

## 3. The AFA ribbon: ANAVETS colours

Lt Beal says the AFA ribbon uses the ANAVETS palette. The poster's print shifted it, the
same print that turned the service medal's gold brown. Keep your stripe pattern and
proportions and swap in the ANAVETS hexes from `medal_specs.py`:

| Stripe | Width | Was | Now |
|---|---|---|---|
| edge | 9 | navy `#101A3D` | blue `#3A5BA8` |
| | 8 | pale teal `#70B3BD` | white `#F2F2F0` |
| | 9 | navy | blue |
| centre | 41 | dark maroon `#491219` | red `#C0272E` |
| | 9 | navy | blue |
| | 8 | pale teal | white |
| edge | 9 | navy | blue |

Regenerate `ribbon_afa` and `medal_afa`, and update the fidelity note: stripe pattern
from the poster, colours from the ANAVETS palette per Lt Beal.

## 4. `src/maple_leaf_path.txt`

`make_medals.py` reads it, and it has never come with a delivery, so nobody here can
regenerate the medals. Please send it.

If it's easy, the font too: `FONT_PATH` is an absolute Linux path, so the script can't
run on Windows. A bundled copy behind a relative path would fix that, if TeX Gyre Heros's
licence allows bundling. cairosvg needing the cairo DLL is our problem, not yours.

## 5. New job: an Air squadron title generator

You offered; Lt Beal said yes. The tool shows your two poster samples for now (89
Pacific, 96 Alouette). What it needs is any squadron:

- **The design:** the half-round dome, the element name arched over the top, the
  squadron number large in the centre, the squadron name on a straight line below.
  Match the poster samples closely enough that a render of 89 PACIFIC sits next to the
  poster crop without looking different.
- **Inputs:** squadron number, squadron name, language. English is ROYAL CANADIAN AIR
  CADETS and French is CADETS DE L'AVIATION ROYALE DU CANADA.
- **Proportions:** the measured badge, 4.25 in × 52 mm (aspect 2.076), not the poster's
  2.253. Long names should shrink to fit rather than overflow.
- **Output:** transparent PNG trimmed to the badge, plus a blank plate carrying the
  arched element name only, one per language.
- **Runs on Windows with Pillow alone:** no cairo, and no absolute font paths. Bundle
  free fonts with the script or take them as arguments. Our army title kit has a
  hardcoded Linux font path and can't run here, which is exactly what to avoid.
- **Name and interface:** `make_squadron_title.py`, something like
  `--number 89 --name PACIFIC --lang en --out 89_pacific_en.png`.

Send 89 PACIFIC (English) and 96 ALOUETTE (French) as test renders, so they can be held
up against the poster.

## Not needed

- **Silver and gold wire wings.** Leave them; the issued nylon wings are what's drawn.
- **Sea.** Coming, but later.

## Expected back

- The medal pack at **58 keys** (52 plus the 6 bars), with `ribbon_afa` and `medal_afa`
  recoloured and nothing else changed. Its manifest and `medal_specs.py` should still
  regenerate one from the other.
- `src/maple_leaf_path.txt`, and the font if you can.
- `make_squadron_title.py` with its fonts, the two blank plates and the two test
  renders.
