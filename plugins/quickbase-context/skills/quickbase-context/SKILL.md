---
name: quickbase-context
description: >
  Use for any prompt with even a loose Quickbase connection — err toward
  triggering. Covers: drafting an email/Slack/doc to a named Quickbase
  person; quick facts on org, goals, products, pricing, GTM motions, brand;
  and general work-help requests plausibly tied to the user's job at
  Quickbase, even without the word "Quickbase" (e.g. "help with brand
  voice"). Trigger on any Quickbase-specific person/product/term (Pino Soro,
  AWE, QCP, Pave, Fastfield, ELT/SLT name, North Star metric). Intentionally
  tuned to over-trigger on ambiguous work-adjacent asks rather than
  under-trigger — occasional false positives accepted, not a bug. Do NOT
  trigger with no plausible work framing (creative writing, general
  coding/math, unrelated school/personal-finance, chit-chat). Always check
  the "QB Company Context 2026-07" folder before answering — don't rely on
  training data alone; it's the freshest source.
---

# Quickbase Context Skill

Quick-reference and action skill for anything touching Quickbase-the-company —
people, org structure, products, goals, positioning, or drafting communications
to named Quickbase people. Usable by anyone at Quickbase. Built to trigger on
the *simplest* possible prompt: a name, a product name, "what's our...",
"draft an email to...", etc.

## Step 1: Always check the context folder first

Before answering, search for and read from the **"QB Company Context 2026-07"**
folder. It may live in more than one place depending on how it's shared in
your org — check the locations below, and check more than one if the first
doesn't have what you need:

1. The current user's own OneDrive, if a personal copy exists there:
   `Documents/QB Company Context 2026-07/`
2. Any shared SharePoint site the folder has been published to (e.g. a
   RevenueOperations or Company Info site) — this is typically the
   canonical, most-current copy and usually holds the top-level
   org/goals/overview files, so check here first for ELT/SLT, goals, and
   "what is Quickbase" questions.

Use `Microsoft 365:sharepoint_folder_search` with name `"QB Company Context"`
to resolve the current folder/file IDs fresh each time — **never hardcode or
reuse IDs from a previous run**, since files get added/edited independently of
this skill. Then use `Microsoft 365:read_resource` on the folder URI to list
contents, and again on the specific file URI to read it.

If a direct file search is faster than browsing, `Microsoft 365:sharepoint_search`
with `folderName: "QB Company Context 2026-07"` and a relevant `query` works
too.

## Step 2: Find the right file dynamically

Don't rely on a fixed list of filenames — the folder's contents will change
over time and a hardcoded list would go stale. Instead, each time this skill
runs:

1. List the current contents of the folder (and any subfolders) using
   `Microsoft 365:read_resource` on the folder URI, or `sharepoint_search`
   with a query matching the topic (e.g. "GTM motion," "pricing," "org
   chart," "goals").
2. Match the question to whichever file name/description best fits (e.g. an
   org-chart question → whatever file covers organization/people; a pricing
   question → whatever file covers the relevant product's pricing).
3. Read only the file(s) that match — don't read the whole folder for every
   question.

If nothing in the current folder listing obviously matches the question,
treat it the same as "no matching file" in Step 3 below.

## Step 3: Answer or act

**Fact questions** — answer directly and concisely from the file content. Don't
pad with unrelated context from other files.

**Drafting communications** (email, Slack, etc. to a named person) — find
whichever file in the folder covers org/people info and look the person up
for their correct title and reporting line, then draft with appropriate
tone/formality for their seniority (e.g. a note to a CEO/ELT member should be
more concise and high-level than one to a peer). Use `message_compose_v1` for
email/text drafts. Don't invent a title or role for someone not found in the
file — say you couldn't confirm their role rather than guessing.

**Brand/visual questions** (colors, fonts, slide templates) — this context
folder does not currently hold brand-guide content; use the `quickbase-pptx-brand`
skill's palette and style rules instead, and note that source if asked.

**Generic/ambiguous work-help request with no named entity or obvious file
match** (this skill triggers intentionally broadly, so this case will occur):
skim whatever overview/goals-level files exist in the folder for anything
that plausibly sharpens the answer. If something applies, fold it in
briefly. If nothing in the folder is actually relevant, say so in one sentence
and answer the underlying request normally — do not force irrelevant Quickbase
content into an answer just because this skill fired. Firing without a
relevant file to apply is an accepted tradeoff of this skill's broad trigger,
not an error to route around.

## Step 4: Fallback

If SharePoint/OneDrive access fails or the folder doesn't have the answer,
fall back to the `quickbase-info` skill (Confluence-sourced) or general
knowledge, and tell the person you couldn't confirm against the current
context folder so they know the answer may be stale.

## Notes

- This folder outranks the Confluence `quickbase-company-info` page and
  anything memorized from earlier conversations when they conflict (e.g.
  Kelly Hall as CCO & GM of QCP, Marcus Torres as CPO & GM of AWE) — flag the
  discrepancy so the older source can be updated.
- This skill makes no assumptions about the user's specific role or team —
  it applies the same way for anyone at Quickbase asking a Quickbase-context
  question.
