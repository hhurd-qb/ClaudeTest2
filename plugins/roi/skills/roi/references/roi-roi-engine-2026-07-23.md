py#!/usr/bin/env python3
"""
Deterministic ROI engine for the AI Use Case ROI skill.
Design contract:
- The LLM does elicitation, classification, and data-grounding. It does NOT do arithmetic.
- This engine does all arithmetic. Given the same inputs JSON and the same assumptions
version, it returns byte-identical output every time, for everyone. No randomness, no
session drift. This is what makes the register a valid RANKING and not a vibe.
- House assumptions live in assumptions.json and are owned/versioned. Any per-case deviation
must be passed as an explicit override and is surfaced in the output (anti-gaming: deviations
from the house method are visible and attributable).
Usage:
python roi\_engine.py inputs.json # single use case -> results JSON
python roi\_engine.py --portfolio cases/\*.json # portfolio capacity-conflict check
python roi\_engine.py --selftest # determinism + reproduction checks
"""
import json, sys, glob, copy
SCENARIOS = ["conservative", "expected", "optimistic"]
def load\_assumptions(path="assumptions.json"):
with open(path) as f:
return json.load(f)
def \_resolve(field\_path, house\_value, overrides):
"""Return (value, override\_record\_or\_None). Overrides are matched by field name."""
for ov in overrides:
if ov.get("field") == field\_path:
return ov["used"], {"field": field\_path, "house": house\_value,
"used": ov["used"], "reason": ov.get("reason", "(no reason given)")}
return house\_value, None
def compute(inputs, A):
"""Pure function: inputs dict + assumptions dict -> results dict. Deterministic."""
uc = inputs["use\_case"]
vtype = uc["value\_type"] # labor | revenue | risk | capability
overrides\_in = inputs.get("overrides", [])
applied\_overrides = []
results = {"use\_case": uc, "scenarios": {}, "overrides\_applied": [],
"grounding": inputs.get("data\_grounding", {}), "flags": []}
# ---- Capability: hard ROI is $0 by definition. Don't manufacture a number. ----
if vtype == "capability":
results["verdict"] = "CAPABILITY — hard ROI $0; justify on option value, not cash."
results["headline"] = {"hard\_cash\_annual": 0}
results["priority\_score"] = None
results["table"] = "capability"
return results
build\_weeks = inputs.get("build", {}).get("weeks") or \
A["build\_tshirt\_weeks"].get(inputs.get("build", {}).get("tshirt", "M"), 6)
builder\_daily = A["role\_costs\_loaded\_annual"][A["builder\_role"]] / A["working\_days\_per\_year"]
build\_cost = build\_weeks \* 5 \* builder\_daily
lab = inputs.get("labor", {})
role = lab.get("role", "AE")
role\_hourly = A["role\_costs\_loaded\_annual"][role] / A["hours\_per\_year"]
volume = lab.get("eligible\_volume\_year", 0)
per\_inst = A["run\_cost\_per\_instance"][inputs.get("run", {}).get("tier", "medium")]
platform = inputs.get("run", {}).get("platform\_annual", A["run\_cost\_platform\_annual\_default"])
run\_annual = volume \* per\_inst + platform
# revenue-chain values (with override resolution)
rc\_house = A["revenue\_chain\_defaults"]
rc = inputs.get("revenue\_chain", {})
justification\_required = set(A.get("require\_justification", {}).get("fields", []))
unjustified\_fields = []
gate\_mismatch\_flagged = False
def rc\_val(name):
house = rc\_house[name]
used = None
# a case may set the value directly in revenue\_chain (treated as override if != house)
if name in rc and rc[name] is not None:
used = rc[name]
if used != house:
applied\_overrides.append({"field": name, "house": house, "used": used,
"reason": rc.get("\_reasons", {}).get(name, "(set on case)")})
else:
used, rec = \_resolve(name, house, overrides\_in)
if rec:
applied\_overrides.append(rec)
# ---- require\_justification enforcement ----
# Some fields (e.g. churn\_reduction) represent a causal claim, not a benchmarkable
# rate, and may NOT be used silently at the house default. A case-specific reason is
# mandatory every time the field is used at all, override or not.
if name in justification\_required:
reason = rc.get("\_reasons", {}).get(name)
if not reason:
unjustified\_fields.append(name)
return used
for sc in SCENARIOS:
auto = A["scenario\_levers"]["automation\_share"][sc]
attribution = A["scenario\_levers"]["attribution"][sc]
# usage factor: augmentation -> adoption(+ramp); autonomous -> coverage(+ramp)
if uc.get("delivery\_model") == "autonomous":
usage = A["scenario\_levers"]["coverage"][sc] \* A["coverage\_year1\_ramp"]
else:
usage = A["scenario\_levers"]["adoption\_steadystate"][sc] \* A["adoption\_year1\_ramp"]
# freed hours
if lab.get("net\_hours\_reported"):
# user gave NET hours saved already -> do NOT re-apply automation share
net\_hrs\_per\_period = lab.get("net\_hours\_per\_period", 0)
periods = lab.get("periods\_per\_year", 52)
freed\_hours = lab.get("people", 0) \* net\_hrs\_per\_period \* periods \* usage
else:
freed\_hours = volume \* lab.get("hours\_per\_instance", 0) \* auto \* usage
gross\_labor\_value = freed\_hours \* role\_hourly
# ---- the gate ----
gate = lab.get("gate")
# ---- mismatch check: 'redeploy' IS the revenue/retention mechanism ----
# If someone frames a case as labor or risk but selects 'redeploy', the case's own
# framing and the math it's about to run disagree. Flag it once (not per-scenario).
if gate == "redeploy" and vtype != "revenue" and not gate\_mismatch\_flagged:
gate\_mismatch\_flagged = True
results["flags"].append(
f"gate\_valuetype\_mismatch: gate is 'redeploy' (a revenue/retention mechanism) "
f"but value\_type is '{vtype}', not 'revenue' — confirm this is really a revenue/"
f"retention case, or pick a gate that matches '{vtype}' framing (diffuse or headcount)"
)
capacity\_fte = freed\_hours / A["hours\_per\_year"]
hard\_cash = 0.0
rev\_detail = None
if vtype == "revenue" or gate == "redeploy":
# downstream-output path (route b / direct revenue)
conv = rc\_val("conversion\_to\_productive")
hpu = rc\_val("hours\_per\_downstream\_unit")
at\_risk = rc\_val("at\_risk\_rate")
churn = rc\_val("churn\_reduction")
value\_per = rc.get("value\_per\_account", 0)
units = (freed\_hours \* conv) / hpu if hpu else 0
at\_risk\_accounts = units \* at\_risk
gross\_rev = at\_risk\_accounts \* value\_per \* churn
hard\_cash = gross\_rev \* attribution
rev\_detail = {"freed\_hours": round(freed\_hours, 1),
"downstream\_units": round(units, 1),
"at\_risk\_accounts": round(at\_risk\_accounts, 2),
"gross\_revenue": round(gross\_rev), "attribution": attribution}
elif gate == "headcount":
fte\_removed = lab.get("headcount\_reduction\_fte", 0)
hard\_cash = min(fte\_removed \* A["role\_costs\_loaded\_annual"][role], gross\_labor\_value)
else: # diffuse
hard\_cash = 0.0
net\_annual = hard\_cash - run\_annual
results["scenarios"][sc] = {
"freed\_hours": round(freed\_hours, 1),
"capacity\_fte": round(capacity\_fte, 2),
"gross\_labor\_value": round(gross\_labor\_value),
"hard\_cash\_annual": round(hard\_cash),
"run\_cost\_annual": round(run\_annual),
"net\_annual": round(net\_annual),
"revenue\_chain": rev\_detail,
}
# de-dup overrides
seen = set()
for ov in applied\_overrides + [o for o in (
\_resolve(f, A["revenue\_chain\_defaults"].get(f), overrides\_in)[1]
for f in A["revenue\_chain\_defaults"] if f != "\_comment") if o]:
key = (ov["field"], ov["used"])
if key not in seen:
seen.add(key)
results["overrides\_applied"].append(ov)
# de-dup and surface any required-justification fields that were used without a reason
if unjustified\_fields:
for f in sorted(set(unjustified\_fields)):
results["flags"].append(f"missing\_justification:{f}")
exp = results["scenarios"]["expected"]
net\_exp = exp["net\_annual"]
hard\_exp = exp["hard\_cash\_annual"]
# ---- population too small for the revenue chain to mean anything ----
# Fractional "at-risk accounts" (e.g. 0.92) is a sign this population is too small for the
# revenue-chain model to produce a believable number, regardless of what the dollar figure
# says - scaling volume won't fix this, the case needs a different framing (labor/capability)
# or a genuinely bigger population.
exp\_rc = exp.get("revenue\_chain")
if exp\_rc and exp\_rc["at\_risk\_accounts"] < 1:
results["flags"].append(
f"population\_too\_small: expected case produces {exp\_rc['at\_risk\_accounts']} "
f"at-risk accounts - a fractional account means this population is too small for "
f"the revenue-chain model to mean anything here; consider a labor or capability "
f"framing instead of forcing this through redeploy/revenue math"
)
# payback & 3yr roi (expected)
results["build\_cost"] = round(build\_cost)
results["build\_weeks"] = build\_weeks
results["payback\_months"] = round(build\_cost / (net\_exp / 12), 1) if net\_exp > 0 else None
denom = build\_cost + 3 \* exp["run\_cost\_annual"]
results["roi\_3yr\_pct"] = round(100 \* (3 \* hard\_exp - 3 \* exp["run\_cost\_annual"] - build\_cost) / denom) if denom else None
# ---- confidence derived from EVIDENCE, not vibes ----
conf, conf\_reason = derive\_confidence(inputs, results["overrides\_applied"], unjustified\_fields)
results["confidence"] = conf
results["confidence\_reason"] = conf\_reason
# priority score (deterministic)
mult = A["confidence\_multiplier"][conf]
results["priority\_score"] = round((net\_exp / 1000) \* mult / build\_weeks) if net\_exp > 0 else 0
# ---- near-zero / negative guardrail ----
if hard\_exp <= A["near\_zero\_floor\_usd"]:
results["verdict"] = ("LOW / NEAR-ZERO HARD ROI — do not build for the ROI. "
"Report as capacity + strategic bet, or reframe (capability, or "
"whole-function headcount play). A verdict beats a decorated non-number.")
results["flags"].append("near\_zero")
results["table"] = "capability" if hard\_exp == 0 and exp["capacity\_fte"] < 0.25 else "register"
else:
results["verdict"] = "Defensible on ROI at expected case. Validate load-bearing assumptions before build."
results["table"] = "register"
return results
def derive\_confidence(inputs, overrides\_applied, unjustified\_fields=None):
unjustified\_fields = unjustified\_fields or []
grounding = inputs.get("data\_grounding", {})
grounded = sum(1 for g in grounding.values() if isinstance(g, dict) and g.get("source") == "system")
holdout = inputs.get("revenue\_chain", {}).get("holdout\_exists", False)
n\_over = len(overrides\_applied)
manual = inputs.get("confidence\_override")
if manual:
return manual["level"], f"manual override: {manual.get('reason', '')}"
# A required-justification field (e.g. churn\_reduction) used with no case-specific reason
# caps confidence at Low no matter how well-grounded everything else is — an unjustified
# causal assumption is a single point of failure for the whole estimate.
if unjustified\_fields:
return "Low", (f"required field(s) used without a case-specific justification: "
f"{', '.join(sorted(set(unjustified\_fields)))} — supply a reason in "
f"revenue\_chain.\_reasons to allow a higher confidence level")
if holdout and grounded >= 1:
return "High", "holdout/control exists and key inputs are system-grounded"
if grounded == 0 and n\_over >= 1:
return "Low", "no system-grounded inputs and one or more manual overrides from house assumptions"
if grounded == 0:
return "Low", "no system-grounded inputs; all facts user-supplied"
if n\_over >= 2:
return "Low", "two or more manual overrides from house assumptions"
return "Medium", "some inputs system-grounded; standard house assumptions otherwise"
def portfolio\_check(case\_files, A):
"""Flag shared-capacity pools claimed by multiple redeploy cases (double-counting)."""
pools = {}
for f in case\_files:
with open(f) as fh:
inp = json.load(fh)
pool = inp.get("shared\_capacity\_pool")
if not pool:
continue
r = compute(inp, A)
claimed = r["scenarios"]["expected"].get("freed\_hours", 0)
pools.setdefault(pool, []).append({"case": inp["use\_case"]["name"], "freed\_hours\_claimed": claimed,
"gate": inp.get("labor", {}).get("gate")})
report = {"pools": pools, "conflicts": []}
for pool, claims in pools.items():
redeploy\_claims = [c for c in claims if c["gate"] in ("redeploy", "headcount")]
if len(redeploy\_claims) > 1:
total = sum(c["freed\_hours\_claimed"] for c in redeploy\_claims)
report["conflicts"].append({
"pool": pool, "cases": [c["case"] for c in redeploy\_claims],
"total\_hours\_claimed": round(total),
"warning": "Multiple cases claim value from the SAME freed hours. These cannot all "
"be redeployed simultaneously — do not sum their hard-cash figures."})
return report
# ------------------------- self-test -------------------------
def \_selftest():
A = load\_assumptions()
qbr = {
"use\_case": {"name": "QBR deck creation", "value\_type": "revenue", "delivery\_model": "augmentation"},
"labor": {"role": "CSM", "people": 50, "eligible\_volume\_year": 200,
"hours\_per\_instance": 3.5, "gate": "redeploy"},
"revenue\_chain": {"value\_per\_account": 55000, "at\_risk\_rate": 0.20,
"\_reasons": {"at\_risk\_rate": "CSMs intentionally target at-risk accounts"}},
"build": {"weeks": 6}, "run": {"tier": "medium"},
}
r1 = compute(copy.deepcopy(qbr), A)
r2 = compute(copy.deepcopy(qbr), A)
assert json.dumps(r1, sort\_keys=True) == json.dumps(r2, sort\_keys=True), "NON-DETERMINISTIC!"
print("determinism: PASS (identical output on repeat run)")
print(f"QBR expected net\_annual: ${r1['scenarios']['expected']['net\_annual']:,}")
print(f"QBR confidence: {r1['confidence']} ({r1['confidence\_reason']})")
print(f"QBR priority: {r1['priority\_score']} payback: {r1['payback\_months']} mo")
print(f"overrides surfaced: {r1['overrides\_applied']}")
print(f"verdict: {r1['verdict']}")
if \_\_name\_\_ == "\_\_main\_\_":
if "--selftest" in sys.argv:
\_selftest()
elif "--portfolio" in sys.argv:
files = [a for a in sys.argv[2:] if not a.startswith("--")]
expanded = []
for f in files:
expanded += glob.glob(f)
print(json.dumps(portfolio\_check(expanded, load\_assumptions()), indent=2))
else:
with open(sys.argv[1]) as f:
inp = json.load(f)
print(json.dumps(compute(inp, load\_assumptions()), indent=2))
