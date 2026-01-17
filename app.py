import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os

# 1. PAGE SETTINGS
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide")

# Google STUN Servers (Mobile networks par video chalane ke liye zaruri)
RTC_CONFIG = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]}]})

# Database Sync Logic (Sir aur Student ko jodne ke liye)
def update_status(key, val):
    with open(f"{key}.txt", "w") as f: f.write(val)

def read_status(key):
    if not os.path.exists(f"{key}.txt"): return "OFF"
    with open(f"{key}.txt", "r") as f: return f.read().strip()

# Initialize Local Session
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'role' not in st.session_state: st.session_state.role = "Student"

# --- LOGIN SYSTEM (10-Digit Check) ---
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

# TEACHER PANEL
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Master Control")
    is_live = st.toggle("🔴 START LIVE CLASS", value=(live_state == "ON"))
    update_status("live", "ON" if is_live else "OFF")
    
    if is_live:
        st.success("✅ Aap Live Hain! Bache ab join kar sakte hain.")
        # Teacher sends video and audio
        webrtc_streamer(key="sir-stream-v15", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIG, media_stream_constraints={"video": True, "audio": True})
        
        st.divider()
        is_call = st.toggle("📞 Start Video Call Interaction", value=(call_state == "ON"))
        update_status("call", "ON" if is_call else "OFF")
    else:
        update_status("call", "OFF")

# STUDENT PANEL (PW Style)
else:
    st.title(f"Namaste, {st.session_state.u_name}")
    
    if live_state == "ON":
        # PW Style Notification Box
        st.markdown("""<div style="background-color:#ff4b4b; color:white; padding:15px; border-radius:10px; text-align:center; border: 2px solid white;"><h3>🔴 HARISH SIR IS LIVE NOW!</h3></div>""", unsafe_allow_html=True)
        
        if st.button("▶️ JOIN LIVE CLASS NOW", use_container_width=True):
            st.session_state.joined = True

        if st.session_state.get('joined', False):
            # Interaction or View Only
            if call_state == "ON":
                st.warning("📞 Interaction Mode: Sir is talking to you face-to-face!")
                webrtc_streamer(key="stu-call-v15", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIG)
            else:
                st.info("📺 Watching Harish Sir Live...")
                # Student receives teacher's stream
                webrtc_streamer(key="stu-view-v15", mode=WebRtcMode.RECVONLY, rtc_configuration=RTC_CONFIG)
            
            if st.button("Leave Class"): st.session_state.joined = False; st.rerun()
    else:
        st.info("Abhi koi Live class nahi chal rahi hai. Sir ke aate hi Join button aa jayega.")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg")