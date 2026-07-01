---
name: deps
description: Audit project dependencies for outdated, vulnerable, or missing packages. Use when the user wants to check dependency health or security.
---

# Check Dependencies

Audit project dependencies for issues.

## Steps

1. Identify the dependency files: `requirements.txt`, `pyproject.toml`, `package.json`, etc.
2. Check for outdated packages:
   - Python: `pip list --outdated` (if in a venv/conda env)
   - Node: `npm outdated`
3. Check for security vulnerabilities:
   - Python: `pip-audit` (if available) or `safety check`
   - Node: `npm audit`
4. Verify lock file consistency:
   - Are pinned versions in requirements.txt still matching pyproject.toml ranges?
   - Any deps in code imports that aren't in requirements?
5. Report: total deps, outdated count, any security issues, any missing deps.
