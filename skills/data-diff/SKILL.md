---
name: data-diff
description: Compare two datasets — tables, files, or a table before/after a pipeline change — and report schema differences, row-count deltas, key-level mismatches, and per-column drift. Use when validating that a refactor, migration, or reload didn't change the data unexpectedly.
argument-hint: "[dataset A] [dataset B] [key columns]"
---

# Data Diff

Answer "is the data still the same?" with evidence instead of a gut check. The natural tool is DuckDB, which reads Parquet, CSV, SQLite, and MotherDuck side by side in one session.

## Steps

1. Identify from the user's request:
   - The two sides: file vs file, table vs table, or the same table before/after a change. If the "before" is about to be overwritten by a re-run, **snapshot it first** (`COPY table TO 'before.parquet'`).
   - The **key column(s)** that identify a row (e.g. `(pair, timestamp)`). Without a key, only aggregate comparisons are possible — say so explicitly.
   - The tolerance: exact match, a float epsilon, and columns to ignore (load timestamps, surrogate ids).

2. **Diff the schemas first**: columns present on only one side, and type mismatches. A schema change usually explains everything downstream — report it before row-level noise.

3. **Compare row counts**: totals per side, and per natural partition (per day, per pair/category) so a localized loss is visible instead of vanishing into the total.

4. **Key-level diff** (needs the key):
   - Keys only in A, keys only in B, and keys in both whose values differ.
   - Use `EXCEPT` in both directions for exact diffs, or a `FULL OUTER JOIN` on the key for value comparison.
   - Duplicate keys on either side are a finding in their own right — report them before joining, since they corrupt the join.

5. **Column-level drift** for keys present in both: which columns differ and by how much (count of differing rows per column; min/max/mean per side for numerics), applying the agreed float tolerance so representation noise doesn't drown real changes.

6. **Show samples**: a handful of actual mismatched rows side by side — enough to diagnose the cause, not a dump.

7. **Report a verdict**: IDENTICAL / IDENTICAL within tolerance / DIFFERENT, with the numbers. Never round "14 rows differ" up to "basically the same" — state exactly what differs, what was ignored, and let the user judge.

## Examples

### Keyed diff vs whole-frame equality

**BAD** — one boolean, no diagnosis:
```python
assert df_old.equals(df_new)   # False. Which rows? Which columns? Why?
```
Also fails on row order, dtype, and float noise that may be perfectly fine.

**GOOD** — keyed, directional, tolerant:
```sql
-- DuckDB: parquet snapshot vs live table, keyed on (pair, ts)
WITH a AS (SELECT * FROM 'before.parquet'),
     b AS (SELECT * FROM trades)
SELECT
  (SELECT count(*) FROM a)                                        AS rows_a,
  (SELECT count(*) FROM b)                                        AS rows_b,
  (SELECT count(*) FROM (SELECT pair, ts FROM a
                         EXCEPT SELECT pair, ts FROM b))          AS keys_only_in_a,
  (SELECT count(*) FROM (SELECT pair, ts FROM b
                         EXCEPT SELECT pair, ts FROM a))          AS keys_only_in_b,
  (SELECT count(*) FROM a JOIN b USING (pair, ts)
    WHERE abs(a.close - b.close) > 1e-9)                          AS close_mismatches;
```

### Honest verdicts

**BAD** — a reassuring summary that hides the finding:
```
Data matches. ✓
```
(14 rows were missing; they were "small" so they got waved through.)

**GOOD** — exact, scoped, and actionable:
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

- Read-only on both sides — this skill never modifies either dataset.
- Row order is not a difference. Never diff by position; diff by key.
- Common false positives to settle up front: float representation, timezone-naive vs -aware timestamps, TEXT vs INTEGER coercion across engines, trailing whitespace, and NULL vs empty string. List whatever was ignored in the final report.
- Big tables: run counts and aggregates in the database, not pandas; pull only the mismatch samples into memory.
- Pairs naturally with `/migrate` (verify a table rebuild copied everything), `/backfill` (verify a re-run reproduced the load), and `/etl-scaffold` (regression-check a transform refactor).
