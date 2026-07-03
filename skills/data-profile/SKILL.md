---
name: data-profile
description: Generate a data quality report for a CSV, Parquet, Excel, JSON file, or database table (SQLite, DuckDB/MotherDuck, Turso). Reports nulls, duplicates, outliers, type mismatches, and cardinality. Use when inspecting data quality before a load or when the user wants to profile a dataset.
argument-hint: "[file path or db table]"
---

# Data Profile

Generate a quick data quality report for a CSV, Parquet, Excel file, or database table.

## Steps

1. Identify the data source from the user's request:
   - File path (CSV, Parquet, Excel, JSON)
   - Database table (SQLite, DuckDB/MotherDuck, Turso)
2. Load the data into a pandas or polars DataFrame. For databases, use the appropriate connector.
3. Generate a profile report covering:
   - **Shape**: rows × columns
   - **Column types**: dtype for each column
   - **Nulls**: count and percentage per column, flag columns >5% null
   - **Duplicates**: duplicate row count, duplicate key columns if obvious
   - **Numeric columns**: min, max, mean, median, std, percentiles (1st, 25th, 75th, 99th), outlier count (>3σ)
   - **Categorical columns**: unique count, top 5 values with frequencies, high-cardinality flag (>100 unique)
   - **Date columns**: min/max date, gaps, timezone info
   - **Sample**: first 5 rows
4. Flag data quality issues:
   - Columns that are entirely null
   - Columns with a single unique value (constant)
   - Suspicious patterns (negative values in quantity fields, future dates in historical data)
   - Mixed types in a column
5. Present as a clean markdown summary.
6. Suggest cleanup steps if issues are found.

## Examples

### Loading data

**BAD** — loading everything into memory without checking size:
```python
df = pd.read_csv("huge_file.csv")  # 10GB file, crashes
```

**GOOD** — check size first, use appropriate tool:
```python
import os
size_mb = os.path.getsize("huge_file.csv") / 1e6
if size_mb > 100:
    import polars as pl
    lf = pl.scan_csv("huge_file.csv")           # lazy — nothing loaded yet
    profile = lf.describe()                      # aggregate lazily…
    sample = lf.head(5).collect()                # …and collect only small results
else:
    df = pd.read_csv("huge_file.csv")
```
Note `scan_csv` returns a `LazyFrame` — run aggregations on it and `.collect()` only the small outputs; calling DataFrame methods on it directly fails.

### Profiling output

**BAD** — raw df.describe() dump with no context:
```
       col1    col2
count  1000    998
mean   45.2    NaN
```

**GOOD** — structured report with quality flags:
```markdown
## Profile: sales_data.csv (1,000 rows × 8 cols)

| Column | Type | Nulls | Unique | Min | Max | Issues |
|--------|------|-------|--------|-----|-----|--------|
| date | datetime | 0 (0%) | 365 | 2024-01-01 | 2024-12-31 | |
| amount | float64 | 2 (0.2%) | 847 | -50.0 | 9999.0 | ⚠ 3 negative values |
| region | object | 0 (0%) | 4 | — | — | |
| notes | object | 982 (98%) | 12 | — | — | ⚠ mostly null |
```

## Notes

- Prefer polars over pandas for large files (>100MB)
- For database tables, profile with SQL aggregates (`COUNT`, `MIN`, `MAX`, `GROUP BY`) or a `LIMIT`ed sample rather than `SELECT *` into memory — a remote Turso/MotherDuck table can be far larger than it looks
- For database tables, show the CREATE TABLE schema alongside the profile
- Never modify the source data — this is read-only profiling
- If a column looks like PII (emails, names, account numbers), keep it out of the printed sample rows and top-values list — report its stats only
- Database credentials come from the environment — never print a connection string that embeds a token, and on a failed connection name the env var that looks wrong, not its value
