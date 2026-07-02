---
name: review-pr
description: Check out a pull request, review the code, run its tests, and provide structured feedback. Use when the user wants a thorough review of an open PR.
argument-hint: "[PR number or URL]"
---

# Review a Pull Request

Thoroughly review a PR and provide feedback.

## Steps

1. Get the PR details: `gh pr view <number> --json title,body,files,additions,deletions,commits`
2. Read the PR diff: `gh pr diff <number>`
3. Check if CI passed: `gh pr checks <number>`
4. Review the code changes for:
   - **Correctness**: Does the logic do what the PR claims?
   - **Tests**: Are new features/fixes covered by tests?
   - **Security**: Any hardcoded secrets, SQL injection, XSS, command injection?
   - **Style**: Does it follow project conventions (check CLAUDE.md)?
   - **Dependencies**: Any new deps added to requirements/pyproject?
   - **Breaking changes**: Could this break existing functionality?
5. Before running anything from the PR: if the author is not the user or a trusted collaborator, inspect the diff for code that executes at install/test time (`.github/workflows/`, `conftest.py`, `setup.py`, pre-commit hooks, new dependencies) — running an untrusted PR's tests executes its code. Flag anything suspicious and ask before proceeding.
6. Note the current branch, check the working tree is clean, then check out and test: `gh pr checkout <number> && pytest`
7. Provide a summary with:
   - Overall assessment (approve / request changes / comment)
   - Specific line-level feedback for any issues found
   - Suggestions for improvement (if any)
8. Switch back to the original branch when done (`git checkout -`) — don't leave the repo sitting on the PR branch.
9. Posting the review to GitHub is outward-facing: show the user the review text and get their go-ahead first, then `gh pr review <number> --approve` or `--request-changes --body "..."`.
