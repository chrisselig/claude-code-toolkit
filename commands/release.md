---
name: release
description: Create a semver tag and GitHub release with auto-generated notes. Use when the user wants to cut a release or tag a new version.
argument-hint: "[major|minor|patch or explicit version]"
---

# Create a Release

Tag and release the current state of the project.

## Steps

1. Verify preconditions — stop and report if any fail:
   - On the default branch (`git branch --show-current` vs `gh repo view --json defaultBranchRef`), unless the user explicitly wants to release from elsewhere.
   - Clean working tree (`git status --porcelain` is empty) and up to date with the remote (`git fetch && git status`).
   - CI green on the latest commit: `gh run list --limit 3` — warn on red and confirm before proceeding.
2. Find commits since the last tag:
   - Last tag: `git describe --tags --abbrev=0` (may fail if no tags exist — that's fine).
   - If a tag exists: `git log --oneline <last-tag>..HEAD`.
   - If no tags exist: `git log --oneline` (full history — do **not** use `HEAD~20`, which errors on short histories).
   - If there are no commits since the last tag, report "nothing to release" and stop.
3. Determine the next version using semver (or use the version the user passed):
   - `feat:` commits → minor bump
   - `fix:` commits → patch bump
   - Breaking changes (`feat!:` / `BREAKING CHANGE:`) → major bump
   - If no previous tags, start at `v0.1.0`
4. Verify the tag doesn't already exist locally or on the remote: `git tag -l v<version>` and `git ls-remote --tags origin v<version>`.
5. Generate release notes from commit messages, grouped by type (Features, Fixes, Docs, etc.).
6. Show the user the proposed version and release notes and **wait for confirmation** — a pushed tag is public and messy to retract.
7. Create the tag: `git tag -a v<version> -m "Release v<version>"`
8. Push the tag: `git push origin v<version>`
9. Create GitHub release: `gh release create v<version> --title "v<version>" --notes "..."`
   - If this fails after the tag was pushed, report clearly that the tag exists but the release does not, so the state isn't ambiguous.
10. Report the release URL.
