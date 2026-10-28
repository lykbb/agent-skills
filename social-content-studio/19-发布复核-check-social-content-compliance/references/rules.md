# Human Review Matrix

Use this after the deterministic scanner. A match locates evidence; the conclusion depends on full language, visuals, product type, proof, transaction flow, and current platform rules.

## Review every content channel

| Channel | Required checks |
| --- | --- |
| Title and cover | absolute claims, clickbait, medical/price promises, visible platform marks, AI/commercial label |
| Body and hashtags | full claim context, keyword stuffing, category/hashtag mismatch, disclosure, sources |
| Voiceover and background audio | spontaneous promises, euphemisms, background speech/music, call-to-action |
| Subtitles, stickers, backdrop, bullet comments | cropped qualifiers, hidden contact cues, price/activity terms, induced interaction |
| OCR and packaging | QR/phone/account, certification, ingredients, dosage, effect, competitor/platform name |
| Product card and transaction flow | item/link match, price, inventory, deadline, gifts, shipping, presale, platform-native checkout |
| Visual actions | people/age, clothing, tattoos, smoke/alcohol, weapons, danger, violence, medical acts, fake experiments |
| Provenance and disclosures | copyright, authorization, data/test source, commercial cooperation, AI generation/assistance |

## Claim and wording risks

### Absolute, ranking, uniqueness, and guarantee

Review complete phrases involving `最`, `第一`, `唯一`, `首`, `顶`, `国家级`, `世界级`, `100%`, `永久`, `绝对`, `保证`, or `零风险`. Do not flag a bare single character. Ask:

- Is the statement commercial or tied to a product/service?
- What is the comparison scope, time period, sample, method, and source?
- Is the evidence current and authorized for public use?
- Will a cover crop or short clip remove the qualifier?

### Authority, certification, endorsement, and data

Require proof and permission for government/army/expert endorsement, official certification, inspection exemption, awards, rankings, sales numbers, clinical results, percentages, laboratory tests, patents, and comparison claims. Do not invent a citation or turn an unverified statement into `据说`.

### Medical, health, cosmetics, body, and regulated products

First identify the product:

- ordinary product or food;
- cosmetic or special cosmetic;
- drug or OTC drug;
- medical device;
- health food;
- medical/beauty service.

For ordinary products, disease treatment/prevention, sterilization, physiological change, immunity, sleep, blood pressure/glucose, fixed-time weight loss, hormone, hair regrowth, scar removal, or similar drug-like outcomes are high risk. Regulated products still need the correct account qualification and claims within the approved scope.

Visual checks include injection/procedure footage, before/after images, fake bread/fruit experiments, excessive retouching, magnified skin defects, certificates, dosage, and product packaging.

### Finance, income, recruitment, courses, education, and employment

Review guaranteed returns, zero risk, guaranteed employment/pass/traffic, `轻松赚钱`, fixed income, agent recruitment, franchise recruitment, and paid courses sold as a guaranteed path to results. State real costs, conditions, uncertainty, and failure risk.

### Price, inventory, deadlines, gifts, and flash sales

Verify:

- actual original/reference price and comparison basis;
- exact start/end date and time;
- inventory and geographic/shipping restrictions;
- product brand/name/core parameters;
- gift quantity and merchant agreement;
- presale status and fulfillment time;
- whether the promised price/product is actually listed.

`限时`, `秒杀`, `最后`, `免费送`, or `仅剩` without complete, truthful conditions requires revision. False countdowns, non-existent stock, unfulfilled gifts, or unlimited-free promises are high risk.

### Induced interaction and fake benefits

High-risk structures bind meaningless interaction to benefits: comment codes, repeated `666`, likes, watch duration, follow, group joining, shipping, price change, qualification, inventory release, or gift eligibility. Normal conversation is different from making interaction a false precondition.

### Private contact and off-platform routing

Inspect words, QR codes, account IDs, phone numbers, gestures, package labels, comments, profile text, and link instructions. Risk increases when users are asked to contact privately, pay externally, use another marketplace, or bypass the platform. A neutral platform mention can be manual review; a transaction instruction is high risk.

### Superstition, pseudoscience, and sensitive claims

Do not sell luck, wealth, exorcism, fortune, feng shui, religion, or pseudoscience as a guaranteed effect. Review discrimination, hate, political extremism, rumors, terrorism, obscenity, sexual content, self-harm, violence, gambling, drugs, weapons, and dangerous mimetic detail.

## Authenticity, provenance, and disclosure

### Commercial content

Check whether there is payment, free product, affiliate commission, brand control, shop/product card, or another interest relationship. Confirm current platform reporting and disclosure requirements. Do not present paid or exchanged content as an independent self-use review.

### AI-generated or assisted content

Check text, image, video, voice, avatar, face swap, and synthetic scenes. Determine whether the platform's current rule requires a publishing setting, visible label, or both. Do not assume one fixed label works forever.

### Originality and copyright

Check script similarity, copied selection/structure, footage, images, music, fonts, screenshots, logos, user comments, and other-platform watermarks. Confirm permission and keep proof. `二次剪辑` alone does not guarantee originality or permission.

### Identity, credentials, privacy, and impersonation

Check fake education/job/medical credentials, official/media impersonation, unauthorized events, net-image avatars presented as real, phone/address/ID information, patient/user data, and third-party QR codes.

## Visual and behavior risks

### People and bodies

- minors independently livestreaming, explaining, promoting, or acting as disallowed endorsers;
- nudity, sexualized clothing/actions, low俗 gestures, or exploitative use of vulnerable people;
- prolonged prominent tattoos where the platform/context makes this risky;
- smoking, drinking, smoke, lighters, alcohol bottles, or intoxication;
- non-consensual filming, privacy exposure, humiliation, bullying, or harassment.

### Dangerous, illegal, or harmful acts

- drugs, guns including replicas/toys, controlled knives, gambling, illegal trade;
- injections, medication, unqualified medical procedures, toxic ingestion, excessive eating, fire/electricity/height/traffic stunts;
- violence, smashing/cutting, threats, gang/loan plots, self-harm, or imitable harmful instructions;
- accident/disaster livestreams or exploitation of people without full civil capacity.

### Misleading demonstrations and selling behavior

- malicious competitor comparison or deliberately unfair conditions;
- fabricated price cutting, fake tragedy, fake patriotism, exaggerated drama, fake recruiting, or false fan benefits;
- product shown in the content differing from the product card/link;
- universal links, unrelated shopping carts, review cashback, mass private links, or platform-external draws;
- recorded/hanging livestream, black screen, looped audio/video, no real-time interaction, or long host absence.

## Xiaohongshu-specific review

- Check title, cover, first paragraph, hashtags, and product/category consistency; flag stuffing rather than naturally used keywords.
- Review false planting, copied selection/structure, undisclosed promotion, excessive retouching, medical/beauty outcomes, and external routing.
- Treat other-platform names as context-dependent unless paired with a transaction/private-contact instruction.
- Do not assume interaction advice in a traffic guide is compliant. `评论区扣1` or similar CTAs must still pass inducement and benefit checks.
- Traffic formulas, ratios, and dates in secondary notes are not official proof; do not cite them as guaranteed ranking logic.

## Douyin-specific review

Open `behavior-rules.json` and assess all 34 rules. Each rule covers voiceover, subtitle, sticker, bullet comment, backdrop, visual action, product card, and livestream process. Record `present`, `absent`, `unclear`, or `not applicable`.

Important conflict: source page 11 suggests replacing `钱` with `米`. Do not follow it. Treat `钱/米` and similar euphemisms as context signals and remove deceptive or risky money/transaction claims instead of evading detection.

## Context downgrades

Consider manual review instead of a violation conclusion when the hit is:

- a clearly visible/audible prohibition or bad-example label;
- criticism, fact-checking, law/policy education, or news reporting;
- an accurate product category/legal name rather than a promised outcome;
- a quotation with an intact qualifier and no commercial endorsement;
- a regulated product claim that may be authorized but still needs scope verification.

Do not hide the finding when a thumbnail, subtitle, edit, or short clip could strip away the qualifier.

## Safe revision principles

- Absolute claim -> bounded, truthful observation with scope/evidence.
- Guaranteed effect -> documented process or personal record without result promise.
- Medical promise -> approved product wording or non-medical feature only when true.
- Fake scarcity -> actual time, inventory, conditions, price basis, and fulfillment.
- Private CTA -> platform-permitted product card/shop/search/disclosure flow.
- Induced interaction -> ordinary non-benefit-linked conversation.
- Evasion language -> remove the risky mechanism; never disguise it.
