# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the ShopSmart Streamlit sales dashboard (KPI cards, trend chart, category/region breakdowns) reading `data/sales-data.csv`.

**Architecture:** Two modules — `analytics.py` (pure, pytest-tested data-loading and calculation functions, no Streamlit/Plotly imports) and `app.py` (the Streamlit page: layout, caching, error handling, and Plotly chart rendering). `analytics.py` is built and tested function-by-function; `app.py` is extended incrementally as each function becomes available.

**Tech Stack:** Python 3, Streamlit, Pandas, Plotly, pytest. Plain `venv/` virtualenv (no uv/conda).

**Spec:** `docs/superpowers/specs/2026-09-22-ecommerce-analytics-dashboard-design.md`

**Plan-task numbering note:** This plan's own tasks are numbered **Plan Task 1–7**, listed under the `## Plan Task N` headings below. Each one also carries a **Milestone:** line naming the `TASKS.md` milestone (`TASK-1`…`TASK-7`) it implements. These two numbering schemes are intentionally separate — a plan task's number and its milestone ID are never the same digit by coincidence; always refer to the milestone by its `TASK-N` label, never by the plan task number.

## Global Constraints

- Plain Python `venv/` virtualenv for dependencies — no uv, no conda.
- `requirements.txt` limited to: `streamlit`, `pandas`, `plotly`, `pytest`.
- All data loading/calculation logic lives in `analytics.py` only, covered by pytest tests in `tests/test_analytics.py`. `analytics.py` never imports `streamlit` or `plotly`.
- Every commit message must start with the `TASKS.md` milestone ID it completes (e.g. `TASK-3: ...`), per the Definition of Done in `TASKS.md`.
- Work happens on the already-checked-out `feature/sales-dashboard` branch. Do not create a git worktree.
- No classes for stateless computation — `analytics.py` functions are plain functions, not methods on a class (YAGNI, per the approved design).
- All charts (line + both bars) use a single accent color, `#2a78d6` — no per-category/per-region color mapping, no legend.
- Trend chart granularity is daily, not monthly.
- No test in `tests/test_analytics.py` reads the real `data/sales-data.csv` — all pytest tests use an in-memory synthetic fixture.

---

## Shared test fixture (used by Plan Tasks 2–5)

All of `tests/test_analytics.py`'s calculation tests share one fixture, defined once in Plan Task 2 and reused (not redefined) afterward:

```python
import pandas as pd
import pytest

SAMPLE_ROWS = [
    {"date": "2024-01-01", "order_id": "ORD-001", "product": "Widget A", "category": "Electronics", "region": "North", "quantity": 1, "unit_price": 100, "total_amount": 100},
    {"date": "2024-01-01", "order_id": "ORD-002", "product": "Widget B", "category": "Accessories", "region": "South", "quantity": 1, "unit_price": 50,  "total_amount": 50},
    {"date": "2024-01-02", "order_id": "ORD-003", "product": "Widget A", "category": "Electronics", "region": "South", "quantity": 1, "unit_price": 200, "total_amount": 200},
    {"date": "2024-01-02", "order_id": "ORD-004", "product": "Widget C", "category": "Audio",       "region": "North", "quantity": 1, "unit_price": 30,  "total_amount": 30},
    {"date": "2024-01-03", "order_id": "ORD-005", "product": "Widget B", "category": "Accessories", "region": "North", "quantity": 1, "unit_price": 70,  "total_amount": 70},
    {"date": "2024-01-03", "order_id": "ORD-006", "product": "Widget C", "category": "Audio",       "region": "South", "quantity": 1, "unit_price": 40,  "total_amount": 40},
    {"date": "2024-01-03", "order_id": "ORD-007", "product": "Widget A", "category": "Electronics", "region": "North", "quantity": 1, "unit_price": 150, "total_amount": 150},
    {"date": "2024-01-04", "order_id": "ORD-008", "product": "Widget B", "category": "Accessories", "region": "South", "quantity": 1, "unit_price": 60,  "total_amount": 60},
    {"date": "2024-01-04", "order_id": "ORD-009", "product": "Widget C", "category": "Audio",       "region": "North", "quantity": 1, "unit_price": 20,  "total_amount": 20},
    {"date": "2024-01-05", "order_id": "ORD-010", "product": "Widget A", "category": "Electronics", "region": "South", "quantity": 1, "unit_price": 80,  "total_amount": 80},
]

@pytest.fixture
def sample_df():
    df = pd.DataFrame(SAMPLE_ROWS)
    df["date"] = pd.to_datetime(df["date"])
    return df
```

Hand-verified expected values from this fixture (used directly in assertions):
- `total_sales` = 800, `total_orders` = 10
- By day (ascending): 01-01=150, 01-02=230, 01-03=260, 01-04=80, 01-05=80
- By category (descending): Electronics=530, Accessories=180, Audio=90
- By region (descending): South=430, North=370

---

## Plan Task 1

**Milestone:** TASK-1 — Environment setup and project initialization

**Files:**
- Create: `requirements.txt`
- Create: `app.py`
- Create: `.streamlit/config.toml`

**Interfaces:**
- Produces: a running (skeleton) `app.py` that Plan Task 2 extends.

- [ ] **Step 1: Create the virtualenv**

```bash
cd /Users/jakebonavia/Documents/ai-dev-workflow-tutorial
python3 -m venv venv
source venv/bin/activate
```

- [ ] **Step 2: Create `requirements.txt`**

```
streamlit
pandas
plotly
pytest
```

- [ ] **Step 3: Install dependencies**

```bash
source venv/bin/activate
pip install -r requirements.txt
```

Expected: all four packages install with no errors.

- [ ] **Step 4: Create `.streamlit/config.toml`**

```toml
[theme]
primaryColor = "#2a78d6"
base = "light"
```

- [ ] **Step 5: Create the `app.py` skeleton**

```python
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
st.write("Dashboard under construction.")
```

- [ ] **Step 6: Verify the app runs**

```bash
source venv/bin/activate
streamlit run app.py --server.headless true --server.port 8501 &
STREAMLIT_PID=$!
sleep 5
curl -sf http://localhost:8501 > /dev/null && echo "OK: app responded" || echo "FAIL: app did not respond"
kill $STREAMLIT_PID
```

Expected: `OK: app responded`.

- [ ] **Step 7: Confirm `venv/` is gitignored**

```bash
grep -n "^venv/$" .gitignore
```

Expected: a match (already present in this repo — no edit needed).

- [ ] **Step 8: Commit**

```bash
git add requirements.txt app.py .streamlit/config.toml
git commit -m "TASK-1: set up environment and project skeleton"
```

---

## Plan Task 2

**Milestone:** TASK-2 — Data loading and basic structure

**Files:**
- Create: `analytics.py`
- Create: `tests/test_analytics.py`
- Modify: `app.py` (extend the skeleton from Plan Task 1)

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `analytics.load_sales_data(path: str) -> pd.DataFrame`, raising `ValueError` on missing required columns. `REQUIRED_COLUMNS: set[str]` constant. The `sample_df` pytest fixture (above), which Plan Tasks 3–5 depend on.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_analytics.py` with the shared fixture block from "Shared test fixture" above, plus:

```python
def test_load_sales_data_valid(tmp_path):
    csv_path = tmp_path / "sales.csv"
    pd.DataFrame(SAMPLE_ROWS).to_csv(csv_path, index=False)

    df = analytics.load_sales_data(str(csv_path))

    assert len(df) == 10
    assert analytics.REQUIRED_COLUMNS.issubset(set(df.columns))
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_load_sales_data_missing_column(tmp_path):
    csv_path = tmp_path / "sales.csv"
    incomplete_rows = [{k: v for k, v in row.items() if k != "region"} for row in SAMPLE_ROWS]
    pd.DataFrame(incomplete_rows).to_csv(csv_path, index=False)

    with pytest.raises(ValueError):
        analytics.load_sales_data(str(csv_path))
```

Add `import analytics` at the top of the test file (alongside `pandas`/`pytest`).

- [ ] **Step 2: Run tests to verify they fail**

```bash
source venv/bin/activate
pytest tests/test_analytics.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'analytics'` (file doesn't exist yet).

- [ ] **Step 3: Implement `analytics.py`**

```python
import pandas as pd

REQUIRED_COLUMNS = {
    "date", "order_id", "product", "category", "region",
    "quantity", "unit_price", "total_amount",
}


def load_sales_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"sales data is missing required columns: {sorted(missing)}")

    try:
        df["date"] = pd.to_datetime(df["date"])
    except (ValueError, TypeError) as e:
        raise ValueError(f"sales data 'date' column could not be parsed: {e}")

    return df
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
source venv/bin/activate
pytest tests/test_analytics.py -v
```

Expected: PASS (2 tests).

- [ ] **Step 5: Wire data loading into `app.py`**

Replace the skeleton's `st.write("Dashboard under construction.")` line with:

```python
import streamlit as st
import analytics

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")


@st.cache_data
def get_sales_data():
    return analytics.load_sales_data("data/sales-data.csv")


try:
    sales_df = get_sales_data()
except ValueError as e:
    st.error(str(e))
    st.stop()

st.write(f"Loaded {len(sales_df)} sales records.")
```

(The `st.write` row-count line is temporary — Plan Task 3 replaces it with the real KPI cards.)

- [ ] **Step 6: Verify the app runs against the real CSV**

```bash
source venv/bin/activate
streamlit run app.py --server.headless true --server.port 8501 &
STREAMLIT_PID=$!
sleep 5
curl -sf http://localhost:8501 > /dev/null && echo "OK: app responded" || echo "FAIL: app did not respond"
kill $STREAMLIT_PID
```

Expected: `OK: app responded`, and no traceback in the terminal output above the curl check.

- [ ] **Step 7: Commit**

```bash
git add analytics.py tests/test_analytics.py app.py
git commit -m "TASK-2: add data loading module with validation and tests"
```

---

## Plan Task 3

**Milestone:** TASK-3 — KPI cards implementation

**Files:**
- Modify: `analytics.py` (add `total_sales`, `total_orders`)
- Modify: `tests/test_analytics.py` (add tests, reusing `sample_df`)
- Modify: `app.py` (add currency formatting + KPI cards, remove the temporary row-count line)

**Interfaces:**
- Consumes: `analytics.load_sales_data`, `sample_df` fixture (Plan Task 2).
- Produces: `analytics.total_sales(df: pd.DataFrame) -> float`, `analytics.total_orders(df: pd.DataFrame) -> int`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_analytics.py`:

```python
def test_total_sales(sample_df):
    assert analytics.total_sales(sample_df) == 800


def test_total_orders(sample_df):
    assert analytics.total_orders(sample_df) == 10
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
source venv/bin/activate
pytest tests/test_analytics.py -v -k "total_sales or total_orders"
```

Expected: FAIL — `AttributeError: module 'analytics' has no attribute 'total_sales'`.

- [ ] **Step 3: Implement the functions**

Append to `analytics.py`:

```python
def total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def total_orders(df: pd.DataFrame) -> int:
    return len(df)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
source venv/bin/activate
pytest tests/test_analytics.py -v
```

Expected: PASS (4 tests total so far).

- [ ] **Step 5: Add KPI cards to `app.py`**

Replace `st.write(f"Loaded {len(sales_df)} sales records.")` with:

```python
def format_currency(value: float) -> str:
    return f"${value:,.0f}"


col1, col2 = st.columns(2)
col1.metric("Total Sales", format_currency(analytics.total_sales(sales_df)))
col2.metric("Total Orders", f"{analytics.total_orders(sales_df):,}")
```

- [ ] **Step 6: Sanity-check against the real data**

```bash
source venv/bin/activate
python -c "
import analytics
df = analytics.load_sales_data('data/sales-data.csv')
print('total_sales:', analytics.total_sales(df))
print('total_orders:', analytics.total_orders(df))
"
```

Expected: `total_orders: 482`, `total_sales:` close to `116500` (PRD's "Expected Output" table — ~$116,500). This is a one-off manual check, not a permanent pytest test (per the design's "no test hits the real CSV" rule).

- [ ] **Step 7: Verify the app runs**

```bash
source venv/bin/activate
streamlit run app.py --server.headless true --server.port 8501 &
STREAMLIT_PID=$!
sleep 5
curl -sf http://localhost:8501 > /dev/null && echo "OK: app responded" || echo "FAIL: app did not respond"
kill $STREAMLIT_PID
```

Expected: `OK: app responded`.

- [ ] **Step 8: Commit**

```bash
git add analytics.py tests/test_analytics.py app.py
git commit -m "TASK-3: implement KPI cards for total sales and orders"
```

---

## Plan Task 4

**Milestone:** TASK-4 — Sales trend chart

**Files:**
- Modify: `analytics.py` (add `sales_by_day`)
- Modify: `tests/test_analytics.py` (add test, reusing `sample_df`)
- Modify: `app.py` (add the line chart)

**Interfaces:**
- Consumes: `sales_df`, `sample_df` fixture (Plan Task 2), KPI card layout (Plan Task 3).
- Produces: `analytics.sales_by_day(df: pd.DataFrame) -> pd.DataFrame` with columns `date`, `total_amount`, sorted ascending by `date`.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_analytics.py`:

```python
def test_sales_by_day(sample_df):
    result = analytics.sales_by_day(sample_df)

    assert list(result.columns) == ["date", "total_amount"]
    assert result["date"].is_monotonic_increasing
    assert result["total_amount"].tolist() == [150, 230, 260, 80, 80]
```

- [ ] **Step 2: Run test to verify it fails**

```bash
source venv/bin/activate
pytest tests/test_analytics.py -v -k sales_by_day
```

Expected: FAIL — `AttributeError: module 'analytics' has no attribute 'sales_by_day'`.

- [ ] **Step 3: Implement the function**

Append to `analytics.py`:

```python
def sales_by_day(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby(df["date"].dt.normalize())["total_amount"].sum().reset_index()
    return result.sort_values("date").reset_index(drop=True)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
source venv/bin/activate
pytest tests/test_analytics.py -v
```

Expected: PASS (5 tests total so far).

- [ ] **Step 5: Add the trend chart to `app.py`**

Add near the top (with the other imports):

```python
import plotly.graph_objects as go

ACCENT_COLOR = "#2a78d6"
```

Add below the KPI cards block:

```python
daily_sales = analytics.sales_by_day(sales_df)

trend_fig = go.Figure(
    go.Scatter(
        x=daily_sales["date"],
        y=daily_sales["total_amount"],
        mode="lines",
        line=dict(color=ACCENT_COLOR, width=2),
        hovertemplate="%{x|%b %d, %Y}<br>$%{y:,.0f}<extra></extra>",
    )
)
trend_fig.update_layout(title="Sales Trend Over Time", xaxis_title="Date", yaxis_title="Sales")
st.plotly_chart(trend_fig, use_container_width=True)
```

- [ ] **Step 6: Verify the app runs**

```bash
source venv/bin/activate
streamlit run app.py --server.headless true --server.port 8501 &
STREAMLIT_PID=$!
sleep 5
curl -sf http://localhost:8501 > /dev/null && echo "OK: app responded" || echo "FAIL: app did not respond"
kill $STREAMLIT_PID
```

Expected: `OK: app responded`.

- [ ] **Step 7: Commit**

```bash
git add analytics.py tests/test_analytics.py app.py
git commit -m "TASK-4: add sales trend line chart"
```

---

## Plan Task 5

**Milestone:** TASK-5 — Category and region breakdowns

**Files:**
- Modify: `analytics.py` (add `sales_by_category`, `sales_by_region`)
- Modify: `tests/test_analytics.py` (add tests, reusing `sample_df`)
- Modify: `app.py` (add the two bar charts)

**Interfaces:**
- Consumes: `sales_df`, `sample_df` fixture (Plan Task 2), `ACCENT_COLOR` (Plan Task 4).
- Produces: `analytics.sales_by_category(df) -> pd.DataFrame` (columns `category`, `total_amount`, sorted descending), `analytics.sales_by_region(df) -> pd.DataFrame` (columns `region`, `total_amount`, sorted descending).

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_analytics.py`:

```python
def test_sales_by_category(sample_df):
    result = analytics.sales_by_category(sample_df)

    assert list(result.columns) == ["category", "total_amount"]
    assert result["category"].tolist() == ["Electronics", "Accessories", "Audio"]
    assert result["total_amount"].tolist() == [530, 180, 90]


def test_sales_by_region(sample_df):
    result = analytics.sales_by_region(sample_df)

    assert list(result.columns) == ["region", "total_amount"]
    assert result["region"].tolist() == ["South", "North"]
    assert result["total_amount"].tolist() == [430, 370]
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
source venv/bin/activate
pytest tests/test_analytics.py -v -k "sales_by_category or sales_by_region"
```

Expected: FAIL — `AttributeError: module 'analytics' has no attribute 'sales_by_category'`.

- [ ] **Step 3: Implement the functions**

Append to `analytics.py`:

```python
def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("category")["total_amount"].sum().reset_index()
    return result.sort_values("total_amount", ascending=False).reset_index(drop=True)


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("region")["total_amount"].sum().reset_index()
    return result.sort_values("total_amount", ascending=False).reset_index(drop=True)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
source venv/bin/activate
pytest tests/test_analytics.py -v
```

Expected: PASS (7 tests total so far).

- [ ] **Step 5: Add the bar charts to `app.py`**

Add below the trend chart:

```python
category_sales = analytics.sales_by_category(sales_df)
region_sales = analytics.sales_by_region(sales_df)

col3, col4 = st.columns(2)

with col3:
    category_fig = go.Figure(
        go.Bar(
            x=category_sales["category"],
            y=category_sales["total_amount"],
            marker_color=ACCENT_COLOR,
            hovertemplate="%{x}<br>$%{y:,.0f}<extra></extra>",
        )
    )
    category_fig.update_layout(title="Sales by Category", xaxis_title="Category", yaxis_title="Sales")
    st.plotly_chart(category_fig, use_container_width=True)

with col4:
    region_fig = go.Figure(
        go.Bar(
            x=region_sales["region"],
            y=region_sales["total_amount"],
            marker_color=ACCENT_COLOR,
            hovertemplate="%{x}<br>$%{y:,.0f}<extra></extra>",
        )
    )
    region_fig.update_layout(title="Sales by Region", xaxis_title="Region", yaxis_title="Sales")
    st.plotly_chart(region_fig, use_container_width=True)
```

- [ ] **Step 6: Verify the app runs**

```bash
source venv/bin/activate
streamlit run app.py --server.headless true --server.port 8501 &
STREAMLIT_PID=$!
sleep 5
curl -sf http://localhost:8501 > /dev/null && echo "OK: app responded" || echo "FAIL: app did not respond"
kill $STREAMLIT_PID
```

Expected: `OK: app responded`.

- [ ] **Step 7: Commit**

```bash
git add analytics.py tests/test_analytics.py app.py
git commit -m "TASK-5: add category and region bar charts"
```

---

## Plan Task 6

**Milestone:** TASK-6 — Testing and refinement

**Files:**
- Modify (if issues found): `app.py`, `analytics.py`

**Interfaces:**
- Consumes: everything built in Plan Tasks 1–5. No new interfaces produced.

- [ ] **Step 1: Run the full test suite**

```bash
source venv/bin/activate
pytest tests/test_analytics.py -v
```

Expected: PASS (7/7 tests).

- [ ] **Step 2: Sanity-check computed values against the PRD's expected output**

```bash
source venv/bin/activate
python -c "
import analytics
df = analytics.load_sales_data('data/sales-data.csv')
print('Total Sales:', analytics.total_sales(df))
print('Total Orders:', analytics.total_orders(df))
print('Top Category:', analytics.sales_by_category(df).iloc[0]['category'])
print('Regions:', analytics.sales_by_region(df)['region'].tolist())
"
```

Expected, per the PRD's "Expected Output" table: Total Sales ≈ 116500, Total Orders = 482, Top Category = Electronics, Regions = the four values North/South/East/West (any order).

- [ ] **Step 3: Full-page smoke test with server logs checked for errors**

```bash
source venv/bin/activate
streamlit run app.py --server.headless true --server.port 8501 > /tmp/streamlit_log.txt 2>&1 &
STREAMLIT_PID=$!
sleep 5
curl -sf http://localhost:8501 > /dev/null && echo "OK: app responded" || echo "FAIL: app did not respond"
kill $STREAMLIT_PID
grep -i "traceback\|error" /tmp/streamlit_log.txt && echo "FOUND ERRORS ABOVE" || echo "OK: no errors in server log"
```

Expected: `OK: app responded` and `OK: no errors in server log`.

- [ ] **Step 4: Manual visual review**

```bash
source venv/bin/activate
streamlit run app.py
```

Open the printed local URL in a browser. Compare against the PRD's "Dashboard Layout" mockup and "Acceptance Criteria" checklist (KPIs visible, trend chart correct, category/region charts sorted correctly, no errors, professional appearance). Stop the server (Ctrl+C) when done.

- [ ] **Step 5: Fix any issues found, then commit**

If Steps 1–4 surfaced any issues, fix them in `app.py`/`analytics.py`, re-run Steps 1–4, then commit:

```bash
git add -A
git commit -m "TASK-6: testing and refinement"
```

If no issues were found, no commit is needed for this milestone — note in `TASKS.md`'s `TASK-6` row that verification passed with no code changes required.

---

## Handoff: TASK-7 — Deployment (executed by you, not by this plan)

This plan stops here. Per your instructions, deployment is yours to run manually, from `main`, after this branch is merged. **Do not attempt any of the following as part of plan execution.**

Once `feature/sales-dashboard` is merged to `main` (PR review, merge — outside this plan's scope):

1. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo, pointing at `app.py` on the `main` branch.
2. Confirm `requirements.txt` is at the repo root (it is) so Streamlit Community Cloud can install dependencies.
3. Deploy and get the public URL.
4. Verify the deployed app loads and matches what you saw locally in Plan Task 6, Step 4.
5. Fill in `TASKS.md`'s `TASK-7` acceptance criteria and `Commit:` line (the deploy itself isn't a commit, but note the PR/merge commit that shipped it) and move `TASK-7` to Done.

This satisfies NFR-5 (Streamlit Community Cloud deployment, publicly accessible via shareable URL) from the PRD.
