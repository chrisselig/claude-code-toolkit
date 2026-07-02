---
name: test
description: Run the project's test suite, diagnose failures, and fix them. Use when the user wants to run tests or fix failing tests.
argument-hint: "[optional test path or -k filter]"
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
4. Re-run after fixing to confirm green. If the same test still fails after ~3 fix attempts, stop and explain what's blocking instead of thrashing.
5. Report: total tests, passed, failed, skipped, duration.

## Notes

- Fix the **code**, not the test — unless the test itself is demonstrably wrong (and say so when it is). Never delete tests, loosen assertions, or add skip/xfail markers just to get to green.
- If no test framework is detected, report that and stop; don't invent a test setup unasked.
- A skipped test count that suddenly jumped is a finding, not a pass — mention it.
