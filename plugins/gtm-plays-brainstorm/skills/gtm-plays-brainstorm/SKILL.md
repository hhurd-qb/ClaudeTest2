---

name: gtm-plays-brainstorm description: Brainstorm and prioritize automated outbound and GTM plays for a B2B SaaS product. Use this skill whenever a user asks which automated GTM plays to run, wants help with outbound automation strategy, is brainstorming signal-based campaigns, or wants to know what outbound and sales motions to automate for their B2B company. Trigger when someone says "what plays should I run," "help me with automated outbound," "what GTM automations make sense for us," "I want to build a signal-based outreach program," or asks for a prioritized list of outbound or GTM ideas. Also use when someone describes a B2B product and wants to know where to start with automated prospecting — even if they don't explicitly say "plays." Use this skill proactively whenever a user shares a product description, ICP, or GTM motion and asks how to grow or find customers faster.

# GTM Plays Brainstorm

A skill for generating and prioritizing automated outbound and GTM plays tailored to a specific B2B product and company context. The goal is to surface the 5-8 highest-leverage plays this company should be running — not a generic list, but a prioritized, opinionated recommendation grounded in their actual GTM motion and the signals they can realistically access.

## Guiding Principles

These principles should shape every recommendation. Internalize them before generating output.

**Signal-based beats cold.** Signal-triggered campaigns outperform cold outreach by 2x-10x. Prioritize plays where a clear buying signal exists. The best signals are often those a company already generates but hasn't operationalized yet — content engagement, product usage data, CRM history.

**Fewer, better contacts win.** The goal of automation is precision, not volume. A list of 50-250 highly targeted contacts with relevant, timely messaging converts far better than a list of 5,000 generic contacts. Recommend plays that enable tight targeting.

**Match plays to GTM motion.** PLG companies have product signals that sales-led companies don't. Sales-led companies can run cold plays that PLG companies shouldn't prioritize. Always filter through the company's actual motion.

**Start with what they already have.** Recommend plays that use existing data sources (CRM, LinkedIn content, product usage, closed-won history) before suggesting new data acquisitions. Complexity should be earned.

**Un-silo channels.** The GTM flywheel: outbound targets hand-raisers from content, best-performing content becomes ads, ads reinforce the outbound list. Surface plays that connect marketing, sales, and product signals.

**Sequence complexity to stage.** Early-stage companies should run 1-2 high-signal plays and get them working. Growth-stage teams layer signals. Scaling teams run full signal stacks and micro-campaigns (50-250 contacts, highly specific, refreshed frequently).

## Step 1: Gather Context

Before generating any plays, check whether the conversation already contains answers to all four of these questions. If any are missing, use the AskUserQuestion tool to collect them — don't skip this step or fill in assumptions.

1. **Product description**: What does the product do and who is the primary buyer?
2. **ICP / target segment**: What companies and personas are they targeting? (industry, size, tech stack, geo, etc.)
3. **GTM motion**: How are they primarily growing? Options: sales-led (SDR/AE outbound), product-led (self-serve + sales-assist), marketing-led (inbound + content), or hybrid.
4. **Company stage**: Early (pre-$1M ARR or <10 employees), Growth ($1M–$20M ARR, 10–100 employees), or Scaling ($20M+ ARR, 100+ employees).

## Step 2: Read the Plays Library

Read `references/plays-library.md` in full. It contains 25+ plays organized by category, with signals, tools, difficulty, and GTM motion fit. Use it as your source of truth for recommendations.

## Step 3: Select and Prioritize

With company context in hand and the plays library loaded, select **5-8 plays** in priority order. Apply these filters:

* Does this company realistically have access to the underlying signal? If not, flag as "Future State" rather than skipping entirely.
* Does the play fit their GTM motion?
* Is the sophistication level appropriate for their stage?
* Is there a specific, high-conviction reason this play fits this company in particular?

Be opinionated. Skip plays that don't fit. Don't pad the list with generic options. If two plays are very similar, pick the better one. Call out the one or two plays you'd stake a reputation on for this company.

## Step 4: Generate Output

Use this format exactly:

---

## Recommended GTM Plays for [Company/Product Name]

**GTM motion**: [Sales-led / PLG / Marketing-led / Hybrid]  
**Stage**: [Early / Growth / Scaling]  
**Biggest untapped signal**: [One sentence on the highest-leverage signal this company isn't yet operationalizing]

---

### Priority Plays

**[Rank]. [Play Name]** · [Category] · Difficulty: [Beginner / Intermediate / Advanced]

**Signal**: [What triggers this play — be specific]  
**How it works**: [2-3 sentence description of the automation workflow, including how data flows]  
**Tools**: [Comma-separated tools that enable this]  
**Why this fits you**: [1-2 sentences grounded specifically in their product, ICP, or motion — not generic]

---

[Repeat for each play]

---

### Where to Start

[1-2 sentences recommending which play to launch first and why, based on ease of setup and expected impact given their stage and existing data]

### Future State

[2-3 plays worth building once the priority plays are running — these can require more data access or sophistication]

---

## Tone

Write like a senior GTM practitioner giving direct advice — specific, grounded, and opinionated. Avoid hedge-everything consulting language. If a play is a clear winner for this company, say so. If a play is tempting but wrong for their stage, say why you left it out.
