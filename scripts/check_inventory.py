#!/usr/bin/env python3
"""Validate manifest.yaml against the actual repository tree.

The manifest is the component inventory and drift anchor (ADR-0007). This
checker parses the manifest without a YAML dependency and verifies that

- the meta block carries an integer inventory_version and a YYYY-MM-DD
  last_verified date,
- every component has name, kind, source, and target, and names are unique,
- every source resolves:
    * an exact file path must exist,
    * a directory source (trailing "/") must exist and be non-empty,
    * a glob source must carry a "files" count matching the actual number of
      matching files.

An unrecognized source pattern is a failure, not a skip: the inventory must
stay machine-checkable. (A prose count inside a source string is exactly what
drifted before this check existed.)
"""
import glob
import re
import sys
from pathlib import Path


def parse_manifest(text):
    """Line-based parse of the flat manifest structure."""
    meta = {}
    components = []
    current = None
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            current = {}
            components.append(current)
            stripped = stripped[2:]
        elif stripped == "components:":
            continue
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip().strip('"')
        if current is None:
            meta[key] = value
        else:
            current[key] = value
    return meta, components


def main():
    root = Path(__file__).resolve().parent.parent
    meta, components = parse_manifest(
        (root / "manifest.yaml").read_text(encoding="utf-8")
    )
    problems = []

    if not meta.get("inventory_version", "").isdigit():
        problems.append("meta.inventory_version missing or not an integer")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", meta.get("last_verified", "")):
        problems.append("meta.last_verified missing or not a YYYY-MM-DD date")

    names = set()
    for comp in components:
        name = comp.get("name", "<unnamed>")
        if name in names:
            problems.append("duplicate component name: " + name)
        names.add(name)
        for field in ("kind", "source", "target"):
            if not comp.get(field):
                problems.append(name + ": missing '" + field + "'")
        source = comp.get("source", "")
        if not source:
            continue
        if any(ch in source for ch in "*?[]"):
            expected = comp.get("files", "")
            if not expected.isdigit():
                problems.append(
                    name
                    + ": glob source without a machine-checkable 'files' count: "
                    + source
                )
                continue
            pattern = str(root / source)
            actual = len(
                [p for p in glob.glob(pattern, recursive=True) if Path(p).is_file()]
            )
            if actual != int(expected):
                problems.append(
                    name
                    + ": manifest expects "
                    + expected
                    + " files for '"
                    + source
                    + "', found "
                    + str(actual)
                )
        elif source.endswith("/"):
            directory = root / source
            if not directory.is_dir() or not any(directory.iterdir()):
                problems.append(name + ": directory source missing or empty: " + source)
        else:
            if not (root / source).is_file():
                problems.append(name + ": source file missing: " + source)

    if problems:
        for problem in problems:
            print("INVENTORY PROBLEM: " + problem)
        print(str(len(components)) + " components parsed")
        return 1
    print("INVENTORY OK: " + str(len(components)) + " components, all sources resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())