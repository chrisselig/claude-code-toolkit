---
name: new-web-app
description: Scaffold a new React + Vite + TypeScript web app with standard tooling — ESLint, Prettier, Vitest, a src layout, and git init. Use when starting a new web app (frontend or full-stack) from scratch that isn't a Python project.
---

# New Web App Setup

Scaffold a new React + Vite + TypeScript web app with standard tooling. This is
the web-app counterpart to `new-project` (which is Python-only).

## Steps

1. Ask the user for: project name, brief description, and whether it needs a
   backend/API (none — static SPA, a Node/Express API alongside it, or it will
   call an existing external API).
2. Check the target directory: if it already exists and is non-empty, or is
   already inside a git repo (`git rev-parse --git-dir`), stop and confirm with
   the user before scaffolding into it.
3. Scaffold with Vite, non-interactively:
   ```bash
   npm create vite@latest <project_name> -- --template react-ts
   cd <project_name> && npm install
   ```
   Default to `npm` unless the user asks for `pnpm`/`yarn`, or a lockfile for
   one already exists in a directory they're scaffolding into.
4. Add standard tooling on top of the Vite template:
   - Prettier + `eslint-config-prettier` (so ESLint and Prettier don't fight
     over formatting rules).
   - Vitest + `@testing-library/react` + `jsdom` for component tests.
   - `package.json` scripts: `dev`, `build`, `preview`, `lint`, `format`, `test`.
5. Confirm `tsconfig.json` has `"strict": true` (the Vite react-ts template sets
   this by default — verify rather than assume, since templates change).
6. Create the remaining project files:
   - `.env.example` — placeholder values only, prefixed `VITE_` for anything
     the client needs to read (see Notes on what never belongs here).
   - `.gitignore` for Node (`node_modules/`, `dist/`, `.env`, `.env.local`, `*.local`).
   - `README.md` with setup/run instructions.
   - `CLAUDE.md` with the project's conventions (styling approach, state
     management choice, testing approach) so they're explicit from commit one.
7. Initialize git: `git init`, then `git status` to confirm `node_modules/`,
   `dist/`, and `.env` are not listed, then
   `git add -A && git commit -m "feat: initial project scaffold"`.
8. Create the GitHub repo if requested: `gh repo create` — confirm public vs
   private with the user, and push the initial commit.
9. Set up branch protection using the flexible approach (PRs required, admin
   bypass) — needs the repo pushed to GitHub first; skip with a note if the
   project stays local. Use the `protect-main` skill.

## Examples

### Environment variables

**BAD** — a secret exposed to every visitor's browser:
```bash
# .env
VITE_STRIPE_SECRET_KEY=sk_live_...
```
Anything prefixed `VITE_` is inlined into the client bundle at build time and
is readable by anyone who opens dev tools. There is no way to keep a
`VITE_`-prefixed value secret.

**GOOD** — public config uses the prefix, secrets stay server-side:
```bash
# .env (client, safe to expose)
VITE_API_URL=https://api.example.com

# .env (server only — never prefixed, never imported by client code)
STRIPE_SECRET_KEY=sk_live_...
```

### Prop typing

**BAD** — no type safety, and `React.FC` silently adds an implicit `children` prop:
```tsx
const Card: React.FC = (props: any) => <div>{props.title}</div>;
```

**GOOD** — explicit interface, no implicit children:
```tsx
interface CardProps {
  title: string;
  onSelect?: () => void;
}

function Card({ title, onSelect }: CardProps) {
  return <div onClick={onSelect}>{title}</div>;
}
```

## Notes

- Never put API keys, database URLs, or other secrets in a `VITE_`-prefixed
  env var — they ship to the browser. Server-side secrets belong in an API
  route/serverless function or a separate backend, never in client code.
- If the project needs a backend, scaffold it in a sibling `server/` directory
  with its own `package.json` — don't mix server and client dependencies in
  one `package.json`, or the client bundle picks up server-only packages.
- For deployment, use the `deploy-web-app` skill once the app is ready to ship.
- For UI component conventions (styling approach, accessibility, composition),
  use the `ui-components` skill.
