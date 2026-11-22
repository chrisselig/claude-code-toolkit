# Research

Delegate a factual investigation to a background agent that reads primary
sources and writes findings to a cited Markdown file, instead of filling
the main conversation with pages of docs excerpts.

Trigger: `/research`

## How It Works

1. **Pin down the question** — restate it back if ambiguous; a background
   agent can't ask follow-ups mid-run.
2. **Launch a background agent** with a fresh context window and a
   self-contained brief.
3. **Primary sources only** — official docs, source code, specs, first-party
   APIs, not a secondary write-up. Every claim traces back to the source
   that owns it; disagreements between sources are stated, not resolved by
   guessing.
4. **Write findings to a single Markdown file**, citing each claim (URL or
   `file:line`), saved where the repo already keeps this kind of note.
5. **Report back a short summary and the file path** — not the full
   contents.

## Notes

- Use this for read-only fact-finding. "Go implement X based on the docs"
  is ordinary delegated work, not this skill.
- A fresh context avoids the agent anchoring on whatever the main
  conversation already assumed about the answer.
- Adapted from [mattpocock/skills](https://github.com/mattpocock/skills)
  (`research`, MIT license).
