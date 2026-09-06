"""Splice the generated art pack into the template and write two files.

  tunic.html        artifact-shaped: page content only, no doctype/html/head/body.
                    The Artifact tool supplies that skeleton at publish time, so
                    adding our own here would double-wrap it.
  tunic.local.html  a complete standalone document, for opening locally or serving.

The second one exists because a fragment is not a valid document. Browsers cope, but
tooling that rewrites HTML does not: Live Server injects its live-reload client by
looking for </body>, and with no </body> to find it lands somewhere unhelpful and the
page's own scripts stop running. Open the .local.html file for local work.
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
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><text y='14' font-size='14'>%F0%9F%8E%96</text></svg>">
<style>html{color-scheme:light dark}body{margin:0;font:14px system-ui,sans-serif}
img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
{content}
</body>
</html>
"""


def main():
    tpl = open(os.path.join(HERE, "tunic.template.html"), encoding="utf-8").read()
    art = open(os.path.join(ROOT, "art", "art_pack.js"), encoding="utf-8").read()
    if "/*__ART_PACK__*/" not in tpl:
        sys.exit("marker /*__ART_PACK__*/ missing from template")
    body = tpl.replace("/*__ART_PACK__*/", art)

    for name, text in [("tunic.html", body),
                       ("tunic.local.html", SKELETON.replace("{content}", body))]:
        p = os.path.join(HERE, name)
        open(p, "w", encoding="utf-8").write(text)
        print(f"{p}  {len(text)/1e6:.2f} MB")


if __name__ == "__main__":
    main()
