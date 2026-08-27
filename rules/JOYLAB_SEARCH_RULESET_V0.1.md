# JOYLAB SEARCH RULESET V0.1

Status: **FROZEN FOR V0.1**

Purpose: define deterministic PASS / FAIL / UNKNOWN decisions for JoyLab finance, investment, technology, and market content audits.

## Global decision rule

- `PASS`: every mandatory check in the gate passes and no blocking condition exists.
- `FAIL`: at least one blocking condition is confirmed.
- `UNKNOWN`: evidence required for a mandatory check is missing, inaccessible, ambiguous, or cannot be verified.
- `UNKNOWN` is never treated as `PASS`.
- Overall document status is `PASS` only when G1-G5 are all `PASS`.
- Any `FAIL` makes the overall status `FAIL`.
- If there is no `FAIL` but one or more gates are `UNKNOWN`, overall status is `UNKNOWN / RELEASE HOLD`.

## G1 — Source Gate

### PASS
All material factual claims have traceable evidence, and finance-critical claims use an acceptable source tier.

Accepted hierarchy:
1. Tier 1 — company IR, regulatory filing, exchange, government, central bank, official statistics.
2. Tier 2 — high-quality wire or major financial publication reporting a clearly attributable fact.
3. Tier 3 — general media or analyst material; usable only when the claim is non-critical or corroborated.
4. Tier 4 — blogs, social media, forums, anonymous/community posts; never sufficient alone for a material investment fact.

### FAIL
- A material factual claim has no source.
- A Tier 4 source is the sole basis of a material investment fact.
- The cited source does not support the claim.
- The content fabricates, alters, or misattributes a source.

### UNKNOWN
- A source is named but cannot be opened or matched to the claim.
- The provenance of a key number cannot be determined.
- Source tier cannot be established.

## G2 — Freshness Gate

Required metadata for time-sensitive market or finance content:
- `source_date`
- `observed_at`
- `data_period`
- `updated_at`

### PASS
- Required date metadata exists for all time-sensitive facts.
- The text clearly distinguishes reporting period from publication/observation time.
- No stale observation is presented as current.

### FAIL
- A stale value is described as current/latest.
- The reporting period is materially misstated.
- Current-price/current-market language is used without a current observation timestamp.

### UNKNOWN
- One or more required dates are missing for a material time-sensitive fact.
- It is impossible to establish whether the observation is stale.

## G3 — Fact Separation Gate

Permitted statement classes:
- `FACT`
- `INTERPRETATION`
- `FORECAST`
- `OPINION`

### PASS
- Material forecasts and interpretations are explicitly distinguishable from verified facts.
- Forward-looking claims are labeled or phrased with uncertainty.
- Calculated values are distinguishable from company-reported values.

### FAIL
- A forecast is written as an established fact.
- An interpretation is attributed to a source that did not make that interpretation.
- A model-derived or calculated number is represented as company-reported.

### UNKNOWN
- Statement type cannot be reliably classified from the text.
- A quoted/asserted claim lacks enough context to determine whether it is historical or forward-looking.

## G4 — Citation Gate

Preferred citation-ready fact unit:
`Entity + Fact + Number + Date/Period + Source`

### PASS
- Every material numeric claim is attributable to a source.
- Core paragraphs remain understandable when quoted independently.
- Entity and relevant period are explicit enough to avoid citation ambiguity.

### FAIL
- A material number has no traceable source.
- A citation points to evidence that contradicts the claim.
- The paragraph depends on an unclear pronoun/context in a way that changes the claim's meaning.

### UNKNOWN
- Source is present but the exact support for the numeric claim cannot be confirmed.
- Citation location or evidence range cannot be established.

## G5 — Investment Content Gate

Blocking certainty phrases include, but are not limited to:
- 무조건 오른다
- 확정 상승
- 반드시 매수
- 100% 수익
- 절대 손실 없음
- 원금 보장
- 확실한 수혜주

### PASS
- Investment analysis expresses scenarios, conditions, risks, or uncertainty where appropriate.
- No guaranteed-return or absolute-certain investment language is used.
- Risks and invalidation conditions are not intentionally hidden when the article makes an investment thesis.

### FAIL
- Guaranteed-return or capital-guarantee language is used without a legally valid guarantee context.
- A security is presented as certain to rise or as mandatory to buy.
- Material known risks are deliberately omitted while certainty is exaggerated.

### UNKNOWN
- The excerpt is too incomplete to determine whether certainty language is qualified elsewhere.

## Overall decision matrix

| G1 | G2 | G3 | G4 | G5 | Overall |
|---|---|---|---|---|---|
| PASS | PASS | PASS | PASS | PASS | PASS |
| any FAIL | any | any | any | any | FAIL |
| no FAIL + any UNKNOWN | | | | | UNKNOWN / RELEASE HOLD |

## V0.1 scope lock

V0.1 audits content only. It does not auto-publish, manipulate rankings, purchase backlinks, automate comments/neighbors, or auto-generate investment recommendations.
