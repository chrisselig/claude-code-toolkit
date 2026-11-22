# Diagnosing Bugs

A disciplined loop for hard, intermittent, or performance-regression bugs.
The rule it enforces: build something that can go red on the exact symptom
**before** forming a theory — a theory with nothing to test it against is a
guess wearing a lab coat.

Trigger: `/diagnosing-bugs`

## How It Works

1. **Redact** — secrets replaced with `<REDACTED>` before anything is shown;
   build loops against env vars, not hardcoded values.
2. **Build a feedback loop** that can go red on this exact bug: a failing
   test, a curl/CLI repro diffed against a known-good snapshot, a headless
   browser script, a replayed trace, a fuzz loop, a bisection loop, a
   differential loop. Tighten it — faster, more specific, more deterministic.
3. **Reproduce and minimize** — confirm it's the user's actual symptom, then
   cut inputs one at a time until every remaining piece is load-bearing.
4. **Hypothesize** — 3–5 ranked, falsifiable predictions, shown to the user
   once before testing any of them.
5. **Instrument** — one variable at a time; tagged `[DEBUG-xxxx]` logs if a
   debugger isn't available; measure-first for performance regressions.
6. **Fix + regression test** — written before the fix, at a seam that
   actually exercises the bug pattern; re-run the original loop after.
7. **Clean up** — repro no longer reproduces, debug tags removed, throwaway
   harnesses deleted, the winning hypothesis named in the commit message.

## Stop Condition

If no feedback loop can be built after a genuine attempt, the skill stops
and asks for a reproducing environment, a redacted artifact, or permission
to add temporary instrumentation — it does not proceed to hypothesizing
without one.

## Notes

- Non-deterministic bugs: the goal is a *higher reproduction rate*, not a
  clean one-shot repro.
- A manual step only a human can do still needs a script wrapped around it —
  see [Wizard](wizard.md) if that manual part needs its own walkthrough.
- Adapted from [mattpocock/skills](https://github.com/mattpocock/skills)
  (MIT license).
