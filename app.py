import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide")

# CSS for Photo-like Cards (As per your design)
st.markdown("""
    <style>
    .card { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 10px solid #ff4b4b; margin-bottom: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .sidebar-pay { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #ddd; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Data Files
PAYMENT_FILE = "payments_list.csv"
QR_IMAGE_PATH = "harish_sir_qr.png"

def update_db(key, val):
    with open(f"{key}.txt", "w") as f: f.write(val)
def read_db(key):
    if not os.path.exists(f"{key}.txt"): return "OFF"
    with open(f"{key}.txt", "r") as f: return f.read().strip()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- LOGIN ---
if not st.session_state.logged_in:
    st.sidebar.title("Streemanit Login")
    u_n = st.sidebar.text_input("Naam:")
    u_m = st.sidebar.text_input("Mobile (10 Digits):")
    if st.sidebar.button("Login"):
        if u_n and len(u_m) == 10:
            st.session_state.logged_in = True; st.session_state.u_name = u_n; st.session_state.u_id = u_m; st.rerun()
    with st.sidebar.expander("Admin Access"):
        key = st.text_input("Security Key", type="password")
        if st.button("Sir Login"):
            if key == "harish_sir_pro":
                st.session_state.role = "Admin"; st.session_state.logged_in = True; st.rerun()
    st.stop()

# --- SIDEBAR (Student View: QR & Payment) ---
with st.sidebar:
    st.header(f"👤 {st.session_state.u_name if st.session_state.get('role') != 'Admin' else 'Harish Sir'}")
    
    if st.session_state.get('role') != "Admin":
        st.markdown('<div class="sidebar-pay">', unsafe_allow_html=True)
        st.subheader("💳 Buy Course (₹499)")
        
        # Display Sir's Uploaded QR
        if os.path.exists(QR_IMAGE_PATH):
            st.image(QR_IMAGE_PATH, caption="Scan this to pay Harish Sir")
        else:
            st.warning("QR Code not uploaded by Sir yet.")
        
        is_paid = os.path.exists(f"pay_{st.session_state.u_id}.txt")
        if is_paid:
            st.success("✅ Access Approved!")
        else:
            st.error("❌ Access Locked")
            if st.button("I have Paid (Notify Sir)"):
                new_data = pd.DataFrame([[st.session_state.u_name, st.session_state.u_id, datetime.now().strftime("%Y-%m-%d %H:%M")]], columns=["Name", "Mobile", "Time"])
                if os.path.exists(PAYMENT_FILE): new_data.to_csv(PAYMENT_FILE, mode='a', header=False, index=False)
                else: new_data.to_csv(PAYMENT_FILE, index=False)
                st.info("Sir notified! Please wait for approval.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- MAIN INTERFACE ---
live_state = read_db("live")

if st.session_state.get('role') == "Admin":
    st.title("👨‍🏫 Harish Sir's Management Panel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📤 Upload Your Bar Code")
        qr_file = st.file_uploader("Choose QR Code Image", type=['png', 'jpg', 'jpeg'])
        if qr_file:
            with open(QR_IMAGE_PATH, "wb") as f: f.write(qr_file.getbuffer())
            st.success("QR Code updated for all students!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔴 Class Control")
        if st.toggle("Go Live", value=(live_state == "ON")):
            update_db("live", "ON")
            webrtc_streamer(key="admin", mode=WebRtcMode.SENDRECV, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else: update_db("live", "OFF")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("👥 Payment Approval List")
        if os.path.exists(PAYMENT_FILE):
            df = pd.read_csv(PAYMENT_FILE)
            st.dataframe(df)
            stu_to_approve = st.text_input("Enter Mobile Number to Approve")
            if st.button("Grant Full Access"):
                with open(f"pay_{stu_to_approve}.txt", "w") as f: f.write("PAID")
                st.success(f"Access granted to {stu_id}")
        else: st.info("No payment requests yet.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.title("English Knowledge Dashboard")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📺 Live Class Status")
    if live_state == "ON":
        if os.path.exists(f"pay_{st.session_state.u_id}.txt"):
            st.success("Sir is Live! Click below to join.")
            webrtc_streamer(key="student", mode=WebRtcMode.RECVONLY, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else:
            st.error("🔒 Locked: Please pay ₹499 and get Sir's approval to watch live.")
    else: st.info("Sir is not live right now.")
    st.markdown('</div>', unsafe_allow_html=True)