"""Ribbon and medal specifications for cadet honours worn on the army cadet tunic.

Keys and precedence follow the tunic tool's own scheme (ARTWORK_REQUEST.md §4),
which is CATO 13-16 para 19 with the Order of St. George inserted at 8 on the
authority of CJCR Gp O 10050.

Fidelity flags:
  MEASURED  - sampled off issued artwork, or a published dimensioned description
  ESTIMATED - read off a photo or thumbnail by eye
Stripe weights are relative and normalise to the ribbon width.

Primary sources: CATO 13-16 (canada.ca), ACLC National Policy 13.1, CJCR Gp O
10050 annexes, CJCR Dress Instructions ch 5, and Blatherwick, "Canadian Orders,
Decorations and Medals", ch 40 *Canadian Navy, Army and Air Cadet Medals*,
11 Jan 2019 - cited below as Blatherwick ch40, which gives dimensioned ribbon
descriptions for most of the set.
"""

MEDALS = {
    # ------------------------------------------------------------- 1 ------
    "bravery": {
        "name": "Cadet Award for Bravery",
        "short": "Bravery",
        "authority": "CATO 13-16 Annex B",
        "precedence": 1,
        "ribbon_width_mm": 38,      # CATO Annex B para 2 says 1.5 in / 3.8 cm.
                                    # Blatherwick ch40 says 36 mm. Unresolved;
                                    # rendered at 35 for row alignment.
        "stripes": [("#1C2E52", 19), ("#D14124", 13), ("#AFC3D6", 36),
                    ("#D14124", 13), ("#1C2E52", 19)],
        "top_bar": "CANADA",
        "suspension": "bar",
        "suspension_text": "CADET",
        "metal": "silver",
        "legend_top": "FOR BRAVERY",
        "legend_top2": "POUR BRAVOURE",
        "legend_bottom": None,
        "device": None,
        "fidelity": "ESTIMATED",
        "source": "Stripe order from CATO 13-16 Annex B para 2 and Blatherwick "
                  "ch40 (dark blue edges, red stripes, wide light blue centre). "
                  "Widths and hex values read off a product photo by eye. "
                  "Blatherwick confirms both legend lines sit in the top third.",
    },
    # ------------------------------------------------------------- 2 ------
    "strathcona": {
        "name": "Lord Strathcona Medal",
        "short": "Strathcona",
        "authority": "CJCR Gp O 10050 Annex B (CATO 13-16 Annex D superseded)",
        "precedence": 2,
        "ribbon_width_mm": 32,      # Blatherwick ch40, corroborated by a ruler
                                    # photo; rendered at 35 for row alignment
        "stripes": [("#9B1B34", 20), ("#1F5A38", 20), ("#9B1B34", 20),
                    ("#1F5A38", 20), ("#9B1B34", 20)],
        "top_bar": None,
        "suspension": "ring",
        "metal": "bronze",
        "legend_top": "AGMINA DUCENS",
        "legend_bottom": None,
        "device": None,
        "fidelity": "MEASURED",
        "source": "Scanline of 10050-Annex-B.pdf art gave five near-equal "
                  "stripes; Blatherwick ch40 confirms five EQUAL stripes of "
                  "dark crimson and dark green on a 32 mm ribbon, and the "
                  "AGMINA DUCENS legend on a copper medal.",
    },
    # ------------------------------------------------------------- 3 ------
    "legion": {
        "name": "Royal Canadian Legion Cadet Medal of Excellence",
        "short": "RCL Excellence",
        "authority": "CATO 13-16 Annex E / CJCR Gp O 10050 Annex C",
        "precedence": 3,
        "ribbon_width_mm": 35,
        "stripes": [("#1F2E66", 25), ("#E8B41F", 50), ("#1F2E66", 25)],
        "top_bar": None,
        "suspension": "ring",
        "metal": "silver",
        "legend_top": "ROYAL CANADIAN LEGION",
        "legend_bottom": "LA LÉGION ROYALE CANADIENNE",
        "centre_lines": ["CADET", "EXCELLENCE"],
        "device": None,
        "fidelity": "MEASURED",
        "source": "Scanline of 10050-Annex-C.pdf art gave blue 23.7 / gold 48.4 "
                  "/ blue 23.7%, rounded to 25/50/25. Blatherwick ch40 confirms "
                  "blue edges with a wide yellow centre and the four-line legend.",
    },
    # ------------------------------------------------------------- 4 ------
    "navyleague": {
        "name": "Navy League of Canada Medal of Excellence",
        "short": "Navy League Excellence",
        "authority": "CATO 13-16 para 10.b (Navy League of Canada documents)",
        "precedence": 4,
        "ribbon_width_mm": 38,      # Blatherwick ch40
        "stripes": [("#C8102E", 10.5), ("#F4F4F2", 7.5), ("#1F4FA8", 2),
                    ("#F4F4F2", 7.5), ("#C8102E", 10.5)],
        "top_bar": None,
        "suspension": "ring",
        "metal": "silver",
        "legend_top": "CADET",
        "legend_bottom": "EXCELLENCE",
        "device": "anchor",
        "fidelity": "MEASURED geometry / ESTIMATED colour",
        "source": "Blatherwick ch40: 38 mm red ribbon, central white stripe "
                  "17 mm, a single 2 mm blue stripe in the centre of the white. "
                  "Silver 44 mm medal, large fouled anchor, CADET above and "
                  "EXCELLENCE below, ring suspension. Exact hues not published, "
                  "so reds and blues match the rest of the set.",
    },
    # ------------------------------------------------------------- 5 ------
    "acmm": {
        "name": "Army Cadet Medal of Merit",
        "short": "ACMM",
        "authority": "Army Cadet League of Canada. Replaces the Maj-Gen W.A. "
                     "Howard Award at CATO 13-16 para 19.e.",
        "precedence": 5,
        "ribbon_width_mm": 35,
        "stripes": [("#C8102E", 50), ("#00703C", 50)],   # scarlet LEFT
        "top_bar": None,
        "suspension": "bar_plain",
        "metal": "gold",
        "legend_top": None,
        "legend_bottom": "MERIT \u2022 MÉRITE",
        "device": "leaf",
        "award_bars": [
            ("RODGER", "bar_rodger"),
            ("HOWARD", "bar_howard"),
            ("PRESIDENT", "bar_president"),
            ("WALSH", "bar_walsh"),
        ],
        "bar_devices": {"RODGER": "#A8906C", "HOWARD": "#9DA3A6",
                        "PRESIDENT": "#F0A526", "WALSH": "#C1272D"},
        "bar_ink": {"WALSH": "#F0A526"},
        "bar_band_frac": 0.75,
        "bar_max_pitch": 2.2,
        "fidelity": "ESTIMATED",
        "source": "Redrawn from the ACLC per-bar illustrations. Blatherwick "
                  "ch40 confirms the ribbon is scarlet on the LEFT half and "
                  "green on the right, and flags that a pre-2019 edition had "
                  "this reversed. Hues read by eye.",
    },
    # ------------------------------------------------------------- 7 ------
    "anavets": {
        "name": "ANAVETS Cadet Medal of Merit",
        "short": "ANAVETS",
        "authority": "CATO 13-16 Annex F / CJCR Gp O 10050 Annex D",
        "precedence": 7,
        "ribbon_width_mm": 35,      # Blatherwick ch40
        "stripes": [("#3A5BA8", 12), ("#C0272E", 8), ("#F2F2F0", 9),
                    ("#3A5BA8", 42), ("#F2F2F0", 9), ("#C0272E", 8),
                    ("#3A5BA8", 12)],
        "top_bar": "CADET",
        "suspension": "bar",
        "suspension_text": "MERITUM",
        "bar_end_leaves": True,
        "disc_checker": ["#C0272E", "#F2F2F0", "#2B4A9B"],
        "metal": "pewter",
        "legend_top": "ARMY NAVY AIR FORCE",
        "legend_bottom": "VETERANS IN CANADA",
        "device": None,
        "fidelity": "ESTIMATED",
        "source": "Blatherwick ch40: 35 mm, blue, red and white edges with a "
                  "wide blue centre - which matches the original scanline of "
                  "the 104 px Annex D thumbnail, so the seven-stripe order is "
                  "restored (an earlier nine-stripe reading off a photo was "
                  "wrong). Blatherwick also confirms the outer annulus is "
                  "divided into 24 equal areas enamelled alternately red, "
                  "white and blue, and that both bars carry a maple leaf at "
                  "each end of the word. Widths and hues still eyeballed.",
    },
    # ------------------------------------------------------------- 8 ------
    "stgeorge": {
        "name": "Order of St. George Medal",
        "short": "St. George",
        "authority": "CJCR Gp O 10050 Annex E. NOT listed in CATO 13-16.",
        "precedence": 8,
        "ribbon_width_mm": 35,
        "stripes": [("#F4F4F2", 10), ("#CE1F2E", 80), ("#F4F4F2", 10)],
        "top_bar": None,
        "suspension": "bar",
        "suspension_text": None,
        "metal": "dark",
        "legend_top": "PRO MERITO",
        "legend_bottom": "ORDER OF ST. GEORGE",
        "device": None,
        "fidelity": "MEASURED",
        "source": "Scanline of 10050-Annex-E.pdf art (290x663 @300ppi), legends "
                  "read off a product photo. Neither Blatherwick ch40 nor "
                  "CATO 13-16 covers this medal.",
    },
    # ------------------------------------------------------------- 9 ------
    "seaservice": {
        "name": "Sea Cadet Service Medal",
        "short": "Sea Service",
        "authority": "CATO 13-16 para 10.c (Navy League of Canada documents)",
        "precedence": 9,
        "ribbon_width_mm": 38,      # Blatherwick ch40
        "stripes": [("#16478A", 10.5), ("#E8B41F", 2), ("#F4F4F2", 5.5),
                    ("#14512B", 2), ("#F4F4F2", 5.5), ("#E8B41F", 2),
                    ("#16478A", 10.5)],
        "top_bar": None,
        "suspension": "ring",
        "metal": "silver",
        "legend_top": "FOR SERVICE",
        "legend_bottom": "POUR SERVICE",
        "device": "anchor",
        "fidelity": "MEASURED geometry / ESTIMATED colour",
        "source": "Blatherwick ch40 (38 mm blue, central white 17 mm carrying "
                  "2 mm yellow at each edge of the white and a 2 mm dark green "
                  "in the middle), corroborated independently by the Wikipedia "
                  "blazon: azure, or, argent, vert, argent, or, azure. Silver "
                  "35 mm medal, large fouled anchor, FOR SERVICE above and "
                  "POUR SERVICE below, ring suspension. Hues not published.",
    },
    # ------------------------------------------------------------- 10 -----
    "armyservice": {
        "name": "Army Cadet Service Medal",
        "short": "ACSM",
        "authority": "ACLC National Policy 13.1",
        "precedence": 10,
        "ribbon_width_mm": 35,
        "stripes": [("#A5182C", 17), ("#D7A22B", 8.5), ("#1C6B3A", 49),
                    ("#D7A22B", 8.5), ("#A5182C", 17)],
        "top_bar": None,
        "suspension": "ring",
        "metal": "gold",
        "legend_top": "SERVICE \u2013 CADETS",
        "legend_bottom": "CANADA",
        "device": "leaf",
        "service_device": "leaf",
        "service_bar_metal": "gold",
        "service_bar_device": True,
        "max_service_bars": 3,
        "fidelity": "MEASURED",
        "source": "Scanline of the ACSM.pdf p5 embedded image, colours re-read "
                  "off a product photo. Blatherwick ch40 fixes the stripe "
                  "ratio (red twice the width of the yellow, red outermost), "
                  "confirms the bar is gold with a flat maple leaf in the "
                  "middle with one gold maple leaf on the undress ribbon per "
                  "bar, and sources the three-bar ceiling.",
    },
    # ------------------------------------------------------------- 11 -----
    "airservice": {
        "name": "Air Cadet Service Medal",
        "short": "Air Service",
        "authority": "CATO 13-16 para 12.b (Air Cadet League of Canada documents)",
        "precedence": 11,
        "ribbon_width_mm": 35,      # Blatherwick ch40
        "stripes": [("#10357F", 10), ("#E8B41F", 4), ("#8FB6D9", 7),
                    ("#E8B41F", 4), ("#10357F", 10)],
        "top_bar": None,
        "suspension": "ring",
        "metal": "gold",
        "legend_top": "SERVICE \u2013 CADETS",
        "legend_bottom": "CANADA",
        "device": "leaf",
        "fidelity": "MEASURED geometry / ESTIMATED colour",
        "source": "Blatherwick ch40 gives all five stripe widths in mm: 10 mm "
                  "royal blue borders for the Air Cadet League's Royal title, "
                  "7 mm light blue centre for the Air Force, two 4 mm gold "
                  "stripes for the four years of service. Gold 35 mm medal "
                  "with the RCAirC crest, SERVICE - CADETS above, CANADA "
                  "below. Hues not published; the central device is a maple "
                  "leaf standing in for the RCAirC crest.",
    },
}

# Not built. No ribbon or medal description could be sourced.
UNSOURCED = {
    "afa": {
        "name": "Air Force Association Medal",
        "precedence": 6,
        "authority": "CATO 13-16 para 12.a / CATO 52-08",
        "reason": "Blatherwick ch40 carries the terms of the award but its "
                  "entry stops after the selection criteria - there is no "
                  "DESCRIPTION or RIBBON section. No other description found. "
                  "Drawing one would be invention, so nothing was produced.",
    },
}

# Commendation and award pins. Sizes from CJCR Dress Instructions ch 5 paras
# 8-12. These are pins, not ribbons, so they carry their own dimensions.
PINS = {
    "pin_cds": {
        "name": "Chief of the Defence Staff Commendation",
        "authority": "CJCR DI ch 5 para 8",
        "w_mm": 20.0, "h_mm": 5.0,
        "metal": "gold", "device": "leaf", "count": 3,
        "fidelity": "MEASURED geometry",
        "source": "Gold plated, satin finished, a bar with three maple leaves, "
                  "2 cm by 0.5 cm.",
    },
    "pin_command": {
        "name": "Command Commendation (VCDS / RCN / CA / RCAF)",
        "authority": "CJCR DI ch 5 para 9",
        "w_mm": 20.0, "h_mm": 5.0,
        "metal": "silver", "device": "leaf", "count": 3,
        "fidelity": "MEASURED geometry",
        "source": "Silver plated, satin finished, a bar with three maple "
                  "leaves, 2 cm by 0.5 cm.",
    },
    "pin_cadet": {
        "name": "Cadet Commendation",
        "authority": "CJCR DI ch 5 para 10 / CATO 13-16 Annex C para 2",
        "w_mm": 20.0, "h_mm": 5.0,
        "metal": "silver", "device": "leaf", "count": 1,
        "fidelity": "MEASURED geometry",
        "source": "Silver plated, a bar with a single maple leaf, 2 cm by "
                  "0.5 cm. Replaces the old ribbon-sized pin_commendation.",
    },
    "pin_navy": {
        "name": "Navy League of Canada Award of Commendation",
        "authority": "CJCR DI ch 5 para 11",
        "w_mm": 20.0, "h_mm": 7.5,
        "metal": "silver", "device": "anchor", "count": 1,
        "fidelity": "MEASURED geometry / ESTIMATED device",
        "source": "Silver plated, 2 cm by 0.75 cm. The order reads \"a bar "
                  "with a single anchor leaf\" [sic] - quirk preserved; read "
                  "as an anchor, which is what Navy League insignia carries.",
    },
}

METALS = {
    "gold":   ["#7A5C14", "#F7E08A", "#C9A13A", "#8A6A1E"],
    "silver": ["#6F7679", "#EDF1F3", "#B6BEC2", "#7B8388"],
    "bronze": ["#6B3A1C", "#D8A06A", "#A35F2F", "#6D3D1E"],
    "pewter": ["#55595C", "#D2D6D9", "#9AA0A4", "#62676B"],
    "dark":   ["#3A3F42", "#A9B0B3", "#6E7579", "#454B4E"],
    "bar_walsh":     ["#8E0C20", "#D9243F", "#C8102E", "#A50E26"],
    "bar_president": ["#C97C10", "#F7B84E", "#F0A526", "#D98C18"],
    "bar_howard":    ["#7A8085", "#C9CFD2", "#9DA3A6", "#868C90"],
    "bar_rodger":    ["#7E6746", "#C4AE8C", "#A8906C", "#8A7350"],
}

# ACMM wearable states. Two rules: the medal is never worn bare, and Walsh
# requires President. 15 non-empty subsets less the 4 carrying Walsh without
# President leaves exactly 11.
ACMM_BARS = [("r", "RODGER"), ("h", "HOWARD"),
             ("p", "PRESIDENT"), ("w", "WALSH")]


def acmm_states():
    out = []
    for mask in range(1, 16):
        picked = [ACMM_BARS[i] for i in range(4) if mask >> i & 1]
        code = "".join(c for c, _ in picked)
        if "w" in code and "p" not in code:
            continue
        out.append((code, [n for _, n in picked]))
    return out
