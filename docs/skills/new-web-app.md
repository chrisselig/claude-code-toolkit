# /new-web-app

Scaffold a new React + Vite + TypeScript web app with standard tooling. This is
the web-app counterpart to [New Project](new-project.md), which is Python-only.

## What It Does

1. Asks for the project name, description, and whether a backend/API is needed.
2. Checks the target directory is safe to scaffold into (empty, not already a git repo).
3. Scaffolds with `npm create vite@latest -- --template react-ts`.
4. Adds Prettier, Vitest, and `@testing-library/react` on top of the Vite defaults.
5. Verifies `tsconfig.json` has `"strict": true`.
6. Creates `.env.example`, `.gitignore`, `README.md`, and `CLAUDE.md`.
7. Initializes git and makes the first commit.
8. Optionally creates the GitHub repo and pushes.
9. Optionally applies branch protection via [Protect Main](protect-main.md).

## Example

```
/new-web-app
```

```
Project name: order-tracker
Description: Internal dashboard for tracking order status
Needs a backend/API? No — calls an existing API

$ npm create vite@latest order-tracker -- --template react-ts
$ cd order-tracker && npm install
$ npm install -D prettier eslint-config-prettier vitest @testing-library/react jsdom

Created: .env.example, .gitignore, README.md, CLAUDE.md
$ git init && git add -A && git commit -m "feat: initial project scaffold"
```

## Notes

- Never put secrets in a `VITE_`-prefixed env var — those ship to the browser bundle.
- A backend, if needed, lives in a sibling `server/` directory with its own `package.json`.
- Follow up with [Deploy Web App](deploy-web-app.md) to ship it, and
  [UI Components](ui-components.md) for component conventions.
