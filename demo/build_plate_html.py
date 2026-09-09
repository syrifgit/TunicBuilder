"""Splice the plate art pack into the template and write two files.

  plate.html        artifact-shaped: page content only. The Artifact tool supplies the
                    document skeleton at publish time.
  plate.local.html  a complete standalone document, for opening locally or serving.

See demo/build.py for why the second one exists.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SKELETON = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>html{color-scheme:light dark}body{margin:0;font:14px system-ui,sans-serif}
img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
{content}
</body>
</html>
"""


def main():
    tpl = open(os.path.join(HERE, "plate.template.html"), encoding="utf-8").read()
    art = open(os.path.join(ROOT, "art", "plate_pack.js"), encoding="utf-8").read()
    if "/*__PLATE_PACK__*/" not in tpl:
        sys.exit("marker /*__PLATE_PACK__*/ missing from template")
    body = tpl.replace("/*__PLATE_PACK__*/", art)

    # Local build keeps the artwork in a sibling file. See demo/build.py for why.
    ART_FILE = "plate_art.js"
    block = "<script>\n/*__PLATE_PACK__*/\n</script>"
    if block not in tpl:
        sys.exit("the art <script> block is not where build_plate_html.py expects it")
    external = tpl.replace(block, f'<script src="{ART_FILE}"></script>')
    open(os.path.join(HERE, ART_FILE), "w", encoding="utf-8").write(art)

    for name, text in [("plate.html", body),                                   # artifact
                       ("plate.local.html", SKELETON.replace("{content}", external))]:
        p = os.path.join(HERE, name)
        open(p, "w", encoding="utf-8").write(text)
        print(f"{p}  {len(text)/1e6:.2f} MB")
    print(f"{os.path.join(HERE, ART_FILE)}  {len(art)/1e6:.2f} MB  (artwork)")


if __name__ == "__main__":
    main()
