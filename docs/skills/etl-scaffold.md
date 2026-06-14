# ETL Pipeline Scaffold

Create a standard Extract-Transform-Load pipeline with modular stages, Pydantic validation, idempotent loads, and structured logging. Supports multiple sources (API, CSV, Excel, web scrape) and destinations (DuckDB/MotherDuck, Turso, SQLite, Parquet, CSV).

## How It Works

1. **Gather requirements** -- Determine the data source, destination, transform logic, and schedule (one-off, daily cron, or event-triggered).
2. **Create the directory structure** -- Generate a standard project layout with separate modules for each ETL stage.
3. **Generate pipeline code** -- Write extract, transform, load, and orchestrator modules following best practices.
4. **Add scheduling** -- Create a cron script or entry point if the pipeline runs on a schedule.

## Directory Structure

```
project_name/
├── src/project_name/
│   ├── __init__.py
│   ├── extract.py       # Data source connectors
│   ├── transform.py     # Cleaning, validation, reshaping
│   ├── load.py          # Database/file writers
│   ├── pipeline.py      # Orchestrator: extract -> transform -> load
│   └── models.py        # Pydantic models for data validation
├── scripts/
│   └── run_pipeline.py  # CLI entry point
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── fixtures/        # Sample data for tests
├── data/                # Local data directory (gitignored)
├── .env.example
├── pyproject.toml
└── README.md
```

## Example Pipeline Code

### Pipeline Orchestration

!!! warning "Bad: monolithic script with no error handling or logging"
    ```python
    import pandas as pd
    df = pd.read_csv("data.csv")
    df = df.dropna()
    df.to_sql("table", conn)
    print("done")
    ```

!!! example "Good: modular, logged, validated, idempotent"
    ```python
    from datetime import date
    from pathlib import Path

    import polars as pl
    from loguru import logger
    from pydantic import BaseModel, field_validator


    class SalesRecord(BaseModel):
        date: date
        amount: float
        region: str

        @field_validator("amount")
        @classmethod
        def amount_positive(cls, v: float) -> float:
            if v < 0:
                raise ValueError(f"Negative amount: {v}")
            return v


    def extract(source_path: Path) -> pl.DataFrame:
        logger.info(f"Extracting from {source_path}")
        return pl.read_csv(source_path)


    def transform(df: pl.DataFrame) -> list[SalesRecord]:
        logger.info(f"Transforming {len(df)} rows")
        df = df.drop_nulls(subset=["date", "amount"])
        df = df.unique(subset=["date", "region"])
        return [SalesRecord(**row) for row in df.to_dicts()]


    def load(records: list[SalesRecord], db_url: str) -> int:
        logger.info(f"Loading {len(records)} records")
        # Upsert to handle reruns safely
        ...
        return len(records)


    def run_pipeline(source: Path, db_url: str) -> None:
        raw = extract(source)
        clean = transform(raw)
        n = load(clean, db_url)
        logger.info(f"Pipeline complete: {n} records loaded")
    ```

### Database Loading

!!! warning "Bad: appends duplicates on every run"
    ```python
    df.to_sql("sales", conn, if_exists="append")
    ```

!!! example "Good: upsert pattern for idempotent loads"
    ```python
    # DuckDB / MotherDuck
    conn.execute("""
        INSERT OR REPLACE INTO sales (date, region, amount)
        SELECT date, region, amount FROM staging_sales
    """)

    # SQLite / Turso
    conn.execute("""
        INSERT INTO sales (date, region, amount) VALUES (?, ?, ?)
        ON CONFLICT(date, region) DO UPDATE SET amount = excluded.amount
    """, params)
    ```

### Environment-Specific Destinations

!!! warning "Bad: hardcoded connection strings"
    ```python
    conn = duckdb.connect("md:my_database")
    ```

!!! example "Good: environment-driven, works locally and in production"
    ```python
    import os
    import duckdb

    DB_URL = os.environ.get("DATABASE_URL", "local.duckdb")

    if DB_URL.startswith("md:"):
        # MotherDuck -- needs MOTHERDUCK_TOKEN in env
        conn = duckdb.connect(DB_URL)
    else:
        conn = duckdb.connect(DB_URL)
    ```

## Key Principles

| Principle | Why It Matters |
|-----------|---------------|
| Validate between stages | Pydantic models catch bad data before it reaches the database |
| Idempotent loads | Pipelines can be safely rerun without creating duplicates |
| Log row counts at each stage | "Extracted 1,200 -> Transformed 1,180 -> Loaded 1,180" makes debugging trivial |
| Store raw data | Keep a copy of raw extracts (in a `raw/` directory or staging table) for debugging |
| Use polars over pandas | Faster execution, lower memory usage, better type safety |

## Notes

- The `data/` directory is always gitignored. Raw data stays local or in cloud storage.
- The `.env.example` file documents required environment variables without exposing secrets.
- Test fixtures in `tests/fixtures/` contain small sample datasets (5-10 rows) for unit tests.
- For scheduled pipelines, a `scripts/run_pipeline.py` CLI entry point is generated with argument parsing.
