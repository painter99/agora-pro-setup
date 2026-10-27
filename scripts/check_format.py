#!/usr/bin/env python3
"""Check that every Skill follows skills/skill-format.md and the Agent
Skills (SKILL.md) layout.

A Skill is a directory skills/**/<skill-name>/ containing a SKILL.md file
with YAML frontmatter (name, description, license) and a Markdown body
carrying the 10 required sections in the documented order. Frontmatter
follows the Agent Skills specification (https://agentskills.io/specification.md).
Content inside code fences is ignored, so example skeletons inside a Skill
do not affect the check.
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

# Documentation about skills, not skills themselves (live at skills/ root).
AUTHOR_DOCS = {"README.md", "skill-format.md", "skill-catalog.md"}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


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


def parse_frontmatter(text):
    """Minimal parser for flat scalar frontmatter (no external YAML dep)."""
    if not text.startswith("---"):
        return None, "missing YAML frontmatter block"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "unterminated YAML frontmatter block"
    fields = {}
    for line in text[3:end].splitlines():
        if not line.strip():
            continue
        if line[:1].isspace():
            return None, "unexpected nested key in frontmatter: " + line.strip()
        m = re.match(r"^([A-Za-z-]+):\s*(.*)$", line)
        if not m:
            return None, "unparsable frontmatter line: " + line.strip()
        value = m.group(2).strip()
        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            value = value[1:-1].replace('\\"', '"')
        fields[m.group(1)] = value
    return fields, None


def catalog_description(text):
    m = re.search(r"^## Catalog description\s*\n(.*?)(?=^## )", text, re.S | re.M)
    return " ".join(m.group(1).split()) if m else None


def check_file(path):
    raw = path.read_text(encoding="utf-8")
    errors = []
    if len(raw.splitlines()) > 500:
        errors.append("SKILL.md exceeds 500 lines")
    text = strip_fences(raw)
    fields, fm_error = parse_frontmatter(text)
    if fm_error:
        errors.append(fm_error)
        fields = {}
    skill_name = path.parent.name
    name = fields.get("name")
    if not name:
        errors.append("frontmatter missing 'name'")
    elif not NAME_RE.match(name):
        errors.append("frontmatter 'name' violates Agent Skills naming rules")
    elif name != skill_name:
        errors.append(
            "frontmatter 'name' does not match directory '" + skill_name + "'"
        )
    description = fields.get("description")
    if not description:
        errors.append("frontmatter missing 'description'")
    elif len(description) > 1024:
        errors.append("frontmatter 'description' exceeds 1024 characters")
    if fields.get("license") != "MIT":
        errors.append("frontmatter missing 'license: MIT'")
    catalog = catalog_description(text)
    if catalog is None:
        errors.append("missing section '## Catalog description'")
    elif description and catalog and description != catalog:
        errors.append("frontmatter 'description' differs from '## Catalog description'")
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
    skills = root / "skills"
    files = sorted(skills.rglob("SKILL.md"))
    strays = sorted(
        p
        for p in skills.rglob("*.md")
        if p.name != "SKILL.md" and p.name not in AUTHOR_DOCS
    )
    if not files:
        print("FAIL: no SKILL.md files found")
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
    for path in strays:
        failures += 1
        print("FAIL " + str(path.relative_to(root)) + " (stray Markdown file; Skills live in <dir>/SKILL.md)")
    print()
    print(
        str(len(files) - failures)
        + "/"
        + str(len(files))
        + " skill files pass format check"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())