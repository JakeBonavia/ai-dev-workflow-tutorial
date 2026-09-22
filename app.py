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

def format_currency(value: float) -> str:
    return f"${value:,.0f}"


col1, col2 = st.columns(2)
col1.metric("Total Sales", format_currency(analytics.total_sales(sales_df)))
col2.metric("Total Orders", f"{analytics.total_orders(sales_df):,}")
