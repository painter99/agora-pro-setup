#!/usr/bin/env python3
"""Check that relative Markdown links resolve to existing files.

Links inside code fences are ignored. Links that point outside the
repository (for example GitHub UI paths like ../../issues) are skipped,
because their existence cannot be verified from a checkout.
"""
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def strip_fences(text):
    out, fence = [], None
    for line in text.splitlines():
        stripped = line.strip()
        if fence is None:
            if stripped.startswith("```") or stripped.startswith("~~~"):
                fence = stripped[:3]
                continue
            out.append(line)
        elif stripped.startswith(fence):
            fence = None
    return "\n".join(out)


def main():
    root = Path(__file__).resolve().parent.parent
    broken = 0
    checked = 0
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = strip_fences(path.read_text(encoding="utf-8"))
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            resolved = (path.parent / file_part).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                continue
            checked += 1
            if not resolved.exists():
                broken += 1
                print(
                    "BROKEN " + str(path.relative_to(root)) + " -> " + target
                )
    print()
    print(str(checked) + " relative links checked, " + str(broken) + " broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())