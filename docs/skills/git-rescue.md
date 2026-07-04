# Git Rescue

Diagnose and recover from git mishaps — lost commits, bad rebases or resets, deleted branches, commits on the wrong branch, or an accidentally committed secret.

Trigger: `/git-rescue`

## How It Works

1. **Diagnose first** — `git status`, `git log`, `git reflog -20`, and `git stash list` before touching anything. The reflog is the rescue map: it records every place HEAD has been.
2. **Safety net** — create a `rescue/<date>` branch pointing at the commits to preserve before applying any fix.
3. **One targeted fix** — matched to the situation: bad reset (reflog + reset), bad rebase (`ORIG_HEAD`), deleted branch (recreate from reflog), wrong branch (branch + reset back), detached HEAD (branch + merge), lost uncommitted work (stash, then `git fsck --lost-found`), rewritten pushed branch (`--force-with-lease` with confirmation, or revert), committed secret (history cleanup **plus credential rotation**).
4. **Verify** — confirm the recovered work is present in the files, not just that a hash moved.
5. **Clean up** — delete the rescue branch only after the user confirms, and explain what went wrong.

## Diagnose, Don't Guess

!!! warning "Bad: reacting with more state-changing commands"
    ```bash
    git reset --hard HEAD~3   # "undo" without looking at the reflog
    git checkout .            # destroys uncommitted work while "fixing"
    git stash clear           # deletes the very stash that held the work
    ```
    Each guess overwrites evidence the reflog, stash, or working tree still held.

!!! example "Good: evidence, backup, one deliberate restore"
    ```bash
    git reflog -20
    # a1b2c3d HEAD@{4}: commit: add straddle exit logic   <- the "lost" work
    git branch rescue/2026-07-02 a1b2c3d
    git log rescue/2026-07-02 --oneline -5
    git reset --hard rescue/2026-07-02
    ```

## Safety Rules

| Rule | Why |
|------|-----|
| Backup branch before every fix | A second mistake without one costs the work |
| No `checkout .` / `clean` / `stash drop` while diagnosing | They destroy the uncommitted state that may need recovering |
| `--force-with-lease`, never `--force`, always confirmed | Bare force-push silently overwrites collaborators' work |
| `git revert` on shared branches | History-safe; nobody's clone breaks |
| Pushed secret ⇒ rotate the credential | It's leaked the moment it's pushed, even if force-pushed away |

## Notes

- The reflog is local-only and expires (default ~90 days) — rescue sooner rather than later.
- Uncommitted changes that were never staged or stashed were never in git; the skill says so honestly instead of pretending.
- For a truly mangled repo, a fresh clone plus cherry-picks from the rescue branch beats surgery in place.
- After a secret cleanup, [Secrets Audit](secrets-audit.md) confirms nothing else is tracked or still in history.
