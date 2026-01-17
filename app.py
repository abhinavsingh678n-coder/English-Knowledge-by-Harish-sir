import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os

# 1. PAGE CONFIG
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide")

# Google STUN Servers (Global link ke liye zaruri)
RTC_CONFIG = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]}]})

# Database Sync Logic
def update_status(key, val):
    with open(f"{key}.txt", "w") as f: f.write(val)

def read_status(key):
    if not os.path.exists(f"{key}.txt"): return "OFF"
    with open(f"{key}.txt", "r") as f: return f.read().strip()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'role' not in st.session_state: st.session_state.role = "Student"

# --- LOGIN SYSTEM ---
if not st.session_state.logged_in:
    st.title("🎓 English Knowledge Login")
    u_n = st.text_input("Apna Naam")
    u_m = st.text_input("Mobile Number (10 Digits)")
    if st.button("Login as Student"):
        if u_n and len(u_m.strip()) == 10:
            st.session_state.logged_in = True; st.session_state.u_name = u_n; st.rerun()
    
    with st.expander("👨‍🏫 Teacher Access"):
        if st.text_input("Security Key", type="password") == "harish_sir_pro":
            if st.button("Sir Login"): 
                st.session_state.role = "Admin"; st.session_state.logged_in = True; st.rerun()
    st.stop()

# --- APP INTERFACE ---
live_state = read_status("live")
call_state = read_status("call")

if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Control Panel")
    is_live = st.toggle("🔴 START LIVE CLASS", value=(live_state == "ON"))
    update_status("live", "ON" if is_live else "OFF")
    
    if is_live:
        st.success("✅ Aap Live Hain! Bache ab join kar sakte hain.")
        webrtc_streamer(key="sir-global", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIG, media_stream_constraints={"video": True, "audio": True})
        st.divider()
        is_call = st.toggle("📞 Start Interaction (Video Call)", value=(call_state == "ON"))
        update_status("call", "ON" if is_call else "OFF")
else:
    st.title(f"Namaste, {st.session_state.u_name}")
    if live_state == "ON":
        st.markdown("""<div style="background-color:#ff4b4b; color:white; padding:15px; border-radius:10px; text-align:center; border: 2px solid white;"><h3>🔴 HARISH SIR IS LIVE NOW!</h3></div>""", unsafe_allow_html=True)
        if st.button("▶️ JOIN LIVE CLASS NOW", use_container_width=True):
            st.session_state.joined = True
        if st.session_state.get('joined', False):
            if call_state == "ON":
                st.warning("📞 Face-to-Face Mode Active!")
                webrtc_streamer(key="stu-global-call", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIG)
            else:
                st.info("📺 Watching Harish Sir Live...")
                webrtc_streamer(key="stu-global-view", mode=WebRtcMode.RECVONLY, rtc_configuration=RTC_CONFIG)
            if st.button("Leave Class"): st.session_state.joined = False; st.rerun()
    else:
        st.info("Sir abhi live nahi hain. Sabhi bacho ko batayein ki class shuru hone par yahan Join button dikhega.")