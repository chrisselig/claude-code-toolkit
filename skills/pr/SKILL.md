---
name: pr
description: Run the full pull-request workflow — lint, test, create a feature branch if needed, commit with conventional-commit messages, push, and open a PR. Use when the user wants to ship changes as a pull request.
---

# Create PR

## Steps

1. Run the project's linter and test suite to verify clean state. Common patterns:
   - `ruff check . --fix` or `flake8` for Python linting
   - `pytest --tb=short -q` for Python tests
   - Fix any issues before proceeding.
2. Review all uncommitted changes with `git status` and `git diff`.
3. Create a descriptive branch name using conventional prefixes: `feat/`, `fix/`, `docs/`, `refactor/`.
4. Stage relevant files (never stage `.env`, credentials, `__pycache__`, or large data files).
5. Commit with a conventional commit message (feat/fix/docs/refactor prefix, concise summary, Co-Authored-By trailer).
6. Push the branch with `-u` flag.
7. Create PR with `gh pr create` using a short title (<70 chars) and a body with:
   - `## Summary` — bullet points of what changed and why
   - `## Test plan` — checklist of how to verify
8. Report the PR URL to the user.
