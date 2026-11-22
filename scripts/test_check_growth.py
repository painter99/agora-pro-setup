#!/usr/bin/env python3
"""Hermetic unittest suite for scripts/check_growth.py (STACK-UNIFY phase 2).

Every test builds a throwaway git repository in a temporary directory using
subprocess git, commits a baseline, pins it as origin/main, applies changes,
and runs the real checker as a subprocess against that repository. Tests are
independent, need no network, and write nothing outside their temp directory.
"""
import os
import shutil
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


# Minimal valid SKILL.md for the CheckFormatTest fixture (finding R2 #7).
FORMAT_SKILL_MD = (
    "---\n"
    "name: beta\n"
    "description: A test skill\n"
    "license: MIT\n"
    "---\n"
    "\n"
    "# Skill: beta\n"
    "\n"
    "## Catalog description\n"
    "A test skill\n"
    "\n"
    "## Purpose\n"
    "p\n"
    "\n"
    "## Load when\n"
    "l\n"
    "\n"
    "## Do not load when\n"
    "d\n"
    "\n"
    "## Dependencies\n"
    "None.\n"
    "\n"
    "## Workflow\n"
    "w\n"
    "\n"
    "## Forbidden behavior\n"
    "f\n"
    "\n"
    "## Verification\n"
    "v\n"
    "\n"
    "## Output contract\n"
    "o\n"
)


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
        # R1 #2: a pinned base must differ from HEAD, so advance HEAD first
        git(self.repo, "commit", "--allow-empty", "-m", "advance HEAD")
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

    # -- R1 review-fix coverage ----------------------------------------------

    def test_uncommitted_untracked_addition_detected(self):
        """R1 #1: an untracked, uncommitted new skill must be visible."""
        self.default_baseline()
        self.seed_skill("beta")  # untracked; no justification anywhere
        proc = self.run_checker()
        self.assert_fail(
            proc,
            "missing justification file 'skills/justifications/beta.md'",
        )
        git(self.repo, "add", "skills/fam/beta/SKILL.md")
        skill = self.repo / "skills" / "fam" / "beta" / "SKILL.md"
        skill.unlink()
        proc = self.run_checker()
        self.assert_fail(proc, "missing justification file 'skills/justifications/beta.md'")
        self.assertIn("skills/fam/beta/SKILL.md", proc.stdout)
        write(skill, "modified working-tree content\n")
        self.justification("beta", omit="Eval")
        git(self.repo, "add", "skills/justifications/beta.md")
        self.justification("beta")  # the staged blob remains incomplete
        self.assert_fail(self.run_checker(), "is missing field 'Eval'")
        git(self.repo, "add", "skills/justifications/beta.md")
        proc = self.run_checker()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_untracked_skill_with_staged_justification_passes(self):
        """R1 #1: proposed-tree semantics - staged justification accepted."""
        self.default_baseline()
        self.seed_skill("beta")
        self.justification("beta")
        git(self.repo, "add", "-A")  # staged, never committed
        proc = self.run_checker()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("GROWTH CHECK PASSED", proc.stdout)

    def test_growth_base_head_fails(self):
        """R1 #2: GROWTH_BASE resolving to HEAD must fail."""
        self.default_baseline()
        head = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        for value in ("HEAD", head):
            proc = self.run_checker(growth_base=value)
            self.assert_fail(proc, "resolves to HEAD")

    def test_duplicate_baseline_entry_fails(self):
        """R1 #3: duplicated baseline entries fail at the base commit."""
        self.seed_skill("alpha")
        self.seed_doc(1, "one")
        write(self.repo / "scripts" / "growth-baseline.txt",
              "# baseline\nskill:alpha\nskill:alpha\ndoc:1\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-m", "baseline with duplicate entry")
        git(self.repo, "update-ref", "refs/remotes/origin/main",
            git(self.repo, "rev-parse", "HEAD").stdout.strip())
        self.assert_fail(self.run_checker(),
                         "duplicate baseline entry 'skill:alpha'")
        # the same dir name under two spellings is also a duplicate
        write(self.repo / "scripts" / "growth-baseline.txt",
              "# baseline\nskill:alpha\nskill:fam/alpha\ndoc:1\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-m", "baseline with name duplicate")
        git(self.repo, "update-ref", "refs/remotes/origin/main",
            git(self.repo, "rev-parse", "HEAD").stdout.strip())
        self.assert_fail(self.run_checker(),
                         "duplicate baseline skill directory name 'alpha'")

    def test_doc_rename_to_duplicate_number_fails(self):
        """R1 #4: a rename onto an already-used docs number fails."""
        self.default_baseline()
        (self.repo / "docs" / "1-one.md").rename(self.repo / "docs" / "2-x.md")
        self.commit("rename doc 1 onto used number 2")
        self.assert_fail(self.run_checker(), "Duplicate docs number 2")

    def test_doc_rename_to_retired_number_fails(self):
        """R1 #4: a rename onto a retired docs number fails."""
        self.seed_doc(1, "one")
        self.seed_doc(2, "two")
        self.pin_base()
        (self.repo / "docs" / "1-one.md").rename(
            self.repo / "docs" / "19-new-topic.md")
        self.commit("rename doc 1 onto retired number 19")
        self.assert_fail(self.run_checker(),
                         "is retired and may never be reused")

    def test_doc_retitle_same_number_passes(self):
        """R1 #4: a same-number rename (pure retitle) stays allowed."""
        self.default_baseline()
        (self.repo / "docs" / "1-one.md").rename(
            self.repo / "docs" / "1-renamed-title.md")
        self.commit("retitle doc 1 in place")
        proc = self.run_checker()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_registry_self_edit_does_not_bypass(self):
        """R1 #5: un-retiring a number in the same changeset has no effect."""
        self.seed_doc(1, "one")
        self.seed_doc(2, "two")
        self.pin_base()  # registry at the base still lists 19
        write(self.repo / "scripts" / "docs-retired-numbers.txt",
              "# edited in the changeset; 19 removed\n")
        write(self.repo / "docs" / "19-reused.md", "content\n")
        self.doc_justification(19)
        self.commit("un-retire 19 and reuse it")
        self.assert_fail(self.run_checker(),
                         "removes retired number")

    def test_registry_absent_at_base_warns_and_treats_empty(self):
        """R1 #5: registry newly introduced - empty set with a warning."""
        self.seed_skill("alpha")
        self.seed_doc(1, "one")
        (self.repo / "scripts" / "docs-retired-numbers.txt").unlink()
        self.commit("drop the registry before the base")
        git(self.repo, "update-ref", "refs/remotes/origin/main",
            git(self.repo, "rev-parse", "HEAD").stdout.strip())
        write(self.repo / "docs" / "2-next.md", "content\n")
        self.doc_justification(2)
        self.commit("add doc 2 while the registry is absent at base")
        proc = self.run_checker()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("WARN:", proc.stdout)
        self.assertIn("docs-retired-numbers.txt", proc.stdout)

    def test_untracked_only_justification_fails(self):
        """R1 #6: justification files must be tracked or staged."""
        self.default_baseline()
        self.seed_skill("beta")
        self.justification("beta")  # written but never added
        git(self.repo, "add", "skills/fam/beta/SKILL.md")
        proc = self.run_checker()
        self.assert_fail(proc, "neither tracked nor staged")


    # -- R2 review-fix coverage ----------------------------------------------

    def test_growth_base_non_ancestor_fails(self):
        """R2 #1: GROWTH_BASE must be an ancestor of HEAD (fail-closed)."""
        self.default_baseline()
        base = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        git(self.repo, "commit", "--allow-empty", "-m", "advance HEAD")
        git(self.repo, "checkout", "--orphan", "unrelated")
        git(self.repo, "commit", "--allow-empty", "-m", "unrelated root")
        sibling = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        git(self.repo, "checkout", "main")
        proc = self.run_checker(growth_base=sibling)
        self.assert_fail(proc, "is not an ancestor of HEAD")
        self.assertIn("GROWTH_BASE", proc.stdout)
        # a verified base (a real ancestor of HEAD) still passes
        proc = self.run_checker(growth_base=base)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_force_added_ignored_staged_file_survives(self):
        """R2 #2: staged force-added ignored files stay in the proposed
        tree (seeded from the real index, not from HEAD)."""
        write(self.repo / ".gitignore", "secret-skill/\n")
        self.default_baseline()
        write(self.repo / "skills" / "fam" / "secret-skill" / "SKILL.md",
              skill_md())
        git(self.repo, "add", "-f", "skills/fam/secret-skill/SKILL.md")
        self.assert_fail(
            self.run_checker(),
            "missing justification file "
            "'skills/justifications/secret-skill.md'",
        )

    def test_justification_blob_authoritative_symlink_rejected(self):
        """R2 #3: validate the staged blob, not working-tree content;
        symlinked justification files are rejected."""
        self.default_baseline()
        self.seed_skill("beta")
        self.justification("beta")
        path = self.repo / "skills" / "justifications" / "beta.md"
        complete = path.read_text(encoding="utf-8")
        path.write_text("# justification\n\nProblem: p\n", encoding="utf-8")
        git(self.repo, "add", "skills/justifications/beta.md")
        path.write_text(complete, encoding="utf-8")
        git(self.repo, "commit", "-m",
            "stage an incomplete justification blob")
        # a justification staged as a symlink is rejected outright
        self.seed_skill("gamma")
        target = self.repo / "outside-gamma.md"
        target.write_text(complete, encoding="utf-8")
        os.symlink(target,
                   self.repo / "skills" / "justifications" / "gamma.md")
        git(self.repo, "add", "skills/justifications/gamma.md")
        proc = self.run_checker()
        self.assert_fail(proc, "is missing field 'Eval'")
        self.assertIn("symlink", proc.stdout)

    def test_exotic_path_z_parsing(self):
        """R2 #4: diff --name-status -z parsing for exotic paths (unicode
        and spaces); the exact unquoted justification name matches."""
        self.default_baseline()
        name = 'naïve "skill"'
        write(self.repo / "skills" / "fam" / name / "SKILL.md", skill_md())
        self.justification(name)
        self.commit("add a skill with a unicode name containing a space")
        path = self.repo / "skills" / "justifications" / (name + ".md")
        path.unlink()
        git(self.repo, "add", "-u")
        proc = self.run_checker()
        self.assert_fail(proc, "missing justification file")
        self.assertIn("skills/fam/" + name + "/SKILL.md", proc.stdout)
        self.justification(name)
        git(self.repo, "add", str(path.relative_to(self.repo)))
        proc = self.run_checker()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("GROWTH CHECK PASSED", proc.stdout)

    def test_skill_name_reuse_across_categories_fails(self):
        """R2 #5: a new skill reusing a skill dir name that exists anywhere
        in the FULL tree at the base fails, even outside the changeset."""
        self.default_baseline()  # base tree has skills/fam/alpha
        # Remove the baseline at the base, then introduce it in this change.
        baseline = self.repo / "scripts" / "growth-baseline.txt"
        baseline.unlink()
        git(self.repo, "add", "-u")
        git(self.repo, "commit", "-m", "remove baseline before base")
        git(self.repo, "update-ref", "refs/remotes/origin/main",
            git(self.repo, "rev-parse", "HEAD").stdout.strip())
        self.write_baseline()
        self.seed_skill("alpha", family="other")
        self.justification("alpha")
        self.commit("add skills/other/alpha reusing the name alpha")
        self.assert_fail(
            self.run_checker(),
            "reuses the skill directory name 'alpha'",
        )

    def test_registry_number_removal_fails(self):
        """R2 #6: a number present at the base but missing from the
        working-tree registry fails (entries may only be added)."""
        self.seed_doc(1, "one")
        self.pin_base()  # registry at the base lists 19
        write(self.repo / "scripts" / "docs-retired-numbers.txt",
              "# 19 removed in this changeset\n")
        git(self.repo, "add", "scripts/docs-retired-numbers.txt")
        self.write_retired_file()  # staged removal, intact working tree
        self.assert_fail(self.run_checker(), "may only be added, never removed")
        git(self.repo, "add", "scripts/docs-retired-numbers.txt")
        write(self.repo / "scripts" / "docs-retired-numbers.txt", "# removed\n")
        self.assert_fail(self.run_checker(), "may only be added, never removed")
        self.commit("remove 19 from the registry")
        self.assert_fail(
            self.run_checker(),
            "may only be added, never removed",
        )


class CheckFormatTest(unittest.TestCase):
    """R2 #7: the skills/justifications/ stray-file exemption is narrow:
    only the exact expected file names are exempt."""

    def test_justification_stray_exemption_is_narrow(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        scripts = root / "scripts"
        scripts.mkdir()
        shutil.copy(SCRIPTS / "check_format.py", scripts / "check_format.py")
        write(root / "skills" / "beta" / "SKILL.md", FORMAT_SKILL_MD)
        for name in ("TEMPLATE.md", "README.md", "docs-3.md", "beta.md"):
            write(root / "skills" / "justifications" / name, "x\n")
        write(root / "skills" / "justifications" / "random-notes.md", "x\n")
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        proc = subprocess.run(
            [sys.executable, str(scripts / "check_format.py")],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
        )
        stray_lines = [line for line in proc.stdout.splitlines()
                       if "(stray Markdown file" in line]
        self.assertEqual(
            stray_lines,
            ["FAIL skills/justifications/random-notes.md (stray Markdown "
             "file; Skills live in <dir>/SKILL.md)"],
        )


if __name__ == "__main__":
    unittest.main()
