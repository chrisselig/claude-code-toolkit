# /coverage

Run tests with code coverage enabled and identify untested areas of the codebase.

## What It Does

1. Detects the coverage target (configured `[tool.coverage]` value, `src/` layout, or the package directory) — it does not blindly assume `src`
2. Runs `pytest --cov=<target> --cov-report=term-missing -q`
3. Identifies files with less than 80% coverage
4. For each low-coverage file, shows the uncovered line ranges
5. Suggests which missing tests would have the highest impact, focusing on business logic rather than boilerplate
6. Reports overall coverage percentage, files below threshold, and total uncovered lines

## Example

```
/coverage
```

Typical output:

```
Coverage Report
===============
Overall: 74% (target: 80%)

Files below 80%:
  src/broker/client.py          62%  (missing: 88-103, 145-162, 201-215)
  src/execution/engine.py       71%  (missing: 54-67, 130-138)
  src/risk/circuit_breaker.py   58%  (missing: 42-78, 95-110)

Files at 100%:
  src/calendar/event_store.py
  src/data/models.py
  src/strategy/straddle.py

High-impact test suggestions:
  1. Test CircuitBreaker.check() with HALTED state  (covers 36 lines)
  2. Test IBClient reconnection path                 (covers 30 lines)
  3. Test ExecutionEngine order rejection flow        (covers 13 lines)
```

!!! warning "Missing pytest-cov"
    If `pytest-cov` is not installed in the current environment, the command will detect this and suggest installing it before proceeding.

!!! tip "Focus on business logic"
    The suggestions prioritize untested business logic (risk checks, order flow, strategy decisions) over configuration parsing or boilerplate, since those are where bugs cause real damage.

## Notes

- The default coverage source is `src/`; this adapts to whatever the project uses
- Coverage is measured on the unit test suite only (integration tests are excluded by default)
- Line ranges in the report correspond to `--cov-report=term-missing` output
- The 80% threshold is a guideline, not a hard rule -- some modules (e.g., CLI entry points) naturally have lower coverage
