"""Splice the plate art pack into the plate template -> plate.html (publishable)."""
import os, sys
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
tpl = open(os.path.join(here,"plate.template.html"), encoding="utf-8").read()
art = open(os.path.join(root,"art","plate_pack.js"), encoding="utf-8").read()
if "/*__PLATE_PACK__*/" not in tpl: sys.exit("marker missing")
out = tpl.replace("/*__PLATE_PACK__*/", art)
p = os.path.join(here,"plate.html"); open(p,"w",encoding="utf-8").write(out)
print(f"{p}  {len(out)/1e6:.2f} MB")
