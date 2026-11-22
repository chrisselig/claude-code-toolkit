---
name: git-guardrails
description: Set up a Claude Code hook that blocks destructive git commands (bare force-push, reset --hard, clean -f, branch -D, checkout/restore .) before they execute. Use when the user wants to prevent destructive git operations, add git safety hooks, or stop Claude from force-pushing or hard-resetting without asking first.
argument-hint: "[project|global]"
---

# Git Guardrails

Installs a `PreToolUse` hook on the `Bash` tool that intercepts and blocks a
fixed list of irreversible git commands before Claude runs them. This turns
the warnings already written into `/git-rescue` ("never run `git reset
--hard` while diagnosing", "`--force-with-lease`, never bare `--force`") into
something enforced, not just advised.

## Steps

1. **Determine scope.** Use the argument if given (`project` or `global`);
   otherwise ask: install for **this project only** (`.claude/settings.json`,
   checked into the repo, applies to everyone who clones it) or **every
   project** (`~/.claude/settings.json`, this machine only)?

2. **Check for an existing install.** Read the target settings file. If
   `hooks.PreToolUse` already contains an entry whose command path ends in
   `block-dangerous-git.sh`, stop and tell the user it's already installed —
   don't create a duplicate entry.

3. **Write the hook script** to `.claude/hooks/block-dangerous-git.sh`
   (project) or `~/.claude/hooks/block-dangerous-git.sh` (global), creating
   the `hooks/` directory if needed, then `chmod +x` it:

   ```bash
   #!/usr/bin/env bash
   # Installed by the /git-guardrails skill.
   # PreToolUse hook on Bash: blocks destructive git commands before Claude
   # runs them. Exit 2 + stderr blocks the call; stderr is shown to Claude
   # as the reason, so it can tell the user instead of retrying blindly.

   if ! command -v python3 &>/dev/null; then
     echo "[git-guardrails] WARNING: python3 not found, cannot parse hook input, allowing command through." >&2
     exit 0
   fi

   COMMAND=$(python3 -c '
   import json, sys
   try:
       data = json.load(sys.stdin)
   except Exception:
       sys.exit(0)
   print(data.get("tool_input", {}).get("command", ""))
   ')

   [[ -z "$COMMAND" ]] && exit 0

   block() {
     echo "BLOCKED by git-guardrails: '$COMMAND' matches '$1'. This is irreversible or touches the remote — ask the user to run it themselves." >&2
     exit 2
   }

   # Bare force-push can silently overwrite a collaborator's commits.
   # --force-with-lease is allowed through: it fails safe if the remote moved.
   if echo "$COMMAND" | grep -qE 'git +push' \
     && echo "$COMMAND" | grep -qE '(--force\b|(^| )-f( |$))' \
     && ! echo "$COMMAND" | grep -q 'force-with-lease'; then
     block "push --force (without --force-with-lease)"
   fi

   echo "$COMMAND" | grep -qE 'git +reset +--hard'                          && block "reset --hard"
   echo "$COMMAND" | grep -qE 'git +clean +-[a-zA-Z]*f'                     && block "clean -f"
   echo "$COMMAND" | grep -qE 'git +branch +-D'                             && block "branch -D"
   echo "$COMMAND" | grep -qE 'git +(checkout|restore) +\.([[:space:]]|$)'  && block "checkout/restore ."

   # ponytail: regex over the raw command string, not a real shell/argv
   # parser — a sufficiently obfuscated or quoted command can slip past.
   # Upgrade to tokenizing the command (shlex-style) if that's ever exploited.
   exit 0
   ```

   Note what's deliberately **not** blocked: plain `git push` (no force
   flag). Several skills in this toolkit (`/pr`, `/release`) push as a normal
   step — blocking all pushes would break them. Only the irreversible variant
   is blocked.

4. **Merge the hook entry into the settings file — never overwrite it.**
   Read the file (or start from `{}` if it doesn't exist), add this entry to
   `hooks.PreToolUse` alongside any entries already there, and write the
   whole file back with Python's `json` module (`json.load`, append, `json.dump`
   with `indent=2`) rather than hand-constructing JSON text:

   ```json
   {
     "matcher": "Bash",
     "hooks": [
       {
         "type": "command",
         "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
       }
     ]
   }
   ```

   Use `~/.claude/hooks/block-dangerous-git.sh` as the command for global scope
   instead of the `$CLAUDE_PROJECT_DIR`-relative path.

5. **Verify.** Pipe a known-bad and a known-good command through the script
   directly and check the exit codes:

   ```bash
   echo '{"tool_input":{"command":"git push origin main --force"}}' | .claude/hooks/block-dangerous-git.sh; echo "exit: $?"
   # expect: BLOCKED message on stderr, exit: 2
   echo '{"tool_input":{"command":"git status"}}' | .claude/hooks/block-dangerous-git.sh; echo "exit: $?"
   # expect: exit: 0, no output
   ```

   If either check doesn't match, fix the script before telling the user it's
   installed.

6. **Report what's blocked and what isn't**, and how to make one deliberate
   exception: run the command in a terminal outside Claude Code, rather than
   editing the hook mid-session.

## Examples

### GOOD vs BAD: writing the settings file

**BAD** — clobbers whatever else was in the file:
```python
json.dump({"hooks": {"PreToolUse": [new_entry]}}, open(path, "w"))
```
This silently deletes any other hooks (e.g. an RTK rewrite hook) and any
non-hook settings (permissions, env) already in the file.

**GOOD** — read, append, write back the whole structure:
```python
data = json.load(open(path)) if path.exists() else {}
data.setdefault("hooks", {}).setdefault("PreToolUse", []).append(new_entry)
json.dump(data, open(path, "w"), indent=2)
```

### GOOD vs BAD: what counts as "destructive"

**BAD** — blocking `git push` outright: now `/pr` and `/release` fail every
time they try to push a feature branch, for no safety benefit (a plain push
can't overwrite anyone's history).

**GOOD** — blocking only the variant that can silently destroy work: bare
`--force`/`-f`, not `--force-with-lease`, not a plain push.

## Notes

- This hook only governs commands Claude runs through the `Bash` tool in this
  Claude Code session — it does not stop a human from running the same
  command directly in their own terminal.
- Pairs with `/git-rescue` (recovers from the same categories of mistake this
  hook prevents) and `/protect-main` (server-side branch protection on
  GitHub — this hook is the client-side equivalent for the local working copy).
- Re-running this skill is idempotent: step 2 stops before creating a
  duplicate hook entry.
- If the user wants a pattern added or removed, edit the `grep` lines in
  step 3's script directly — there's no separate config file to keep in sync.
