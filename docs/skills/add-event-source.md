# Add Event Source

Onboard a new economic event to the forex trading bot, ensuring the full pipeline is ready: the cron schedule covers the event time, strategy params match the MC analysis, the calendar has the dates, and Dukascopy history is downloaded.

Trigger: `/add-event-source`

## How It Works

1. **Identify the event** — name, country/currency pair, release time (ET), frequency, and whether it comes from Forex Factory or a static calendar.
2. **Check MC approval** — read the matching report in `docs/research/` (produced by [MC Analysis](mc-analysis.md)) to confirm the pair+event passes walk-forward validation and note the recommended params. Warn on AVOID/BORDERLINE.
3. **Check cron coverage** — the bot must be running *before* the event. Work back from event time through pre-event lead time and TWS startup to the required cron entry.
4. **Calendar source** — Forex Factory (auto-scraped) or `config/static_events.yaml` (manual, official dates cross-referenced from two sources).
5. **Check `config/settings.yaml`** — instrument present, `straddle_pair_overrides` params from MC, `event_overrides` where an event needs different params than the pair default, spread limits.
6. **Dukascopy data** — verify the pair is downloaded; if not, run [Backfill](backfill.md).
7. **Turso sync window** — the sync cron must cover event time through the max holding window.
8. **Summary checklist** — a pass/fail table before making any changes on a feature branch.

## Cron Coverage

!!! warning "Bad: assuming the bot is always running"
    ```
    BOJ is at 4:30 AM ET. The bot will pick it up.
    ```
    The bot only runs when TWS is started by cron. No covering entry = not running.

!!! example "Good: calculate back from event time"
    ```
    BOJ 4:30 AM ET = 2:30 AM MT; 30-min lead → running by 2:00 AM MT
    TWS startup ~4 min → cron at 1:50 AM MT → 50 1 * * 1-5
    ```

## Event-Specific Params

!!! warning "Bad: overwriting the pair default"
    Changing `USDJPY` defaults changes **all** USDJPY events.

!!! example "Good: `event_overrides`"
    ```yaml
    USDJPY:
      distance_pips: 50      # default for other events
      event_overrides:
        BOJ: { distance_pips: 25, tp_pips: 15, sl_pips: 15 }
    ```

## Notes

- Verify every event time against the official source — BOJ in particular announces at varying times.
- Paper trading (port 4002/7497) runs unattended; live trading (4001/7496) needs 2FA and cannot auto-start.
- For events that fire only 8–12x/year, a daily "just in case" cron wastes resources — consider a wrapper that checks the schedule first.
- Upstream of this skill: [MC Analysis](mc-analysis.md) (approval) and [Backfill](backfill.md) (data). Downstream: [Trade Review](trade-review.md) to confirm it performs live.
