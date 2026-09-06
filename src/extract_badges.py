import _paths  # noqa: F401  - chdir to repo root, expose data/
#!/usr/bin/env python3
"""
Extract every badge from A-CR-CCP-750/DA-003 (Symbols of the Royal Canadian Army Cadets)
as vector SVG plus a high-resolution PNG fallback.

The poster is Illustrator vector art (58k drawing objects, 18 rasters), so almost
every badge comes out resolution-independent. The 18 rasters are the medals and
banners, which are photographs and will extract as PNG only.

Method: cluster the page's vector objects into connected components, discard the
background panels and rules, then name each cluster from the caption directly
beneath it.

Usage:  python3 extract_badges.py poster.pdf out_dir
Output: out_dir/<slug>.svg, out_dir/<slug>.png, out_dir/manifest.csv
"""

import sys, os, csv, re, subprocess
import pymupdf

MIN_AREA      = 400     # pt^2, drops hairlines and stray anchor points
MAX_AREA      = 90000   # pt^2, drops full-width background panels
MERGE_GAP     = 6       # pt, objects closer than this join the same badge
CAPTION_BAND  = 60      # pt, how far below a badge to look for its caption
PNG_DPI       = 600


LIGATURES = {"\ufb00":"ff","\ufb01":"fi","\ufb02":"fl","\ufb03":"ffi","\ufb04":"ffl",
             "\u2019":"'", "\u2013":"-", "\u2014":"-"}

def slug(s):
    for k, v in LIGATURES.items():
        s = s.replace(k, v)
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    return re.sub(r"[\s_-]+", "_", s)[:60] or "unnamed"


def cluster(rects, gap):
    """Union-find over rects that overlap once inflated by `gap`."""
    parent = list(range(len(rects)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    infl = [pymupdf.Rect(r.x0 - gap, r.y0 - gap, r.x1 + gap, r.y1 + gap) for r in rects]
    # bucket by coarse grid so this stays near-linear instead of O(n^2)
    grid = {}
    for i, r in enumerate(infl):
        for gx in range(int(r.x0 // 50), int(r.x1 // 50) + 1):
            for gy in range(int(r.y0 // 50), int(r.y1 // 50) + 1):
                grid.setdefault((gx, gy), []).append(i)
    for cell in grid.values():
        for a in range(len(cell)):
            for b in range(a + 1, len(cell)):
                i, j = cell[a], cell[b]
                if infl[i].intersects(infl[j]):
                    union(i, j)

    groups = {}
    for i in range(len(rects)):
        groups.setdefault(find(i), []).append(rects[i])
    out = []
    for g in groups.values():
        u = g[0]
        for r in g[1:]:
            u = u | r
        out.append(u)
    return out


def caption_for(box, words, band):
    """Words sitting just under the badge, within its horizontal span."""
    lo, hi = box.y1, box.y1 + band
    near = [w for w in words
            if lo <= w[1] <= hi and w[0] < box.x1 + 12 and w[2] > box.x0 - 12]
    if not near:
        return ""
    top_line = min(w[1] for w in near)
    line = [w for w in near if abs(w[1] - top_line) < 6]
    return " ".join(w[4] for w in sorted(line, key=lambda w: w[0]))


def main(pdf_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    src = pymupdf.open(pdf_path)
    page = src[0]

    rects = [d["rect"] for d in page.get_drawings()
             if MIN_AREA < d["rect"].get_area() < MAX_AREA]
    boxes = [b for b in cluster(rects, MERGE_GAP)
             if MIN_AREA < b.get_area() < MAX_AREA
             and 12 < b.width < 400 and 12 < b.height < 400]
    boxes.sort(key=lambda b: (round(b.y0 / 20), b.x0))

    words = page.get_text("words")
    seen, manifest = {}, []

    for box in boxes:
        cap = caption_for(box, words, CAPTION_BAND)
        for k, v in LIGATURES.items():
            cap = cap.replace(k, v)
        name = slug(cap)
        seen[name] = seen.get(name, 0) + 1
        if seen[name] > 1:
            name = f"{name}_{seen[name]}"

        pad = pymupdf.Rect(box.x0 - 3, box.y0 - 3, box.x1 + 3, box.y1 + 3) & page.rect

        # vector export: crop a copy of the page, then let poppler emit SVG
        tmp = os.path.join(out_dir, f".{name}.pdf")
        d = pymupdf.open()
        d.insert_pdf(src)
        d[0].set_cropbox(pad)
        d.save(tmp, garbage=4, deflate=True, clean=True)
        d.close()
        svg = os.path.join(out_dir, f"{name}.svg")
        subprocess.run(["pdftocairo", "-svg", tmp, svg],
                       stderr=subprocess.DEVNULL, check=False)
        os.remove(tmp)

        png = os.path.join(out_dir, f"{name}.png")
        page.get_pixmap(clip=pad, dpi=PNG_DPI, alpha=True).save(png)

        manifest.append({
            "slug": name,
            "caption": cap,
            "x_pt": round(pad.x0, 1), "y_pt": round(pad.y0, 1),
            "w_pt": round(pad.width, 1), "h_pt": round(pad.height, 1),
            "aspect": round(pad.width / pad.height, 3),
            "svg": os.path.basename(svg) if os.path.exists(svg) else "",
            "png": os.path.basename(png),
            "qual_type": "", "qual_category": "", "qualification_name": "", "slot": "",
        })

    with open(os.path.join(out_dir, "data/manifest.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
        w.writeheader()
        w.writerows(manifest)

    print(f"{len(manifest)} badges -> {out_dir}")
    print("Blank columns in manifest.csv are for you to map onto QualMap.")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "badges_out")
