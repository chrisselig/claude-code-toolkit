# Skills Overview

The Claude Code Toolkit ships with 17 built-in skills that automate common development and data engineering workflows. Each skill is a structured procedure that Claude follows step-by-step, ensuring consistent, high-quality results.

## Skills by Category

### Git and GitHub

| Skill | Description |
|-------|-------------|
| [PR Workflow](pr.md) | Lint, test, branch, commit, and open a pull request in one pass |
| [Review PR](review-pr.md) | Check out a PR, review the diff, run tests, and post feedback |
| [Protect Main](protect-main.md) | Apply branch protection rules via the GitHub API |
| [Cleanup Branches](cleanup-branches.md) | Delete local and remote branches that have been merged to main |

### Data Engineering

| Skill | Description |
|-------|-------------|
| [Data Profile](data-profile.md) | Generate a data quality report for CSV, Parquet, Excel, or database tables |
| [API Explore](api-explore.md) | Hit a public API, inspect the response, and generate a typed Python client |
| [ETL Scaffold](etl-scaffold.md) | Create a standard Extract-Transform-Load pipeline with Pydantic validation |
| [Backfill](backfill.md) | Idempotent, resumable, gap-aware historical data loads |
| [Migrate](migrate.md) | Versioned, reversible schema migrations for SQLite, Turso, and DuckDB |

### Trading

| Skill | Description |
|-------|-------------|
| [MC Analysis](mc-analysis.md) | Monte Carlo + walk-forward validation, writing a strategy research report |
| [Trade Review](trade-review.md) | Analyze closed trades and compare live P&L against the backtest |
| [Add Event Source](add-event-source.md) | Onboard a new economic event to the forex trading bot |

### Project Setup

| Skill | Description |
|-------|-------------|
| [New Project](new-project.md) | Scaffold a Python project with pyproject.toml, ruff, pytest, and git |

### Code Quality

| Skill | Description |
|-------|-------------|
| [Lint Fix](lint-fix.md) | Auto-detect the project linter and fix all errors without manual intervention |

### Dashboards and Visualization

| Skill | Description |
|-------|-------------|
| [Deploy Streamlit](deploy-streamlit.md) | Deploy or debug a Streamlit app locally, on Streamlit Cloud, or via Docker |
| [New Dashboard](new-dashboard.md) | Scaffold a Streamlit or Shiny dashboard over your data source |
| [Data Visualization](visualization.md) | Create clear, honest charts following Edward Tufte and Stephen Few principles |

## How Skills Work

Skills are defined as step-by-step markdown instructions in `skills/*/SKILL.md`. When you ask Claude to perform one of these tasks, it follows the procedure exactly, using the appropriate CLI tools (`gh`, `git`, `ruff`, `pytest`, etc.) and applying the good-practice patterns documented in each skill.

!!! tip "Invoking a skill"
    You do not need to name the skill explicitly. Asking "open a PR for my changes" will trigger the PR Workflow skill. Asking "profile this CSV" will trigger Data Profile. Claude matches your intent to the appropriate skill automatically.

## Customization

Each skill can be extended or overridden by editing its `SKILL.md` file in the `skills/` directory. Project-specific conventions defined in `CLAUDE.md` take precedence over skill defaults when there is a conflict.
