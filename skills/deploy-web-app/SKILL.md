---
name: deploy-web-app
description: Deploy or debug a web app (Vite/React SPA, Next.js, or static site) to Vercel, Netlify, or Docker. Use when shipping a web app, troubleshooting a deployment, or diagnosing a build/runtime error.
---

# Deploy Web App

Deploy or debug a non-Python web application.

## Steps

1. Verify the app builds locally: `npm run build`. For a Vite SPA, also smoke
   test the production build with `npm run preview` — dev mode hides bugs that
   only show up in the built bundle (missing env vars, broken relative paths).
2. Check for common issues before deploying:
   - No secrets in client-bundled env vars — anything prefixed `VITE_`
     (Vite) or `NEXT_PUBLIC_` (Next.js) ships to the browser; server secrets
     must be read only in server-side code (API routes, serverless functions).
   - `.env`/`.env.local` gitignored **and** not already tracked (`git ls-files`).
   - No hardcoded `localhost` URLs for API calls — use an env var for the API
     base URL so it resolves correctly in production.
   - `node_modules/` and the build output (`dist/`, `.next/`) gitignored.
3. **Secret scan before any push** — deploying via a connected GitHub repo means
   pushing the code, and a pushed token is burned even if removed later:
   - Grep for hardcoded tokens:
     `grep -riE "token|api_key|secret|password" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" .`
     and stop on any hit that isn't an env-var read.
   - For a deeper pass that includes git history, run `/secrets-audit` — a
     secret deleted from the tip may still be in a commit that's about to be pushed.
4. Deploy based on target:
   - **Vercel**: `vercel --prod`, or connect the GitHub repo for git-based
     deploys — framework (Vite/Next.js) is auto-detected.
   - **Netlify**: `netlify deploy --prod`; set the build command and publish
     directory in `netlify.toml` if not already configured.
   - **Docker**: generate a multi-stage Dockerfile — a `node` build stage,
     then serve the static output from `nginx` (SPA) or `node:alpine` running
     `next start` (Next.js SSR).
5. For a static SPA (Vite, not Next.js), add a catch-all rewrite so
   client-side routing doesn't 404 on refresh — e.g. a Vercel `rewrites` rule
   or Netlify `_redirects` file pointing all paths to `/index.html`.
6. Verify the deployment is live and report the URL. If it fails, pull the
   platform's actual build/runtime logs (Vercel dashboard or `vercel logs`,
   Netlify deploy log, `docker logs`) and diagnose from the real error — the
   most common causes are a missing env var on the platform (not just
   locally), a package needed at runtime that's listed under `devDependencies`,
   or a build command that doesn't match what the platform expects.

## Examples

### API base URL

**BAD** — works locally, 404s in every deployed environment:
```ts
fetch("http://localhost:3000/api/users")
```

**GOOD** — resolves per environment:
```ts
fetch(`${import.meta.env.VITE_API_URL}/api/users`)
```

### Client-side routing on refresh

**BAD** — no rewrite rule; refreshing `/dashboard` returns a 404 from the host:
```
# no _redirects or rewrites configured
```

**GOOD** — Netlify `_redirects`, so every path falls back to the SPA shell:
```
/*    /index.html   200
```

## Notes

- Next.js deploys most smoothly on Vercel (built by the same team); other
  hosts need `next build && next start`, or the `output: "standalone"` build
  mode for a minimal Docker image.
- Use `/secrets-audit` for the deeper, history-inclusive scan — same caveat as
  the Streamlit deploy skill: removing a secret from the current file doesn't
  remove it from history.
- If the app was scaffolded with `new-web-app`, its `.env.example` already
  documents which vars are client-safe (`VITE_`-prefixed) vs. server-only.
