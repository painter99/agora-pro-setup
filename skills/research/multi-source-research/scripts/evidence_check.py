#!/usr/bin/env python3
"""Validate a research evidence file and render its evidence matrix.

Input: JSONL, one claim per line. See references/evidence-matrix.md for the schema.
Exit codes: 0 gate passed, 1 gate failed, 2 input unreadable or unparsable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

CLAIM_TYPES = {"fact", "calculation", "estimate", "assumption", "interpretation", "recommendation"}
PROVENANCE = {
    "PRIMARY_DIRECT",
    "OFFICIAL_AGGREGATE",
    "MODEL_OUTPUT",
    "DERIVED_INTERPOLATED",
    "CROWDSOURCED",
    "VENDOR_CLAIM",
    "SECONDARY_REPORT",
    "UNKNOWN",
}
PROVENANCE_ALIASES = {
    "DIRECT_STATION": "PRIMARY_DIRECT",
    "OFFICIAL_NETWORK": "OFFICIAL_AGGREGATE",
    "INTERPOLATED": "DERIVED_INTERPOLATED",
}
EVIDENCE_LEVELS = {"yes", "partial", "no"}
INDEPENDENCE = {"yes", "no", "n/a"}
STATUSES = {"verified", "limited", "disputed", "single-source", "unverified", "insufficient"}
STATUS_ALIASES = {
    "verified": "verified",
    "limited": "limited",
    "limited evidence": "limited",
    "disputed": "disputed",
    "single-source": "single-source",
    "single source": "single-source",
    "single-source — limited confidence": "single-source",
    "single-source - limited confidence": "single-source",
    "unverified": "unverified",
    "insufficient": "insufficient",
    "insufficient access": "insufficient",
}
SOFT_PROVENANCE = {"MODEL_OUTPUT", "DERIVED_INTERPOLATED", "CROWDSOURCED"}
SUPERLATIVES = re.compile(
    r"\b(best|fastest|slowest|most accurate|most reliable|most secure|most popular|"
    r"cheapest|safest|leading|superior|unmatched|number one|#1|world's best|"
    r"highest|lowest|greatest)\b",
    re.IGNORECASE,
)
MATRIX_COLUMNS = [
    "Claim",
    "Type",
    "Source",
    "Provenance",
    "Evidence",
    "Observed",
    "Accessed",
    "Published",
    "Independent",
    "Status",
]
EXAMPLE = {
    "claim": "Library X 4.2 requires Python 3.11 or newer",
    "type": "fact",
    "source": "Library X changelog",
    "url": "https://example.com/changelog",
    "provenance": "PRIMARY_DIRECT",
    "evidence": "yes",
    "observed": "2026-10-02",
    "accessed": "2026-11-15",
    "published": "2026-09-28",
    "independent": "yes",
    "status": "verified",
}


def norm(value) -> str:
    return str(value).strip() if value is not None else ""


def parse_date(value: str):
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def normalize_status(value: str):
    return STATUS_ALIASES.get(value.lower())


def normalize_provenance(value: str):
    key = value.upper().replace(" ", "_").replace("-", "_")
    key = PROVENANCE_ALIASES.get(key, key)
    return key if key in PROVENANCE else None


class Row:
    def __init__(self, number: int, raw: dict):
        self.number = number
        self.raw = {norm(k).lower(): v for k, v in raw.items()}
        self.errors: list[tuple[str, str]] = []
        self.warnings: list[tuple[str, str]] = []

        self.claim = norm(self.raw.get("claim"))
        self.type = norm(self.raw.get("type")).lower()
        self.source = norm(self.raw.get("source"))
        self.url = norm(self.raw.get("url"))
        self.provenance_raw = norm(self.raw.get("provenance"))
        self.provenance = normalize_provenance(self.provenance_raw)
        self.evidence = norm(self.raw.get("evidence")).lower()
        self.independent = norm(self.raw.get("independent")).lower()
        self.status_raw = norm(self.raw.get("status"))
        self.status = normalize_status(self.status_raw)
        self.metric = norm(self.raw.get("metric"))
        self.wording = norm(self.raw.get("wording"))
        self.justification = norm(self.raw.get("single_source_justification"))
        self.observed = norm(self.raw.get("observed"))
        self.accessed = norm(self.raw.get("accessed"))
        self.published = norm(self.raw.get("published"))

    def validate(self, stale_days: int) -> None:
        e, w = self.errors, self.warnings

        if not self.claim:
            e.append(("claim", "missing claim text"))
        elif len(self.claim) > 220:
            w.append(("claim", "long claim; split into atomic assertions"))

        if not self.type:
            e.append(("type", "missing claim type"))
        elif self.type not in CLAIM_TYPES:
            e.append(("type", f"unknown type {self.type!r}; expected one of {sorted(CLAIM_TYPES)}"))

        if not self.source:
            e.append(("source", "missing source name"))
        if not self.url:
            w.append(("url", "no URL recorded"))

        if not self.provenance_raw:
            e.append(("provenance", "missing provenance class"))
        elif self.provenance is None:
            e.append(("provenance", f"unknown class {self.provenance_raw!r}; expected one of {sorted(PROVENANCE)}"))

        if not self.evidence:
            e.append(("evidence", "missing evidence flag (yes/partial/no)"))
        elif self.evidence not in EVIDENCE_LEVELS:
            e.append(("evidence", f"invalid evidence flag {self.evidence!r}"))

        if self.independent and self.independent not in INDEPENDENCE:
            e.append(("independent", f"invalid value {self.independent!r}; expected yes/no/n/a"))
        elif self.status == "verified" and not self.independent:
            w.append(("independent", "verified claim does not state whether it was independently checked"))

        if not self.status_raw:
            e.append(("status", "missing status"))
        elif self.status is None:
            e.append(("status", f"unknown status {self.status_raw!r}"))

        for field in ("observed", "accessed", "published"):
            value = getattr(self, field)
            if value and parse_date(value) is None:
                e.append((field, f"invalid date {value!r}; expected YYYY-MM-DD"))

        if self.status == "verified":
            if self.evidence and self.evidence != "yes":
                e.append(("status", "verified requires direct evidence (evidence=yes)"))
            if self.independent == "no" and not self.justification:
                e.append(("status", "verified with independent=no needs single_source_justification"))
            if self.type in {"interpretation", "recommendation", "assumption"}:
                e.append(("status", f"a {self.type} cannot be verified; use limited or unverified"))
            if self.provenance in {"VENDOR_CLAIM", "UNKNOWN"}:
                e.append(("status", f"{self.provenance} cannot support a verified claim"))
            if self.provenance in SOFT_PROVENANCE:
                w.append(("status", f"{self.provenance} verified only as 'the source states X', not as measurement"))
            if self.published:
                published = parse_date(self.published)
                if published and (date.today() - published).days > stale_days:
                    w.append(("published", f"published {(date.today() - published).days} days ago; confirm still current"))

        if self.provenance in {"PRIMARY_DIRECT", "OFFICIAL_AGGREGATE"} and self.type in {"fact", "estimate"}:
            if not self.observed:
                w.append(("observed", "measurement time missing for a time-sensitive claim"))

        text = f"{self.claim} {self.wording}"
        if SUPERLATIVES.search(text) and not self.metric:
            if self.status in {"verified", "limited"}:
                e.append(("claim", "superlative without a named metric and comparison"))
            else:
                w.append(("claim", "superlative without a named metric"))

    @property
    def display_status(self) -> str:
        return self.status or (self.status_raw or "?").lower()

    def cell(self, column: str) -> str:
        values = {
            "Claim": self.claim,
            "Type": self.type,
            "Source": self.source,
            "Provenance": self.provenance or self.provenance_raw,
            "Evidence": self.evidence,
            "Observed": self.observed,
            "Accessed": self.accessed,
            "Published": self.published,
            "Independent": self.independent,
            "Status": self.display_status,
        }
        return str(values[column]).replace("|", "\\|").replace("\n", " ")


def load_rows(path: Path) -> tuple[list[Row], list[str]]:
    rows: list[Row] = []
    parse_errors: list[str] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as exc:
            parse_errors.append(f"line {number}: invalid JSON ({exc.msg})")
            continue
        if not isinstance(payload, dict):
            parse_errors.append(f"line {number}: expected a JSON object")
            continue
        rows.append(Row(number, payload))
    return rows, parse_errors


def render_matrix(rows: list[Row]) -> str:
    header = "| " + " | ".join(MATRIX_COLUMNS) + " |"
    divider = "|" + "|".join(["---"] * len(MATRIX_COLUMNS)) + "|"
    lines = [header, divider]
    for row in rows:
        lines.append("| " + " | ".join(row.cell(column) for column in MATRIX_COLUMNS) + " |")
    return "\n".join(lines)


def render_report(rows: list[Row], parse_errors: list[str], strict: bool) -> tuple[str, bool]:
    errors = [(row.number, field, message) for row in rows for field, message in row.errors]
    warnings = [(row.number, field, message) for row in rows for field, message in row.warnings]
    failed = bool(errors) or bool(parse_errors) or (strict and bool(warnings))

    lines: list[str] = []
    lines.append(f"Claims: {len(rows)} · Errors: {len(errors) + len(parse_errors)} · Warnings: {len(warnings)}")
    for message in parse_errors:
        lines.append(f"ERROR  {message}")
    for number, field, message in errors:
        lines.append(f"ERROR  line {number} [{field}] {message}")
    for number, field, message in warnings:
        lines.append(f"WARN   line {number} [{field}] {message}")

    status_counts: dict[str, int] = {}
    for row in rows:
        if not row.errors:
            status_counts[row.display_status] = status_counts.get(row.display_status, 0) + 1
    if status_counts:
        summary = ", ".join(f"{key} {value}" for key, value in sorted(status_counts.items()))
        lines.append(f"Status mix (rows without errors): {summary}")
    lines.append(f"GATE: {'FAIL' if failed else 'PASS'}" + (" (strict)" if strict else ""))
    return "\n".join(lines), not failed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a research evidence file and render its matrix.")
    parser.add_argument("path", nargs="?", help="JSONL evidence file")
    parser.add_argument("--matrix-only", action="store_true", help="print only the Markdown matrix")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--json", action="store_true", help="emit a JSON summary instead of text")
    parser.add_argument("--stale-days", type=int, default=365, help="freshness threshold for verified claims")
    parser.add_argument("--example", action="store_true", help="print one valid JSONL line and exit")
    args = parser.parse_args(argv)

    if args.example:
        print(json.dumps(EXAMPLE, ensure_ascii=False))
        return 0
    if not args.path:
        parser.error("path is required unless --example is used")

    path = Path(args.path)
    if not path.is_file():
        print(f"ERROR  cannot read {path}", file=sys.stderr)
        return 2

    rows, parse_errors = load_rows(path)
    if not rows and not parse_errors:
        print(f"ERROR  no claims found in {path}", file=sys.stderr)
        return 2

    for row in rows:
        row.validate(args.stale_days)

    if args.matrix_only:
        print(render_matrix(rows))
        return 0

    report, passed = render_report(rows, parse_errors, args.strict)
    if args.json:
        payload = {
            "claims": len(rows),
            "errors": [{"line": r.number, "field": f, "message": m} for r in rows for f, m in r.errors],
            "warnings": [{"line": r.number, "field": f, "message": m} for r in rows for f, m in r.warnings],
            "parse_errors": parse_errors,
            "passed": passed,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(report)
        print()
        print(render_matrix(rows))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
