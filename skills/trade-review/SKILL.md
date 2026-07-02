---
name: trade-review
description: Analyze closed trades from Turso/SQLite/DuckDB and report P&L, win rate, expectancy, drawdown, and Sharpe — then compare live results against the backtest to detect strategy drift. Use when the user wants a trading performance review, a P&L summary, or to check whether a strategy is still working live.
argument-hint: "[time window] [pair/event filter]"
---

# Trade Review

Turn the bot's closed-trade log into an honest performance picture, broken down by pair and event, and flag where live results diverge from the Monte Carlo expectations.

## Steps

1. Identify scope from the user's request:
   - Time window (last week, month, since a date, all time).
   - Filter by pair and/or event, or review everything.
   - Data source: the trades table in Turso (default), local SQLite, or DuckDB/MotherDuck.

2. **Load closed trades.** Query only settled trades (has an exit price and exit time). Never mix open positions into realized-P&L stats.
   - Confirm the row count and date range so the user knows what is being measured.

3. **Compute per-trade P&L in pips and account currency.** Respect trade direction (long/short legs of the straddle), and include costs already captured in the log (spread, commission) so the numbers match the broker.

4. **Aggregate metrics** overall and grouped by `pair` and `event`:
   - Trade count, win rate, net pips, net currency P&L.
   - Expectancy (avg pips/trade), profit factor (gross win / gross loss).
   - Max drawdown (peak-to-trough on the cumulative equity curve).
   - Sharpe-like ratio (mean return / std of returns) — label it as a rough gauge, not annualized unless there is enough data.
   - Max consecutive losses, largest single loss.

5. **Compare live vs backtest.** For each pair+event, read the matching `docs/research/<pair>_<event>_mc.md` and put live expectancy next to the Monte Carlo median and 5th percentile.
   - Within the MC distribution -> performing as expected.
   - Below the 5th percentile -> flag as **possible edge decay** and recommend re-running `/mc-analysis`.
   - Also flag execution problems distinct from strategy: frequent single-leg fills, abnormal slippage, or spread blowouts at event time.

6. **Present a clean report:** an overall summary, a per-pair/event table, the equity curve description (or a chart via `/visualization` if asked), and a short "what to act on" list.

7. Never modify trade data — this is read-only analysis.

## Examples

### Counting only what's realized

**BAD** — mixing open and closed positions:
```sql
SELECT SUM(unrealized_pnl + realized_pnl) FROM trades;  -- moves every tick
```
Unrealized P&L is mark-to-market noise. It makes "performance" change every time you run the report.

**GOOD** — realized only, explicit:
```sql
SELECT pair, event, entry_time, exit_time, pips, pnl
FROM trades
WHERE exit_time IS NOT NULL          -- settled
  AND exit_time >= :since;
```

### Live vs backtest comparison

**BAD** — judging live in a vacuum:
```
USDJPY/BOJ is down 40 pips over 6 trades. The strategy is broken, turn it off.
```
Six trades is inside normal variance for most edges. Killing it here may be a mistake.

**GOOD** — measured against the strategy's own distribution:
```
USDJPY / BOJ — 6 trades, -40 pips, expectancy -6.7 pips/trade
Backtest (docs/research): MC median +30 pips/quarter, 5th pct -25 pips
Live sits below the 5th percentile -> possible edge decay OR small-sample variance.
Action: only 6 trades — keep paper/live small, re-run /mc-analysis at 15 trades
before deciding. Also: 2 of 6 were single-leg fills (execution, not strategy).
```

## Notes

- Small samples lie. Always show the trade count next to any win rate or expectancy, and resist strong conclusions under ~20 trades.
- Separate **strategy** problems (negative expectancy with clean fills) from **execution** problems (single-leg fills, slippage, spread) — the fixes are completely different.
- Win rate alone is meaningless without payoff: a 40% win rate with 3:1 winners is excellent; an 80% win rate with 1:5 losers is a slow bleed. Always pair win rate with expectancy/profit factor.
- Drawdown should be computed on the ordered equity curve (by exit time), not as the single worst trade.
- If the user wants charts (equity curve, per-event bars), hand off to the `/visualization` skill for Tufte-clean output.
- Timezones: the trades table stores UTC or MT depending on the bot config — confirm which before bucketing by day, or daily P&L will be misattributed around midnight.
