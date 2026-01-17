import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os
import json
import pandas as pd
from datetime import datetime

# 1. ELITE UI CONFIGURATION
st.set_page_config(page_title="Harish Sir English Pro", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Premium "App" Feel
st.markdown("""
    <style>
    /* Professional PW-Style UI */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #F4F7FE; }
    .hero-section {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF8F8F 100%);
        color: white; padding: 40px; border-radius: 0 0 40px 40px;
        text-align: center; margin-bottom: 25px; box-shadow: 0 10px 20px rgba(255, 75, 75, 0.2);
    }
    .feature-card {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
        border-bottom: 5px solid #FF4B4B; transition: 0.3s;
    }
    .feature-card:hover { transform: translateY(-5px); }
    .nav-bar { background: white; padding: 15px; position: fixed; bottom: 0; width: 100%; display: flex; justify-content: space-around; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# Data Infrastructure
DB_FILE = "education_pro_db.json"
QR_IMG = "official_qr.png"

def load_pro_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {}

def save_pro_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 🟢 PREMIUM LOGIN SYSTEM ---
if not st.session_state.logged_in:
    st.markdown('<div class="hero-section"><h1>🎓 Harish Sir Classes</h1><p>Future of English Learning</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tab_log, tab_reg, tab_adm = st.tabs(["Login", "Sign Up", "Admin Portal"])
        db = load_pro_db()

        with tab_log:
            m = st.text_input("Mobile Number", placeholder="10 Digits")
            p = st.text_input("Password", type="password")
            if st.button("LOGIN NOW", use_container_width=True):
                if m in db and db[m]['password'] == p:
                    st.session_state.logged_in = True; st.session_state.u_id = m; st.session_state.u_name = db[m]['name']; st.session_state.role = "Student"; st.rerun()
                else: st.error("❌ Details galat hain!")

        with tab_reg:
            name = st.text_input("Full Name")
            mob = st.text_input("Mobile", key="rm")
            pas = st.text_input("Set Secure Password", type="password", key="rp")
            if st.button("CREATE ACCOUNT", use_container_width=True):
                if len(mob) == 10 and mob.isdigit():
                    db[mob] = {"name": name, "password": pas, "paid": False}; save_pro_db(db); st.success("🎉 Account Ready!")
                else: st.error("❌ Valid 10-digit number dalein.")

        with tab_adm:
            if st.text_input("Admin Key", type="password") == "harish_sir_pro":
                if st.button("SIR LOGIN"): st.session_state.logged_in = True; st.session_state.u_name = "Harish Sir"; st.session_state.role = "Admin"; st.rerun()
    st.stop()

# --- 🔵 APP DASHBOARD ---
with st.sidebar:
    st.markdown(f'<div style="text-align:center;"><h3>👤 {st.session_state.u_name}</h3></div>', unsafe_allow_html=True)
    st.caption("Org Code: YICKLF | Verified User ✅")
    
    db = load_pro_db()
    is_paid = db.get(st.session_state.get('u_id',''), {}).get("paid", False) if st.session_state.role != "Admin" else True
    
    if not is_paid:
        st.markdown('<div style="background:#FFF0F0; padding:15px; border-radius:15px; text-align:center; border:1px solid #FF4B4B;">', unsafe_allow_html=True)
        st.write("🔒 PREMIUM LOCKED")
        if os.path.exists(QR_IMG): st.image(QR_IMG, caption="Scan to Pay ₹499")
        st.markdown(f"[Send Screenshot](https://wa.me/919999999999?text=UnlockID:{st.session_state.u_id})")
        st.markdown('</div>', unsafe_allow_html=True)
    
    menu = st.radio("Menu", ["🏠 Dashboard", "🔴 Live Class", "❓ Ask Doubt", "📝 Homework", "📂 Resources"])
    if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- 🔴 LIVE & CONTENT ENGINE ---
live_f = "live_status.txt"
live_on = os.path.exists(live_f) and open(live_f).read() == "ON"

if st.session_state.role == "Admin":
    st.title("👨‍🏫 Sir Control Center")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("Manage Live")
        if st.toggle("Start Stream", value=live_on):
            open(live_f, "w").write("ON")
            webrtc_streamer(key="sir_pro", mode=WebRtcMode.SENDRECV, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else: open(live_f, "w").write("OFF")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("Update Barcode")
        qr_up = st.file_uploader("Upload New QR", type=['png','jpg'])
        if qr_up:
            with open(QR_IMG, "wb") as f: f.write(qr_up.getbuffer())
            st.success("QR Updated!")
        st.markdown('</div>', unsafe_allow_html=True)

    m_app = st.text_input("Mobile No. to Approve")
    if st.button("UNLOCK STUDENT ACCESS", use_container_width=True):
        db = load_pro_db(); db[m_app]["paid"] = True; save_pro_db(db); st.success("Student Approved!")

else:
    if menu == "🏠 Dashboard":
        st.markdown(f'<div class="hero-section"><h2>Hello, {st.session_state.u_name}</h2></div>', unsafe_allow_html=True)
        if live_on: st.markdown('<div class="feature-card" style="border-left:10px solid red;">🔴 LIVE CLASS IS ON! Join Now.</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card"><h3>📖 Chapter: Tenses</h3><p>Recorded classes and notes updated.</p></div>', unsafe_allow_html=True)

    elif menu == "🔴 Live Class":
        if is_paid:
            if live_on: webrtc_streamer(key="stu_pro", mode=WebRtcMode.RECVONLY, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            else: st.info("Sir abhi offline hain.")
        else: st.error("🔒 Course purchase kijiye live dekhne ke liye.")