---
name: new-dashboard
description: Scaffold a new data dashboard app in Streamlit or Shiny for Python, wired to a Turso/DuckDB/SQLite data source with cached queries and a clean layout. Use when starting a new dashboard, an internal data app, or a reporting UI.
---

# New Dashboard

Scaffold a dashboard that reads from an existing database and presents it cleanly. Defaults to Streamlit; use Shiny for Python when the user wants reactive, finer-grained UI control.

## Steps

1. Ask (or infer) the essentials:
   - Framework: **Streamlit** (fast, simple) or **Shiny for Python** (reactive, granular).
   - Data source: Turso, DuckDB/MotherDuck, SQLite, or Parquet.
   - What it shows: the core tables/metrics and any filters (date range, pair, category).

2. **Scaffold the structure:**
   ```
   dashboard/
   ├── app.py               # entry point
   ├── data.py              # cached data-access layer (all DB queries here)
   ├── components/          # reusable chart/table functions
   ├── .streamlit/config.toml   # (Streamlit) theme + settings
   ├── .env.example         # DB connection vars
   └── requirements.txt / pyproject.toml
   ```

3. **Isolate data access in `data.py`.** All queries live here behind cached functions — the UI never opens a connection inline. Cache with `@st.cache_data` (Streamlit) or a module-level cached helper (Shiny) so every widget interaction doesn't re-hit the database.

4. **Read connection details from the environment**, never hardcoded. Default to a local file for dev, the cloud DB when the env var is set.

5. **Build the layout:** a title, a filter sidebar, headline metrics up top, then charts/tables. Keep charts honest and high-density (defer to the `/visualization` skill's principles — zero-baseline bars, no chartjunk, direct labels).

6. **Add a run/deploy note** to the README: `streamlit run app.py` or `shiny run app.py`, plus the required env vars. If deploying Streamlit, point to the `/deploy-streamlit` skill.

7. Generate the code, confirm it imports/launches, and summarize how to run it.

## Examples

### Cached, isolated data access

**BAD** — query in the render path, new connection every rerun:
```python
import streamlit as st, duckdb
st.title("Trades")
conn = duckdb.connect("md:trading")           # reconnects on every widget change
df = conn.execute("SELECT * FROM trades").df() # re-runs on every interaction
st.dataframe(df)
```

**GOOD** — cached function, connection reused, env-driven:
```python
# data.py
import os, duckdb, streamlit as st

@st.cache_resource
def _conn():
    return duckdb.connect(os.environ.get("DATABASE_URL", "local.duckdb"))

@st.cache_data(ttl=300)
def load_trades(since: str):
    return _conn().execute(
        "SELECT * FROM trades WHERE exit_time >= ?", [since]
    ).df()
```

### Honest headline metrics

**BAD** — a metric with no context:
```python
st.metric("P&L", "1240")   # pips? dollars? over what window?
```

**GOOD** — labeled and scoped:
```python
st.metric("Net P&L (pips, last 30d)", f"{net:+,.0f}", delta=f"{vs_prev:+,.0f} vs prior 30d")
```

## Notes

- Choose Streamlit for speed of build and simple top-to-bottom apps; choose Shiny for Python when you need reactive dependencies, modules, or tighter layout control.
- Cache aggressively but set a TTL on live data so the dashboard refreshes — an over-cached dashboard silently shows stale numbers.
- Keep all SQL in `data.py`. Mixing queries into UI code makes the app impossible to test and slow to render.
- Secrets: use `.streamlit/secrets.toml` or environment variables, never commit the Turso/MotherDuck token.
- For charts, hand off styling decisions to the `/visualization` skill rather than reinventing them here.
- This scaffolds the app; shipping a Streamlit app is the `/deploy-streamlit` skill's job.
