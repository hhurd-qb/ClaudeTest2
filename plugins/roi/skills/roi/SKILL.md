---
name: roi
description: >-
  Trigger this skill whenever the user says "/roi" — with or without anything else in the message.
  Also use whenever a user wants to estimate, scope, justify, or prioritize an AI/automation idea
  without typing "/roi" (e.g. 'ROI of automating X', 'business case for [AI idea]'). Scopes a use
  case into a defensible ROI estimate via a deterministic engine (roi_engine.py) against versioned
  house assumptions (assumptions.json) — same inputs always yield the same number. Hands the
  person a standalone intake form every trigger, and always asks before publishing to Confluence
  and/or Jira. Do NOT trigger for a generic non-AI ROI question (e.g. 'ROI of an office lease'),
  or when a case is pasted purely for reference, not scoring — ask if unclear.
---

# /roi — AI Use Case ROI

When the user types `/roi` — alone, or followed by a one-liner like `/roi automate QBR decks for
CSMs` — start this workflow immediately from Step 0 below. Don't wait for a fuller description;
if they gave a one-liner alongside `/roi`, use it to seed Step 2's classification and skip straight
to whatever you can't infer from it.

## Design principle
You (the LLM) do elicitation, classification, override capture, narrative, and the Confluence
and/or Jira write. You do **not** do arithmetic or invent assumptions — the engine does all math,
deterministically, from `assumptions.json`. Same inputs -> same output, for everyone, forever.
Confidence is *derived from evidence*, not asserted.

Trust in this system comes from four things, in order: real numbers wherever you can get them, a
method nobody can quietly bend, a human who owns the assumptions, and a published track record of
projected-vs-realized. Your job is the first two on every run.

`assumptions.json` holds the house numbers (current version and full changelog are in its own
`_meta` block — check there for what's currently in effect, rather than relying on this file's
prose). Fields under `require_justification` (currently `churn_reduction`) can never be used
silently, even at the house default — a case-specific reason is mandatory or confidence is capped
at Low. Fields under `_meta.flagged_for_validation` (currently `build_tshirt_weeks` and
`role_costs_loaded_annual`) are judgment calls awaiting real data — say so plainly if a case leans
on them.

## Workflow

### Step 0 - Surface the standalone intake form, every time
The moment this skill triggers, before anything else: copy `references/intake-form.html` to the
outputs folder and present it via present_files. Tell the person briefly what it is — a
self-contained form that collects a case's facts into the same schema this skill uses, so they can
fill it out at their own pace or hand it to someone without code execution enabled. Be explicit
about what it does **not** do: it doesn't calculate anything. No math, no engine, no house numbers
applied — it only packages inputs. All arithmetic still happens here, in this conversation, via the
real engine. Then continue to Step 1.

**If the person pastes back a completed JSON payload from the form:** don't re-run the full
interview from scratch. Validate it against `references/schema.md`, ask only about anything missing
or that still needs grounding/justification (Steps 2-4 below), then proceed straight to running the
engine (Step 5). Treat the pasted JSON as a strong starting draft, not a finished, trusted input -
you still own grounding it and catching anything that needs a reason.

**Keep it in sync:** `intake-form.html` still embeds a copy of the house numbers as a JS object,
purely to pre-fill and display current defaults (e.g. showing "House default: 0.08" next to
`churn_reduction`) — not to calculate anything. If you ever update `assumptions.json`, update that
embedded object in `intake-form.html` in the same edit, so the defaults shown to the person match
what the real engine will actually use.

### Step 1 - Read the assumptions and the schema
Read `references/assumptions.json` (the house numbers - never override them ad hoc in your head) and
`references/schema.md` (the input contract). You will assemble an inputs JSON that conforms to the
schema and hand it to the engine.

### Step 2 - Classify, then interview (<=7 questions, in plain language)
Propose the value type (labor / revenue / risk / capability) and delivery model (augmentation vs
autonomous) from the one-liner, then ask only what you can't infer. Prefer tappable options. Ask in
everyday language, not schema field names — the person answering usually isn't the one who reads
the JSON. Translate their answer into the schema field yourself; don't make them speak schema.

**Plain-language question bank** (map each to its schema field silently):
| Ask this | Not this | Maps to |
|---|---|---|
| "What's this idea in one sentence — what does the AI actually do?" | "State the use_case.one_liner" | `use_case.one_liner` |
| "Whose job does this touch, and roughly how many of them are there?" | "Specify labor.role and labor.people" | `labor.role`, `labor.people` |
| "How many times a year does this happen? (e.g. 200 QBRs/year, 5,000 tickets/month)" | "eligible_volume_year?" | `labor.eligible_volume_year` |
| "Today, without AI, how long does one of these take from start to finish?" | "hours_per_instance?" | `labor.hours_per_instance` |
| "If this works, does the freed-up time mostly (a) get soaked up in other work, (b) get redirected to something valuable like at-risk accounts, or (c) let you actually cut headcount/hours?" | "What's the gate — diffuse, redeploy, or headcount?" | `labor.gate` |
| "Rough guess: is this a couple weeks of build (small), a month or two (medium), or a real quarter-long project (large)?" | "build.tshirt?" | `build.tshirt` / `build.weeks` |
| *(revenue/redeploy only)* "What's a typical account worth per year — ARR or margin?" | "value_per_account?" | `revenue_chain.value_per_account` |
| *(revenue/redeploy only)* "What's the baseline rate this is supposed to move — like churn %, win rate, or conversion rate — today?" | "baseline rate?" | the relevant `revenue_chain` field |
| *(only if churn is the lever)* "Why do you believe freeing up this time would actually reduce churn, specifically? (e.g. a past pilot, a known pattern, CSMs targeting at-risk accounts)" | *(silently accepting the house default)* | `revenue_chain._reasons.churn_reduction` — **required, not optional** |

If the person answers a question that maps to more than one field at once (common with the
gate question), just parse it out — don't ask them to restate it in parts.

### Step 3 - Use real numbers wherever you can get them (connectors optional, never required)
The house numbers in `assumptions.json` are the source of truth for rates and haircuts. For
case-specific facts (volume, headcount, baseline rates, ARR), prefer a real number over a
remembered or guessed one whenever one is available to you — from a connected system, a document
the person has open, or a number they read off a report. But never block the estimate on a missing
connector: if nothing is connected or accessible, ask the person directly and mark it user-supplied.
Do not silently treat a guess as fact, and do not silently claim something is system-grounded if you
didn't actually verify it this session.

Record provenance for each key input in the inputs JSON `data_grounding` block with `source:
"system"` (you verified it against something this session) or `source: "user"` (it's their word).
The engine reads this to derive confidence - verified inputs earn higher confidence automatically;
unverified ones score Low. Tell the user plainly what's verified and what isn't; that honesty is the
whole point, not a connector integration.

### Step 4 - Capture overrides explicitly
Any per-case value that differs from `assumptions.json` (e.g. at-risk rate 20% vs house 10%) goes in
the `overrides` array with a `reason`. The engine surfaces these in the output and on the page.
Deviating from the house method is allowed; hiding it is not. If you find yourself wanting to
override several house numbers to make a case work, that is a signal the case is weak - say so.

**Required-justification fields:** `assumptions.json.require_justification` lists fields
(currently just `churn_reduction`) that cannot be used at all - default or overridden - without a
case-specific reason in `revenue_chain._reasons`. If you don't have a real reason, ask the person
for one (see the plain-language question bank in Step 2) rather than filling in a placeholder. If
they can't give one, say so plainly: the engine will cap confidence at Low and flag the case, and
that's the correct outcome, not a bug to route around.

### Step 5 - Run the engine
Write the inputs JSON to a file and run:
`python references/roi_engine.py inputs.json`
Use the returned numbers verbatim. **Do not recompute, round differently, or "adjust" the engine's
output** - that reintroduces exactly the drift this whole design exists to kill. If a number looks
wrong, the fix is the inputs or the assumptions file, not a manual edit.

### Step 6 - Present the result honestly
Show the headline (conservative -> expected net, payback, 3-yr ROI), the derived confidence *and its
reason*, the capacity figure if any, every override with its reason, and what was/wasn't grounded.
Lead with the conservative number. If the engine returns a `near_zero` flag, lead with the **verdict**
("don't build this for the ROI - here's the real reason to, or don't"), not the number. If it returns
`table: capability`, present it as an option-value bet with $0 hard ROI.

Be explicit about total uncertainty: the displayed range reflects delivery levers only; the business-
chain inputs (at-risk %, churn lift, ARR) carry their own 2x+ uncertainty, so the true error bar is
wider than the conservative-expected band. Say this. False precision loses the finance audience.

### Step 7 - Validation gate before publishing anywhere
An estimate does not go anywhere on one person's say-so. Before offering to publish:
- If confidence is **Low** OR any load-bearing input is user-supplied (not verified) OR there are >=2
  overrides -> it's publishable only as **DRAFT / pending validation**, and you must name who
  should validate it (e.g. "RevOps to confirm the at-risk rate against real account data before this
  counts").
- **High/Medium** with verified inputs -> publishable as PROJECTED.
Never present a number as validated that isn't. State the gate outcome to the person as part of
Step 6's results, before asking about publishing at all.

### Step 8 - Ask where this should go, then publish (confirm first, always)
Never publish or file anything without asking first, every time - regardless of how confident the
estimate is or whether this feels like a routine case. Ask the person plainly: should this become
a Confluence ROI register entry, a Jira ticket, both, or neither yet? Wait for their answer before
writing anywhere.

**If Confluence:** Follow `references/confluence.md`. Create the detail page (include the grounding
provenance, the overrides table, and the validation status from Step 7), append/sort the register
row, and return the link. Preview the content and get a yes before writing.

**If Jira:** Confirm which project it should go in if it isn't already obvious from context (use
the Atlassian Jira tools to look up visible projects if unsure - don't guess a project key). Default
to issue type "Task" unless the person specifies otherwise. Put the case name and one-liner in the
summary, and the full result - headline scenarios, confidence and its reason, overrides, the
validation-gate status from Step 7, and any flags - in the description, exactly as shown in chat.
Preview the summary and description and get a yes before creating the issue.

**If both:** do Confluence first, then include the resulting page link in the Jira ticket
description so the two stay connected.

**If neither yet:** that's a fine outcome - not every estimate needs to be filed immediately. Say
so plainly and stop there.

## Portfolio integrity (run before any register total)
Every case records a `shared_capacity_pool` (e.g. "CSM-hours", "AE-selling-hours"). Before anyone
sums the register or reports a portfolio number, run:
`python references/roi_engine.py --portfolio path/to/cases/*.json`
It flags when multiple redeploy/headcount cases claim value from the *same* freed hours - which
cannot all be true at once. Do not sum conflicting cases' hard cash. This is the guard against the
aggregation error that discredits hand-built portfolio numbers.

## Governance (state these; they are the trust backbone, not optional extras)
- **`assumptions.json` has a named owner** (RevOps/Finance). Challenges to method go to the owner and
  a version bump - not to per-entry debates. Assign the owner before opening this to submitters.
- **Lifecycle:** entries are PROJECTED, reviewed on a set cadence, and expire if not validated. A
  stale register poisons trust in the fresh entries.
- **Track record is the real currency:** publish projected-vs-realized for every shipped case,
  including misses. Nothing else converts "a clever tool" into "the number the business believes."
  Capture the baseline + metric now (measurement plan on every page) even though the payoff is months
  out.

## Honest scope
This tool imposes disciplined, transparent, *reproducible* argument on AI-investment decisions. It is
not an objective oracle - inputs are still elicited, and the revenue path still depends on judgment.
Sell it as a structured argument backed by an owned method and a track record, not as truth. For small
decisions, don't over-model - a coarse cash/capacity/capability x S/M/L triage is often the honest
right-sized answer; reserve the full engine for cases big enough to justify it.
