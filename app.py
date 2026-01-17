import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os
import pandas as pd
import json

# 1. PAGE SETUP
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide")

# Data Storage Files
USER_DB = "user_database.json"
QR_IMAGE_PATH = "harish_sir_qr.png"

# Helper Functions
def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f: return json.load(f)
    return {}

def save_user(mobile, password, name):
    users = load_users()
    users[mobile] = {"password": password, "name": name, "paid": False}
    with open(USER_DB, "w") as f: json.dump(users, f)

def update_db(key, val):
    with open(f"{key}.txt", "w") as f: f.write(val)

def read_db(key):
    if not os.path.exists(f"{key}.txt"): return "OFF"
    with open(f"{key}.txt", "r") as f: return f.read().strip()

# --- LOGIN & REGISTRATION LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🎓 English Knowledge - Harish Sir")
    
    choice = st.radio("Select Option", ["Login", "Register (Naye bacho ke liye)"])
    users = load_users()

    if choice == "Register (Naye bacho ke liye)":
        name = st.text_input("Apna Naam")
        reg_mobile = st.text_input("Mobile Number (10 Digits)")
        reg_pass = st.text_input("Naya Password Set Karein", type="password")
        
        if st.button("Create Account"):
            if len(reg_mobile) == 10 and reg_mobile.isdigit():
                if reg_mobile in users:
                    st.error("Ye number pehle se register hai. Login karein.")
                elif len(reg_pass) < 4:
                    st.error("Password kam se kam 4 aksharo ka rakhein.")
                else:
                    save_user(reg_mobile, reg_pass, name)
                    st.success("Registration Successful! Ab Login tab par jayein.")
            else:
                st.error("Keval 10-digit ka Indian Mobile number dalein.")

    else:
        log_mobile = st.text_input("Mobile Number")
        log_pass = st.text_input("Password", type="password")
        
        if st.button("Login Now"):
            if log_mobile == "9999999999" and log_pass == "harish_sir_pro": # Master Admin Login
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.session_state.u_name = "Harish Sir"
                st.rerun()
            elif log_mobile in users and users[log_mobile]["password"] == log_pass:
                st.session_state.logged_in = True
                st.session_state.u_id = log_mobile
                st.session_state.u_name = users[log_mobile]["name"]
                st.session_state.role = "Student"
                st.rerun()
            else:
                st.error("Mobile Number ya Password galat hai.")
    st.stop()

# --- APP INTERFACE ---
with st.sidebar:
    st.header(f"👤 {st.session_state.u_name}")
    
    if st.session_state.role == "Student":
        users = load_users()
        is_paid = users[st.session_state.u_id].get("paid", False)
        
        if is_paid:
            st.success("✅ PAID STUDENT")
        else:
            st.error("❌ ACCESS LOCKED")
            st.subheader("💳 Unlock Full Course")
            if os.path.exists(QR_IMAGE_PATH):
                st.image(QR_IMAGE_PATH, caption="Scan & Pay ₹499")
            st.markdown(f"[Send Screenshot to Sir](https://wa.me/919999999999?text=Mera%20Number%20{st.session_state.u_id}%20hai)")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- DASHBOARD ---
live_state = read_db("live")

if st.session_state.role == "Admin":
    st.title("👨‍🏫 Harish Sir Control Panel")
    tab1, tab2 = st.columns(2)
    
    with tab1:
        st.subheader("🔴 Live Control")
        if st.toggle("Start Class", value=(live_state == "ON")):
            update_db("live", "ON")
            webrtc_streamer(key="sir", mode=WebRtcMode.SENDRECV, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else: update_db("live", "OFF")
        
        st.subheader("📤 Upload QR Scanner")
        qr_file = st.file_uploader("Upload Image", type=['png','jpg'])
        if qr_file:
            with open(QR_IMAGE_PATH, "wb") as f: f.write(qr_file.getbuffer())
            st.success("QR Code Updated!")

    with tab2:
        st.subheader("✅ Approve Students")
        users = load_users()
        m_to_pay = st.text_input("Enter Student Mobile")
        if st.button("Activate Account"):
            if m_to_pay in users:
                users[m_to_pay]["paid"] = True
                with open(USER_DB, "w") as f: json.dump(users, f)
                st.success(f"{users[m_to_pay]['name']} is now Paid!")
            else: st.error("User not found.")

else:
    st.title("Student Dashboard")
    users = load_users()
    is_paid = users[st.session_state.u_id].get("paid", False)
    
    if live_state == "ON":
        if is_paid:
            st.success("Sir is Live! Watch Below.")
            webrtc_streamer(key="stu", mode=WebRtcMode.RECVONLY, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else: st.error("🔒 Locked: Pehle pay karein aur Sir se permission lein.")
    else: st.info("Class abhi band hai.")