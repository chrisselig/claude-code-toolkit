---
name: lint-fix
description: Auto-detect the project linter (ruff, falling back to flake8) and fix all linting errors autonomously. Use when the user wants lint errors cleaned up across the codebase.
---

# Fix All Lint Errors

Autonomously fix all linting errors in the project.

## Steps

1. Detect the project's linter by checking for config files:
   - `ruff.toml` or `[tool.ruff]` in `pyproject.toml` → use `ruff check . --fix`
   - `setup.cfg` with `[flake8]` → use `flake8`
   - `.eslintrc*` → use `eslint --fix`
2. Run the test suite first to record the baseline — if tests already fail, note which, so later failures aren't misattributed to the lint fixes.
3. Run the linter and capture all errors.
4. For auto-fixable errors, apply fixes automatically.
5. For remaining errors, fix them manually by reading and editing the affected files.
   - Fix the underlying issue; never silence an error with `# noqa`, `# type: ignore`, or a config-level ignore unless it's a demonstrable false positive — and say so when you do.
   - Lint fixes must not change behavior. If a "fix" requires restructuring logic (e.g. an unused variable that reveals a real bug), flag it to the user instead of guessing.
6. Re-run the linter to verify zero errors.
7. Run the test suite again and compare to the step-2 baseline to ensure fixes didn't break anything.
8. If any step fails more than 3 times, stop and explain the root cause.
9. Report what was fixed, and separately anything suppressed or flagged.

Do NOT commit — let the user decide when to commit.
