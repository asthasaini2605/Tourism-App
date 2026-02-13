import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import base64
from datetime import datetime

# ---------- Config ----------
st.set_page_config(page_title="Tourism Dashboard 🇮🇳", layout="wide", initial_sidebar_state="expanded")

# ---------- Enhanced CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

/* Main container */
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

/* Header styles */
.dashboard-header {
    text-align: center;
    padding: 30px;
    background: linear-gradient(135deg, #ff6600, #ffcc00);
    border-radius: 20px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(255,102,0,0.3);
}

.dashboard-title {
    color: white;
    font-size: 3rem;
    font-weight: 800;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    margin-bottom: 10px;
}

.dashboard-subtitle {
    color: rgba(255,255,255,0.95);
    font-size: 1.2rem;
    font-weight: 400;
}

/* Metric cards */
.metric-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.metric-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 25px;
    border-radius: 15px;
    color: white;
    text-align: center;
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

/* Tabs styling */
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
    color: white;
    border-color: #ff6600;
}

/* Info boxes */
.info-box {
    background: linear-gradient(135deg, #e0f7fa, #b2ebf2);
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #00acc1;
    margin: 20px 0;
}

.success-box {
    background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #4caf50;
    margin: 20px 0;
}

.warning-box {
    background: linear-gradient(135deg, #fff3e0, #ffe0b2);
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #ff9800;
    margin: 20px 0;
}

/* Chart containers */
.chart-container {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    margin: 20px 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #667eea, #764ba2);
}

section[data-testid="stSidebar"] > div {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}

/* Selectbox and inputs */
.stSelectbox > div > div {
    background: white;
    border-radius: 10px;
}

/* Dataframe styling */
.dataframe {
    border-radius: 10px !important;
    overflow: hidden;
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    margin-top: 40px;
    color: #666;
    border-top: 2px solid #eee;
}
</style>
""", unsafe_allow_html=True)

# ---------- Clean Gradient Background ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
""", unsafe_allow_html=True)

# ---------- Load Data ----------
@st.cache_data
def load_and_clean(path):
    try:
        df = pd.read_csv(path)
        df = df[df['Circle'] != 'Total'].copy()
        df.columns = [col.replace('-20', '20').replace('-19', '19') for col in df.columns]
        df['state'] = df['state'].astype(str).str.strip().str.title()
        df['TotalVisitors'] = df['Domestic19'] + df['Foreign19']
        for col in ['Domestic19','Foreign19','Domesticgrowth','Foreigngrowth']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df.dropna(inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_and_clean("india2.csv")

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### 🎛️ Dashboard Controls")
    st.markdown("---")
    
    # Filter options
    st.markdown("#### 📍 Filters")
    
    # State filter
    all_states = ['All States'] + sorted(df['state'].unique().tolist())
    selected_state = st.selectbox("Select State", all_states)
    
    # Visitor type filter
    visitor_type = st.radio("Visitor Type", ["All", "Domestic", "Foreign"])
    
    # Growth filter
    min_growth = st.slider("Minimum Growth %", -100, 200, -100)
    
    st.markdown("---")
    st.markdown("#### 📊 Quick Stats")
    st.metric("Total States", df['state'].nunique())
    st.metric("Total Monuments", len(df))
    st.metric("Avg Visitors/Monument", f"{df['TotalVisitors'].mean():.0f}")
    
    st.markdown("---")
    st.markdown("#### ℹ️ About")
    st.info("This dashboard provides comprehensive insights into India's tourism landscape with interactive visualizations and analytics.")

# Apply filters
filtered_df = df.copy()
if selected_state != 'All States':
    filtered_df = filtered_df[filtered_df['state'] == selected_state]
if visitor_type == "Domestic":
    filtered_df = filtered_df[filtered_df['Domesticgrowth'] >= min_growth]
elif visitor_type == "Foreign":
    filtered_df = filtered_df[filtered_df['Foreigngrowth'] >= min_growth]

# ---------- Header ----------
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">🌆 India Tourism Analytics Dashboard</div>
    <div class="dashboard-subtitle">Explore tourism growth, popular destinations, and interactive insights</div>
</div>
""", unsafe_allow_html=True)

# ---------- Key Metrics ----------
st.markdown("### 📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_visitors = filtered_df['TotalVisitors'].sum()
    st.metric("Total Visitors", f"{total_visitors/1e6:.2f}M", 
              delta=f"{filtered_df['Domesticgrowth'].mean():.1f}% growth")

with col2:
    domestic = filtered_df['Domestic19'].sum()
    st.metric("Domestic Visitors", f"{domestic/1e6:.2f}M",
              delta=f"{filtered_df['Domesticgrowth'].mean():.1f}%")

with col3:
    foreign = filtered_df['Foreign19'].sum()
    st.metric("Foreign Visitors", f"{foreign/1e3:.0f}K",
              delta=f"{filtered_df['Foreigngrowth'].mean():.1f}%")

with col4:
    st.metric("States Covered", filtered_df['state'].nunique())

with col5:
    st.metric("Monuments", len(filtered_df))

st.markdown("---")

# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview", "🏞️ State Analysis", "📈 Growth Trends", 
    "🗺️ India Map", "🎯 Top Performers", "🧭 Plan My Trip"
])

# --- Tab 1: Overview ---
with tab1:
    st.markdown("### ✨ Tourism Landscape Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Places count by state
        places_count = filtered_df.groupby('state')['Name of the Monument'].count().sort_values(ascending=False).head(15)
        
        fig = go.Figure(data=[
            go.Bar(x=places_count.values, y=places_count.index,
                   orientation='h',
                   marker=dict(color=places_count.values,
                             colorscale='Viridis',
                             showscale=True))
        ])
        fig.update_layout(
            title="Top 15 States by Tourist Places",
            xaxis_title="Number of Places",
            yaxis_title="State",
            height=500,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Visitor distribution pie chart
        visitor_dist = pd.DataFrame({
            'Type': ['Domestic', 'Foreign'],
            'Count': [filtered_df['Domestic19'].sum(), filtered_df['Foreign19'].sum()]
        })
        
        fig = px.pie(visitor_dist, values='Count', names='Type',
                     title='Domestic vs Foreign Visitors Distribution',
                     color_discrete_sequence=['#ff6600', '#ffcc00'],
                     hole=0.4)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top monuments
    st.markdown("#### 🏆 Top 10 Most Visited Monuments")
    top_monuments = filtered_df.nlargest(10, 'TotalVisitors')[
        ['Name of the Monument', 'state', 'TotalVisitors', 'Domestic19', 'Foreign19']
    ].reset_index(drop=True)
    st.dataframe(top_monuments, use_container_width=True)

# --- Tab 2: State Analysis ---
with tab2:
    st.markdown("### 🏞️ Detailed State-wise Analysis")
    
    states = sorted(filtered_df['state'].unique())
    state = st.selectbox("🔍 Select a State for Detailed Analysis:", states, key="state_select")
    
    subset = filtered_df[filtered_df['state'] == state]
    
    if not subset.empty:
        # State metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Places", len(subset))
        with col2:
            st.metric("Total Visitors", f"{subset['TotalVisitors'].sum()/1e6:.2f}M")
        with col3:
            st.metric("Avg Growth", f"{subset['Domesticgrowth'].mean():.1f}%")
        with col4:
            st.metric("Top Monument", subset.nlargest(1, 'TotalVisitors')['Name of the Monument'].values[0][:20])
        
        st.markdown("---")
        
        # Detailed data table
        st.markdown(f"#### 📋 All Monuments in {state}")
        display_df = subset[['Name of the Monument','Domestic19','Foreign19','Domesticgrowth','Foreigngrowth']].copy()
        display_df.columns = ['Monument', 'Domestic', 'Foreign', 'Dom. Growth %', 'For. Growth %']
        st.dataframe(display_df, use_container_width=True)
        
        # Visualization
        st.markdown(f"#### 📊 Visitor Comparison in {state}")
        plot_data = subset[['Name of the Monument','Domestic19','Foreign19']].melt(
            id_vars='Name of the Monument', var_name='Visitor Type', value_name='Visitors')
        
        fig = px.bar(plot_data, x='Visitors', y='Name of the Monument',
                     color='Visitor Type', orientation='h',
                     title=f"Visitor Distribution Across Monuments in {state}",
                     color_discrete_sequence=['#ff6600', '#ffcc00'])
        fig.update_layout(height=max(400, len(subset) * 30))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No data available for the selected state with current filters.")

# --- Tab 3: Growth Trends ---
with tab3:
    st.markdown("### 📈 Tourism Growth Analysis (2019–2020)")
    
    # Growth comparison
    growth = filtered_df.groupby('state')[['Domesticgrowth','Foreigngrowth']].mean().reset_index()
    growth = growth.sort_values('Domesticgrowth', ascending=False).head(20)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Domestic Growth',
        x=growth['state'],
        y=growth['Domesticgrowth'],
        marker_color='#ff6600'
    ))
    fig.add_trace(go.Bar(
        name='Foreign Growth',
        x=growth['state'],
        y=growth['Foreigngrowth'],
        marker_color='#ffcc00'
    ))
    
    fig.update_layout(
        title='Top 20 States by Average Growth Rate',
        xaxis_title='State',
        yaxis_title='Growth Rate (%)',
        barmode='group',
        height=500,
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Growth insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚀 Fastest Growing (Domestic)")
        top_growth_dom = filtered_df.nlargest(5, 'Domesticgrowth')[
            ['state', 'Name of the Monument', 'Domesticgrowth']
        ]
        st.dataframe(top_growth_dom, use_container_width=True)
    
    with col2:
        st.markdown("#### 🌍 Fastest Growing (Foreign)")
        top_growth_for = filtered_df.nlargest(5, 'Foreigngrowth')[
            ['state', 'Name of the Monument', 'Foreigngrowth']
        ]
        st.dataframe(top_growth_for, use_container_width=True)
    
    st.info("💡 **Insight**: States with high growth rates represent emerging destinations with increasing tourism potential!")

# --- Tab 4: India Map ---
with tab4:
    st.markdown("### 🗺️ Interactive Tourism Heatmap of India")
    
    # Use reliable GeoJSON
    india_geojson = "https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson"
    
    # Aggregate visitors by state
    state_visitors = filtered_df.groupby('state')['TotalVisitors'].sum().reset_index()
    
    # Normalize state names
    state_visitors['state'] = state_visitors['state'].str.title().replace({
        'Andaman And Nicobar Islands': 'Andaman & Nicobar Islands',
        'Nct Of Delhi': 'Delhi',
        'Jammu And Kashmir': 'Jammu & Kashmir',
        'Odisha': 'Orissa',
        'Pondicherry': 'Puducherry'
    })
    
    # Create choropleth map
    fig_map = px.choropleth(
        state_visitors,
        geojson=india_geojson,
        featureidkey="properties.NAME_1",
        locations="state",
        color="TotalVisitors",
        color_continuous_scale="YlOrRd",
        title="Tourism Intensity Across Indian States",
        hover_name="state",
        hover_data={'TotalVisitors': ':,.0f'}
    )
    
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(height=600)
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.info("🧭 **Interactive Map**: Hover over states to see detailed visitor statistics. Darker colors indicate higher tourism activity!")

# --- Tab 5: Top Performers ---
with tab5:
    st.markdown("### 🎯 Top Performing Destinations")
    
    # Leaderboard
    st.markdown("#### 🏆 Overall Leaderboard")
    
    leaderboard = filtered_df.groupby('state').agg({
        'TotalVisitors': 'sum',
        'Domestic19': 'sum',
        'Foreign19': 'sum',
        'Domesticgrowth': 'mean',
        'Foreigngrowth': 'mean',
        'Name of the Monument': 'count'
    }).round(2)
    
    leaderboard.columns = ['Total Visitors', 'Domestic', 'Foreign', 
                           'Avg Dom. Growth %', 'Avg For. Growth %', 'No. of Places']
    leaderboard = leaderboard.sort_values('Total Visitors', ascending=False).head(15)
    
    st.dataframe(leaderboard, use_container_width=True)
    
    # Category winners
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 👥 Most Domestic Visitors")
        top_dom = filtered_df.nlargest(5, 'Domestic19')[['Name of the Monument', 'state', 'Domestic19']]
        for idx, row in top_dom.iterrows():
            st.markdown(f"**{row['Name of the Monument'][:30]}**")
            st.caption(f"{row['state']} • {row['Domestic19']:,.0f} visitors")
            st.markdown("---")
    
    with col2:
        st.markdown("#### 🌍 Most Foreign Visitors")
        top_for = filtered_df.nlargest(5, 'Foreign19')[['Name of the Monument', 'state', 'Foreign19']]
        for idx, row in top_for.iterrows():
            st.markdown(f"**{row['Name of the Monument'][:30]}**")
            st.caption(f"{row['state']} • {row['Foreign19']:,.0f} visitors")
            st.markdown("---")
    
    with col3:
        st.markdown("#### 📈 Highest Growth")
        top_growth = filtered_df.nlargest(5, 'Domesticgrowth')[['Name of the Monument', 'state', 'Domesticgrowth']]
        for idx, row in top_growth.iterrows():
            st.markdown(f"**{row['Name of the Monument'][:30]}**")
            st.caption(f"{row['state']} • +{row['Domesticgrowth']:.1f}% growth")
            st.markdown("---")

# --- Tab 6: Plan My Trip ---
with tab6:
    st.markdown("### 🧭 AI-Powered Trip Planner")
    
    # Recommendation engine
    st.markdown("#### 🎯 Get Personalized Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        trip_duration = st.select_slider(
            "Trip Duration",
            options=["Weekend (2-3 days)", "Short Trip (4-7 days)", "Long Trip (8+ days)"]
        )
        
        interests = st.multiselect(
            "Your Interests",
            ["History & Heritage", "Nature & Wildlife", "Beaches", "Mountains", 
             "Spiritual", "Adventure", "Culture"]
        )
    
    with col2:
        budget = st.select_slider(
            "Budget Level",
            options=["Budget", "Moderate", "Luxury"]
        )
        
        season = st.selectbox(
            "Preferred Season",
            ["Winter (Nov-Feb)", "Summer (Mar-Jun)", "Monsoon (Jul-Oct)", "Any"]
        )
    
    if st.button("🔍 Generate Recommendations", use_container_width=True):
        st.markdown("---")
        st.markdown("#### 🌟 Recommended Destinations")
        
        # Smart recommendations
        top_states = filtered_df.groupby('state').agg({
            'TotalVisitors': 'mean',
            'Domesticgrowth': 'mean',
            'Name of the Monument': 'count'
        }).sort_values(by='TotalVisitors', ascending=False).head(5)
        
        for idx, (state, row) in enumerate(top_states.iterrows(), 1):
            with st.expander(f"🏆 #{idx} Recommendation: {state}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Avg Visitors", f"{row['TotalVisitors']/1e3:.0f}K")
                with col2:
                    st.metric("Growth Rate", f"{row['Domesticgrowth']:.1f}%")
                with col3:
                    st.metric("Places", int(row['Name of the Monument']))
                
                # Get top places in this state
                state_places = filtered_df[filtered_df['state'] == state].nlargest(3, 'TotalVisitors')
                st.markdown("**Must-Visit Places:**")
                for _, place in state_places.iterrows():
                    st.markdown(f"• {place['Name of the Monument']}")
    
    st.markdown("---")
    
    # Seasonal recommendations
    st.markdown("#### 🌦️ Best Destinations by Season")
    
    season_data = pd.DataFrame({
        "Season": ["🥶 Winter (Nov–Feb)", "☀️ Summer (Mar–Jun)", "🌧️ Monsoon (Jul–Oct)"],
        "Best Destinations": [
            "Rajasthan, Delhi, Goa, Tamil Nadu, Kerala",
            "Kashmir, Himachal Pradesh, Uttarakhand, Sikkim",
            "Kerala, Goa, Maharashtra (Western Ghats), Northeast States"
        ],
        "Why Visit": [
            "Pleasant weather, festivals, beach destinations",
            "Cool mountain retreats, valley of flowers",
            "Lush greenery, waterfalls, off-season discounts"
        ]
    })
    
    st.table(season_data)

# ---------- Footer ----------
st.markdown("---")
st.markdown("""
<div class="footer">
    <p style="font-size:1.1rem; color:#333; margin-bottom:10px;">
        <b>India Tourism Analytics Dashboard</b>
    </p>
    <p style="color:#666;">
        Developed with ❤️ by <b>Aniket Bharti</b> • Data Analysis & Visualization Project • © 2025
    </p>
    <p style="font-size:0.9rem; color:#999; margin-top:10px;">
        Last Updated: """ + datetime.now().strftime("%B %d, %Y") + """
    </p>
</div>
""", unsafe_allow_html=True)
