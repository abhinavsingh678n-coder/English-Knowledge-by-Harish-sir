import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os
import json

# 1. PAGE SETUP
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide")

# CSS for Professional Look
st.markdown("""
    <style>
    .card { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 10px solid #ff4b4b; margin-bottom: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# Files
USER_DB = "users_data.json"
QR_IMAGE_PATH = "harish_qr.png"

def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f: return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB, "w") as f: json.dump(users, f)

def read_db(key):
    if not os.path.exists(f"{key}.txt"): return "OFF"
    with open(f"{key}.txt", "r") as f: return f.read().strip()

# Initialize Session State
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'u_name' not in st.session_state: st.session_state.u_name = ""

# --- LOGIN & REGISTER ---
if not st.session_state.logged_in:
    st.title("📖 English Knowledge - Harish Sir")
    tab1, tab2, tab3 = st.tabs(["Student Login", "Register", "Admin Login"])
    users = load_users()

    with tab1:
        l_mob = st.text_input("Mobile No.")
        l_pass = st.text_input("Password", type="password")
        if st.button("Login"):
            if l_mob in users and users[l_mob]['password'] == l_pass:
                st.session_state.logged_in = True
                st.session_state.u_id = l_mob
                st.session_state.u_name = users[l_mob]['name']
                st.session_state.role = "Student"
                st.rerun()
            else: st.error("Galat Number/Password")

    with tab2:
        r_name = st.text_input("Naam")
        r_mob = st.text_input("Mobile (10 Digits)")
        r_pass = st.text_input("Password", type="password")
        if st.button("Create Account"):
            if len(r_mob) == 10:
                users[r_mob] = {"name": r_name, "password": r_pass, "paid": False}
                save_users(users)
                st.success("Account Ready! Ab Login karein.")

    with tab3:
        if st.text_input("Sir Key", type="password") == "harish_sir_pro":
            if st.button("Admin Login"):
                st.session_state.logged_in = True
                st.session_state.u_name = "Harish Sir"
                st.session_state.role = "Admin"
                st.rerun()
    st.stop()

# --- APP INTERFACE ---
with st.sidebar:
    st.header(f"👤 {st.session_state.u_name}")
    st.caption("Organization Code YICKLF")
    
    if st.session_state.role == "Student":
        users = load_users()
        is_paid = users[st.session_state.u_id].get("paid", False)
        if is_paid: st.success("✅ PAID USER")
        else:
            st.error("❌ ACCESS LOCKED")
            if os.path.exists(QR_IMAGE_PATH): st.image(QR_IMAGE_PATH, caption="Scan to Pay ₹499")
            else: st.warning("Sir ne QR upload nahi kiya.")
            st.markdown(f"[Send Screenshot to Sir](https://wa.me/919999999999?text=Mera%20ID:{st.session_state.u_id})")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- MAIN DASHBOARD ---
live_state = read_db("live")

if st.session_state.role == "Admin":
    st.title("👨‍🏫 Sir Control Panel")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📤 QR Upload")
        qr_up = st.file_uploader("Upload Bar Code", type=['png','jpg'])
        if qr_up:
            with open(QR_IMAGE_PATH, "wb") as f: f.write(qr_up.getbuffer())
            st.success("QR Updated!")
        
        st.subheader("🔴 Live Class")
        if st.toggle("Go Live", value=(live_state == "ON")):
            with open("live.txt", "w") as f: f.write("ON")
            webrtc_streamer(key="sir", mode=WebRtcMode.SENDRECV, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else:
            with open("live.txt", "w") as f: f.write("OFF")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("✅ Approve Student")
        users = load_users()
        m_app = st.text_input("Mobile No. to Approve")
        if st.button("Give Full Access"):
            if m_app in users:
                users[m_app]["paid"] = True
                save_users(users)
                st.success("Approved!")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.title("English Knowledge Dashboard")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if live_state == "ON":
        users = load_users()
        if users[st.session_state.u_id].get("paid"):
            st.success("Sir is Live!")
            webrtc_streamer(key="stu", mode=WebRtcMode.RECVONLY, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else: st.error("🔒 Locked: Please Pay ₹499 first.")
    else: st.info("No Live Class at the moment.")
    st.markdown('</div>', unsafe_allow_html=True)