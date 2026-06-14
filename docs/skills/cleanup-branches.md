# Cleanup Branches

Delete local and remote branches that have been merged into `main`. Only merged branches are removed. Unmerged branches are never touched.

## How It Works

1. **Switch to main** -- Check out `main` and pull the latest changes.
2. **List merged local branches** -- Find all local branches that have been fully merged into `main`.
3. **List merged remote branches** -- Find all remote branches that have been fully merged into `origin/main`.
4. **Confirm with the user** -- Show exactly which branches will be deleted before proceeding.
5. **Delete local branches** -- Remove merged local branches with `git branch -d`.
6. **Delete remote branches** -- Remove merged remote branches with `git push origin --delete`.
7. **Prune stale refs** -- Run `git remote prune origin` to clean up stale remote-tracking references.
8. **Report** -- Summarize how many branches were cleaned up.

## Example Session

```bash
# Step 1: Switch to main
$ git checkout main && git pull
Already on 'main'
Already up to date.

# Step 2-3: List merged branches
$ git branch --merged main | grep -v '^\*\|main\|master'
  feat/add-export
  fix/null-check
  docs/update-readme

$ git branch -r --merged origin/main | grep -v 'main\|master\|HEAD'
  origin/feat/add-export
  origin/fix/null-check

# Step 4: Confirm (shown to user)
Local branches to delete:
  - feat/add-export
  - fix/null-check
  - docs/update-readme

Remote branches to delete:
  - origin/feat/add-export
  - origin/fix/null-check

# Step 5-6: Delete
$ git branch -d feat/add-export fix/null-check docs/update-readme
Deleted branch feat/add-export (was a1b2c3d).
Deleted branch fix/null-check (was d4e5f6a).
Deleted branch docs/update-readme (was 7b8c9d0).

$ git push origin --delete feat/add-export fix/null-check
 - [deleted]         feat/add-export
 - [deleted]         fix/null-check

# Step 7: Prune
$ git remote prune origin
Pruning origin
 * [pruned] origin/docs/update-readme

# Step 8: Report
Cleaned up 3 local and 2 remote branches.
```

## Safety Checks

| Check | Purpose |
|-------|---------|
| Only `--merged` branches | Unmerged work is never deleted |
| `git branch -d` (not `-D`) | Fails safely if git detects the branch is not fully merged |
| `main` and `master` excluded | The primary branch is never deleted |
| User confirmation | The list of branches is shown before any deletion occurs |

!!! warning "What this skill will NOT do"
    - Delete branches that have not been merged into `main`
    - Delete the `main` or `master` branch
    - Force-delete branches (`-D` is never used)
    - Delete branches without showing the list to the user first

## Dry Run

To preview which branches would be cleaned up without deleting anything, the skill shows the merged branch list and asks for confirmation. If the user declines, no branches are deleted.

```bash
# Preview only -- no deletions
$ git branch --merged main | grep -v '^\*\|main\|master'
  feat/add-export
  fix/null-check

$ git branch -r --merged origin/main | grep -v 'main\|master\|HEAD'
  origin/feat/add-export
```

!!! tip "When to run this"
    Run branch cleanup periodically, especially after a batch of PRs has been merged. A project with dozens of stale branches makes `git branch` output noisy and `git log --all --graph` unreadable.

## Notes

- The skill always starts by switching to `main` and pulling the latest changes to ensure the merged-branch list is accurate.
- Remote branches that were deleted on GitHub (e.g., via the "Delete branch" button after merging a PR) are cleaned up by `git remote prune origin`.
- If a branch exists locally but not on the remote (or vice versa), only the existing copy is deleted.
- The `docs/update-readme` branch in the example above exists only locally (it was merged via a different workflow), so it is deleted locally and pruned from remote tracking.
