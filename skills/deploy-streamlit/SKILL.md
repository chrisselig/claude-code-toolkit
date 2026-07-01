---
name: deploy-streamlit
description: Deploy or debug a Streamlit dashboard application. Use when shipping a Streamlit app, troubleshooting a deployment, or diagnosing runtime errors in a Streamlit dashboard.
---

# Deploy Streamlit App

Deploy or debug a Streamlit application.

## Steps

1. Verify the app runs locally: `streamlit run app.py --server.headless true`
2. Check for common issues before deploying:
   - All imports available in requirements.txt
   - No hardcoded local file paths (use relative paths or env vars)
   - Secrets in `.streamlit/secrets.toml` or env vars, not in code
   - Database connections handle both local and remote (MotherDuck, Turso)
3. Deploy based on target:
   - **Streamlit Cloud**: Push to GitHub, connect at share.streamlit.io
   - **Local systemd**: Create a service file for persistent local hosting
   - **Docker**: Generate Dockerfile
4. Verify deployment is live and report the URL.

## Examples

### Database connections

**BAD** — hardcoded paths, crashes in cloud:
```python
import sqlite3
conn = sqlite3.connect("/home/user/data/app.db")
```

**GOOD** — environment-aware, works locally and in cloud:
```python
import os
import duckdb

@st.cache_resource
def get_connection():
    db_url = os.environ.get("DATABASE_URL", "local.duckdb")
    return duckdb.connect(db_url, read_only=True)
```

### Caching

**BAD** — reloads data on every interaction:
```python
def load_data():
    return pd.read_csv("big_file.csv")  # runs every click
df = load_data()
```

**GOOD** — cached, with TTL for fresh data:
```python
@st.cache_data(ttl=3600)  # refresh hourly
def load_data():
    return pd.read_csv("big_file.csv")
df = load_data()
```

### Layout

**BAD** — everything in a single column, no structure:
```python
st.title("Dashboard")
st.metric("Sales", 100)
st.metric("Users", 50)
st.dataframe(df)
fig = px.line(df, x="date", y="value")
st.plotly_chart(fig)
```

**GOOD** — organized with columns, tabs, sidebar filters:
```python
st.set_page_config(layout="wide", page_title="Sales Dashboard")

with st.sidebar:
    date_range = st.date_input("Date Range", value=(start, end))
    region = st.selectbox("Region", ["All"] + regions)

col1, col2, col3 = st.columns(3)
col1.metric("Sales", f"${total:,.0f}", f"{delta:+.1f}%")
col2.metric("Orders", orders)
col3.metric("Avg Order", f"${avg:,.2f}")

tab1, tab2 = st.tabs(["Charts", "Data"])
with tab1:
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    st.dataframe(df, use_container_width=True)
```

## Notes

- Always use `st.cache_data` for DataFrames and `st.cache_resource` for connections
- Set `layout="wide"` for data-heavy dashboards
- Use `st.secrets` for Streamlit Cloud, env vars for local/Docker
- Add a `.streamlit/config.toml` for theme consistency across environments
