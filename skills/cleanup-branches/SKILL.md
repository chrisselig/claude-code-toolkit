# Cleanup Merged Branches

Delete local and remote branches that have been merged to main.

## Steps

1. Switch to main and pull latest: `git checkout main && git pull`
2. List merged local branches: `git branch --merged main | grep -v '^\*\|main\|master'`
3. List remote branches: `git branch -r --merged origin/main | grep -v 'main\|master\|HEAD'`
4. Show the user what will be deleted and confirm before proceeding.
5. Delete local merged branches: `git branch -d <branch>`
6. Delete remote merged branches: `git push origin --delete <branch>`
7. Run `git remote prune origin` to clean up stale remote tracking refs.
8. Report how many branches were cleaned up.
