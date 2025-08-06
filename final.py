import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("final_dataset.csv")

# Add title to sidebar
st.sidebar.markdown("### 📊 Education & Economic Growth")
st.sidebar.markdown("A dashboard exploring how education influences economy 🌍")



# Set up the Streamlit app with pages
st.set_page_config(page_title="Education & Economic Growth", layout="wide")

# Page selection
page = st.sidebar.radio("Select Page", ["Home", "Insights"])

if page == "Home":
    st.title("📊 Education & Economic Growth Dashboard")

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Countries", df.shape[0])

    most_gdp_continent = df.groupby("Continent")['GDP per Capita (Current USD)'].mean().idxmax()
    k2.metric("Top Continent by GDP per Capita", most_gdp_continent)

    least_unemp_country = df.loc[df['Unemployment Rate (%)'].idxmin()]['Country']
    k3.metric("Lowest Unemployment Rate", least_unemp_country)

    count_100_lit = (df['Literacy Rate'] == 100).sum()
    k4.metric("Countries with 100% Literacy", count_100_lit)

    # Filters
    st.sidebar.header("Filters")
    selected_continent = st.sidebar.selectbox("Continent", [None] + sorted(df['Continent'].dropna().unique().tolist()))
    selected_country = st.sidebar.selectbox("Country", [None] + sorted(df['Country'].dropna().unique().tolist()))
    selected_gdp_cat = st.sidebar.selectbox("GDP Category", [None] + sorted(df['GDP per Capita Category'].dropna().unique().tolist()))

    filtered_df = df.copy()
    if selected_continent:
        filtered_df = filtered_df[filtered_df['Continent'] == selected_continent]
    if selected_country:
        filtered_df = filtered_df[filtered_df['Country'] == selected_country]
    if selected_gdp_cat:
        filtered_df = filtered_df[filtered_df['GDP per Capita Category'] == selected_gdp_cat]

    # Scatter Plot
    st.subheader("Literacy Rate vs GDP (Current USD)")
    fig1 = px.scatter(
        filtered_df,
        x="Literacy Rate",
        y="GDP (Current USD)",
        color="Continent",
        hover_name="Country",
        size="GDP (Current USD)",
        title="GDP vs Literacy Rate by Country"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Donut Charts per Continent (subplot)
    st.subheader("GDP per Capita Category Distribution by Continent")
    continents = df['Continent'].dropna().unique()
    donut_cols = st.columns(3)
    for i, cont in enumerate(continents):
        cont_data = df[df['Continent'] == cont]['GDP per Capita Category'].value_counts().reset_index()
        cont_data.columns = ['GDP Category', 'Count']
        with donut_cols[i % 3]:
            fig = px.pie(cont_data, names='GDP Category', values='Count', hole=0.5, title=cont)
            st.plotly_chart(fig, use_container_width=True)

    # Bar chart: Literacy & Unemployment by Continent
    st.subheader("Mean Literacy & Unemployment Rate by Continent")
    agg = df.groupby('Continent')[['Literacy Rate', 'Unemployment Rate (%)']].mean().reset_index()
    agg = agg.sort_values(by='Literacy Rate', ascending=False)
    fig2 = px.bar(agg, x='Continent', y=['Literacy Rate', 'Unemployment Rate (%)'], barmode='group')
    st.plotly_chart(fig2, use_container_width=True)

    # Heatmap
    st.subheader("Correlation Heatmap")
    heat_cols = ['Literacy Rate', 'Physician Density', 'GDP (Current USD)', 'GDP Growth (% Annual)',
                 'GDP per Capita (Current USD)', 'Unemployment Rate (%)']
    fig3, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(df[heat_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    st.pyplot(fig3)

elif page == "Insights":
    st.title("📈 Deeper Insights")

    # 1. Top 10 Countries by GDP
    st.subheader("Top 10 Countries by GDP (Current USD)")
    top_gdp = df.sort_values(by="GDP (Current USD)", ascending=False).head(10)
    fig4 = px.bar(top_gdp, x="Country", y="GDP (Current USD)", color="Country")
    st.plotly_chart(fig4, use_container_width=True)

    # 2. Top 10 Countries by Physician Density
    st.subheader("Top 10 Countries by Physician Density")
    top_phys = df.sort_values(by="Physician Density", ascending=False).head(10)
    fig5 = px.bar(top_phys, x="Country", y="Physician Density", color="Country")
    st.plotly_chart(fig5, use_container_width=True)

    # 3. Scatter Plot: Physician Density vs Unemployment
    st.subheader("Physician Density vs Unemployment Rate")
    fig6 = px.scatter(df, x="Physician Density", y="Unemployment Rate (%)", color="Continent",
                      hover_name="Country", size="Physician Density")
    st.plotly_chart(fig6, use_container_width=True)

    # 4. GDP of Countries with 100% Literacy Rate (Descending with GDP Category Labels)


df_100 = df[df['Literacy Rate'] == 100]


df_100_sorted = df_100.sort_values(by='GDP (Current USD)', ascending=False)


fig7 = px.bar(
    df_100_sorted,
    x='Country',
    y='GDP (Current USD)',
    color='GDP per Capita Category',
    text='GDP per Capita Category',
    title="GDP of Countries with 100% Literacy Rate "
)


fig7.update_traces(textposition='outside')
fig7.update_layout(
    xaxis_tickangle=45,
    xaxis={'categoryorder': 'total descending'}
)

st.plotly_chart(fig7, use_container_width=True)





