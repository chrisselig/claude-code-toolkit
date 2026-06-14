# Data Profile

Generate a data quality report for any tabular data source: CSV, Parquet, Excel, JSON, or a database table (SQLite, DuckDB/MotherDuck, Turso). The report surfaces nulls, duplicates, outliers, type mismatches, and other quality issues without modifying the source data.

## How It Works

1. **Identify the source** -- Determine whether the input is a file path or a database table.
2. **Load the data** -- Use pandas for small files (<100 MB) or polars for larger files. For databases, use the appropriate connector.
3. **Generate the profile** -- Compute statistics for every column:
    - Shape (rows x columns)
    - Column data types
    - Null counts and percentages (flagged if >5%)
    - Duplicate row counts
    - Numeric stats: min, max, mean, median, std, percentiles (1st, 25th, 75th, 99th), outlier count (>3 sigma)
    - Categorical stats: unique count, top 5 values with frequencies, high-cardinality flag (>100 unique)
    - Date columns: min/max date, gap detection, timezone info
4. **Flag quality issues** -- Identify columns that are entirely null, constant, contain mixed types, or have suspicious patterns (negative quantities, future dates in historical data).
5. **Present the report** -- Output a clean markdown summary with a table and issue flags.
6. **Suggest fixes** -- Recommend cleanup steps for each issue found.

## Example Output

Given a file `sales_data.csv` with 10,000 rows:

```markdown
## Profile: sales_data.csv (10,000 rows x 8 cols)

| Column      | Type     | Nulls       | Unique | Min        | Max        | Issues                  |
|-------------|----------|-------------|--------|------------|------------|-------------------------|
| order_id    | int64    | 0 (0.0%)   | 10,000 | 1          | 10,000     |                         |
| date        | datetime | 0 (0.0%)   | 731    | 2022-01-01 | 2023-12-31 |                         |
| customer_id | int64    | 0 (0.0%)   | 4,218  | 1001       | 9999       |                         |
| amount      | float64  | 12 (0.1%)  | 8,493  | -125.50    | 48,999.00  | 7 negative values       |
| region      | object   | 0 (0.0%)   | 4      | --         | --         |                         |
| channel     | object   | 0 (0.0%)   | 1      | --         | --         | constant (all "online") |
| notes       | object   | 9,814 (98%)| 86     | --         | --         | mostly null             |
| score       | mixed    | 0 (0.0%)   | 47     | --         | --         | mixed types (int+str)   |

### Quality Issues
1. **amount**: 7 rows with negative values -- verify if these are refunds or errors.
2. **channel**: constant column ("online") -- consider dropping.
3. **notes**: 98% null -- low information value.
4. **score**: mixed types detected (integers and strings) -- standardize to one type.
```

## Data Loading

!!! warning "Bad: loading without checking file size"
    ```python
    df = pd.read_csv("huge_file.csv")  # 10 GB file, OOM crash
    ```

!!! example "Good: size-aware loading"
    ```python
    import os
    size_mb = os.path.getsize("huge_file.csv") / 1e6
    if size_mb > 100:
        import polars as pl
        df = pl.scan_csv("huge_file.csv")  # lazy evaluation
    else:
        df = pd.read_csv("huge_file.csv")
    ```

## Data Validation Patterns

!!! warning "Bad: raw `df.describe()` dump with no context"
    ```
           col1    col2
    count  1000    998
    mean   45.2    NaN
    ```

!!! example "Good: structured report with actionable flags"
    Each column gets its own row in the summary table, with an `Issues` column that highlights problems requiring attention. Numeric columns include outlier counts. Categorical columns flag high cardinality.

## Quality Checks Performed

| Check | Condition | Flag |
|-------|-----------|------|
| Nulls | >5% of rows | Column flagged with null percentage |
| Duplicates | Duplicate rows exist | Row count and suggested key columns |
| Outliers | Values beyond 3 standard deviations | Count of outlier values |
| Constants | Only 1 unique value | "constant" flag |
| Mixed types | Multiple dtypes in a column | "mixed types" flag |
| All null | 100% null | "entirely null" flag |
| High cardinality | >100 unique values in a string column | "high cardinality" flag |
| Negative values | Negative numbers in quantity/amount fields | Count of negatives |

## Notes

- This skill is strictly read-only. It never modifies the source data.
- For database tables, the `CREATE TABLE` schema is shown alongside the profile.
- Polars is preferred over pandas for files over 100 MB due to lower memory usage and faster execution.
- The first 5 rows are always included as a sample to help the user orient.
