import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os
import json
import qrcode
from io import BytesIO
from datetime import datetime

# 1. PREMIUM MOBILE APP UI CONFIG
st.set_page_config(page_title="Harish Sir English Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Professional PW Styling */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #F4F7FE; }
    
    .app-header {
        background: linear-gradient(135deg, #002E5D 0%, #0056B3 100%);
        color: white; padding: 30px; border-radius: 0 0 35px 35px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .feature-card {
        background: white; padding: 25px; border-radius: 22px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
        border-left: 10px solid #FFD700; /* Golden Theme for Selection Batch */
    }
    
    .live-indicator {
        background: #FF0000; color: white; padding: 4px 12px;
        border-radius: 20px; font-weight: bold; font-size: 11px;
        animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# Data & Security Config
USER_DB = "enterprise_users_v2.json"
SIR_UPI = "8948636213@ybl"
COURSE_PRICE = "499"

def load_db():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f: return json.load(f)
    return {}

def save_db(data):
    with open(USER_DB, "w") as f: json.dump(data, f)

# Professional UPI QR Engine
def generate_pro_qr(upi_id, amount, user_id):
    # Auto-fills name, amount and remarks in the student's payment app
    upi_url = f"upi://pay?pa={upi_id}&pn=Harish_Sir&am={amount}&cu=INR&tn=Selection_Batch_ID_{user_id}"
    qr = qrcode.make(upi_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    return buf.getvalue()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 🔐 SECURE LOGIN / REGISTRATION ---
if not st.session_state.logged_in:
    st.markdown('<div class="app-header"><h1>🎓 ENGLISH KNOWLEDGE PRO</h1><p>Future of Selection Starts Here</p></div>', unsafe_allow_html=True)
    tab_log, tab_reg, tab_adm = st.tabs(["🔑 Login", "✨ New Student", "👨‍🏫 Admin"])
    db = load_db()

    with tab_log:
        m = st.text_input("Registered Mobile Number")
        p = st.text_input("Password", type="password")
        if st.button("LOGIN TO CLASSROOM", use_container_width=True):
            if m in db and db[m]['password'] == p:
                st.session_state.logged_in = True; st.session_state.u_id = m; st.session_state.u_name = db[m]['name']; st.session_state.role = "Student"; st.rerun()
            else: st.error("❌ Invalid Mobile or Password")

    with tab_reg:
        n = st.text_input("Full Name")
        rm = st.text_input("Mobile (10 Digits)")
        rp = st.text_input("Set Secure Password", type="password")
        if st.button("GET STARTED", use_container_width=True):
            if len(rm) == 10 and rm.isdigit():
                db[rm] = {"name": n, "password": rp, "paid": False, "date": str(datetime.now())}
                save_db(db); st.success("✅ Registration Successful! Please Login.")
            else: st.error("❌ Use valid 10-digit Indian mobile number")

    with tab_adm:
        if st.text_input("Master Admin Key", type="password") == "harish_sir_pro":
            if st.button("SIR LOGIN"): st.session_state.logged_in = True; st.session_state.role = "Admin"; st.session_state.u_name = "Harish Sir"; st.rerun()
    st.stop()

# --- 📱 PROFESSIONAL SIDEBAR (PW Menu Style) ---
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.u_name}")
    st.caption("Batch: Selection 2026 | Verified ✅")
    
    db = load_db()
    is_paid = db.get(st.session_state.get('u_id',''), {}).get("paid", False) if st.session_state.role != "Admin" else True
    
    if not is_paid:
        st.markdown('<div class="feature-card" style="border-left:8px solid #FF0000; text-align:center;">', unsafe_allow_html=True)
        st.write("🔒 PREMIUM LOCKED")
        # Dynamic QR for Harish Sir
        qr_img = generate_pro_qr(SIR_UPI, COURSE_PRICE, st.session_state.u_id)
        st.image(qr_img, caption=f"Scan to Unlock for ₹{COURSE_PRICE}")
        st.markdown(f"[WhatsApp Receipt](https://wa.me/918948636213?text=Unlock_My_ID_{st.session_state.u_id})")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    menu = st.radio("MAIN MENU", ["🏠 Dashboard", "🔴 Live Class", "📂 Study Material", "📝 Homework", "❓ Doubt Desk"])
    if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- 🚀 ENGINE: LIVE CLASS & ADMIN CONTROL ---
live_active = os.path.exists("live_active.txt") and open("live_active.txt").read() == "ON"

if st.session_state.role == "Admin":
    st.title("👨‍🏫 Sir's Control Console")
    a1, a2 = st.tabs(["📡 Live Control", "👥 Student Management"])
    with a1:
        if st.toggle("Start Live Stream", value=live_active):
            with open("live_active.txt", "w") as f: f.write("ON")
            webrtc_streamer(key="sir_pro", mode=WebRtcMode.SENDRECV, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else: open("live_active.txt", "w").write("OFF")
    with a2:
        m_app = st.text_input("Enter Student Mobile Number")
        if st.button("APPROVE PAID ACCESS"):
            db = load_db(); db[m_app]["paid"] = True; save_db(db); st.success(f"{m_app} is now a Premium Student!")

else: # Student Classroom logic
    if menu == "🏠 Dashboard":
        st.markdown('<div class="app-header"><h2>DASHBOARD</h2></div>', unsafe_allow_html=True)
        if live_active:
            st.markdown('<div class="feature-card"><h3><span class="live-indicator">LIVE</span> Class is Running!</h3><p>Harish Sir is teaching live now. Join quickly.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card"><h3>📅 Schedule</h3><p>Tense Part 2 - Live at 10:00 AM Tomorrow</p></div>', unsafe_allow_html=True)

    elif menu == "🔴 Live Class":
        if is_paid:
            if live_active: 
                webrtc_streamer(key="stu_pro", mode=WebRtcMode.RECVONLY, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            else: st.info("Class has not started. Please check the dashboard for schedule.")
        else: st.error("🔒 Full access required. Please pay via sidebar to join live.")