# MC Analysis

Run Monte Carlo and walk-forward validation for a forex pair + economic event, then write the `docs/research/` report that the [Add Event Source](add-event-source.md) skill reads. This is the upstream gate — no event reaches the live bot without a PASS here.

Trigger: `/mc-analysis`

## How It Works

1. **Identify the target** — pair (e.g. USDJPY), event (e.g. BOJ Policy Rate), and the params to validate or sweep (`distance_pips`, `tp_pips`, `sl_pips`).
2. **Confirm historical data exists** — the backtest needs Dukascopy bars covering every past event date. If missing, run [Backfill](backfill.md) first.
3. **Walk-forward validation** — split events chronologically, optimize on in-sample folds, measure on untouched out-of-sample folds. Never optimize on the full history.
4. **Monte Carlo simulation** — bootstrap the out-of-sample trade sequence (~10,000 runs) to estimate the distribution of outcomes, including the left tail.
5. **Verdict** — PASS / BORDERLINE / AVOID against consistent thresholds on out-of-sample expectancy and 5th-percentile Monte Carlo outcome.
6. **Write the report** to `docs/research/<pair>_<event>_mc.md` in the format `add-event-source` expects.

## Why Walk-Forward + Monte Carlo

!!! warning "Bad: optimize and report on the same data"
    ```python
    best = max(grid, key=lambda p: backtest(all_events, p).net_pips)
    print(backtest(all_events, best).net_pips)   # in-sample fantasy
    ```
    This reports the best-fit curve, not forward performance. It always looks good and never survives live.

!!! example "Good: optimize in-sample, measure out-of-sample"
    ```python
    for train, test in walk_forward_split(events, n_folds=5):
        best = max(grid, key=lambda p: backtest(train, p).expectancy)
        oos.append(backtest(test, best))   # untouched data
    ```

## Verdict Thresholds

| Verdict | Condition |
|---------|-----------|
| PASS | Positive out-of-sample expectancy across folds **and** acceptable 5th-percentile Monte Carlo outcome |
| BORDERLINE | Positive in aggregate but fragile (some losing folds or a meaningful left tail) — paper-trade only |
| AVOID | Negative out-of-sample expectancy or unacceptable tail risk |

## Notes

- Keep in-sample and out-of-sample strictly separated in time — shuffling leaks the future.
- Model realistic costs: event-time spread, slippage, and single-leg fills.
- Fewer than ~20 historical events means low confidence — state it in the report.
- Analysis-only: it writes a report and does not touch live config or cron. That is [Add Event Source](add-event-source.md).
