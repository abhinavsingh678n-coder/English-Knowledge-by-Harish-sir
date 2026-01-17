import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os
import json

# 1. PAGE SETUP
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide")

# Data Storage
USER_DB = "users_data.json"
QR_IMAGE_PATH = "harish_qr.png"

def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f: return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB, "w") as f: json.dump(users, f)

# Initializing Session States to prevent Errors
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'u_name' not in st.session_state: st.session_state.u_name = ""
if 'role' not in st.session_state: st.session_state.role = "Student"

# --- LOGIN & REGISTER SYSTEM ---
if not st.session_state.logged_in:
    st.title("🎓 Harish Sir - Classroom Login")
    tab1, tab2, tab3 = st.tabs(["Student Login", "Register (New Student)", "Admin Access"])
    
    users = load_users()

    with tab1: # Login
        log_mob = st.text_input("Mobile Number", key="l_mob")
        log_pass = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login Now"):
            if log_mob in users and users[log_mob]['password'] == log_pass:
                st.session_state.logged_in = True
                st.session_state.u_id = log_mob
                st.session_state.u_name = users[log_mob]['name']
                st.session_state.role = "Student"
                st.rerun()
            else: st.error("Galat Number ya Password!")

    with tab2: # Register
        reg_name = st.text_input("Apna Naam")
        reg_mob = st.text_input("Mobile Number (10 Digits)")
        reg_pass = st.text_input("Password Set Karein", type="password")
        if st.button("Create Account"):
            if len(reg_mob) == 10 and reg_mob.isdigit():
                users[reg_mob] = {"name": reg_name, "password": reg_pass, "paid": False}
                save_users(users)
                st.success("Account ban gaya! Ab Login tab par jayein.")
            else: st.error("Sahi 10-digit number dalein.")

    with tab3: # Admin Login (Harish Sir)
        sir_pass = st.text_input("Sir Security Key", type="password")
        if st.button("Sir Login"):
            if sir_pass == "harish_sir_pro":
                st.session_state.logged_in = True
                st.session_state.u_name = "Harish Sir"
                st.session_state.role = "Admin"
                st.rerun()
            else: st.error("Galat Key!")
    st.stop()

# --- SIDEBAR (Updated with Screenshot features) ---
with st.sidebar:
    st.header(f"👤 {st.session_state.u_name}")
    st.caption("Organization Code YICKLF")
    
    if st.session_state.role == "Student":
        users = load_users()
        is_paid = users[st.session_state.u_id].get("paid", False)
        if is_paid: st.success("✅ PAID USER")
        else:
            st.error("❌ FREE USER")
            st.subheader("Buy Full Course (₹499)")
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=harishsir@upi&pn=HarishSir&am=499")
            st.caption("Scan and pay ₹499")
    
    st.divider()
    # New options as per your screenshot
    st.write("📂 Free Material")
    st.write("💬 Students Testimonial")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- DASHBOARD ---
if st.session_state.role == "Admin":
    st.title("👨‍🏫 Harish Sir Management")
    users = load_users()
    m_approve = st.text_input("Approve Student (Mobile Number)")
    if st.button("Grant Access"):
        if m_approve in users:
            users[m_approve]["paid"] = True
            save_users(users)
            st.success(f"Mobile {m_approve} Approved!")
        else: st.error("Number nahi mila.")
else:
    st.title(f"Namaste, {st.session_state.u_name}")
    st.info("Class ke liye sidebar se 'Live' check karein.")