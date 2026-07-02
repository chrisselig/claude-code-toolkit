---
name: deps
description: Audit project dependencies for outdated, vulnerable, or missing packages. Use when the user wants to check dependency health or security.
---

# Check Dependencies

Audit project dependencies for issues.

## Steps

1. Identify the dependency files: `requirements.txt`, `pyproject.toml`, `package.json`, etc.
2. Check for outdated packages:
   - Python: `pip list --outdated` (if in a venv/conda env; for conda-managed packages also check `conda list`)
   - Node: `npm outdated`
3. Check for security vulnerabilities:
   - Python: `pip-audit` (install it if missing — do not use `safety check`, which now requires a login)
   - Node: `npm audit`
4. Verify lock file consistency:
   - Are pinned versions in requirements.txt still matching pyproject.toml ranges?
   - Any deps in code imports that aren't in requirements?
5. Report: total deps, outdated count, any security issues, any missing deps.

Read-only audit: report findings and suggested upgrade commands, but never upgrade, pin, or remove packages unless the user asks. If a tool is unavailable and can't be installed, say which check was skipped rather than silently omitting it.
