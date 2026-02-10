import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import base64

# ---------- Config ----------
st.set_page_config(page_title="Tourism Dashboard 🇮🇳", layout="wide")

# ---------- Background ----------
def set_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        div[data-testid="stAppViewContainer"] > .main {{
            background: rgba(255,255,255,0.8);
            backdrop-filter: blur(5px);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_from_local("india.jpg")

# ---------- Load Data ----------
@st.cache_data
def load_and_clean(path):
    df = pd.read_csv(path)
    df = df[df['Circle'] != 'Total'].copy()
    df.columns = [col.replace('-20', '20').replace('-19', '19') for col in df.columns]
    df['state'] = df['state'].astype(str).str.strip().str.title()
    df['TotalVisitors'] = df['Domestic19'] + df['Foreign19']
    for col in ['Domestic19','Foreign19','Domesticgrowth','Foreigngrowth']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(inplace=True)
    return df

df = load_and_clean("india2.csv")

# ---------- Title ----------
st.markdown("<h1 style='text-align:center;'>🌆 India Tourism Data Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#333;'>Explore tourism growth, popular destinations, and interactive insights.</p>", unsafe_allow_html=True)
st.success(f"✅ Data Loaded Successfully! Total Records: {len(df)}")

# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", "🏞️ State Analysis", "📈 Growth Trends", "🗺️ India Map", "🧭 Plan My Trip"
])

# --- Overview ---
with tab1:
    st.subheader("✨ Overview of Tourism Data")
    places_count = df.groupby('state')['Name of the Monument'].count().sort_values(ascending=False)
    plt.figure(figsize=(12, 5))
    sns.barplot(x=places_count.index, y=places_count.values, palette="Spectral")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt.gcf())
    plt.clf()
    st.info("🌍 Number of Tourist Places by State")

# --- State Analysis ---
with tab2:
    st.subheader("🏞️ State-wise Visitor Analysis")
    states = sorted(df['state'].unique())
    state = st.selectbox("Select a State:", states)
    subset = df[df['state'] == state]
    if not subset.empty:
        st.dataframe(subset[['Name of the Monument','Domestic19','Foreign19','Domesticgrowth','Foreigngrowth']])
        plot_data = subset[['Name of the Monument','Domestic19','Foreign19']].melt(
            id_vars='Name of the Monument', var_name='Visitor Type', value_name='Visitors')
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(data=plot_data, x='Visitors', y='Name of the Monument', hue='Visitor Type', palette='Set2')
        plt.title(f"Visitor Counts in {state}")
        st.pyplot(fig)
    else:
        st.warning("No data found for this state.")

# --- Growth Trends ---
with tab3:
    st.subheader("📈 Growth Trends (2019–2020)")
    growth = df.groupby('state')[['Domesticgrowth','Foreigngrowth']].mean().reset_index()
    growth_melt = growth.melt(id_vars='state', var_name='Type', value_name='Growth %')
    fig, ax = plt.subplots(figsize=(14,6))
    sns.barplot(data=growth_melt, x='state', y='Growth %', hue='Type', palette='coolwarm')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    st.info("💡 States with high growth rates are emerging destinations!")

# --- India Map ---
with tab4:
    st.subheader("🗺️ Interactive India Tourism Heatmap")

    # Use reliable GeoJSON file
    india_geojson = "https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson"

    # Aggregate visitors by state
    state_visitors = df.groupby('state')['TotalVisitors'].sum().reset_index()

    # Normalize state names for consistency
    state_visitors['state'] = state_visitors['state'].str.title().replace({
        'Andaman And Nicobar Islands': 'Andaman & Nicobar Islands',
        'Nct Of Delhi': 'Delhi',
        'Jammu And Kashmir': 'Jammu & Kashmir',
        'Odisha': 'Orissa',
        'Pondicherry': 'Puducherry'
    })

    # Create the choropleth map
    fig_map = px.choropleth(
        state_visitors,
        geojson=india_geojson,
        featureidkey="properties.NAME_1",  # Match property name in GeoJSON
        locations="state",
        color="TotalVisitors",
        color_continuous_scale="YlOrRd",
        title="Tourism Heatmap of India (Total Visitors 2019-2020)",
        hover_name="state"
    )

    fig_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map, use_container_width=True)
    st.info("🧭 Hover over each state to see total visitor counts!")


# --- Plan My Trip ---
with tab5:
    st.subheader("🧭 Plan My Trip")
    top_states = df.groupby('state')[['TotalVisitors','Domesticgrowth']].mean().sort_values(by='TotalVisitors', ascending=False).head(5)
    st.markdown("### 🌴 Top Recommended States")
    st.dataframe(top_states)
    season_data = pd.DataFrame({
        "Season": ["Winter (Nov–Feb)", "Summer (Mar–Jun)", "Monsoon (Jul–Oct)"],
        "Best For": ["Rajasthan, Delhi, Goa", "Kashmir, Himachal", "Kerala, Tamil Nadu"]
    })
    st.table(season_data)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#444;'>Developed by Aniket Bharti • Data Analysis Project • © 2025</p>", unsafe_allow_html=True)
