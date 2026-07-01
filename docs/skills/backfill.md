# Backfill

Fill a data store with historical records over a date range, safely restartable and gap-aware. Generalizes the Dukascopy download pattern to any source — API, files, ticks or bars.

Trigger: `/backfill`

## How It Works

1. **Identify** source, entity, date range, granularity, and destination.
2. **Detect what's present** — query the destination for existing coverage and the *gaps inside* the range, not just the ends. Only fetch what is missing.
3. **Chunk** by day or week so the job is resumable and memory-bounded.
4. **Fetch with retries and backoff**, respecting rate limits. Log and skip a persistently failing chunk rather than aborting the whole run.
5. **Write idempotently** — upsert / `INSERT OR REPLACE` / partition-overwrite keyed on (entity, timestamp).
6. **Verify per chunk** and report honest coverage: fetched, skipped, failed, and any gaps remaining.

## Gap-Aware, Idempotent

!!! warning "Bad: re-download the whole range every run"
    ```python
    for day in date_range(start, end):
        db.insert(fetch(pair, day))   # duplicates everything, wastes the API budget
    ```

!!! example "Good: fetch only missing days, upsert"
    ```python
    have = set(db.query("SELECT DISTINCT date FROM bars WHERE pair = ?", pair))
    missing = [d for d in date_range(start, end) if d not in have and is_trading_day(d)]
    for day in missing:
        db.execute("INSERT OR REPLACE INTO bars ...", fetch_with_retry(pair, day))
    ```

## Honest Coverage Reporting

!!! example "Report exactly what's still missing"
    ```
    Backfill USDJPY 1-min 2023 — Fetched 248 | Skipped 9 | Failed 2
    Still missing: 2023-06-14, 2023-11-03 (source 503 after 5 retries)
    ```

## Notes

- Weekends and market holidays are legitimately empty for forex — use a trading calendar so real holes stand out.
- Idempotency is the point: key every write on (entity, timestamp) so re-runs never duplicate.
- Store raw responses when feasible — re-transforming locally beats re-hitting the API.
- After backfilling the trading bot's history, the natural next step is [MC Analysis](mc-analysis.md).
