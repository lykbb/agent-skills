#!/usr/bin/env python3
"""Check this bundle's entry points, portable resources and local prose links.

This is a read-only package check. It does not validate product behavior.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "SKILL.md", "README.md", "项目说明.md", "agents/openai.yaml",
    "references/workflow-contract.md", "references/initiation-to-prd.md",
    "references/execution-adapter.md", "references/mvp-acceptance.md",
    "assets/project-AGENTS.md", "assets/project-state.md", "assets/prd-template.md",
    "scripts/check_project.py", "tests/test_check_project.py",
    "modules/ai-product-initiation/SKILL.md",
    "modules/ai-product-initiation/scripts/render_report.py",
    "modules/ai-product-initiation/assets/report-template.html",
    "modules/ai-product-initiation/assets/report-template-grid.html",
    "modules/agent-blueprint/SKILL.md", "modules/agent-blueprint/BLUEPRINT.md",
    "modules/agent-blueprint/使用引导.md", "modules/agent-blueprint/blueprint/cli.py",
    "modules/agent-blueprint/LICENSE", "modules/ai-product-starter-kit/AGENTS.md",
    "modules/ai-product-starter-kit/LICENSE", "modules/ai-product-starter-kit/verify.sh",
)


def prose_only(text: str) -> str:
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return re.sub(r"`[^`\n]*`", "", "\n".join(lines))


def main() -> int:
    errors = []
    paths = list(ROOT.rglob("*"))
    files = [p for p in paths if p.is_file() and not p.is_symlink()]
    for p in paths:
        if p.is_symlink():
            errors.append("Symlink: " + str(p.relative_to(ROOT)))
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            errors.append("Missing: " + name)
    manifests = [p for p in files if p.name == "SKILL.md"]
    for p in manifests:
        text = p.read_text(encoding="utf-8")
        front = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
        if not front:
            errors.append("Missing frontmatter: " + str(p.relative_to(ROOT)))
            continue
        name = re.search(r"^name:\s*([^\n]+)$", front.group(1), re.M)
        description = re.search(r"^description:[ \t]*(\S[^\n]*)$", front.group(1), re.M)
        if description and description.group(1).strip() in {"|", ">", "|-", ">-"}:
            remainder = front.group(1)[description.end():]
            if not re.search(r"^[ \t]+\S", remainder, re.M):
                description = None
        if not name or not description:
            errors.append("Incomplete metadata: " + str(p.relative_to(ROOT)))
        elif name.group(1).strip().strip("\"'") != p.parent.name:
            errors.append("Skill name/folder mismatch: " + str(p.relative_to(ROOT)))
    checked_links = 0
    for p in files:
        if p.suffix == ".json":
            try:
                json.loads(p.read_text(encoding="utf-8"))
            except (ValueError, UnicodeError):
                errors.append("Invalid JSON: " + str(p.relative_to(ROOT)))
        if p.suffix != ".md":
            continue
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", prose_only(p.read_text(encoding="utf-8"))):
            target = unquote(target.strip("<>").split("#", 1)[0])
            if not target or re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            checked_links += 1
            resolved = (p.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append("Link leaves package: " + str(p.relative_to(ROOT)) + " -> " + target)
                continue
            if not resolved.exists():
                errors.append("Broken link: " + str(p.relative_to(ROOT)) + " -> " + target)
    for p in files:
        if p.name == ".env" or (p.name.startswith(".env.") and p.name not in {".env.example", ".env.sample", ".env.template"}):
            errors.append("Private configuration included: " + str(p.relative_to(ROOT)))
        if any(part in {".git", ".venv", "node_modules", "__pycache__"} for part in p.relative_to(ROOT).parts):
            errors.append("Runtime or cache included: " + str(p.relative_to(ROOT)))
    print(json.dumps({
        "ok": not errors, "files": len(files), "skill_manifests": len(manifests),
        "local_links_checked": checked_links, "errors": errors,
        "scope": "Package structure only; no business MVP, network or model validation.",
    }, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
