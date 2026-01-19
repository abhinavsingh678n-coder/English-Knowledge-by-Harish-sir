import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os
import json
import qrcode
from io import BytesIO

# 1. UI CONFIGURATION
st.set_page_config(page_title="Harish Sir English Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background: #F4F7FE; }
    .nav-header { background: #002E5D; color: white; padding: 25px; border-radius: 0 0 30px 30px; text-align: center; margin-bottom: 20px;}
    .batch-card { background: white; padding: 20px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; border-left: 8px solid #FFD700; }
    .live-dot { height: 12px; width: 12px; background-color: #ff0000; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# Data Persistence
USER_DB = "users_v4.json"
BATCH_DB = "batches_v4.json"
SIR_UPI = "8948636213@ybl"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f: return json.load(f)
    return {}

def save_data(file, data):
    with open(file, "w") as f: json.dump(data, f)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 🟢 AUTH & NAVIGATION (Same as before) ---
if not st.session_state.logged_in:
    st.markdown('<div class="nav-header"><h1>🎓 HARISH SIR ENGLISH PRO</h1></div>', unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["🔒 Login", "✨ Register", "👨‍🏫 Admin"])
    db = load_data(USER_DB)
    with t1:
        m = st.text_input("Mobile No.")
        p = st.text_input("Password", type="password")
        if st.button("LOGIN", use_container_width=True):
            if m in db and db[m]['password'] == p:
                st.session_state.logged_in = True; st.session_state.u_id = m; st.session_state.u_name = db[m]['name']; st.session_state.role = "Student"; st.rerun()
    with t2:
        n = st.text_input("Full Name"); rm = st.text_input("Mobile"); rp = st.text_input("Password", type="password")
        if st.button("CREATE ACCOUNT"):
            db[rm] = {"name": n, "password": rp, "purchased": []}; save_data(USER_DB, db); st.success("Account Created!")
    with t3:
        if st.text_input("Admin Key", type="password") == "harish_sir_pro":
            if st.button("SIR LOGIN"): st.session_state.logged_in = True; st.session_state.u_name = "Harish Sir"; st.session_state.role = "Admin"; st.rerun()
    st.stop()

with st.sidebar:
    st.markdown(f"### Hi, {st.session_state.u_name}")
    if st.session_state.role == "Admin":
        menu = st.radio("SIR MENU", ["Create Batch", "Approve Payments", "🔴 Go Live"])
    else:
        menu = st.radio("STUDENT MENU", ["🏠 Explore Batches", "📚 My Batches"])
    if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- 👨‍🏫 ADMIN: BATCH-WISE LIVE CONTROL ---
if st.session_state.role == "Admin":
    batches = load_data(BATCH_DB)
    
    if menu == "Create Batch":
        st.title("Create New Batch")
        bn = st.text_input("Batch Name")
        bp = st.number_input("Batch Price", min_value=0)
        bd = st.text_area("Description")
        if st.button("Launch Batch"):
            batches[bn] = {"price": bp, "desc": bd, "is_live": False}
            save_data(BATCH_DB, batches); st.success(f"Batch {bn} Live!")

    elif menu == "🔴 Go Live":
        st.title("Select Batch to Start Live Class")
        if not batches: st.warning("Pehle ek batch banaiye.")
        else:
            for b_name in batches.keys():
                st.markdown(f'<div class="batch-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([3, 1])
                with col1: st.subheader(b_name)
                with col2:
                    # Toggle switch for Live Status
                    if batches[b_name].get("is_live", False):
                        if st.button("Stop Live", key=f"stop_{b_name}"):
                            batches[b_name]["is_live"] = False
                            save_data(BATCH_DB, batches); st.rerun()
                    else:
                        if st.button("Start Live", key=f"start_{b_name}"):
                            batches[b_name]["is_live"] = True
                            save_data(BATCH_DB, batches); st.rerun()
                
                # Streaming area if Live is ON
                if batches[b_name].get("is_live", False):
                    st.error(f"🔴 Currently Live in {b_name}")
                    webrtc_streamer(key=f"sir_{b_name}", mode=WebRtcMode.SENDRECV, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
                st.markdown('</div>', unsafe_allow_html=True)

# --- 🎓 STUDENT: MY BATCHES WITH LIVE INDICATOR ---
else:
    batches = load_data(BATCH_DB)
    users = load_data(USER_DB)
    my_p = users.get(st.session_state.u_id, {}).get("purchased", [])

    if menu == "🏠 Explore Batches":
        st.title("New Batches for You")
        for name, info in batches.items():
            if name not in my_p:
                st.markdown(f'<div class="batch-card">', unsafe_allow_html=True)
                st.subheader(name)
                st.write(f"Price: ₹{info['price']}")
                if st.button("Check Details", key=name):
                    upi_url = f"upi://pay?pa={SIR_UPI}&pn=Harish_Sir&am={info['price']}&cu=INR&tn=Batch_{name}_ID_{st.session_state.u_id}"
                    qr = qrcode.make(upi_url); buf = BytesIO(); qr.save(buf, format="PNG")
                    st.image(buf.getvalue(), caption="Scan to Pay")
                st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "📚 My Batches":
        st.title("Your Classroom")
        if not my_p: st.info("Koi batch nahi mila.")
        else:
            for b_name in my_p:
                st.markdown(f'<div class="batch-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([3, 1])
                with col1:
                    is_live = batches.get(b_name, {}).get("is_live", False)
                    if is_live: st.markdown('<h3><span class="live-dot"></span>' + b_name + ' (LIVE NOW)</h3>', unsafe_allow_html=True)
                    else: st.subheader(b_name)
                with col2:
                    if st.button("Enter Class", key=f"go_{b_name}"):
                        st.session_state.watching = b_name
                
                if st.session_state.get("watching") == b_name:
                    if is_live:
                        webrtc_streamer(key=f"stu_{b_name}", mode=WebRtcMode.RECVONLY, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
                    else: st.warning("Abhi Sir live nahi hain. Purani recording check karein.")
                st.markdown('</div>', unsafe_allow_html=True)