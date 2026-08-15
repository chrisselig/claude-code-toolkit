# /deploy-web-app

Deploy or debug a non-Python web app — a Vite/React SPA, a Next.js app, or a
static site — to Vercel, Netlify, or Docker.

## What It Does

1. Verifies the app builds locally (`npm run build`, plus `npm run preview` for
   a Vite SPA to smoke-test the production bundle).
2. Checks for common pre-deploy issues: secrets in client-exposed env vars,
   untracked `.env` files, hardcoded `localhost` URLs, build output committed
   to git.
3. Runs a secret scan before any push — a pushed token is burned even if
   removed later.
4. Deploys to the requested target: Vercel, Netlify, or Docker.
5. Adds a client-side routing rewrite for static SPAs so page refreshes don't 404.
6. Verifies the deployment is live and pulls the platform's actual logs if it fails.

## Example

```
/deploy-web-app
```

```
$ npm run build
✓ built in 4.2s
$ npm run preview
✓ production build serves correctly on :4173

Checking for exposed secrets...
✓ No hardcoded tokens found
✓ .env is gitignored and not tracked

Deploying to Vercel...
✓ Live at https://order-tracker.vercel.app
```

## Notes

- Anything prefixed `VITE_` (Vite) or `NEXT_PUBLIC_` (Next.js) ships to the
  browser — never put a real secret in one of these.
- Next.js deploys most smoothly on Vercel; other hosts need
  `next build && next start` or the `output: "standalone"` mode.
- For a deeper, history-inclusive secret scan, run [Secrets Audit](secrets-audit.md).
