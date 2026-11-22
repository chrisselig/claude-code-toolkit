# Git Guardrails

Install a `PreToolUse` hook that blocks destructive git commands — bare
force-push, `reset --hard`, `clean -f`, `branch -D`, `checkout`/`restore .`
— before Claude runs them.

Trigger: `/git-guardrails`

## How It Works

1. **Scope** — ask whether to install for this project (`.claude/settings.json`)
   or every project (`~/.claude/settings.json`).
2. **Idempotency check** — stop if the hook is already installed instead of
   duplicating the entry.
3. **Write the hook script** to `.claude/hooks/block-dangerous-git.sh` (or the
   global equivalent) and make it executable. Plain `git push` is
   deliberately **not** blocked — `/pr` and `/release` need it to work.
4. **Merge** the hook into `hooks.PreToolUse` in the settings file — read,
   append, write back the whole structure, never overwrite it.
5. **Verify** with a known-bad and known-good command piped through the
   script directly, checking exit codes 2 and 0.
6. **Report** what's blocked and how to make a deliberate exception (run it
   in a terminal outside Claude Code).

## What Gets Blocked

| Command | Why |
|---------|-----|
| `git push --force` / `-f` (without `--force-with-lease`) | Can silently overwrite a collaborator's history |
| `git reset --hard` | Discards uncommitted work irreversibly |
| `git clean -f` / `-fd` | Deletes untracked files with no undo |
| `git branch -D` | Force-deletes a branch even with unmerged commits |
| `git checkout .` / `git restore .` | Discards all working-tree changes |

`--force-with-lease` and plain `git push` are allowed through.

## Notes

- Client-side only — it governs what Claude runs in this session, not what
  a human types directly into their own terminal.
- Pairs with [Git Rescue](git-rescue.md) (recovers from the mistakes this
  hook prevents) and [Protect Main](protect-main.md) (the server-side
  equivalent on GitHub).
- To add or remove a blocked pattern, edit the `grep` lines in the installed
  script directly.
