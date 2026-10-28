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


if __name__ == "__main__":
    unittest.main()
