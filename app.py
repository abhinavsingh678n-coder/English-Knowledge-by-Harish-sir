import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os

# 1. PAGE SETTINGS
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Signaling Configuration (Google's Public Server for Video Sync)
RTC_CONFIG = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# GLOBAL STATUS SYNC (File based)
def set_status(key, val):
    with open(f"{key}.txt", "w") as f: f.write(val)

def get_status(key):
    if not os.path.exists(f"{key}.txt"): return "OFF"
    with open(f"{key}.txt", "r") as f: return f.read().strip()

# Initialize Local Session
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'role' not in st.session_state: st.session_state.role = "Student"

# --- LOGIN SYSTEM ---
if not st.session_state.logged_in:
    st.title("🎓 English Knowledge Login")
    with st.expander("👨‍🏫 Harish Sir Access"):
        if st.text_input("Security Key", type="password") == "harish_sir_pro":
            if st.button("Admin Login"):
                st.session_state.role = "Admin"; st.session_state.logged_in = True; st.rerun()

    u_name = st.text_input("Apna Naam")
    u_mobile = st.text_input("Mobile Number (10 Digits)")
    if st.button("Login as Student"):
        if u_name and len(u_mobile.strip()) == 10:
            st.session_state.logged_in = True; st.session_state.user_name = u_name; st.session_state.user_id = u_mobile.strip(); st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("📖 English Knowledge")
    st.caption("By Harish Sir")
    menu = st.radio("Navigation", ["🏠 Dashboard", "🎥 Recorded", "📚 Notes", "💬 Ask Doubts"])
    if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- ADMIN PANEL (Harish Sir) ---
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Master Control Panel")
    t1, t2 = st.tabs(["🚀 LIVE CLASS", "📊 POLLS"])
    
    with t1:
        # Toggle Live Status
        is_live = st.toggle("🔴 START LIVE CLASS", value=(get_status("live") == "ON"))
        set_status("live", "ON" if is_live else "OFF")
        
        if is_live:
            st.success("✅ Aap Live Hain! Bache ab jud sakte hain.")
            # SIR'S CAMERA (SEND ONLY)
            webrtc_streamer(key="sir-main", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIG)
            
            st.divider()
            is_call = st.toggle("📞 Start Video Call Interaction", value=(get_status("call") == "ON"))
            set_status("call", "ON" if is_call else "OFF")
        else:
            set_status("call", "OFF")

# --- STUDENT PANEL (PW Style) ---
else:
    live_state = get_status("live")
    call_state = get_status("call")
    
    if live_state == "ON":
        st.markdown("""
            <div style="background-color:#ff4b4b; color:white; padding:20px; border-radius:15px; text-align:center; border: 3px solid white;">
                <h2 style="color:white; margin:0;">🔴 HARISH SIR IS LIVE NOW!</h2>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("▶️ JOIN LIVE CLASS NOW", use_container_width=True):
            st.session_state.joined = True

        if st.session_state.get('joined', False):
            # PW Mode Logic
            if call_state == "ON":
                st.warning("📞 Video Call Active: Sir is talking to you!")
                webrtc_streamer(key="stu-interaction", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIG)
            else:
                st.info("📺 Watching Harish Sir Live...")
                webrtc_streamer(key="stu-view", mode=WebRtcMode.RECVONLY, rtc_configuration=RTC_CONFIG)
            
            if st.button("Leave Class"): st.session_state.joined = False; st.rerun()

    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.user_name}")
        if live_state == "OFF": st.info("Abhi koi Live class nahi chal rahi hai.")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg")