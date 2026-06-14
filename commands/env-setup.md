# Environment Setup

Set up or verify a Python development environment for the current project.

## Steps

1. Detect the project's environment setup:
   - `environment.yml` → conda
   - `pyproject.toml` or `requirements.txt` → pip/venv
   - Existing conda env or `.venv` directory
2. Based on what's found:
   - **New env**: Create conda env or venv with the right Python version
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

**GOOD** — isolated, reproducible:
```bash
conda create -n myproject python=3.12 -y
conda activate myproject
pip install -r requirements.txt
pip install -e ".[dev]"
```
