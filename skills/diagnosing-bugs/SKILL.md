---
name: diagnosing-bugs
description: A disciplined loop for hard, intermittent, or performance-regression bugs — build a feedback loop that can go red on the exact symptom before hypothesizing, then reproduce, minimize, rank hypotheses, instrument, fix, and clean up. Use when the user says "diagnose" or "debug this", reports something broken/throwing/failing/slow, or a quick guess-and-fix attempt didn't stick.
argument-hint: "[symptom or failing command]"
---

# Diagnosing Bugs

The failure mode this skill exists to prevent: reading the code, forming a
theory, and editing based on the theory — with nothing that can prove the
theory right or wrong. Build something that can go red on the bug *first*;
everything after that is mechanical.

## Steps

1. **Redact before showing anything.** Any command output, log, or captured
   artifact pasted into the conversation or written to a file gets secrets
   replaced with `<REDACTED>` first. Read credentials from env vars rather
   than hardcoding them into a reproduction script, so a shown command never
   carries a live value.

2. **Build a feedback loop that can go red on this exact bug.** This is the
   real work. In roughly this order of preference: a failing test at the
   nearest seam, a script/curl against a running instance, a CLI invocation
   diffed against a known-good snapshot, a headless-browser script asserting
   on DOM/console/network, a replayed captured trace, a minimal throwaway
   harness, a fuzz loop (for "sometimes wrong output" bugs), a bisection loop
   (`git bisect run`), a differential loop (old version vs new, or config A
   vs B). Tighten whatever you build: make it faster, make the assertion
   specific to the symptom (not "didn't crash"), make it deterministic
   (pin time, seed RNG, isolate the filesystem, freeze network).
   - **Stop condition:** if no loop is buildable after a genuine attempt,
     say so explicitly, list what you tried, and ask the user for a
     reproducing environment, a redacted captured artifact (log dump, HAR
     file, screen recording with timestamps), or permission to add
     temporary instrumentation. Do not move to step 4 without a loop.

3. **Run the loop and confirm it reproduces the user's actual symptom** —
   not a different failure that happens to live nearby. For non-deterministic
   bugs, the goal is a *higher reproduction rate*, not a clean one-shot
   repro: loop the trigger 100×, parallelize, add stress, narrow timing
   windows. A 50%-flake bug is debuggable; a 1% one usually isn't yet — keep
   raising the rate until it is. Then minimize: cut inputs, callers, config,
   and steps one at a time, re-running after each cut, until every remaining
   element is load-bearing (removing any one of them makes the loop go
   green).

4. **Generate 3–5 ranked, falsifiable hypotheses before testing any of
   them.** Each one states a prediction: "if X is the cause, then changing Y
   makes the bug disappear / changing Z makes it worse." A hypothesis that
   can't be phrased that way is a vibe — sharpen it or drop it. Show the
   ranked list to the user once; they often have domain knowledge that
   re-ranks it instantly ("we just deployed a change to #3") or rules one
   out. Don't block on a response — proceed with your own ranking if they're
   not around.

5. **Instrument to test the hypotheses, one variable at a time.** Prefer a
   debugger/REPL breakpoint over logs where the environment supports it —
   one breakpoint beats ten log lines. If logging, tag every line with a
   unique prefix (e.g. `[DEBUG-a4f2]`) so cleanup is a single grep, and never
   "log everything and grep after." For performance regressions, logs are
   usually the wrong tool: establish a baseline with a timing harness or
   profiler, then bisect against it — measure first, guess second.

6. **Write the regression test before the fix, at the seam that exercises
   the real bug pattern.** If the only available seam is too shallow to
   replicate what actually triggered the bug (a unit test when the bug needs
   the chain of callers that produced it), that gap is itself a finding —
   note it, and apply the fix without pretending a shallow test proves
   anything. If a correct seam exists: turn the minimized repro into a
   failing test, watch it fail, apply the fix, watch it pass, then re-run
   the original (un-minimized) loop from step 3 to confirm the real-world
   case is fixed too, not just the minimized one.

7. **Clean up before declaring done:**
   - [ ] the original repro from step 3 no longer reproduces
   - [ ] the regression test passes (or its absence is explicitly documented)
   - [ ] every `[DEBUG-...]` line is removed (`grep` the prefix to confirm)
   - [ ] throwaway harnesses/scripts are deleted
   - [ ] the hypothesis that turned out correct is named in the commit or PR
         message, so the next person who hits this doesn't re-diagnose it

## Examples

### GOOD vs BAD: starting the investigation

**BAD** — a theory with nothing behind it:
> "This looks like a race condition in `fetchUser` — here's a fix."

No step above ever ran. The "fix" has no way to be proven right, and no way
to be proven wrong either.

**GOOD** — a loop first:
```bash
pytest tests/test_fetch_user.py::test_concurrent_fetch -x
# FAILED: expected 1 call, got 3 — reproduces every run
```
Now every hypothesis in step 4 has something to test against.

### GOOD vs BAD: hypothesis generation

**BAD** — one hypothesis, tested by editing immediately: "probably a caching
bug" → starts rewriting the cache layer with no prediction stated, so a
negative result ("still broken") teaches nothing about *why*.

**GOOD** — ranked and falsifiable:
```
1. Cache key missing tenant_id → predicts: adding tenant_id to the key fixes it.
2. Retry logic double-fires on timeout → predicts: raising the timeout makes it worse.
3. Stale connection-pool entry → predicts: restarting between calls hides the bug.
```
Each one, tested, narrows the search even when it's wrong.

## Notes

- Never skip step 2 to save time. A theory built from reading code alone,
  with no red-capable check behind it, is the exact failure this skill
  exists to prevent — it feels faster and is usually slower, because a wrong
  fix still has to be diagnosed later.
- A manual step only a human can perform (clicking through a UI) still needs
  a structured loop wrapped around it — script the setup and the assertion,
  so the human click is the only unautomatable part. See `/wizard` if the
  manual part itself needs a repeatable walkthrough.
- If the bug involves a secret-touching path (auth headers, tokens in a
  captured request), redact before the first message that shows it, not
  after — once a secret is in the conversation transcript, redacting later
  doesn't undo that.
- Adapted from mattpocock/skills (`diagnosing-bugs`, MIT license), © Matt Pocock.
