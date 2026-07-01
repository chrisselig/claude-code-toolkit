# Migrate

Evolve a database schema through small, ordered, reversible migration files instead of ad-hoc `ALTER TABLE` in a REPL. Works for SQLite, Turso/libSQL, and DuckDB/MotherDuck.

Trigger: `/migrate`

## How It Works

1. **Identify the change** and target database (add/drop/rename column, new table, index, backfill).
2. **Inspect current state** — read the live schema and the latest applied migration version. Never write a migration blind.
3. **Ordered files** — zero-padded, timestamped `migrations/NNNN_description.sql`, each with `-- Up` and `-- Down`.
4. **Track applied versions** in a `schema_migrations(version, applied_at)` table so migrations are idempotent across dev/prod.
5. **Apply in a transaction** where the engine supports DDL transactions; roll back on failure so the schema is never half-migrated.
6. **NOT NULL on populated tables** — add nullable, backfill, then constrain.

## Reversible, Idempotent Migrations

!!! warning "Bad: irreversible, unsafe on a populated table"
    ```sql
    ALTER TABLE trades ADD COLUMN event TEXT NOT NULL;
    ```
    No default fails on existing rows; no guard breaks reruns; no down migration.

!!! example "Good: guarded and reversible"
    ```sql
    -- Up
    ALTER TABLE trades ADD COLUMN event TEXT;             -- nullable first
    UPDATE trades SET event = 'UNKNOWN' WHERE event IS NULL;

    -- Down
    ALTER TABLE trades DROP COLUMN event;
    ```

## Engine Differences

| Operation | DuckDB/MotherDuck | SQLite/Turso |
|-----------|-------------------|--------------|
| Add column | `ALTER TABLE ... ADD` | `ALTER TABLE ... ADD` |
| Change type | `ALTER ... TYPE` | rebuild table (copy/swap) |
| Drop column | supported | 3.35+ only, else rebuild |

## Notes

- Test every migration against a copy of the real database before production/MotherDuck.
- Keep migrations small and single-purpose — one logical change per file.
- Commit migration files; they are the versioned history of the schema.
- External-source data backfills belong to [Backfill](backfill.md), not a DDL migration.
