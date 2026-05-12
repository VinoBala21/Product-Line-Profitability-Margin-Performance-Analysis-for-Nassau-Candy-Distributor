import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(page_title="Product Profitability Dashboard", layout="wide")

st.title(" Nassau Candy Distributor")

# --------------------------------------------------
# LOAD DATA FUNCTION
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Nassau_Candy_Distributor.csv")

    # Convert date columns
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

    # KPI Calculations
    df['Gross Margin %'] = (df['Gross Profit'] / df['Sales']) * 100
    df['Profit per Unit'] = df['Gross Profit'] / df['Units']
    df['Profit per Unit'] = df['Profit per Unit'].fillna(0)

    # Contribution KPIs
    df['Revenue Contribution %'] = df['Sales'] / df['Sales'].sum() * 100
    df['Profit Contribution %'] = df['Gross Profit'] / df['Gross Profit'].sum() * 100

    # Margin Volatility
    volatility = df.groupby('Product Name')['Gross Margin %'].std().reset_index()
    volatility.columns = ['Product Name', 'Margin Volatility']

    df = df.merge(volatility, on='Product Name', how='left')

    return df

df = load_data()



# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

date_range = st.sidebar.date_input(
    "Date Range",
    [df['Order Date'].min(), df['Order Date'].max()]
)

division = st.sidebar.multiselect(
    "Division",
    df['Division'].unique(),
    default=df['Division'].unique()
)

margin = st.sidebar.slider("Margin Threshold (%)", 0, 100, 10)

product = st.sidebar.text_input("Product Search")

risk_threshold = st.sidebar.slider("Risk Margin Threshold", 0, 50, 15)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------
filtered = df[
    (df['Order Date'] >= pd.to_datetime(date_range[0])) &
    (df['Order Date'] <= pd.to_datetime(date_range[1])) &
    (df['Division'].isin(division)) &
    (df['Gross Margin %'] >= margin)
]

if product:
    filtered = filtered[filtered['Product Name'].str.contains(product, case=False)]

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------


k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Sales", f"${filtered['Sales'].sum():,.0f}")
k2.metric("Total Profit", f"${filtered['Gross Profit'].sum():,.0f}")
k3.metric("Average Gross Margin (%)", f"{filtered['Gross Margin %'].mean():.2f}")
k4.metric("Profit per Unit", f"{filtered['Profit per Unit'].mean():.2f}")


# --------------------------------------------------
# PRODUCT PROFITABILITY
# --------------------------------------------------
st.markdown("## Product Profitability Overview")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Product Margin Leaderboard")

    leaderboard = filtered.groupby('Product Name').agg({
        'Gross Profit': 'sum',
        'Gross Margin %': 'mean'
    }).sort_values(by='Gross Margin %', ascending=False).head(10)

    st.dataframe(leaderboard)

with col2:
    st.subheader("Top Products by Profit")

    top_profit = filtered.groupby('Product Name')['Gross Profit'].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots()
    top_profit.plot(kind='bar', ax=ax)
    st.pyplot(fig)

# --------------------------------------------------
# DIVISION PERFORMANCE
# --------------------------------------------------
st.markdown("## Division Performance Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue vs Profit")

    division_summary = filtered.groupby('Division')[['Sales', 'Gross Profit']].sum()

    fig, ax = plt.subplots()
    division_summary.plot(kind='bar', ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Margin Distribution")

    fig, ax = plt.subplots()
    sns.boxplot(data=filtered, x='Division', y='Gross Margin %', ax=ax)
    st.pyplot(fig)

# --------------------------------------------------
# COST DIAGNOSTICS
# --------------------------------------------------
st.markdown("## Cost vs Margin Diagnostics")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Cost vs Sales Scatter Plot")

    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered, x='Sales', y='Cost', ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Margin Risk Flags")

    risk = filtered[filtered['Gross Margin %'] < risk_threshold]

    if risk.empty:
        st.success("All products meet the selected margin threshold")
    else:
        st.dataframe(risk[['Product Name', 'Sales', 'Gross Profit', 'Gross Margin %']])

# --------------------------------------------------
# PARETO ANALYSIS
# --------------------------------------------------
import plotly.graph_objects as go

st.markdown("## Profit Concentration Analysis")

pareto = filtered.groupby('Product Name')['Sales'].sum().sort_values(ascending=False)
pareto_df = pareto.reset_index()
pareto_df['Cumulative %'] = (pareto_df['Sales'].cumsum() / pareto_df['Sales'].sum() * 100).round(2)

fig = go.Figure()
fig.add_trace(go.Bar(x=pareto_df['Product Name'], y=pareto_df['Sales'], name='Sales', marker_color='#3498db', yaxis='y1'))
fig.add_trace(go.Scatter(x=pareto_df['Product Name'], y=pareto_df['Cumulative %'], name='Cumulative %', mode='lines+markers', line=dict(color='#e74c3c', width=3), yaxis='y2'))
fig.update_layout(
    title='Pareto 80/20',
    yaxis=dict(title='Sales ($)'),
    yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 115]),
    height=450,
    xaxis=dict(tickangle=-35)
)
fig.add_hline(y=80, line_dash="dash", line_color="orange", annotation_text="80%", secondary_y=True)
st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------
# DEPENDENCY INDICATORS
# --------------------------------------------------
st.markdown("## Dependency Indicators")

top_80_count = (pareto_df['Cumulative %'] <= 80).sum()

d1, d2 = st.columns(2)

d1.metric("Products contributing to 80% Sales", top_80_count)
d2.metric("Total Products", len(pareto_df))