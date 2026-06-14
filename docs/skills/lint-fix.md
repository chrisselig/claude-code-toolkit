# Lint Fix

Automatically detect the project's linter, fix all errors, and verify that the test suite still passes. This skill handles both auto-fixable and manual-fix-required errors without committing changes.

## How It Works

1. **Detect the linter** -- Check for configuration files to determine which linter the project uses:
    - `ruff.toml` or `[tool.ruff]` in `pyproject.toml` -- use `ruff check . --fix`
    - `setup.cfg` with `[flake8]` section -- use `flake8`
    - `.eslintrc*` files -- use `eslint --fix`
2. **Run the linter** -- Execute the linter and capture all errors.
3. **Auto-fix** -- Apply automatic fixes for errors the linter can resolve on its own.
4. **Manual fix** -- For remaining errors, read the affected files and apply fixes by hand.
5. **Re-run** -- Run the linter again to verify zero errors remain.
6. **Test** -- Run the test suite to confirm that fixes did not introduce regressions.
7. **Bail out** -- If any step fails more than 3 times, stop and explain the root cause.
8. **Report** -- Summarize what was fixed. Do not commit.

## Linter Detection

The skill checks configuration files in this priority order:

| File / Section | Linter | Fix Command |
|----------------|--------|-------------|
| `ruff.toml` | ruff | `ruff check . --fix` |
| `pyproject.toml` `[tool.ruff]` | ruff | `ruff check . --fix` |
| `setup.cfg` `[flake8]` | flake8 | `flake8` (no auto-fix) |
| `.eslintrc.json` / `.eslintrc.js` | ESLint | `eslint --fix .` |

!!! tip "Ruff is preferred"
    Ruff can auto-fix most errors and runs significantly faster than flake8 or pylint. If no linter is configured, the skill suggests adding `[tool.ruff]` to `pyproject.toml`.

## Example Fix Output

```
$ ruff check . --fix
src/app/views.py:12:1: F401 [*] `os` imported but unused
src/app/views.py:45:5: F841 [*] Local variable `tmp` is assigned but never used
src/app/models.py:8:1: I001 [*] Import block is unsorted
Found 3 errors (3 fixed, 0 remaining)

$ ruff check .
All checks passed!

$ pytest --tb=short -q
24 passed in 4.12s
```

## Handling Unfixable Errors

Some errors cannot be auto-fixed and require manual intervention:

```python
# E501: Line too long (ruff can't auto-fix without changing logic)
# Before
result = some_function(argument_one, argument_two, argument_three, argument_four, argument_five)

# After: manual line break
result = some_function(
    argument_one,
    argument_two,
    argument_three,
    argument_four,
    argument_five,
)
```

```python
# F811: Redefinition of unused name
# Before
def process(data):
    ...

def process(data):  # F811: redefined
    ...

# After: rename or remove the duplicate
def process(data):
    ...

def process_batch(data):
    ...
```

!!! warning "When fixes break tests"
    If removing an "unused" import causes an `ImportError` at runtime (e.g., the import has side effects or is used by a framework), the skill restores the import and adds a `# noqa: F401` comment instead.

    ```python
    from celery import shared_task  # noqa: F401  -- used by Celery autodiscover
    ```

## Common Error Categories

| Code | Description | Auto-fixable |
|------|-------------|--------------|
| F401 | Unused import | Yes |
| F841 | Unused variable | Yes |
| I001 | Unsorted imports | Yes |
| E501 | Line too long | No (requires manual reformatting) |
| F811 | Redefined name | No (requires judgment) |
| E711 | Comparison to None | Yes (`== None` to `is None`) |

## Notes

- The skill never commits changes. The user decides when and how to commit after reviewing the fixes.
- If no linter is configured, the skill suggests adding ruff configuration to `pyproject.toml` before proceeding.
- Flake8 has no built-in auto-fix capability. When flake8 is detected, all fixes are applied manually.
- The 3-attempt limit prevents infinite loops on errors that resist automated fixes.
