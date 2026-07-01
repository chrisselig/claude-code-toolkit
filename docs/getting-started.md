# Getting Started

This guide walks you through installing and configuring the Claude Code Toolkit — a collection of reusable skills and commands for Python data engineering, Git/GitHub workflows, and dashboard development.

---

## Prerequisites

Before installing the toolkit, ensure you have the following:

| Tool | Minimum Version | Purpose |
|------|----------------|---------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Latest | The CLI agent that consumes skills and commands |
| [GitHub CLI (`gh`)](https://cli.github.com/) | 2.x | PR creation, repo management, issue tracking |
| [Python](https://www.python.org/) | 3.12+ | Runtime for all scripts and projects |
| [Ruff](https://docs.astral.sh/ruff/) | 0.4+ | Linting and formatting |
| [pytest](https://docs.pytest.org/) | 8.x | Test runner |
| Git | 2.x | Version control |

!!! note "Used by this project"
    - **[uv](https://github.com/astral-sh/uv)** — Fast Python package installer, used for dependency management. Run `uv sync` to install dev dependencies.
    - **[pre-commit](https://pre-commit.com/)** — Git hook management for automated linting. Run `pre-commit install` after cloning.
    - **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** — Powers the documentation site.

Verify your environment:

```bash
claude --version
gh --version
python3 --version
ruff version
pytest --version
```

---

## Development Setup

If you're contributing to the toolkit itself, install dev dependencies and pre-commit hooks:

```bash
uv sync
pre-commit install
```

This installs `mkdocs-material`, `ruff`, and `pre-commit` into a local virtual environment and enables the pre-commit hooks for linting on every commit.

---

## Installation

Choose one of three methods depending on how much of the toolkit you need.

### Method 1: Full Install (Recommended)

Clone the repository and symlink all skills and commands into your Claude Code configuration directories.

```bash
# Clone the toolkit
git clone https://github.com/YOUR_ORG/claude-code-toolkit.git ~/claude-code-toolkit

# Create the Claude config directories if they don't exist
mkdir -p ~/.claude/skills
mkdir -p ~/.claude/commands

# Symlink all skills
for skill_dir in ~/claude-code-toolkit/skills/*/; do
    skill_name=$(basename "$skill_dir")
    ln -sf "$skill_dir" ~/.claude/skills/"$skill_name"
done

# Symlink all commands
for cmd_file in ~/claude-code-toolkit/commands/*.md; do
    cmd_name=$(basename "$cmd_file")
    ln -sf "$cmd_file" ~/.claude/commands/"$cmd_name"
done
```

!!! tip "Verify the symlinks"
    ```bash
    ls -la ~/.claude/skills/
    ls -la ~/.claude/commands/
    ```
    Each entry should point back to the corresponding file in your cloned repository.

### Method 2: Cherry-Pick

Copy only the specific skills or commands you need.

```bash
# Example: install just the PR workflow command
mkdir -p ~/.claude/commands
cp ~/claude-code-toolkit/commands/pr.md ~/.claude/commands/pr.md

# Example: install just the Python data engineering skill
mkdir -p ~/.claude/skills/python-data-engineering
cp ~/claude-code-toolkit/skills/python-data-engineering/SKILL.md \
   ~/.claude/skills/python-data-engineering/SKILL.md
```

!!! warning "Cherry-picked files won't auto-update"
    Since these are copies (not symlinks), you will need to manually re-copy files when the toolkit is updated. Consider Method 1 if you want automatic updates via `git pull`.

### Method 3: Manual (Create Your Own)

Use the toolkit's structure as a template and write your own skills and commands from scratch.

```bash
# Create a custom skill
mkdir -p ~/.claude/skills/my-custom-skill
cat > ~/.claude/skills/my-custom-skill/SKILL.md << 'EOF'
# My Custom Skill

## Purpose
Describe what this skill teaches Claude Code to do.

## Instructions
- Step-by-step rules Claude should follow.
- Be specific about tools, conventions, and constraints.

## Examples
Show concrete input/output examples so Claude understands the expected behavior.
EOF

# Create a custom command
cat > ~/.claude/commands/my-command.md << 'EOF'
# My Command

Description of what this command does when invoked with `/my-command`.

## Steps
1. First action.
2. Second action.
3. Final action.
EOF
```

---

## Directory Structure

The toolkit follows the directory layout that Claude Code expects:

```
~/.claude/
  skills/
    python-data-engineering/
      SKILL.md              # Skill definition file (must be named SKILL.md)
    git-github-workflow/
      SKILL.md
    dashboard-dev/
      SKILL.md
    ...
  commands/
    pr.md                   # Slash command: /pr
    status.md               # Slash command: /status
    lint.md                 # Slash command: /lint
    ...
```

### Skills vs. Commands

| | Skills | Commands |
|---|--------|----------|
| **Location** | `~/.claude/skills/<name>/SKILL.md` | `~/.claude/commands/<name>.md` |
| **Invoked by** | Claude automatically, based on context | User types `/<name>` in the CLI |
| **Purpose** | Persistent knowledge and conventions | On-demand actions and workflows |
| **Scope** | Always active in every conversation | Only runs when explicitly called |

!!! info "Project-level overrides"
    You can also place skills and commands inside a specific project's `.claude/` directory. Project-level definitions take precedence over global ones in `~/.claude/`.

    ```
    your-project/
      .claude/
        skills/
          project-specific-skill/
            SKILL.md
        commands/
          deploy.md
    ```

---

## Verify Installation

Once installed, verify that Claude Code can see your skills and commands.

**Check commands:** Open Claude Code and type `/` — you should see your installed commands appear in the autocomplete list.

```
$ claude
> /pr          # Should appear if pr.md is installed
> /status      # Should appear if status.md is installed
```

**Check skills:** Skills load automatically. You can confirm they are being read by asking Claude directly:

```
> What skills do you have loaded?
```

Claude will list the active skills it has access to.

!!! warning "Restart required"
    If you add or modify skills/commands while Claude Code is running, you need to start a new session for the changes to take effect.

---

## Quick Test

Run the `/status` command to confirm everything is working:

```
$ claude
> /status
```

This command asks Claude to report on the current state of your project — Git branch, recent commits, test status, and any uncommitted changes. If it runs without errors and produces a meaningful summary, your installation is working correctly.

You can also try a Git workflow command:

```
> /pr
```

This will walk you through creating a pull request with conventional commit messages, running lint checks, and opening the PR via `gh`.

---

## Customization

Every skill and command is a plain Markdown file. Edit them to match your team's conventions.

### Common Customizations

**Change the default Python version:**

Open the relevant skill file and update version references:

```bash
$EDITOR ~/.claude/skills/python-data-engineering/SKILL.md
```

**Adjust Git workflow rules:**

If your team uses a different branch naming convention or merge strategy, edit the Git skill:

```bash
$EDITOR ~/.claude/skills/git-github-workflow/SKILL.md
```

**Add project-specific overrides:**

For per-project rules that differ from global defaults, create a project-level skill:

```bash
mkdir -p .claude/skills/project-overrides
cat > .claude/skills/project-overrides/SKILL.md << 'EOF'
# Project Overrides

## Conventions
- Use `uv` instead of `pip` for dependency management.
- Branch prefix: `feature/` instead of `feat/`.
- Run `make test` instead of `pytest` directly.
EOF
```

!!! tip "Keep skills focused"
    Each skill should cover one domain. Rather than putting everything into a single large skill file, split concerns into separate skills (e.g., one for testing conventions, one for deployment, one for code style). This makes them easier to maintain and reuse across projects.

---

## Updating

If you used **Method 1 (Full Install)** with symlinks, updating is a single command:

```bash
cd ~/claude-code-toolkit
git pull
```

All symlinked skills and commands will automatically reflect the latest changes.

!!! note "Check the changelog"
    After pulling updates, review the commit history for any breaking changes to skill or command formats:

    ```bash
    git log --oneline -10
    ```

If you used **Method 2 (Cherry-Pick)**, you will need to manually re-copy any updated files:

```bash
# Check what changed since your last update
cd ~/claude-code-toolkit
git pull
git diff HEAD~5 --name-only -- skills/ commands/

# Re-copy any files that changed
cp ~/claude-code-toolkit/commands/pr.md ~/.claude/commands/pr.md
```

---

## Next Steps

- Browse the [Skills Reference](skills/index.md) to see all available skills.
- Browse the [Commands Reference](commands/index.md) to see all available slash commands.
- Read the [Contributing Guide](contributing.md) to add your own skills and commands to the toolkit.
