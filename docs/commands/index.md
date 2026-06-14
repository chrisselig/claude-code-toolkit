# Commands

Commands are quick, single-purpose actions that gather information or perform a focused task. Unlike [skills](../skills/), which are multi-step interactive workflows with decision points, commands run a well-defined sequence of steps and report back.

| Aspect | Commands | Skills |
|--------|----------|--------|
| **Purpose** | Quick checks, reports, single actions | Multi-step workflows with decisions |
| **Duration** | Seconds to a minute | Minutes, often interactive |
| **Example** | `/status` shows project health | `/pr` walks through lint, test, branch, commit, push, PR |

---

## Available Commands

| Command | Description |
|---------|-------------|
| [`/status`](status.md) | Git status, recent commits, open PRs, lint and test health |
| [`/todo`](todo.md) | Scan roadmap files and inline TODOs across the codebase |
| [`/test`](test.md) | Run the test suite, diagnose and fix failures |
| [`/coverage`](coverage.md) | Run tests with coverage, highlight untested code |
| [`/deps`](deps.md) | Audit dependencies for outdated, vulnerable, or missing packages |
| [`/release`](release.md) | Semver version bump, git tag, and GitHub release |
| [`/db-schema`](db-schema.md) | Inspect, compare, or document database schemas |
| [`/cron`](cron.md) | List, add, validate, or remove cron jobs |
| [`/env-setup`](env-setup.md) | Set up or verify a Python development environment |

---

## Usage

Type any command name as a slash command in Claude Code:

```
/status
/test
/deps
```

Commands require no arguments. They auto-detect project context (language, framework, test runner, database type) and adapt accordingly.

!!! tip "Combine commands for a full health check"
    Run `/status`, then `/test`, then `/deps` in sequence to get a comprehensive view of project health before starting work.
