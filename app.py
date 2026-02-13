import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="🧳 Travel Packages Insights", layout="wide", initial_sidebar_state="expanded")

# --------------------------------------------------
# Enhanced CSS Styling
# --------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    div[data-testid="stAppViewContainer"] > .main {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    /* Header Styles */
    h1, h2, h3 {
        color: #ff6600 !important;
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #ff6600, #ffcc00);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(255,102,0,0.3);
    }
    
    .main-title {
        color: white !important;
        font-size: 3rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 10px;
    }
    
    .main-subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        font-weight: 400;
    }
    
    /* Metric Cards */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 20px rgba(102,126,234,0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(102,126,234,0.4);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 5px;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea, #764ba2);
    }
    
    section[data-testid="stSidebar"] > div {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px;
        padding: 15px 25px;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff6600, #ffcc00);
        color: white !important;
        border-color: #ff6600;
    }
    
    /* Package Cards */
    .package-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid #ff6600;
        transition: all 0.3s ease;
    }
    
    .package-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(255,102,0,0.2);
    }
    
    .package-title {
        color: #ff6600;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .package-detail {
        color: #666;
        font-size: 0.95rem;
        margin: 5px 0;
    }
    
    /* Chart Containers */
    .chart-container {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    /* Info Boxes */
    .info-box {
        background: linear-gradient(135deg, #e0f7fa, #b2ebf2);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00acc1;
        margin: 20px 0;
        color: #00695c;
    }
    
    .success-box {
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #4caf50;
        margin: 20px 0;
        color: #2e7d32;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ff9800;
        margin: 20px 0;
        color: #e65100;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #ff6600, #ff9933);
        color: white;
        font-weight: 700;
        border-radius: 10px;
        padding: 12px 30px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff9933, #ffcc00);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255,102,0,0.3);
    }
    
    /* Dataframe Styling */
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        margin-top: 50px;
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        border-radius: 20px;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load Data Function
# --------------------------------------------------
@st.cache_data
def load_data():
    file_path = Path("hotel.csv")
    
    if not file_path.exists():
        st.error("⚠️ hotel.csv file not found! Please ensure it's in the correct directory.")
        st.stop()
    
    df = pd.read_csv(file_path, sep=",", encoding="utf-8", on_bad_lines="skip")
    df.columns = [c.strip() for c in df.columns]
    
    # Ensure Destination column exists
    if "Destination" not in df.columns and len(df.columns) > 3:
        df = df.rename(columns={df.columns[3]: "Destination"})
    
    return df

df = load_data()

# --------------------------------------------------
# Filter India Packages
# --------------------------------------------------
india_df = df[df["Destination"].str.contains(
    "India|Delhi|Goa|Munnar|Shimla|Kerala|Ooty|Jaipur|Agra|Manali|Darjeeling|Mysore|Amritsar|Udaipur|Coorg|Rameshwaram|Madurai",
    case=False, na=False)].copy()

# Extract duration
india_df["Duration_Days"] = pd.to_numeric(
    india_df["Itinerary"].astype(str).str.extract(r'(\d+)')[0],
    errors="coerce"
)

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Package Filters")
    st.markdown("---")
    
    # Destination filter
    all_destinations = ['All'] + sorted(india_df["Destination"].dropna().unique().tolist())
    selected_destination = st.multiselect(
        "📍 Select Destinations",
        all_destinations,
        default=['All']
    )
    
    # Package type filter
    all_types = ['All'] + sorted(india_df["Package Type"].dropna().unique().tolist())
    selected_types = st.multiselect(
        "🎯 Package Types",
        all_types,
        default=['All']
    )
    
    # Duration filter
    min_dur, max_dur = int(india_df["Duration_Days"].min()), int(india_df["Duration_Days"].max())
    duration_range = st.slider(
        "⏱️ Duration (Days)",
        min_dur, max_dur, (min_dur, max_dur)
    )
    
    st.markdown("---")
    
    # Quick stats in sidebar
    st.markdown("### 📊 Quick Stats")
    st.metric("Total Packages", len(india_df))
    st.metric("Destinations", india_df["Destination"].nunique())
    st.metric("Avg Duration", f"{india_df['Duration_Days'].mean():.1f} days")
    
    st.markdown("---")
    
    # Export option
    if st.button("📥 Export Filtered Data", use_container_width=True):
        csv = india_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="india_packages.csv",
            mime="text/csv"
        )

# Apply filters
filtered_df = india_df.copy()

if 'All' not in selected_destination:
    filtered_df = filtered_df[filtered_df["Destination"].isin(selected_destination)]

if 'All' not in selected_types:
    filtered_df = filtered_df[filtered_df["Package Type"].isin(selected_types)]

filtered_df = filtered_df[
    (filtered_df["Duration_Days"] >= duration_range[0]) &
    (filtered_df["Duration_Days"] <= duration_range[1])
]

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown("""
<div class="main-header">
    <div class="main-title">🧳 Travel Package Intelligence Hub</div>
    <div class="main-subtitle">Discover, Compare & Book Your Perfect Indian Adventure</div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Key Metrics
# --------------------------------------------------
st.markdown("### 📊 Dashboard Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📦 Total Packages", len(filtered_df), 
              delta=f"{len(filtered_df) - len(india_df)} filtered" if len(filtered_df) != len(india_df) else None)

with col2:
    st.metric("🗺️ Destinations", filtered_df["Destination"].nunique())

with col3:
    st.metric("🎯 Package Types", filtered_df["Package Type"].nunique())

with col4:
    avg_duration = int(filtered_df["Duration_Days"].mean()) if not filtered_df.empty else 0
    st.metric("⏱️ Avg Duration", f"{avg_duration} days")

with col5:
    popular_dest = filtered_df["Destination"].mode()[0] if not filtered_df.empty else "N/A"
    st.metric("🏆 Top Destination", popular_dest[:15])

st.markdown("---")

# --------------------------------------------------
# Tabs for Insights
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Analytics", "🗺️ Destinations", "⏱️ Duration", 
    "🔍 Package Explorer", "💬 Insights", "🎯 Recommendations", "📈 Trends"
])

# --------------------------------------------------
# TAB 1 — Analytics Dashboard
# --------------------------------------------------
with tab1:
    st.markdown("### 📊 Package Analytics Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Package Type Distribution
        type_counts = filtered_df["Package Type"].value_counts()
        fig = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title="Package Type Distribution",
            color_discrete_sequence=px.colors.sequential.RdBu,
            hole=0.4
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top Destinations
        top_dest = filtered_df["Destination"].value_counts().head(10)
        fig = px.bar(
            x=top_dest.values,
            y=top_dest.index,
            orientation='h',
            title="Top 10 Destinations",
            color=top_dest.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Duration Distribution
    st.markdown("### ⏱️ Trip Duration Analysis")
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=filtered_df["Duration_Days"],
        nbinsx=15,
        marker_color='#ff6600',
        opacity=0.7
    ))
    fig.update_layout(
        title="Distribution of Trip Durations",
        xaxis_title="Number of Days",
        yaxis_title="Number of Packages",
        height=400,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# TAB 2 — Destination Explorer
# --------------------------------------------------
with tab2:
    st.markdown("### 🌆 Destination Deep Dive")
    
    # Destination selector
    selected_dest = st.selectbox(
        "Select a destination to explore",
        sorted(filtered_df["Destination"].unique())
    )
    
    dest_packages = filtered_df[filtered_df["Destination"] == selected_dest]
    
    # Destination metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Packages", len(dest_packages))
    with col2:
        st.metric("Package Types", dest_packages["Package Type"].nunique())
    with col3:
        st.metric("Avg Duration", f"{dest_packages['Duration_Days'].mean():.1f} days")
    with col4:
        st.metric("Duration Range", f"{dest_packages['Duration_Days'].min():.0f}-{dest_packages['Duration_Days'].max():.0f} days")
    
    st.markdown("---")
    
    # Package breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### 📦 Available Package Types in {selected_dest}")
        type_dist = dest_packages["Package Type"].value_counts()
        fig = px.bar(
            x=type_dist.index,
            y=type_dist.values,
            color=type_dist.values,
            color_continuous_scale='Sunset'
        )
        fig.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"#### ⏱️ Duration Options for {selected_dest}")
        dur_counts = dest_packages["Duration_Days"].value_counts().sort_index()
        fig = px.line(
            x=dur_counts.index,
            y=dur_counts.values,
            markers=True
        )
        fig.update_layout(
            xaxis_title="Days",
            yaxis_title="Number of Packages",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Sample packages
    st.markdown(f"#### 🎯 Featured Packages for {selected_dest}")
    sample_packages = dest_packages.head(5)
    
    for idx, row in sample_packages.iterrows():
        with st.expander(f"📦 {row['Package Name']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Type:** {row['Package Type']}")
                st.markdown(f"**Duration:** {row['Duration_Days']:.0f} days")
                st.markdown(f"**Itinerary:** {row['Itinerary']}")
            with col2:
                if pd.notna(row.get('Hotel Details')):
                    st.markdown(f"**🏨 Hotel:** {row['Hotel Details'][:50]}")
                if pd.notna(row.get('Sightseeing Places Covered')):
                    st.markdown(f"**📍 Sightseeing:** {row['Sightseeing Places Covered'][:100]}")

# --------------------------------------------------
# TAB 3 — Duration Analysis
# --------------------------------------------------
with tab3:
    st.markdown("### ⏱️ Find Packages by Duration")
    
    # Duration distribution chart
    st.markdown("#### 📊 Package Availability by Duration")
    dur_count = filtered_df["Duration_Days"].value_counts().sort_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dur_count.index,
        y=dur_count.values,
        marker=dict(
            color=dur_count.values,
            colorscale='Viridis',
            showscale=True
        ),
        text=dur_count.values,
        textposition='auto'
    ))
    fig.update_layout(
        xaxis_title="Duration (Days)",
        yaxis_title="Number of Packages",
        height=400,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Duration selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        days = st.slider("🔍 Select Trip Duration (Days)", 
                        int(filtered_df["Duration_Days"].min()), 
                        int(filtered_df["Duration_Days"].max()), 
                        5)
    
    with col2:
        st.metric("Packages Available", len(filtered_df[filtered_df["Duration_Days"] == days]))
    
    # Filter by duration
    result_df = filtered_df[filtered_df["Duration_Days"] == days]
    
    if not result_df.empty:
        st.success(f"✅ Found {len(result_df)} packages for **{days}-day trips**")
        
        # Group by destination
        dest_counts = result_df["Destination"].value_counts()
        
        st.markdown(f"#### 🗺️ Available Destinations ({days} days)")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            for dest, count in dest_counts.items():
                st.markdown(f"**{dest}**: {count} package(s)")
        
        with col2:
            fig = px.pie(
                values=dest_counts.values,
                names=dest_counts.index,
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Sunset
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        # Display packages
        st.markdown("#### 📦 Package Details")
        display_cols = ["Package Name", "Package Type", "Destination", "Itinerary", "Hotel Details", "Sightseeing Places Covered"]
        available_cols = [col for col in display_cols if col in result_df.columns]
        
        st.dataframe(
            result_df[available_cols].sort_values(by="Destination"),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("⚠️ No packages found for that duration. Try adjusting your filters.")

# --------------------------------------------------
# TAB 4 — Advanced Package Explorer
# --------------------------------------------------
with tab4:
    st.markdown("### 🔍 Advanced Package Explorer")
    
    # Multi-criteria search
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_dest = st.multiselect(
            "🗺️ Destinations",
            options=sorted(filtered_df["Destination"].unique()),
            default=[]
        )
    
    with col2:
        search_type = st.multiselect(
            "🎯 Package Types",
            options=sorted(filtered_df["Package Type"].dropna().unique()),
            default=[]
        )
    
    with col3:
        search_duration = st.multiselect(
            "⏱️ Duration (days)",
            options=sorted(filtered_df["Duration_Days"].dropna().unique().astype(int)),
            default=[]
        )
    
    # Apply search filters
    search_df = filtered_df.copy()
    
    if search_dest:
        search_df = search_df[search_df["Destination"].isin(search_dest)]
    if search_type:
        search_df = search_df[search_df["Package Type"].isin(search_type)]
    if search_duration:
        search_df = search_df[search_df["Duration_Days"].isin(search_duration)]
    
    st.markdown(f"### 📊 Search Results: {len(search_df)} packages found")
    
    if not search_df.empty:
        # Sort options
        sort_by = st.selectbox(
            "Sort by:",
            ["Package Name", "Destination", "Duration_Days", "Package Type"]
        )
        
        search_df = search_df.sort_values(by=sort_by)
        
        # Display results as cards
        for idx, row in search_df.iterrows():
            st.markdown(f"""
            <div class="package-card">
                <div class="package-title">🎯 {row['Package Name']}</div>
                <div class="package-detail">📍 <b>Destination:</b> {row['Destination']}</div>
                <div class="package-detail">🎨 <b>Type:</b> {row['Package Type']}</div>
                <div class="package-detail">⏱️ <b>Duration:</b> {row['Duration_Days']:.0f} days</div>
                <div class="package-detail">📋 <b>Itinerary:</b> {row['Itinerary']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No packages match your search criteria. Try adjusting your filters.")

# --------------------------------------------------
# TAB 5 — Word Cloud & Insights
# --------------------------------------------------
with tab5:
    st.markdown("### 💬 Popular Attractions & Insights")
    
    # Word Cloud
    text = " ".join(filtered_df["Sightseeing Places Covered"].dropna().astype(str))
    
    if text.strip():
        wordcloud = WordCloud(
            width=1200, 
            height=500, 
            background_color="white", 
            colormap="plasma",
            max_words=100
        ).generate(text)
        
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        ax.set_title("Most Mentioned Sightseeing Spots", fontsize=18, fontweight='bold')
        st.pyplot(fig)
        plt.close()
    
    st.markdown("---")
    
    # Key insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Top 10 Most Popular Destinations")
        top_dests = filtered_df["Destination"].value_counts().head(10)
        fig = px.bar(
            x=top_dests.values,
            y=top_dests.index,
            orientation='h',
            color=top_dests.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Package Type Popularity")
        type_counts = filtered_df["Package Type"].value_counts().head(10)
        fig = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Sunset
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# TAB 6 — AI Recommendations
# --------------------------------------------------
with tab6:
    st.markdown("### 🎯 Personalized Recommendations")
    
    st.markdown("""
    <div class="info-box">
        <h4>🤖 AI-Powered Package Suggestions</h4>
        <p>Tell us your preferences, and we'll recommend the perfect packages for you!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pref_duration = st.selectbox(
            "Preferred Trip Length",
            ["Weekend (2-4 days)", "Week-long (5-7 days)", "Extended (8+ days)", "Flexible"]
        )
    
    with col2:
        pref_type = st.multiselect(
            "Interests",
            filtered_df["Package Type"].dropna().unique(),
            default=[]
        )
    
    with col3:
        budget = st.select_slider(
            "Budget Level",
            options=["Budget", "Moderate", "Premium", "Luxury"]
        )
    
    if st.button("🔮 Get Recommendations", use_container_width=True):
        st.markdown("---")
        st.markdown("### ✨ Your Personalized Recommendations")
        
        # Filter based on preferences
        rec_df = filtered_df.copy()
        
        if pref_duration == "Weekend (2-4 days)":
            rec_df = rec_df[rec_df["Duration_Days"].between(2, 4)]
        elif pref_duration == "Week-long (5-7 days)":
            rec_df = rec_df[rec_df["Duration_Days"].between(5, 7)]
        elif pref_duration == "Extended (8+ days)":
            rec_df = rec_df[rec_df["Duration_Days"] >= 8]
        
        if pref_type:
            rec_df = rec_df[rec_df["Package Type"].isin(pref_type)]
        
        # Get top recommendations
        if not rec_df.empty:
            top_recs = rec_df.sample(min(5, len(rec_df)))
            
            for idx, (_, row) in enumerate(top_recs.iterrows(), 1):
                with st.expander(f"🌟 Recommendation #{idx}: {row['Package Name']}", expanded=True):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**📍 Destination:** {row['Destination']}")
                        st.markdown(f"**🎨 Package Type:** {row['Package Type']}")
                        st.markdown(f"**⏱️ Duration:** {row['Duration_Days']:.0f} days")
                        st.markdown(f"**📋 Itinerary:** {row['Itinerary']}")
                    
                    with col2:
                        st.markdown("**✅ Why This Package?**")
                        st.info(f"• Matches your {pref_duration.lower()} preference\n• Perfect for {budget} budget")
                        
                        if pd.notna(row.get('Sightseeing Places Covered')):
                            st.markdown(f"**🗺️ Highlights:** {row['Sightseeing Places Covered'][:100]}...")
        else:
            st.warning("No packages match your exact criteria. Try adjusting your preferences!")

# --------------------------------------------------
# TAB 7 — Trends & Analytics
# --------------------------------------------------
with tab7:
    st.markdown("### 📈 Package Trends & Market Analysis")
    
    # Duration trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Duration Distribution by Package Type")
        
        duration_by_type = filtered_df.groupby(['Package Type', 'Duration_Days']).size().reset_index(name='count')
        
        fig = px.scatter(
            duration_by_type,
            x='Duration_Days',
            y='Package Type',
            size='count',
            color='count',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🗺️ Destination Diversity by Duration")
        
        dest_by_duration = filtered_df.groupby('Duration_Days')['Destination'].nunique().reset_index()
        
        fig = px.line(
            dest_by_duration,
            x='Duration_Days',
            y='Destination',
            markers=True,
            color_discrete_sequence=['#ff6600']
        )
        fig.update_layout(
            xaxis_title="Trip Duration (Days)",
            yaxis_title="Number of Unique Destinations",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Market insights
    st.markdown("---")
    st.markdown("### 💡 Market Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h4>🎯 Most Versatile Destination</h4>
            <p><b>{}</b></p>
            <p>Offers {} different package types</p>
        </div>
        """.format(
            filtered_df.groupby('Destination')['Package Type'].nunique().idxmax(),
            filtered_df.groupby('Destination')['Package Type'].nunique().max()
        ), unsafe_allow_html=True)
    
    with col2:
        avg_dur = filtered_df['Duration_Days'].mean()
        st.markdown(f"""
        <div class="info-box">
            <h4>⏱️ Average Trip Duration</h4>
            <p><b>{avg_dur:.1f} days</b></p>
            <p>Most packages range 3-7 days</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        most_common_type = filtered_df['Package Type'].mode()[0] if not filtered_df.empty else "N/A"
        st.markdown(f"""
        <div class="warning-box">
            <h4>🏆 Most Popular Type</h4>
            <p><b>{most_common_type}</b></p>
            <p>Traveler favorite category</p>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.markdown("""
<div class="footer">
    <h3 style="color:#ff6600;">🧳 India Travel Packages Intelligence Platform</h3>
    <p style="margin:15px 0;">Discover • Compare • Book Your Dream Indian Adventure</p>
    <p style="color:#666; margin-top:20px;">
        Developed with ❤️ by <b>Aniket Bharti</b> • Data Analytics & Visualization Project
    </p>
    <p style="color:#999; font-size:0.9rem; margin-top:10px;">
        © 2025 • Powered by Streamlit & Python
    </p>
</div>
""", unsafe_allow_html=True)

