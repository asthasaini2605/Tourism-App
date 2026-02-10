import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="🧳 Travel Packages Insights", layout="wide")

st.markdown("""
    <style>
    h1, h2, h3 {
        color: #ff6600 !important;
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background: linear-gradient(180deg, #fffaf0 0%, #fff5e1 100%);
    }
    .highlight {
        font-size: 18px;
        color: #333;
        background: rgba(255, 255, 255, 0.7);
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        r"C:\Users\adity\OneDrive\Desktop\DBMS lab\Tourismapp\hotel.csv",
        sep=",",
        encoding="utf-8",
        on_bad_lines="skip"
    )
    df.columns = [c.strip() for c in df.columns]
    if "Destination" not in df.columns:
        df = df.rename(columns={df.columns[3]: "Destination"})
    return df

import pandas as pd
from pathlib import Path
import streamlit as st

@st.cache_data
def load_data():
    file_path = Path("hotel.csv")  # relative path

    if not file_path.exists():
        st.error("hotel.csv file not found! Put it inside the Tourismapp folder.")
        st.stop()

    df = pd.read_csv(file_path, sep=",", encoding="utf-8", on_bad_lines="skip")
    return df

df = load_data()


# --------------------------------------------------
# Filter India Packages
# --------------------------------------------------
india_df = df[df["Destination"].str.contains(
    "India|Delhi|Goa|Munnar|Shimla|Kerala|Ooty|Jaipur|Agra|Manali|Darjeeling|Mysore|Amritsar|Udaipur|Coorg|Rameshwaram|Madurai",
    case=False, na=False)]

st.title("🧭 Travel Package Analysis Dashboard - Incredible India 🇮🇳")
st.markdown("### ✨ Explore insights and trends from Indian travel packages — destinations, types, durations, and more!")

# --------------------------------------------------
# Summary Section
# --------------------------------------------------
st.subheader("📋 Summary Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Packages", len(india_df))
col2.metric("Unique Destinations", india_df["Destination"].nunique())
col3.metric("Package Types", india_df["Package Type"].nunique())

# Handle numeric extraction safely
duration_series = india_df["Itinerary"].astype(str).str.extract(r'(\d+)').dropna()
avg_duration = int(duration_series[0].astype(int).mean()) if not duration_series.empty else 0
col4.metric("Average Duration (days)", avg_duration)

st.markdown("<hr>", unsafe_allow_html=True)

# --------------------------------------------------
# Tabs for Insights
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Package Types",
    "🗺️ Popular Destinations",
    "🕒 Duration Distribution",
    "🏆 Top Tourist Packages",
    "💬 Word Cloud",
    "🧳 Find Packages by Duration"
])

# --------------------------------------------------
# TAB 1 — Package Type Distribution
# --------------------------------------------------
with tab1:
    st.subheader("📦 Package Type Distribution")
    plt.figure(figsize=(10, 5))
    sns.countplot(x="Package Type", data=india_df, palette="viridis")
    plt.title("Count of Travel Packages by Type", fontsize=14)
    st.pyplot(plt.gcf())
    plt.clf()

# --------------------------------------------------
# TAB 2 — Most Popular Destinations
# --------------------------------------------------
with tab2:
    st.subheader("🌆 Top Travel Destinations in India")
    top_dest = india_df["Destination"].value_counts().head(10)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=top_dest.values, y=top_dest.index, palette="coolwarm")
    plt.title("Top 10 Travel Destinations", fontsize=14)
    st.pyplot(plt.gcf())
    plt.clf()

# --------------------------------------------------
# TAB 3 — Duration Analysis
# --------------------------------------------------
with tab3:
    st.subheader("🕒 Trip Duration Distribution")
    dur = india_df["Itinerary"].astype(str).str.extract(r'(\d+)').dropna()[0].astype(int)
    plt.figure(figsize=(10, 5))
    sns.histplot(dur, bins=10, kde=True, color="orange")
    plt.title("Distribution of Trip Duration", fontsize=14)
    plt.xlabel("Number of Days")
    plt.ylabel("Number of Packages")
    st.pyplot(plt.gcf())
    plt.clf()

# --------------------------------------------------
# TAB 4 — Interactive Top Packages
# --------------------------------------------------
# --------------------------------------------------
# TAB 4 — Interactive Top Packages
# --------------------------------------------------
with tab4:
    st.subheader("🏆 Explore Top Tourist Packages")

    # --- Prepare Duration column before filtering ---
    india_df["Duration_Days"] = pd.to_numeric(
        india_df["Itinerary"].astype(str).str.extract(r'(\d+)')[0],
        errors="coerce"
    )

    # --- Filters ---
    col1, col2, col3 = st.columns(3)
    destination_filter = col1.selectbox("🌍 Select Destination", ["All"] + sorted(india_df["Destination"].unique().tolist()))
    package_type_filter = col2.selectbox("🎯 Select Package Type", ["All"] + sorted(india_df["Package Type"].dropna().unique().tolist()))
    duration_filter = col3.slider("🕒 Filter by Duration (Days)", 1, 20, (1, 10))

    # --- Apply filters ---
    filtered_df = india_df.copy()
    if destination_filter != "All":
        filtered_df = filtered_df[filtered_df["Destination"] == destination_filter]
    if package_type_filter != "All":
        filtered_df = filtered_df[filtered_df["Package Type"] == package_type_filter]
    filtered_df = filtered_df[
        (filtered_df["Duration_Days"] >= duration_filter[0]) &
        (filtered_df["Duration_Days"] <= duration_filter[1])
    ]

    # --- Show Data ---
    if not filtered_df.empty:
        st.dataframe(
            filtered_df[
                ["Package Name", "Package Type", "Destination", "Itinerary", "Hotel Details", "Sightseeing Places Covered", "Duration_Days"]
            ]
            .sort_values(by="Duration_Days", ascending=False)
            .head(15)
            .style.set_properties(**{
                'background-color': '#fff5e6',
                'color': '#333',
                'border-color': '#ffcc66'
            }),
            use_container_width=True
        )
    else:
        st.warning("No packages match your filters! Try adjusting your search criteria.")


# --------------------------------------------------
# TAB 5 — Word Cloud of Sightseeing Spots
# --------------------------------------------------
with tab5:
    st.subheader("💬 Top Sightseeing Attractions")
    text = " ".join(india_df["Sightseeing Places Covered"].dropna().astype(str))
    wordcloud = WordCloud(width=900, height=400, background_color="white", colormap="plasma").generate(text)

    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Most Mentioned Sightseeing Spots", fontsize=14)
    st.pyplot(plt.gcf())

# --------------------------------------------------
# TAB 6 — Find Packages by Duration (New Feature)
# --------------------------------------------------
# --------------------------------------------------
# TAB 5 — Find Packages by Duration
# --------------------------------------------------
tab6 = st.tabs(["🎒 Find Packages by Duration"])[0]

with tab6:
    st.subheader("🎯 Discover Packages Based on Trip Duration")

    # --- Prepare duration column ---
    india_df["Duration_Days"] = pd.to_numeric(
        india_df["Itinerary"].astype(str).str.extract(r'(\d+)')[0],
        errors="coerce"
    )

    # --- Summary bar chart ---
    st.markdown("#### 📊 Distribution of Packages by Duration")
    dur_count = india_df["Duration_Days"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=dur_count.index, y=dur_count.values, palette="crest", ax=ax)
    ax.set_xlabel("Duration (Days)")
    ax.set_ylabel("Number of Packages")
    ax.set_title("How Many Packages Exist for Each Duration", fontsize=13)
    st.pyplot(fig)

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Slider for user input ---
    days = st.slider("⏳ Select Desired Trip Duration (Days)", 1, int(india_df["Duration_Days"].max()), 5)

    # --- Filter packages matching chosen duration ---
    result_df = india_df[india_df["Duration_Days"] == days]

    if not result_df.empty:
        st.success(f"✅ Found {len(result_df)} packages for **{days}-day trips**")
        st.dataframe(
            result_df[
                ["Package Name", "Package Type", "Destination", "Itinerary", "Hotel Details", "Sightseeing Places Covered"]
            ]
            .sort_values(by="Destination")
            .style.set_properties(**{
                'background-color': '#fff5e6',
                'color': '#333',
                'border-color': '#ffcc66'
            }),
            use_container_width=True
        )
    else:
        st.warning("No packages found for that duration. Try adjusting your selection.")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>Developed by <b>Aniket Bharti</b> • Data Analysis & Visualization • © 2025</p>", unsafe_allow_html=True)
