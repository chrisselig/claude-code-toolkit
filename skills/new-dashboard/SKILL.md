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
   ├── styles.css           # ALL custom CSS lives here — never inline
   ├── .streamlit/config.toml   # (Streamlit) theme + settings
   ├── .env.example         # DB connection vars
   └── requirements.txt / pyproject.toml
   ```

3. **Isolate data access in `data.py`.** All queries live here behind cached functions — the UI never opens a connection inline. Cache with `@st.cache_data` (Streamlit) or a module-level cached helper (Shiny) so every widget interaction doesn't re-hit the database.

4. **Read connection details from the environment**, never hardcoded. Default to a local file for dev, the cloud DB when the env var is set.

5. **Respect the framework's reactivity model.** This is the thing that makes these apps fast or slow, correct or buggy — get it right up front.
   - **Streamlit** reruns the *entire script top-to-bottom* on every widget interaction. So: keep expensive work behind `@st.cache_data`/`@st.cache_resource` (see step 3), and persist anything that must survive a rerun (a running total, a selected row, a wizard step) in `st.session_state` — a plain local variable resets every interaction. Don't fake reactivity with manual reruns unless you need them.
   - **Shiny for Python** has a real reactive graph — don't write it like Streamlit. Read inputs inside `@render.*` outputs and `@reactive.calc` (cached, recomputes only when its inputs change); use `@reactive.effect` only for side effects. Derive a value once in a `@reactive.calc` and reuse it rather than recomputing per output.
   - Either way: state flows one direction (inputs → derived data → outputs). Don't mutate shared globals from the render path.

6. **Handle loading, empty, and error states — don't assume the happy path.** A dashboard that shows a raw traceback or a blank screen when the DB is down or a filter matches nothing reads as broken. Wrap slow queries in a spinner (`st.spinner` / Shiny's built-in busy indicators), show an explicit "no data for this filter" message on an empty result, and catch connection/query failures to surface a readable message instead of a stack trace.

7. **Build the layout:** a title, a filter sidebar, headline metrics up top, then charts/tables. Keep charts honest and high-density (defer to the `/visualization` skill's principles — zero-baseline bars, no chartjunk, direct labels).

8. **Put all custom CSS in `styles.css` — never inline.** Create a `styles.css` file and load it once at app startup. Do not sprinkle `st.markdown("<style>…</style>", unsafe_allow_html=True)` through the app, and do not pass `style="…"` on individual HTML elements. One file, loaded once, is the single source of truth for styling — it keeps the Python readable, makes styles reusable, and lets a designer edit CSS without touching app logic.

9. **Add a run/deploy note** to the README: `streamlit run app.py` or `shiny run app.py`, plus the required env vars. If deploying Streamlit, point to the `/deploy-streamlit` skill.

10. Generate the code, confirm it imports/launches, and summarize how to run it.

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

### Reactivity & state

**BAD (Streamlit)** — local variable expected to persist across reruns:
```python
count = 0
if st.button("Add"):
    count += 1          # resets to 0 on the next rerun — always shows 1
st.write(count)
```

**GOOD (Streamlit)** — state kept in `st.session_state`:
```python
st.session_state.setdefault("count", 0)
if st.button("Add"):
    st.session_state.count += 1
st.write(st.session_state.count)
```

**BAD (Shiny)** — recomputing the same expensive query in every output:
```python
@render.data_frame
def table():
    return load_trades(input.since())        # query runs here…
@render.text
def total():
    return f"{load_trades(input.since()).pnl.sum():,.0f}"   # …and again here
```

**GOOD (Shiny)** — derive once in a `@reactive.calc`, reuse everywhere:
```python
@reactive.calc
def trades():
    return load_trades(input.since())        # recomputes only when `since` changes
@render.data_frame
def table():
    return trades()
@render.text
def total():
    return f"{trades().pnl.sum():,.0f}"
```

### Loading, empty, and error states

**BAD** — blank screen on empty data, raw traceback when the DB is down:
```python
df = load_trades(since)          # unhandled: connection error crashes the page
st.dataframe(df)                 # empty filter → a bare empty table, no explanation
```

**GOOD** — spinner, explicit empty state, readable failure:
```python
try:
    with st.spinner("Loading trades…"):
        df = load_trades(since)
except Exception as e:
    st.error(f"Couldn't reach the database: {e}")
    st.stop()

if df.empty:
    st.info("No trades in this window. Widen the date range.")
else:
    st.dataframe(df)
```

### External CSS, not inline

**BAD** — inline `<style>` blocks scattered through the app:
```python
st.markdown("<style>.stMetric{background:#111;padding:1rem}</style>", unsafe_allow_html=True)
st.markdown("<style>h1{color:#4af}</style>", unsafe_allow_html=True)  # more styling later, elsewhere
st.markdown('<div style="padding:1rem;border:1px solid #333">…</div>', unsafe_allow_html=True)
```

**GOOD (Streamlit)** — one `styles.css`, loaded once at startup:
```css
/* styles.css */
.stMetric { background: #111; padding: 1rem; border-radius: 8px; }
h1 { color: #4af; }
```
```python
# app.py — load once, near the top
from pathlib import Path
import streamlit as st

def load_css(path: str = "styles.css"):
    st.markdown(f"<style>{Path(path).read_text()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Trades", layout="wide")
load_css()   # every rule now lives in styles.css
```

**GOOD (Shiny for Python)** — link the stylesheet via `ui.include_css`:
```python
from pathlib import Path
from shiny import ui

app_ui = ui.page_fluid(
    ui.include_css(Path(__file__).parent / "styles.css"),
    ui.h1("Trades"),
    # …
)
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
- Learn the reactivity model before writing UI: Streamlit reruns the whole script per interaction (persist with `st.session_state`); Shiny recomputes only the reactive nodes whose inputs changed (derive with `@reactive.calc`). Writing Shiny like Streamlit — or expecting Streamlit locals to persist — is the most common source of bugs here.
- Always handle the unhappy path: a slow query needs a spinner, an empty result needs a message, and a failed connection needs a caught, readable error — never a raw traceback on the page.
- Keep all SQL in `data.py`. Mixing queries into UI code makes the app impossible to test and slow to render.
- Keep all custom CSS in `styles.css`, loaded once. No inline `<style>` blocks and no `style="…"` attributes on elements — inline styling scatters presentation through the logic and can't be reused or themed. Streamlit theme tokens (colors, fonts) still belong in `.streamlit/config.toml`; `styles.css` is for the rest.
- Secrets: use `.streamlit/secrets.toml` or environment variables, never commit the Turso/MotherDuck token.
- For charts, hand off styling decisions to the `/visualization` skill rather than reinventing them here.
- This scaffolds the app; shipping a Streamlit app is the `/deploy-streamlit` skill's job.
