---
name: review-pr
description: Check out a pull request, review the code, run its tests, and provide structured feedback. Use when the user wants a thorough review of an open PR.
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
5. Check out the branch locally and run tests: `gh pr checkout <number> && pytest`
6. Provide a summary with:
   - Overall assessment (approve / request changes / comment)
   - Specific line-level feedback for any issues found
   - Suggestions for improvement (if any)
7. Optionally post the review: `gh pr review <number> --approve` or `--request-changes --body "..."`
