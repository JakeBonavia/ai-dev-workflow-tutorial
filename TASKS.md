# Tasks

This file tracks all work for the ShopSmart e-commerce analytics dashboard, based on `prd/ecommerce-analytics.md`.

## Definition of Done

- Acceptance criteria for the milestone are met
- App runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message

## To Do

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the finished dashboard so it is publicly accessible via a shareable URL.
- [ ] App is deployed to Streamlit Community Cloud
- [ ] Public URL loads the dashboard correctly with no errors
- [ ] URL is documented for stakeholder review

Commit:

## In Progress

## Done

### TASK-1: Environment setup and project initialization
Set up the Python project structure, dependencies, and Streamlit skeleton app.
- [x] `requirements.txt` includes Streamlit, Pandas, and Plotly
- [x] `app.py` exists and runs with `streamlit run app.py` showing a placeholder page
- [x] Project folder structure includes a `data/` directory for `sales-data.csv`

Commit: ec38018

### TASK-2: Data loading and basic structure
Load `sales-data.csv` into a Pandas DataFrame and validate its structure.
- [x] CSV loads without errors and columns match the spec (date, order_id, product, category, region, quantity, unit_price, total_amount)
- [x] Date column is parsed as a proper date type
- [x] Loaded row count matches the expected 482 records

Commit: 5d7d07e

### TASK-3: KPI cards implementation
Display Total Sales and Total Orders as KPI cards at the top of the dashboard.
- [x] Total Sales is calculated correctly and formatted as currency (e.g. $116,500)
- [x] Total Orders shows the correct transaction count (482)
- [x] KPI cards are displayed prominently at the top of the page

Commit: 9d74ea1

### TASK-4: Sales trend chart
Build a line chart showing sales over time.
- [x] Line chart renders with time on the x-axis and sales amount on the y-axis
- [x] Chart includes interactive tooltips showing exact values
- [x] Chart data matches the underlying CSV aggregation

Commit: 8890242

### TASK-5: Category and region breakdowns
Build bar charts showing sales by category and by region.
- [x] Category bar chart shows all 5 categories, sorted highest to lowest, with tooltips
- [x] Region bar chart shows all 4 regions, sorted highest to lowest, with tooltips
- [x] Both charts are placed side by side on the dashboard

Commit: 8eca7e2

### TASK-6: Testing and refinement
Verify the dashboard meets all Phase 1 acceptance criteria and polish the layout.
- [x] All values (KPIs, chart data) match expected calculations from the CSV
- [x] Dashboard runs with no errors or warnings and loads within 5 seconds
- [x] Layout and labels look professional and suitable for an executive presentation

Commit: No code changes required — verified in session (pytest 7/7 passing, values matched PRD's expected output, user confirmed visual review in browser)
