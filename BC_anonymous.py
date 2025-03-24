# %%
import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit_authenticator as stauth
import plotly.graph_objects as go

# Hashed password generated from helper script
hashed_passwords = [
    'password123'  # hash of 'password123'
]

# User credentials
credentials = {
    'usernames': {
        'jane': {
            'name': 'Jane',
            'password': hashed_passwords[0]
        }
    }
}

# Authenticator setup
authenticator = stauth.Authenticate(
    credentials,
    "ghg_dashboard",  # Cookie name
    "abcdef",         # Signature key
    cookie_expiry_days=1
)

# Login
authenticator.login(location='main')

# Check authentication status
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')

        # -------- Dashboard Code --------
        # Load emissions data
    df = pd.read_csv("Empreinte carbone anonymous 2023.csv")
    actions_df = pd.read_csv("BC_trajectory_anonymous.csv")

    # Sidebar filters
    year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))
    category = st.sidebar.multiselect("Select Categories", df['Catégorie Bilan Carbone'].unique(), default=df['Catégorie Bilan Carbone'].unique())

    # Filter data
    filtered_df = df[(df['Year'] == year) & (df['Catégorie Bilan Carbone'].isin(category))]

    # Create Tabs
    tab1, tab2 = st.tabs(["📊 Dashboard", "📁 Raw Data & Extra Insights"])

    # TAB 1 - Main Dashboard
    with tab1:
        st.title("GHG Emissions Dashboard")
        st.subheader(f"Total Emissions in {year}")
        st.metric(label="Total Emissions (tCO2e)", value=round(filtered_df['GHG Emissions (kgCO2e)'].sum(), 2))

        # Bar Chart
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

        # Treemap
        st.subheader("Drill-down Treemap: Category → Subcategory → ModelID")
        fig_treemap = px.treemap(
            filtered_df,
            path=["Catégorie Bilan Carbone", "Sous-Catégorie Bilan Carbone", "ModelID"],
            values="GHG Emissions (kgCO2e)",
            title="Hierarchical View of Emissions",
        )
        st.plotly_chart(fig_treemap)

        # Waterfall
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

    # TAB 2 - Raw Data & Extra Insights
    with tab2:
        st.title("Explore the Data")
        st.subheader("Filtered Emissions Data")
        st.dataframe(filtered_df)

        st.subheader("Decarbonization Actions (All Years)")
        st.dataframe(actions_df)

    

elif st.session_state["authentication_status"] is False:
    st.error("Username or password is incorrect")

elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")
