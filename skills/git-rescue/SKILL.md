---
name: git-rescue
description: Diagnose and recover from git mishaps — lost commits, bad rebases or resets, deleted branches, commits on the wrong branch, or an accidentally committed secret. Use when git is in a bad state and work appears lost.
argument-hint: "[what went wrong]"
---

# Git Rescue

Recover from a git mistake without making it worse. The core fact: **committed work is almost never lost** — the reflog keeps orphaned commits for ~90 days — but a panicked second command can destroy what the first one didn't.

## Steps

1. **Stop and diagnose before acting.** Run these and read the output before touching anything:
   - `git status` — current branch, staged/unstaged state
   - `git log --oneline -10` — where HEAD is now
   - `git reflog -20` — where HEAD has *been* (this is the rescue map)
   - `git stash list` — anything parked
   If the user's description is vague, ask what they expected to see vs what they see.

2. **Create a safety net before any fix**: `git branch rescue/<date> <hash>` pointing at the commit(s) to preserve. Every recovery below starts with this — a backup branch costs nothing; a second mistake without one costs the work.

3. Match the situation and apply one targeted fix:
   - **Bad reset / "my commits disappeared"**: find the pre-reset entry in `git reflog`, then `git reset --hard <hash>` (only if the working tree is clean) or cherry-pick from the rescue branch.
   - **Bad rebase or merge**: immediately after, `git reset --hard ORIG_HEAD`; later, find the pre-rebase entry in the reflog.
   - **Deleted branch**: find its last tip in `git reflog` and recreate it: `git branch <name> <hash>`.
   - **Committed on the wrong branch**: `git branch correct-branch` (captures HEAD), then move the wrong branch back with `git reset --hard HEAD~N` — verify N against `git log` first, and only if those commits exist on the new branch.
   - **Detached HEAD with commits**: `git branch rescue/detached <hash>`, then merge or cherry-pick onto the intended branch.
   - **Lost uncommitted changes**: check `git stash list` first. If the changes were ever staged, `git fsck --lost-found` may surface dangling blobs; if they were never `git add`ed or stashed, say honestly that git never had them.
   - **Rewrote a pushed branch (amend/rebase)**: if others may have pulled it, prefer `git revert` or coordinating with them; if the branch is the user's alone, `git push --force-with-lease` — never bare `--force`, and only with explicit user confirmation.
   - **Committed a secret (.env, token, key)**: strip it from history (`git filter-repo`, or amend if not yet pushed) — but if it was ever pushed, treat it as leaked and tell the user to **rotate the credential** regardless of the cleanup.

4. **Verify the rescue.** `git log --oneline`, `git status`, and open or diff the recovered files — confirm the user's actual work is present, not just that a hash moved.

5. **Clean up** the `rescue/` branch only after the user confirms everything is back, and explain in a sentence or two what went wrong so it's avoidable next time.

## Examples

### Reacting vs diagnosing

**BAD** — more state-changing commands as guesses:
```bash
git reset --hard HEAD~3   # "undo" without looking at the reflog
git checkout .            # destroys uncommitted work while "fixing"
git stash clear           # deletes the very stash that held the work
```
Each guess overwrites evidence the reflog, stash, or working tree still held.

**GOOD** — evidence first, backup second, one deliberate fix:
```bash
git reflog -20
# a1b2c3d HEAD@{4}: commit: add straddle exit logic   <- the "lost" work
git branch rescue/2026-07-02 a1b2c3d      # safety net
git log rescue/2026-07-02 --oneline -5    # confirm these are the right commits
git reset --hard rescue/2026-07-02        # single targeted restore
```

### Fixing a shared branch

**BAD** — rewriting history others may have pulled:
```bash
git rebase -i HEAD~5 && git push --force   # collaborators' clones now diverge
```

**GOOD** — a revert is history-safe:
```bash
git revert <bad-commit>    # new commit that undoes it; nobody's clone breaks
git push
```

## Notes

- The reflog is **local-only**: it cannot rescue commits made on another machine, and entries expire (default ~90 days). Rescue sooner rather than later.
- While diagnosing, never run `git checkout .`, `git clean`, `git reset --hard`, or `git stash drop/clear` — they destroy exactly the uncommitted state that might need recovering.
- `--force-with-lease`, never `--force`, and only after explicit user confirmation. On shared or protected branches, fix with `git revert` instead of rewriting.
- A pushed secret is burned even if it's force-pushed away seconds later — scrapers watch public repos. Rotation is the fix; history cleanup is just hygiene.
- If the repo state is truly mangled, a fresh clone plus cherry-picks from the rescue branch beats surgery in place.
