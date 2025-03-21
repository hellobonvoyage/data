# %%
import pandas as pd
import streamlit as st
import plotly.express as px

# Load your emissions data
df = pd.read_csv("Empreinte carbone anonymous 2023.csv")  # Columns: ['Year', 'Catégorie Bilan Carbone', 'Sous-Catégorie Bilan Carbone', 'ModelID', 'GHG Emissions (kgCO2e)']

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
fig.update_layout(barmode='stack')  # or 'group'
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
