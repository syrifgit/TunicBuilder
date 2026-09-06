"""Confirmed identifications, from Lt Beal's read of the poster layout.
slug -> (label, family, note). Authoritative over any caption in manifest.csv."""

LABELS = {
 # --- top row: poster titles and heraldry, none of it worn on the sleeve ---
 "symboles_des_cadets":  ("Poster title", "not_a_badge", ""),
 "royaux_de_larmée":     ("Poster title", "not_a_badge", ""),
 "unnamed":              ("Poster title block", "not_a_badge", ""),
 "royaux":               ("Poster title fragment", "not_a_badge", ""),
 "cadets":               ("Poster title fragment", "not_a_badge", ""),
 "canadienne":           ("Poster title fragment", "not_a_badge", ""),
 "larmée_canadienne":    ("Poster title fragment", "not_a_badge", ""),
 "emblem":               ("RCAC Emblem", "heraldry", "Marketing use. Not worn on uniform."),
 "unnamed_2":            ("RCAC Banner", "heraldry", ""),
 "royal_canadian_army_cadets_camp_flag": ("Camp Flag", "heraldry", ""),
 "unnamed_3":            ("Cadets Flag", "heraldry", ""),
 "trumpet_banner":       ("Trumpet Banner", "heraldry", ""),
 "pipe_banner":          ("Pipe Banner", "heraldry", ""),
 "headdress_badge":      ("Headdress Badge", "heraldry", "Cap badge, not a sleeve item."),

 # --- shoulder pair, extracted as two bad crops; split by recut_shoulder.py ---
 "da_vi_d_d_e_f_al_ar_de": ("Shoulder title + RCAC badge (example 1)", "shoulder",
                            "BAD CROP: merges corps name title with the RCAC circle below it."),
 "unnamed_5":              ("Shoulder title + RCAC badge (example 2)", "shoulder",
                            "BAD CROP: same template as item 15, different corps name."),
 "unnamed_4":              ("Commander's Cadet Commendation Pin", "out_of_scope",
                            "Pinned insignia, front of tunic."),

 # --- rank and appointment ---
 "lance_corporal":         ("Lance Corporal", "rank", ""),
 "corporal":               ("Corporal", "rank", ""),
 "master_corporal":        ("Master Corporal", "rank", ""),
 "sergeant":               ("Sergeant", "rank", ""),
 "unnamed_6":              ("Warrant Officer", "rank", "Caption lost by the extractor."),
 "master_warrant_officer": ("Master Warrant Officer", "rank", ""),
 "chief_warrant_officer":  ("Chief Warrant Officer", "rank", ""),
 "drum_major":             ("Drum Major", "appointment", ""),
 "pipe_major":             ("Pipe Major", "appointment", ""),

 # --- star levels, then three terminated / out-of-scope families ---
 "green_star":  ("Green Star", "star", ""),
 "red_star":    ("Red Star", "star", ""),
 "silver_star": ("Silver Star", "star", ""),
 "gold_star":   ("Gold Star", "star", ""),
 "master_cadet":("Master Cadet", "terminated", "Terminated programme. Slot stays vacant."),
 "level_1":     ("National Star of Excellence 1", "terminated", "Terminated programme."),
 "level_2":     ("National Star of Excellence 2", "terminated", "Terminated programme."),
 "level_3":     ("National Star of Excellence 3", "terminated", "Terminated programme."),
 "level_4":     ("National Star of Excellence 4", "terminated", "Terminated programme."),
 "bronze_level":("Duke of Edinburgh's Award – Bronze", "dofe", "Pin. Not in QualMap."),
 "silver_level":("Duke of Edinburgh's Award – Silver", "dofe", "Pin. Not in QualMap."),
 "gold_level":  ("Duke of Edinburgh's Award – Gold", "dofe", "Pin. Not in QualMap."),

 # --- summer training, top row ---
 "general_training":              ("General Training", "ctc", "No matching QualMap row."),
 "basic_expedition":              ("Expedition – Basic", "ctc", ""),
 "expedition_instructor":         ("Expedition – Instructor", "ctc", ""),
 "leadership_and_challenge":      ("Expedition – Leadership and Challenge", "ctc", ""),
 "basic_marksman":                ("Marksmanship – Basic", "ctc", ""),
 "air_rifle_marksmanship":        ("Air Rifle Marksmanship Instructor", "ctc", ""),
 "fullbore_marksmanship":         ("Marksmanship – Fullbore Phase 1", "ctc", ""),
 "fullbore_marksmanship_2":       ("Marksmanship – Fullbore Phase 2", "ctc", ""),
 "basic_fitness_and_sports":      ("Fitness and Sports – Basic", "ctc", ""),
 "fitness_and_sports_instructor": ("Fitness and Sports – Instructor", "ctc", ""),
 "basic_drill_and_ceremonial":    ("Drill and Ceremonial – Basic", "ctc", ""),
 "and_ceremonial_instructor":     ("Drill and Ceremonial – Instructor", "ctc", ""),

 # --- summer training, bottom row ---
 "staff_cadet":       ("Staff Cadet", "ctc", ""),
 "army_cadet_voyage": ("Army Cadet Voyage", "ctc", "No matching QualMap row."),
 "maple_leaf":        ("Maple Leaf Exchange", "ctc", "No matching QualMap row. Caption was wrong."),
 "canadian_armed_forces": ("Parachutist badge", "out_of_scope",
                           "Left breast, 0.5 cm above the pocket. Caption was wrong."),
 "military_band":   ("Military Band – Basic", "ctc", ""),
 "military_band_2": ("Military Band – Intermediate", "ctc", ""),
 "military_band_3": ("Military Band – Advanced", "ctc", ""),
 "pipe_band":       ("Pipe Band – Basic", "ctc", ""),
 "pipe_band_2":     ("Pipe Band – Intermediate", "ctc", ""),
 "pipe_band_3":     ("Pipe Band – Advanced", "ctc", ""),

 # --- sleeve proficiency ---
 "marksman":               ("Marksman", "marksmanship", ""),
 "first_class_marksman":   ("First Class Marksman", "marksmanship", ""),
 "expert_marksman":        ("Expert Marksman", "marksmanship", ""),
 "distinguished_marksman": ("Distinguished Marksman", "marksmanship", ""),
 "emergency":              ("First Aid – Emergency", "first_aid", ""),
 "standard":               ("First Aid – Standard", "first_aid", ""),
 "basic_qualification":    ("Music – Basic", "music", ""),
 "qualification_level_1":  ("Music – Level 1", "music", ""),
 "unnamed_7":              ("Music levels 2-5 + Canada wordmark", "music",
                            "BAD CROP: levels 2-4 recovered by recut_music.py."),
 "level_5":                ("Music – Level 5", "music", ""),

 # --- bottom pin section: mostly never extracted ---
 "unnamed_8":  ("Unidentified fragment", "not_a_badge", "Effectively blank."),
 "unnamed_9":  ("Expedition – Regional pin", "out_of_scope", "Front of tunic, left pocket."),
 "unnamed_10": ("Poster footer element", "not_a_badge", ""),
 "unnamed_11": ("Poster footer element", "not_a_badge", ""),
 "unnamed_12": ("Poster footer element", "not_a_badge", ""),
 "unnamed_13": ("Poster footer element", "not_a_badge", ""),
 "unnamed_14": ("Poster footer element", "not_a_badge", ""),
}

# On the poster but never extracted. extract_badges.py clusters vector drawing
# objects, so raster artwork and anything outside its area filters was dropped.
MISSING = [
 ("Army Cadet Service Medal (+ bar)", "medal",      "Medal row"),
 ("Order of St George",               "medal",      "Medal row"),
 ("ANAVETS Medal of Merit",           "medal",      "Medal row"),
 ("Major-General W.A. Howard Award",  "medal",      "Medal row"),
 ("Legion Medal of Excellence",       "medal",      "Medal row"),
 ("Lord Strathcona Medal",            "medal",      "Medal row"),
 ("Cadet Award for Bravery",          "medal",      "Medal row"),
 ("RCAC National Rifle Team pin",     "out_of_scope","Summer training bottom row"),
 ("Belzile Trophy pin",               "out_of_scope","Summer training bottom row"),
 ("Marksmanship competition pins x4", "out_of_scope","Zones / Prov / Nat / Nat Winners"),
 ("Biathlon competition pins x4",     "out_of_scope","Zones / Prov / Nat / Nat Winners"),
 ("Expedition pins (National etc.)",  "out_of_scope","Only Regional was extracted"),
]
