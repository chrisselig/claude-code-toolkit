# New Project

Scaffold a new Python project with a standard directory layout, `pyproject.toml`, linter and test configuration, `.gitignore`, and an initial git commit. Optionally creates a GitHub repository and applies branch protection.

## How It Works

1. **Gather inputs** -- Ask for the project name, a brief description, and the target Python version (defaults to 3.12).
2. **Create the directory structure** -- Generate the standard src-layout project.
3. **Generate configuration files** -- Write `pyproject.toml`, `.gitignore`, `.env.example`, and `CLAUDE.md`.
4. **Initialize git** -- Run `git init`, stage all files, and create the initial commit.
5. **Create GitHub repo** -- If requested, run `gh repo create` to create a remote repository.
6. **Apply branch protection** -- Set up flexible protection on the main branch (PRs required, admin bypass).

## Directory Structure

```
project_name/
├── src/project_name/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── CLAUDE.md
```

## Generated `pyproject.toml`

The generated `pyproject.toml` includes project metadata, ruff configuration, and pytest settings:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Brief project description"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "ruff>=0.8",
]

[tool.ruff]
target-version = "py312"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

## Generated `.gitignore`

The `.gitignore` covers standard Python exclusions:

```gitignore
# Virtual environments
.venv/
venv/

# Python
__pycache__/
*.pyc
*.pyo
dist/
*.egg-info/

# Secrets
.env

# IDE
.idea/
.vscode/
*.swp

# Data
*.db
data/
```

## Generated `CLAUDE.md`

The `CLAUDE.md` file establishes project conventions for Claude Code:

```markdown
# Project Name

## Conventions
- Python 3.12+, use `from __future__ import annotations`
- Type hints on all function signatures
- Linter: ruff (config in pyproject.toml)
- Tests: pytest (run with `pytest tests/ -v`)

## Commands
- Lint: `ruff check . --fix`
- Test: `pytest tests/ -v`
```

## What Gets Configured

| Tool | Configuration | Purpose |
|------|---------------|---------|
| ruff | `[tool.ruff]` in pyproject.toml | Linting and import sorting |
| pytest | `[tool.pytest.ini_options]` in pyproject.toml | Test discovery and async mode |
| git | `.gitignore` | Exclude generated files and secrets |
| Claude Code | `CLAUDE.md` | Project conventions for AI assistance |

## Customization

!!! tip "Adjusting for your stack"
    The scaffold is a starting point. Common modifications after scaffolding:

    - Add `sqlalchemy`, `httpx`, or other dependencies to `[project.dependencies]`
    - Add `[tool.ruff.lint.per-file-ignores]` for test files
    - Extend `.gitignore` for your specific data formats
    - Add a `Makefile` or `justfile` for common commands

## Notes

- The src-layout (`src/project_name/`) is used instead of flat layout to prevent accidental imports from the project root.
- The initial commit message follows conventional commit format: `feat: initial project scaffold`.
- Branch protection uses the flexible approach: PRs are required for non-admins, but the repo owner can push directly. See the [Protect Main](protect-main.md) skill for details.
- The `.env.example` file documents required environment variables without containing actual secrets.
