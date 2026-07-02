---
name: log-triage
description: Parse a Loguru (or plain) log file from a pipeline or bot run, surface errors and warnings, and summarize what happened. Use when the user wants to know how an unattended run went, diagnose a failure, or scan logs for anomalies.
argument-hint: "[log file path (defaults to newest in logs/)]"
---

# Log Triage

Turn a log file from an unattended run (ETL pipeline, trading bot, cron job) into a short, honest summary of what happened and what needs attention.

## Steps

1. Locate the log from the user's request or the project's conventional path (`logs/`, a Loguru sink, or a file they name). If several exist, use the most recent unless told otherwise.

2. Scan the log and count events by level: `TRACE/DEBUG/INFO/SUCCESS/WARNING/ERROR/CRITICAL` (Loguru levels). Report the totals.

3. **Extract every ERROR and CRITICAL** with its timestamp, message, and — if present — the traceback. Group identical/similar errors so a message repeated 500 times is reported once with a count, not 500 lines.

4. **Pull the run's narrative** from INFO/SUCCESS lines: pipeline stage counts (extracted N -> transformed M -> loaded M), trades placed/closed, start and end timestamps, total duration. Flag if the run has a start but no clean completion line (crashed or still running).

5. **Flag anomalies** beyond raw errors:
   - Row counts that dropped to zero or fell sharply vs the narrative.
   - Retries / backoff / reconnect loops (source flakiness).
   - Warnings about spread, single-leg fills, disconnects (trading bot).
   - Long gaps between timestamps (a stall).

6. **Present a concise report:** a one-line verdict (clean / warnings / failed), the level counts, the grouped errors with counts, the run narrative, and a short "what to look at" list.

## Example

```
Log Triage: logs/pipeline_2026-07-01.log
================================================
Verdict: FAILED — run started but never completed

Levels: INFO 412 | SUCCESS 3 | WARNING 8 | ERROR 1 | CRITICAL 0

Narrative:
  06:00:02  Pipeline start
  06:00:05  Extracted 14,203 rows from API
  06:00:07  Transformed 14,180 rows (23 dropped: null date)
  06:00:09  ERROR loading to MotherDuck — no clean completion after this

Errors (grouped):
  ×1  ConnectionError: MOTHERDUCK_TOKEN expired (06:00:09)
        duckdb.IOException: Could not connect to md:trading

Warnings (grouped):
  ×8  Rate limit hit, backing off 2s (06:00:03–06:00:05)

Look at:
  1. Token expired mid-run — rotate MOTHERDUCK_TOKEN, then re-run.
  2. 23 rows dropped for null date upstream — check the source export.
  3. 8 rate-limit warnings — extract nearly tripped the API's limit.
```

## Notes

- Loguru's default format is `time | LEVEL | module:function:line - message`. Parse on that structure; fall back to substring matching on level names for non-Loguru logs.
- Always group repeated errors with a count. A wall of identical tracebacks buries the one error that matters.
- A run with a start line but no success/completion line is a crash or a hang — call it out even if there is no explicit ERROR.
- This is read-only triage. It diagnoses; it does not edit code or config. For fixing failing tests use `/test`; for the trading pipeline, feed findings into `/trade-review` or `/add-event-source`.
- If the log is huge, scan for level markers and timestamps rather than reading every line; report the window actually examined.
