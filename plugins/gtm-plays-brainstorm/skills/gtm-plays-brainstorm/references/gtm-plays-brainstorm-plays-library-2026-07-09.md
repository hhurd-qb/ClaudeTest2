# GTM Plays Library

A curated library of 25+ automated outbound and GTM plays synthesized from Growth Unhinged research and practitioner playbooks. Each play includes signal, mechanism, tools, difficulty, and GTM motion fit.

---

## Category Overview

* **Signal-based plays** (1–9): Triggered by behavioral or firmographic signals indicating buying intent
* **Warm outbound plays** (10–14): Target people with prior relationship, brand, or network proximity
* **Personalization plays** (15–17): Enhance relevance of any outreach through contextual data
* **Social plays** (18–19): Leverage LinkedIn activity and content engagement
* **Product-led plays** (20–24): Require product usage data; PLG/hybrid only
* **Expansion plays** (25–26): Target existing customers for upsell/expansion

---

## Signal-Based Plays

Signal-based plays consistently outperform cold outreach by 2x-10x. Prioritize these when a clear, timely signal exists.

### 1. Website Visitor De-anonymization

**Signal**: Company or person visits your website — especially high-intent pages (pricing, integrations, enterprise)  
**How it works**: Use a de-anonymization tool to identify visiting companies (and sometimes contacts). Enrich with Clay. Score with AI. Route Tier 1 accounts to Slack for immediate cold calling; Tier 2–3 enter automated email/LinkedIn sequences.  
**Tools**: Warmly, RB2B, Apollo, CommonRoom, Koala, ZoomInfo (de-anon); Clay (enrichment); BetterContact (phone); Instantly / HeyReach (sequences)  
**Difficulty**: Beginner  
**Best for**: All GTM motions  
**Pro-tip**: Don't explicitly say "I saw you on our pricing page." Reference the underlying topic (e.g., scaling sales, reducing churn) naturally.

### 2. Competitor Displacement via Tech Stack Signals

**Signal**: Company is using a competitor or complementary tool (identified via BuiltWith, job postings, or intent data)  
**How it works**: Build a list of companies using a specific tech stack. Enrich with relevant contacts. Run a displacement or expansion campaign referencing a specific use case or pain point relevant to that tool stack.  
**Tools**: BuiltWith, Theirstack, Sumble (tech signals); Clay (enrichment); Apollo / ZoomInfo (contacts)  
**Difficulty**: Intermediate  
**Best for**: Sales-led, marketing-led  
**Pro-tip**: Job postings are a great proxy for tech stack — a Data Engineer role mentioning Snowflake reveals the stack even if BuiltWith can't detect it.

### 3. Look-alike Targeting (Closed-won Similarity)

**Signal**: Company matches the profile of recently closed-won customers  
**How it works**: Pull closed-won accounts from CRM. Use AI to identify what they share (industry, size, tech stack, hiring patterns, growth signals). Build a look-alike list and run cold outreach targeting their profiles.  
**Tools**: Clay, Apollo, ZoomInfo (list building); ChatGPT / AI (pattern matching); CRM  
**Difficulty**: Intermediate  
**Best for**: Sales-led, marketing-led

### 4. Job Change of Champions

**Signal**: A past champion (closed-won contact) moves to a new ICP-fit company  
**How it works**: Track when contacts from closed-won accounts change jobs. When they land at a new ICP-fit company, reach out — they already know your product and can be your internal champion at the new account.  
**Tools**: Champify, UserGems, Clay, CommonRoom, Koala, Pocus, Unify, ZoomInfo  
**Difficulty**: Beginner  
**Best for**: All GTM motions  
**Pro-tip**: Send a small gift to welcome them to their new role — automate this with Postal, Reachdesk, or Sendoso.

### 5. LinkedIn Engagement (Own Content)

**Signal**: ICP-fit person recently liked, commented, or reposted your team's LinkedIn content  
**How it works**: Track engagement on all employee posts using Trigify. Track profile visitors with Teamfluence. Route data to Clay via webhook. Qualify and enrich. Enroll in tiered sequences based on lead score.  
**Tools**: Trigify (engagement tracking), Teamfluence (profile visitors), Clay (routing + enrichment), Findymail (email finding), ChatGPT (qualification), HeyReach / Instantly (sequences)  
**Difficulty**: Intermediate  
**Best for**: Marketing-led, sales-led  
**Performance data**: LinkedIn connections of founders — a related signal-based play — generated a 25.4% reply rate ([Workflows.io](http://Workflows.io), 2025). Signal-based plays from content consistently outperform cold.

### 6. LinkedIn Connections of Founders/Execs

**Signal**: Person is a 1st-degree LinkedIn connection of a company founder or exec AND fits ICP criteria  
**How it works**: Export LinkedIn connections natively (no extra tools required). Run company and person qualification through Clay. Score with ChatGPT. Route by tier: Tier 1 to cold calling, Tier 2–3 to automated email + LinkedIn sequences. Messaging can be conversational since they've warmed up to your content.  
**Tools**: LinkedIn (native export), Clay, ChatGPT, HubSpot, Instantly, HeyReach, BetterContact  
**Difficulty**: Beginner  
**Best for**: All GTM motions  
**Why it works**: These prospects have already been exposed to your network and content; outreach feels warm rather than cold.

### 7. Social Listening (Keyword Monitoring)

**Signal**: ICP-fit person engages with LinkedIn posts containing relevant keywords (competitor name, pain-point topic, category keyword)  
**How it works**: Clay continuously monitors LinkedIn for specific keywords. Captures who's engaging with those posts. Enriches contact and company data. ChatGPT qualifies ICP fit. Assigns leads to sequences based on score.  
**Tools**: Clay (keyword monitoring + enrichment), ChatGPT (qualification), HubSpot, HeyReach, Instantly, Findymail, BetterContact  
**Difficulty**: Intermediate  
**Best for**: Marketing-led, sales-led

### 8. Relevant Job Postings

**Signal**: Company posts a job that signals they need what you sell or are using a specific technology  
**How it works**: Monitor job boards for relevant postings. When a company posts a target role (e.g., VP Sales for a sales tool vendor; Data Engineer mentioning Snowflake for a data product), trigger outreach to the relevant buyer persona.  
**Tools**: Clay, Theirstack, Sumble  
**Difficulty**: Intermediate  
**Best for**: Sales-led, marketing-led  
**Example**: A sales candidate database company scans target accounts daily. When any posts for an AE, it sends the VP of Sales 3 pre-vetted candidates with "if you want more like this, I can give you a tour."

### 9. Geo/Event-based Outreach

**Signal**: Upcoming or recent conference, sports event, or city-specific milestone relevant to your ICP  
**How it works**: Build an ICP-filtered list of prospects in a specific city or attending a specific event. Personalize outreach referencing the event as a reason to connect in person or acknowledge a shared context.  
**Tools**: Apollo, ZoomInfo (geo-filtered lists); Clay (enrichment)  
**Difficulty**: Beginner  
**Best for**: Sales-led

---

## Warm Outbound Plays

These plays target people with some prior relationship, brand awareness, or network proximity. They typically require less trust-building than cold outreach.

### 10. Customer Alumni

**Signal**: Person previously worked at a closed-won customer account and has since moved to a new ICP-fit company  
**How it works**: Pull closed-won accounts from CRM. Use Clay to find people who used to work there. Qualify their current company. Score with ChatGPT. Route to tiered outreach — Tier 1 gets manual prospecting, Tier 2-3 get automated email + LinkedIn sequences.  
**Tools**: HubSpot (CRM), Clay (alumni lookup + enrichment), ChatGPT (scoring), Instantly, HeyReach  
**Difficulty**: Intermediate  
**Best for**: Sales-led, marketing-led

### 11. Closed-lost Reopen (9-month cadence)

**Signal**: Opportunity was closed-lost exactly 9 months ago  
**How it works**: CRM automation flags Closed-lost opportunities at the 9-month mark. For Tier 1 accounts, notify the account owner and make Step 1 manual. For others, enroll in an automated sequence. Use the OpenAI API to summarize the last call and insert a personalized reference line ("To jog your memory, here's what we discussed…").  
**Tools**: HubSpot or any CRM (native trigger), OpenAI API (call summary), sales engagement tool  
**Difficulty**: Beginner  
**Best for**: Sales-led  
**Pro-tip**: The call summary personalization hook is highly effective — it shows you remember them without being generic.

### 12. Champion Tracking (Job Changes — All Buyers)

**Signal**: Any key buyer persona in your CRM changes companies — not just closed-won contacts  
**How it works**: Track any contact in your CRM who fits a key buyer persona and changes jobs. Automatically reach out to welcome them to their new role and explore if they'd use your product again or at the new company.  
**Tools**: Champify, Clay, CommonRoom, Koala, Pocus, Unify, UserGems, ZoomInfo  
**Difficulty**: Beginner  
**Best for**: All GTM motions

### 13. Warm Intro via Mutual Investors or Advisors

**Signal**: Target account shares a mutual investor, advisor, or customer connection  
**How it works**: Map your investor and advisor network against your target account list. Identify warm paths in. Request introductions programmatically or flag accounts for reps to pursue manually via Sales Navigator.  
**Tools**: Cabal, Commsor, The Swarm (network mapping); Sales Navigator (manual lookup)  
**Difficulty**: Intermediate  
**Best for**: Early-stage sales-led; also effective at growth stage for Tier 1 accounts

### 14. Prior Colleagues of New Flagship Customers

**Signal**: A new flagship customer just signed → their former colleagues at prior companies may be ICP-fit  
**How it works**: When a landmark deal closes, run an automated lookup of where key contacts at that company previously worked. Find ex-colleagues now at ICP-fit companies. Reach out referencing the mutual connection.  
**Tools**: Clay, LinkedIn  
**Difficulty**: Intermediate  
**Best for**: Sales-led

---

## Personalization Plays

These plays enhance the relevance of any outreach through contextual data. They work best layered on top of a signal-based targeting strategy.

### 15. Pre-call Research Brief

**Signal**: Upcoming first meeting booked in CRM  
**How it works**: Automatically pull a prospect research brief before the first call — recent news, competitive intel, LinkedIn activity, company milestones, open roles. Deliver to the rep via Slack or CRM task before the meeting.  
**Tools**: Clay, ChatGPT, HubSpot, Slack  
**Difficulty**: Intermediate  
**Best for**: Sales-led

### 16. Account-specific Landing Pages

**Signal**: Target account in an active outreach sequence  
**How it works**: Create dynamic landing pages personalized to the prospect's company, industry, and pain points. Link from outbound emails as the primary CTA.  
**Tools**: Mutiny, Intellimize  
**Difficulty**: Advanced  
**Best for**: Sales-led (Tier 1 accounts), marketing-led at scale

### 17. 1:1 Video Outreach (Automated)

**Signal**: Target account in an active outreach sequence — typically Tier 1 or 2  
**How it works**: Create personalized short videos referencing the prospect's company name, website screenshot, or a specific pain point. AI-assisted tools can semi-automate production at scale.  
**Tools**: Sendspark, Vidyard, Loom  
**Difficulty**: Intermediate  
**Best for**: Sales-led (Tier 1/2 accounts)

---

## Social Plays

### 18. LinkedIn Connection Request with Content Reference

**Signal**: ICP-fit person, no existing LinkedIn connection  
**How it works**: Run a LinkedIn connection request campaign that references a specific post the person engaged with — or one of your posts — as the reason for connecting.  
**Tools**: HeyReach, Expandi, Dripify  
**Difficulty**: Beginner  
**Best for**: Sales-led, marketing-led

### 19. Influencer/Creator Audience Prospecting

**Signal**: Active LinkedIn creator in your ICP space engaging relevant content  
**How it works**: Identify people in your ICP who are active LinkedIn creators or have significant followings. Build a prospect list from their engaged audience (likers, commenters, followers).  
**Tools**: Clay, Trigify  
**Difficulty**: Advanced  
**Best for**: Marketing-led, content-heavy companies

---

## Product-led Plays

These plays require access to product usage data. Only recommend for companies with a PLG or hybrid GTM motion.

### 20. PQL Outbound (End Users + Decision Makers)

**Signal**: User reaches a product-qualified lead (PQL) threshold — e.g., completes a key activation event  
**How it works**: When a PQL is detected, three things happen automatically: (1) the PQL user enters an info-gathering sequence, (2) other end users at the same company are identified and added to sequences, (3) decision makers at the company are found and added to a DM-specific sequence. This creates multi-threaded outbound across the account.  
**Tools**: Apollo, Clay, CommonRoom, Koala, Pocus, ZoomInfo (contact finding); data warehouse + reverse-ETL tool like Census or Hightouch (for product data connection to CRM)  
**Difficulty**: Advanced  
**Best for**: PLG, hybrid PLG  
**Pro-tip**: For low-ACV products, the CTA should drive free sign-ups. For high-ACV, gather end-user feedback and package it into a deck for the decision maker.

### 21. Non-user Expansion (Existing Account)

**Signal**: Account has 1+ existing user(s) but many potential users in the org who haven't adopted  
**How it works**: Identify non-users within accounts that already have existing product users. Reach out to pull them in with a specific use case or team angle — or surface the account to a sales rep for expansion outreach.  
**Tools**: Product data + CRM; Apollo or ZoomInfo (contact finding)  
**Difficulty**: Intermediate  
**Best for**: PLG, hybrid PLG

### 22. Aha Moment Trigger

**Signal**: Free or trial account reaches a key activation milestone in the product  
**How it works**: When an admin reaches the aha moment (product-defined), trigger an automated sales outreach sequence to convert them to paid. Reference their specific in-product action as context.  
**Tools**: Product instrumentation + CRM; Pocus, Koala, or CommonRoom (PLS platform); sales engagement tool  
**Difficulty**: Intermediate  
**Best for**: PLG

### 23. High-intent Page Visit (Existing Product User)

**Signal**: An existing product user (free or trial) visits a high-intent page — pricing, integrations, enterprise  
**How it works**: When a known product user visits a high-intent page, trigger outreach to the admin or relevant decision maker referencing their interest in a specific area.  
**Tools**: Website visitor tracking + product data integration; CRM; sales engagement tool; Warmly  
**Difficulty**: Intermediate  
**Best for**: PLG, hybrid PLG

### 24. Multi-domain Roll-up (Exec Buyer)

**Signal**: Multiple accounts or signups from the same parent domain or organization  
**How it works**: When multiple accounts or product users from the same org are identified, trigger an outbound campaign targeting an exec buyer to consolidate into an enterprise deal.  
**Tools**: CRM (roll-up detection); Clay (enrichment); sales engagement tool  
**Difficulty**: Intermediate  
**Best for**: PLG, hybrid PLG

---

## Expansion Plays

### 25. Usage Limit Approaching

**Signal**: Account's product usage (seats, credits, API calls) is approaching their plan limit  
**How it works**: Programmatically reach out to the admin when usage approaches the limit. For high-ACV accounts, push a Slack notification to the Account Manager. For low-ACV, fully automate.  
**Tools**: Product data + CRM; Pocus, Koala, CommonRoom (PLS); sales engagement tool  
**Difficulty**: Intermediate  
**Best for**: PLG, hybrid PLG  
**Pro-tip**: For low ACV: automate fully. For high ACV: human review before sending.

### 26. Free Trial of Upsell Package

**Signal**: Account begins a free trial of a higher-tier feature set or package  
**How it works**: When an account starts an upsell trial, automatically trigger an outreach sequence offering setup assistance, a training session, or a check-in call to maximize trial-to-paid conversion.  
**Tools**: Product data + CRM; sales engagement tool  
**Difficulty**: Beginner  
**Best for**: PLG, hybrid PLG

---

## Quick Reference: GTM Motion → Best Plays

### Sales-led (SDR/AE outbound)

Start with: Website visitor de-anon (#1), LinkedIn connections of founders (#6), Closed-lost reopen (#11), Champion tracking (#12)  
Layer: Social listening (#7), competitor displacement (#2), job postings (#8), LinkedIn engagement (#5)  
Advanced: Look-alike targeting (#3), warm intros (#13), personalized video (#17), customer alumni (#10)

### Product-led (PLG / self-serve)

Start with: Website visitor de-anon (#1), Champion tracking (#12), PQL outbound (#20)  
Layer: Aha moment trigger (#22), high-intent page visit (#23), usage limit approaching (#25)  
Advanced: Multi-domain roll-up (#24), non-user expansion (#21)

### Marketing-led (inbound + content)

Start with: LinkedIn engagement — own content (#5), LinkedIn connections of founders (#6), Closed-lost reopen (#11)  
Layer: Social listening (#7), look-alike targeting (#3), champion tracking (#12)  
Advanced: Influencer/creator prospecting (#19), account-specific landing pages (#16)

### Hybrid (PLG + sales)

All of the above. Prioritize: Website visitors (#1), PQL outbound (#20), champion tracking (#12), LinkedIn engagement (#5)

---

## Quick Reference: Company Stage → Sophistication Level

### Early (pre-$1M ARR, <10 employees)

Run 1-2 plays max. Use existing data. Don't over-engineer.  
Best fits: Closed-lost reopen (#11), LinkedIn connections of founders (#6), website visitors (#1), champion tracking (#12)

### Growth ($1M–$20M ARR, 10–100 employees)

Run 3-5 plays in parallel. Begin layering signals and building a targeting stack.  
Add: LinkedIn engagement (#5), social listening (#7), job postings (#8), customer alumni (#10)

### Scaling ($20M+ ARR, 100+ employees)

Full signal stack. Micro-campaigns (50-250 contacts, specific and refreshed frequently). Stack signals for tiered lead scoring.  
Add: Look-alike targeting (#3), warm intros (#13), PQL outbound (#20), expansion plays (#25-26), personalized landing pages (#16)
