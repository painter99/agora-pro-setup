#!/usr/bin/env python3
"""Growth-control checker (STACK-UNIFY phase 2).

Additive deterministic gate, hooked into scripts/check.sh after the existing
checks. It never weakens or replaces an existing check; it only adds rules:

1. Base selection (fail-closed, never HEAD):
   - env GROWTH_BASE, if set, must resolve to a commit that differs from
     HEAD (a pinned base equal to HEAD would hide every addition);
   - else git merge-base HEAD origin/main, if the origin/main ref exists;
   - else FAIL with a clear message. There is no fallback to HEAD, because
     that could hide additions.
2. The changeset is the diff between the base commit and the PROPOSED TREE:
   the working tree as it would be committed (tracked files with staged and
   unstaged changes plus untracked non-ignored files), materialized through
   a temporary copy of the index, so uncommitted additions are visible.
   Every newly added or renamed-to skills/**/SKILL.md requires
   skills/justifications/<skill-dir-name>.md with all required fields
   nonempty, and the justification file must be tracked or at least staged
   in the index (untracked-only justifications are rejected). Skills listed
   in the reviewed baseline as of the base commit are grandfathered only
   when they appear as plain additions of the same full skill path (status
   A); the baseline is read and duplicate-checked at the base commit, so a
   changeset cannot grandfather its own additions by editing the baseline
   in the same commit; a rename or copy from any path always requires a
   justification for the new path, so renames cannot hide additions.
   Justifications match skills 1:1; a duplicate justification for two
   skills fails.
3. Every newly added docs/<number>-*.md - additions include rename and copy
   destinations, except a same-number rename (a pure retitle): the number
   must be unique, must not appear in the retired-numbers registry as of
   the base commit, and must be the next free number above the current
   maximum. A companion skills/justifications/docs-<number>.md with
   nonempty fields is required.
4. Proposal budget: at most 1 new skill AND at most 1 new doc per changeset;
   more must be split into independently reviewable increments.
5. Every skills/**/SKILL.md in the tree is limited to 500 lines (baseline
   items are exempt from justifications, never from this limit).

The checker verifies presence and structure, not truth; review assesses
content. Stdlib only, deterministic, fail-closed.
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MAX_SKILL_LINES = 500
JUST_DIR = "skills/justifications"

SKILL_FIELDS = [
    "Problem",
    "Trigger / anti-trigger",
    "Existing alternatives and overlap",
    "Evidence / usage",
    "Why a skill extension is insufficient",
    "Safety / dependencies",
    "Eval",
    "Owner",
]

DOC_FIELDS = [
    "Owner",
    "Overlap / alternatives",
    "Why an existing doc cannot hold it",
    "Links",
    "Maintenance owner",
    "Expected reader",
]

FIELD_RE = re.compile(r"^\s*(?:[-*]\s*)?\*{0,2}(.+?)\*{0,2}\s*:\s*(.*)$")
DOC_NUM_RE = re.compile(r"^docs/(\d+)-.+\.md$")


def git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root)] + list(args),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def find_root(failures):
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        failures.append(
            "Not inside a git repository (git rev-parse --show-toplevel failed); "
            "run scripts/check_growth.py from a repository checkout."
        )
        return None
    return Path(proc.stdout.strip())


def get_base(root, failures):
    """Resolve the comparison base. Fail-closed; never falls back to HEAD."""
    env_base = os.environ.get("GROWTH_BASE", "").strip()
    if env_base:
        rc, out, _ = git(root, "rev-parse", "--verify", "--quiet",
                         env_base + "^{commit}")
        if rc != 0 or not out.strip():
            failures.append(
                "GROWTH_BASE '" + env_base + "' does not resolve to a commit; "
                "refusing to run without a valid base (fail-closed)."
            )
            return None, None
        resolved = out.strip()
        rc2, head, _ = git(root, "rev-parse", "--verify", "--quiet", "HEAD")
        if rc2 == 0 and head.strip() and resolved == head.strip():
            failures.append(
                "GROWTH_BASE '" + env_base + "' resolves to HEAD ("
                + resolved[:12] + "); a pinned base must differ from HEAD, "
                "because comparing HEAD with itself would hide every "
                "addition (fail-closed)."
            )
            return None, None
        return resolved, "GROWTH_BASE"
    rc, out, _ = git(root, "rev-parse", "--verify", "--quiet",
                     "refs/remotes/origin/main")
    if rc == 0 and out.strip():
        rc2, merge_base, err2 = git(root, "merge-base", "HEAD", "origin/main")
        if rc2 != 0 or not merge_base.strip():
            failures.append(
                "Cannot compute git merge-base HEAD origin/main: "
                + err2.strip()
                + "; refusing to fall back to HEAD (fail-closed)."
            )
            return None, None
        return merge_base.strip(), "merge-base HEAD origin/main"
    failures.append(
        "No growth base available: set GROWTH_BASE to a pinned base commit, or "
        "ensure the 'origin/main' ref exists. Refusing to fall back to HEAD, "
        "because that could hide additions (fail-closed)."
    )
    return None, None


def parse_baseline(lines, failures, source):
    """Parse baseline entries; duplicates fail (fail-closed).

    A baseline entry may be a bare skill directory name ('skill:alpha') or a
    path relative to skills/ ('skill:fam/alpha'). The same skill must not be
    listed twice - neither as the same raw entry nor under two spellings
    that share one directory name - because duplicated entries could
    otherwise bypass justification and budget checks.
    """
    skill_entries = []
    docs = set()
    for lineno, line in enumerate(lines, 1):
        entry = line.strip()
        if not entry or entry.startswith("#"):
            continue
        if entry.startswith("skill:") and len(entry) > 6:
            skill_entries.append((lineno, entry[6:]))
        elif entry.startswith("doc:") and entry[4:].isdigit():
            number = int(entry[4:])
            if number in docs:
                failures.append(
                    source + ":" + str(lineno) + ": duplicate baseline entry "
                    "'doc:" + entry[4:] + "'."
                )
            docs.add(number)
        else:
            failures.append(
                source + ":" + str(lineno)
                + ": unrecognized entry '" + entry
                + "' (expected 'skill:<dir-name>', 'skill:<path>' or "
                "'doc:<number>')."
            )
    seen_raw = {}
    seen_name = {}
    for lineno, value in skill_entries:
        if value in seen_raw:
            failures.append(
                source + ":" + str(lineno) + ": duplicate baseline entry "
                "'skill:" + value + "' (first listed on line "
                + str(seen_raw[value]) + ")."
            )
        else:
            seen_raw[value] = lineno
        name = value.rsplit("/", 1)[-1]
        if name in seen_name and seen_name[name] != value:
            failures.append(
                source + ":" + str(lineno) + ": duplicate baseline skill "
                "directory name '" + name + "' ('skill:" + seen_name[name]
                + "' and 'skill:" + value + "')."
            )
        else:
            seen_name.setdefault(name, value)
    return skill_entries, docs


def load_baseline(root, base, failures):
    """Grandfathering baseline: always validated, grandfathered at the base.

    The baseline file must exist in the working tree and parse cleanly
    (fail-closed). Grandfathering, however, uses the baseline as of the base
    commit, so a changeset cannot grandfather its own additions by editing
    scripts/growth-baseline.txt in the same commit. Baseline entries are
    resolved to full skill paths in the base tree, so additions are compared
    by full skill path, not by bare directory name. When the file does not
    exist at the base (the baseline is being introduced by this very
    changeset), the grandfather set is empty: every added skill then needs
    its own justification.
    """
    path = root / "scripts" / "growth-baseline.txt"
    if not path.is_file():
        failures.append(
            "scripts/growth-baseline.txt is missing; the checker refuses to "
            "run without a reviewed baseline (fail-closed)."
        )
        return None
    parse_baseline(path.read_text(encoding="utf-8").splitlines(), failures,
                   "scripts/growth-baseline.txt (working tree)")
    if base is None:
        return set(), set()
    rc, out, _ = git(root, "show", base + ":scripts/growth-baseline.txt")
    if rc != 0:
        return set(), set()
    entries, docs = parse_baseline(out.splitlines(), failures,
                                   "scripts/growth-baseline.txt (base "
                                   + base[:12] + ")")
    rc, lst, err = git(root, "ls-tree", "-r", "--name-only", base, "--",
                       "skills")
    if rc != 0:
        failures.append("git ls-tree failed: " + err.strip())
        return set(), docs
    base_paths = set()
    by_name = {}
    for line in lst.splitlines():
        rel = line.strip()
        name = skill_name_of(rel)
        if name is not None:
            base_paths.add(rel)
            by_name.setdefault(name, []).append(rel)
    skills = set()
    for _, value in entries:
        if "/" in value:
            full = "skills/" + value + "/SKILL.md"
            if full in base_paths:
                skills.add(full)
            # a path form that matches no base path grandfathers nothing
        else:
            matches = by_name.get(value, [])
            if len(matches) > 1:
                failures.append(
                    "scripts/growth-baseline.txt (base " + base[:12] + "): "
                    "baseline entry 'skill:" + value + "' resolves to "
                    "multiple skill paths in the base tree ("
                    + ", ".join(sorted(matches))
                    + "); list the full path to disambiguate."
                )
            skills.update(matches)
    return skills, docs


def parse_retired(lines, failures, source):
    retired = set()
    for lineno, line in enumerate(lines, 1):
        entry = line.strip()
        if not entry or entry.startswith("#"):
            continue
        if entry.isdigit():
            retired.add(int(entry))
        else:
            failures.append(
                source + ":" + str(lineno)
                + ": unrecognized entry '" + entry + "' (expected a number)."
            )
    return retired


def load_retired(root, base, failures, warnings):
    """Retired docs numbers, read at the base commit (same rule as the
    baseline): a changeset cannot un-retire a number by editing the registry
    in the same changeset. When the registry does not exist at the base (it
    is newly introduced by this very changeset), the retired set is empty
    with a warning, not an error."""
    rc, out, _ = git(root, "show",
                     base + ":scripts/docs-retired-numbers.txt")
    if rc != 0:
        warnings.append(
            "scripts/docs-retired-numbers.txt is absent at the base commit; "
            "treating the retired-numbers set as empty for this run (the "
            "registry is newly introduced in this changeset)."
        )
        retired = set()
    else:
        retired = parse_retired(out.splitlines(), failures,
                                "scripts/docs-retired-numbers.txt (base "
                                + base[:12] + ")")
    path = root / "scripts" / "docs-retired-numbers.txt"
    if path.is_file():
        parse_retired(path.read_text(encoding="utf-8").splitlines(),
                      failures,
                      "scripts/docs-retired-numbers.txt (working tree)")
    elif retired:
        failures.append(
            "scripts/docs-retired-numbers.txt is missing from the working "
            "tree although it exists at the base commit; deleting the "
            "registry would leave future changesets unprotected "
            "(fail-closed)."
        )
    return retired


def proposed_tree(root, failures):
    """Materialize the PROPOSED TREE and return its tree sha.

    The proposed tree is the working tree as it would be committed: tracked
    files with their staged and unstaged changes plus untracked non-ignored
    files. It is built in a temporary copy of the index (read-tree HEAD,
    then add -A, which respects .gitignore), so the real index is left
    untouched and the result is deterministic. Any git error is fail-closed.
    """
    fd, index_path = tempfile.mkstemp(prefix="growth-index-")
    os.close(fd)
    try:
        env = dict(os.environ)
        env["GIT_INDEX_FILE"] = index_path
        steps = (
            (("read-tree", "HEAD"), "git read-tree HEAD", False),
            (("add", "-A", "--", "."), "git add -A", False),
            (("write-tree",), "git write-tree", True),
        )
        tree = None
        for args, label, needs_output in steps:
            proc = subprocess.run(["git", "-C", str(root)] + list(args),
                                  env=env, capture_output=True, text=True)
            if proc.returncode != 0 or (needs_output
                                        and not proc.stdout.strip()):
                failures.append(
                    label + " failed while building the proposed tree: "
                    + proc.stderr.strip() + " (fail-closed)."
                )
                return None
            if needs_output:
                tree = proc.stdout.strip()
        return tree
    finally:
        try:
            os.unlink(index_path)
        except OSError:
            pass


def changed_entries(root, base, failures):
    """Diff the base commit against the PROPOSED TREE (working tree incl.
    untracked non-ignored files), so staged, unstaged and uncommitted
    untracked additions are all visible; returns (status, src, dst)."""
    tree = proposed_tree(root, failures)
    if tree is None:
        return None
    rc, out, err = git(root, "diff", "--name-status", "-M", base, tree)
    if rc != 0:
        failures.append("git diff failed: " + err.strip())
        return None
    entries = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status = "".join(ch for ch in parts[0] if ch.isalpha())
        if status == "A":
            entries.append((status, None, parts[1]))
        elif status in ("R", "C") and len(parts) >= 3:
            entries.append((status, parts[1], parts[2]))
    return entries


def skill_name_of(path):
    if path.startswith("skills/") and path.endswith("/SKILL.md"):
        intermediate = path[len("skills/"):-len("/SKILL.md")]
        if intermediate:
            return intermediate.rsplit("/", 1)[-1]
    return None


def check_fields(root, relpath, fields, failures, prefix):
    path = root / relpath
    if not path.is_file():
        failures.append(prefix + ": missing justification file '" + relpath
                        + "'.")
        return
    rc, _, _ = git(root, "ls-files", "--error-unmatch", "--", relpath)
    if rc != 0:
        failures.append(prefix + ": '" + relpath + "' is neither tracked nor "
                        "staged in the git index (git ls-files); untracked-"
                        "only justification files are not accepted "
                        "(fail-closed).")
    parsed = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = FIELD_RE.match(line)
        if match:
            label = match.group(1).strip()
            if label not in parsed:
                parsed[label] = match.group(2)
    for field in fields:
        if field not in parsed:
            failures.append(prefix + ": '" + relpath + "' is missing field '"
                            + field + "'.")
        elif not parsed[field].strip():
            failures.append(prefix + ": '" + relpath + "' field '" + field
                            + "' is empty.")


def collect_doc_numbers(root, base, added_paths, failures):
    """Map doc number -> set of path labels from baseline, base and tree."""
    used = {}

    def add(number, label):
        used.setdefault(number, set()).add(label)

    rc, out, err = git(root, "ls-tree", "-r", "--name-only", base, "--",
                       "docs")
    if rc != 0:
        failures.append("git ls-tree failed: " + err.strip())
        return None
    for path in out.splitlines():
        match = DOC_NUM_RE.match(path.strip())
        if match:
            add(int(match.group(1)), path.strip() + " (in base)")
    docs_dir = root / "docs"
    if docs_dir.is_dir():
        for path in sorted(docs_dir.glob("*.md")):
            rel = "docs/" + path.name
            if rel in added_paths:
                continue
            match = DOC_NUM_RE.match(rel)
            if match:
                add(int(match.group(1)), rel + " (in tree)")
    return used


def check_line_limits(root, failures):
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        failures.append("skills/ directory is missing (fail-closed).")
        return
    for path in sorted(skills_dir.rglob("SKILL.md")):
        with path.open("rb") as handle:
            count = sum(1 for _ in handle)
        if count > MAX_SKILL_LINES:
            rel = path.relative_to(root)
            failures.append(
                str(rel) + ":" + str(count) + " lines exceeds the "
                + str(MAX_SKILL_LINES) + "-line Skill limit."
            )


def main():
    failures = []
    warnings = []

    root = find_root(failures)
    base = base_desc = None
    baseline = None
    retired = None
    if root is not None:
        base, base_desc = get_base(root, failures)
        baseline = load_baseline(root, base, failures)
        if base is not None:
            retired = load_retired(root, base, failures, warnings)

    entries = None
    if base is not None:
        entries = changed_entries(root, base, failures)

    if not failures and entries is not None and baseline is not None:
        base_skills, base_docs = baseline

        # --- New / renamed-to skills -------------------------------------
        new_skills = []
        for status, src, path in entries:
            name = skill_name_of(path)
            if name is not None:
                new_skills.append((status, src, path, name))

        by_name = {}
        for _, _, path, name in new_skills:
            by_name.setdefault(name, []).append(path)
        for name, paths in sorted(by_name.items()):
            if len(paths) > 1:
                failures.append(
                    "Duplicate skill name '" + name + "' claimed by "
                    + ", ".join(sorted(paths))
                    + "; each skill needs its own justification (1:1)."
                )

        for status, src, path, name in new_skills:
            if status == "A" and path in base_skills:
                continue  # baseline grandfathering: a plain re-add of a
                # baseline path (compared by full skill path); renames and
                # copies are never grandfathered
            prefix = "New/renamed skill '" + path + "'"
            check_fields(root, JUST_DIR + "/" + name + ".md", SKILL_FIELDS,
                         failures, prefix)

        budget_new_skills = sorted(
            {path for _, _, path, _ in new_skills if path not in base_skills}
        )
        if len(budget_new_skills) > 1:
            failures.append(
                "Proposal budget exceeded: " + str(len(budget_new_skills))
                + " new skills in one changeset ("
                + ", ".join(budget_new_skills)
                + "); at most 1 is allowed - split into independently "
                "reviewable increments."
            )

        # --- New docs -----------------------------------------------------
        doc_adds = []
        for status, src, path in entries:
            match = DOC_NUM_RE.match(path)
            if not match:
                continue
            if status == "A":
                doc_adds.append((int(match.group(1)), path))
            elif status in ("R", "C") and src is not None:
                src_match = DOC_NUM_RE.match(src)
                if (status == "R" and src_match
                        and src_match.group(1) == match.group(1)):
                    continue  # same-number rename: a pure retitle; the
                    # number is freed and re-used 1:1, so the destination
                    # is not an addition (a same-number copy keeps the
                    # source and stays an addition)
                doc_adds.append((int(match.group(1)), path))

        by_number = {}
        for number, path in doc_adds:
            by_number.setdefault(number, []).append(path)
        for number, paths in sorted(by_number.items()):
            if len(paths) > 1:
                failures.append(
                    "Duplicate docs number " + str(number) + " added in the "
                    "same changeset: " + ", ".join(sorted(paths)) + "."
                )

        added_paths = {path for _, path in doc_adds}
        used = collect_doc_numbers(root, base, added_paths, failures)
        if used is None:
            used = {}
        for number, path in sorted(doc_adds):
            if retired is not None and number in retired:
                failures.append(
                    "Docs number " + str(number) + " ('" + path
                    + "') is retired and may never be reused."
                )
            elif used.get(number):
                failures.append(
                    "Duplicate docs number " + str(number) + ": '" + path
                    + "' conflicts with already-used number "
                    + "(by " + ", ".join(sorted(used[number])) + ")."
                )
            check_fields(root, JUST_DIR + "/docs-" + str(number) + ".md",
                         DOC_FIELDS, failures,
                         "New doc '" + path + "'")

        all_current = set(base_docs) | set(used)
        current_max = max(all_current) if all_current else 0
        expected = current_max + 1
        while retired is not None and expected in retired:
            expected += 1
        for number, path in sorted(doc_adds):
            if number != expected:
                failures.append(
                    "'" + path + "' is not the next free docs number "
                    "(expected " + str(expected) + "; current maximum is "
                    + str(current_max)
                    + "; retired numbers are never reused)."
                )

        if len(doc_adds) > 1:
            failures.append(
                "Proposal budget exceeded: " + str(len(doc_adds))
                + " new docs in one changeset ("
                + ", ".join(sorted(p for _, p in doc_adds))
                + "); at most 1 is allowed - split into independently "
                "reviewable increments."
            )

    # --- 500-line limit for every skill in the tree ----------------------
    if not failures and root is not None:
        check_line_limits(root, failures)

    for warning in warnings:
        print("WARN: " + warning)
    if failures:
        print("GROWTH CHECK FAILED")
        for failure in failures:
            print("FAIL: " + failure)
        return 1
    print(
        "GROWTH CHECK PASSED (base " + base[:12] + " via " + base_desc + ")"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
