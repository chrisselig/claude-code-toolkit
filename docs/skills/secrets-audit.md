# Secrets Audit

Audit a repository for exposed secrets — hardcoded tokens, committed `.env` files, credentials in git history — and check `.gitignore` and `.env.example` hygiene.

Trigger: `/secrets-audit`

## How It Works

1. **Redaction rule first** — every finding is reported as file, line, and variable name plus a fingerprint (first 4 characters + length). The full secret value never appears in output, so the audit can't become the leak.
2. **Ignore hygiene** — `.gitignore` must cover `.env`, `.streamlit/secrets.toml`, `*.pem`, `*.key`, `credentials*.json`; missing entries are listed.
3. **Tracked files** — `git ls-files` is checked for secret-holding files, because `.gitignore` doesn't help if the file was added before the rule existed.
4. **Working-tree scan** — `gitleaks`/`trufflehog` when installed, otherwise grep patterns for assignments, known token prefixes (`ghp_`, `sk-`, `AKIA`, JWTs), and URLs with embedded credentials — with placeholders filtered out.
5. **History scan** — the whole log, not just HEAD: a secret deleted in a later commit is still in every clone. Huge repos get a bounded scan, stated honestly in the report.
6. **`.env.example` check** — example files must hold placeholders only.
7. **Severity-ranked report** — LEAKED (pushed: rotate now), committed-but-unpushed (scrub via [Git Rescue](git-rescue.md)), hardcoded in the tree, and hygiene gaps — ending in a one-line verdict: CLEAN / HYGIENE GAPS / LEAKED.
8. **Stop after reporting** — rotation, history rewrites, and `.gitignore` edits happen only when the user asks.

## Redacted Reporting

!!! warning "Bad: the audit becomes the leak"
    ```
    Found MOTHERDUCK_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIi... in scripts/sync.py:12
    ```
    The full token is now in the conversation, the terminal scrollback, and any transcript that captures them.

!!! example "Good: location and fingerprint, never the value"
    ```
    LEAKED  scripts/sync.py:12  MOTHERDUCK_TOKEN hardcoded (eyJh…, 180 chars, JWT shape)
            In history since a1b2c3d (2026-05-14), pushed to origin → rotate now.
    ```

## Verdict Honesty

!!! warning "Bad: green because the tip is clean"
    ```
    No secrets found in the codebase ✓
    ```
    The scan only looked at HEAD; the token deleted in last week's "remove key" commit is still in history and in every clone.

!!! example "Good: history included, gaps named"
    ```
    Verdict: LEAKED (1) + HYGIENE GAPS (2)
    - MOTHERDUCK_TOKEN in commits a1b2c3d..f4e5d6a, pushed → rotate now, then /git-rescue to scrub.
    - trades.db tracked by git → add to .gitignore, git rm --cached trades.db
    - .env.example line 3 holds a real-looking key (sk-p…, 51 chars) → replace with a placeholder
    ```

## Notes

- **Rotation beats deletion, always.** A secret that touched a pushed commit, a log file, or a pasted terminal is compromised no matter how thoroughly it's scrubbed. Every LEAKED finding says "rotate" before anything about cleanup.
- The skill never opens `.env` or `secrets.toml` to "verify" contents — presence checks and pattern scans are enough; reading a secrets file pulls the values into the conversation.
- Read-only by design: no `git filter-repo`, no `.gitignore` edits, no rotation. History surgery is [Git Rescue](git-rescue.md)'s job.
- Natural habit points: before [Deploy Streamlit](deploy-streamlit.md) pushes a repo, before flipping a repo public in [New Project](new-project.md), and after a Git Rescue secret cleanup.
