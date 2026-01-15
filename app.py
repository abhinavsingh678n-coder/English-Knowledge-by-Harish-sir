import streamlit as st
from streamlit_webrtc import webrtc_streamer
import time

# 1. Page Config
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- LOGIN SYSTEM ---
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    
    # Staff/Teacher Entry
    with st.expander("👨‍🏫 Harish Sir Login"):
        admin_key = st.text_input("Admin Password", type="password")
        if st.button("Login as Sir"):
            if admin_key == "harish_sir_pro":
                st.session_state.role = "Admin"
                st.rerun()

    st.write("---")
    # Student Entry
    st.subheader("Student Login")
    u_name = st.text_input("Apna Naam Dalein")
    u_mobile = st.text_input("10-digit Mobile Number Dalein")
    
    if st.button("Enter Classroom"):
        # Validation Logic: Space hatao aur length check karo
        clean_mobile = u_mobile.strip()
        if u_name and clean_mobile.isdigit() and len(clean_mobile) == 10:
            st.session_state.logged_in = True
            st.session_state.user_name = u_name
            st.session_state.user_id = clean_mobile
            st.rerun()
        else:
            st.error("❌ Galat Detail! Naam bharein aur Mobile Number sahi 10 digits ka hona chahiye.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("📖 English Knowledge")
    st.caption("By Harish Sir")
    st.divider()
    menu = st.radio("Menu", ["🏠 Dashboard", "🔴 Live Class", "🎥 Recorded Classes", "📂 My Notes", "❓ Ask Doubt"])
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = "Student"
        st.rerun()

# --- ADMIN PANEL ---
if st.session_state.role == "Admin":
    st.title("👨‍🏫 Harish Sir's Panel")
    t1, t2, t3 = st.tabs(["🚀 Live", "📤 Homework", "💬 Doubts"])
    
    with t1:
        topic = st.text_input("Class Topic")
        webrtc_streamer(key="sir-live", rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        if st.button("End & Save"):
            st.session_state.recorded_classes.insert(0, {"title": f"{topic} ({time.strftime('%d-%m %H:%M')})"})
            st.success("Saved!")

    with t2:
        h_t = st.text_input("Title")
        h_f = st.file_uploader("Upload")
        if st.button("Upload Now"):
            if h_t and h_f:
                st.session_state.homework_list.insert(0, {"title": h_t, "file": h_f})
                st.success("Uploaded!")

    with t3:
        for i, d in enumerate(st.session_state.doubts):
            with st.expander(f"From: {d['user']} (ID: {d['id']})"):
                st.write(f"Q: {d['question']}")
                if d['answer']: st.info(f"Ans: {d['answer']}")
                else:
                    ans = st.text_area("Reply", key=f"ans_{i}")
                    if st.button("Send", key=f"btn_{i}"):
                        st.session_state.doubts[i]['answer'] = ans
                        st.rerun()

# --- STUDENT PANEL ---
else:
    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.user_name}!")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)
    
    elif menu == "🔴 Live Class":
        webrtc_streamer(key="stu-live", rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        
    elif menu == "🎥 Recorded Classes":
        for vid in st.session_state.recorded_classes:
            st.warning(f"📺 {vid['title']} (Processing for Playback)")

    elif menu == "📂 My Notes":
        for item in st.session_state.homework_list:
            st.download_button(f"Download {item['title']}", data=item['file'])

    elif menu == "❓ Ask Doubt":
        with st.form("doubt_form"):
            q = st.text_area("Apna Sawal")
            if st.form_submit_button("Bhejein"):
                if q:
                    st.session_state.doubts.append({"user": st.session_state.user_name, "id": st.session_state.user_id, "question": q, "answer": None})
                    st.success("Bhej diya gaya!")
        for d in reversed(st.session_state.doubts):
            if d['id'] == st.session_state.user_id:
                st.write(f"❓ {d['question']}")
                if d['answer']: st.info(f"✅ {d['answer']}")
                st.divider()