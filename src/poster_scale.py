"""Is the poster drawn to a consistent scale? Compare each badge whose real size we
already measured against its trimmed artwork size. If pt-per-cm is constant, the
unmeasured badges (RCAC sleeve badge, corps name title) can be derived rather than
guessed - which is open question 7."""
import _paths  # noqa: F401  - chdir to repo root, expose data/
import zipfile, io, sys, unicodedata, re
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
z = zipfile.ZipFile("rcac_badges.zip")
Z = {unicodedata.normalize("NFC", n): n for n in z.namelist()}
def px(slug):
    n = unicodedata.normalize("NFC", slug + ".png")
    key = Z.get(n) or next((v for k, v in Z.items()
          if re.sub(r"[^a-z0-9_]","",k.lower()) == re.sub(r"[^a-z0-9_]","",n.lower())), None)
    im = Image.open(io.BytesIO(z.read(key))).convert("RGBA")
    bb = im.getbbox(); im = im.crop(bb)
    return im.width, im.height
PT = lambda p: p / 600 * 72          # 600 dpi extraction -> PostScript points

KNOWN = [
  ("lance_corporal","LCpl chevron",10.0,None),("corporal","Cpl chevron",10.0,None),
  ("master_corporal","MCpl chevron",10.0,None),("sergeant","Sgt chevron",10.0,None),
  ("unnamed_6","WO crown",5.08,5.08),
  ("master_warrant_officer","MWO",7.62,5.08),
  ("chief_warrant_officer","CWO (est)",7.62,10.16),
  ("drum_major","Drum Major",10.0,11.0),("pipe_major","Pipe Major",10.0,11.0),
  ("green_star","Star level",2.85,2.71),
  ("marksman","Marksman assembly",5.5,7.485),
  ("distinguished_marksman","Distinguished",6.0,8.0),
  ("general_training","CTC circle",3.0,3.0),
  ("basic_expedition","CTC circle",3.0,3.0),
  ("staff_cadet","CTC circle",3.0,3.0),
  ("pipe_band","CTC circle",3.0,3.0),
  ("emergency","First aid cross",3.0,None),
  ("basic_qualification","Music circle",3.0,3.0),
]
print(f"{'slug':26} {'what':20} {'w_pt':>7} {'h_pt':>7} {'cm w':>6} {'pt/cm w':>8} {'pt/cm h':>8}")
sw, sh = [], []
for slug, what, cw, ch in KNOWN:
    w, h = px(slug); wp, hp = PT(w), PT(h)
    rw = wp / cw; sw.append((rw, what))
    rh = hp / ch if ch else None
    if rh: sh.append((rh, what))
    print(f"{slug:26} {what:20} {wp:7.1f} {hp:7.1f} {cw:6.2f} {rw:8.2f} {(f'{rh:8.2f}' if rh else '       -')}")

vals = [r for r, _ in sw] + [r for r, _ in sh]
vals.sort()
med = vals[len(vals)//2]
print(f"\nmedian pt/cm = {med:.2f}   spread {min(vals):.2f} .. {max(vals):.2f}")
print("outliers vs median (>12%):")
for r, what in sorted(sw + sh):
    if abs(r - med) / med > 0.12: print(f"   {what:22} {r:7.2f}  ({(r-med)/med*+100:+.0f}%)")

print("\nUNMEASURED - size implied if the poster scale holds:")
for slug, what in [("emblem","Generic logo (not uniform)"),("headdress_badge","Headdress badge"),
                   ("unnamed_2","unnamed_2"),("unnamed_3","unnamed_3"),
                   ("unnamed_4","unnamed_4 (wide strip)"),("unnamed_5","unnamed_5"),
                   ("da_vi_d_d_e_f_al_ar_de","item 15"),
                   ("royal_canadian_army_cadets_camp_flag","camp flag")]:
    w, h = px(slug); wp, hp = PT(w), PT(h)
    print(f"   {slug:36} {wp:7.1f} x {hp:6.1f} pt  ->  {wp/med:5.2f} x {hp/med:5.2f} cm   aspect {w/h:.3f}")
