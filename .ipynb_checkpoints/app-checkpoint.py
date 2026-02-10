import streamlit as st
from pathlib import Path
from PIL import Image
import base64

st.set_page_config(page_title="Incredible India 🌏", layout="wide")

# --------------------- CSS ---------------------
st.markdown("""
<style>
/* Page main content */
div[data-testid="stAppViewContainer"] > .main {
    margin-top: 180px;
}

/* Navbar styling */
.navbar {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    display:flex;
    justify-content:center;
    gap:20px;
    z-index:9999;
    background: rgba(255,255,255,0.95);
    padding: 12px 28px;
    border-radius: 14px;
    border: 1px solid rgba(255,204,0,0.4);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}
.nav-btn {
    background: #ff6600;
    padding:10px 20px;
    border-radius:50px;
    color:white;
    font-weight:600;
    text-decoration:none;
    transition: all 0.3s ease;
    border: 1px solid #ffcc00;
}
.nav-btn:hover {
    background: #ffcc00;
    color:#c44f00;
    transform: scale(1.05);
}

/* Main title */
.animated-title {
    font-size:3rem;
    font-weight:800;
    text-align:center;
    background: linear-gradient(90deg,#ff6600,#ffcc00,#ff0099);
    -webkit-background-clip:text;
    color: transparent;
    animation: gradientShift 6s linear infinite;
    font-family: Poppins, sans-serif;
}
@keyframes gradientShift {
    0%{background-position:0% 50%}
    50%{background-position:100% 50%}
    100%{background-position:0% 50%}
}
.subtitle {
    text-align:center; 
    color:#333; 
    margin-top:6px; 
    font-size:1.1rem;
}
.typewriter{
    width: 85%;
    margin: 10px auto 30px auto;
    font-size:1.05rem;
    color:#4a2c15;
    border-right:.12em solid #4a2c15;
    white-space:nowrap;
    overflow:hidden;
    text-align:center;
    animation: typing 5s steps(80,end), blink 0.8s step-end infinite;
}
@keyframes typing{ from {width:0} to {width:100%} }
@keyframes blink{ 50% { border-color: transparent } }

/* Image styling */
div[data-testid="stImage"] img {
    border-radius: 14px;
    transition: transform 0.35s ease, box-shadow 0.35s ease;
    box-shadow: 0 8px 22px rgba(0,0,0,0.12);
}
div[data-testid="stImage"] img:hover {
    transform: translateY(-6px) scale(1.03);
    box-shadow: 0 20px 40px rgba(0,0,0,0.18);
}
.img-caption { 
    text-align:center; 
    font-weight:600; 
    margin-top:8px; 
    color:#222; 
}

/* Buttons styling */
.button-center {
    display:flex;
    justify-content:center;
    gap:24px;
    margin-top:40px;
}
.stButton>button {
    background: linear-gradient(90deg,#ff6600,#ffcc00);
    color:white;
    font-weight:700;
    font-size:18px;
    padding:14px 32px;
    border-radius:12px;
    box-shadow: 0 10px 28px rgba(255,153,51,0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 14px 36px rgba(255,153,51,0.3);
}

/* Footer */
.credits {
    text-align:center; 
    color:#444; 
    margin-top:36px; 
    font-size:0.95rem; 
}
</style>
""", unsafe_allow_html=True)

# --------------------- Background ---------------------
def set_background_local(image_path: str):
    p = Path(image_path)
    if not p.exists():
        st.warning(f"Background image not found: {image_path}")
        return
    data = p.read_bytes()
    b64 = base64.b64encode(data).decode()
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

set_background_local("india.jpg")

# --------------------- Navbar ---------------------
st.markdown("""
<div class="navbar">
  <a class="nav-btn" href="#home">Home</a>
  <a class="nav-btn" href="#gallery">Gallery</a>
  <a class="nav-btn" href="#dashboard">Dashboard</a>
  <a class="nav-btn" href="#about">About</a>
</div>
""", unsafe_allow_html=True)

# --------------------- Header ---------------------
st.markdown("<div id='home' class='animated-title'>🌏 Welcome to Incredible India 🇮🇳</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A journey through nature, culture, history and flavors.</div>", unsafe_allow_html=True)
st.markdown("<div class='typewriter'>From the Taj Mahal to the backwaters of Kerala — discover India's diversity and warmth.</div>", unsafe_allow_html=True)

# --------------------- Image Gallery ---------------------
monuments = [
    ("Taj Mahal, Agra", "tajmahal.jpg"),
    ("Goa Beach", "goa.jpg"),
    ("Jaipur Palace", "jaipur.jpg"),
    ("Himalayas", "himalayas.jpg"),
    ("Kerala Backwaters", "kerala.jpg"),
]
TARGET_WIDTH = 560
TARGET_HEIGHT = 360

def load_and_resize(path, w=TARGET_WIDTH, h=TARGET_HEIGHT):
    p = Path(path)
    if not p.exists():
        return None
    img = Image.open(p).convert("RGB")
    img = img.resize((w,h), Image.LANCZOS)
    return img

st.markdown("<div id='gallery'></div>", unsafe_allow_html=True)
# Row 1
col1, col2 = st.columns(2, gap="large")
with col1:
    img = load_and_resize(monuments[0][1])
    if img:
        st.image(img, width=TARGET_WIDTH)
        st.markdown(f"<div class='img-caption'>{monuments[0][0]}</div>", unsafe_allow_html=True)
with col2:
    img = load_and_resize(monuments[1][1])
    if img:
        st.image(img, width=TARGET_WIDTH)
        st.markdown(f"<div class='img-caption'>{monuments[1][0]}</div>", unsafe_allow_html=True)

# Row 2
col3, col4 = st.columns(2, gap="large")
with col3:
    img = load_and_resize(monuments[2][1])
    if img:
        st.image(img, width=TARGET_WIDTH)
        st.markdown(f"<div class='img-caption'>{monuments[2][0]}</div>", unsafe_allow_html=True)
with col4:
    img = load_and_resize(monuments[3][1])
    if img:
        st.image(img, width=TARGET_WIDTH)
        st.markdown(f"<div class='img-caption'>{monuments[3][0]}</div>", unsafe_allow_html=True)

# Row 3 - Center image
center_col_left, center_col_mid, center_col_right = st.columns([1,2,1])
with center_col_mid:
    img = load_and_resize(monuments[4][1], w=int(TARGET_WIDTH*1.05), h=int(TARGET_HEIGHT*1.05))
    if img:
        st.image(img, width=int(TARGET_WIDTH*1.05))
        st.markdown(f"<div class='img-caption'>{monuments[4][0]}</div>", unsafe_allow_html=True)

# --------------------- Buttons ---------------------
st.markdown("<div id='dashboard'></div>", unsafe_allow_html=True)
st.markdown("<div class='button-center'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("🧭 Start Exploring the Dashboard"):
        st.switch_page("pages/1_Tourism_Dashboard.py")
with col2:
    if st.button("📊 Explore Travel Packages Insights"):
        st.switch_page("pages/2_Travel_Packages_Insights.py")
st.markdown("</div>", unsafe_allow_html=True)

# --------------------- Footer ---------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div id='about' class='credits'>Developed with ❤️ by <b>Aniket Bharti</b> • Data Visualization Project • © 2025</div>", unsafe_allow_html=True)
