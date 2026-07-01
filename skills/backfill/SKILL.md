---
name: backfill
description: Load historical data for a date range into a database or file store idempotently and resumably, detecting and filling gaps without creating duplicates. Use when the user needs to backfill history, re-download missing dates, or fill holes in a time-series (e.g. Dukascopy bars, API history).
---

# Historical Backfill

Fill a data store with historical records over a date range, safely restartable and gap-aware. Generalizes the Dukascopy download pattern to any source (API, files, ticks/bars).

## Steps

1. Identify from the user's request:
   - Source (API endpoint, Dukascopy, file dump) and entity (pair, symbol, dataset).
   - Date range and granularity (1-min bars, daily, hourly).
   - Destination (Parquet partitions, DuckDB/MotherDuck, Turso, SQLite).

2. **Detect what's already present before downloading anything.** Query the destination for the min/max timestamp and, more importantly, the *gaps* — missing days inside the existing range, not just the ends. Only fetch what is missing.

3. **Chunk the work** by a natural period (per day or per week). Small chunks make the job resumable and keep memory bounded.

4. **Fetch each missing chunk** with retries and backoff. Respect the source's rate limits. On a transient failure, retry; on a persistent failure, log the chunk and continue — never let one bad day abort the whole backfill.

5. **Write idempotently.** Use upsert / `INSERT OR REPLACE` / partition-overwrite keyed on (entity, timestamp) so re-running a chunk never duplicates rows. For Parquet, write one file per partition and overwrite that partition.

6. **Verify after each chunk:** expected vs actual row count, and no unexpected gap remains. Log `entity date: N rows` per chunk.

7. **Report a coverage summary:** requested range, chunks fetched, chunks skipped (already present), chunks failed (with dates), and any remaining gaps. Do not claim full coverage if chunks failed — say exactly which dates are still missing.

## Examples

### Gap detection vs blind re-download

**BAD** — re-downloading the whole range every run:
```python
for day in date_range(start, end):
    rows = fetch(pair, day)
    db.insert(rows)   # duplicates everything already there; wastes the API budget
```

**GOOD** — fetch only the missing days, upsert:
```python
have = set(db.query("SELECT DISTINCT date FROM bars WHERE pair = ?", pair))
missing = [d for d in date_range(start, end) if d not in have and is_trading_day(d)]
logger.info(f"{pair}: {len(missing)} missing of {len(list(date_range(start,end)))} days")
for day in missing:
    rows = fetch_with_retry(pair, day)
    db.execute("INSERT OR REPLACE INTO bars ...", rows)   # idempotent
    logger.info(f"{pair} {day}: {len(rows)} rows")
```

### Honest coverage reporting

**BAD** — silent partial success:
```
Backfill complete.
```
Three days failed and were skipped, but the user now believes the data is whole.

**GOOD** — explicit gaps:
```
Backfill USDJPY 1-min 2023-01-01 → 2023-12-31
Fetched: 248 days | Skipped (already present): 9 | Failed: 2
Still missing: 2023-06-14, 2023-11-03 (source returned 503 after 5 retries)
Re-run to retry the failed days.
```

## Notes

- Weekends and market holidays are legitimately empty for forex — don't flag them as gaps. Use a trading-calendar check so real holes stand out from expected ones.
- Idempotency is the whole point: a backfill you can't safely re-run is a liability. Key every write on (entity, timestamp).
- Store the source's raw response before transforming when feasible — re-transforming from local raw is far cheaper than re-hitting the API.
- Rate limits: prefer a small concurrency with backoff over hammering the source. A backfill that gets you IP-banned is slower than a polite one.
- For very large ranges, Parquet partitioned by `entity/year/month` is cheaper to gap-check and overwrite than a single monolithic table.
- After a backfill for the trading bot, the natural next step is `/mc-analysis` (now that the history exists) — mention it if the context fits.
