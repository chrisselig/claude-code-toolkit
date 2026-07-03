---
name: new-project
description: Scaffold a new Python project with standard tooling — a miniforge conda environment, ruff, pytest, pre-commit, a src layout, and pyproject.toml. Use when starting a new Python project from scratch.
---

# New Python Project Setup

Scaffold a new Python project with standard tooling.

## Steps

1. Ask the user for: project name, brief description, and Python version (default 3.12).
2. Check the target directory: if it already exists and is non-empty, or is already inside a git repo (`git rev-parse --git-dir`), stop and confirm with the user before scaffolding into it.
3. **Create a miniforge conda environment** for the project (preferred over venv/uv — matches the user's work setup):
   ```bash
   conda create -n <project_name> python=3.12 -y
   conda run -n <project_name> python --version   # verify; `conda activate` doesn't work in non-interactive shells
   ```
   Fall back to `venv` only if the user explicitly asks or conda is unavailable. If an env with that name already exists, ask before reusing or recreating it.
4. Create the project structure:

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

5. Generate `pyproject.toml` with:
   - Project metadata
   - `[tool.ruff]` config (line-length=120, target Python version)
   - `[tool.pytest.ini_options]` config
   - `[project.optional-dependencies]` with dev deps (pytest, ruff)
6. Generate `.gitignore` for Python (venv, __pycache__, .env, *.pyc, dist/, *.egg-info/) **before** the first commit. Seed `.env.example` with placeholder values only (`API_KEY=your-key-here`) — never copy or read a real `.env` to build it.
7. Generate a minimal `CLAUDE.md` with project conventions.
8. Initialize git repo: `git init`, then `git status` to confirm `.env` and other ignored files are not listed, then `git add -A && git commit -m "feat: initial project scaffold"`.
9. Create GitHub repo if requested: `gh repo create` — confirm public vs private with the user, and push the initial commit.
10. Set up branch protection using the flexible approach (PRs required, admin bypass) — this needs the repo pushed to GitHub first; skip with a note if the project stays local. Use the `/protect-main` skill.
