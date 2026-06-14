# /test

Run the project's test suite, report results, and diagnose any failures.

## What It Does

1. Detects the test framework:
    - `pytest.ini`, `pyproject.toml` with `[tool.pytest]`, or a `tests/` directory indicates pytest
    - `package.json` with a test script indicates npm/vitest/jest
2. Runs the full test suite with verbose output
3. If tests fail:
    - Shows failing test names and error messages
    - Reads the failing test files and the source code under test
    - Diagnoses the root cause
    - Suggests or applies fixes
4. Reports totals: passed, failed, skipped, and duration

## Example

```
/test
```

Typical output for a passing suite:

```
Test Results (pytest)
=====================
47 passed, 0 failed, 3 skipped in 12.4s
```

Typical output when a test fails:

```
Test Results (pytest)
=====================
46 passed, 1 failed, 3 skipped in 13.1s

FAILED: tests/unit/test_risk.py::test_max_position_size
-------------------------------------------------------
AssertionError: assert 150000 <= 100000

Diagnosis:
  The test expects max position size of 100,000 units, but
  RiskManager.validate() now returns 150,000 after commit a5845a5
  changed the default leverage from 10:1 to 15:1.

  Root cause: config/settings.yaml was updated but the test
  fixture still uses the old default.

Suggested fix:
  Update the fixture in tests/conftest.py to set leverage=15
  or adjust the assertion to match the new default.
```

!!! example "Auto-fix mode"
    When a failure diagnosis is straightforward (e.g., an outdated assertion or a missing import), the command can apply the fix directly and re-run the tests to confirm.

## Notes

- Unit tests are run by default; integration tests (marked `@pytest.mark.integration`) are skipped unless the user requests them
- The command never hits real external services -- it relies on the project's existing mocks
- For Python projects, the command uses the project's configured interpreter, not system Python
