---
name: secrets-audit
description: Audit a repository for exposed secrets — hardcoded tokens, committed .env files, credentials in git history — and check .gitignore and .env.example hygiene. Read-only; findings are reported with redacted values and rotation guidance. Use when checking a repo for leaked credentials, before making a repo public or deploying, or after a suspected secret exposure.
argument-hint: "[path (defaults to current repo)]"
---

# Secrets Audit

Find credentials that are exposed — in the working tree, in tracked files, or in git history — and report them **without ever printing a secret**. Read-only: this skill never edits files, rewrites history, or rotates anything; it says exactly what to rotate and hands off cleanup.

## Steps

1. **Set the redaction rule before scanning.** Every matched value is reported as file, line number, and variable name, plus a fingerprint only (first 4 characters + length, e.g. `ghp_… (40 chars)`). Never paste a full candidate secret into output, a report file, or a commit message — the audit must not become the leak.

2. **Check ignore hygiene.** Verify `.gitignore` covers the secret-holding files this stack uses: `.env` and `.env.*` (except `.env.example`), `.streamlit/secrets.toml`, `*.pem`, `*.key`, `credentials*.json`, `.netrc`. Report exactly which entries are missing.

3. **Check what git actually tracks** — `.gitignore` doesn't help if the file was added before the rule existed:
   - `git ls-files | grep -iE '\.env$|secrets\.toml|\.pem$|\.key$|credential'`
   - Any hit is a finding even if the file "looks empty" now; `git log --oneline -- <file>` shows how long it has been tracked.

4. **Scan the working tree for hardcoded secrets.** Prefer a real scanner if installed (`gitleaks detect` or `trufflehog filesystem .`); otherwise grep for the usual shapes, excluding `.git/`, lockfiles, and `.env.example`:
   - Assignments: `(api_?key|secret|token|password|passwd)\s*[:=]\s*['"][^'"]{8,}`
   - Known prefixes: `ghp_`, `github_pat_`, `sk-`, `xoxb-`, `AKIA`, `eyJ` (JWT)
   - URLs with embedded credentials: `[a-z]+://[^/\s:]+:[^@\s]+@` and `authToken=` query params
   Filter out obvious placeholders (`your-key-here`, `changeme`, `<TOKEN>`, `${VAR}`, `os.environ[...]` reads) so the report isn't noise.

5. **Scan git history, not just the tip** — a secret deleted in a later commit is still in every clone:
   - `gitleaks detect --log-opts="--all"` if available; otherwise `git log --all --diff-filter=A --name-only` for secret-named files, and `git grep <pattern>` over recent history for the highest-signal patterns.
   - If the repo is huge, bound the scan (e.g. the last 200 commits) and say so in the report — a bounded scan reported honestly beats an unbounded one that never finishes.

6. **Check `.env.example`** (and any `*.sample`/`*.example` config) contains placeholders only — a real value pasted into an example file is the most commonly missed leak.

7. **Report findings by severity, redacted**, ending with a one-line verdict (CLEAN / HYGIENE GAPS / LEAKED):
   - **Leaked** — in history on a pushed branch: the credential is burned. Name it and tell the user to **rotate it now**; cleanup is secondary. If the repo is public, assume it was scraped within minutes.
   - **Committed locally** — in history but never pushed: strip it (`git filter-repo`, or amend if it's the last commit) — hand off to `/git-rescue`.
   - **Hardcoded in the working tree** — move to `.env`/an env var before the next commit.
   - **Hygiene gaps** — missing `.gitignore` entries or real-looking values in `.env.example`: list the exact lines to add or change.

8. **Stop after reporting.** Rotation, history rewrites, and `.gitignore` edits happen only when the user asks — rotating invalidates a credential other systems may be using, and history rewrites need coordination.

## Examples

### Reporting a finding

**BAD** — the audit becomes the leak:
```
Found MOTHERDUCK_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIi... in scripts/sync.py:12
```
The full token is now in the conversation, the terminal scrollback, and any transcript or log that captures them.

**GOOD** — location and fingerprint, never the value:
```
LEAKED  scripts/sync.py:12  MOTHERDUCK_TOKEN hardcoded (eyJh…, 180 chars, JWT shape)
        In history since a1b2c3d (2026-05-14), pushed to origin → rotate now.
```

### Verdict honesty

**BAD** — green because the tip is clean:
```
No secrets found in the codebase ✓
```
The scan only looked at HEAD; the token deleted in last week's "remove key" commit is still in history and in every clone.

**GOOD** — history included, gaps named:
```
Verdict: LEAKED (1) + HYGIENE GAPS (2)
- MOTHERDUCK_TOKEN in commits a1b2c3d..f4e5d6a, pushed → rotate now, then /git-rescue to scrub.
- trades.db tracked by git → add to .gitignore, git rm --cached trades.db
- .env.example line 3 holds a real-looking key (sk-p…, 51 chars) → replace with a placeholder
```

## Notes

- **Rotation beats deletion, always.** A secret that touched a pushed commit, a log file, or a pasted terminal is compromised no matter how thoroughly it is scrubbed afterwards. Every LEAKED finding says "rotate" before it says anything about cleanup.
- Never open `.env` or `secrets.toml` to "verify" their contents — presence checks (`test -f`, `git ls-files`) and pattern scans are enough. Reading a secrets file pulls the values into the conversation, which is itself a leak.
- Read-only by design: no `git filter-repo`, no `.gitignore` edits, no rotation from this skill. History surgery is `/git-rescue`'s job.
- Grep patterns have false positives (test fixtures, docs, hashes). Check the surrounding lines and mark uncertain hits "review manually" instead of crying LEAKED at a fixture.
- `gitleaks`/`trufflehog` beat grep on both recall and precision — prefer them when installed and fall back to the patterns above.
- Natural habit points: before `/deploy-streamlit` pushes a repo, before flipping a repo public in `/new-project`, and after a `/git-rescue` secret cleanup to confirm nothing else is exposed.
