import streamlit as st
from pathlib import Path
from PIL import Image
import base64

st.set_page_config(page_title="Incredible India 🌏", layout="wide", initial_sidebar_state="collapsed")

# --------------------- CSS ---------------------
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

/* Page main content */
div[data-testid="stAppViewContainer"] > .main {
    margin-top: 100px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

/* Navbar styling */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 9999;
    background: linear-gradient(135deg, rgba(255,102,0,0.95), rgba(255,204,0,0.95));
    padding: 15px 40px;
    box-shadow: 0 4px 30px rgba(0,0,0,0.2);
    backdrop-filter: blur(10px);
}

.navbar-brand {
    font-size: 1.8rem;
    font-weight: 800;
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.navbar-links {
    display: flex;
    gap: 25px;
}

.nav-btn {
    background: rgba(255,255,255,0.2);
    padding: 10px 24px;
    border-radius: 30px;
    color: white;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
    border: 2px solid rgba(255,255,255,0.3);
    backdrop-filter: blur(5px);
}

.nav-btn:hover {
    background: white;
    color: #ff6600;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

/* Hero Section */
.hero-section {
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,248,240,0.9));
    border-radius: 20px;
    margin-bottom: 40px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

.animated-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ff6600, #ffcc00, #ff0099, #6600ff);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 8s ease infinite;
    margin-bottom: 15px;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.subtitle {
    font-size: 1.3rem;
    color: #555;
    margin: 20px 0;
    font-weight: 300;
}

.typewriter {
    max-width: 900px;
    margin: 25px auto;
    font-size: 1.1rem;
    color: #4a2c15;
    padding: 15px;
    background: rgba(255,248,220,0.7);
    border-left: 4px solid #ff6600;
    border-radius: 8px;
}

/* Stats Section */
.stats-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 40px 0;
}

.stat-card {
    background: linear-gradient(135deg, #ff6600, #ffcc00);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    box-shadow: 0 8px 20px rgba(255,102,0,0.3);
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px) scale(1.02);
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 5px;
}

.stat-label {
    font-size: 1rem;
    font-weight: 400;
    opacity: 0.95;
}

/* Gallery Section */
.gallery-header {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    color: #333;
    margin: 50px 0 30px 0;
    position: relative;
}

.gallery-header::after {
    content: '';
    display: block;
    width: 100px;
    height: 4px;
    background: linear-gradient(90deg, #ff6600, #ffcc00);
    margin: 15px auto;
    border-radius: 2px;
}

/* Image styling */
div[data-testid="stImage"] {
    transition: transform 0.3s ease;
}

div[data-testid="stImage"] img {
    border-radius: 20px;
    transition: all 0.4s ease;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    border: 3px solid white;
}

div[data-testid="stImage"]:hover img {
    transform: translateY(-10px) scale(1.05);
    box-shadow: 0 20px 50px rgba(0,0,0,0.25);
}

.img-caption {
    text-align: center;
    font-weight: 600;
    margin-top: 12px;
    color: #333;
    font-size: 1.1rem;
    padding: 8px;
    background: rgba(255,255,255,0.8);
    border-radius: 8px;
    backdrop-filter: blur(5px);
}

/* Features Section */
.features-section {
    background: linear-gradient(135deg, rgba(102,0,255,0.05), rgba(255,0,153,0.05));
    padding: 50px 20px;
    border-radius: 20px;
    margin: 50px 0;
}

.feature-card {
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    margin-bottom: 20px;
    border: 2px solid transparent;
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: #ff6600;
    box-shadow: 0 10px 30px rgba(255,102,0,0.2);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 15px;
}

.feature-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #333;
    margin-bottom: 10px;
}

.feature-desc {
    color: #666;
    line-height: 1.6;
}

/* Buttons styling */
.button-section {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin: 60px 0;
    flex-wrap: wrap;
}

.stButton>button {
    background: linear-gradient(135deg, #ff6600, #ff9933);
    color: white;
    font-weight: 700;
    font-size: 1.1rem;
    padding: 18px 40px;
    border-radius: 50px;
    border: none;
    box-shadow: 0 10px 30px rgba(255,102,0,0.3);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #ff9933, #ffcc00);
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 15px 40px rgba(255,153,51,0.4);
}

/* Testimonial Section */
.testimonial-section {
    background: linear-gradient(135deg, rgba(255,248,220,0.8), rgba(255,240,200,0.8));
    padding: 40px;
    border-radius: 20px;
    margin: 40px 0;
    text-align: center;
}

.testimonial-text {
    font-size: 1.2rem;
    font-style: italic;
    color: #555;
    margin-bottom: 15px;
}

.testimonial-author {
    font-weight: 600;
    color: #ff6600;
}

/* Footer */
.footer {
    background: linear-gradient(135deg, #333, #555);
    color: white;
    padding: 40px 20px;
    border-radius: 20px;
    margin-top: 60px;
}

.footer-content {
    text-align: center;
}

.social-links {
    margin: 20px 0;
}

.social-icon {
    display: inline-block;
    margin: 0 10px;
    font-size: 1.5rem;
    transition: transform 0.3s ease;
}

.social-icon:hover {
    transform: scale(1.2);
}

.credits {
    text-align: center;
    color: rgba(255,255,255,0.8);
    margin-top: 20px;
    font-size: 0.95rem;
}

/* Responsive Design */
@media (max-width: 768px) {
    .animated-title {
        font-size: 2rem;
    }
    .navbar {
        flex-direction: column;
        padding: 10px 20px;
    }
    .navbar-links {
        margin-top: 10px;
    }
    .stats-container {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# --------------------- Clean Gradient Background ---------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
</style>
""", unsafe_allow_html=True)

# --------------------- Navbar ---------------------
st.markdown("""
<div class="navbar">
  <div class="navbar-brand">🇮🇳 Incredible India</div>
  <div class="navbar-links">
    <a class="nav-btn" href="#home">🏠 Home</a>
    <a class="nav-btn" href="#gallery">🖼️ Gallery</a>
    <a class="nav-btn" href="#features">✨ Features</a>
    <a class="nav-btn" href="#explore">🧭 Explore</a>
  </div>
</div>
""", unsafe_allow_html=True)

# --------------------- Hero Section ---------------------
st.markdown("""
<div id="home" class="hero-section">
    <div class="animated-title">🌏 Welcome to Incredible India 🇮🇳</div>
    <div class="subtitle">A journey through nature, culture, history and flavors</div>
    <div class="typewriter">
        From the majestic Taj Mahal to the serene backwaters of Kerala — discover India's incredible diversity, 
        rich heritage, and warm hospitality through our interactive tourism platform.
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------- Stats Section ---------------------
st.markdown("""
<div class="stats-container">
    <div class="stat-card">
        <div class="stat-number">29</div>
        <div class="stat-label">States & UTs</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">40+</div>
        <div class="stat-label">UNESCO Sites</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">500+</div>
        <div class="stat-label">Tourist Destinations</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">∞</div>
        <div class="stat-label">Experiences</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------- Image Gallery ---------------------
st.markdown("<div id='gallery' class='gallery-header'>📸 Explore Iconic Destinations</div>", unsafe_allow_html=True)

monuments = [
    ("Taj Mahal, Agra", "tajmahal.jpg", "The epitome of love and Mughal architecture"),
    ("Goa Beach", "goa.jpg", "Sun, sand, and stunning coastal beauty"),
    ("Jaipur Palace", "jaipur.jpg", "Royal heritage and vibrant culture"),
    ("Himalayas", "himalayas.jpg", "Majestic peaks and spiritual serenity"),
    ("Kerala Backwaters", "kerala.jpg", "Tranquil waters and lush greenery"),
]

TARGET_WIDTH = 600
TARGET_HEIGHT = 400

def load_and_resize(path, w=TARGET_WIDTH, h=TARGET_HEIGHT):
    p = Path(path)
    if not p.exists():
        return None
    img = Image.open(p).convert("RGB")
    img = img.resize((w, h), Image.LANCZOS)
    return img

# Row 1
col1, col2 = st.columns(2, gap="large")
with col1:
    img = load_and_resize(monuments[0][1])
    if img:
        st.image(img, use_container_width=True)
        st.markdown(f"<div class='img-caption'>🕌 {monuments[0][0]}<br><small>{monuments[0][2]}</small></div>", unsafe_allow_html=True)
with col2:
    img = load_and_resize(monuments[1][1])
    if img:
        st.image(img, use_container_width=True)
        st.markdown(f"<div class='img-caption'>🏖️ {monuments[1][0]}<br><small>{monuments[1][2]}</small></div>", unsafe_allow_html=True)

# Row 2
col3, col4 = st.columns(2, gap="large")
with col3:
    img = load_and_resize(monuments[2][1])
    if img:
        st.image(img, use_container_width=True)
        st.markdown(f"<div class='img-caption'>🏰 {monuments[2][0]}<br><small>{monuments[2][2]}</small></div>", unsafe_allow_html=True)
with col4:
    img = load_and_resize(monuments[3][1])
    if img:
        st.image(img, use_container_width=True)
        st.markdown(f"<div class='img-caption'>🏔️ {monuments[3][0]}<br><small>{monuments[3][2]}</small></div>", unsafe_allow_html=True)

# Row 3 - Featured image
st.markdown("<br>", unsafe_allow_html=True)
center_col_left, center_col_mid, center_col_right = st.columns([1, 2, 1])
with center_col_mid:
    img = load_and_resize(monuments[4][1], w=700, h=450)
    if img:
        st.image(img, use_container_width=True)
        st.markdown(f"<div class='img-caption'>🛶 {monuments[4][0]}<br><small>{monuments[4][2]}</small></div>", unsafe_allow_html=True)

# --------------------- Features Section ---------------------
st.markdown("<div id='features' class='features-section'>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:#333; margin-bottom:40px;'>✨ Platform Features</h2>", unsafe_allow_html=True)

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>📊</div>
        <div class='feature-title'>Interactive Analytics</div>
        <div class='feature-desc'>Explore tourism data with dynamic charts, growth trends, and state-wise analysis</div>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>🗺️</div>
        <div class='feature-title'>Heat Maps</div>
        <div class='feature-desc'>Visualize visitor distribution across India with interactive geographical maps</div>
    </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>🧳</div>
        <div class='feature-title'>Smart Packages</div>
        <div class='feature-desc'>Find perfect travel packages based on duration, destination, and preferences</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --------------------- Testimonial ---------------------
st.markdown("""
<div class="testimonial-section">
    <div class="testimonial-text">
        "India is the cradle of the human race, the birthplace of human speech, the mother of history, 
        the grandmother of legend, and the great grandmother of tradition."
    </div>
    <div class="testimonial-author">— Mark Twain</div>
</div>
""", unsafe_allow_html=True)

# --------------------- CTA Buttons ---------------------
st.markdown("<div id='explore'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:#333; margin:50px 0 30px 0;'>🧭 Start Your Journey</h2>", unsafe_allow_html=True)

st.markdown("<div class='button-section'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("📊 Tourism Analytics Dashboard", use_container_width=True):
        st.switch_page("pages/1_Tourism_Dashboard.py")
with col2:
    if st.button("🧳 Travel Packages Explorer", use_container_width=True):
        st.switch_page("pages/2_Travel_Packages_Insights.py")
st.markdown("</div>", unsafe_allow_html=True)

# --------------------- Footer ---------------------
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <h3 style="margin-bottom:20px;">🇮🇳 Incredible India Tourism Platform</h3>
        <p style="margin-bottom:20px;">Explore. Discover. Experience.</p>
        <div class="social-links">
            <span class="social-icon">📧</span>
            <span class="social-icon">🌐</span>
            <span class="social-icon">📱</span>
        </div>
        <div class="credits">
            Developed with ❤️ by <b>Aniket Bharti</b> • Data Visualization & Analysis Project • © 2025
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
