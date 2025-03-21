# %%
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Load emissions data
df = pd.read_csv("Empreinte carbone anonymous 2023.csv")  # Columns: ['Year', 'Catégorie Bilan Carbone', 'Sous-Catégorie Bilan Carbone', 'ModelID', 'GHG Emissions (kgCO2e)']

# Load decarbonization actions data
actions_df = pd.read_csv("BC_trajectory_anonymous.csv")  # Columns: ['Year', 'Solution', 'GHG Emissions reduction compared to no action (kgCO2e)']

# Sidebar filters
year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))
category = st.sidebar.multiselect("Select Categories", df['Catégorie Bilan Carbone'].unique(), default=df['Catégorie Bilan Carbone'].unique())

# Filter data
filtered_df = df[(df['Year'] == year) & (df['Catégorie Bilan Carbone'].isin(category))]

# Display data
st.title("GHG Emissions Dashboard")
st.subheader(f"Total Emissions in {year}")
st.metric(label="Total Emissions (tCO2e)", value=round(filtered_df['GHG Emissions (kgCO2e)'].sum(), 2))

# Bar chart: Emissions by Category and Subcategory
fig = px.bar(
    filtered_df,
    x="Catégorie Bilan Carbone",
    y="GHG Emissions (kgCO2e)",
    color="Sous-Catégorie Bilan Carbone",
    title="Emissions by Category and Subcategory",
    labels={"GHG Emissions (kgCO2e)": "Emissions (kgCO2e)"},
)
fig.update_layout(barmode='stack')
st.plotly_chart(fig)

# Treemap: Category > Subcategory > ModelID
st.subheader("Drill-down Treemap: Category → Subcategory → ModelID")
fig_treemap = px.treemap(
    filtered_df,
    path=["Catégorie Bilan Carbone", "Sous-Catégorie Bilan Carbone", "ModelID"],
    values="GHG Emissions (kgCO2e)",
    title="Hierarchical View of Emissions",
)
st.plotly_chart(fig_treemap)

# Waterfall Chart: Impact of Decarbonization Actions
st.subheader("Decarbonization Impact by 2030")
actions_2030 = actions_df[actions_df['Year'] == 2030]

data = [
    go.Waterfall(
        name="GHG Reduction Actions",
        orientation="v",
        measure=["absolute"] + ["relative"] * (len(actions_2030) - 1) + ["absolute"],
        x=["Baseline Emissions"] + actions_2030["Solution"].tolist() + ["Projected Emissions"],
        y=[0] + actions_2030["GHG Emissions reduction compared to no action (kgCO2e)"].tolist() + [sum(actions_2030["GHG Emissions reduction compared to no action (kgCO2e)"])],
        textposition="outside",
        connector=dict(line=dict(color="rgb(63, 63, 63)"))
    )
]

fig_waterfall = go.Figure(data)
fig_waterfall.update_layout(
    title="GHG Reduction from Actions (2030)",
    xaxis_title="Actions",
    yaxis_title="Emissions Reduction (kgCO2e)",
)
st.plotly_chart(fig_waterfall)
