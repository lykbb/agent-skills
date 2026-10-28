#!/usr/bin/env python3
"""Read-only structural preflight for an explicitly selected business project.

This utility never runs project code or validates a live model, UI, or service.
Its JSON result is deliberately insufficient to accept an MVP.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
STAGES = ("planning", "mvp")
IGNORED_DIRECTORIES = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", ".env",
    "node_modules", "vendor", "site-packages", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache",
    ".next", "dist", "build", "out", "coverage", ".idea", ".vscode",
    "docs", "doc", "tests", "test", "__tests__",
}
SOURCE_SUFFIXES = {
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".go", ".rs", ".java", ".kt", ".kts", ".swift", ".dart",
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".cs",
    ".php", ".rb", ".ex", ".exs", ".vue", ".svelte", ".html",
    ".css", ".scss", ".sass", ".less", ".sql", ".sh", ".lua",
}


def result_base(stage: str) -> dict:
    return {
        "stage": stage,
        "static_ready": False,
        "runtime_validation": "not_performed",
        "mvp_accepted": False,
        "checks": {},
        "missing": [],
        "errors": [],
        "source_files": [],
        "scope": "File presence only; document meaning and runtime behavior are not verified.",
    }


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def file_check(root: Path, relative: str) -> dict:
    path = root / relative
    try:
        resolved = path.resolve(strict=True)
        safe = is_within(resolved, root)
        present = safe and resolved.is_file()
        nonempty = present and resolved.stat().st_size > 0
    except (OSError, RuntimeError):
        safe = present = nonempty = False
    return {"path": relative, "present": present, "nonempty": nonempty,
            "inside_project": safe}


def is_source_candidate(path: Path) -> bool:
    name = path.name.lower()
    if name.startswith(".env") or path.suffix.lower() not in SOURCE_SUFFIXES:
        return False
    if name in {"conftest.py", "setup.py"} or name.startswith("test_"):
        return False
    if re.search(r"(?:[._-](?:test|spec)|\.config)\.[^.]+$", name):
        return False
    return True


def source_candidates(root: Path) -> tuple[list[str], list[dict]]:
    found: list[str] = []
    errors: list[dict] = []

    def on_error(error: OSError) -> None:
        # Do not emit exception text: it may contain an arbitrary OS message.
        errors.append({"code": "source_scan_unavailable",
                       "message": "A project directory could not be inspected."})

    for directory, directories, filenames in os.walk(
        root, topdown=True, followlinks=False, onerror=on_error
    ):
        base = Path(directory)
        directories[:] = sorted(
            name for name in directories
            if name.lower() not in IGNORED_DIRECTORIES
            and not name.startswith(".env")
            and not (base / name).is_symlink()
        )
        for filename in sorted(filenames):
            candidate = base / filename
            if candidate.is_symlink() or not is_source_candidate(candidate):
                continue
            try:
                if candidate.is_file() and candidate.stat().st_size > 0:
                    found.append(candidate.relative_to(root).as_posix())
            except OSError:
                on_error(OSError())
    return found, errors


def check_project(project_root: str, stage: str = "planning") -> tuple[dict, int]:
    result = result_base(stage)
    if stage not in STAGES:
        result["errors"].append({"code": "invalid_stage", "message": "Use planning or mvp."})
        return result, 2
    try:
        root = Path(project_root).expanduser().resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        result["errors"].append({"code": "invalid_project_root",
                                 "message": "The project root must be an existing directory."})
        return result, 2
    if not root.is_dir():
        result["errors"].append({"code": "invalid_project_root",
                                 "message": "The project root must be a directory."})
        return result, 2
    if is_within(root, PACKAGE_ROOT):
        result["errors"].append({"code": "skill_package_is_not_project",
                                 "message": "Select a business project outside this skill package."})
        return result, 2
    result["project_root"] = str(root)

    required = ["docs/PRD/PRD.md", "docs/项目状态.md"]
    if stage == "mvp":
        required.append("README.md")
    for relative in required:
        check = file_check(root, relative)
        result["checks"][relative] = check
        if not check["nonempty"]:
            result["missing"].append(relative)

    if stage == "mvp":
        candidates, errors = source_candidates(root)
        result["source_files"] = candidates
        result["errors"].extend(errors)
        result["checks"]["business_source"] = {"present": bool(candidates),
                                                "count": len(candidates)}
        if not candidates:
            result["missing"].append("business_source")

    result["static_ready"] = not result["missing"] and not result["errors"]
    return result, 0 if result["static_ready"] else 1


def emit(result: dict) -> None:
    print(json.dumps(result, ensure_ascii=False, indent=2))


class JSONArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        result = result_base("unknown")
        result["errors"].append({"code": "invalid_arguments", "message": message})
        emit(result)
        self.exit(2)


def main(argv: list[str] | None = None) -> int:
    parser = JSONArgumentParser(add_help=False, description=__doc__)
    parser.add_argument("--project-root")
    parser.add_argument("--stage", choices=STAGES, default="planning")
    parser.add_argument("-h", "--help", action="store_true")
    args = parser.parse_args(argv)
    if args.help:
        emit({"usage": "python3 scripts/check_project.py --project-root PATH --stage planning|mvp",
              "stages": list(STAGES), "read_only": True,
              "exit_codes": {"0": "Static files present", "1": "Missing or unreadable items",
                             "2": "Invalid arguments or project root"},
              "runtime_validation": "not_performed", "mvp_accepted": False})
        return 0
    if not args.project_root:
        parser.error("--project-root is required")
    result, status = check_project(args.project_root, args.stage)
    emit(result)
    return status


if __name__ == "__main__":
    sys.exit(main())
