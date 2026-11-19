---
name: pii-audit
description: Audit a repository and its data files for exposed personally identifiable information — real names, SSNs/SINs, emails, phone numbers, addresses, DOB, or payment card numbers in tracked data files, code, logs, or fixtures. Read-only; findings are reported with type and fingerprint, never the real value. Use when checking a data pipeline or dashboard repo for PII exposure, before sharing a dataset externally, before deploying a dashboard that queries real customer/HR/financial data, or after onboarding a new data source.
argument-hint: "[path (defaults to current repo)]"
---

# PII Audit

Find personally identifiable information that shouldn't be where it is — committed in a data file, hardcoded in a fixture, or printed to logs — and report it **without ever printing the real value**. Read-only: this skill never edits, masks, deletes, or anonymizes data; it says exactly what's exposed and hands off remediation.

## Steps

1. **Set the redaction rule before scanning.** Every match is reported as file, line (or column name + row count for data files), and PII type, plus a masked sample (e.g. `***-**-1234`, `j***@***.com`, `(***) ***-4471`). Never paste a real name, number, or address into output, a report file, or a commit message — the audit must not become the leak.

2. **Enumerate what counts as PII for this scan**: SSN (`\d{3}-\d{2}-\d{4}`), Canadian SIN (`\d{3}[\s-]?\d{3}[\s-]?\d{3}`), email addresses in data/fixture files (not `.env`/config, which is [Secrets Audit](../secrets-audit/SKILL.md)'s job), phone numbers, street addresses, dates of birth, credit card numbers (Luhn-valid 13–19 digit runs), and full names paired with any of the above in the same row/record — a name alone is low-signal, a name next to a SIN is not.

3. **Check column/field names first** — cheapest, highest-signal pass. Grep schema definitions, CSV/Parquet headers, SQL `CREATE TABLE`, and Pydantic/dataclass field names for `ssn|sin|dob|birth|email|phone|address|credit_card|card_number|first_name|last_name|full_name`. A column named `ssn` is a finding regardless of what's actually in it.

4. **Scan tracked data files for real values**, sampling rather than dumping: for each CSV/Parquet/Excel/SQLite/DuckDB file tracked by git (`git ls-files | grep -iE '\.(csv|parquet|xlsx?|db|duckdb|sqlite)$'`), read a small sample of rows and run the patterns from step 2 against them. Report "column X, N of M sampled rows match SSN shape" — not the matched values themselves.

5. **Scan code and notebooks for PII in logs or hardcoded fixtures**: `print(`/`logging.`/`st.write(`/`f"..."` statements that interpolate a PII-named column or variable (risk: PII lands in log aggregators or Streamlit/Shiny session state visible to other users), and test fixtures or seed scripts with real-looking names/numbers instead of synthetic ones (`faker`, `factory_boy` placeholders are fine; a literal `"123-45-6789"` in a test file is not).

6. **Scan git history, not just the tip** — a data file deleted in a later commit is still in every clone: `git log --all --diff-filter=A --name-only` for data-file paths matching step 4's extensions, bounded to the last 200 commits on huge repos (state the bound honestly in the report).

7. **Check for missing controls** rather than just exposure: does the pipeline mask/hash/pseudonymize PII columns before they reach a dashboard, export, or third-party API call? Is there a `.gitignore` entry for the raw-data directory this project uses? No controls isn't itself a leak, but it's a finding — "HR analytics joins on raw SIN with no hashing step" is worth reporting even if the file isn't tracked yet.

8. **Report findings by severity, redacted**, ending with a one-line verdict (CLEAN / HYGIENE GAPS / EXPOSED):
   - **Exposed in history or working tree, pushed** — real PII in a commit on a pushed branch: the data is burned for the people in it. Name the file and row count, and say so plainly — rotation doesn't apply to a person's SIN, so this needs a disclosure/legal conversation, not just a code fix.
   - **Exposed, local only** — tracked but never pushed: untrack and purge via [Git Rescue](../git-rescue/SKILL.md).
   - **Hardcoded fixture/test data** — replace with synthetic data (`faker`) before the next commit.
   - **Hygiene gaps** — missing masking/hashing step, missing `.gitignore` entry for a raw-data directory, PII interpolated into a log statement.

9. **Stop after reporting.** Masking, hashing, deletion, and history rewrites happen only when the user asks — removing a person's data from a system others may already query needs coordination, not a unilateral edit.

## Examples

### Reporting a finding

**BAD** — the audit becomes the leak:
```
Row 14 of customers.csv has SSN 123-45-6789 for Jane Doe.
```
A real SSN and name are now in the conversation, the terminal scrollback, and any transcript that captures them.

**GOOD** — type, location, and masked sample, never the real value:
```
EXPOSED  data/customers.csv  column "ssn": 212 of 212 sampled rows match SSN shape (***-**-6789 pattern)
         Tracked since 4f2a1bc (2026-03-02), pushed to origin → this is real customer PII in every clone.
```

### Verdict honesty

**BAD** — green because no obviously-named file was checked:
```
No PII found ✓
```
The scan only grepped filenames for "customer" or "pii"; `export_2026_q1.csv` with the same columns was never opened.

**GOOD** — scope and gaps stated:
```
Verdict: EXPOSED (1) + HYGIENE GAPS (2)
- data/customers.csv column "ssn" → real SIN-shaped values, pushed → untrack + /git-rescue, then a disclosure conversation.
- etl/transform.py:41 logs the full "email" column via logging.info() → strip from the log statement.
- benefits_finder/raw/ has no .gitignore entry → add it before the next real-data drop.
```

## Notes

- **A person's PII isn't a secret you rotate.** Once a SIN or DOB tied to a real person is in a pushed commit, deleting it later doesn't undo the exposure — every EXPOSED finding says so plainly instead of implying cleanup fixes it.
- Never print a full matched value to "confirm" a hit — masked samples and row/column counts are enough. Printing the real value pulls it into the conversation, which is itself a leak.
- Read-only by design: no file edits, no masking, no git history rewrites. History surgery is [Git Rescue](../git-rescue/SKILL.md)'s job; data-quality (not privacy) issues are [Data Profile](../data-profile/SKILL.md)'s job.
- Column-name matches can be false positives (`email_template.html`, a `name` column on a non-personal entity). Check what the column actually holds before calling it a finding.
- This skill covers PII *in data*; credentials and API tokens are [Secrets Audit](../secrets-audit/SKILL.md)'s scope — run both when onboarding a new data source.
- Natural habit points: before sharing a dataset or export outside the team, before `/deploy-streamlit` or `/deploy-web-app` ships a dashboard over real data, and after onboarding any new data source into an ETL pipeline.
