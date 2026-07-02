---
name: protect-main
description: Check whether the main branch has GitHub protection rules and apply flexible protection (require PRs, allow admin bypass) if missing. Use when setting up branch protection on a repo.
---

# Protect Main Branch

Check if the main branch has protection rules enabled. If not, apply flexible protection (require PRs but allow admin bypass).

## Steps

1. Determine the default branch — don't assume `main`:
   `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`
2. Run `gh api repos/{owner}/{repo}/branches/<default>/protection` to check current status.
3. If protected, report the current rules and exit without changing anything — the existing rules may be intentionally stricter than this skill's defaults.
4. If not protected (HTTP 404 "Branch not protected"), apply flexible protection. Pass the payload as a JSON body with `--input` — typed nulls and nested objects are unreliable with `--field`:

```bash
gh api "repos/{owner}/{repo}/branches/<default>/protection" \
  --method PUT --input - <<'EOF'
{
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": false,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 0
  },
  "enforce_admins": false,
  "required_status_checks": null,
  "restrictions": null
}
EOF
```

5. Confirm protection was applied by re-running the GET from step 2 and showing the resulting rules.

## Notes

- A 404 on the GET can mean "branch not protected" **or** "branch doesn't exist" — check the message body before applying.
- A 403 usually means a private repo on a free plan (branch protection requires a paid plan for private repos) or missing admin rights. Report the actual error; don't retry.
- All four top-level keys in the payload are required by the API — omitting one is a 422, not a partial update.

## Rules Applied

- PRs required (no direct pushes from non-admins)
- Admin bypass enabled (repo owner can still push directly)
- Force pushes blocked
- Branch deletion blocked
- 0 approvals required (can merge own PRs)
