# /healthcheck

Confirm that an unattended job did what it was supposed to. Answers "did last night's run actually work?" by checking a database's reachability, freshness, volume, and continuity against expectations — without watching it live.

## What It Does

1. **Reachability** — connect to the target database; if it fails (expired token, wrong URL), report that first.
2. **Freshness** — age of the newest row vs the expected cadence plus a grace margin, accounting for weekends/holidays.
3. **Volume** — recent row counts vs the recent norm (0 rows or 10x is a problem even if the job "completed").
4. **Continuity** — gaps in the expected sequence across the recent window, not just at the tail.
5. **Verdict** — a per-check pass/fail table with actual numbers and, on failure, the likely cause and fix.

## Example

```
/healthcheck
```

```
Healthcheck: Turso `trading` — trades + bars
DB reachable    PASS   connected in 180ms
Freshness       FAIL   newest bar age 38h (expected < 25h)
Volume          PASS   412 rows last window (norm ~380–450)
Continuity      FAIL   missing bars for 2026-07-01

Verdict: STALE — no data for 2026-07-01.
Likely cause: the 05:00 sync cron didn't run or TWS wasn't up.
Check crontab + logs (hand off to /log-triage).
```

!!! tip "Make it recurring"
    Pairs naturally with `/loop` or a cron that runs `/healthcheck` and alerts on FAIL.

## Notes

- Distinguish "expected empty" (weekends, holidays, infrequent events) from "stale" so it doesn't cry wolf.
- Freshness needs the right timezone — convert UTC storage to the cadence's timezone before computing age.
- "Completed" is not "worked" — always check volume and freshness, not just a clean exit.
- Read-only — it verifies state; on a FAIL it points to `/log-triage` or `/cron`.
- Credentials come from the environment and are never printed — an auth failure names the variable, not its value.
