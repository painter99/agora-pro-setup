#!/usr/bin/env python3
"""Build or verify a handoff packet manifest.

Usage:
  packet_manifest.py <paths...> [--base REV] [--json OUT] [--max-kb N]
  packet_manifest.py --check MANIFEST.json

Markdown goes to stdout; --json also writes a sidecar used by --check.
Exit codes: 0 clean, 1 drift detected, 2 input error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

IGNORED_DIRS = {
    ".git",
    ".gradle",
    ".idea",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "target",
    "venv",
}
IGNORED_FILES = {".DS_Store"}


def iter_files(paths: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in paths:
        path = Path(raw).expanduser()
        if path.is_file():
            found.append(path)
        elif path.is_dir():
            for child in sorted(path.rglob("*")):
                if not child.is_file():
                    continue
                if any(part in IGNORED_DIRS for part in child.parts):
                    continue
                if child.name in IGNORED_FILES:
                    continue
                found.append(child)
        else:
            raise FileNotFoundError(raw)
    unique = {path.resolve(): path for path in found}
    return [unique[key] for key in sorted(unique, key=lambda p: str(p))]


def describe(path: Path) -> dict:
    data = path.read_bytes()
    try:
        label = str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        label = str(path.resolve())
    return {
        "path": label,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "lines": data.count(b"\n"),
    }


def render_markdown(base: str, entries: list[dict], max_kb: int) -> str:
    total = sum(entry["bytes"] for entry in entries)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "### Manifest packetu",
        "",
        f"Base: {base or 'neuvedeno'} · Vytvořeno: {stamp} · "
        f"Souborů: {len(entries)} · Celkem: {total / 1024:.1f} kB",
        "",
        "| Soubor | SHA-256 | Bajtů | Řádků |",
        "|---|---|---|---|",
    ]
    for entry in entries:
        lines.append(
            f"| {entry['path']} | {entry['sha256'][:16]}… | {entry['bytes']} | {entry['lines']} |"
        )
    if total > max_kb * 1024:
        lines.extend(
            [
                "",
                f"Pozor: packet má {total / 1024:.1f} kB, nad limitem {max_kb} kB. "
                "Zvážit předání cest místo vloženého obsahu.",
            ]
        )
    return "\n".join(lines)


def check(manifest_path: Path) -> int:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"CHYBA  manifest nelze přečíst: {exc}", file=sys.stderr)
        return 2

    changed: list[str] = []
    missing: list[str] = []
    for entry in manifest.get("files", []):
        path = Path(entry["path"])
        if not path.is_file():
            missing.append(entry["path"])
            continue
        current = hashlib.sha256(path.read_bytes()).hexdigest()
        if current != entry["sha256"]:
            changed.append(entry["path"])

    for path in missing:
        print(f"CHYBÍ   {path}")
    for path in changed:
        print(f"ZMĚNA   {path}")
    if not missing and not changed:
        print(f"BEZ ZMĚNY  {len(manifest.get('files', []))} souborů odpovídá manifestu")
        return 0
    print(f"NESOULAD  {len(changed)} změněno, {len(missing)} chybí — packet je neplatný")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manifest packetu pro předání kontextu.")
    parser.add_argument("paths", nargs="*", help="soubory nebo složky packetu")
    parser.add_argument("--base", default="", help="revize, větev nebo jiný identifikátor snapshotu")
    parser.add_argument("--json", dest="json_out", help="zapsat JSON sidecar pro pozdější --check")
    parser.add_argument("--check", help="ověřit existující JSON manifest proti aktuálním souborům")
    parser.add_argument("--max-kb", type=int, default=200, help="limit velikosti packetu v kB")
    args = parser.parse_args(argv)

    if args.check:
        return check(Path(args.check))
    if not args.paths:
        parser.error("zadej alespoň jednu cestu, nebo použij --check")

    try:
        files = iter_files(args.paths)
    except FileNotFoundError as exc:
        print(f"CHYBA  cesta neexistuje: {exc}", file=sys.stderr)
        return 2
    if not files:
        print("CHYBA  žádné soubory nenalezeny", file=sys.stderr)
        return 2

    entries = [describe(path) for path in files]
    print(render_markdown(args.base, entries, args.max_kb))

    if args.json_out:
        payload = {
            "base": args.base,
            "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "files": entries,
            "total_bytes": sum(entry["bytes"] for entry in entries),
        }
        Path(args.json_out).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"\nJSON manifest: {args.json_out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
