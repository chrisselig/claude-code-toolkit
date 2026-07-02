---
name: cleanup-branches
description: Delete local and remote git branches that have already been merged to main. Use when cleaning up stale branches after PRs are merged.
---

# Cleanup Merged Branches

Delete local and remote branches that have been merged to main.

## Steps

1. Check the working tree is clean (`git status --porcelain`). If not, stop — switching branches with uncommitted changes risks losing or dragging work.
2. Switch to main and pull latest: `git checkout main && git pull`
3. List merged local branches: `git branch --merged main | grep -v '^\*\|main\|master'`
4. **Catch squash- and rebase-merged branches too** — `--merged` only sees true merge commits, so branches merged via GitHub's "Squash and merge" never show up. For each remaining local branch, check whether its PR was merged:
   `gh pr list --state merged --head <branch> --json number,mergedAt`
   Branches with a merged PR are safe to delete even though git says "not merged".
5. List remote branches: `git branch -r --merged origin/main | grep -v 'main\|master\|HEAD'`
6. Show the user exactly what will be deleted — local and remote in separate lists — and confirm before proceeding. Never include the default branch, the current branch, or a branch with an **open** PR.
7. Delete local merged branches: `git branch -d <branch>`. For squash-merged branches confirmed via a merged PR in step 4, `-d` will refuse — use `git branch -D <branch>` only for those confirmed cases, never as a blanket fallback.
8. Delete remote merged branches: `git push origin --delete <branch>` — only branches the user confirmed; skip any that GitHub already auto-deleted.
9. Run `git remote prune origin` to clean up stale remote tracking refs.
10. Report how many branches were cleaned up, and list any that were kept and why (unmerged commits, open PR, unpushed work).

## Notes

- A branch that is neither `--merged` nor attached to a merged PR contains unmerged work. Leave it alone and list it for the user — deleting it destroys commits.
- If `gh` is unavailable, skip the squash-merge check and only delete what `--merged` reports; tell the user which branches were left because they couldn't be verified.
