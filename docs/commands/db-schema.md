# /db-schema

Inspect, compare, or document database schemas for SQLite, DuckDB, Turso, and SQLAlchemy-based projects.

## What It Does

1. Detects the database type from the project or user request:
    - **SQLite** (`.db`, `.sqlite`): uses `sqlite3 ... ".schema"`
    - **DuckDB/MotherDuck** (`.duckdb`, `md:`): uses `duckdb -c "SHOW TABLES; DESCRIBE ...;"`
    - **Turso**: uses `turso db shell` or the libsql Python client
    - **SQLAlchemy**: reads model definitions from Python source files
2. Shows all tables with columns, types, primary keys, foreign keys, and indexes
3. If comparing two databases (e.g., local vs. production):
    - Diffs schemas side by side
    - Flags missing tables, missing columns, type mismatches, and missing indexes
4. If generating a migration, shows the `ALTER TABLE` statements needed

## Example

```
/db-schema
```

Typical output for a SQLite database:

```markdown
## Tables (3)

### trades (847 rows)
| Column     | Type      | Nullable | Key | Default          |
|------------|-----------|----------|-----|------------------|
| id         | INTEGER   | NO       | PK  | autoincrement    |
| pair       | TEXT      | NO       |     | --               |
| direction  | TEXT      | NO       |     | --               |
| entry_px   | REAL      | NO       |     | --               |
| exit_px    | REAL      | YES      |     | --               |
| pnl        | REAL      | YES      |     | --               |
| opened_at  | TIMESTAMP | NO       |     | CURRENT_TIMESTAMP|
| closed_at  | TIMESTAMP | YES      |     | --               |

### events (1,203 rows)
| Column     | Type      | Nullable | Key | Default          |
|------------|-----------|----------|-----|------------------|
| id         | INTEGER   | NO       | PK  | autoincrement    |
| name       | TEXT      | NO       |     | --               |
| scheduled  | TIMESTAMP | NO       | IDX | --               |
| impact     | TEXT      | NO       |     | --               |

### signals (412 rows)
...
```

!!! tip "Schema diffing"
    When comparing two databases, the output highlights differences clearly: added tables in green, removed columns flagged with warnings, and type mismatches called out explicitly.

!!! warning "Destructive migrations"
    When generating migration statements, the command warns before suggesting any `DROP COLUMN` or type-change operations, since these can cause data loss.

## Notes

- For SQLAlchemy projects, the command reads the Python model definitions directly rather than connecting to a live database
- Row counts are approximate for large tables (uses SQLite `max(rowid)` or equivalent)
- The command does not execute migrations; it only generates and displays the SQL
