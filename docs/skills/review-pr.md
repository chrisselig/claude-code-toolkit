# Review PR

Thoroughly review a pull request by examining the diff, checking CI status, running tests locally, and providing structured feedback. Can optionally post the review directly to GitHub.

## How It Works

1. **Get PR details** -- Fetch the title, description, changed files, additions, deletions, and commit list using `gh pr view`.
2. **Read the diff** -- Examine all code changes with `gh pr diff`.
3. **Check CI** -- Verify whether CI checks passed with `gh pr checks`.
4. **Review the code** -- Evaluate changes against six criteria (see below).
5. **Run tests locally** -- Check out the branch with `gh pr checkout` and run the test suite.
6. **Provide feedback** -- Summarize findings with an overall assessment and specific line-level comments.
7. **Post the review** -- Optionally submit the review to GitHub with `gh pr review`.

## Review Criteria

| Criterion | What to Check |
|-----------|---------------|
| Correctness | Does the logic do what the PR title and description claim? |
| Tests | Are new features and bug fixes covered by tests? |
| Security | Any hardcoded secrets, SQL injection, XSS, or command injection? |
| Style | Does the code follow project conventions from `CLAUDE.md`? |
| Dependencies | Are new dependencies added to `requirements.txt` or `pyproject.toml`? |
| Breaking changes | Could this change break existing functionality or APIs? |

## Example Review

```bash
# Step 1: Fetch PR details
$ gh pr view 42 --json title,body,files,additions,deletions
{
  "title": "feat: add CSV export endpoint",
  "additions": 147,
  "deletions": 12,
  "files": [
    {"path": "src/app/export.py", "additions": 95},
    {"path": "src/app/routes.py", "additions": 22},
    {"path": "tests/test_export.py", "additions": 30}
  ]
}

# Step 2: Read the diff
$ gh pr diff 42

# Step 3: Check CI
$ gh pr checks 42
All checks passed

# Step 4-5: Checkout and test
$ gh pr checkout 42
$ pytest --tb=short -q
18 passed in 5.23s
```

## Feedback Format

The review follows a consistent structure:

```markdown
## PR Review: feat: add CSV export endpoint (#42)

### Overall Assessment
**Approve** -- Clean implementation with good test coverage.

### Feedback

**src/app/export.py:34** -- The CSV writer does not escape commas
in field values. Consider using `csv.writer` instead of manual
string concatenation.

**src/app/export.py:67** -- This query fetches all rows without
a LIMIT. For large tables, this could cause memory issues. Add
pagination or streaming.

**src/app/routes.py:45** -- Good: the endpoint requires
authentication. No security concerns.

### Suggestions
- Add a `Content-Disposition` header so browsers download the
  file instead of displaying it inline.
- Consider adding a row count limit parameter with a sensible
  default (e.g., 10,000 rows).
```

## Good vs Bad Reviews

!!! warning "Bad: vague, unhelpful feedback"
    ```
    Looks good to me.
    ```

    ```
    This code is bad. Please fix.
    ```

!!! example "Good: specific, actionable, with line references"
    ```
    src/app/export.py:34 -- The CSV writer uses string concatenation
    (`",".join(row)`) which breaks when field values contain commas.
    Replace with `csv.writer` from the standard library:

        import csv
        writer = csv.writer(output)
        writer.writerow(header)
        writer.writerows(data)
    ```

## Posting Reviews to GitHub

After completing the review, the skill can submit it directly:

```bash
# Approve
$ gh pr review 42 --approve --body "Clean implementation, good tests."

# Request changes
$ gh pr review 42 --request-changes --body "See inline comments for required fixes."

# Comment only (no approval or rejection)
$ gh pr review 42 --comment --body "A few suggestions, nothing blocking."
```

## Notes

- The skill always checks out the branch and runs tests locally before providing feedback. Remote CI alone is not sufficient.
- When reviewing large PRs (>500 lines changed), the skill focuses on the most critical files first and flags the PR size as a concern.
- Security issues (hardcoded secrets, injection vulnerabilities) are always flagged as "request changes" regardless of other code quality.
- The review checks for consistency with `CLAUDE.md` project conventions if that file exists in the repository.
