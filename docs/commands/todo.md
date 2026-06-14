# /todo

Scan the project for remaining TODO items in roadmap files and inline source comments.

## What It Does

1. Searches for roadmap or TODO files in common locations (`TODO.md`, `docs/TODO.md`, `docs/research/todo.md`, `ROADMAP.md`)
2. If found, parses the file and summarizes:
    - Items marked as done (strikethrough or checkmarks)
    - Items still open, grouped by priority or category
    - Count of done vs. remaining
3. Scans source files for inline markers: `TODO`, `FIXME`, `HACK`, `XXX`
4. Presents a combined summary

## Example

```
/todo
```

Typical output:

```
Roadmap: docs/research/todo.md
================================
Done:   14 items
Open:    6 items

Open Items:
  [High]   Add retry logic to IB reconnection
  [High]   Implement PCE event handler
  [Medium] Add Telegram alert for circuit breaker reset
  [Medium] Write integration tests for order pipeline
  [Low]    Dashboard: add drawdown chart
  [Low]    Docs: document deployment process

Inline TODOs (source code):
================================
  src/broker/client.py:142       TODO: handle daily disconnect gracefully
  src/risk/circuit_breaker.py:87 FIXME: race condition on concurrent checks
  src/strategy/straddle.py:203   TODO: add spread check before entry
  tests/unit/test_journal.py:45  TODO: add edge case for empty trades

Total: 14 done, 6 roadmap + 4 inline = 10 remaining
```

!!! warning "Inline markers in third-party code"
    The scan filters by common source extensions (`.py`, `.ts`, `.js`) and limits results to 30 entries to avoid noise from vendored or generated files.

## Notes

- Roadmap files are read in full; inline TODOs are found via `grep -rn`
- The command distinguishes between `TODO` (planned work), `FIXME` (known bugs), `HACK` (technical debt), and `XXX` (dangerous or fragile code)
- If no roadmap file exists, only inline markers are reported
