from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCANNER = ROOT / "scripts" / "scan_text.py"


def run_scan(text: str, *extra: str) -> dict:
    command = [
        sys.executable,
        str(SCANNER),
        "--platform",
        "both",
        "--text",
        text,
        "--format",
        "json",
        *extra,
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(completed.stdout)


class ScannerTests(unittest.TestCase):
    def test_combined_copy_risks(self):
        result = run_scan("全网第一，100%有效，三天瘦十斤。评论区扣666领福利，我私信发你微信二维码，靠它月入六位数。")
        categories = "\n".join(item["category"] for item in result["findings"])
        self.assertIn("绝对化", categories)
        self.assertIn("医疗", categories)
        self.assertIn("诱导互动", categories)
        self.assertIn("私下联系", categories)
        self.assertIn("金融收益", categories)

    def test_negated_educational_context_is_manual_review(self):
        result = run_scan("发布普通食品时，禁止宣称治疗疾病，也不要写根治。")
        self.assertTrue(result["findings"])
        self.assertTrue(all(item["severity"] == "review" for item in result["findings"]))

    def test_common_word_is_not_automatic_high_risk(self):
        result = run_scan("这个产品的外壳设计让我觉得使用起来比较安全。")
        safety = [item for item in result["findings"] if item["matched"].replace(" ", "") == "安全"]
        self.assertTrue(safety)
        self.assertTrue(all(item["severity"] == "review" for item in safety))

    def test_obfuscated_private_contact_is_detected(self):
        result = run_scan("想了解的话可以加 微 信，我发外部链接。")
        self.assertTrue(any("私下联系" in item["category"] for item in result["findings"]))

    def test_douyin_behavior_signal_is_detected(self):
        result = run_scan("直播时让未成年人口播带货，再拿仿真枪砸竞品，还让大家扣666领福利。")
        self.assertTrue(any("毒品武器" in item["category"] or "危险" in item["category"] for item in result["findings"]))
        self.assertTrue(any("未成年人" in item["category"] for item in result["findings"]))

    def test_regulated_product_requires_scope_review(self):
        result = run_scan("用于治疗相关症状。", "--product-type", "device")
        medical = [item for item in result["findings"] if "医疗" in item["category"] or "健康" in item["category"]]
        self.assertTrue(medical)
        self.assertTrue(all(item["severity"] == "review" for item in medical))

    def test_all_34_behavior_numbers_can_surface_in_report(self):
        behavior_payload = json.loads((ROOT / "references" / "behavior-rules.json").read_text(encoding="utf-8"))
        text = "；".join(rule["signals"][0] for rule in behavior_payload["rules"])
        result = run_scan(text)
        behavior_numbers = {
            int(item["category"].split("：", 1)[0].split()[-1])
            for item in result["findings"]
            if item["category"].startswith("抖音行为 ")
        }
        self.assertEqual(behavior_numbers, set(range(1, 35)))

    def test_latin_terms_do_not_fire_inside_longer_english_words(self):
        result = run_scan("这个 product 是今年的 PROJECT，先在 desktop 上跑通，maximum 并发先不调，CTO 也同意，Act 和 Stop 两个按钮先不做。")
        matched = {item["matched"] for item in result["findings"]}
        self.assertFalse(matched & {"ct", "top", "max"})

    def test_latin_terms_still_fire_as_standalone_words(self):
        result = run_scan("做了CT检查，销量TOP1，含hEGF成分，Top-K 也算，还有 ProMax 和两个 MVPs。")
        matched = [item["matched"] for item in result["findings"]]
        self.assertIn("ct", matched)
        self.assertIn("egf", matched)
        self.assertIn("max", matched)
        self.assertIn("mvp", matched)
        self.assertEqual(matched.count("top"), 2)

    def test_short_lexicon_terms_are_hints_for_non_commercial_content(self):
        text = "我试用了这个智能排序功能，用户还愿意继续用。"
        graded = run_scan(text)
        self.assertTrue(any(item["severity"] in {"high", "medium"} for item in graded["findings"]))
        self.assertEqual(graded["counts"]["hint"], 0)
        relaxed = run_scan(text, "--commercial", "no")
        self.assertEqual({item["matched"] for item in relaxed["findings"]}, {item["matched"] for item in graded["findings"]})
        self.assertTrue(all(item["severity"] == "hint" for item in relaxed["findings"]))
        self.assertEqual(relaxed["counts"]["high"] + relaxed["counts"]["medium"] + relaxed["counts"]["review"], 0)

    def test_strong_claims_stay_graded_for_non_commercial_content(self):
        result = run_scan("这款茶能延年益寿，想了解可以加微信。", "--commercial", "no")
        graded = {item["matched"]: item["severity"] for item in result["findings"]}
        self.assertEqual(graded.get("延年益寿"), "high")
        self.assertTrue(
            any("私下联系" in item["category"] and item["severity"] == "high" for item in result["findings"])
        )

    def test_hint_does_not_mask_overlapping_graded_term(self):
        result = run_scan("这是中医院自制的药膏。", "--commercial", "no")
        graded = {item["matched"]: item["severity"] for item in result["findings"]}
        self.assertEqual(graded.get("中医"), "hint")
        self.assertEqual(graded.get("医院自制"), "high")

    def test_markdown_folds_hints_into_one_line_per_term(self):
        text = "第一步先写一段，第一版再改一段。"
        command = [
            sys.executable,
            str(SCANNER),
            "--platform",
            "both",
            "--text",
            text,
            "--commercial",
            "no",
            "--format",
            "markdown",
        ]
        report = subprocess.run(command, check=True, capture_output=True, text=True).stdout
        self.assertIn("短词提示 4", report)
        self.assertIn("无需要定级的文字命中。", report)
        self.assertEqual(report.count("- `第一` ×2"), 1)
        self.assertEqual(report.count("- `一段` ×2"), 1)


if __name__ == "__main__":
    unittest.main()
