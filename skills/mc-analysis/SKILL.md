---
name: mc-analysis
description: Run Monte Carlo and walk-forward validation for a forex pair+event strategy, then write the research report that add-event-source reads. Use when evaluating whether a new pair+event combination is tradeable, or re-validating an existing strategy's params (distance/TP/SL pips).
---

# Monte Carlo & Walk-Forward Analysis

Validate a straddle strategy for a currency pair + economic event, and produce the `docs/research/` report that the `add-event-source` skill consumes. This is the upstream gate: no event should be added to the live bot without a PASS here.

## Steps

1. Identify the target from the user's request:
   - Pair (e.g. USDJPY) and event (e.g. BOJ Policy Rate).
   - Candidate params to sweep, or a single param set to validate: `distance_pips`, `tp_pips`, `sl_pips`, `pre_event_minutes`, `max_holding_minutes`.

2. **Confirm the historical data exists.** The backtest needs Dukascopy 1-min bars for the pair covering all past event dates.
   - Check `data/` (or the project's tick/bar store) for the pair.
   - If missing or stale, stop and tell the user to run the `/backfill` skill (or `scripts/download_dukascopy.py`) first. Do not backtest on partial data.

3. **Align event dates.** Load the event's historical release timestamps from the same source the bot uses (Forex Factory export or `config/static_events.yaml`). Confirm the count is enough for statistical power — flag if fewer than ~20 events (walk-forward needs multiple folds).

4. **Run the walk-forward validation.** Split events chronologically into in-sample (optimize params) and out-of-sample (test) folds. Never optimize on the full history.
   - For each fold: pick the best param set on in-sample, then measure its performance on the untouched out-of-sample events.
   - Report per-fold and aggregate out-of-sample metrics: net pips, win rate, expectancy (pips/trade), profit factor, max consecutive losses.

5. **Run the Monte Carlo simulation.** Resample the out-of-sample trade sequence (bootstrap, ~10,000 runs) to estimate the distribution of outcomes, not a single lucky path.
   - Report: median net pips, 5th/95th percentile, probability of a losing period, max drawdown distribution.

6. **Decide the verdict** using consistent thresholds:
   - **PASS** — positive out-of-sample expectancy across folds AND the 5th-percentile Monte Carlo outcome is acceptable (survives a bad run).
   - **BORDERLINE / paper-trade only** — positive in aggregate but fragile (fails some folds, or 5th percentile is a meaningful loss).
   - **AVOID** — negative out-of-sample expectancy or unacceptable tail risk.

7. **Write the report** to `docs/research/<pair>_<event>_mc.md` in the format `add-event-source` expects. Include: the recommended params, the verdict, per-fold table, Monte Carlo percentiles, event count, data date range, and the date the analysis was run.

8. Summarize the verdict and recommended params to the user. If PASS, remind them the next step is `/add-event-source`.

## Examples

### Avoiding overfitting

**BAD** — optimizing params on all history, then reporting that same history as the result:
```python
best = max(param_grid, key=lambda p: backtest(all_events, p).net_pips)
print(f"Strategy makes {backtest(all_events, best).net_pips} pips")  # in-sample fantasy
```
This reports the best-fit curve, not what you'd have earned trading forward. It will always look good and will not survive live.

**GOOD** — optimize in-sample, measure out-of-sample:
```python
folds = walk_forward_split(events, n_folds=5)
oos_results = []
for train, test in folds:
    best = max(param_grid, key=lambda p: backtest(train, p).expectancy)
    oos_results.append(backtest(test, best))   # untouched data
report(aggregate(oos_results))
```

### Reporting the verdict

**BAD** — a single point estimate:
```
Strategy nets +340 pips. Looks good, add it.
```
One number hides the risk. +340 could be one huge event masking many losers.

**GOOD** — distribution-aware:
```
USDJPY / BOJ — VERDICT: BORDERLINE (paper-trade only)
Out-of-sample expectancy: +4.2 pips/trade across 5 folds (2 folds negative)
Monte Carlo (10k runs): median +180 pips, 5th pct -95 pips, P(losing quarter) 18%
Recommended params: distance=25, tp=15, sl=15
Rationale: positive on aggregate but two losing folds and a real left tail.
```

## Notes

- Keep in-sample and out-of-sample strictly separated in time. Shuffling events across the split leaks future information.
- Model realistic costs: spread at event time (use `risk.max_spread_overrides` as a proxy), slippage on the straddle fills, and the possibility that only one leg fills.
- Event times drift (BOJ especially). Use the actual historical release timestamp per event, not a fixed clock time.
- Fewer than ~20 historical events means low confidence — say so explicitly in the report rather than presenting a clean verdict.
- This skill is analysis-only. It writes a report; it does not touch `config/settings.yaml`, cron, or live params — that is `add-event-source`'s job.
- Re-run this whenever a strategy underperforms live (see `/trade-review`) to check whether the edge decayed or it was variance.
