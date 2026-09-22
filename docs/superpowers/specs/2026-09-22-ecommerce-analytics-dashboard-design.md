# Design: E-Commerce Analytics Sales Dashboard

Source: `prd/ecommerce-analytics.md`. Tracked milestones: `TASKS.md` (TASK-1 through TASK-7).

## Summary

A single-page Streamlit dashboard reading `data/sales-data.csv` and showing two KPI cards (Total Sales, Total Orders), a daily sales trend line chart, and category/region sales bar charts. Phase 1 scope only — no auth, filtering, export, or database integration (see PRD "Phase 2: Future Enhancements").

## Project structure

```
ai-dev-workflow-tutorial/
├── app.py                  # Streamlit page: layout, KPI cards, charts
├── analytics.py            # Data loading + calculations (pure functions)
├── requirements.txt        # streamlit, pandas, plotly, pytest
├── venv/                   # local virtualenv (already gitignored)
├── .streamlit/
│   └── config.toml         # theme colors
├── data/
│   └── sales-data.csv      # (already exists)
├── tests/
│   └── test_analytics.py   # pytest unit tests against a synthetic fixture
├── prd/ecommerce-analytics.md
└── TASKS.md
```

`analytics.py` has no Streamlit or Plotly imports — only pandas — so it's testable without a running app. `app.py` is the only file that imports Streamlit/Plotly and is the sole consumer of `analytics.py`.

## `analytics.py` — data module

```python
REQUIRED_COLUMNS = {"date", "order_id", "product", "category", "region",
                     "quantity", "unit_price", "total_amount"}

def load_sales_data(path: str) -> pd.DataFrame:
    """Load and parse the sales CSV. Raises ValueError if required columns
    are missing or the date column can't be parsed."""

def total_sales(df: pd.DataFrame) -> float:
    """Sum of total_amount."""

def total_orders(df: pd.DataFrame) -> int:
    """Count of rows (one row = one order line)."""

def sales_by_day(df: pd.DataFrame) -> pd.DataFrame:
    """Columns: date, total_amount — summed per calendar day, sorted by date."""

def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Columns: category, total_amount — summed per category,
    sorted descending by total_amount."""

def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Columns: region, total_amount — summed per region,
    sorted descending by total_amount."""
```

Notes:
- `load_sales_data` does the "basic validation" agreed in brainstorming: checks `REQUIRED_COLUMNS` is a subset of the loaded columns and that `date` parses, raising `ValueError` with a plain-English message otherwise. No deeper validation (no null/negative checks) — this is a fixed, known sample file for Phase 1.
- The four calculation functions are pure (no I/O, no Streamlit) — same input always gives same output — which is what makes them cheap to unit test against a small fixture instead of the real CSV.
- Sort order for category/region lives here, not in `app.py`, so chart code just plots whatever order it receives.
- Assumption: one CSV row = one order/transaction (`total_orders` counts rows, not distinct `order_id`s). The PRD's expected value (482 orders = 482 records) and data spec support this; there's no indication of multi-line orders sharing an `order_id`.

## `app.py` — UI layer

**Layout (top to bottom):**
1. `st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")` + page title
2. Two-column KPI row: `st.metric("Total Sales", ...)` / `st.metric("Total Orders", ...)`
3. Full-width line chart: daily sales trend (`sales_by_day`)
4. Two-column row: category bar chart (`sales_by_category`) | region bar chart (`sales_by_region`)

**Data loading:** `analytics.load_sales_data("data/sales-data.csv")` is called once at the top of `app.py`, wrapped in `@st.cache_data` so Streamlit doesn't re-read/re-parse the CSV on every widget interaction. This directly serves NFR-1's 5-second load target at negligible cost given the file's size (482 rows).

**Error handling:** The `load_sales_data` call is wrapped in `try/except ValueError`; on failure, show `st.error(str(e))` and `st.stop()` instead of a raw traceback. This is the only place a real failure can occur — everything downstream of a successful load is pure pandas/Plotly and won't raise under normal conditions.

**Chart colors:** All three charts (line + two bars) use a single accent hue, `#2a78d6`, rather than a different color per bar/category. Each chart plots one measure against one categorical/temporal axis, and the axis labels already carry identity, so per-category coloring would be redundant rather than informative, and it avoids needing a legend where none is needed. One hex constant, no color-mapping dict.

**Tooltips:** Plotly's default hover already provides interactive per-point/per-bar tooltips (satisfies FR-2/3/4). Each trace sets a `hovertemplate` so values render as `$X,XXX` instead of Plotly's raw float default.

**Formatting:** A small helper in `app.py` (not `analytics.py` — presentation, not calculation) formats floats as `$X,XXX` for KPI cards and chart hover text, per FR-1.

**Trend chart granularity:** Daily (not monthly) — decided in brainstorming.

## Testing (`tests/test_analytics.py`)

- A synthetic fixture: an 8-10 row DataFrame (or CSV string) spanning ≥2 categories, ≥2 regions, and multiple dates, with `total_amount` values chosen so expected sums are easy to hand-verify. No test touches the real `data/sales-data.csv`, keeping tests fast and independent of that file.
- One test per calculation function:
  - `test_total_sales` — sum matches hand-computed total
  - `test_total_orders` — count matches row count
  - `test_sales_by_day` — per-day sums correct, sorted by date
  - `test_sales_by_category` — per-category sums correct, sorted descending by total_amount
  - `test_sales_by_region` — per-region sums correct, sorted descending by total_amount
- `test_load_sales_data_missing_column` — a DataFrame/CSV missing a required column raises `ValueError`.

## Dev environment

- `python3 -m venv venv` at repo root; activate with `source venv/bin/activate` (plain venv, no uv/conda, per ground rules).
- `requirements.txt` pins exactly: `streamlit`, `pandas`, `plotly`, `pytest`.
- `.streamlit/config.toml` sets `primaryColor = "#2a78d6"` (matches the chart accent) on Streamlit's default light theme — no custom CSS.
- `venv/` is already present in `.gitignore`.

## Out of scope (per PRD Phase 2)

User auth, real-time DB integration, export, email alerts, filtering/date range selection, drill-down, mobile-responsive design. Deployment to Streamlit Community Cloud (TASK-7) is planned but executed by the user, not part of this implementation's automated steps.
