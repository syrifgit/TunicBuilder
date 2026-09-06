"""Every script in src/ runs relative to the repo root, not to src/.

Import this first and it puts you there, and makes data/ importable so
`from labels import LABELS` keeps working.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
RULES = os.path.join(ROOT, "rules", "army_tunic_placement_rules_2.json")
ART = os.path.join(ROOT, "art")
RECUT = os.path.join(ART, "recut")

if DATA not in sys.path:
    sys.path.insert(0, DATA)
os.chdir(ROOT)
