import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os

# 1. PAGE SETTINGS
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# --- ADVANCED VIDEO SYNC (Mobile Network Fix) ---
# Ye configuration video ko 4G/5G mobile par chalane ke liye zaruri hai
RTC_CONFIG = RTCConfiguration(
    {"iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
        {"urls": ["stun:stun2.l.google.com:19302"]}
    ]}
)

# --- DATABASE SYNC LOGIC ---
def update_db(key, val):
    with open(f"{key}.txt", "w") as f: f.write(val)

def read_db(key):
    if not os.path.exists(f"{key}.txt"): return "OFF"
    with open(f"{key}.txt", "r") as f: return f.read().strip()

# Initialize Local Session
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'role' not in st.session_state: st.session_state.role = "Student"

# --- LOGIN SYSTEM ---
if not st.session_state.logged_in:
    st.title("🎓 English Knowledge Login")
    tab_st, tab_sir = st.tabs(["Student Entry", "Harish Sir Access"])
    
    with tab_st:
        u_name = st.text_input("Apna Naam")
        u_mob = st.text_input("Mobile (10 Digits Only)")
        if st.button("Login as Student"):
            if u_name and len(u_mob.strip()) == 10:
                st.session_state.logged_in = True; st.session_state.u_name = u_name; st.session_state.u_id = u_mob.strip(); st.rerun()
            else: st.error("❌ Sahi Naam aur 10-digit number dalein.")

    with tab_sir:
        pwd = st.text_input("Security Key", type="password")
        if st.button("Admin Login"):
            if pwd == "harish_sir_pro":
                st.session_state.role = "Admin"; st.session_state.logged_in = True; st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("📖 English Knowledge")
    st.caption("By Harish Sir")
    menu = st.radio("Navigation", ["🏠 Dashboard", "🎥 Recorded", "📚 Notes", "💬 Doubts"])
    if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- ADMIN PANEL (Teacher Control) ---
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Master Control")
    # Live Status Toggle
    is_live = st.toggle("🔴 START LIVE CLASS", value=(read_db("live") == "ON"))
    update_db("live", "ON" if is_live else "OFF")
    
    if is_live:
        st.success("✅ Aap Live Hain! Bache ab 'Join' button dekh sakte hain.")
        # TEACHER VIDEO (SEND & RECEIVE)
        webrtc_streamer(
            key="sir-stream-final", 
            mode=WebRtcMode.SENDRECV, 
            rtc_configuration=RTC_CONFIG,
            media_stream_constraints={"video": True, "audio": True}
        )
        
        st.divider()
        # Interaction Control
        is_call = st.toggle("📞 Start Video Call Interaction", value=(read_db("call") == "ON"))
        update_db("call", "ON" if is_call else "OFF")
    else:
        update_db("call", "OFF")

# --- STUDENT PANEL (PW Style Logic) ---
else:
    live_now = read_db("live")
    call_now = read_db("call")
    
    if live_now == "ON":
        st.markdown("""
            <div style="background-color:#ff4b4b; color:white; padding:15px; border-radius:10px; text-align:center; border: 2px solid white;">
                <h2>🔴 HARISH SIR IS LIVE NOW!</h2>
                <p>Niche button par click karke class join karein.</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("▶️ JOIN LIVE CLASS NOW", use_container_width=True):
            st.session_state.joined = True

        if st.session_state.get('joined', False):
            # Dynamic Switching: Video Call or Just Lecture
            if call_now == "ON":
                st.warning("📞 Interaction Mode: Sir is talking to you face-to-face!")
                webrtc_streamer(key="stu-interaction-final", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIG)
            else:
                st.info("📺 Watching Harish Sir Live...")
                # RECVONLY means student only watches teacher
                webrtc_streamer(key="stu-view-final", mode=WebRtcMode.RECVONLY, rtc_configuration=RTC_CONFIG)
            
            if st.button("Leave Class"): st.session_state.joined = False; st.rerun()
    
    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.u_name}")
        if live_now == "OFF": 
            st.info("Abhi koi Live class nahi chal rahi hai. Jab Sir live honge, yahan JOIN button aa jayega.")
        else:
            st.success("Harish Sir Live hain! Upar Join button par click karein.")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg")