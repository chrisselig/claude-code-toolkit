---
name: status
description: Report git status, recent commits, open PRs, and lint/test health in one summary. Use when the user wants a quick overview of the project's current state.
---

# Project Status

Give a quick status report on the current state of the project.

## Steps

1. Run `git status` to show uncommitted changes.
2. Run `git log --oneline -10` to show recent commits.
3. Run `git branch -a` to show all branches.
4. Check for open PRs: `gh pr list --state open` — if `gh` is missing or unauthenticated, skip and note it rather than failing the whole report.
5. Check for failing CI: `gh run list --limit 5`
6. Run the linter (ruff/flake8/eslint) in check-only mode and report the error count. Do not auto-fix anything — status is read-only.
7. Run the test suite quietly (`pytest -q --tb=no`) and report pass/fail count. If the suite is slow (>~2 min) or absent, skip it and say so instead of stalling the summary.
8. Present a concise summary: branch, uncommitted changes, open PRs, test/lint health. Mark any skipped checks explicitly so silence isn't mistaken for health.
