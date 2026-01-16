import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import time

# 1. PAGE SETTINGS
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage Initialization
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'is_live' not in st.session_state: st.session_state.is_live = False 
if 'call_active' not in st.session_state: st.session_state.call_active = False 
if 'active_poll' not in st.session_state: st.session_state.active_poll = None
if 'poll_results' not in st.session_state: st.session_state.poll_results = {}
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- LOGIN SYSTEM (Strict 10-Digit Mobile Check) ---
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    
    # Hidden Admin Login for Harish Sir
    with st.expander("👨‍🏫 Harish Sir Access"):
        admin_key = st.text_input("Security Key", type="password")
        if st.button("Admin Login"):
            if admin_key == "harish_sir_pro":
                st.session_state.role = "Admin"
                st.rerun()

    st.write("---")
    st.subheader("Student Classroom Entry")
    u_name = st.text_input("Apna Naam")
    u_mobile = st.text_input("Mobile Number (10 Digits Only)")
    
    if st.button("Enter Classroom"):
        clean_num = u_mobile.strip()
        # Requirement: Exactly 10 digits for mobile login
        if u_name and clean_num.isdigit() and len(clean_num) == 10:
            st.session_state.logged_in = True
            st.session_state.user_name = u_name
            st.session_state.user_id = clean_num
            st.rerun()
        else:
            st.error("❌ Galat Entry! Naam aur 10-digit mobile number bharein.")
    st.stop()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown(f"### 📖 English Knowledge\n**By Harish Sir**")
    st.divider()
    menu = st.radio("Menu", ["🏠 Dashboard", "🎥 Recorded Classes", "📂 My Notes", "❓ Ask Doubt"])
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = "Student"
        st.rerun()

# --- ADMIN PANEL (Harish Sir's Control) ---
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Master Control")
    t1, t2, t3 = st.tabs(["🚀 LIVE CLASS CONTROL", "📊 POLLS", "📤 CONTENT"])
    
    with t1:
        if not st.session_state.is_live:
            if st.button("🔴 START LIVE CLASS"):
                st.session_state.is_live = True
                st.rerun()
        else:
            st.success("✅ Aap Live Hain! Bache ab jud sakte hain.")
            # Teacher Stream (Master View)
            webrtc_streamer(key="sir-stream", mode=WebRtcMode.SENDRECV, 
                            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            
            st.divider()
            # Video Call Interaction Toggle
            if not st.session_state.call_active:
                if st.button("📞 Start Interaction (Video Call bacho se)"):