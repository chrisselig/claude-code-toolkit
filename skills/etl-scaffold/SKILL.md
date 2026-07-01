---
name: etl-scaffold
description: Scaffold a standard Extract-Transform-Load pipeline project with extract/transform/load modules, Pydantic models, tests, and idempotent database loading. Use when starting a new data pipeline or ETL project.
---

# ETL Pipeline Scaffold

Create a standard Extract-Transform-Load pipeline for a data project.

## Steps

1. Ask the user for:
   - Data source(s): API, CSV, Excel, web scrape
   - Destination: MotherDuck, Turso, SQLite, Parquet, CSV
   - Transform requirements (cleaning, aggregation, joining)
   - Schedule: one-off, daily cron, triggered
2. Create the pipeline structure:

```
project_name/
├── src/project_name/
│   ├── __init__.py
│   ├── extract.py      # Data source connectors
│   ├── transform.py    # Cleaning, validation, reshaping
│   ├── load.py         # Database/file writers
│   ├── pipeline.py     # Orchestrator: extract → transform → load
│   └── models.py       # Pydantic models for data validation
├── scripts/
│   └── run_pipeline.py # CLI entry point
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── fixtures/       # Sample data for tests
├── data/               # Local data directory (gitignored)
├── .env.example
├── pyproject.toml
└── README.md
```

3. Generate the pipeline code following the patterns below.
4. Add a cron script if scheduled.

## Examples

### Pipeline orchestration

**BAD** — monolithic script, no error handling, no logging:
```python
import pandas as pd
df = pd.read_csv("data.csv")
df = df.dropna()
df.to_sql("table", conn)
print("done")
```

**GOOD** — modular, logged, validated, idempotent:
```python
from loguru import logger
from pydantic import BaseModel, field_validator

class SalesRecord(BaseModel):
    date: date
    amount: float
    region: str

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
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

def run_pipeline(source: Path, db_url: str):
    raw = extract(source)
    clean = transform(raw)
    n = load(clean, db_url)
    logger.info(f"Pipeline complete: {n} records loaded")
```

### Database loading

**BAD** — appends duplicates on every run:
```python
df.to_sql("sales", conn, if_exists="append")
```

**GOOD** — upsert pattern, idempotent:
```python
# DuckDB / MotherDuck
conn.execute("""
    INSERT OR REPLACE INTO sales (date, region, amount)
    SELECT date, region, amount FROM staging_sales
""")

# Turso / SQLite
conn.execute("""
    INSERT INTO sales (date, region, amount) VALUES (?, ?, ?)
    ON CONFLICT(date, region) DO UPDATE SET amount = excluded.amount
""", params)
```

### Environment-specific destinations

**BAD** — hardcoded connection strings:
```python
conn = duckdb.connect("md:my_database")
```

**GOOD** — environment-driven, local dev vs production:
```python
import os
import duckdb

DB_URL = os.environ.get("DATABASE_URL", "local.duckdb")  # local default

if DB_URL.startswith("md:"):
    # MotherDuck — needs MOTHERDUCK_TOKEN in env
    conn = duckdb.connect(DB_URL)
else:
    conn = duckdb.connect(DB_URL)
```

## Notes

- Always validate data with Pydantic models between extract and load
- Make pipelines idempotent — safe to rerun without creating duplicates
- Use polars over pandas for transform steps (faster, less memory)
- Log row counts at each stage: extracted N → transformed M → loaded M
- Store raw data before transforms for debugging (raw/ directory or staging table)
