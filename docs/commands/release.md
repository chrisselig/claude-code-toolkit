# /release

Create a semver-tagged release with auto-generated release notes and publish it to GitHub.

## What It Does

1. Verifies preconditions: on the default branch, clean working tree, up to date with the remote, CI green
2. Lists commits since the last tag to determine what has changed (full history if the repo has no tags yet)
3. Determines the next version using semantic versioning:
    - `feat:` commits trigger a **minor** bump
    - `fix:` commits trigger a **patch** bump
    - Breaking changes trigger a **major** bump
    - If no previous tags exist, starts at `v0.1.0`
4. Generates release notes from commit messages, grouped by type (Features, Fixes, Docs, etc.)
5. Verifies the proposed tag doesn't already exist locally or on the remote
6. Shows the proposed version and notes for user confirmation
7. Creates an annotated git tag
8. Pushes the tag to the remote
9. Creates a GitHub release via `gh release create`
10. Reports the release URL

## Example

```
/release
```

Typical interaction:

```
Commits since v0.3.1 (12 commits):
  feat: add Telegram notifications
  feat: add circuit breaker auto-reset
  fix: correct timezone in scheduler
  fix: handle empty order response
  docs: update deployment guide

Proposed version: v0.4.0 (minor bump — 2 new features)

Release notes:
  ## Features
  - Add Telegram notifications
  - Add circuit breaker auto-reset

  ## Fixes
  - Correct timezone in scheduler
  - Handle empty order response

  ## Documentation
  - Update deployment guide

Proceed? (waiting for confirmation)

Tag v0.4.0 created and pushed.
GitHub release: https://github.com/user/repo/releases/tag/v0.4.0
```

!!! warning "Confirmation required"
    The command always pauses for user confirmation before creating the tag and release. No tags are pushed without explicit approval.

!!! tip "Conventional commits"
    This command works best with [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, etc.). Without them, version bumping falls back to a patch increment and release notes are a flat list.

## Notes

- Requires `gh` (GitHub CLI) to be authenticated
- Tags are annotated (`git tag -a`), not lightweight
- The command does not modify `pyproject.toml` or `package.json` version fields; it only creates git tags and GitHub releases
