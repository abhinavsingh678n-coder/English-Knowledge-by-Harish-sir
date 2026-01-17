import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os

# 1. PAGE SETTINGS & BRANDING
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Branding Header
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>📖 English Knowledge</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>By: Harish Sir</h3>", unsafe_allow_html=True)
st.write("---")

# Video Sync Config (Global Fix)
RTC_CONFIG = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]}]})

# Database Sync Logic
def set_st(key, val):
    with open(f"{key}.txt", "w") as f: f.write(val)

def get_st(key):
    if not os.path.exists(f"{key}.txt"): return "OFF"
    with open(f"{key}.txt", "r") as f: return f.read().strip()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'role' not in st.session_state: st.session_state.role = "Student"

# --- LOGIN SYSTEM ---
if not st.session_state.logged_in:
    st.subheader("🎓 Student Classroom Login")
    u_n = st.text_input("Apna Pura Naam")
    u_m = st.text_input("Mobile Number (10 Digits)")
    if st.button("Enter Classroom"):
        if u_n and len(u_m.strip()) == 10:
            st.session_state.logged_in = True; st.session_state.u_name = u_n; st.rerun()
        else: st.error("❌ Sahi 10-digit number aur naam bharein.")

    with st.expander("👨‍🏫 Harish Sir Access (Staff Only)"):
        if st.text_input("Staff Security Key", type="password") == "harish_sir_pro":
            if st.button("Sir Login"): 
                st.session_state.role = "Admin"; st.session_state.logged_in = True; st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg")
    st.title("English Knowledge")
    st.caption("Guide: Harish Sir")
    st.divider()
    menu = st.radio("Navigation", ["🏠 Dashboard", "🎥 Recorded", "📚 Notes", "💬 Doubts"])
    if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- APP INTERFACE ---
live_now = get_st("live")
call_now = get_st("call")

if st.session_state.role == "Admin":
    st.header("👨‍🏫 Master Control Panel")
    is_live = st.toggle("🔴 START LIVE CLASS", value=(live_now == "ON"))
    set_st("live", "ON" if is_live else "OFF")
    
    if is_live:
        st.success("✅ Aap Live Hain! Bache ab join kar sakte hain.")
        # Teacher Video
        webrtc_streamer(key="sir-branded-v1", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIG)
        st.divider()
        is_call = st.toggle("📞 Start Interaction Mode", value=(call_now == "ON"))
        set_st("call", "ON" if is_call else "OFF")

else:
    if live_now == "ON":
        st.markdown(f"""
            <div style="background-color:#ff4b4b; color:white; padding:20px; border-radius:15px; text-align:center; border: 3px solid #ffd700;">
                <h1 style="color:white; margin:0;">🔴 HARISH SIR IS LIVE NOW!</h1>
                <p style="margin:5px 0 0 0; font-size:18px;">Click below to join the classroom</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("▶️ JOIN HARISH SIR'S CLASS", use_container_width=True):
            st.session_state.joined = True

        if st.session_state.get('joined', False):
            if call_now == "ON":
                st.warning("📞 Face-to-Face Mode: Sir is talking to you!")
                webrtc_streamer(key="stu-branded-call", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIG)
            else:
                st.info("📺 Watching Harish Sir Live...")
                # Student View
                webrtc_streamer(key="stu-branded-view", mode=WebRtcMode.RECVONLY, rtc_configuration=RTC_CONFIG)
            
            if st.button("Leave Class"): st.session_state.joined = False; st.rerun()

    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.u_name}")
        if live_now == "OFF": 
            st.info("Harish Sir abhi live nahi hain. Class shuru hote hi yahan 'Join' button aa jayega.")
        else:
            st.success("Harish Sir ki class chalu hai! Upar 'Join' par click karein.")