# %%
import pandas as pd
import streamlit as st
import plotly.express as px


# Load your emissions data
df = pd.read_csv("Empreinte carbone anonymous 2023.csv")  # Example: columns = ['Year', 'Category', 'Emissions_tCO2e']

# Sidebar filters
year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))
category = st.sidebar.multiselect("Select Categories", df['Catégorie Bilan Carbone'].unique(), default=df['Catégorie Bilan Carbone'].unique())

# Filter data
filtered_df = df[(df['Year'] == year) & (df['Catégorie Bilan Carbone'].isin(category))]

# Display data
st.title("GHG Emissions Dashboard")
st.subheader(f"Total Emissions in {year}")
st.metric(label="Total Emissions (tCO2e)", value=round(filtered_df['GHG Emissions (kgCO2e)'].sum(), 2))

# Plot with subcategories
fig = px.bar(
    filtered_df,
    x="Catégorie Bilan Carbone",
    y="GHG Emissions (kgCO2e)",
    color="Sous-Catégorie Bilan Carbone",
    title="Emissions by Category and Subcategory",
    labels={"GHG Emissions (kgCO2e)": "Emissions (kgCO2e)"},
)

fig.update_layout(barmode='stack')  # or 'group' if you prefer grouped bars
st.plotly_chart(fig)
