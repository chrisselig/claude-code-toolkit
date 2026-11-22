# Wizard

Generate a self-contained bash script that walks a human, stage by stage,
through a manual setup or migration procedure the agent can't perform
itself — opening URLs, capturing values, writing them to `.env` and GitHub
secrets, confirming before anything irreversible.

Trigger: `/wizard`

## How It Works

1. **Scope the procedure** — read `.env`/`.env.example`, the README,
   `docker-compose*`, framework config, and every `secrets.*`/`vars.*`
   reference in CI workflows to find every value that needs capturing.
   Confirm the ordered stage list with the user before writing anything.
2. **Write the shared wizard library verbatim** — progress counter,
   cross-platform `open_url` (including WSL), hidden secret entry,
   idempotent `.env` upserts, `gh secret`/`gh variable` writes. This part is
   identical across every wizard and is never hand-edited.
3. **Author the stages** below the library marker: one `stage()` per manual
   step, using `open_url` before `ask`/`ask_secret`, `write_env` for
   persisted values, `set_secret`/`set_var` only for what CI actually reads,
   `confirm` before anything irreversible.
4. **Verify statically** — `bash -n`, `shellcheck` if available. Never run it
   end-to-end; it blocks on human input and opens a browser.
5. **Hand off** — `chmod +x`, tell the user how to run it, commit it only if
   it's a repeatable setup path rather than a one-off cutover.

## Notes

- Don't invoke this for steps the agent can perform itself — that's scope
  creep onto a human who didn't need to be involved.
- The library degrades gracefully if `gh` isn't installed or authenticated:
  it warns and records the gap in the closing summary instead of failing.
- Library adapted from [mattpocock/skills](https://github.com/mattpocock/skills)
  (`wizard`/`template.sh`, MIT license).
