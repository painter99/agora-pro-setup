#!/usr/bin/env python3
"""Check that every Skill file follows skills/skill-format.md.

Required: a '# Skill: <name>' title and the 10 required '##' sections in the
documented order. Content inside code fences is ignored, so example skeletons
inside a Skill do not affect the check.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Catalog description",
    "Purpose",
    "Load when",
    "Do not load when",
    "Dependencies",
    "Workflow",
    "Forbidden behavior",
    "Verification",
    "Output contract",
]

# Documentation about skills, not skills themselves.
EXCLUDED = {"README.md", "skill-format.md", "skill-catalog.md"}


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


def check_file(path):
    text = strip_fences(path.read_text(encoding="utf-8"))
    errors = []
    if not re.search(r"^# Skill: \S", text, re.M):
        errors.append("missing '# Skill: <name>' title")
    found = []
    for section in REQUIRED:
        match = re.search(r"^## " + re.escape(section) + r"\s*$", text, re.M)
        if match:
            found.append((match.start(), section))
        else:
            errors.append("missing section '## " + section + "'")
    ordered = [name for _, name in sorted(found)]
    expected = [name for name in REQUIRED if any(name == n for _, n in found)]
    if ordered != expected:
        errors.append("sections out of order: " + ", ".join(ordered))
    return errors


def main():
    root = Path(__file__).resolve().parent.parent
    files = sorted(
        p for p in (root / "skills").rglob("*.md") if p.name not in EXCLUDED
    )
    if not files:
        print("FAIL: no skill files found")
        return 1
    failures = 0
    for path in files:
        errors = check_file(path)
        rel = path.relative_to(root)
        if errors:
            failures += 1
            print("FAIL " + str(rel))
            for error in errors:
                print("  - " + error)
        else:
            print("PASS " + str(rel))
    print()
    print(str(len(files) - failures) + "/" + str(len(files)) + " skill files pass format check")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())