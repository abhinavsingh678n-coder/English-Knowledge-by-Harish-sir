import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os
import json
import qrcode
from io import BytesIO

# UI CONFIG
st.set_page_config(page_title="Harish Sir Pro", layout="wide", initial_sidebar_state="collapsed")

# CSS for Professional Look
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background: #F4F7FE; }
    .nav-header { background: #002E5D; color: white; padding: 20px; border-radius: 0 0 25px 25px; text-align: center; }
    .batch-card { background: white; padding: 20px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; border-left: 8px solid #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# Data Store & UPI
USER_DB = "users_v5.json"
BATCH_DB = "batches_v5.json"
SIR_UPI = "8948636213@ybl"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f: return json.load(f)
    return {}

def save_data(file, data):
    with open(file, "w") as f: json.dump(data, f)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- AUTH SYSTEM (FIXED DUPLICATE IDs) ---
if not st.session_state.logged_in:
    st.markdown('<div class="nav-header"><h1>🎓 HARISH SIR ENGLISH PRO</h1></div>', unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["🔒 Login", "✨ Register", "👨‍🏫 Admin"])
    db = load_data(USER_DB)
    
    with t1:
        m_log = st.text_input("Mobile No.", key="login_mob")
        p_log = st.text_input("Password", type="password", key="login_pass")
        if st.button("LOGIN", use_container_width=True):
            if m_log in db and db[m_log]['password'] == p_log:
                st.session_state.logged_in = True; st.session_state.u_id = m_log; st.session_state.u_name = db[m_log]['name']; st.session_state.role = "Student"; st.rerun()
    
    with t2:
        # FIXED: Added unique 'key' to avoid DuplicateElementId error
        n_reg = st.text_input("Full Name", key="reg_name")
        rm_reg = st.text_input("10 Digit Mobile", key="reg_mob")
        rp_reg = st.text_input("Password", type="password", key="reg_pass")
        if st.button("CREATE ACCOUNT", use_container_width=True):
            if len(rm_reg) == 10:
                db[rm_reg] = {"name": n_reg, "password": rp_reg, "purchased": []}; save_data(USER_DB, db); st.success("Account Created!")
    
    with t3:
        # FIXED: Added unique 'key' for Admin
        if st.text_input("Admin Key", type="password", key="admin_pass_key") == "harish_sir_pro":
            if st.button("SIR LOGIN"): st.session_state.logged_in = True; st.session_state.u_name = "Harish Sir"; st.session_state.role = "Admin"; st.rerun()
    st.stop()

# --- MAIN APP LOGIC ---
with st.sidebar:
    st.markdown(f"### Hi, {st.session_state.u_name}")
    if st.session_state.role == "Admin":
        menu = st.radio("SIR MENU", ["Create Batch", "Approve Payments", "🔴 Go Live"])
    else:
        menu = st.radio("STUDENT MENU", ["🏠 Explore Batches", "📚 My Batches"])
    if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- ADMIN: BATCH CONTROL ---
if st.session_state.role == "Admin":
    batches = load_data(BATCH_DB)
    if menu == "Create Batch":
        st.title("Add New Batch")
        bn = st.text_input("Batch Name", key="new_batch_name")
        bp = st.number_input("Batch Price (₹)", min_value=0, key="new_batch_price")
        if st.button("Launch"):
            batches[bn] = {"price": bp, "is_live": False}
            save_data(BATCH_DB, batches); st.success(f"Batch {bn} Live!")
    
    elif menu == "🔴 Go Live":
        st.title("Live Control Center")
        for b_name in batches.keys():
            st.markdown(f'<div class="batch-card"><h3>{b_name}</h3></div>', unsafe_allow_html=True)
            if st.toggle(f"Go Live in {b_name}", key=f"live_{b_name}"):
                batches[b_name]["is_live"] = True; save_data(BATCH_DB, batches)
                webrtc_streamer(key=f"sir_stream_{b_name}", mode=WebRtcMode.SENDRECV)
            else:
                batches[b_name]["is_live"] = False; save_data(BATCH_DB, batches)

# --- STUDENT: BATCHES ---
else:
    batches = load_data(BATCH_DB)
    users = load_data(USER_DB)
    my_p = users.get(st.session_state.u_id, {}).get("purchased", [])

    if menu == "🏠 Explore Batches":
        st.title("Available Batches")
        for name, info in batches.items():
            if name not in my_p:
                st.markdown(f'<div class="batch-card"><h4>{name}</h4><p>Price: ₹{info["price"]}</p></div>', unsafe_allow_html=True)
                if st.button(f"Buy {name}", key=f"buy_{name}"):
                    upi_url = f"upi://pay?pa={SIR_UPI}&pn=Harish_Sir&am={info['price']}&cu=INR&tn=Batch_{name}_ID_{st.session_state.u_id}"
                    qr = qrcode.make(upi_url); buf = BytesIO(); qr.save(buf, format="PNG")
                    st.image(buf.getvalue(), caption="Scan to Unlock")
    
    elif menu == "📚 My Batches":
        st.title("My Classroom")
        for b_name in my_p:
            is_live = batches.get(b_name, {}).get("is_live", False)
            st.markdown(f'<div class="batch-card"><h4>{"🔴" if is_live else "📖"} {b_name}</h4></div>', unsafe_allow_html=True)
            if st.button(f"Enter {b_name}", key=f"enter_{b_name}"):
                if is_live: webrtc_streamer(key=f"stu_stream_{b_name}", mode=WebRtcMode.RECVONLY)
                else: st.warning("Sir is currently offline.")