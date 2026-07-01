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
4. Check for open PRs: `gh pr list --state open`
5. Check for failing CI: `gh run list --limit 5`
6. Run the linter (ruff/flake8/eslint) and report error count.
7. Run the test suite and report pass/fail count.
8. Present a concise summary: branch, uncommitted changes, open PRs, test/lint health.
