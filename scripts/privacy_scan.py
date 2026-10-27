#!/usr/bin/env python3
"""Scan all repository Markdown, YAML, and systemd-unit files for
personal-identifier patterns.

The repository must stay English, anonymized, and generic. This scan is a
net, not a judge: every finding needs human review before content is pushed
to the public repository.

Intentionally not flagged (documented allowlist):
- the repository owner's public GitHub handle in self-referential URLs —
  standard open-source practice, public by construction;
- /home/agora — the app-derived example username used consistently in the
  repository's command examples;
- RFC 5737 documentation IP ranges, loopback, and unspecified addresses —
  reserved for examples.
"""
import re
import sys
from pathlib import Path

PATTERNS = {
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+"),
    "phone_intl": re.compile(r"\+\d{1,3}[\s-]?\d{3}[\s-]?\d{3,4}(?:[\s-]?\d{3,4})?"),
    "ipv4": re.compile(
        r"\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b"
    ),
    "home_path": re.compile(r"/home/[A-Za-z0-9_.-]+"),
    "czech_family_term": re.compile(
        r"\b(?:dcera|dcer[aeou]|syn[au]?|manžel\w*|rodin\w*|zasnouben\w*"
        r"|svatb\w*|place1)\b",
        re.I,
    ),
    "personal_name": re.compile(r"\b(?:name1|name2)\b", re.I),
}

SAFE_IP_PREFIXES = (
    "192.0.2.",
    "198.51.100.",
    "203.0.113.",
    "127.0.0.",
    "0.0.0.0",
    "255.255.255.",
)


def is_allowed(kind, match_text):
    if kind == "ipv4":
        return match_text.startswith(SAFE_IP_PREFIXES)
    if kind == "home_path":
        return match_text == "/home/agora" or match_text.startswith("/home/agora/")
    return False


def main():
    root = Path(__file__).resolve().parent.parent
    findings = 0
    files = 0
    scanned_suffixes = (".md", ".yaml", ".yml", ".service", ".timer")
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts or path.suffix.lower() not in scanned_suffixes:
            continue
        files += 1
        text = path.read_text(encoding="utf-8")
        for kind, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                if is_allowed(kind, match.group(0)):
                    continue
                findings += 1
                line = text.count("\n", 0, match.start()) + 1
                print(
                    "FINDING [" + kind + "] "
                    + str(path.relative_to(root))
                    + ":"
                    + str(line)
                    + " -> "
                    + match.group(0)
                )
    print()
    print(str(files) + " files scanned, " + str(findings) + " findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())