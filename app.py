import streamlit as st

# 1. Page Configuration - Browser ke nishaan mitane ke liye
st.set_page_config(
    page_title="Selection Way",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Professional App UI (CSS)
st.markdown("""
    <style>
    /* Header, Footer aur Menu chhupane ke liye */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* App ka Background aur Font */
    .stApp {
        background-color: #f0f2f5;
    }
    
    /* Professional Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #1a73e8;
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Cards Style */
    .course-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. App Body
st.markdown("<h1 style='text-align: center; color: #1a73e8;'>Selection Way</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #5f6368;'>Education for Bright Future</p>", unsafe_allow_html=True)

# Live Class Section
st.markdown('<div class="course-card">', unsafe_allow_html=True)
st.subheader("🔴 Live Classroom")
st.write("Harish Sir is ready to teach. Click below to join.")
if st.button("JOIN LIVE CLASS"):
    # Bina kisi redirection ke video room mein bhejne ke liye
    st.markdown(f'<meta http-equiv="refresh" content="0;URL=https://meet.jit.si/SelectionWay_Pro_Room">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Study Material Section
st.markdown('<div class="course-card">', unsafe_allow_html=True)
st.subheader("📚 Free Study Material")
st.write("Download daily notes and practice sets.")
if st.button("Access Notes"):
    st.info("Notes Section Coming Soon!")
st.markdown('</div>', unsafe_allow_html=True)