#!/usr/bin/env python3
"""
Build the deployable English Trainer.

Inlines src/content.js into src/index.html and writes docs/index.html, which is
what GitHub Pages serves. Run this after any change to the app or the content:

    python3 build.py

Then commit and push; the site updates in about a minute.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"

MARKER = '<script src="content.js"></script>'


def fail(msg):
    print(f"BUILD FAILED: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    html_path = SRC / "index.html"
    content_path = SRC / "content.js"

    for p in (html_path, content_path):
        if not p.exists():
            fail(f"missing {p.relative_to(ROOT)}")

    html = html_path.read_text(encoding="utf-8")
    content = content_path.read_text(encoding="utf-8")

    if MARKER not in html:
        fail(f"{MARKER} not found in src/index.html")

    # A literal closing script tag inside the data would end the tag early and
    # silently truncate the page. Match the real thing, not a mention in a
    # comment: the browser only ends a script at "</script" followed by a
    # tag-terminating character.
    if re.search(r"</script[\s/>]", content, re.I):
        fail("content.js contains a literal closing script tag — it would truncate the bundle")

    bundle = html.replace(MARKER, "<script>\n" + content + "\n</script>")

    # Sanity checks on the produced artifact. Count only real tags at the start
    # of a line — the word "<script>" also appears inside code comments.
    if 'src="content.js"' in bundle:
        fail("external script reference survived inlining")
    opens = len(re.findall(r"(?m)^<script[ >]", bundle))
    closes = len(re.findall(r"(?m)^</script>", bundle))
    if opens != closes:
        fail(f"unbalanced script tags in output ({opens} open, {closes} close)")

    n_phrases = len(re.findall(r"\n  \{ id: \"", content))
    n_lessons = len(re.findall(r"\{ id: \d+,\s+title:", content))
    if n_phrases == 0:
        fail("no phrases found in content.js — refusing to publish an empty app")

    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(bundle, encoding="utf-8")
    # Tell GitHub Pages not to run Jekyll over these files.
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    kb = len(bundle.encode("utf-8")) / 1024
    print(f"✓ docs/index.html  ({kb:.0f} KB)")
    print(f"  {n_phrases} phrases · {n_lessons} lessons")
    print("\nNext: git add -A && git commit -m 'Update' && git push")


if __name__ == "__main__":
    main()
