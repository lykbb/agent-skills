"""Behavioral tests for the read-only project preflight; standard library only."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE_ROOT / "scripts/check_project.py"
SPEC = importlib.util.spec_from_file_location("project_preflight", SCRIPT)
PREFLIGHT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREFLIGHT)


class ProjectPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="product-preflight-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.project = self.base / "business"
        self.project.mkdir()

    def write(self, relative, content="fixture\n"):
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def planning_files(self):
        self.write("docs/PRD/PRD.md", "# A proposed user task\n")
        self.write("docs/项目状态.md", "# Planning; runtime verification is pending\n")

    def snapshot(self):
        return {
            path.relative_to(self.project).as_posix():
                hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
            for path in self.project.rglob("*")
        }

    def run_cli(self, root=None, stage="planning"):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--project-root", str(root or self.project),
             "--stage", stage],
            capture_output=True, text=True, env=env, check=False,
        )
        self.assertEqual(completed.stderr, "")
        return completed, json.loads(completed.stdout)

    def test_external_planning_project_is_checked_without_writes(self):
        self.planning_files()
        before = self.snapshot()
        completed, result = self.run_cli()
        self.assertEqual(completed.returncode, 0)
        self.assertTrue(result["static_ready"])
        self.assertEqual(result["runtime_validation"], "not_performed")
        self.assertFalse(result["mvp_accepted"])
        self.assertEqual(before, self.snapshot())

    def test_skill_package_descendants_and_symlink_aliases_are_rejected(self):
        alias = self.base / "package-alias"
        alias.symlink_to(PACKAGE_ROOT, target_is_directory=True)
        for root in [PACKAGE_ROOT, PACKAGE_ROOT / "scripts", alias, alias / "scripts"]:
            with self.subTest(root=root):
                completed, result = self.run_cli(root)
                self.assertEqual(completed.returncode, 2)
                self.assertFalse(result["static_ready"])
                self.assertEqual(result["errors"][0]["code"], "skill_package_is_not_project")

    def test_missing_planning_documents_fail(self):
        completed, result = self.run_cli()
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(set(result["missing"]), {"docs/PRD/PRD.md", "docs/项目状态.md"})
        self.assertFalse(result["static_ready"])

    def test_complete_mvp_structure_does_not_claim_runtime_acceptance(self):
        self.planning_files()
        self.write("README.md", "# Start and validation instructions\n")
        self.write("backend/app/main.py", 'raise RuntimeError("project code must not run")\n')
        before = self.snapshot()
        completed, result = self.run_cli(stage="mvp")
        self.assertEqual(completed.returncode, 0)
        self.assertTrue(result["static_ready"])
        self.assertEqual(result["source_files"], ["backend/app/main.py"])
        self.assertEqual(result["runtime_validation"], "not_performed")
        self.assertIs(result["mvp_accepted"], False)
        self.assertNotIn("project code must not run", completed.stdout)
        self.assertEqual(before, self.snapshot())

    def test_dependency_test_document_and_symlink_files_do_not_count_as_business_source(self):
        self.planning_files()
        self.write("README.md")
        for relative in ["docs/example.py", "tests/test_app.py", "test_root.py",
                         "node_modules/package/index.js", "vendor/library.py",
                         ".venv/lib/runtime.py", "env/worker.py", ".git/hook.sh",
                         "frontend/vite.config.ts", "frontend/app.spec.ts"]:
            self.write(relative)
        external = self.base / "outside.py"
        external.write_text("secret = 'outside'\n")
        (self.project / "linked.py").symlink_to(external)
        completed, result = self.run_cli(stage="mvp")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(result["source_files"], [])
        self.assertIn("business_source", result["missing"])

    def test_env_content_is_neither_read_nor_returned(self):
        self.planning_files()
        sentinel = "NEVER_ECHO_PRIVATE_CREDENTIAL_72841"
        self.write(".env", "MODEL_API_KEY=" + sentinel + "\n")
        with patch.object(Path, "read_text", side_effect=AssertionError("No content reads allowed")):
            result, status = PREFLIGHT.check_project(str(self.project), "planning")
        self.assertEqual(status, 0)
        self.assertNotIn(sentinel, json.dumps(result))
        completed, cli_result = self.run_cli()
        self.assertEqual(completed.returncode, 0)
        self.assertNotIn(sentinel, completed.stdout + completed.stderr)
        self.assertEqual(cli_result["runtime_validation"], "not_performed")
        self.assertFalse(cli_result["mvp_accepted"])


if __name__ == "__main__":
    unittest.main()
