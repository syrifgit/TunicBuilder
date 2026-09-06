"""Expedition insignia belongs on the RIGHT, above the nametag - not the left pocket.

CH5-B's expedition figure: "Expedition participation insignia is worn over the right
jacket/shirt pocket, centred 0.5 cm over the nametag." I had it modelled correctly in
front_right_expedition AND wrongly as a left-pocket pin stream, so selecting it put a
pin in the wrong place. Removing the left-pocket stream and giving the right-hand slot
a proper level dropdown with the real artwork.

National Rifle Team stays, but its location is NOT confirmed - flagged as such until
Lt Beal validates it.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
p = "tunic.template.html"
s = open(p, encoding="utf-8").read()
orig = s
subs = []

# ---- drop the left-pocket expedition stream ----
subs.append(('''  {key:"exped", label:"Expedition", slot:"Expedition", opts:[
    {v:"none",           nm:"None"},
    {v:"exped_lvl1",     nm:"Level 1 (nothing worn)", worn:false},
    {v:"exped_lvl2",     nm:"Level 2 (nothing worn)", worn:false},
    {v:"exped_regional", nm:"Regional", est:true},
    {v:"exped_national", nm:"National / International", est:true}]},
''', ""))

# ---- expedition levels, worn on the right above the nametag ----
subs.append(('const EXPED_D = 2.54;                        // ESTIMATE, 1 in circle',
'''// Expedition participation insignia. Worn over the RIGHT pocket, 0.5 cm above the
// nametag - not with the left-pocket competition pins. Levels 1 and 2 are recorded
// but carry nothing, same as ALP.
const EXPED_D = 2.54;                        // ESTIMATE, 1 in circle
const EXPEDITION = {
  none:      {label:"None"},
  lvl1:      {label:"Level 1 (nothing worn)", worn:false},
  lvl2:      {label:"Level 2 (nothing worn)", worn:false},
  regional:  {label:"Regional", art:"exped_regional"},
  national:  {label:"National / International", art:"exped_national"}
};'''))

subs.append(('''  if (F.expedition){
    put(R,{ face:"front", side:"right", slot:"front_right_expedition",
      label:"Expedition participation insignia", x:0, y: tagY + NAMETAG_H + 0.5,
      w:EXPED_D, h:EXPED_D, art:"exped", conf:"estimate",
      fdatum:"above_nametag", edge:"bottom",
      rel:{of:"the nametag", ofShort:"Nametag", gap:0.5, dir:"above"},
      cite:"CH5-B expedition figure — centred 0.5 cm over the nametag" });
  }''',
'''  const ex = EXPEDITION[F.expedition] || EXPEDITION.none;
  if (ex.art){
    put(R,{ face:"front", side:"right", slot:"front_right_expedition",
      label:`Expedition – ${ex.label}`, x:0, y: tagY + NAMETAG_H + 0.5,
      w:EXPED_D, h:EXPED_D, art:ex.art, conf:"estimate",
      fdatum:"above_nametag", edge:"bottom",
      rel:{of:"the nametag", ofShort:"Nametag", gap:0.5, dir:"above"},
      cite:"CH5-B expedition figure — over the RIGHT pocket, centred 0.5 cm over the nametag" });
    add("Expedition insignia sits over the RIGHT pocket, 0.5 cm above the nametag — not with the left-pocket competition pins. The workbook slots it out_of_scope_left_pocket, which the Chapter 5 figure supersedes.",
        "info", "CH5-B expedition figure vs D - Qual Info");
  } else if (ex.worn === false){
    add(`Expedition ${ex.label.split(" (")[0]} is recorded but nothing is worn for it. Only Regional and National carry a pin.`,
        "info", "D - Qual Info");
  }'''))

# ---- rifle team location is unconfirmed ----
subs.append(('''    if (shown.some(o => o.est))''',
'''    if (shown.some(o => o.stream.key === "rifleTeam"))
      add("National Rifle Team pin location is NOT confirmed. It is drawn on the left pocket with the competition pins because the workbook slots it there, but that has not been checked against a figure. Do not sew from this row yet.",
          "crit", "pending validation");
    if (shown.some(o => o.est))'''))

# ---- control: checkbox becomes a dropdown ----
subs.append(('''        <label class="toggle"><input type="checkbox" id="fExped"> Expedition insignia</label>
''', ""))
subs.append(('''      <div class="field"><label for="fDofe">DofE pin</label><select id="fDofe"></select></div>''',
'''      <div class="field"><label for="fDofe">DofE pin</label><select id="fDofe"></select></div>
      <div class="field"><label for="fExped">Expedition</label><select id="fExped"></select></div>
      <p style="margin:0; font-size:11px; color:var(--ink-3); line-height:1.35">Worn above the nametag on this side, not with the pocket pins.</p>'''))

subs.append(('''  fill("fNatCom", NATCOM, k => NATCOM[k]);''',
'''  fill("fNatCom", NATCOM, k => NATCOM[k]);
  fill("fExped", EXPEDITION, k => EXPEDITION[k].label);'''))

subs.append(('''    parachutist:false, commemorative:false, poppy:false,
    pins:{mkComp:"comp_mk_prov", biComp:"none", exped:"exped_regional", rifleTeam:"none"},''',
'''    parachutist:false, commemorative:false, poppy:false, expedition:"regional",
    pins:{mkComp:"comp_mk_prov", biComp:"none", rifleTeam:"none"},'''))
subs.append(('''    cadetCommend:false, navyLeague:false, dofe:"none", nationalCommend:"none",
    parachutist:false''',
'''    cadetCommend:false, navyLeague:false, dofe:"none", nationalCommend:"none",
    parachutist:false'''))

for old, new in subs:
    if old not in s:
        print("MISS:", old.strip().splitlines()[0][:70]); continue
    s = s.replace(old, new, 1)

# the old boolean default and binding
s = s.replace('anniversary:false, expedition:false,', 'anniversary:false,')
s = s.replace('fAnniv:"anniversary", fExped:"expedition",', 'fAnniv:"anniversary",')
s = s.replace('fCadetCom:"cadetCommend", fNavy:"navyLeague", fPara:"parachutist",',
              'fCadetCom:"cadetCommend", fNavy:"navyLeague", fPara:"parachutist",\n  fExped:"expedition",')

assert s != orig
open(p, "w", encoding="utf-8").write(s)
for probe in ['const EXPEDITION', 'exped:"exped_regional"', 'expedition:"regional"',
              'NOT confirmed', 'fExped:"expedition"']:
    print(("ok   " if probe in s else "gone "), probe)
