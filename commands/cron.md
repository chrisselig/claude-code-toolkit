---
name: cron
description: List, add, validate, or remove cron jobs for the current project. Use when the user wants to inspect or edit their crontab or a project's scheduled jobs.
---

# Manage Cron Jobs

List, add, validate, or remove cron jobs for the current project.

## Steps

1. List current crontab: `crontab -l`
2. Based on the user's request:
   - **List**: Show all cron jobs with human-readable schedule descriptions
   - **Add**: Write the new cron entry, validate the schedule expression, confirm with the user before installing
   - **Remove**: Show the entry to remove, confirm, then install updated crontab
   - **Validate**: Check that scripts referenced in cron jobs exist and are executable
3. When adding a cron job:
   - Use absolute paths for all scripts and interpreters
   - Redirect output to a log file: `>> ~/logs/job.log 2>&1`
   - Add a comment above the entry explaining what it does
   - Verify the script exists and is executable (`chmod +x`)

**BAD** — relative paths, no logging, no comments:
```
0 5 * * * python script.py
```

**GOOD** — absolute paths, logged, documented:
```bash
# Daily ETL pipeline — 5 AM MT, logs to ~/logs/
0 5 * * * /home/doopdeep/anaconda3/envs/myenv/bin/python /home/doopdeep/project/scripts/run_pipeline.py >> /home/doopdeep/logs/etl.log 2>&1
```
