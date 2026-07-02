# Protect Main

Check whether the `main` branch has protection rules enabled, and apply flexible protection if it does not. Uses the GitHub API directly via the `gh` CLI.

## How It Works

1. **Detect the default branch** -- `gh repo view --json defaultBranchRef` (works for `main`, `master`, or anything else).
2. **Check current status** -- Query the GitHub API for existing protection rules on the default branch.
3. **If already protected** -- Report the current rules and exit. No changes are made.
4. **If unprotected** -- Apply flexible protection rules via `PUT` to the branch protection endpoint.
5. **Verify** -- Re-query the endpoint and confirm the rules landed.

## Protection Rules Applied

| Rule | Setting | Effect |
|------|---------|--------|
| Pull request reviews | Required | No direct pushes from non-admin contributors |
| Required approvals | 0 | You can merge your own PRs without waiting for review |
| Dismiss stale reviews | Disabled | Approvals are not dismissed when new commits are pushed |
| Code owner reviews | Disabled | No `CODEOWNERS` file required |
| Enforce admins | Disabled | Repo owner/admins can push directly to main |
| Force pushes | Blocked | Prevents history rewriting on main |
| Branch deletion | Blocked | Main cannot be deleted |
| Status checks | None required | CI is not gated (add manually if needed) |

## The API Call

The payload is passed as a JSON body via `--input` — typed nulls and nested objects are unreliable with `--field`:

```bash
gh api "repos/{owner}/{repo}/branches/main/protection" \
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

## Flexible vs Strict Protection

The skill applies **flexible** protection by default, which is suitable for solo developers and small teams. Here is how it compares to a stricter setup:

| Setting | Flexible (default) | Strict |
|---------|-------------------|--------|
| Approvals required | 0 | 1 or more |
| Admin bypass | Yes | No (`enforce_admins=true`) |
| Stale review dismissal | No | Yes |
| Status checks | None | CI must pass |
| Code owners | Not required | Required |

!!! tip "Upgrading to strict protection"
    If your project grows to multiple contributors, consider tightening the rules:

    ```bash
    gh api "repos/{owner}/{repo}/branches/main/protection" \
      --method PUT --input - <<'EOF'
    {
      "required_pull_request_reviews": {
        "dismiss_stale_reviews": true,
        "require_code_owner_reviews": true,
        "required_approving_review_count": 1
      },
      "enforce_admins": true,
      "required_status_checks": { "strict": true, "contexts": ["ci"] },
      "restrictions": null
    }
    EOF
    ```

## Verification

After applying protection, the skill runs a verification query:

```bash
$ gh api repos/{owner}/{repo}/branches/main/protection \
    --jq '{
      pr_reviews: .required_pull_request_reviews.required_approving_review_count,
      enforce_admins: .enforce_admins.enabled,
      force_pushes: .allow_force_pushes.enabled
    }'

{
  "pr_reviews": 0,
  "enforce_admins": false,
  "force_pushes": false
}
```

## Notes

- This skill requires the `gh` CLI to be authenticated with a token that has `repo` scope.
- Branch protection is a GitHub feature. It does not apply to local-only repositories.
- The skill targets the repo's default branch (detected via `gh repo view`). To protect other branches (e.g., `develop`), modify the branch name in the API call.
- A 403 on the PUT usually means a private repo on a free plan or missing admin rights — the skill reports the error instead of retrying.
- Free GitHub plans support branch protection on public repos only. Private repos require GitHub Pro or a paid plan.
