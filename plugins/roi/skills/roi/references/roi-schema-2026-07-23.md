# Input Contract ([schema.md](http://schema.md))

The engine (`roi_engine.py`) consumes one JSON object per use case. The LLM assembles it from the  
interview + data-grounding. House numbers (rates, scenario levers, haircuts) are NOT in here — they  
live in `assumptions.json`. This file holds only case facts, provenance, and explicit overrides.

json{
"use\_case": {
"name": "AI-Assisted QBR Deck Creation for CSMs",
"owner": "TBD",
"requestor": "Seth",
"date": "2026-06-29",
"one\_liner": "AI drafts QBR decks from Salesforce+Gainsight data; CSMs review.",
"value\_type": "revenue", // labor | revenue | risk | capability
"delivery\_model": "augmentation" // augmentation | autonomous
},
"labor": {
"role": "CSM", // must match a key in assumptions.role\_costs\_loaded\_annual
"people": 50,
"eligible\_volume\_year": 200, // instances/yr the AI touches
"hours\_per\_instance": 3.5, // raw task time today
"net\_hours\_reported": false, // true => hours\_per\_instance is ALREADY net saved; engine skips automation haircut
"net\_hours\_per\_period": null, // used only if net\_hours\_reported
"periods\_per\_year": 52,
"gate": "redeploy", // headcount | redeploy | diffuse
"headcount\_reduction\_fte": 0 // used only if gate == headcount
},
"revenue\_chain": { // required if value\_type==revenue OR gate==redeploy
"value\_per\_account": 55000, // ARR or margin per account (GROUND THIS)
"at\_risk\_rate": 0.20, // omit to use house default; setting it != house = an override
"churn\_reduction": null, // null => house default
"conversion\_to\_productive": null, // null => house default (fraction of freed hrs that become real units)
"hours\_per\_downstream\_unit": null, // null => house default
"holdout\_exists": false, // true bumps confidence and lets attribution rise
"\_reasons": {"at\_risk\_rate": "CSMs intentionally target at-risk accounts"}
},
"build": { "weeks": 6, "tshirt": "M" }, // weeks wins if present; else tshirt maps via assumptions
"run": { "tier": "medium", "platform\_annual": 1000 }, // tier: light|medium|heavy
"data\_grounding": { // provenance per key input -> drives derived confidence
"eligible\_volume\_year": {"value": 200, "source": "user", "system\_value": null, "system": null},
"value\_per\_account": {"value": 55000, "source": "system", "system\_value": 55000, "system": "Salesforce"},
"at\_risk\_rate": {"value": 0.20, "source": "user", "system\_value": null, "system": "Gainsight (not pulled)"}
},
"overrides": [ // any deviation from assumptions.json, with a reason
{"field": "at\_risk\_rate", "used": 0.20, "reason": "CSMs intentionally target at-risk accounts"}
],
"confidence\_override": null, // {"level":"Medium","reason":"..."} to force; else derived
"shared\_capacity\_pool": "CSM-hours" // for portfolio conflict detection
}

## Rules the LLM must honor

* Never put rates/haircuts/scenario percentages in here — those come from `assumptions.json`.
* `source: "system"` means you actually pulled it from a connector this session. Do not label a  
  guess as system-grounded. Confidence depends on honesty here.
* Every value that differs from the house default appears in `overrides` with a real reason.
* `value_per_account` and the baseline rate being moved are required (not optional) for revenue  
  cases, and should be grounded, not remembered.
