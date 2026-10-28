#!/usr/bin/env python3
"""Check that this skill package contains its own instructions and resources."""
import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRS = {
    "social-content-studio": ".",
    "long-article": "01-长文-long-article",
    "xiaohongshu-post": "02-图文-xiaohongshu-post",
    "short-posts": "03-短帖-short-posts",
    "tutorial-article": "04-教程-tutorial",
    "news-research-brief": "05-资讯调研-news-brief",
    "clean-long-transcript": "11-转写整理-clean-long-transcript",
    "huashu-topic-gen": "12-选题大纲-huashu-topic-gen",
    "content-research": "13-调研核验-content-research",
    "writing-skill": "14-正文写作-writing-skill",
    "xiaohongshu-image-posts": "15-小红书分页-xiaohongshu-image-posts",
    "title-creator": "16-标题封面字-title-creator",
    "article-visuals": "17-长文配图-article-visuals",
    "social-image-studio": "18-生图制作-social-image-studio",
    "check-social-content-compliance": "19-发布复核-check-social-content-compliance",
}
NAMES = list(DIRS)

def prose_only(text):
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            value = marker.group(1)[0]
            if fence is None:
                fence = value
            elif fence == value:
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return re.sub(r"`[^`\n]*`", "", "\n".join(lines))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-clients", action="store_true",
                        help="Also inspect existing local client entry points.")
    options = parser.parse_args()
    errors = []
    files = []
    symlinks = []
    for parent, directories, names in os.walk(ROOT, followlinks=False):
        for name in directories + names:
            candidate = Path(parent) / name
            if candidate.is_symlink():
                symlinks.append(str(candidate.relative_to(ROOT)))
        for name in names:
            candidate = Path(parent) / name
            if candidate.is_file() and not candidate.is_symlink():
                files.append(candidate)
    if symlinks:
        errors.append("Package contains symlinks: " + ", ".join(symlinks))
    for name in NAMES:
        directory = ROOT / DIRS[name]
        manifest = directory / "SKILL.md"
        if not manifest.is_file():
            errors.append("Missing manifest: " + str(manifest))
            continue
        content = manifest.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.S)
        if not match:
            errors.append("Missing frontmatter: " + str(manifest))
            continue
        value = re.search(r"^name:\s*(.+)$", match.group(1), re.M)
        if not value or value.group(1).strip().strip(chr(34) + chr(39)) != name:
            errors.append("Unexpected skill name: " + str(manifest))
        if not re.search(r"^description:\s*\S.+$", match.group(1), re.M):
            errors.append("Missing description: " + str(manifest))
    references = 0
    for document in [p for p in files if p.suffix == ".md"]:
        content = document.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", prose_only(content)):
            target = target.strip("<>").split("#", 1)[0]
            if not target or re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            references += 1
            resolved = (document.parent / target).resolve()
            if not resolved.is_relative_to(ROOT):
                errors.append("Reference leaves package: " + str(document.relative_to(ROOT)) + " -> " + target)
            elif not resolved.exists():
                errors.append("Broken reference: " + str(document.relative_to(ROOT)) + " -> " + target)
    client_entries = 0
    client_packages = 0
    if options.check_clients:
        for folder in [".agents", ".codex", ".workbuddy", ".codebuddy", ".claude"]:
            client = Path.home() / folder / "skills"
            if not client.is_dir():
                continue
            package = client / ROOT.name
            client_packages += 1
            if not package.is_dir() or package.resolve() != ROOT:
                errors.append("Unreadable or noncanonical client package: " + str(package))
                continue
            for name in NAMES:
                manifest = package / DIRS[name] / "SKILL.md"
                client_entries += 1
                canonical_manifest = ROOT / DIRS[name] / "SKILL.md"
                if not manifest.is_file():
                    errors.append("Unreadable packaged client entry: " + str(manifest))
                elif manifest.resolve() != canonical_manifest.resolve():
                    errors.append("Client package maintains another copy: " + str(manifest))
            for alternate in client.iterdir():
                if alternate.name == ROOT.name:
                    continue
                if alternate.name in NAMES:
                    errors.append("Redundant top-level packaged skill entry: " + str(alternate))
                    continue
                alternate_manifest = alternate / "SKILL.md"
                if not alternate_manifest.is_file():
                    continue
                alternate_text = alternate_manifest.read_text(encoding="utf-8")
                field = re.search(r"^name:\s*(.+)$", alternate_text, re.M)
                if not field:
                    continue
                declared = field.group(1).strip().strip(chr(34) + chr(39))
                if declared in NAMES:
                    errors.append("Packaged skill exposed outside package: " + str(alternate_manifest))
    print(json.dumps({
        "ok": not errors, "skills_checked": len(NAMES),
        "package_files": len(files), "package_symlinks": len(symlinks),
        "package_bytes": sum(p.stat().st_size for p in files),
        "local_references_checked": references,
        "client_packages_checked": client_packages,
        "client_entries_checked": client_entries, "errors": errors,
        "scope": "Package completeness and readable entry points; no model calls or publishing.",
    }, ensure_ascii=False, indent=2))
    return int(bool(errors))

if __name__ == "__main__":
    sys.exit(main())
