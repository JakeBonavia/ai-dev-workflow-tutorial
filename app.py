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
