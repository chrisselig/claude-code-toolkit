# Writing Your Own Skills and Commands

This guide covers how to create custom skills and commands for Claude Code,
including file structure, best practices, and realistic examples.

---

## Skills vs Commands — When to Use Which

Skills and commands serve different purposes. Choosing the wrong format leads to
either unnecessary complexity or insufficient guidance.

| Criteria | Skill | Command |
|---|---|---|
| **Steps involved** | Multi-step with branching logic | Single-purpose, linear |
| **Decision-making** | Claude must choose between paths | Minimal or no decisions |
| **Typical duration** | Minutes (creates files, runs tests, opens PRs) | Seconds (reads state, prints output) |
| **Examples needed** | Yes — code examples guide quality | Rarely necessary |
| **Use cases** | PR creation, deployment, data profiling, refactoring | Status checks, dependency audits, log tailing |

**Rule of thumb:** If the task involves "check something and report," use a command.
If the task involves "do something that depends on what you find," use a skill.

```text
Does the task require creating or modifying files?
  YES --> Does it involve decision points or branching?
    YES --> Skill
    NO  --> Could still be a skill, but a command may suffice
  NO  --> Command
```

---

## Skill File Structure

Skills live at `~/.claude/skills/<name>/SKILL.md` (global) or
`.claude/skills/<name>/SKILL.md` (project-scoped).

### Annotated Template

```markdown
# <Skill Name>

<!-- A one-line description of what this skill does and when to use it. -->
Create a pull request with conventional commit messages and a structured PR body.

## Steps

<!-- Numbered, specific, action-oriented steps. -->
<!-- Include decision points where Claude must choose a path. -->

1. Run `git status` to check for uncommitted changes.
   - If there are uncommitted changes, stage and commit them with a
     conventional commit message (e.g., `feat:`, `fix:`, `docs:`).
   - If the working tree is clean, proceed to step 2.

2. Determine the current branch name. If on `main`, stop and warn the user
   that PRs should not be created from the main branch.

3. Push the branch to the remote with `git push -u origin <branch>`.

4. Create the PR using `gh pr create` with:
   - A title matching the branch name converted to a sentence.
   - A body containing: Summary, Changes, and Testing sections.

5. Print the PR URL to the user.

## Examples

<!-- Label examples clearly. Explain WHY something is good or bad. -->

### GOOD: Commit message

```text
feat: add retry logic to webhook handler
```

Follows conventional commits. The scope is clear from the message alone.

### BAD: Commit message

```text
updates
```

No type prefix, no indication of what changed or why.

## Notes

<!-- Edge cases, warnings, and constraints. -->
- If `gh` CLI is not installed, instruct the user to install it.
- Never force-push unless the user explicitly requests it.
- If the branch has no commits ahead of main, warn the user instead of
  creating an empty PR.
```

!!! info "Required Sections"
    Every skill file must have **Steps**. The **Examples** and **Notes** sections
    are optional but strongly recommended — they prevent common mistakes and
    reduce ambiguity.

---

## Command File Structure

Commands live at `~/.claude/commands/<name>.md` (global) or
`.claude/commands/<name>.md` (project-scoped). They are simpler than skills.

### Annotated Template

```markdown
# <Command Name>

<!-- One-line purpose statement. -->
Report the current git status, branch, and recent commit history.

## Steps

1. Run `git status --short` and display the output.
2. Run `git log --oneline -10` and display the output.
3. Summarize: number of modified files, untracked files, and current branch.
```

Commands do not typically need Examples or Notes sections. If you find yourself
adding branching logic and code examples, you probably want a skill instead.

---

## Writing Effective Steps

Steps are the core of both skills and commands. Poorly written steps produce
unpredictable results.

### Principles

1. **Be specific and numbered.** Claude follows numbered steps in order.
2. **Include decision points.** Use "If X, do Y; otherwise Z" to handle branches.
3. **Reference concrete tools and commands.** Say `run pytest tests/unit/ -v`,
   not "run the tests."
4. **State the expected outcome.** Say "this should print 0 failures" so Claude
   knows what success looks like.

### GOOD Step

```markdown
3. Run `pytest tests/unit/ -v --tb=short`.
   - If all tests pass, proceed to step 4.
   - If any tests fail, stop and report the failing test names and error
     messages. Do not continue to step 4.
```

This is specific, references an exact command, and handles both outcomes.

### BAD Step

```markdown
3. Make sure the tests pass.
```

No command specified. No guidance on what to do if tests fail. Claude must
guess what "make sure" means.

---

## Good/Bad Code Examples in Skills

Examples in skill files serve as calibration. Claude uses them to understand
the quality bar you expect. Without examples, Claude falls back to generic
defaults that may not match your project conventions.

### Format

Label every example with **GOOD** or **BAD**. Always explain **why** — the
label alone is not enough.

### Realistic Example

Suppose you have a skill for writing database migration scripts:

````markdown
## Examples

### BAD: Migration script

```sql
ALTER TABLE users ADD COLUMN age int;
```

Missing a default value. Missing a `NOT NULL` constraint or explicit `NULL`.
No `IF NOT EXISTS` guard — reruns will fail. No down migration.

### GOOD: Migration script

```sql
-- Up
ALTER TABLE users ADD COLUMN IF NOT EXISTS age INTEGER NOT NULL DEFAULT 0;

-- Down
ALTER TABLE users DROP COLUMN IF EXISTS age;
```

Includes both directions. Uses `IF NOT EXISTS` / `IF EXISTS` for idempotency.
Specifies `NOT NULL` with a sensible default.
````

!!! warning "Do Not Over-Constrain Examples"
    Examples should demonstrate principles (idempotency, safety, conventions),
    not dictate exact syntax for every scenario. Claude needs room to adapt
    to the specific context.

---

## Testing Your Skills

A skill that works in your main project may break in other contexts. Test
before relying on it.

1. **Try it in a fresh repository.** Clone a minimal test project and invoke
   the skill. Missing assumptions surface quickly in an empty repo.

2. **Test edge cases.** Consider what happens when:
    - The repository has no tests, no linter, or no CI configuration.
    - The working tree is clean (nothing to commit).
    - The user is on the `main` branch.
    - A required CLI tool (`gh`, `jq`, `docker`) is not installed.

3. **Iterate on wording.** If Claude misinterprets a step, rephrase it.
   Small wording changes — "create" vs. "append to," "stop" vs. "warn and
   continue" — produce meaningfully different behavior.

4. **Check output quality.** Review what Claude actually produces. If commit
   messages, PR bodies, or generated code do not meet your standards, add
   or refine the Examples section.

---

## Tips and Best Practices

!!! tip "Keep Skills Focused"
    One workflow per skill. A skill that handles PR creation, deployment, **and**
    changelog updates is doing too much. Split it into three skills and compose
    them if needed.

!!! tip "Don't Over-Specify"
    Prescribe the **what** and the **constraints**, not every implementation
    detail. Claude is better at filling in standard patterns than following
    overly rigid pseudo-code. Say "write unit tests for the new function" rather
    than dictating exact test method names and assertions.

!!! tip "Include Error Handling Guidance"
    Tell Claude what to do when things go wrong. "If the build fails, report
    the error and stop" is better than silence — without guidance, Claude may
    retry indefinitely or silently skip the failure.

!!! tip "Add Notes for Edge Cases"
    The Notes section is your safety net. Use it for constraints that do not
    fit neatly into steps: rate limits, required permissions, OS-specific
    behavior, or tools that must be installed.

!!! tip "Use Action Verbs"
    Start every step with a verb: Run, Create, Check, Read, Open, Delete.
    Passive or ambiguous phrasing ("The tests should be passing") gives Claude
    less to act on than direct instructions ("Run the test suite and verify
    all tests pass").
