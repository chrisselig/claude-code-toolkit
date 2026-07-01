# Trade Review

Turn the bot's closed-trade log into an honest performance picture — P&L, win rate, expectancy, drawdown, Sharpe — broken down by pair and event, and compared against the Monte Carlo expectations to detect strategy drift.

Trigger: `/trade-review`

## How It Works

1. **Scope** — time window, optional pair/event filter, data source (Turso by default, SQLite, or DuckDB/MotherDuck).
2. **Load closed trades** — settled trades only (exit price + exit time). Never mix in open positions.
3. **Per-trade P&L** in pips and account currency, respecting direction and captured costs.
4. **Aggregate metrics** overall and by pair/event: win rate, net pips, expectancy, profit factor, max drawdown, Sharpe-like ratio, max consecutive losses.
5. **Live vs backtest** — read the matching `docs/research/<pair>_<event>_mc.md` and place live expectancy next to the Monte Carlo median and 5th percentile.
6. **Report** — summary, per-pair/event table, equity-curve description, and a short "what to act on" list.

## Judging Live Against the Distribution

!!! warning "Bad: judging live in a vacuum"
    ```
    USDJPY/BOJ is down 40 pips over 6 trades. Strategy is broken, turn it off.
    ```
    Six trades is inside normal variance for most edges.

!!! example "Good: measured against the strategy's own distribution"
    ```
    USDJPY / BOJ — 6 trades, -40 pips, expectancy -6.7 pips/trade
    Backtest MC median +30 pips/quarter, 5th pct -25 pips
    Live below 5th percentile → possible edge decay OR small-sample variance.
    Action: re-run /mc-analysis at 15 trades before deciding.
    ```

## Metrics Reported

| Metric | Meaning |
|--------|---------|
| Win rate | % of trades profitable — meaningless without payoff |
| Expectancy | Average pips per trade |
| Profit factor | Gross win / gross loss |
| Max drawdown | Peak-to-trough on the cumulative equity curve |
| Sharpe-like | Mean return / std of returns (rough gauge) |
| Max consecutive losses | Worst losing streak |

## Notes

- Small samples lie — always show the trade count next to any rate, and resist conclusions under ~20 trades.
- Separate **strategy** problems (negative expectancy, clean fills) from **execution** problems (single-leg fills, slippage, spread).
- Win rate must be paired with payoff: 40% at 3:1 beats 80% at 1:5.
- For charts, hand off to [Data Visualization](visualization.md). Read-only — it never modifies trade data.
