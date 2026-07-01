---
name: test
description: Run the project's test suite, diagnose failures, and fix them. Use when the user wants to run tests or fix failing tests.
---

# Run Tests

Run the project's test suite and report results.

## Steps

1. Detect the test framework:
   - `pytest.ini`, `pyproject.toml [tool.pytest]`, or `tests/` dir → pytest
   - `package.json` with test script → npm/vitest/jest
2. Run the full test suite with verbose output.
3. If tests fail:
   - Show the failing test names and error messages
   - Read the failing test files and the source code they test
   - Diagnose the root cause
   - Suggest or apply fixes
4. Report: total tests, passed, failed, skipped, duration.
