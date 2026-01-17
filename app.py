import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os

# 1. PAGE SETTINGS
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide")

# Google STUN Servers
RTC_CONFIG = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# Database Logic (Files based)
def update_db(key, val):
    with open(f"{key}.txt", "w") as f: f.write(val)

def read_db(key):
    if not os.path.exists(f"{key}.txt"): return "OFF"
    with open(f"{key}.txt", "r") as f: return f.read().strip()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'role' not in st.session_state: st.session_state.role = "Student"

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🎓 English Knowledge Login")
    u_n = st.text_input("Naam")
    u_m = st.text_input("Mobile (10 Digits)")
    if st.button("Enter Classroom"):
        if u_n and len(u_m.strip()) == 10:
            st.session_state.logged_in = True; st.session_state.u_name = u_n; st.session_state.u_id = u_m.strip(); st.rerun()
    with st.expander("Admin Access"):
        if st.text_input("Password", type="password") == "harish_sir_pro":
            if st.button("Sir Login"): st.session_state.role = "Admin"; st.session_state.logged_in = True; st.rerun()
    st.stop()

# --- SIDEBAR (Updated with Screenshot features) ---
with st.sidebar:
    st.header(f"👤 {st.session_state.u_name if st.session_state.role != 'Admin' else 'Harish Sir'}")
    st.caption("Organization Code: YICKLF")
    
    # PAID STATUS CHECK
    is_paid = os.path.exists(f"pay_{st.session_state.get('u_id', '')}.txt")
    if st.session_state.role == "Admin" or is_paid:
        st.success("✅ PAID USER")
    else:
        st.error("❌ FREE USER")
        st.subheader("💳 Unlock Full Course")
        # Barcode/Scanner Image
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=harishsir@upi&pn=Harish%20Sir&am=499", caption="Scan & Pay ₹499")
        st.markdown("[WhatsApp Screenshot](https://wa.me/919999999999)")

    st.divider()
    menu = st.radio("Menu", ["🏠 Dashboard", "🔴 Live Class", "🎥 Recorded", "📂 Free Material"])
    if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- INTERFACE ---
live_state = read_db("live")

if st.session_state.role == "Admin":
    st.header("👨‍🏫 Master Control")
    col1, col2 = st.columns(2)
    with col1:
        is_live = st.toggle("🔴 START CLASS", value=(live_state == "ON"))
        update_db("live", "ON" if is_live else "OFF")
    with col2:
        stu_id = st.text_input("Student Mobile to Approve")
        if st.button("Activate Student"):
            with open(f"pay_{stu_id}.txt", "w") as f: f.write("PAID")
            st.success(f"Student {stu_id} is now Paid!")

    if is_live:
        webrtc_streamer(key="sir-live-final", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIG)
else:
    if menu == "🏠 Dashboard":
        st.title(f"Hi, {st.session_state.u_name}")
        if live_state == "ON":
            st.markdown("<div style='background-color:red; color:white; padding:20px; border-radius:10px; text-align:center;'><h1>🔴 LIVE CLASS ON!</h1><p>Join from sidebar</p></div>", unsafe_allow_html=True)
        else:
            st.info("Sir is not live.")
    elif menu == "🔴 Live Class":
        if live_state == "ON":
            if is_paid:
                webrtc_streamer(key="stu-live-final", mode=WebRtcMode.RECVONLY, rtc_configuration=RTC_CONFIG)
            else:
                st.error("🔒 Paid Course: Please pay and send screenshot to join.")
        else: st.info("Class is off.")