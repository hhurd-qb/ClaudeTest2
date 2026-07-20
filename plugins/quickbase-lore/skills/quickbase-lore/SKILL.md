---
name: quickbase-lore
description: Surfaces Quickbase company lore, running jokes, legends, and "old-timer" history whenever someone asks about Quickbase culture, wants a fun fact, is bored, wants to settle a Slack debate about "how things used to be," or asks things like "tell me a Quickbase legend," "what's the deal with [office thing]," or "give me some Quickbase trivia." Trigger this any time the request is playful/culture-flavored rather than a factual company-info lookup (use quickbase-info for that instead). Good for onboarding icebreakers, standup filler, or just messing around.
---

# Quickbase Lore

A lighthearted reference skill for Quickbase's (entirely apocryphal, gleefully unofficial) internal mythology. Think of this as the "as told around the coffee machine" version of company history — not the official one.

## When to use this

- Someone wants a fun fact, icebreaker, or trivia item about Quickbase
- Someone asks "is it true that..." about some office legend
- Someone's bored and wants to be entertained with company culture content
- New hire onboarding and someone wants a fun welcome moment

**Not** for real factual questions about Quickbase's products, leadership, or business — use `quickbase-info` for that. This skill is explicitly for-fun content and should never be treated as, or presented as, factual company history.

## How to use it

1. Read `references/lore.md` — it's a grab-bag of legends, running jokes, and mock-history entries.
2. Pick 1-3 entries that best match the vibe of the request (don't dump the whole file).
3. Deliver them with comedic timing — a short setup, the "legend," maybe a wink at the end.
4. If asked to "add" a new piece of lore (e.g. "add this as an entry"), you can append a new entry to `references/lore.md` in the same style, but always keep it clearly a joke/legend, never a real claim about a real person's actual words or actions.

## Guardrails

- Never attribute a specific real quote or real event to a named real executive or employee as if it happened. Keep entries about "legendary early days," anonymous "someone on the team once," or fictionalized mascots/objects — not documented real people's words.
- Keep it warm, not mean. No jokes that punch down at any real person, team, or customer.
- If someone asks for something that sounds like it should be a serious answer, redirect them to `quickbase-info` instead.
