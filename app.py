import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os
import json
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide")

# CSS for Photo-like Cards
st.markdown("""
    <style>
    .card { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 10px solid #ff4b4b; margin-bottom: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# Files
USER_DB = "users_data.json"
QR_IMAGE_PATH = "harish_qr.png"
DOUBT_FILE = "doubts.csv"

def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f: return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB, "w") as f: json.dump(users, f)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'u_name' not in st.session_state: st.session_state.u_name = ""

# --- LOGIN & REGISTER ---
if not st.session_state.logged_in:
    st.title("📖 English Knowledge - Harish Sir")
    t1, t2, t3 = st.tabs(["Student Login", "Register", "Admin Login"])
    users = load_users()
    with t1:
        l_mob = st.text_input("Mobile No.")
        l_pass = st.text_input("Password", type="password")
        if st.button("Login"):
            if l_mob in users and users[l_mob]['password'] == l_pass:
                st.session_state.logged_in = True; st.session_state.u_id = l_mob; st.session_state.u_name = users[l_mob]['name']; st.session_state.role = "Student"; st.rerun()
            else: st.error("Galat Details!")
    with t2:
        r_name = st.text_input("Naam"); r_mob = st.text_input("Mobile (10 Digits)"); r_pass = st.text_input("Set Password", type="password")
        if st.button("Create Account"):
            if len(r_mob) == 10:
                users[r_mob] = {"name": r_name, "password": r_pass, "paid": False}; save_users(users); st.success("Ready! Login karein.")
    with t3:
        if st.text_input("Sir Key", type="password") == "harish_sir_pro":
            if st.button("Admin Login"): st.session_state.logged_in = True; st.session_state.u_name = "Harish Sir"; st.session_state.role = "Admin"; st.rerun()
    st.stop()

# --- SIDEBAR (Updated Screenshot Menu) ---
with st.sidebar:
    st.header(f"👤 {st.session_state.u_name}")
    st.caption("Organization Code YICKLF")
    
    if st.session_state.role == "Student":
        users = load_users()
        is_paid = users[st.session_state.u_id].get("paid", False)
        if not is_paid:
            st.error("❌ ACCESS LOCKED")
            if os.path.exists(QR_IMAGE_PATH): st.image(QR_IMAGE_PATH, caption="Scan to Pay")
            st.markdown(f"[Send Screenshot to Sir](https://wa.me/919999999999)")
    
    menu = st.radio("Menu", ["🏠 Dashboard", "🔴 Live Class", "❓ Doubt Panel", "📝 Homework", "📂 Free Material"])
    if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- MAIN DASHBOARD ---
live_state = "ON" if os.path.exists("live.txt") and open("live.txt").read() == "ON" else "OFF"

if st.session_state.role == "Admin":
    st.title("👨‍🏫 Sir Control Panel")
    t_live, t_pay, t_doubts = st.tabs(["Live & QR", "Approvals", "Student Doubts"])
    
    with t_live:
        qr_up = st.file_uploader("Upload Bar Code", type=['png','jpg'])
        if qr_up:
            with open(QR_IMAGE_PATH, "wb") as f: f.write(qr_up.getbuffer())
            st.success("QR Updated!")
        if st.toggle("Go Live", value=(live_state == "ON")):
            with open("live.txt", "w") as f: f.write("ON")
            webrtc_streamer(key="sir", mode=WebRtcMode.SENDRECV, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else:
            with open("live.txt", "w") as f: f.write("OFF")

    with t_pay:
        m_app = st.text_input("Approve Mobile No.")
        if st.button("Grant Access"):
            users = load_users(); users[m_app]["paid"] = True; save_users(users); st.success("Approved!")

    with t_doubts:
        if os.path.exists(DOUBT_FILE): st.dataframe(pd.read_csv(DOUBT_FILE))

else:
    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.u_name}")
        if live_state == "ON": st.error("🔴 SIR IS LIVE NOW!")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg")

    elif menu == "❓ Doubt Panel":
        st.subheader("Ask Sir a Question")
        msg = st.text_area("Apna doubt yahan likhein...")
        if st.button("Submit Doubt"):
            d_data = pd.DataFrame([[st.session_state.u_name, msg]], columns=["Student", "Doubt"])
            if os.path.exists(DOUBT_FILE): d_data.to_csv(DOUBT_FILE, mode='a', header=False, index=False)
            else: d_data.to_csv(DOUBT_FILE, index=False)
            st.success("Doubt Sir ko bhej diya gaya hai!")

    elif menu == "📝 Homework":
        st.subheader("Homework Upload")
        hw_file = st.file_uploader("Upload Homework (PDF/Image)")
        if hw_file: st.success("Homework Uploaded Successfully!")

    elif menu == "🔴 Live Class":
        users = load_users()
        if users[st.session_state.u_id].get("paid"):
            if live_state == "ON": webrtc_streamer(key="stu", mode=WebRtcMode.RECVONLY, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            else: st.info("Sir is not live.")
        else: st.error("🔒 Please pay to watch live.")