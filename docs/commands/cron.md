# /cron

List, add, validate, or remove cron jobs for the current project.

## What It Does

1. Lists the current crontab with `crontab -l`
2. Based on the user's request:
    - **List**: displays all cron jobs with human-readable schedule descriptions
    - **Add**: writes a new cron entry, validates the schedule expression, and confirms before installing
    - **Remove**: shows the entry to remove, confirms, then installs the updated crontab
    - **Validate**: checks that scripts referenced in cron jobs exist and are executable
3. Before installing any modified crontab, backs up the current one (`crontab -l > ~/.crontab.backup.<timestamp>`), shows a diff for confirmation, installs the full edited table (never `crontab -r`), and re-lists to verify
4. When adding entries, enforces best practices:
    - Absolute paths for all scripts and interpreters (cron has a minimal PATH and no shell profile)
    - Output redirected to a log file (and the log directory exists)
    - A comment above each entry explaining its purpose
    - Verification that the target script exists and is executable
    - Schedules written in the server's local timezone

## Example

```
/cron
```

Typical output when listing:

```
Current Cron Jobs
=================
1. Weekdays at 5:00 AM MT — Start TWS and trading bot
   0 5 * * 1-5 /home/user/scripts/start_tws_and_bot.sh >> /home/user/logs/bot.log 2>&1

2. Sundays at 3:00 PM MT — Start TWS for AU events
   0 15 * * 0 /home/user/scripts/start_tws_and_bot.sh >> /home/user/logs/bot.log 2>&1

All scripts verified: exist and are executable.
```

### Good vs. Bad Cron Entries

A well-formed entry uses absolute paths, captures output, and includes a descriptive comment:

```bash
# Daily ETL pipeline -- 5 AM MT, logs to ~/logs/
0 5 * * * /home/user/anaconda3/envs/myenv/bin/python /home/user/project/scripts/run_pipeline.py >> /home/user/logs/etl.log 2>&1
```

!!! warning "Common mistakes"
    The following entry will silently fail in most cases because cron does not load your shell profile, so `python` may not resolve and relative paths will not work:

    ```
    0 5 * * * python script.py
    ```

    Always use absolute paths for both the interpreter and the script.

## Notes

- The command never installs a cron entry without user confirmation
- When removing entries, the full entry is shown for review before deletion
- The validate mode checks that every script referenced in the crontab exists on disk and has the executable bit set
- Cron uses the system timezone; the command displays the timezone alongside schedules to avoid confusion
