---
name: env-setup
description: Set up or verify a Python development environment for the current project, preferring miniforge conda environments. Use when the user wants to bootstrap or check their dev environment.
---

# Environment Setup

Set up or verify a Python development environment for the current project.

## Steps

1. Detect the project's environment setup:
   - `environment.yml` → conda
   - `pyproject.toml` or `requirements.txt` → pip/venv
   - Existing conda env or `.venv` directory
2. Based on what's found:
   - **New env**: Create a **miniforge conda environment** (preferred — matches the setup usable at work). Fall back to `venv` only if the user asks or conda is unavailable.
   - **Existing env**: Verify all deps are installed, check for version conflicts
   - **Stale env**: Compare installed packages against requirements
3. Install dependencies:
   - `pip install -r requirements.txt` for pinned deps
   - `pip install -e ".[dev]"` if pyproject.toml has dev extras
4. Verify the environment:
   - Python version matches project requirements
   - All imports in `src/` resolve without ImportError
   - Linter and test runner are available
5. Report: env name, Python version, package count, any issues.

**BAD** — using system Python, no isolation:
```bash
pip install pandas  # installs globally, version conflicts
```

**GOOD** — isolated, reproducible, miniforge conda (preferred):
```bash
# conda provided by miniforge (conda-forge default channel)
conda create -n myproject python=3.12 -y
conda activate myproject
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Notes

- Prefer **miniforge** conda environments when creating a new environment — the user uses this at work and finds it easier than venv/uv. Only use `venv`/`uv` when the user explicitly asks or conda is unavailable.
- Miniforge defaults to the `conda-forge` channel; no need to pass `-c conda-forge` for common packages.
- `conda activate` only works in interactive shells. From scripts or Claude's shell, use `conda run -n <env> python ...` (or the env's absolute path, `~/miniforge3/envs/<env>/bin/python`) to run commands inside the env.
- Never install into the `base` environment. If the current env is `base` or system Python, create a project env first.
- If an env with the project's name already exists, verify against it instead of creating a duplicate — ask before recreating or deleting an existing env.
