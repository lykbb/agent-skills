# Source Notes and Authority Boundaries

The corpus was rebuilt on 2026-07-18 from four attachments read from the user's Feishu Base. The attachments were downloaded temporarily for extraction and visual review. No skill content was uploaded or written back to Feishu.

The original attachment binaries are intentionally not bundled in the skill. `source-corpus.json` and `coverage.json` retain each source file's SHA-256 fingerprint; `scripts/build_full_corpus.py` can rebuild the derived resources when the four attachments are supplied again, and the hashes can confirm whether they are the same files.

## 1. 小红书官方流量推送机制.docx

- Extracted: 234 non-empty OOXML text records, 7 rendered pages, no embedded media files.
- The document describes itself as a June 2026 compilation based on official and industry public information.
- It does not provide enough primary-source links to treat each formula, percentage, threshold, model name, or date as a confirmed current official rule.
- Use its compliance-related items as traffic-risk context, not as guaranteed ranking logic.

## 2. 小红书违禁词合规手册 (2).docx

- Extracted: 385 non-empty OOXML text records, 14 rendered pages, no embedded media files.
- The document identifies `亚莎` as compiler and is a secondary handbook, not a platform-issued policy file.
- Dates, penalty percentages, legal conclusions, and claims described as latest rules require current official verification before definitive use.
- Its word lists and checklists are useful as conservative pre-publication signals.

## 3. 违禁词.xlsx

- Extracted: 1 worksheet, 24 columns, 1016 non-empty cells, with actual content through row 236. The workbook's styled worksheet dimension extends farther, but rows after 236 contain no values.
- Compiled: all 989 non-empty cells from row 4 onward have a corresponding lexicon record in `full-terms.json`.
- The 24 columns cover absolute/authority/guarantee/finance/medical/superstition terms and special industries such as cosmetics, devices, health food, alcohol, infant formula, education, disinfectants, real estate, and medical services.
- The workbook itself warns that many items require the complete advertising context, subjective scope, product qualification, and supporting evidence. Do not turn the matrix into an unconditional word blacklist.

## 4. 抖音全套违禁词与违规行为规避指南.pdf

- Extracted: 22 pages, 21 pages with text, and a final visual back cover with no new rule text.
- The file is branded `交个朋友电商学苑` and is secondary training material, not an official current Douyin policy export.
- It contains ten wording families, 34 behavior categories, penalty tables, examples, and quiz material.
- Some pages suggest homophones, gestures, repeated words, or euphemisms such as using `米` for `钱`. These are not adopted. The skill explicitly rejects evasion and rewrites the underlying claim or behavior.

## Conflict handling

- A traffic suggestion is not automatically compliant. For example, the traffic document gives a `评论区扣1/扣2` interaction example, while the compliance handbook and Douyin material treat benefit-linked or meaningless coded comments as risky. Use the stricter interpretation and inspect whether a benefit, qualification, shipping, or price is attached.
- Replacement examples in secondary training material may themselves be misleading or evasive. A rewrite must be independently truthful and within product/platform scope.
- When the four sources conflict, prioritize current law and current official platform rules, then the safer interpretation. State uncertainty instead of inventing certainty.

## Coverage claim

`Complete` means complete relative to the extractable text, spreadsheet cells, and visually reviewed pages of these four supplied files. It does not mean every future platform rule, every legal jurisdiction, or every enforcement decision is covered.
