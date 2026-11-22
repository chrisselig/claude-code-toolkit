---
name: research
description: Delegate a factual investigation to a background agent that reads primary sources and writes findings to a Markdown file instead of filling the main conversation. Use when the user wants a topic researched, API or documentation facts gathered, or reading legwork offloaded while other work continues.
argument-hint: "[question to investigate]"
---

# Research

Spin up a background agent with a fresh context window to do the reading,
so the main conversation keeps working instead of filling up with pages of
docs excerpts. The agent's output is a cited file, not a wall of text.

## Steps

1. **Pin down the question precisely.** A background agent can't ask
   follow-up questions mid-run, so restate an ambiguous request back to the
   user before launching — "which SDK version?", "the REST or the webhook
   API?" — rather than guessing and finding out later the agent answered
   the wrong question.

2. **Launch a background agent** (this toolkit's `Agent` tool with a fresh,
   non-forked agent, or a forked agent if the investigation genuinely needs
   this conversation's context) with a self-contained brief covering steps
   3–5 below. It gets no other context than what the brief states.

3. **Its job: investigate against primary sources only** — official docs,
   source code, specs, first-party APIs — not a blog post or forum thread
   summarizing them. Follow every claim back to the source that actually
   makes it. If two sources disagree, state the disagreement rather than
   silently picking one.

4. **Write the findings to a single Markdown file, citing each claim's
   source** (a URL, or a `file:line` for a source-code claim). Save it where
   the repo already keeps this kind of note; if there's no existing
   convention, create one location (e.g. `docs/research/`) and say so
   rather than scattering files wherever felt convenient.

5. **Report back a short summary** — a few sentences plus the file path —
   not the full file contents, so the main conversation doesn't inherit
   everything the background agent read.

## Examples

### GOOD vs BAD: sourcing a claim

**BAD:**
> Rate limits are 100 req/min.

No source — could be stale, could be a different pricing tier, could be
wrong.

**GOOD:**
> Rate limit: 100 req/min on the free tier (docs: `api.example.com/docs/limits`,
> retrieved 2026-11-22; confirmed in the SDK source via
> `RATE_LIMIT_FREE = 100` at `config.py:42`).

### GOOD vs BAD: where findings land

**BAD** — the agent's answer is five pages of docs excerpts pasted directly
into the chat, pushing everything else out of context.

**GOOD** — the agent writes `docs/research/stripe-webhook-retries.md` with
citations, and the chat gets three sentences and the path.

## Notes

- A fresh-context background agent avoids anchoring on whatever the main
  conversation already assumed about the answer — it reads the primary
  source cold, rather than confirming a bias already in play.
- If primary sources conflict or are silent on the question, the file says
  so explicitly rather than filling the gap with an inference presented as
  settled fact.
- This is for read-only fact-finding. If the task is "go implement X based
  on the docs," that's ordinary delegated work, not this skill — the
  distinguishing feature here is that the deliverable is a cited note, not
  code.
- Adapted from mattpocock/skills (`research`, MIT license), © Matt Pocock.
