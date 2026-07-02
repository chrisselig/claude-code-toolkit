---
name: healthcheck
description: Verify a scheduled pipeline or sync actually landed — check row counts, data freshness, and database reachability against expectations. Use when the user wants to confirm a cron job succeeded, check data freshness, or sanity-check that a database is up to date.
argument-hint: "[db/table to check] [expected cadence]"
---

# Healthcheck

Confirm that an unattended job did what it was supposed to. Answers the question "did last night's run actually work?" without needing to watch it live.

## Steps

1. Identify what to check from the user's request or the project config: which database/table (Turso, DuckDB/MotherDuck, SQLite), and the expected cadence (hourly, daily, per-event).

2. **Reachability.** Connect to the database. If the connection fails (expired token, wrong URL, network), stop and report that first — nothing else matters if the DB is down.

3. **Freshness.** Query the latest timestamp in the target table and compare to now:
   - Compute the age of the newest row.
   - Compare against the expected cadence plus a grace margin (e.g. a daily job's newest row should be < ~25h old).
   - Account for weekends/holidays for market data — no new forex bars on Sunday is healthy, not stale.

4. **Volume.** Compare recent row counts to the recent norm. A sync that ran but wrote 0 rows, or 10x the usual, is a problem even though it "completed".

5. **Continuity.** Check for gaps in the expected sequence (missing days/hours) over the recent window, not just at the tail.

6. **Report a verdict per check** with the actual numbers:

   | Check | Status | Detail |
   |-------|--------|--------|
   | DB reachable | PASS/FAIL | connection + latency |
   | Freshness | PASS/FAIL | newest row age vs expected |
   | Volume | PASS/FAIL | rows last period vs norm |
   | Continuity | PASS/FAIL | missing periods, if any |

   End with a one-line overall verdict and, on any FAIL, the most likely cause and fix.

## Example

```
Healthcheck: Turso `trading` — trades + bars
================================================
DB reachable    PASS   connected in 180ms
Freshness       FAIL   newest bar 2026-06-30 21:00 UTC (age 38h; expected < 25h)
Volume          PASS   412 rows in last sync window (norm ~380–450)
Continuity      FAIL   missing bars for 2026-07-01 (all hours)

Verdict: STALE — no data for 2026-07-01.
Likely cause: the 05:00 sync cron didn't run or TWS wasn't up.
Check: `crontab -l` for sync_to_turso.py, and logs/ for a 2026-07-01 run
(hand off to /log-triage).
```

## Notes

- Distinguish "expected empty" from "stale". Weekends, holidays, and events that only fire a few times a year produce legitimate gaps — encode that so the check doesn't cry wolf.
- Freshness needs the right timezone. If the table stores UTC but the cadence is reasoned in MT, convert before computing age or the verdict will be off by hours.
- "The job completed" is not "the job worked". Always check volume and freshness, not just that a process exited 0.
- Read-only. This verifies state; it does not fix it. On a FAIL, point to the next step: `/log-triage` for the run's logs, `/cron` to inspect the schedule.
- Good as a recurring check — pairs naturally with `/loop` or a cron that runs this and alerts on FAIL.
