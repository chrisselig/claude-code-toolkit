# /status

Quick status report on the current state of the project, covering version control, CI health, and code quality.

## What It Does

1. Runs `git status` to show uncommitted changes
2. Runs `git log --oneline -10` for recent commit history
3. Lists all branches with `git branch -a`
4. Checks for open pull requests via `gh pr list`
5. Checks recent CI runs via `gh run list`
6. Runs the project linter (ruff, flake8, or eslint) and reports error count
7. Runs the test suite and reports pass/fail count
8. Presents a concise summary

## Example

```
/status
```

Typical output:

```
Project Status
==============

Branch:       feat/add-notifications
Uncommitted:  2 modified, 1 untracked

Recent Commits (last 5):
  a5845a5  feat: add Telegram notifier module
  c32728e  fix: correct timezone handling in scheduler
  abed99c  docs: update API reference
  1ae01a5  refactor: extract risk validation
  402ce0a  test: add unit tests for circuit breaker

Open PRs: 1
  #42  feat: add Telegram notifications  (feat/add-notifications -> main)

CI:  Last 3 runs PASSED

Lint:  0 errors (ruff)
Tests: 47 passed, 0 failed, 3 skipped (12.4s)
```

!!! tip "First thing in the morning"
    Run `/status` at the start of a session to orient yourself: see what branch you are on, whether CI is green, and if any PRs need attention.

## Notes

- Requires `gh` (GitHub CLI) to be authenticated for PR and CI checks
- Auto-detects the linter: checks for ruff, flake8, or eslint in order
- Auto-detects the test runner: pytest, unittest, npm test, or vitest
- If the repo has no remote or `gh` is not installed, those steps are skipped gracefully
