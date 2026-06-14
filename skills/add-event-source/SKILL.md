# Add Event Source

Add a new economic event source to the forex trading bot. Ensures the full pipeline is ready: cron schedule covers event times, strategy params match MC analysis, static calendar has dates, and Dukascopy data is downloaded.

## Steps

1. Identify the new event from the user's request:
   - Event name (e.g., "BOJ Policy Rate", "RBA Rate Decision")
   - Country and currency pair (e.g., Japan -> USDJPY)
   - Typical release time in ET (e.g., BOJ = ~4:30 AM ET, varies)
   - Frequency (monthly, 8x/year, quarterly, etc.)
   - Source: Forex Factory (auto-scraped) or static calendar (manual YAML)

2. **Check MC analysis approval.** Read the relevant MC report in `docs/research/` to confirm:
   - The pair + event combination passes walk-forward validation.
   - Note the recommended params (distance/TP/SL pips).
   - If analysis says "avoid" or "borderline/paper-trade only", warn the user and confirm before proceeding.

3. **Check cron schedule coverage.** The bot must be running BEFORE the event. Calculate:
   - Event time in MT (America/Edmonton). ET is MT + 2 hours.
   - The bot needs `pre_event_minutes` (currently 30 min) lead time.
   - TWS takes up to 3 minutes to start + 15 seconds init = ~4 minutes.
   - Therefore TWS+bot must start at least **35 minutes before** the event.
   - Current cron entries are in `scripts/start_tws_and_bot.sh` (comments) and the user's crontab.
   - If no existing cron covers the event time, propose a new cron entry.
   - Run `crontab -l` to see current entries.
   - Format: `minute hour * * days` in MT (server timezone).
   - Prefer grouping events that are close in time under one cron entry.
   - BOJ example: 4:30 AM ET = 2:30 AM MT -> cron at `50 1 * * 1-5` (1:50 AM MT, 40 min buffer).

4. **Check if event is on Forex Factory or needs static calendar.**
   - Forex Factory covers: US events (NFP, CPI, FOMC, PPI, GDP, PCE, UC, ISM, Retail Sales), AU events (RBA, AU CPI, AU Employment), some JPY events.
   - Static calendar needed for: SARB, TCMB, SA CPI, and any event NOT reliably on Forex Factory.
   - If static calendar is needed, check `config/static_events.yaml` for existing entries.
   - Add event dates sourced from the **official central bank calendar** — never extrapolate or invent dates.
   - Cross-reference at least two sources for dates.

5. **Check `config/settings.yaml`.**
   - Verify the pair is in `trading.instruments`.
   - Verify `straddle_pair_overrides` has the correct params from MC analysis.
   - If the event needs different params than the pair's default (like TCMB vs US events on USDTRY), add an `event_overrides` entry.
   - Verify `risk.max_spread_overrides` has an appropriate spread limit for the pair.

6. **Check Dukascopy historical data.**
   - Verify the pair exists in `scripts/download_dukascopy.py` event-pair mapping.
   - If not, add it and run a download: `~/anaconda3/envs/forex-bot/bin/python scripts/download_dukascopy.py --pair PAIR --timeframe 1min`.

7. **Check Turso sync cron window.** The Turso sync cron must cover the event time + holding window:
   - Run `crontab -l` and find the `sync_to_turso.py` entries.
   - Current weekday window: `7 5-23 * * 1-5` (5 AM - 11 PM MT).
   - Current Sunday window: `7 15-23 * * 0` (3 PM - 11 PM MT).
   - The sync must run from event time through `max_holding_minutes` (currently 120 min) after the event.
   - If the event falls outside the sync window, extend the hour range in the crontab.
   - Example: an event at 9 PM MT with 2-hour hold needs sync until 11 PM MT. If the window ends at 5 PM, extend to `5-23`.

8. **Check Turso schema.** Verify the Turso dashboard can display the new pair/event. No code changes needed — Turso stores whatever the bot pushes — but confirm the pair name is consistent.

9. **Summary checklist.** Print a table:

   | Check | Status | Action needed |
   |-------|--------|---------------|
   | MC analysis approved | PASS/FAIL/BORDERLINE | link to report |
   | Cron covers event time | PASS/FAIL | proposed cron entry |
   | Calendar source | FF / Static | dates added? |
   | settings.yaml pair | PASS/FAIL | what to add |
   | Strategy params | PASS/FAIL | params from MC |
   | Spread limit | PASS/FAIL | value |
   | Dukascopy data | PASS/FAIL | download needed? |
   | Turso sync window | PASS/FAIL | extended hours needed? |

10. After user confirms, make the changes (cron, config, static calendar). Commit on a feature branch.

## Examples

### Checking cron coverage

**BAD** — assuming the bot is always running:
```
BOJ is at 4:30 AM ET. The bot will pick it up.
```
The bot only runs when TWS is started by cron. If no cron entry covers the event time, the bot is not running.

**GOOD** — calculating from event time back to required cron:
```
BOJ Policy Rate: 4:30 AM ET = 2:30 AM MT
Pre-event lead time: 30 minutes -> must be running by 2:00 AM MT
TWS startup overhead: ~4 minutes -> cron at 1:50 AM MT
Proposed cron: 50 1 * * 1-5
This only runs on BOJ days (~8/year), so consider a conditional check
or a separate cron that exits early if no BOJ event is scheduled today.
```

### Adding event_overrides

**BAD** — overwriting the pair's default params:
```yaml
USDJPY:
  distance_pips: 25   # Changed from BOJ-optimal to match some other event
  tp_pips: 15
  sl_pips: 15
```
This changes ALL USDJPY events. If the pair trades on both US and BOJ events with different optimal params, the default should be the most common event source.

**GOOD** — using event_overrides for event-specific params:
```yaml
USDJPY:
  distance_pips: 50    # Default for US events (if applicable)
  tp_pips: 70
  sl_pips: 10
  event_overrides:
    BOJ:
      distance_pips: 25
      tp_pips: 15
      sl_pips: 15
```

### Checking Turso sync coverage

**BAD** — ignoring the sync window:
```
The trade will sync to Turso automatically.
```
The Turso sync runs on a cron schedule, not continuously. If the event fires outside the sync window, the dashboard won't update until the next sync period.

**GOOD** — verifying the sync window covers event + hold:
```
BOJ at 9:00 PM MT + 2hr max hold = 11:00 PM MT
Current weekday sync: 5-23 MT -> covers up to 11:07 PM MT
PASS — no change needed.

If sync were 5-17 MT:
FAIL — extend to 5-23: sed 's/5-17/5-23/' in crontab
```

## Notes

- The bot's `pre_event_minutes` setting (currently 30) determines how early before the event the straddle orders are placed. The cron must start TWS+bot before this window opens.
- TWS has a daily disconnect at ~11:45 PM ET. Events between 11:30 PM and 12:15 AM ET are risky due to potential disconnect/reconnect timing.
- Paper trading on port 4002/7497 does NOT require 2FA — fully unattended. Live trading on port 4001/7496 requires 2FA and cannot auto-start.
- IB Gateway restarts are idempotent — `start_tws_and_bot.sh` checks if TWS is already running before launching.
- For events that only happen 8-12 times per year (like BOJ, TCMB), running a daily cron that starts early "just in case" wastes resources. Consider a wrapper script that checks if an event is scheduled today before starting TWS.
- All event times should be verified against the official source. BOJ in particular announces at varying times (typically ~12:00 JST / ~11:00 PM ET previous day, but can be as late as 3:30 PM JST / 2:30 AM ET).
- After adding a new cron entry, update the comments in `scripts/start_tws_and_bot.sh` to document it.
