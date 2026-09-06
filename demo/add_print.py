"""Print-friendly output: white paper, letter proportions, no screen chrome.

Two things, sharing one set of tokens:
  - `body.paper` previews it on screen inside a letter-landscape box
  - `@media print` applies the same thing for real, and hides the controls

The sleeve fill goes from rifle green to a pale tint in paper mode. The badges carry
their own dark green grounds, so they still read, and it saves a page of toner.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
p = "tunic.template.html"
s = open(p, encoding="utf-8").read()
orig = s
subs = []

PAPER_TOKENS = """
/* ---------- paper: shared by the on-screen preview and real printing ---------- */
body.paper{
  --paper:#FFFFFF; --sheet:#FFFFFF; --card:#FFFFFF; --plate:#FFFFFF;
  --ink:#111111; --ink-2:#3A3A3A; --ink-3:#6A6A6A;
  --rule:#B8B8B8; --rule-2:#DCDCDC;
  --green:#0F4A32; --green-soft:#FFFFFF;
  --brass:#7A5A0C; --brass-soft:#FFFFFF;
  --warn:#7A4208; --warn-soft:#FFFFFF;
  --crit:#8A1F22; --crit-soft:#FFFFFF;
  --ok:#1F5136; --ok-soft:#FFFFFF;
  --cloth:#EEF2EC; --cloth-edge:#5E6E63;
  --shadow:none;
}
body.paper .rail,
body.paper .masthead .stamp,
body.paper #zIn, body.paper #zOut, body.paper #zFit, body.paper #zOne,
body.paper .zoombar .pct, body.paper .zoombar .hint{ display:none }
body.paper .shell{ grid-template-columns:1fr }
body.paper .sheetwrap{ box-shadow:none }
/* the drawing sits on a letter landscape page and is fitted to it */
body.paper .viewport{
  overflow:hidden; max-height:none; aspect-ratio:11/8.5; padding:10px;
  display:grid; place-items:center; cursor:default;
}
body.paper .viewport svg{
  width:auto !important; height:auto !important; max-width:100%; max-height:100%;
}

@media print{
  :root{
    --paper:#FFFFFF; --sheet:#FFFFFF; --card:#FFFFFF; --plate:#FFFFFF;
    --ink:#111111; --ink-2:#3A3A3A; --ink-3:#6A6A6A;
    --rule:#B8B8B8; --rule-2:#DCDCDC;
    --green:#0F4A32; --green-soft:#FFFFFF;
    --brass:#7A5A0C; --brass-soft:#FFFFFF;
    --warn:#7A4208; --warn-soft:#FFFFFF;
    --crit:#8A1F22; --crit-soft:#FFFFFF;
    --ok:#1F5136; --ok-soft:#FFFFFF;
    --cloth:#EEF2EC; --cloth-edge:#5E6E63;
    --shadow:none;
  }
  @page{ size:letter landscape; margin:12mm }
  html,body{ background:#fff !important }
  .rail, .zoombar, .masthead .stamp, footer.foot .noprint{ display:none !important }
  .shell{ display:block }
  .stage{ padding:0; gap:12px }
  .sheetwrap{ border:none; box-shadow:none }
  .viewport{ overflow:visible !important; max-height:none !important; padding:0 }
  .viewport svg{ width:100% !important; height:auto !important; max-width:100% }
  /* one page for the drawing, then the guide */
  .sheetwrap{ break-after:page; page-break-after:always }
  .panel{ break-inside:auto }
  thead{ display:table-header-group }
  tr, .finding{ break-inside:avoid; page-break-inside:avoid }
  a[href]::after{ content:"" }
  .legend{ font-size:10px }
  body{ font-size:11px }
  td, th{ padding:3px 8px }
}
"""
subs.append(("@media (prefers-reduced-motion:reduce){*{transition:none!important; animation:none!important}}",
             PAPER_TOKENS + "\n@media (prefers-reduced-motion:reduce){*{transition:none!important; animation:none!important}}"))

subs.append(('''        <span class="hint">Pinch to zoom, drag to pan. Ctrl + scroll also zooms.</span>''',
'''        <span class="hint">Pinch to zoom, drag to pan. Ctrl + scroll also zooms.</span>
        <span style="flex:1 1 auto"></span>
        <button type="button" id="zPaper" aria-pressed="false">Paper</button>
        <button type="button" id="zPrint">Print</button>'''))

subs.append(('''  let rt;
  window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(refresh, 150); });
  return {refresh};''',
'''  // Paper mode previews the printed page: white ground, letter landscape, no chrome.
  // The SVG is handed back to CSS so it fits the page box instead of being sized in px.
  const paperBtn = document.getElementById("zPaper");
  function setPaper(on){
    document.body.classList.toggle("paper", on);
    paperBtn.setAttribute("aria-pressed", on ? "true" : "false");
    if (on){ svg.style.width = ""; svg.style.height = ""; }
    else fit();
  }
  paperBtn.addEventListener("click", () => setPaper(!document.body.classList.contains("paper")));
  document.getElementById("zPrint").addEventListener("click", () => window.print());

  let rt;
  window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(refresh, 150); });
  return {refresh: () => { if (!document.body.classList.contains("paper")) refresh(); }};''',))

for old, new in subs:
    if old not in s:
        print("MISS:", old.strip().splitlines()[0][:70]); continue
    s = s.replace(old, new, 1)

# refresh() is now wrapped, so rename the inner one to avoid shadowing confusion
s = s.replace("  function refresh(){ if (scale === null || !userSet) fit(); else apply(false); }",
              "  function refresh(){ if (scale === null || !userSet) fit(); else apply(false); }")

assert s != orig
open(p, "w", encoding="utf-8").write(s)
for probe in ["body.paper", "@media print", "zPaper", "zPrint", "size:letter landscape"]:
    print(("ok   " if probe in s else "MISS "), probe)
