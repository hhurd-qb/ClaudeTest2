json{
"\_meta": {
"version": "1.1.0",
"owner": "RevOps — <assign a named owner>",
"last\_updated": "2026-07-23",
"note": "These are the HOUSE assumptions. They are the single authority for every ROI estimate. Do not change per-estimate — change here, bump the version, and every future estimate inherits it. Any per-case deviation must be recorded as an explicit override with a reason (the engine flags these). Argue with the owner of this file, not with individual briefs.",
"changelog": [
"1.0.0 (2026-06-29): initial house assumptions extracted from methodology v1",
"1.1.0 (2026-07-23): conservatism revision. Lowered automation\_share and adoption\_steadystate across all three scenarios; steepened adoption\_year1\_ramp; lowered conversion\_to\_productive. churn\_reduction lowered to 0.08 AND reclassified as a required-justification field (see require\_justification) — it can no longer be used silently as a free default. build\_tshirt\_weeks widened pending real Jira build-history validation (flagged, not yet data-backed). role\_costs\_loaded\_annual left unchanged pending Finance/HR reconciliation (flagged, not yet data-backed)."
],
"flagged\_for\_validation": {
"build\_tshirt\_weeks": "Widened by judgment (~1.5x), not yet checked against actual Jira build-time history for prior AI/automation projects. Treat as placeholder.",
"role\_costs\_loaded\_annual": "Not yet reconciled against real Quickbase comp bands / HRIS. No connector available to verify."
}
},
"role\_costs\_loaded\_annual": {
"\_comment": "Fully-loaded annual cost (salary + benefits + overhead ≈ base × 1.3). NOT OTE. OTE only enters revenue math, never time-valuation.",
"SDR": 95000,
"AE": 143000,
"CSM": 150000,
"RevOps\_analyst": 120000,
"support\_rep": 85000,
"renewals\_specialist": 100000,
"PMM\_PM": 165000,
"engineer": 190000,
"manager": 210000
},
"hours\_per\_year": 2080,
"working\_days\_per\_year": 260,
"builder\_role": "engineer",
"scenario\_levers": {
"\_comment": "Scenario variance comes from DELIVERY levers only. Business-chain values (at-risk rate, churn lift, ARR) are point estimates with separate sensitivity — they do not swing by scenario.",
"automation\_share": {"conservative": 0.40, "expected": 0.55, "optimistic": 0.80},
"adoption\_steadystate": {"conservative": 0.30, "expected": 0.50, "optimistic": 0.75},
"coverage": {"conservative": 0.70, "expected": 0.85, "optimistic": 0.95},
"attribution": {"conservative": 0.50, "expected": 0.50, "optimistic": 0.80}
},
"adoption\_year1\_ramp": 0.60,
"coverage\_year1\_ramp": 0.80,
"revenue\_chain\_defaults": {
"\_comment": "Defaults for the redeploy/revenue path. Conservative by design. Per-case overrides must be justified.",
"conversion\_to\_productive": 0.40,
"hours\_per\_downstream\_unit": 3,
"at\_risk\_rate": 0.10,
"churn\_reduction": 0.08
},
"require\_justification": {
"\_comment": "Fields listed here CANNOT be used silently, even at the house default. The submitter must supply a case-specific reason in revenue\_chain.\_reasons. If absent, the engine flags the case (results.flags) and caps confidence at Low, regardless of grounding elsewhere. This exists because these fields represent a causal claim (e.g. 'freeing CSM time reduces churn'), not a benchmarkable rate — silently accepting a default here would hide the weakest link in the chain.",
"fields": ["churn\_reduction"]
},
"run\_cost\_per\_instance": {
"light": 0.06,
"medium": 0.30,
"heavy": 1.00
},
"run\_cost\_platform\_annual\_default": 1000,
"build\_tshirt\_weeks": {"S": 3, "M": 9, "L": 18},
"confidence\_multiplier": {"High": 1.0, "Medium": 0.7, "Low": 0.4},
"near\_zero\_floor\_usd": 15000
}
