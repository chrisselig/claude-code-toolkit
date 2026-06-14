# Test Coverage Report

Run tests with coverage and identify untested code.

## Steps

1. Run pytest with coverage: `pytest --cov=src --cov-report=term-missing -q`
   - If `pytest-cov` is not installed, suggest installing it.
2. Identify files with less than 80% coverage.
3. For each low-coverage file, show the uncovered line ranges.
4. Suggest which missing tests would have the highest impact (focus on business logic, not boilerplate).
5. Report: overall coverage %, files below 80%, total uncovered lines.
