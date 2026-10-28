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

Additional patterns:
- czech_prose — the repository is English-only; Czech prose (3+ diacritic
  glyphs on one line) outside code fences signals leaked instance content.
  Code fences are exempt: Skills may legitimately quote Czech examples.
- model_id — versioned model identifiers (e.g. gemini-2.5-pro, and spaced
  forms like "Claude Opus 4.1" via a bounded sub-name group) leak a
  personal model-routing stack; product names like "Claude Code" do not
  match because a digit is required.

Hardened after an adversarial self-test (2026-10-28): family-term coverage
extended with generic Czech kinship stems, personal-name pattern matches
inflected forms, model_id matches spaced forms. Known accepted gaps:
obfuscated contact strings, short Czech lines with <= 2 diacritic glyphs,
instance-specific proper nouns (adding them here would publish them).
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
        r"|svatb\w*|place1|sestr\w*|bratr\w*|mamink\w*|tat[íi]n\w*"
        r"|tát\w*|dítě|dět\w*|vnuk\w*|vnučk\w*|tchyn\w*|tchán\w*)\b",
        re.I,
    ),
    "personal_name": re.compile(r"\b(?:name1|name2)\w*", re.I),
    "model_id": re.compile(
        r"\b(?:claude|gemini|deepseek|qwen|glm|gpt|llama|mistral|kimi|grok)"
        r"(?:[-_ ]?(?:opus|sonnet|haiku|pro|flash|mini|nano|large|small|air|max|lite))*"
        r"[-_ ]?[a-z]?\d",
        re.I,
    ),
}

CZECH_GLYPHS = re.compile(r"[áčďéěíĺľňóŕřšťúůýžÁČĎÉĚÍĹĽŇÓŔŘŠŤÚŮÝŽ]")

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


def non_fenced_lines(text):
    """Return (line number, line) pairs for lines outside ``` / ~~~ fences."""
    out, fence = [], None
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if fence is None:
            if stripped.startswith("```") or stripped.startswith("~~~"):
                fence = stripped[:3]
                continue
            out.append((i, line))
        elif stripped.startswith(fence):
            fence = None
    return out


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
        for lineno, line_text in non_fenced_lines(text):
            if len(CZECH_GLYPHS.findall(line_text)) >= 3:
                findings += 1
                print(
                    "FINDING [czech_prose] "
                    + str(path.relative_to(root))
                    + ":"
                    + str(lineno)
                    + " -> "
                    + line_text.strip()[:80]
                )
    print()
    print(str(files) + " files scanned, " + str(findings) + " findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())