# /todo

File open roadmap items and inline `TODO`/`FIXME`/`HACK`/`XXX` comments as GitHub
issues, instead of just printing a status report.

## What It Does

1. Verifies `gh` is authenticated and the current directory is a GitHub repo.
2. Scans for open work:
    - Roadmap/TODO files in common locations (`TODO.md`, `docs/TODO.md`,
      `docs/research/todo.md`, `ROADMAP.md`) — items not marked done.
    - Inline `TODO`, `FIXME`, `HACK`, `XXX` markers in source, excluding vendored
      and generated directories.
3. Dedupes against existing GitHub issues (open and closed) using a hidden
   `<!-- todo-source: file:line -->` marker embedded in each issue body, so
   reruns don't create duplicates.
4. Drafts a proposed issue per remaining item: a conventional-commit-style title,
   a body with the source location and context, and labels (`bug`, `tech-debt`,
   `enhancement`, `priority:*`) — creating any missing standard labels first.
5. Shows the full proposed batch and **waits for confirmation** before creating
   anything on GitHub.
6. Creates the confirmed issues with `gh issue create`, retrying once on failure.
7. Reports what was created, what was already tracked, and what failed.
8. Optionally — only if you say yes — updates the inline comments to reference
   the new issue number (`TODO(#123): ...`) for traceability.

## Example

```
/todo
```

Typical flow:

```
Scanning docs/research/todo.md and source for TODO/FIXME/HACK/XXX...
Found 6 roadmap items, 4 inline markers.
3 already tracked by existing issues (skipped).

Proposed issues:
  fix: handle IB Gateway daily disconnect at 11:45 PM ET      [bug, priority:medium]
    src/broker/client.py:142
  refactor: extract retry logic out of order placement        [tech-debt]
    src/execution/engine.py:87
  feat: add Telegram alert for circuit breaker reset           [enhancement]
    docs/research/todo.md

Create these 3 issues? (y/n)
```

## Notes

- Nothing is written to GitHub until you confirm the batch — this is a
  shared-state, visible action, not a read-only report.
- One issue per discrete item; unrelated TODOs are never bundled together.
- If a PR resolves one of these issues, include `Closes #<issue>` in the PR
  body (see [PR Workflow](pr.md)) so merging it closes the issue automatically.
- Requires the `gh` CLI, authenticated (`gh auth status`).
