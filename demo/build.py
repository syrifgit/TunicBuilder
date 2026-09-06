"""Splice the generated art pack into the demo template -> tunic.html (publishable)."""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
tpl = open(os.path.join(here, "tunic.template.html"), encoding="utf-8").read()
art = open(os.path.join(root, "art", "art_pack.js"), encoding="utf-8").read()
if "/*__ART_PACK__*/" not in tpl:
    sys.exit("marker /*__ART_PACK__*/ missing from template")
out = tpl.replace("/*__ART_PACK__*/", art)
p = os.path.join(here, "tunic.html")
open(p, "w", encoding="utf-8").write(out)
print(f"{p}  {len(out)/1e6:.2f} MB")
