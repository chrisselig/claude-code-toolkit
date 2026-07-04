# Deploy Streamlit

Deploy or debug a Streamlit application. Covers local development, Streamlit Community Cloud, Docker, and systemd service setups. Handles environment-aware database connections, caching, and layout best practices.

## How It Works

1. **Verify locally** -- Run `streamlit run app.py --server.headless true` and confirm the app loads without errors.
2. **Pre-deployment checks** -- Validate that all imports are in `requirements.txt`, no hardcoded local paths exist, and secrets are stored properly.
3. **Deploy** -- Push to the appropriate target:
    - **Streamlit Community Cloud**: Push to GitHub, connect at `share.streamlit.io`
    - **Local systemd service**: Generate a service file for persistent hosting
    - **Docker**: Generate a `Dockerfile` with the correct base image and port exposure
4. **Verify** -- Confirm the deployment is live and report the URL.

## Database Connections

!!! warning "Bad: hardcoded paths that crash in the cloud"
    ```python
    import sqlite3
    conn = sqlite3.connect("/home/user/data/app.db")
    ```

!!! example "Good: environment-aware, works locally and in Streamlit Cloud"
    ```python
    import os
    import duckdb
    import streamlit as st

    @st.cache_resource
    def get_connection():
        db_url = os.environ.get("DATABASE_URL", "local.duckdb")
        return duckdb.connect(db_url, read_only=True)
    ```

    On Streamlit Cloud, set `DATABASE_URL` in the app's Secrets management. Locally, it falls back to a local DuckDB file.

## Caching

Streamlit reruns the entire script on every user interaction. Without caching, data reloads on every button click.

!!! warning "Bad: reloads data on every interaction"
    ```python
    def load_data():
        return pd.read_csv("big_file.csv")  # runs on every click
    df = load_data()
    ```

!!! example "Good: cached with TTL for fresh data"
    ```python
    @st.cache_data(ttl=3600)  # refresh hourly
    def load_data():
        return pd.read_csv("big_file.csv")
    df = load_data()
    ```

Use `@st.cache_data` for DataFrames and serializable objects. Use `@st.cache_resource` for database connections and ML models.

## Layout

!!! warning "Bad: everything in a single column with no structure"
    ```python
    st.title("Dashboard")
    st.metric("Sales", 100)
    st.metric("Users", 50)
    st.dataframe(df)
    fig = px.line(df, x="date", y="value")
    st.plotly_chart(fig)
    ```

!!! example "Good: organized with columns, tabs, and sidebar filters"
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

## Secrets Management

| Environment | Method |
|-------------|--------|
| Local dev | `.env` file loaded with `python-dotenv` or `.streamlit/secrets.toml` |
| Streamlit Cloud | App settings > Secrets (TOML format) |
| Docker | `--env-file .env` flag or Docker Compose `env_file` directive |

!!! tip "Streamlit secrets.toml format"
    ```toml
    # .streamlit/secrets.toml (gitignored)
    DATABASE_URL = "md:my_production_db"
    API_KEY = "sk-..."
    ```
    Access in code with `st.secrets["DATABASE_URL"]`.

## Pre-Deployment Checklist

1. All imports listed in `requirements.txt` with pinned versions
2. No absolute file paths -- use relative paths or environment variables
3. Secrets in `.streamlit/secrets.toml` or env vars, never in source code
4. `st.set_page_config()` called as the first Streamlit command
5. Heavy computations wrapped in `@st.cache_data` or `@st.cache_resource`
6. `.streamlit/config.toml` present for consistent theming

## Notes

- Always set `layout="wide"` for data-heavy dashboards with multiple charts or tables.
- Add a `.streamlit/config.toml` for theme consistency across local and deployed environments.
- For Docker deployments, expose port 8501 and set `--server.address 0.0.0.0`.
- Streamlit Cloud provides free hosting for public repos. Private repos require a paid plan.
- The pre-push secret scan pairs with [Secrets Audit](secrets-audit.md) for a deeper pass that includes git history.
