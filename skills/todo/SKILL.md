---
name: todo
description: Scan roadmap files and inline TODO/FIXME/HACK/XXX comments, dedupe against existing GitHub issues, then file the remaining open items as new issues after user confirmation. Use when the user wants outstanding work tracked as GitHub issues instead of a scattered TODO list.
---

# File TODOs as GitHub Issues

Turn open roadmap items and inline `TODO`/`FIXME`/`HACK`/`XXX` comments into tracked
GitHub issues, instead of just reporting them. Never creates an issue silently —
always shows the proposed batch and waits for confirmation first, since opening
issues is visible to everyone with repo access.

## Steps

1. Verify prerequisites — stop and report if either fails:
   - `gh auth status` succeeds (if not, tell the user to run `gh auth login`).
   - `gh repo view --json nameWithOwner` resolves the current repo.

2. Scan for open work:
   - **Roadmap files**: look in common locations (`docs/research/todo.md`, `TODO.md`,
     `docs/TODO.md`, `ROADMAP.md`). If found, read it and extract items **not** marked
     done (strikethrough/checked), capturing any priority or category label.
   - **Inline markers**: scan source for `TODO`, `FIXME`, `HACK`, `XXX`, excluding
     vendored/generated dirs:
     ```bash
     grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.py" --include="*.ts" --include="*.js" \
       --exclude-dir={.git,.venv,venv,node_modules,site,dist,build} .
     ```
     Adjust `--include` patterns to match the project's actual languages.
   - If nothing is found in either source, report "nothing to file" and stop —
     do not create empty or speculative issues.

3. Dedupe against existing issues so reruns don't create duplicates:
   - `gh issue list --state all --limit 300 --json number,title,body,state`
   - Every issue this skill creates carries a hidden marker in its body:
     `<!-- todo-source: <file>:<line> -->` for inline items, or
     `<!-- todo-source: roadmap:<slug-of-item-text> -->` for roadmap items.
   - Drop any scanned item whose marker already matches an existing issue
     (open **or** closed — a closed issue means it was already resolved and
     tracked; don't re-file it just because the comment is still in the code).

4. For each remaining item, draft a proposed issue:
   - **Title** (`<type>: <description>`, same convention as commit messages):
     `FIXME` → `fix:`, `HACK` → `refactor:`, `XXX` → `fix:` (note it's fragile/dangerous
     in the body), inline `TODO` / roadmap item → `chore:` or `feat:` — pick whichever
     the surrounding text implies.
   - **Body**: the source location (`file:line`), a short code snippet or the roadmap
     item's own text for context, the roadmap priority if there was one, and the
     hidden `<!-- todo-source: ... -->` marker from step 3.
   - **Labels**: `bug` for FIXME/XXX, `tech-debt` for HACK/inline TODO, `enhancement`
     for roadmap items that read like new capability, plus `priority:high` /
     `priority:medium` / `priority:low` when the roadmap specified one.
     Check `gh label list` first; create any of the standard labels above that are
     missing (`gh label create <name> --color <hex> --description "..."`) before
     using them — issue creation fails on an unknown label.

5. Show the user the full proposed batch — title, labels, source location, one row
   per issue — and **wait for explicit confirmation** before creating anything.
   This is the safety gate: nothing from step 4 is written to GitHub yet.

6. On confirmation, create each issue:
   ```bash
   gh issue create --title "<title>" --body "<body>" --label "<label1>" --label "<label2>"
   ```
   Capture the returned URL/number for each. If one fails, retry once; if it fails
   again, report the failure and move on to the rest of the batch rather than
   stopping the whole run.

7. Report a summary: issues created (title + URL), items skipped as already tracked,
   and any that failed after retry.

8. Ask whether the user wants inline comments updated to reference the new issue,
   e.g. `TODO(#123): ...`. Only touch source files if they say yes — this is a
   separate, explicit confirmation from step 5 because it edits tracked files
   across the repo rather than just creating issues.

## Examples

### BAD: proposed issue

```
Title: fix stuff
Body: see code
```
No file location, no context, no dedup marker — unfindable later and will be
re-proposed as a "new" item on the next run since nothing ties it back to the source.

### GOOD: proposed issue

```
Title: fix: handle IB Gateway daily disconnect at 11:45 PM ET
Body:
Source: src/broker/client.py:142

    # TODO: handle daily disconnect gracefully
    def reconnect(self): ...

The health check doesn't currently detect stale connections around the daily
IB Gateway reset, so it waits for the next operation to fail instead.

<!-- todo-source: src/broker/client.py:142 -->
Labels: bug, priority:medium
```
Specific title, exact source location, enough context to act without re-reading
the surrounding code, and a marker so a future `/todo` run recognizes it's tracked.

## Notes

- One issue per discrete item — don't bundle unrelated TODOs into a single issue.
- Never file issues for markers inside vendored, generated, or third-party
  directories; reuse the same `--exclude-dir` filtering as the scan.
- Label creation is additive and low-risk, but still report which labels were
  created so the user isn't surprised by new labels appearing on the repo.
- Closing the loop: when a PR resolves one of these issues, include
  `Closes #<issue>` or `Fixes #<issue>` in the PR body (see the `pr` skill) so
  merging it auto-closes the issue instead of leaving it stale.
- If `gh issue list` returns more than 300 issues, the dedupe check only covers
  the most recent 300 — tell the user so they know duplicates are possible on
  very large repos.
