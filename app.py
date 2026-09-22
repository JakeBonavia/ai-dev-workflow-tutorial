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
