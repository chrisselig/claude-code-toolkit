---
name: todo
description: Scan the project for roadmap files and inline TODO/FIXME comments and report what remains. Use when the user wants to see outstanding work or TODO items.
---

# Check TODO Status

Scan the project for remaining TODO items and give a status report.

## Steps

1. Look for a roadmap/TODO file (common locations: `docs/research/todo.md`, `TODO.md`, `docs/TODO.md`, `ROADMAP.md`).
2. If found, read it and summarize:
   - Items marked as DONE (strikethrough or checkmarks)
   - Items still open, grouped by priority/category
   - Count: X done, Y remaining
3. Also scan the codebase for inline TODOs, excluding vendored and generated dirs:
   `grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.py" --include="*.ts" --include="*.js" --exclude-dir={.git,.venv,venv,node_modules,site,dist,build} . | head -30`
   - If more than 30 hits, report the total count so the truncation is visible.
4. Present a concise summary of what's left to do.
