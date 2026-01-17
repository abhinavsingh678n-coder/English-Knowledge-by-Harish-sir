import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os
import json
import pandas as pd

# 1. ULTRA-PRO UI CONFIG (Bilkul App jaisa look)
st.set_page_config(page_title="Harish Sir Pro App", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Premium App Look */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #F0F4FF; }
    
    /* PW Style Gradient Header */
    .app-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white; padding: 30px; border-radius: 0 0 35px 35px;
        text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Smooth Feature Cards */
    .pro-card {
        background: white; padding: 25px; border-radius: 20px;
        margin-top: -20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 10px solid #1E3A8A;
    }
    
    /* Live Indicator */
    .live-pulse {
        background: red; border-radius: 50%; width: 12px; height: 12px;
        display: inline-block; margin-right: 8px; animation: pulse 1s infinite;
    }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. ADVANCED STREAMING CONFIG (Bina rukawat class ke liye)
RTC_CONFIG = RTCConfiguration(
    {"iceServers": [
        {"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]},
        {"urls": ["stun:stun2.l.google.com:19302", "stun:stun3.l.google.com:19302"]}
    ]}
)

# Data Persistence
DB = "pro_user_data.json"
QR_IMG = "official_scanner.png"

def load_db():
    if os.path.exists(DB):
        with open(DB, "r") as f: return json.load(f)
    return {}

def save_db(data):
    with open(DB, "w") as f: json.dump(data, f)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- AUTHENTICATION ---
if not st.session_state.logged_in:
    st.markdown('<div class="app-header"><h1>🎓 English Knowledge Pro</h1><p>Powered by Harish Sir</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        t_log, t_reg, t_adm = st.tabs(["🔑 Login", "📝 Register", "👨‍🏫 Admin"])
        db = load_db()

        with t_log:
            mob = st.text_input("Mobile No.")
            pas = st.text_input("Password", type="password")
            if st.button("LOG IN", use_container_width=True):
                if mob in db and db[mob]['password'] == pas:
                    st.session_state.logged_in = True; st.session_state.u_id = mob; st.session_state.u_name = db[mob]['name']; st.session_state.role = "Student"; st.rerun()
                else: st.error("Wrong Details!")

        with t_reg:
            name = st.text_input("Name")
            rm = st.text_input("10 Digit Mobile")
            rp = st.text_input("Create Password", type="password")
            if st.button("CREATE ACCOUNT", use_container_width=True):
                if len(rm) == 10:
                    db[rm] = {"name": name, "password": rp, "paid": False}; save_db(db); st.success("Ready! Please Login.")
        
        with t_adm:
            if st.text_input("Sir Key", type="password") == "harish_sir_pro":
                if st.button("Admin Entry"): st.session_state.logged_in = True; st.session_state.role = "Admin"; st.session_state.u_name = "Harish Sir"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- APP INTERFACE ---
with st.sidebar:
    st.markdown(f"### Welcome\n## {st.session_state.u_name}")
    st.caption("Premium Account Status: Active ✅")
    
    db = load_db()
    is_paid = db.get(st.session_state.get('u_id',''), {}).get("paid", False) if st.session_state.role != "Admin" else True
    
    if not is_paid:
        st.warning("🔒 Course Locked")
        if os.path.exists(QR_IMG): st.image(QR_IMG, caption="Scan to Pay ₹499")
        st.markdown(f"[WhatsApp Screenshot](https://wa.me/919999999999?text=ID:{st.session_state.u_id})")
    
    menu = st.radio("Navigation", ["🏠 Home", "🔴 Live Class", "📝 Homework", "❓ Doubt Panel"])
    if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- LOGIC ENGINE ---
live_state = "ON" if os.path.exists("live_active.txt") and open("live_active.txt").read() == "ON" else "OFF"

if st.session_state.role == "Admin":
    st.title("👨‍🏫 Harish Sir's Control Center")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("1. Stream Management")
        if st.toggle("Start Live Class", value=(live_state == "ON")):
            with open("live_active.txt", "w") as f: f.write("ON")
            webrtc_streamer(key="admin_stream", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIG, media_stream_constraints={"video": True, "audio": True})
        else: open("live_active.txt", "w").write("OFF")

    with col_b:
        st.subheader("2. Student Approval")
        m_app = st.text_input("Student Mobile Number")
        if st.button("Approve Student"):
            db = load_db(); db[m_app]["paid"] = True; save_db(db); st.success("Access Granted!")

else: # Student Logic
    if menu == "🏠 Home":
        st.markdown(f'<div class="app-header"><h2>Welcome, {st.session_state.u_name}</h2></div>', unsafe_allow_html=True)
        if live_state == "ON":
            st.markdown('<div class="pro-card"><h3><span class="live-pulse"></span> Harish Sir is LIVE!</h3><p>Go to "Live Class" tab to join.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="pro-card"><h3>📚 Latest Material</h3><p>Tense & Verbs notes uploaded in PDF.</p></div>', unsafe_allow_html=True)

    elif menu == "🔴 Live Class":
        if is_paid:
            if live_state == "ON":
                st.success("Connected to Harish Sir's Classroom")
                webrtc_streamer(key="student_stream", mode=WebRtcMode.RECVONLY, rtc_configuration=RTC_CONFIG, media_stream_constraints={"video": True, "audio": True})
            else: st.info("Abhi koi live class nahi chal rahi hai.")
        else: st.error("🔒 Please unlock the course to watch live classes.")