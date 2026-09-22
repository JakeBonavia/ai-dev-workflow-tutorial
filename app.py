import streamlit as st
import plotly.graph_objects as go

import analytics

ACCENT_COLOR = "#2a78d6"

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

def format_currency(value: float) -> str:
    return f"${value:,.0f}"


col1, col2 = st.columns(2)
col1.metric("Total Sales", format_currency(analytics.total_sales(sales_df)))
col2.metric("Total Orders", f"{analytics.total_orders(sales_df):,}")

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
