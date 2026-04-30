import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.header("Interactive Sales Dashboard")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("Online Sales Data.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")

region_filter = st.sidebar.multiselect(
    "Select Region or Regions",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

product_filter = st.sidebar.multiselect(
    "Select Products",
    options=sorted(df["Product Category"].dropna().unique()),
    default=sorted(df["Product Category"].dropna().unique())
)

# Filter data
filtered_df = df[
    (df["Region"].isin(region_filter)) &
    (df["Product Category"].isin(product_filter))
]

# Show selections
st.markdown(
    f"##### Region Selected: {', '.join(region_filter) if region_filter else 'None'}\n"
    f"##### Product Selected: {', '.join(product_filter) if product_filter else 'None'}"
)

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# Metrics
col1, col2 = st.columns(2)

with col1:
    total_sales = filtered_df["Total Revenue"].sum()
    st.metric("Total Revenue", f"${total_sales:,.2f}")

with col2:
    average_sales = filtered_df["Total Revenue"].mean()
    st.metric("Average Revenue", f"${average_sales:,.2f}")

# Tabs
tab1, tab2 = st.tabs(["Sales by Product", "Sales by Region"])

with tab1:
    st.subheader("Sales by Product")
    product_data = (
        filtered_df.groupby("Product Category", as_index=False)["Total Revenue"]
        .sum()
        .sort_values("Total Revenue", ascending=False)
    )

    figure1 = px.bar(
        product_data,
        x="Product Category",
        y="Total Revenue",
        color="Product Category",
        text="Total Revenue",
        title="Sales by Product"
    )
    figure1.update_traces(texttemplate="$%{text:,.2f}", textposition="outside")
    figure1.update_layout(xaxis_title="Product Category", yaxis_title="Total Revenue")
    st.plotly_chart(figure1, use_container_width=True)

with tab2:
    st.subheader("Sales by Region")
    region_data = (
        filtered_df.groupby("Region", as_index=False)["Total Revenue"]
        .sum()
        .sort_values("Total Revenue", ascending=False)
    )

    figure2 = px.pie(
        region_data,
        names="Region",
        values="Total Revenue",
        title="Sales by Region"
    )
    figure2.update_traces(textinfo="percent+label")
    st.plotly_chart(figure2, use_container_width=True)

