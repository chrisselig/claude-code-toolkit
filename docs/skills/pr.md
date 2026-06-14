# PR Workflow

Automates the full pull request lifecycle: lint, test, branch, commit, push, and open a PR with a structured description. This is the most frequently used skill in the toolkit.

## How It Works

1. **Lint and test** -- Run the project's linter (`ruff check . --fix` or `flake8`) and test suite (`pytest --tb=short -q`). Fix any issues before proceeding.
2. **Review changes** -- Run `git status` and `git diff` to understand what will be committed.
3. **Create a branch** -- Use a conventional prefix: `feat/`, `fix/`, `docs/`, or `refactor/`.
4. **Stage files** -- Stage relevant files individually. Never stage `.env`, credentials, `__pycache__`, or large data files.
5. **Commit** -- Write a conventional commit message with a `Co-Authored-By` trailer.
6. **Push** -- Push the branch with the `-u` flag to set up tracking.
7. **Open the PR** -- Use `gh pr create` with a short title and a body containing a `## Summary` and `## Test plan`.
8. **Report** -- Return the PR URL to the user.

## Example Session

```bash
# Step 1: Lint
$ ruff check . --fix
Found 2 fixable errors. Fixed 2 errors.

# Step 2: Tests
$ pytest --tb=short -q
12 passed in 3.41s

# Step 3: Review changes
$ git status
On branch main
Changes not staged for commit:
  modified:   src/app/models.py
  modified:   src/app/views.py
  new file:   tests/test_views.py

# Step 4-5: Branch, stage, commit
$ git checkout -b feat/user-search
$ git add src/app/models.py src/app/views.py tests/test_views.py
$ git commit -m "feat: add user search endpoint with full-text filtering

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"

# Step 6-7: Push and create PR
$ git push -u origin feat/user-search
$ gh pr create --title "feat: add user search endpoint" --body "..."
```

## Commit Messages

!!! example "Good commit messages"
    ```
    feat: add user search with full-text filtering
    fix: prevent division by zero in portfolio calculation
    docs: add API authentication guide
    refactor: extract validation logic into shared module
    ```

!!! warning "Bad commit messages"
    ```
    update files
    fix stuff
    WIP
    changes
    feat: add user search endpoint with full-text filtering across all user fields including name, email, and department with pagination support
    ```

    The last example is too long. Keep the subject line under 70 characters and use the commit body for details.

## Handling Lint Failures

When the linter reports errors that cannot be auto-fixed, the skill follows this process:

1. Read the affected file and understand the error.
2. Apply the fix manually (e.g., add a missing type annotation, remove an unused import).
3. Re-run the linter to confirm zero errors remain.
4. If errors persist after 3 attempts, stop and explain the root cause to the user.

```python
# Before: ruff reports F841 (local variable assigned but never used)
def process(data):
    result = transform(data)  # F841: 'result' never used
    return data

# After: fix applied
def process(data):
    return transform(data)
```

## Staging Safety

!!! warning "Files that are never staged"
    The skill explicitly skips these files to prevent accidental exposure of secrets or unnecessary noise:

    - `.env` and `.env.*` files
    - `credentials.json`, `serviceAccountKey.json`
    - `__pycache__/` directories
    - `*.pyc` files
    - Large binary or data files

## Notes

- The PR body always includes a `## Summary` with bullet points and a `## Test plan` with a verification checklist.
- If the project has no linter configured, the lint step is skipped with a note to the user.
- The skill respects existing branch conventions defined in `CLAUDE.md`.
