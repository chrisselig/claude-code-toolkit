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
2. Run the linter and capture all errors.
3. For auto-fixable errors, apply fixes automatically.
4. For remaining errors, fix them manually by reading and editing the affected files.
5. Re-run the linter to verify zero errors.
6. Run the test suite to ensure fixes didn't break anything.
7. If any step fails more than 3 times, stop and explain the root cause.
8. Report what was fixed.

Do NOT commit — let the user decide when to commit.
