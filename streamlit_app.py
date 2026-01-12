import streamlit as st
import pandas as pd

# Set up the page
st.set_page_config(page_title="School Energy Dashboard", layout="wide")
st.title("🏫 School Energy Consumption Dashboard")

# 1. Initialize connection to Azure SQL
conn = st.connection(name="sql", type="sql")

# 2. Query the Demo_Energy table
@st.cache_data(ttl=600)
def get_all_data():
    query = "SELECT * FROM Demo_Energy ORDER BY building_name, month"
    df = conn.query(query)
    return df

df = get_all_data()

# Display raw data
with st.expander("View Raw Data"):
    st.dataframe(df)

# Sidebar for user interaction
st.sidebar.header("Filters")
selected_building = st.sidebar.selectbox(
    "Choose a School:",
    options=df['building_name'].unique()
)

# Filter data based on selection
filtered_df = df[df['building_name'] == selected_building]

# Create two columns for the charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Monthly Electricity Consumption")
    chart_df_line = filtered_df[['month', 'electricity_kwh']].copy()
    chart_df_line.set_index('month', inplace=True)
    st.line_chart(chart_df_line)

with col2:
    st.subheader("📊 Monthly Cost Breakdown")
    chart_df_bar = filtered_df[['month', 'cost']].copy()
    chart_df_bar.set_index('month', inplace=True)
    st.bar_chart(chart_df_bar)

# Summary metric
total_cost = filtered_df['cost'].sum()
st.metric(label=f"Total Cost for {selected_building} (Period)", value=f"\${total_cost:,.0f}")
