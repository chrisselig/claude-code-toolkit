# /env-setup

Detect, create, or verify a Python development environment for the current project.

## What It Does

1. Detects the project's environment configuration:
    - `environment.yml` indicates conda
    - `pyproject.toml` or `requirements.txt` indicates pip/venv
    - An existing conda env or `.venv` directory
2. Based on what is found:
    - **New environment**: creates a miniforge conda env (preferred) with the correct Python version, falling back to venv only if asked or conda is unavailable
    - **Existing environment**: verifies all dependencies are installed and checks for version conflicts
    - **Stale environment**: compares installed packages against requirements and flags drift
3. Installs dependencies:
    - `pip install -r requirements.txt` for pinned dependencies
    - `pip install -e ".[dev]"` if `pyproject.toml` has dev extras
4. Verifies the environment:
    - Python version matches project requirements
    - All imports in `src/` resolve without `ImportError`
    - Linter and test runner are available
5. Reports: environment name, Python version, package count, and any issues

## Example

```
/env-setup
```

Typical output for an existing environment:

```
Environment Check
=================
Type:     conda (forex-bot)
Python:   3.12.4
Packages: 34 installed

Verification:
  All imports resolve                       OK
  requirements.txt matches installed        OK
  pytest available                          OK
  ruff available                            OK

No issues found.
```

Typical output when problems are detected:

```
Environment Check
=================
Type:     venv (.venv)
Python:   3.11.6
Packages: 28 installed

Issues:
  Python version mismatch: project requires >=3.12, found 3.11.6
  Missing packages: httpx, pydantic-settings
  Outdated: sqlalchemy 2.0.20 (requirements.txt pins 2.0.36)

Suggested fix:
  pip install httpx pydantic-settings
  pip install sqlalchemy==2.0.36
```

### Good vs. Bad Environment Setup

!!! warning "System Python is not isolated"
    Installing packages globally with `pip install pandas` leads to version conflicts across projects. Always use an isolated environment.

The correct approach:

```bash
conda create -n myproject python=3.12 -y
conda activate myproject          # interactive shells
# from scripts / non-interactive shells, use: conda run -n myproject pip install ...
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Notes

- The command does not activate environments (that requires shell integration), but it identifies which environment to use and verifies its contents
- For conda environments, it checks the conda env list to find matching environments by name
- Import verification scans `src/` for `import` and `from ... import` statements and confirms each top-level package is installed
- The command never modifies an environment without user confirmation
- Secrets are verified by presence, not value — the command never reads a `.env` file or prints an environment variable's value
