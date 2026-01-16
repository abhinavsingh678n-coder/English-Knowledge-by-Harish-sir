import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import os

# 1. PAGE SETTINGS
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# DATABASE SIMULATION (File based sync for Sir and Students)
def set_live_status(status):
    with open("live_status.txt", "w") as f:
        f.write(status)

def get_live_status():
    if not os.path.exists("live_status.txt"): return "OFF"
    with open("live_status.txt", "r") as f:
        return f.read().strip()

# Initialize Local Session Data
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'homework_list' not in st.session_state: st.session_state.homework_list = []

# --- LOGIN SYSTEM ---
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    with st.expander("👨‍🏫 Harish Sir Access"):
        admin_key = st.text_input("Security Key", type="password")
        if st.button("Admin Login"):
            if admin_key == "harish_sir_pro":
                st.session_state.role = "Admin"
                st.rerun()

    st.subheader("Student Login")
    u_name = st.text_input("Apna Naam")
    u_mobile = st.text_input("Mobile Number (10 Digits)")
    if st.button("Login"):
        if u_name and len(u_mobile.strip()) == 10:
            st.session_state.logged_in = True
            st.session_state.user_name = u_name
            st.session_state.user_id = u_mobile.strip()
            st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("📖 English Knowledge")
    st.caption("By Harish Sir")
    st.divider()
    menu = st.radio("Navigation", ["🏠 Dashboard", "🎥 Recorded", "📚 Notes", "💬 Ask Doubts"])
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = "Student"
        st.rerun()

# --- ADMIN PANEL (Harish Sir) ---
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Master Control Panel")
    t1, t2, t3 = st.tabs(["🚀 LIVE CLASS", "📊 POLLS", "📤 CONTENT"])
    
    with t1:
        current_live = get_live_status()
        if current_live == "OFF":
            if st.button("🔴 START LIVE CLASS"):
                set_live_status("ON")
                st.rerun()
        else:
            st.success("✅ Aap Live Hain! Bache ab jud sakte hain.")
            webrtc_streamer(key="sir-stream-v4", mode=WebRtcMode.SENDRECV, 
                            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            
            st.divider()
            interaction = st.toggle("📞 Allow Students Video Call")
            if interaction: set_live_status("INTERACT")
            else: set_live_status("ON")
            
            if st.button("🏁 END FULL CLASS"):
                set_live_status("OFF")
                st.rerun()

# --- STUDENT PANEL (PW Style - Direct Sync) ---
else:
    live_state = get_live_status()
    
    # PW Style Notification Box (Only shows if File says ON or INTERACT)
    if live_state != "OFF":
        st.markdown("""
            <div style="background-color:#ff4b4b; color:white; padding:20px; border-radius:15px; text-align:center; font-weight:bold; margin-bottom:20px; border: 3px solid #ffd700;">
                <h1 style="color:white; margin:0;">🔴 HARISH SIR IS LIVE NOW!</h1>
                <p style="margin:5px 0 0 0; font-size:18px;">Click 'Join' to start learning</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("▶️ JOIN LIVE CLASS NOW", use_container_width=True):
            st.session_state.show_live = True

        if st.session_state.get('show_live', False):
            if live_state == "INTERACT":
                st.warning("📞 Face-to-Face Mode: Sir is talking to you!")
                webrtc_streamer(key="stu-v4-call", mode=WebRtcMode.SENDRECV, 
                                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            else:
                st.info("📺 Watching Harish Sir Live...")
                webrtc_streamer(key="stu-v4-view", mode=WebRtcMode.RECVONLY, 
                                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            
            if st.button("Leave Class"):
                st.session_state.show_live = False
                st.rerun()
    
    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.user_name}")
        if live_state == "OFF":
            st.info("Abhi koi Live class nahi chal rahi hai. Sir ke Live aate hi Join ka button aa jayega.")
        else:
            st.success("Live class chalu hai! Upar 'Join' par click karein.")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg")
    
    # (Recorded, Notes, Doubts logic below)