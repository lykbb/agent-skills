---
name: check-social-content-compliance
description: Comprehensive pre-publication compliance review for Xiaohongshu and Douyin. Check titles, copy, hashtags, comments, voiceovers, transcripts, subtitles, OCR, covers, product cards, screenshots, videos, livestream plans, claims, disclosures, and visual behavior. Use when the user asks to查违规、查违禁词、查口播、审文案、查限流风险、检查视频/字幕/画面、发布前过审，或希望在不改变原意的前提下改得更稳妥。
---

# Social Content Compliance Review

Use this one skill for copy, voiceover, subtitle, image, video, and livestream risk checks. It contains the complete extracted corpus of the user's four source files, a compiled 24-column advertising lexicon, curated cross-platform rules, and Douyin's 34 behavior categories.

## State the boundary correctly

- Say `覆盖用户提供的四份资料` rather than `覆盖所有平台未来规则`.
- Treat every keyword hit as evidence to inspect, not an automatic violation.
- Platform rules, laws, category permissions, and enforcement can change. For a current definitive answer, regulated product, or high-stakes claim, verify current official rules before final approval.
- Never promise `一定过审`, `零违规`, or `不会限流`.
- Never recommend homophones, spaces, symbols, emoji, pinyin, gestures, or euphemisms to evade detection. Rewrite or remove the underlying claim or behavior.

## 1. Establish the review scope

Infer what is available and continue without blocking when possible. Record:

- target platform: `xiaohongshu`, `douyin`, or `both` when unknown/cross-posted;
- input type: title, body, voiceover, subtitle, OCR, cover, comment, image, video, or livestream plan;
- whether the content is commercial, sponsored, affiliate, product-linked, or purely editorial;
- product type: ordinary product, cosmetic, drug, medical device, health food, medical service, or unknown;
- evidence references: line number, field name, screenshot region, or timestamp.

Product type and commercial context change the conclusion. Do not judge a medical-device claim as if it were an ordinary product, and do not treat a quoted prohibition as the creator's own promise.

## 2. Build one unified review corpus

Label each channel before scanning so the report can point back to the source:

```text
[标题] ...
[正文] ...
[话题] ...
[置顶评论] ...
[口播 00:00-00:08] ...
[字幕 00:00-00:08] ...
[OCR/封面] ...
[商品卡/价格/活动] ...
[画面动作 00:00-00:08] ...
[AI/商业/版权标注] ...
```

For video or livestream material, review all of these layers:

1. Spoken language: transcript, filler words, spontaneous claims, background speech, and song/recording content that remains audible.
2. Visible language: hard subtitles, stickers, bullet comments, backdrop, package text, price cards, QR/contact details, cover, ending card, and OCR.
3. Visual behavior: people, age, clothing/exposure, tattoos, smoke/alcohol, weapons, dangerous acts, medical procedures, violence, fake experiments, giveaways, and product demonstrations.
4. Transaction flow: product card, link, price, inventory, activity dates, gift conditions, shipping promises, private contact, and off-platform payment.
5. Provenance and disclosure: copyright/authorization, commercial cooperation, AI generation/assistance, credentials, data sources, and before/after evidence.

Inspect the beginning, ending, every scene change, and every flagged timestamp. A clean transcript does not prove a clean video.

## 3. Run the deterministic scan

Use the bundled scanner as the first pass:

```bash
python scripts/scan_text.py \
  --platform both \
  --input-kind voiceover \
  --product-type unknown \
  --commercial unknown \
  --text-file /path/to/review-corpus.txt \
  --format markdown
```

Options:

- `--platform`: `xiaohongshu`, `douyin`, or `both`.
- `--input-kind`: `title`, `body`, `voiceover`, `subtitle`, `ocr`, `cover`, `comment`, `video`, or `auto`.
- `--product-type`: `ordinary`, `cosmetic`, `drug`, `device`, `health-food`, `medical-service`, or `unknown`.
- `--commercial`: `yes`, `no`, or `unknown`.
- `--format json` for structured downstream processing.

The scanner uses three layers in order:

1. `references/rules.json`: curated strong claims and patterns.
2. `references/full-terms.json`: every non-empty source cell from row 4 onward in the 24-column `违禁词.xlsx` matrix.
3. `references/behavior-rules.json`: all 34 Douyin behavior categories and text-planning signals.

Do not stop at the scanner. It cannot prove visual safety, authorization, truthfulness, product eligibility, or current platform policy.

## 4. Complete the contextual and visual review

Read `references/rules.md` and check every applicable family:

- absolute, ranking, authority, test-data, price, inventory, deadline, guarantee, income, or course-outcome claims;
- medical, health, cosmetic, weight-loss, disinfectant, drug, device, health-food, and medical-service claims;
- private contact, QR codes, off-platform transactions, other-platform promotion, and meaningless interaction tied to benefits;
- fake scarcity, fake giveaways, induced flash sales, false experiments, malicious comparisons, mismatched product cards, and review cashback;
- originality, copyright, other-platform watermarks, fake identity/credentials, privacy, AI labels, and commercial disclosures;
- minors, nudity/sexualization, tattoos, tobacco/alcohol, weapons, drugs, gambling, self-harm, violence, dangerous stunts, political/hate content, rumors, and superstition;
- livestream-specific process risks such as recording/hanging, no real-time interaction, non-self real-name use, overseas broadcast, universal links, and mass private messages.

For Douyin, read all of `references/behavior-rules.json` and mark each of the 34 items `present`, `absent`, `unclear`, or `not applicable`. Do not replace this with keyword matching.

For Xiaohongshu, also check:

- title/body/cover/hashtag relevance and keyword stuffing;
- fake planting, undisclosed promotion, copied selection/structure, excessive retouching, and unlabelled AI assistance when required;
- competitor-platform mention versus actual transaction routing;
- whether a traffic-optimization suggestion conflicts with compliance. Interaction tactics in a traffic guide are not automatically safe CTAs.

## 5. Decide risk with context

Use these levels:

- `高风险`: strong legal/platform risk, serious misleading claim, prohibited transaction route, dangerous content, or behavior that should be removed before publishing.
- `需修改`: meaningful risk, missing boundary, incomplete activity rule, unsupported data, or wording that should be narrowed.
- `人工复核`: context-dependent word, regulated-category boundary, visual-only issue, quotation/education context, unclear proof, or source/current-rule uncertainty.
- `未发现明显风险`: no obvious issue in the material actually reviewed. Never call this guaranteed compliant.

Apply these context rules:

- Downgrade clear prohibitions, criticism, news reporting, legal education, or quoted bad examples when the full qualifier remains visible/audible.
- Keep the hit visible if cropping, subtitles, cover text, or a short clip could remove the qualifier.
- Upgrade commercial promises, health outcomes, private-contact CTAs, fabricated scarcity, unfulfilled benefits, or dangerous demonstrations.
- Do not flag bare single characters such as `最`, `首`, `一`, `顶`, or `极`; inspect the complete advertising phrase.
- Require proof for rankings, sales numbers, percentages, experiments, certifications, endorsements, comparisons, test results, and time-limited offers.

## 6. Give minimal, usable revisions

- Preserve the user's structure, tone, and intent.
- Change only risky lines unless a complete rewrite is requested.
- Remove the underlying misleading claim instead of swapping one risky synonym for another.
- A safer sentence must remain truthful; do not invent data, authorization, user experience, product scope, or disclaimers.
- For activity/price copy, include actual dates, inventory, product details, restrictions, presale status, and fulfillment conditions.
- For health/beauty content, describe truthful ingredients, usage, texture, or personal records without promising treatment or guaranteed outcomes.
- For private-routing content, use only the platform's permitted product card, shop, search, or disclosure flow.

## 7. Produce the final report

Follow `references/report-template.md`. Every finding must include:

1. level, platform, and channel;
2. exact excerpt/timestamp/frame;
3. risk category and contextual reason;
4. source index or current official rule when verified;
5. minimal revision or operational fix;
6. what still requires manual proof or visual review.

Always include a coverage statement listing what was and was not reviewed. If the user gave only a script, say that the final video's visuals, OCR, music, product card, disclosures, and live behavior remain unchecked.

## Reference routing

- `references/rules.md`: human review matrix and platform-specific checks.
- `references/report-template.md`: required output structure.
- `references/source-notes.md`: provenance, authority limits, and conflicting-source handling.
- `references/coverage.json`: exact source and compilation counts.
- `references/rules.json`: curated deterministic rules.
- `references/full-terms.json`: source-complete spreadsheet lexicon.
- `references/behavior-rules.json`: all 34 Douyin behaviors.
- `references/source-corpus.json`: complete extracted source records; load only for audit, disputes, or source lookup because it is large.

Run `python scripts/audit_coverage.py` after changing any rule resource. Use `scripts/build_full_corpus.py` only when rebuilding from the four source attachments.
