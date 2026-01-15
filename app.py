import streamlit as st
from streamlit_webrtc import webrtc_streamer

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# 2. SESSION STATE FOR DATA (Permanent storage ke liye Google Sheets zaruri hoga)
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'user_id' not in st.session_state: st.session_state.user_id = ""

# 3. CUSTOM CSS FOR PREMIUM LOOK
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    header {visibility: hidden;}
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3em; }
    .doubt-card { background-color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #1a73e8; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .sidebar-title { text-align: center; color: #1a73e8; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("<h2 class='sidebar-title'>📖 English Knowledge</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>By Harish Sir</p>", unsafe_allow_html=True)
    st.divider()
    
    # Menu for Students
    menu = st.radio("Menu", ["🏠 Dashboard", "🔴 Live Class", "🎥 Recorded Classes", "📂 My Notes", "❓ Ask Doubt"])
    
    st.write("---")
    # Secret Teacher Entry (Bachon ko nahi dikhega jab tak expand na karein)
    with st.expander("👨‍🏫 Teacher Access"):
        admin_pwd = st.text_input("Security Key", type="password")
        if admin_pwd == "harish_sir_pro":
            st.session_state.role = "Admin"
            st.success("Admin Mode Active!")
        else:
            st.session_state.role = "Student"

# 5. ADMIN PANEL LOGIC (Sir ke liye)
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Control Center")
    st.info("Sir, yahan se aap classes aur homework manage karein.")
    
    tab1, tab2, tab3 = st.tabs(["🚀 Live & Recorded", "📤 Homework", "💬 Doubt Panel"])
    
    with tab1:
        st.subheader("Class Management")
        with st.form("class_form", clear_on_submit=True):
            v_title = st.text_input("Topic Name")
            v_link = st.text_input("YouTube Live/Video Link")
            if st.form_submit_button("Publish Class"):
                if v_title and v_link:
                    st.session_state.recorded_classes.insert(0, {"title": v_title, "link": v_link})
                    st.success("Class bacho ke liye live/recorded section mein add ho gayi!")

    with tab2:
        st.subheader("Upload Notes/Homework")
        with st.form("hw_form", clear_on_submit=True):
            h_title = st.text_input("Notes Title")
            h_file = st.file_uploader("Select PDF or Image", type=['pdf', 'jpg', 'png'])
            if st.form_submit_button("Upload Now"):
                if h_title and h_file:
                    st.session_state.homework_list.insert(0, {"title": h_title, "file": h_file})
                    st.success("Homework bacho ke dashboard par pahunch gaya!")

    with tab3:
        st.subheader("💬 Bachon ke Doubts (With Student ID)")
        if not st.session_state.doubts:
            st.info("Abhi koi doubt nahi aaya hai.")
        else:
            for i, d in enumerate(st.session_state.doubts):
                with st.container():
                    st.markdown(f"""
                    <div class='doubt-card'>
                        <strong>Student:</strong> {d['user']} | <strong>ID:</strong> {d['id']}<br>
                        <strong>Question:</strong> {d['question']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if d['answer']: