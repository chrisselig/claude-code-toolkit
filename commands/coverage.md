---
name: coverage
description: Run the test suite with coverage and highlight untested code. Use when the user wants a coverage report or to find gaps in test coverage.
argument-hint: "[optional test path or package to measure]"
---

# Test Coverage Report

Run tests with coverage and identify untested code.

## Steps

1. Determine the coverage target — don't assume `src`:
   - `[tool.coverage]` or `--cov` in `pyproject.toml`/`setup.cfg` → use the configured value.
   - `src/<package>/` layout → `--cov=src`.
   - Flat layout → `--cov=<package_dir>`.
2. Run pytest with coverage: `pytest --cov=<target> --cov-report=term-missing -q`
   - If `pytest-cov` is not installed, suggest installing it and stop.
   - If no tests are collected, report that and stop — 0% of nothing is not a coverage report.
   - If tests fail, still report coverage but flag that failing tests make the numbers unreliable.
3. Identify files with less than 80% coverage. Ignore virtualenvs, migrations, and generated code.
4. For each low-coverage file, show the uncovered line ranges.
5. Suggest which missing tests would have the highest impact (focus on business logic, not boilerplate).
6. Report: overall coverage %, files below 80%, total uncovered lines.

Read-only: this reports coverage; it does not write tests or modify code.
