# /deps

Audit project dependencies for outdated versions, security vulnerabilities, and consistency issues.

## What It Does

1. Identifies dependency files: `requirements.txt`, `pyproject.toml`, `package.json`, etc.
2. Checks for outdated packages:
    - Python: `pip list --outdated`
    - Node: `npm outdated`
3. Checks for security vulnerabilities:
    - Python: `pip-audit` (installed on demand; `safety check` is no longer used — it requires a login)
    - Node: `npm audit`
4. Verifies lock file consistency:
    - Are pinned versions in `requirements.txt` still within `pyproject.toml` ranges?
    - Are there imports in source code that reference packages not listed in requirements?
5. Reports totals: dependency count, outdated count, security issues, missing dependencies

## Example

```
/deps
```

Typical output:

```
Dependency Audit
================
Total packages:  34 (from requirements.txt)
Outdated:         3
Vulnerabilities:  1

Outdated:
  Package       Installed  Latest   Type
  httpx         0.25.0     0.28.1   minor
  pydantic      2.5.0      2.10.3   minor
  sqlalchemy    2.0.23     2.0.36   patch

Vulnerabilities:
  Package    Version  Advisory
  certifi    2023.7   GHSA-xqr8-7jwr-rhp7 (moderate)
             Fix: upgrade to >= 2024.2.2

Consistency:
  OK - all imports resolve to installed packages
  OK - pinned versions match pyproject.toml ranges
```

!!! warning "Security vulnerabilities"
    When vulnerabilities are found, the command shows the advisory ID, severity, and the minimum fixed version. Upgrade promptly for anything rated high or critical.

!!! tip "Phantom dependencies"
    The consistency check catches "phantom dependencies" -- packages your code imports that are only available as transitive dependencies of other packages. These can break silently when you upgrade or remove the parent package.

## Notes

- Requires an active virtual environment or conda environment for accurate results
- For Python projects, `pip-audit` is preferred over `safety` as it uses the PyPI advisory database directly
- The command does not automatically upgrade packages; it only reports findings
