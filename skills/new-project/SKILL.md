# New Python Project Setup

Scaffold a new Python project with standard tooling.

## Steps

1. Ask the user for: project name, brief description, and Python version (default 3.12).
2. Create the project structure:

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

3. Generate `pyproject.toml` with:
   - Project metadata
   - `[tool.ruff]` config (line-length=120, target Python version)
   - `[tool.pytest.ini_options]` config
   - `[project.optional-dependencies]` with dev deps (pytest, ruff)
4. Generate `.gitignore` for Python (venv, __pycache__, .env, *.pyc, dist/, *.egg-info/).
5. Generate a minimal `CLAUDE.md` with project conventions.
6. Initialize git repo: `git init && git add -A && git commit -m "feat: initial project scaffold"`
7. Create GitHub repo if requested: `gh repo create`
8. Set up branch protection using the flexible approach (PRs required, admin bypass).
