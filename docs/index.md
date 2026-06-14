# Claude Code Toolkit

A collection of reusable [Claude Code](https://claude.com/claude-code) **skills** and **commands** for Python data engineering, Git/GitHub workflows, and dashboard development.

---

## What is this?

Claude Code lets you define custom **skills** (multi-step workflows) and **commands** (quick actions) that are available in every session. This toolkit is a curated set of both, designed for a specific workflow:

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

But many of the tools are **generic enough for any Python project** — the Git workflows, testing commands, and project scaffolding work everywhere.

---

## Skills vs Commands

| | Skills | Commands |
|---|---|---|
| **What** | Multi-step interactive workflows | Quick single-purpose actions |
| **Where** | `~/.claude/skills/<name>/SKILL.md` | `~/.claude/commands/<name>.md` |
| **Trigger** | `/skill-name` | `/command-name` |
| **Example** | `/pr` walks through lint → test → branch → commit → push → PR | `/status` shows git status + open PRs + test health |
| **Best for** | Complex processes with decisions | Information gathering, quick checks |

---

## Quick Reference

### Skills

| Skill | What it does |
|-------|-------------|
| [`/pr`](skills/pr.md) | Full PR workflow: lint, test, branch, commit, push, create PR |
| [`/data-profile`](skills/data-profile.md) | Profile a CSV/Parquet/DB table for quality issues |
| [`/api-explore`](skills/api-explore.md) | Hit an API, inspect response, generate typed client |
| [`/etl-scaffold`](skills/etl-scaffold.md) | Create a standard ETL pipeline project |
| [`/deploy-streamlit`](skills/deploy-streamlit.md) | Deploy or debug a Streamlit dashboard |
| [`/lint-fix`](skills/lint-fix.md) | Auto-detect linter, fix all errors |
| [`/new-project`](skills/new-project.md) | Scaffold a Python project with standard tooling |
| [`/protect-main`](skills/protect-main.md) | Apply branch protection rules |
| [`/review-pr`](skills/review-pr.md) | Review a PR: checkout, read diff, run tests |
| [`/cleanup-branches`](skills/cleanup-branches.md) | Delete merged local + remote branches |
| [`/visualization`](skills/visualization.md) | Create clear, honest charts (Tufte/Few best practices) |

### Commands

| Command | What it does |
|---------|-------------|
| [`/status`](commands/status.md) | Git status, recent commits, open PRs, test health |
| [`/todo`](commands/todo.md) | Scan for roadmap files and inline TODOs |
| [`/test`](commands/test.md) | Run tests, diagnose failures |
| [`/coverage`](commands/coverage.md) | Test coverage with untested code highlighted |
| [`/deps`](commands/deps.md) | Audit for outdated/vulnerable packages |
| [`/release`](commands/release.md) | Semver tag + GitHub release |
| [`/db-schema`](commands/db-schema.md) | Inspect or diff database schemas |
| [`/cron`](commands/cron.md) | Manage cron jobs |
| [`/env-setup`](commands/env-setup.md) | Set up or verify Python environment |

---

## Get Started

See the [Getting Started](getting-started.md) guide to install these in your Claude Code setup.
