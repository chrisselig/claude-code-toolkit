---
name: new-project
description: Scaffold a new Python project with standard tooling — a miniforge conda environment, ruff, pytest, pre-commit, a src layout, and pyproject.toml. Use when starting a new Python project from scratch.
---

# New Python Project Setup

Scaffold a new Python project with standard tooling.

## Steps

1. Ask the user for: project name, brief description, and Python version (default 3.12).
2. **Create a miniforge conda environment** for the project (preferred over venv/uv — matches the user's work setup):
   ```bash
   conda create -n <project_name> python=3.12 -y
   conda activate <project_name>
   ```
   Fall back to `venv` only if the user explicitly asks or conda is unavailable.
3. Create the project structure:

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

4. Generate `pyproject.toml` with:
   - Project metadata
   - `[tool.ruff]` config (line-length=120, target Python version)
   - `[tool.pytest.ini_options]` config
   - `[project.optional-dependencies]` with dev deps (pytest, ruff)
5. Generate `.gitignore` for Python (venv, __pycache__, .env, *.pyc, dist/, *.egg-info/).
6. Generate a minimal `CLAUDE.md` with project conventions.
7. Initialize git repo: `git init && git add -A && git commit -m "feat: initial project scaffold"`
8. Create GitHub repo if requested: `gh repo create`
9. Set up branch protection using the flexible approach (PRs required, admin bypass).
