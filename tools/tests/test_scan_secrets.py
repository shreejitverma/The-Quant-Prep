"""Behaviour tests for tools/scan-secrets.sh, the secret gate run by CI and .no-mistakes.yaml.

Each test builds a throwaway git repo, commits a change shape, and runs the real script against it.
Skipped when gitleaks is not installed (the CI secrets job installs it; the platform job does not).
"""

from __future__ import annotations

import os
import random
import shutil
import string
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "tools" / "scan-secrets.sh"


def fake_token(seed: int) -> str:
    # Built at run time so the test file itself carries no credential-shaped literal.
    rng = random.Random(seed)
    return "".join(rng.choice(string.ascii_letters + string.digits) for _ in range(32))


@unittest.skipUnless(shutil.which("gitleaks") and shutil.which("git"), "gitleaks and git are required")
class ScanSecretsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="scan-secrets-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.env = {
            **os.environ,
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@example.com",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@example.com",
        }
        self.git("init", "-q", "-b", "main")
        shutil.copy(REPO / ".gitleaks.toml", self.tmp / ".gitleaks.toml")
        self.write("app.py", "a = 1\nb = 2\nc = 3\nd = 4\ne = 5\n")
        self.commit("base")
        self.base = self.git("rev-parse", "HEAD")
        self.secret = f'authtoken = "{fake_token(7)}"\n'

    def git(self, *args: str, check: bool = True) -> str:
        out = subprocess.run(["git", *args], cwd=self.tmp, env=self.env, capture_output=True, text=True)
        if check and out.returncode != 0:
            self.fail(f"git {' '.join(args)} failed: {out.stderr}")
        return out.stdout.strip()

    def write(self, rel: str, text: str) -> None:
        (self.tmp / rel).write_text(text)

    def commit(self, message: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def branch(self, name: str, rel: str, text: str) -> None:
        self.git("checkout", "-q", "-b", name, self.base)
        self.write(rel, text)
        self.commit(name)
        self.git("checkout", "-q", "main")

    def scan(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["sh", str(SCRIPT), self.base], cwd=self.tmp, env=self.env, capture_output=True, text=True)

    def assert_leak(self) -> None:
        out = self.scan()
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertIn("leaks found", out.stdout + out.stderr)

    def assert_clean(self) -> None:
        out = self.scan()
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)

    def test_plain_commit_with_secret_fails(self) -> None:
        self.write("plain.py", self.secret)
        self.commit("add secret")
        self.assert_leak()

    def test_clean_merge_passes(self) -> None:
        self.branch("side", "side.txt", "x\n")
        self.write("f.txt", "y\n")
        self.commit("feat")
        self.git("merge", "-q", "--no-ff", "-m", "merge", "side")
        self.assert_clean()

    def test_secret_added_only_in_merge_commit_fails(self) -> None:
        self.branch("side", "app.py", "a = 10\nb = 2\nc = 3\nd = 4\ne = 5\n")
        self.write("f.txt", "y\n")
        self.commit("feat")
        self.git("merge", "-q", "--no-ff", "--no-commit", "side")
        self.write("app.py", (self.tmp / "app.py").read_text() + self.secret)
        self.commit("merge")
        self.assert_leak()

    def test_secret_in_conflict_resolution_fails(self) -> None:
        self.branch("side", "app.py", "a = 10\n")
        self.write("app.py", "a = 20\n")
        self.commit("feat")
        self.git("merge", "-q", "side", check=False)
        self.write("app.py", "a = 20\n" + self.secret)
        self.commit("resolve")
        self.assert_leak()

    def test_clean_octopus_merge_passes(self) -> None:
        self.branch("s1", "s1.txt", "1\n")
        self.branch("s2", "s2.txt", "2\n")
        self.write("f.txt", "3\n")
        self.commit("feat")
        self.git("merge", "-q", "-m", "octopus", "s1", "s2")
        self.assertEqual(self.git("rev-list", "--min-parents=3", "--count", "HEAD"), "1")
        self.assert_clean()

    def test_secret_added_only_in_octopus_merge_fails(self) -> None:
        self.branch("s1", "s1.txt", "1\n")
        self.branch("s2", "s2.txt", "2\n")
        self.write("f.txt", "3\n")
        self.commit("feat")
        self.git("merge", "-q", "--no-commit", "s1", "s2")
        self.write("octo.py", self.secret)
        self.commit("octopus")
        self.assertEqual(self.git("rev-list", "--min-parents=3", "--count", "HEAD"), "1")
        self.assert_leak()

    def test_unknown_base_is_an_error(self) -> None:
        self.base = "deadbeefdeadbeef"
        out = self.scan()
        self.assertEqual(out.returncode, 1)
        self.assertIn("not a known commit", out.stderr)


if __name__ == "__main__":
    unittest.main()
