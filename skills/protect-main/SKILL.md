---
name: protect-main
description: Check whether the main branch has GitHub protection rules and apply flexible protection (require PRs, allow admin bypass) if missing. Use when setting up branch protection on a repo.
---

# Protect Main Branch

Check if the main branch has protection rules enabled. If not, apply flexible protection (require PRs but allow admin bypass).

## Steps

1. Run `gh api repos/{owner}/{repo}/branches/main/protection` to check current status.
2. If protected, report the current rules and exit.
3. If not protected (HTTP 404), apply flexible protection:

```bash
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field "required_pull_request_reviews[dismiss_stale_reviews]=false" \
  --field "required_pull_request_reviews[require_code_owner_reviews]=false" \
  --field "required_pull_request_reviews[required_approving_review_count]=0" \
  --field "enforce_admins=false" \
  --field "required_status_checks=null" \
  --field "restrictions=null"
```

4. Confirm protection was applied successfully.

## Rules Applied

- PRs required (no direct pushes from non-admins)
- Admin bypass enabled (repo owner can still push directly)
- Force pushes blocked
- Branch deletion blocked
- 0 approvals required (can merge own PRs)
