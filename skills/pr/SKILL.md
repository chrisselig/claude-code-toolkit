---
name: pr
description: Run the full pull-request workflow — lint, test, create a feature branch if needed, commit with conventional-commit messages, push, and open a PR. Use when the user wants to ship changes as a pull request.
---

# Create PR

## Steps

1. Run the project's linter and test suite to verify clean state. Common patterns:
   - `ruff check . --fix` or `flake8` for Python linting
   - `pytest --tb=short -q` for Python tests
   - Fix any issues before proceeding. If the same failure persists after ~3 fix attempts, stop and report it rather than looping.
   - If the repo has no linter or tests, note that and continue — don't invent them here.
2. Review all uncommitted changes with `git status` and `git diff`. If there is nothing to commit and the branch has no commits ahead of the base, stop — don't open an empty PR.
3. Check the current branch:
   - On `main`/`master` → create a descriptive branch with a conventional prefix: `feat/`, `fix/`, `docs/`, `refactor/`.
   - Already on a feature branch → stay on it unless the changes clearly belong elsewhere.
4. Stage relevant files explicitly (never stage `.env`, credentials, `__pycache__`, or large data files). Prefer naming files over `git add -A`, and scan the staged diff for anything that looks like a secret before committing.
5. Commit with a conventional commit message (feat/fix/docs/refactor prefix, concise summary, Co-Authored-By trailer).
6. Push the branch with `-u` flag. Never push directly to the default branch.
7. Create PR with `gh pr create` using a short title (<70 chars) and a body with:
   - `## Summary` — bullet points of what changed and why
   - `## Test plan` — checklist of how to verify
8. Report the PR URL to the user.

## Notes

- If `gh` is not authenticated (`gh auth status` fails), stop after pushing and give the user the compare URL instead of erroring out mid-flow.
- Do not merge the PR — opening it is the end of this skill unless the user asks.
- If push is rejected because the remote diverged, fetch and rebase the feature branch; never force-push without asking.
