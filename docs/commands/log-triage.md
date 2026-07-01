# /log-triage

Turn a log file from an unattended run (ETL pipeline, trading bot, cron job) into a short, honest summary of what happened and what needs attention. Built for Loguru output but works on any leveled log.

## What It Does

1. Locates the log (named file or conventional `logs/` path; most recent by default).
2. Counts events by level (`DEBUG/INFO/SUCCESS/WARNING/ERROR/CRITICAL`).
3. Extracts every ERROR/CRITICAL with timestamp and traceback, **grouping duplicates** with a count.
4. Reconstructs the run narrative from INFO/SUCCESS lines — stage row counts, trades, start/end, duration.
5. Flags anomalies: zero/collapsed row counts, retry loops, disconnects, long timestamp gaps, a start with no completion.
6. Presents a one-line verdict plus grouped errors and a "what to look at" list.

## Example

```
/log-triage
```

```
Log Triage: logs/pipeline_2026-07-01.log
Verdict: FAILED — run started but never completed

Levels: INFO 412 | SUCCESS 3 | WARNING 8 | ERROR 1 | CRITICAL 0

Narrative:
  06:00:02  Pipeline start
  06:00:07  Transformed 14,180 rows (23 dropped: null date)
  06:00:09  ERROR loading to MotherDuck — no completion after this

Errors (grouped):
  ×1  ConnectionError: MOTHERDUCK_TOKEN expired (06:00:09)

Look at:
  1. Token expired mid-run — rotate MOTHERDUCK_TOKEN, re-run.
  2. 23 rows dropped for null date upstream — check the source export.
```

!!! tip "Pair with cron"
    Run `/log-triage` after any overnight job to see how it went without reading raw logs. Feed a trading run's findings into `/trade-review` or `/add-event-source`.

## Notes

- Loguru's default format is `time | LEVEL | module:function:line - message`; parsing falls back to level-name matching for other logs.
- Always groups repeated errors with a count so the one that matters isn't buried.
- A start line with no completion line is a crash or hang — flagged even without an explicit ERROR.
- Read-only triage — it diagnoses, it does not edit code or config.
