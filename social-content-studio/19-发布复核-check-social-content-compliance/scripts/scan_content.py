#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


SEVERITY_ORDER = {"high": 0, "medium": 1, "review": 2}
SEVERITY_LABEL = {"high": "高风险", "medium": "需修改", "review": "人工复核"}
NEGATION_OR_EDUCATION = re.compile(r"(?:禁止|严禁|避免|不要|不得|不能|不应|不可|违规词|违禁词|错误示例|反例|不代表|并非).{0,10}$")
REGULATED_PRODUCT_TYPES = {"drug", "device", "health-food", "medical-service"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan Xiaohongshu/Douyin content with the four-source compliance corpus.")
    parser.add_argument("--platform", choices=["xiaohongshu", "douyin", "both"], default="both")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--text-file")
    parser.add_argument(
        "--input-kind",
        choices=["auto", "title", "body", "voiceover", "subtitle", "ocr", "cover", "comment", "video"],
        default="auto",
    )
    parser.add_argument(
        "--product-type",
        choices=["unknown", "ordinary", "cosmetic", "drug", "device", "health-food", "medical-service"],
        default="unknown",
    )
    parser.add_argument("--commercial", choices=["unknown", "yes", "no"], default="unknown")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser.parse_args()


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text).lower()


def excerpt(text: str, start: int, end: int, radius: int = 38) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    return text[left:right].replace("\n", " ").strip()


def term_pattern(term: str) -> str:
    normalized = normalize(term)
    separator = r"[\s._·•*#~—\-\/]*"
    return separator.join(re.escape(char) for char in normalized)


def selected_platforms(platform: str) -> set[str]:
    return {"xiaohongshu", "douyin"} if platform == "both" else {platform}


def context_adjustment(
    text: str,
    start: int,
    severity: str,
    category: str,
    product_type: str,
    commercial: str,
) -> tuple[str, str | None]:
    before = text[max(0, start - 24) : start]
    if NEGATION_OR_EDUCATION.search(before):
        return "review", "命中词位于禁止、反例或教学语境附近，需确认截图/剪辑后限定语仍完整可见。"
    if product_type in REGULATED_PRODUCT_TYPES and any(word in category for word in ("医疗", "健康", "器械", "保健")):
        return "review", "属于受监管产品，需核对资质和获批宣传范围，不能仅凭关键词判断。"
    if commercial == "no" and severity == "high" and any(word in category for word in ("绝对化", "价格", "收益")):
        return "review", "当前标记为非商业内容，但仍需确认是否存在隐性推广、商品推荐或误导性事实陈述。"
    return severity, None


def add_finding(
    findings: list[dict],
    occupied: set[tuple[int, int]],
    *,
    text: str,
    start: int,
    end: int,
    matched: str,
    rule_term: str,
    severity: str,
    platforms: list[str],
    category: str,
    reason: str,
    suggestion: str,
    source_refs: list[str],
    layer: str,
    product_type: str,
    commercial: str,
    deduplicate_span: bool = True,
) -> None:
    span = (start, end)
    if deduplicate_span and span in occupied:
        return
    adjusted, context_note = context_adjustment(text, start, severity, category, product_type, commercial)
    findings.append(
        {
            "severity": adjusted,
            "platforms": platforms,
            "category": category,
            "matched": matched,
            "rule_term": rule_term,
            "excerpt": excerpt(text, start, end),
            "reason": reason,
            "suggestion": suggestion,
            "context_note": context_note,
            "source_refs": source_refs,
            "rule_layer": layer,
            "start": start,
            "end": end,
        }
    )
    occupied.add(span)


def scan_curated(
    text: str,
    normalized_text: str,
    platform: str,
    rules: list[dict],
    findings: list[dict],
    occupied: set[tuple[int, int]],
    product_type: str,
    commercial: str,
) -> None:
    selected = selected_platforms(platform)
    for rule in rules:
        active_platforms = [value for value in rule["platforms"] if value in selected]
        if not active_platforms:
            continue
        candidates = [(term, term_pattern(term)) for term in rule.get("terms", [])]
        candidates.extend((pattern, pattern) for pattern in rule.get("patterns", []))
        for label, pattern in candidates:
            for match in re.finditer(pattern, normalized_text, flags=re.IGNORECASE):
                add_finding(
                    findings,
                    occupied,
                    text=text,
                    start=match.start(),
                    end=match.end(),
                    matched=match.group(0),
                    rule_term=label,
                    severity=rule["severity"],
                    platforms=active_platforms,
                    category=rule["category"],
                    reason=rule["reason"],
                    suggestion=rule["suggestion"],
                    source_refs=rule.get("source_refs", []),
                    layer="curated",
                    product_type=product_type,
                    commercial=commercial,
                )


def scan_full_lexicon(
    text: str,
    normalized_text: str,
    platform: str,
    entries: list[dict],
    findings: list[dict],
    occupied: set[tuple[int, int]],
    product_type: str,
    commercial: str,
) -> None:
    selected = selected_platforms(platform)
    for entry in entries:
        active_platforms = [value for value in entry["platforms"] if value in selected]
        if not active_platforms:
            continue
        for term in entry.get("terms", []):
            for match in re.finditer(term_pattern(term), normalized_text, flags=re.IGNORECASE):
                severity = "review" if entry["match_mode"] == "context" else entry["severity"]
                add_finding(
                    findings,
                    occupied,
                    text=text,
                    start=match.start(),
                    end=match.end(),
                    matched=match.group(0),
                    rule_term=term,
                    severity=severity,
                    platforms=active_platforms,
                    category=entry["category"],
                    reason=entry["context_note"],
                    suggestion="核对完整语境、商品类别、证据和限定范围；不要只替换命中词。",
                    source_refs=[entry["source_ref"]],
                    layer="full-lexicon",
                    product_type=product_type,
                    commercial=commercial,
                )


def scan_behavior_signals(
    text: str,
    normalized_text: str,
    platform: str,
    rules: list[dict],
    findings: list[dict],
    occupied: set[tuple[int, int]],
    product_type: str,
    commercial: str,
) -> None:
    if platform not in {"douyin", "both"}:
        return
    for rule in rules:
        for signal in rule["signals"]:
            for match in re.finditer(term_pattern(signal), normalized_text, flags=re.IGNORECASE):
                add_finding(
                    findings,
                    occupied,
                    text=text,
                    start=match.start(),
                    end=match.end(),
                    matched=match.group(0),
                    rule_term=signal,
                    severity=rule["severity"],
                    platforms=["douyin"],
                    category=f"抖音行为 {rule['number']:02d}：{rule['title']}",
                    reason="口播、脚本或画面计划触发了抖音 34 类行为检查信号。",
                    suggestion=rule["safer_direction"],
                    source_refs=rule["source_ref"],
                    layer="behavior",
                    product_type=product_type,
                    commercial=commercial,
                    deduplicate_span=False,
                )


def deduplicate_findings(findings: list[dict]) -> list[dict]:
    layer_priority = {"curated": 0, "behavior": 1, "full-lexicon": 2}
    candidates = sorted(
        findings,
        key=lambda item: (
            layer_priority[item["rule_layer"]],
            item["start"],
            -(item["end"] - item["start"]),
            SEVERITY_ORDER[item["severity"]],
        ),
    )
    accepted: list[dict] = []
    for item in candidates:
        if any(
            existing["start"] <= item["start"]
            and existing["end"] >= item["end"]
            and SEVERITY_ORDER[existing["severity"]] < SEVERITY_ORDER[item["severity"]]
            and set(existing["platforms"]).issuperset(item["platforms"])
            for existing in accepted
        ):
            continue
        if item["rule_layer"] == "full-lexicon" and any(
            existing["rule_layer"] == "curated"
            and existing["start"] <= item["start"]
            and existing["end"] >= item["end"]
            for existing in accepted
        ):
            continue
        same_category_overlap = next(
            (
                existing
                for existing in accepted
                if existing["category"] == item["category"]
                and max(existing["start"], item["start"]) < min(existing["end"], item["end"])
            ),
            None,
        )
        if same_category_overlap is not None:
            continue
        accepted.append(item)
    accepted.sort(key=lambda item: (SEVERITY_ORDER[item["severity"]], item["start"], item["end"]))
    return accepted


def scan(text: str, args: argparse.Namespace, reference_dir: Path) -> dict:
    normalized_text = normalize(text)
    curated = json.loads((reference_dir / "rules.json").read_text(encoding="utf-8"))
    lexicon = json.loads((reference_dir / "full-terms.json").read_text(encoding="utf-8"))
    behaviors = json.loads((reference_dir / "behavior-rules.json").read_text(encoding="utf-8"))
    coverage = json.loads((reference_dir / "coverage.json").read_text(encoding="utf-8"))
    findings: list[dict] = []
    occupied: set[tuple[int, int]] = set()
    scan_curated(text, normalized_text, args.platform, curated["rules"], findings, occupied, args.product_type, args.commercial)
    scan_full_lexicon(text, normalized_text, args.platform, lexicon["entries"], findings, occupied, args.product_type, args.commercial)
    scan_behavior_signals(text, normalized_text, args.platform, behaviors["rules"], findings, occupied, args.product_type, args.commercial)
    findings = deduplicate_findings(findings)
    counts = Counter(item["severity"] for item in findings)
    return {
        "platform": args.platform,
        "input_kind": args.input_kind,
        "product_type": args.product_type,
        "commercial": args.commercial,
        "rule_version": curated["version"],
        "coverage_version": coverage["version"],
        "coverage_scope": coverage["scope_statement"],
        "counts": {key: counts.get(key, 0) for key in ("high", "medium", "review")},
        "findings": findings,
        "behavior_rules_requiring_visual_review": 34 if args.platform in {"douyin", "both"} else 0,
    }


def render_markdown(result: dict) -> str:
    findings = result["findings"]
    counts = result["counts"]
    lines = [
        "# 发布前合规初筛",
        "",
        f"- 平台：{result['platform']}",
        f"- 输入类型：{result['input_kind']}",
        f"- 商品类型：{result['product_type']}",
        f"- 命中：高风险 {counts['high']} / 需修改 {counts['medium']} / 人工复核 {counts['review']}",
        "",
        "## 结论",
        "",
    ]
    if findings:
        highest = SEVERITY_LABEL[findings[0]["severity"]]
        lines.append(f"最高风险级别：**{highest}**。命中只是定位证据，需结合完整语境、画面、商品资质和平台当前规则判断。")
    else:
        lines.append("未发现明显的文字规则命中；这不等于视频或文案保证合规，仍需完成下方非文本检查。")
    lines += ["", "## 命中项", ""]
    if not findings:
        lines.append("无文字命中。")
    for index, item in enumerate(findings, start=1):
        platforms = ", ".join(item["platforms"])
        lines += [
            f"### {index}. {SEVERITY_LABEL[item['severity']]} | {platforms} | {item['category']}",
            "",
            f"- 证据：`{item['excerpt']}`",
            f"- 命中：`{item['matched']}`",
            f"- 原因：{item['reason']}",
            f"- 最小修改：{item['suggestion']}",
        ]
        if item.get("context_note"):
            lines.append(f"- 语境提示：{item['context_note']}")
        if item.get("source_refs"):
            lines.append(f"- 来源索引：{'；'.join(item['source_refs'])}")
        lines.append("")
    lines += [
        "## 非文本必检",
        "",
        "- [ ] 标题、正文、话题、置顶评论、简介和商品卡",
        "- [ ] 全部口播、字幕、贴纸、弹幕、封面字和画面 OCR",
        "- [ ] 二维码、手机号、账号、外链、其他平台水印和站外交易暗示",
        "- [ ] 商品、价格、库存、活动时间、赠品、对比实验和资质证据是否一致",
        "- [ ] 人物年龄、裸露/纹身、烟酒、武器、危险动作、医疗操作和敏感场景",
        "- [ ] 音乐、图片、视频、脚本版权，以及 AI/商业合作标注",
        "- [ ] 抖音发布时逐项核对 34 类行为规则，不可只凭干净的口播稿放行",
        "",
        "## 边界",
        "",
        "覆盖用户提供的四份资料，但平台规则会更新；这是发布前风险筛查，不代表平台最终审核结果。不得用谐音、空格、符号、emoji 或暗语规避审核。",
    ]
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    text = Path(args.text_file).read_text(encoding="utf-8") if args.text_file else args.text
    reference_dir = Path(__file__).resolve().parent.parent / "references"
    result = scan(text, args, reference_dir)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
