# Claude Code Toolkit

**[View the full documentation](https://chrisselig.github.io/claude-code-toolkit/)**

A collection of reusable [Claude Code](https://claude.com/claude-code) skills and commands for Python data engineering, Git/GitHub workflows, and dashboard development.

These are the global skills and commands I use across all my projects. They live in `~/.claude/skills/` and `~/.claude/commands/` and are available in every Claude Code session regardless of which project I'm in.

---

## Quick Start

```bash
# Clone into your home directory
git clone git@github.com:chrisselig/claude-code-toolkit.git ~/claude-code-toolkit

# Symlink into Claude Code's config
ln -sf ~/claude-code-toolkit/skills/* ~/.claude/skills/
ln -sf ~/claude-code-toolkit/commands/* ~/.claude/commands/
```

Or copy individual files:

```bash
# Just want the PR skill?
cp -r ~/claude-code-toolkit/skills/pr ~/.claude/skills/
```

---

## What's Included

### Skills (interactive workflows)

Skills are multi-step workflows triggered with `/skill-name`. They guide Claude through a structured process.

| Skill | Trigger | Description |
|-------|---------|-------------|
| [PR](skills/pr/) | `/pr` | Lint, test, branch, commit, push, create PR — the full workflow |
| [Data Profile](skills/data-profile/) | `/data-profile` | Profile a CSV/Parquet/DB table for data quality issues |
| [API Explore](skills/api-explore/) | `/api-explore` | Hit an API, inspect the response, generate a typed Python client |
| [ETL Scaffold](skills/etl-scaffold/) | `/etl-scaffold` | Create a standard Extract-Transform-Load pipeline project |
| [Deploy Streamlit](skills/deploy-streamlit/) | `/deploy-streamlit` | Deploy or debug a Streamlit dashboard |
| [Lint Fix](skills/lint-fix/) | `/lint-fix` | Auto-detect linter and fix all errors autonomously |
| [New Project](skills/new-project/) | `/new-project` | Scaffold a new Python project with standard tooling |
| [Protect Main](skills/protect-main/) | `/protect-main` | Check and apply branch protection rules |
| [Review PR](skills/review-pr/) | `/review-pr` | Checkout, review code, run tests, provide feedback on a PR |
| [Cleanup Branches](skills/cleanup-branches/) | `/cleanup-branches` | Delete all merged local and remote branches |
| [Data Visualization](skills/visualization/) | `/visualization` | Create clear, honest charts following Tufte and Few principles |
| [Backfill](skills/backfill/) | `/backfill` | Idempotent, resumable, gap-aware historical data loads |
| [Migrate](skills/migrate/) | `/migrate` | Versioned, reversible schema migrations for SQLite/Turso/DuckDB |
| [New Dashboard](skills/new-dashboard/) | `/new-dashboard` | Scaffold a Streamlit or Shiny dashboard over your data source |
| [MC Analysis](skills/mc-analysis/) | `/mc-analysis` | Monte Carlo + walk-forward validation → strategy research report |
| [Trade Review](skills/trade-review/) | `/trade-review` | Analyze closed trades; compare live P&L vs backtest for drift |
| [Add Event Source](skills/add-event-source/) | `/add-event-source` | Onboard a new economic event to the forex trading bot |

### Commands (quick actions)

Commands are triggered with `/command-name` and run a focused task.

| Command | Trigger | Description |
|---------|---------|-------------|
| [Status](commands/status.md) | `/status` | Git status, recent commits, open PRs, lint/test health |
| [TODO](commands/todo.md) | `/todo` | Scan for roadmap files and inline TODOs |
| [Test](commands/test.md) | `/test` | Run test suite, diagnose and fix failures |
| [Coverage](commands/coverage.md) | `/coverage` | Test coverage report with untested code highlighted |
| [Dependencies](commands/deps.md) | `/deps` | Audit for outdated, vulnerable, or missing packages |
| [Release](commands/release.md) | `/release` | Semver tag + GitHub release with auto-generated notes |
| [DB Schema](commands/db-schema.md) | `/db-schema` | Inspect, compare, or diff database schemas |
| [Cron](commands/cron.md) | `/cron` | List, add, validate, or remove cron jobs |
| [Env Setup](commands/env-setup.md) | `/env-setup` | Set up or verify a Python dev environment |
| [Log Triage](commands/log-triage.md) | `/log-triage` | Parse Loguru logs, group errors, summarize an unattended run |
| [Healthcheck](commands/healthcheck.md) | `/healthcheck` | Verify a scheduled job landed: freshness, volume, continuity |

---

## My Workflow

I build Python data projects that follow this pattern:

```
Free API / CSV / Excel
        │
        ▼
   ┌─────────┐
   │ Extract  │  httpx, pandas, polars
   └────┬─────┘
        │
   ┌────▼─────┐
   │ Transform │  polars, Pydantic validation
   └────┬─────┘
        │
   ┌────▼─────┐
   │   Load    │  MotherDuck, Turso, SQLite
   └────┬─────┘
        │
   ┌────▼──────┐
   │ Dashboard  │  Streamlit, Shiny
   └────────────┘
```

These skills and commands are designed around this workflow. They assume:

- **Python 3.12+** with a miniforge conda environment (preferred) or venv
- **Git + GitHub** with conventional commits and PRs
- **ruff** for linting (falls back to flake8)
- **pytest** for testing
- **Pydantic** for data validation
- **polars** preferred over pandas for large data
- **Loguru** for logging

---

## Skill Anatomy

Each skill lives in its own directory with a `SKILL.md` file:

```
skills/
└── data-profile/
    └── SKILL.md
```

A good skill file has:

1. **Title** — what it does in 3-5 words
2. **Steps** — numbered, specific actions for Claude to follow
3. **Good/Bad examples** — concrete code showing the right and wrong way
4. **Notes** — edge cases, preferences, gotchas

Example structure:

```markdown
# Skill Name

Brief description.

## Steps

1. First step
2. Second step
3. ...

## Examples

### Scenario Name

**BAD** — why this is wrong:
\```python
bad_code()
\```

**GOOD** — why this is right:
\```python
good_code()
\```

## Notes

- Important caveat
- Edge case to handle
```

---

## Development Setup

```bash
# Install dev dependencies (mkdocs-material, ruff, pre-commit)
uv sync

# Enable pre-commit hooks
pre-commit install
```

---

## Contributing

This is a personal toolkit, but if you find it useful:

1. Fork it
2. Add your own skills/commands
3. Submit a PR if you think others would benefit

---

## License

MIT
