---
name: db-schema
description: Inspect, compare, or diff database schemas for SQLite, DuckDB/MotherDuck, or Turso. Use when the user wants to see a table's structure or compare schemas across databases.
argument-hint: "[db path/url] [table]"
---

# Database Schema

Inspect, compare, or generate database schemas.

## Steps

1. Detect the database type from the user's request or project files:
   - SQLite (`.db`, `.sqlite`): `sqlite3 db.sqlite ".schema"`
   - DuckDB/MotherDuck (`.duckdb`, `md:`): `duckdb -c "SHOW TABLES; DESCRIBE table_name;"`
   - Turso: Use `turso db shell` or the libsql Python client
   - SQLAlchemy: Read model definitions from `models.py`
2. Show all tables with their columns, types, primary keys, foreign keys, and indexes.
3. If comparing two databases (e.g., local vs production):
   - Diff the schemas side by side
   - Flag: missing tables, missing columns, type mismatches, missing indexes
4. If generating a migration:
   - Show the ALTER TABLE statements needed to sync
   - Warn about destructive changes (column drops, type changes)
   - Do **not** apply them here — hand off to the `/migrate` skill, which versions and applies migrations safely.

This command is strictly read-only: open SQLite/DuckDB files with read-only flags where supported, and never execute DDL or DML while inspecting. If a connection fails (missing file, expired Turso token), report the cause and stop rather than guessing at the schema.

**BAD** — raw SQL dump with no context:
```
CREATE TABLE t1 (id INTEGER, name TEXT, ...50 more lines...);
```

**GOOD** — structured summary:
```markdown
## Tables (3)

### users (1,234 rows)
| Column | Type | Nullable | Key | Default |
|--------|------|----------|-----|---------|
| id | INTEGER | NO | PK | autoincrement |
| email | TEXT | NO | UQ | — |
| created_at | TIMESTAMP | NO | — | CURRENT_TIMESTAMP |
```
