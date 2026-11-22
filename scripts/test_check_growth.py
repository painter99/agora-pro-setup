#!/usr/bin/env python3
"""Hermetic unittest suite for scripts/check_growth.py (STACK-UNIFY phase 2).

Every test builds a throwaway git repository in a temporary directory using
subprocess git, commits a baseline, pins it as origin/main, applies changes,
and runs the real checker as a subprocess against that repository. Tests are
independent, need no network, and write nothing outside their temp directory.
"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
CHECKER = SCRIPTS / "check_growth.py"

RETIRED_FILE = (
    "# Retired docs numbers are never reused; a retired number keeps its\n"
    "# number unused.\n19\n"
)

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


def git(cwd, *args):
    return subprocess.run(
        ["git", *args], cwd=str(cwd), check=True, capture_output=True, text=True
    )


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


SKILL_MD_HEADER = (
    "---\nname: placeholder\ndescription: placeholder\nlicense: MIT\n---\n\n"
    "# Skill body\n"
)
SKILL_MD_HEADER_LINES = SKILL_MD_HEADER.count("\n")  # 7 header lines


def skill_md(lines=12):
    """Fixture whose file length is exactly `lines` lines (min: header)."""
    body = "\n".join(
        "line %d" % (i + 1)
        for i in range(max(0, lines - SKILL_MD_HEADER_LINES))
    )
    return SKILL_MD_HEADER + body + ("\n" if body else "")


class GrowthCheckerTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name) / "repo"
        self.repo.mkdir()
        git(self.repo, "init")
        git(self.repo, "symbolic-ref", "HEAD", "refs/heads/main")
        git(self.repo, "config", "user.email", "tester@localhost")
        git(self.repo, "config", "user.name", "tester")
        self.baseline_skills = []
        self.baseline_docs = []
        self.write_retired_file()
        self.commit("baseline setup")

    # -- repository helpers ------------------------------------------------

    def write_retired_file(self):
        write(self.repo / "scripts" / "docs-retired-numbers.txt", RETIRED_FILE)

    def write_baseline(self):
        lines = ["# baseline"]
        lines += ["skill:" + name for name in sorted(self.baseline_skills)]
        lines += ["doc:%d" % n for n in sorted(self.baseline_docs)]
        write(self.repo / "scripts" / "growth-baseline.txt", "\n".join(lines) + "\n")

    def commit(self, message):
        self.write_baseline()
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-m", message)
        return git(self.repo, "rev-parse", "HEAD").stdout.strip()

    def pin_base(self):
        """Commit the baseline and pin it as origin/main."""
        sha = self.commit("baseline")
        git(self.repo, "update-ref", "refs/remotes/origin/main", sha)
        return sha

    def seed_skill(self, name, family="fam", lines=12):
        write(self.repo / "skills" / family / name / "SKILL.md", skill_md(lines))
        if name not in self.baseline_skills:
            self.baseline_skills.append(name)

    def seed_doc(self, number, slug):
        write(self.repo / "docs" / ("%d-%s.md" % (number, slug)), "content\n")
        if number not in self.baseline_docs:
            self.baseline_docs.append(number)

    def justification(self, name, omit=None):
        values = dict(
            Problem="p",
            **{"Trigger / anti-trigger": "t",
               "Existing alternatives and overlap": "a",
               "Evidence / usage": "e",
               "Why a skill extension is insufficient": "w",
               "Safety / dependencies": "s",
               "Eval": "v",
               "Owner": "o"}
        )
        if omit:
            del values[omit]
        body = "".join(key + ": " + values[key] + "\n" for key in SKILL_FIELDS
                       if key in values)
        write(self.repo / "skills" / "justifications" / (name + ".md"),
              "# justification\n\n" + body)

    def doc_justification(self, number, omit=None):
        values = dict(
            **{"Owner": "o",
               "Overlap / alternatives": "ov",
               "Why an existing doc cannot hold it": "w",
               "Links": "l",
               "Maintenance owner": "m",
               "Expected reader": "r"}
        )
        if omit:
            del values[omit]
        body = "".join(key + ": " + values[key] + "\n" for key in DOC_FIELDS
                       if key in values)
        write(self.repo / "skills" / "justifications" / ("docs-%d.md" % number),
              "# justification\n\n" + body)

    def run_checker(self, growth_base=None):
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env.pop("GROWTH_BASE", None)
        if growth_base is not None:
            env["GROWTH_BASE"] = growth_base
        return subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=str(self.repo),
            env=env,
            capture_output=True,
            text=True,
        )

    def assert_fail(self, proc, fragment):
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("GROWTH CHECK FAILED", proc.stdout)
        self.assertIn(fragment, proc.stdout)

    def default_baseline(self):
        self.seed_skill("alpha")
        self.seed_doc(1, "one")
        self.seed_doc(2, "two")
        self.pin_base()

    # -- positive fixtures ---------------------------------------------------

    def test_clean_baseline_passes(self):
        self.default_baseline()
        proc = self.run_checker()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("GROWTH CHECK PASSED", proc.stdout)

    def test_new_skill_with_complete_justification_passes(self):
        self.default_baseline()
        self.seed_skill("beta")
        self.justification("beta")
        self.commit("add beta skill")
        proc = self.run_checker()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("GROWTH CHECK PASSED", proc.stdout)

    def test_new_doc_with_justification_passes(self):
        self.default_baseline()
        write(self.repo / "docs" / "3-next-topic.md", "content\n")
        self.doc_justification(3)
        self.commit("add doc 3")
        proc = self.run_checker()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_growth_base_env_used_when_origin_missing(self):
        self.default_baseline()
        git(self.repo, "update-ref", "-d", "refs/remotes/origin/main")
        base = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        proc = self.run_checker(growth_base=base)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_boundary_500_lines_passes(self):
        self.seed_skill("edge", lines=500)
        self.pin_base()
        proc = self.run_checker()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    # -- negative fixtures ---------------------------------------------------

    def test_missing_justification_fails(self):
        self.default_baseline()
        self.seed_skill("beta")
        self.commit("add beta without justification")
        self.assert_fail(
            self.run_checker(),
            "missing justification file 'skills/justifications/beta.md'",
        )

    def test_missing_field_fails(self):
        self.default_baseline()
        self.seed_skill("beta")
        self.justification("beta", omit="Eval")
        self.commit("add beta with incomplete justification")
        self.assert_fail(
            self.run_checker(), "is missing field 'Eval'"
        )

    def test_empty_field_fails(self):
        self.default_baseline()
        self.seed_skill("beta")
        self.justification("beta")
        path = self.repo / "skills" / "justifications" / "beta.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "Eval: v", "Eval:"), encoding="utf-8")
        self.commit("add beta with empty field")
        self.assert_fail(self.run_checker(), "field 'Eval' is empty")

    def test_duplicate_skill_name_fails(self):
        self.default_baseline()
        self.seed_skill("dup", family="fam1")
        self.seed_skill("dup", family="fam2")
        self.justification("dup")
        self.commit("add two skills named dup")
        self.assert_fail(self.run_checker(), "Duplicate skill name 'dup'")

    def test_rename_from_baseline_requires_justification(self):
        self.seed_skill("old")
        self.seed_doc(1, "one")
        self.pin_base()
        (self.repo / "skills" / "fam" / "old").rename(
            self.repo / "skills" / "fam" / "new")
        self.commit("rename old to new")
        self.assert_fail(
            self.run_checker(),
            "missing justification file 'skills/justifications/new.md'",
        )

    def test_missing_base_fails(self):
        self.default_baseline()
        git(self.repo, "update-ref", "-d", "refs/remotes/origin/main")
        proc = self.run_checker()
        self.assert_fail(proc, "No growth base available")
        self.assertIn("fail-closed", proc.stdout)

    def test_invalid_growth_base_fails(self):
        self.default_baseline()
        proc = self.run_checker(growth_base="no-such-ref")
        self.assert_fail(proc, "does not resolve to a commit")

    def test_duplicate_doc_number_fails(self):
        self.default_baseline()
        write(self.repo / "docs" / "3-alpha.md", "content\n")
        write(self.repo / "docs" / "3-beta.md", "content\n")
        self.doc_justification(3)
        self.commit("add two docs numbered 3")
        self.assert_fail(
            self.run_checker(), "Duplicate docs number 3 added in the same changeset"
        )

    def test_retired_doc_number_fails(self):
        for number in range(1, 19):
            self.seed_doc(number, "doc%d" % number)
        self.pin_base()
        write(self.repo / "docs" / "19-retired-topic.md", "content\n")
        self.doc_justification(19)
        self.commit("reuse retired number 19")
        self.assert_fail(
            self.run_checker(), "is retired and may never be reused"
        )

    def test_non_next_doc_number_fails(self):
        self.default_baseline()
        write(self.repo / "docs" / "5-jump-ahead.md", "content\n")
        self.doc_justification(5)
        self.commit("skip to number 5")
        self.assert_fail(
            self.run_checker(),
            "is not the next free docs number (expected 3",
        )

    def test_two_new_docs_budget_fails(self):
        self.default_baseline()
        write(self.repo / "docs" / "3-first.md", "content\n")
        write(self.repo / "docs" / "4-second.md", "content\n")
        self.doc_justification(3)
        self.doc_justification(4)
        self.commit("add two docs")
        self.assert_fail(
            self.run_checker(), "split into independently reviewable increments"
        )

    def test_overlong_skill_fails(self):
        self.seed_skill("big", lines=501)
        self.seed_doc(1, "one")
        self.pin_base()
        self.assert_fail(
            self.run_checker(),
            "501 lines exceeds the 500-line Skill limit",
        )


if __name__ == "__main__":
    unittest.main()
