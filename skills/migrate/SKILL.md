---
name: migrate
description: Create and apply versioned, idempotent schema migrations for SQLite, Turso/libSQL, or DuckDB/MotherDuck, with matching up/down scripts. Use when the user needs to add a column, change a table, or evolve a database schema safely across environments.
argument-hint: "[schema change description] [target db]"
---

# Database Migration

Evolve a database schema through small, ordered, reversible migration files instead of ad-hoc `ALTER TABLE` in a REPL. Works for SQLite, Turso/libSQL, and DuckDB/MotherDuck.

## Steps

1. Identify the change and the target database from the user's request (add/drop/rename column, new table, index, backfill a value).

2. **Inspect current state first.** Read the live schema (`.schema` / `PRAGMA table_info` / `DESCRIBE`) and check the migrations directory for the latest applied version. Never write a migration blind.

3. **Create a migrations directory if absent:** `migrations/` with zero-padded, timestamped, ordered files:
   ```
   migrations/
   ├── 0001_create_trades.sql
   ├── 0002_add_event_column.sql
   └── _applied.sql        # or a schema_migrations table tracking version + applied_at
   ```

4. **Write the migration with both directions.** Every file has an `-- Up` and a `-- Down` section. Use idempotency guards (`IF EXISTS` / `IF NOT EXISTS`) so a partial or repeated run does not crash.

5. **Track applied versions.** Maintain a `schema_migrations(version TEXT PRIMARY KEY, applied_at TIMESTAMP)` table. Before applying, check it; after applying, insert the version. This makes migrations idempotent across dev/prod.

6. **Back up before applying.** For file databases, copy the file (`cp trades.db trades.db.bak-<date>`); for Turso, `turso db shell <db> .dump > backup.sql`; for MotherDuck, `EXPORT DATABASE` or at minimum a `CREATE TABLE ... AS SELECT` copy of the affected tables. A down migration protects against a *wrong* migration, not a *botched* one.

7. **Apply inside a transaction** where the engine supports DDL transactions (SQLite/libSQL do; DuckDB largely does). If anything fails, roll back so the schema is never left half-migrated.

8. **Handle NOT NULL on existing tables in the safe order:** add the column as nullable (or with a default) -> backfill values -> then add the constraint. Adding `NOT NULL` with no default to a populated table fails.

9. Report what changed, the new version number, and how to roll back.

## Examples

### A safe, reversible migration

**BAD** — irreversible, non-idempotent, unsafe on a populated table:
```sql
ALTER TABLE trades ADD COLUMN event TEXT NOT NULL;
```
No default -> fails if `trades` has rows. No `IF NOT EXISTS` -> rerun crashes. No down migration -> no way back.

**GOOD** — guarded, reversible, ordered:
```sql
-- 0002_add_event_column.sql

-- Up
ALTER TABLE trades ADD COLUMN event TEXT;          -- nullable first
UPDATE trades SET event = 'UNKNOWN' WHERE event IS NULL;   -- backfill
-- (SQLite can't add NOT NULL after the fact without a table rebuild;
--  enforce it in the app/Pydantic layer, or rebuild the table if required.)

-- Down
ALTER TABLE trades DROP COLUMN event;
```

### Engine differences

**BAD** — assuming one dialect everywhere:
```sql
ALTER TABLE trades ALTER COLUMN pips SET DATA TYPE DOUBLE;  -- not valid in SQLite
```

**GOOD** — dialect-aware:
```
DuckDB/MotherDuck: ALTER TABLE trades ALTER pips TYPE DOUBLE;
SQLite/Turso:      no ALTER TYPE — create new table, copy, swap, drop old.
```

## Notes

- SQLite/libSQL have limited `ALTER TABLE`: no drop/alter-type of a column in old versions. For those, use the rebuild pattern (create new table with desired schema, `INSERT ... SELECT`, drop old, rename). Newer SQLite (3.35+) supports `DROP COLUMN`.
- Always test the migration against a copy of the real database before running it on production/MotherDuck.
- Keep migrations small and single-purpose — one logical change per file. Easier to review, easier to roll back.
- MotherDuck: migrations run against the cloud database; confirm you are pointed at the right `md:` database and not a local file.
- Commit the migration files. They are the versioned history of the schema and must travel with the code.
- If the change needs a data backfill from an external source (not just a constant), that is a job for the `/backfill` skill, not a DDL migration.
