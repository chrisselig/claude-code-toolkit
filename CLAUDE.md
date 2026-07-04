# claude-code-toolkit

Source of truth for the global Claude Code skills (`skills/*/SKILL.md`) and commands
(`commands/*.md`) deployed to `~/.claude/`. The `docs/` tree is a human-facing mirror
built with MkDocs Material and deployed by CI on merge to main. `site/` is build
output — never edit or commit it.

## Editing skills and commands

Every skill/command file follows the house format (see `docs/writing-your-own.md`
for the full guide):

- Frontmatter: `name` (must match the directory/file name), `description`
  (what it does + a "Use when ..." sentence — this is how Claude decides to invoke it),
  and `argument-hint` when the skill takes arguments.
- A `## Steps` section is required: numbered, action-verb steps with decision points
  ("If X, do Y; otherwise Z") and explicit stop conditions for failures.
- Skills should have `## Examples` (labeled **GOOD**/**BAD**, always explaining *why*)
  and `## Notes` for edge cases. Commands stay lean.
- Safety rails are the point of this repo: destructive actions get a backup step and
  user confirmation; read-only skills say they are read-only; bounded retries
  (~3 attempts, then stop and explain); never silence errors to force green.

## The mirror rule

Every change to a skill or command must update its docs page
(`skills/foo/SKILL.md` ↔ `docs/skills/foo.md`, `commands/foo.md` ↔ `docs/commands/foo.md`).
New pages must be added to the `nav` in `mkdocs.yml`, the tables in
`docs/skills/index.md` or `docs/commands/index.md`, and the README's skill/command
tables. `tests/test_toolkit_lint.py` enforces the structural parts of this.

## Verification before any PR

```bash
uv run pytest -q               # structural lint of all skill/command/doc files
uv run mkdocs build --strict   # docs must build clean
uv run pre-commit run --all-files
```

## Workflow

Changes land via PRs to `main` (branch protection is on) with conventional-commit
messages. CI deploys the docs site after merge.
