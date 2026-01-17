import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os

# 1. PAGE SETTINGS
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Google STUN Servers
RTC_CONFIG = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# Database Sync
def update_db(key, val):
    with open(f"{key}.txt", "w") as f: f.write(val)

def read_db(key):
    if not os.path.exists(f"{key}.txt"): return "OFF"
    with open(f"{key}.txt", "r") as f: return f.read().strip()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'role' not in st.session_state: st.session_state.role = "Student"

# --- LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>📖 English Knowledge</h1>", unsafe_allow_html=True)
    u_n = st.text_input("Naam")
    u_m = st.text_input("Mobile (10 Digits)")
    if st.button("Login"):
        if u_n and len(u_m.strip()) == 10:
            st.session_state.logged_in = True
            st.session_state.u_name = u_n
            st.session_state.u_id = u_m.strip()
            st.rerun()
    with st.expander("Admin Access"):
        if st.text_input("Password", type="password") == "harish_sir_pro":
            if st.button("Sir Login"): st.session_state.role = "Admin"; st.session_state.logged_in = True; st.rerun()
    st.stop()

# --- SIDEBAR & PAYMENT SYSTEM ---
with st.sidebar:
    st.markdown(f"## 👤 {st.session_state.u_name if st.session_state.role != 'Admin' else 'Harish Sir'}")
    
    # Check if student is approved (Paid)
    is_paid = os.path.exists(f"pay_{st.session_state.get('u_id', '')}.txt")
    
    if st.session_state.role == "Admin":
        st.success("👨‍🏫 ADMIN MODE")
    elif is_paid:
        st.success("✅ PAID USER")
    else:
        st.error("❌ FREE USER")
        st.subheader("💳 Buy Full Course (₹499)")
        # BAR CODE (QR Code) for Harish Sir
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=harishsir@upi&pn=Harish%20Sir&am=499", caption="Scan & Pay ₹499")
        st.write("Scan karke screenshot WhatsApp karein.")
        st.markdown("[WhatsApp Screenshot](https://wa.me/919999999999)")

    st.divider()
    menu = st.radio("Menu", ["🏠 Dashboard", "🔴 Live Class", "📂 Free Material"])
    if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- MAIN INTERFACE ---
live_state = read_db("live")

if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir Admin Panel")
    col1, col2 = st.columns(2)
    with col1:
        is_live = st.toggle("🔴 LIVE CLASS START", value=(live_state == "ON"))
        update_db("live", "ON" if is_live else "OFF")
    with col2:
        stu_id = st.text_input("Student Number to Approve")
        if st.button("Approve Payment"):
            with open(f"pay_{stu_id}.txt", "w") as f: f.write("PAID")
            st.success(f"Student {stu_id} Approved!")

    if is_live:
        webrtc_streamer(key="sir-final", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIG)

else:
    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.u_name}")
        if live_state == "ON":
            st.markdown("<div style='background-color:red; color:white; padding:10px; text-align:center;'><h2>🔴 HARISH SIR IS LIVE!</h2></div>", unsafe_allow_html=True)
        else:
            st.info("Sir abhi live nahi hain.")

    elif menu == "🔴 Live Class":
        if live_state == "ON":
            if is_paid:
                st.success("Access Granted!")
                webrtc_streamer(key="stu-final", mode=WebRtcMode.RECVONLY, rtc_configuration=RTC_CONFIG)
            else:
                st.error("🔒 PAID CLASS: Pehle payment karein (Sidebar mein scanner hai).")
        else:
            st.info("Class abhi band hai.")