---
name: release
description: Create a semver tag and GitHub release with auto-generated notes. Use when the user wants to cut a release or tag a new version.
---

# Create a Release

Tag and release the current state of the project.

## Steps

1. Run `git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~20)..HEAD` to see commits since last tag.
2. Determine the next version using semver:
   - `feat:` commits → minor bump
   - `fix:` commits → patch bump
   - Breaking changes → major bump
   - If no previous tags, start at `v0.1.0`
3. Generate release notes from commit messages, grouped by type (Features, Fixes, Docs, etc.).
4. Show the user the proposed version and release notes for confirmation.
5. Create the tag: `git tag -a v<version> -m "Release v<version>"`
6. Push the tag: `git push origin v<version>`
7. Create GitHub release: `gh release create v<version> --title "v<version>" --notes "..."`
8. Report the release URL.
