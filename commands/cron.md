---
name: cron
description: List, add, validate, or remove cron jobs for the current project. Use when the user wants to inspect or edit their crontab or a project's scheduled jobs.
argument-hint: "[list|add|remove|validate] [job description]"
---

# Manage Cron Jobs

List, add, validate, or remove cron jobs for the current project.

## Steps

1. List current crontab: `crontab -l` (an empty crontab exits non-zero — that's fine, not an error).
2. Based on the user's request:
   - **List**: Show all cron jobs with human-readable schedule descriptions
   - **Add**: Write the new cron entry, validate the schedule expression, confirm with the user before installing
   - **Remove**: Show the entry to remove, confirm, then install updated crontab
   - **Validate**: Check that scripts referenced in cron jobs exist and are executable
3. Before installing any modified crontab:
   - **Back up the current one first**: `crontab -l > ~/.crontab.backup.$(date +%Y%m%d-%H%M%S)` — a bad install wipes every job, and there is no undo without a backup.
   - Show the user a diff of old vs new and get confirmation.
   - Install by writing the **full edited table** (`crontab <file>`). Never use `crontab -r`, and never install a partial table — both destroy unrelated entries.
   - Re-run `crontab -l` afterwards and confirm the result matches what was intended.
4. When adding a cron job:
   - Use absolute paths for all scripts and interpreters (cron runs with a minimal PATH and no shell profile — `conda activate` and `~` expansion in commands are not available)
   - Redirect output to a log file: `>> ~/logs/job.log 2>&1`, and make sure the log directory exists
   - Add a comment above the entry explaining what it does
   - Verify the script exists and is executable (`chmod +x`)
   - Remember cron schedules run in the **server's local timezone** — convert event times before writing the entry
   - Never embed a secret inline in a crontab entry — `crontab -l`, the backup files above, and any pasted diff would all capture it. Have the script load its own environment (dotenv or a config file); if an existing entry already carries an inline credential, redact it when displaying and flag it for cleanup

**BAD** — relative paths, no logging, no comments:
```
0 5 * * * python script.py
```

**GOOD** — absolute paths, logged, documented:
```bash
# Daily ETL pipeline — 5 AM MT, logs to ~/logs/
0 5 * * * /home/doopdeep/anaconda3/envs/myenv/bin/python /home/doopdeep/project/scripts/run_pipeline.py >> /home/doopdeep/logs/etl.log 2>&1
```
