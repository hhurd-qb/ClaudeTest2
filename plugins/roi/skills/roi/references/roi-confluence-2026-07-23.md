# Confluence Push Reference

Two pages: a single **register** (parent, one row per use case, sortable for prioritization) and one  
**detail page** per use case (the auditable brief). Always preview and get a yes before any write.

## Configuration

* **Space key**: ask the user the first time ("Which Confluence space should the AI ROI register  
  live in?") and reuse it. Optionally hard-code a default here once known.
* Get `cloudId` via the Atlassian connector before searching/creating.

## Step 1 — Find or create the register

Search with CQL (Confluence Query Language, not JQL):

title ~ "AI Use Case ROI Register" AND type = page AND space = "<SPACEKEY>"

* **Found** → read it, you'll append a row in Step 3.
* **Not found** → offer to create it from the Register template below. Don't create silently.

## Step 2 — Create the detail page

Title format: `AI ROI — <Use Case Name>`. Use this exact structure (HTML/markdown as the connector  
supports). Every section is required; the **Assumptions & basis** and **Measurement plan** sections  
are what make the estimate auditable and the loop closeable, so never drop them.

# AI ROI — <Use Case Name>
> Status: PROJECTED — to be validated post-deployment | Requestor: <name> | Date: <date>
> Value type: <Labor | Revenue | Risk/Quality | Capability>
## Summary
<1–2 sentences: the task, who does it today, what the AI does.>
## Headline
- Conservative net annual: $<X>
- Expected net annual: $<Y>
- Payback: ~<Z> months
- 3-yr ROI: <%>
- Confidence: <High | Medium | Low>
<If capability-only: "Hard ROI $0 — justified by option value (below).">
## Capacity created (non-cash, reported separately)
<e.g. "≈ 0.5 FTE-equivalent of AE capacity" — only if labor route (c)/(b). Omit if not applicable.>
## Inputs (supplied by requestor)
| Input | Value |
|---|---|
| Task & who does it | <…> |
| Roles / # people | <…> |
| Frequency / volume | <…> |
| Time per instance (today) | <…> |
| Freed-time disposition | <(a) headcount removed / (b) redeployed to <named output> / (c) diffuse> |
## Assumptions & basis (supplied by Claude — editable)
| Assumption | Value | Basis |
|---|---|---|
| Fully-loaded rate | $<…>/hr | benchmark, role <…> |
| Automation share | <…>% | review/exceptions remain |
| Adoption (steady / yr-1) | <…>% / <…>% | ramp |
| Attribution factor | <…> | <holdout? default 0.5> |
| Build cost | $<…> | <S/M/L> × loaded daily rate |
| Run cost | $<…>/yr | volume × per-instance LLM + platform |
## ROI calculation
<Show the formula path used (from roi-math.md) and the conservative/expected/optimistic numbers.>
## Attribution & confidence
<The counterfactual ("absent the AI, …"), the haircut applied, and why the confidence tier.>
## Risks & dependencies
<Data access, integration, trust/accuracy, change management, etc.>
## Measurement plan (how Projected becomes Realized)
| Baseline (today) | Success metric | Target | Check-in date |
|---|---|---|---|
| <current value> | <the metric that proves it> | <…> | <date> |
## Prioritization
| Expected Net Annual ($K) | Confidence (mult) | Effort (build-weeks) | Priority score |
|---|---|---|---|
| <…> | <H 1.0 / M 0.7 / L 0.4> | <S2 / M6 / L12> | <computed> |

## Step 3 — Append the row to the register & re-sort

Add one row to the register table, then sort the table by **Priority score descending** so the  
register always reads top-to-bottom as the build order.

### Register page template (only if creating it fresh)

# AI Use Case ROI Register
Single source of truth for proposed AI/automation use cases and their projected ROI. Every entry is
PROJECTED until its measurement plan is validated post-deployment, at which point Status moves to
REALIZED. Numbers are conservative-to-expected ranges, net of run cost. Sorted by Priority (build
order). Methodology: hard cash only when a head leaves or a named output is produced; diffuse time
savings are reported as capacity, not cash.
| Priority | Use Case | Owner | Type | Net Annual (Cons.–Exp.) | Payback | Effort | Confidence | Status | Brief |
|---|---|---|---|---|---|---|---|---|---|
| <score> | <name> | <owner> | <type> | $<X>–$<Y> | <Z> mo | <S/M/L> | <H/M/L> | PROJECTED | <link to detail page> |

## After writing

Give the user the detail-page link and a two-line summary (headline + priority). Do not paste the  
whole brief back into chat — it's on the page.
