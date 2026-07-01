# New Dashboard

Scaffold a data dashboard that reads from an existing database and presents it cleanly. Defaults to Streamlit; uses Shiny for Python when you want reactive, finer-grained UI control.

Trigger: `/new-dashboard`

## How It Works

1. **Choose** framework (Streamlit or Shiny), data source (Turso, DuckDB/MotherDuck, SQLite, Parquet), and the tables/metrics to show.
2. **Scaffold** `app.py`, a cached `data.py` access layer, a `components/` directory, config, and `.env.example`.
3. **Isolate data access** — all queries live in `data.py` behind cached functions; the UI never opens a connection inline.
4. **Env-driven connection** — local file for dev, cloud DB when the env var is set.
5. **Layout** — title, filter sidebar, headline metrics, then honest high-density charts.
6. **Run/deploy note** in the README; hand off shipping to [Deploy Streamlit](deploy-streamlit.md).

## Cached, Isolated Data Access

!!! warning "Bad: query in the render path"
    ```python
    conn = duckdb.connect("md:trading")            # reconnects every rerun
    df = conn.execute("SELECT * FROM trades").df() # re-runs on every interaction
    ```

!!! example "Good: cached function, env-driven"
    ```python
    @st.cache_resource
    def _conn():
        return duckdb.connect(os.environ.get("DATABASE_URL", "local.duckdb"))

    @st.cache_data(ttl=300)
    def load_trades(since: str):
        return _conn().execute("SELECT * FROM trades WHERE exit_time >= ?", [since]).df()
    ```

## Streamlit vs Shiny

| Choose | When |
|--------|------|
| Streamlit | Fast build, simple top-to-bottom apps |
| Shiny for Python | Reactive dependencies, modules, tighter layout control |

## Notes

- Cache aggressively but set a TTL on live data, or the dashboard silently shows stale numbers.
- Keep all SQL in `data.py` — mixing queries into UI code makes the app untestable and slow.
- Never commit the Turso/MotherDuck token; use secrets or environment variables.
- Defer chart styling to [Data Visualization](visualization.md); defer deployment to [Deploy Streamlit](deploy-streamlit.md).
