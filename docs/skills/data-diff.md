# Data Diff

Compare two datasets — tables, files, or a table before/after a pipeline change — and report schema differences, row-count deltas, key-level mismatches, and per-column drift. The regression test for data work: run it after a transform refactor, a migration, or a reload.

Trigger: `/data-diff`

## How It Works

1. **Identify the two sides and the key** — file vs file, table vs table, or before/after the same table (snapshotting the "before" if a re-run will overwrite it). A row key like `(pair, timestamp)` enables row-level diffing; without one, only aggregates can be compared.
2. **Schema diff first** — missing columns and type mismatches usually explain everything downstream.
3. **Row counts** — total and per partition (per day, per category) so a localized loss doesn't vanish into the total.
4. **Key-level diff** — keys only in A, only in B, and keys in both with differing values (`EXCEPT` both ways, or a `FULL OUTER JOIN`). Duplicate keys are reported as a finding before joining.
5. **Column drift** — differing-row counts per column and numeric stats per side, within an agreed float tolerance.
6. **Samples and verdict** — a few real mismatched rows, then IDENTICAL / IDENTICAL within tolerance / DIFFERENT with exact numbers and a list of what was ignored.

## Keyed Diff, Not Frame Equality

!!! warning "Bad: one boolean, no diagnosis"
    ```python
    assert df_old.equals(df_new)   # False. Which rows? Which columns? Why?
    ```
    Also fails on row order, dtype, and float noise that may be perfectly fine.

!!! example "Good: keyed, directional, tolerant (DuckDB)"
    ```sql
    WITH a AS (SELECT * FROM 'before.parquet'),
         b AS (SELECT * FROM trades)
    SELECT
      (SELECT count(*) FROM a) AS rows_a,
      (SELECT count(*) FROM b) AS rows_b,
      (SELECT count(*) FROM (SELECT pair, ts FROM a
                             EXCEPT SELECT pair, ts FROM b)) AS keys_only_in_a,
      (SELECT count(*) FROM (SELECT pair, ts FROM b
                             EXCEPT SELECT pair, ts FROM a)) AS keys_only_in_b,
      (SELECT count(*) FROM a JOIN b USING (pair, ts)
        WHERE abs(a.close - b.close) > 1e-9) AS close_mismatches;
    ```

## Example Report

```
Diff: before.parquet vs trades (key: pair, ts | float tol 1e-9 | ignored: loaded_at)
Schema:  identical (12 columns)
Rows:    1,204,331 vs 1,204,317  (14 fewer in B)
Keys:    14 only in A — all pair=USDJPY, date 2023-06-14 | 0 only in B
Values:  0 mismatches within tolerance
Verdict: DIFFERENT — B is missing USDJPY 2023-06-14 (14 rows); all else identical.
Next: re-run /backfill for that date, then re-diff.
```

## Notes

- Read-only on both sides; the skill never modifies either dataset.
- Row order is not a difference — diff by key, never by position.
- Tolerance is agreed up front (float epsilon, ignored columns, timezone handling) and everything ignored is listed in the report.
- DuckDB is the default engine because it reads Parquet, CSV, SQLite, and MotherDuck in one session; big tables are aggregated in-database rather than in pandas.
- Pairs with [Migrate](migrate.md) (verify a table rebuild), [Backfill](backfill.md) (verify a re-run), and [ETL Scaffold](etl-scaffold.md) (regression-check a transform refactor).
- Connection credentials for both sides come from environment variables and never appear in output or the final report.
