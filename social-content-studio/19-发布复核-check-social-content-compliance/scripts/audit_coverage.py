#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "references"


def load(name: str):
    return json.loads((REF / name).read_text(encoding="utf-8"))


def main() -> int:
    corpus = load("source-corpus.json")
    lexicon = load("full-terms.json")
    behaviors = load("behavior-rules.json")
    rules = load("rules.json")
    coverage = load("coverage.json")
    sources = corpus["sources"]
    xlsx_records = [
        record
        for sheet in sources["prohibited_terms"]["sheets"]
        for record in sheet["records"]
    ]
    expected_lexicon_ids = {
        f"xlsx-{record['sheet']}-{record['coordinate']}"
        for record in xlsx_records
        if record["row"] >= 4
    }
    actual_lexicon_ids = {entry["id"] for entry in lexicon["entries"]}
    required_files = [
        ROOT / "SKILL.md",
        ROOT / "agents" / "openai.yaml",
        ROOT / "scripts" / "scan_text.py",
        ROOT / "scripts" / "scan_content.py",
        ROOT / "scripts" / "build_full_corpus.py",
        ROOT / "scripts" / "audit_coverage.py",
        ROOT / "tests" / "test_scan_content.py",
        ROOT / "examples" / "example-review.md",
        REF / "rules.json",
        REF / "rules.md",
        REF / "full-terms.json",
        REF / "behavior-rules.json",
        REF / "source-corpus.json",
        REF / "coverage.json",
        REF / "source-notes.md",
        REF / "report-template.md",
    ]
    checks = {
        "traffic_records_234": sources["xiaohongshu_traffic"]["record_count"] == 234,
        "xiaohongshu_compliance_records_385": sources["xiaohongshu_compliance"]["record_count"] == 385,
        "xlsx_nonempty_cells_1016": sources["prohibited_terms"]["record_count"] == 1016,
        "xlsx_actual_content_through_row_236": sources["prohibited_terms"]["sheets"][0]["last_content_row"] == 236,
        "every_xlsx_row4plus_cell_has_one_lexicon_record": expected_lexicon_ids == actual_lexicon_ids,
        "lexicon_record_count_989": len(lexicon["entries"]) == 989,
        "pdf_pages_22": sources["douyin_guide"]["page_count"] == 22,
        "pdf_nonempty_text_pages_21": sources["douyin_guide"]["nonempty_text_pages"] == 21,
        "page_22_visual_back_cover_reviewed": sources["douyin_guide"]["pages"][21]["visual_note"] == "封底，无新增规则",
        "douyin_behavior_rules_1_through_34": [item["number"] for item in behaviors["rules"]] == list(range(1, 35)),
        "curated_rule_count_at_least_20": len(rules["rules"]) >= 20,
        "all_curated_regex_patterns_compile": all(
            re.compile(pattern) is not None
            for rule in rules["rules"]
            for pattern in rule.get("patterns", [])
        ),
        "coverage_builder_checks_true": all(coverage["checks"].values()),
        "coverage_source_hashes_match_corpus": coverage["source_sha256"]
        == {key: value["sha256"] for key, value in sources.items()},
        "all_required_files_exist": all(path.is_file() for path in required_files),
    }
    result = {
        "ok": all(checks.values()),
        "checks": checks,
        "counts": {
            "traffic_records": sources["xiaohongshu_traffic"]["record_count"],
            "xiaohongshu_compliance_records": sources["xiaohongshu_compliance"]["record_count"],
            "xlsx_nonempty_cells": sources["prohibited_terms"]["record_count"],
            "xlsx_lexicon_records": len(lexicon["entries"]),
            "pdf_pages": sources["douyin_guide"]["page_count"],
            "douyin_behavior_rules": len(behaviors["rules"]),
            "curated_rules": len(rules["rules"]),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
