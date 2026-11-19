# PII Audit

Audit a repository and its data files for exposed personally identifiable information — real names, SSNs/SINs, emails, phone numbers, addresses, DOB, or payment card numbers in tracked data files, code, logs, or fixtures.

Trigger: `/pii-audit`

## How It Works

1. **Redaction rule first** — every finding is reported as file, line (or column + row count), and PII type, plus a masked sample (`***-**-1234`, `j***@***.com`). The real value never appears in output.
2. **PII types enumerated** — SSN, Canadian SIN, email, phone, address, DOB, credit card (Luhn-valid), and full names paired with any of those in the same record.
3. **Column/field names checked first** — schema definitions, CSV/Parquet headers, `CREATE TABLE`, and Pydantic/dataclass fields for PII-shaped names, cheapest and highest-signal pass.
4. **Tracked data files sampled** — CSV/Parquet/Excel/SQLite/DuckDB files tracked by git get a row sample checked against the PII patterns; reported as match counts, never matched values.
5. **Code and notebooks scanned** for PII interpolated into log/print statements, and fixtures/seed scripts with real-looking data instead of synthetic (`faker`) data.
6. **History scan** — data files deleted in a later commit are still in every clone; huge repos get a bounded scan, stated honestly.
7. **Missing controls flagged** — no masking/hashing step before a dashboard or export, no `.gitignore` entry for a raw-data directory.
8. **Severity-ranked report** — EXPOSED (pushed: a disclosure conversation, not just a code fix), exposed-local-only (scrub via [Git Rescue](git-rescue.md)), hardcoded fixtures, and hygiene gaps — ending in a one-line verdict: CLEAN / HYGIENE GAPS / EXPOSED.
9. **Stop after reporting** — masking, hashing, deletion, and history rewrites happen only when the user asks.

## Redacted Reporting

!!! warning "Bad: the audit becomes the leak"
    ```
    Row 14 of customers.csv has SSN 123-45-6789 for Jane Doe.
    ```
    A real SSN and name are now in the conversation, the terminal scrollback, and any transcript that captures them.

!!! example "Good: type, location, and masked sample, never the real value"
    ```
    EXPOSED  data/customers.csv  column "ssn": 212 of 212 sampled rows match SSN shape (***-**-6789 pattern)
             Tracked since 4f2a1bc (2026-03-02), pushed to origin → real customer PII in every clone.
    ```

## Verdict Honesty

!!! warning "Bad: green because no obviously-named file was checked"
    ```
    No PII found ✓
    ```
    The scan only grepped filenames for "customer" or "pii"; a differently-named export with the same columns was never opened.

!!! example "Good: scope and gaps stated"
    ```
    Verdict: EXPOSED (1) + HYGIENE GAPS (2)
    - data/customers.csv column "ssn" → real SIN-shaped values, pushed → untrack + /git-rescue, then a disclosure conversation.
    - etl/transform.py:41 logs the full "email" column via logging.info() → strip from the log statement.
    - benefits_finder/raw/ has no .gitignore entry → add it before the next real-data drop.
    ```

## Notes

- **A person's PII isn't a secret you rotate.** Once a SIN or DOB tied to a real person is pushed, deleting it later doesn't undo the exposure — findings say so plainly.
- Never print a full matched value to confirm a hit — masked samples and counts are enough.
- Read-only by design: no edits, no masking, no history rewrites. History surgery is [Git Rescue](git-rescue.md)'s job; data-quality issues are [Data Profile](data-profile.md)'s job.
- Column-name matches can be false positives — check what the column actually holds before calling it a finding.
- Covers PII *in data*; credentials and API tokens are [Secrets Audit](secrets-audit.md)'s scope — run both when onboarding a new data source.
- Natural habit points: before sharing a dataset externally, before [Deploy Streamlit](deploy-streamlit.md) or [Deploy Web App](deploy-web-app.md) ships a dashboard over real data, and after onboarding any new data source.
