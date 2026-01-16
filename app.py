import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import time

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage Initialization
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'active_poll' not in st.session_state: st.session_state.active_poll = None
if 'poll_results' not in st.session_state: st.session_state.poll_results = {}
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- LOGIN SYSTEM (10-Digit Check) ---
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    with st.expander("👨‍🏫 Harish Sir Login"):
        admin_pwd = st.text_input("Security Key", type="password")
        if st.button("Admin Login"):
            if admin_pwd == "harish_sir_pro":
                st.session_state.role = "Admin"
                st.rerun()

    st.subheader("Student Login")
    u_name = st.text_input("Apna Naam")
    u_mobile = st.text_input("Mobile Number (10 Digits)")
    if st.button("Enter Classroom"):
        clean_num = u_mobile.strip()
        if u_name and clean_num.isdigit() and len(clean_num) == 10:
            st.session_state.logged_in = True
            st.session_state.user_name = u_name
            st.session_state.user_id = clean_num
            st.rerun()
        else:
            st.error("❌ Galat Entry! 10-digit number aur naam zaruri hai.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 📖 English Knowledge")
    st.caption("By Harish Sir")
    st.divider()
    menu = st.radio("Menu", ["🏠 Dashboard", "🔴 Live Class", "🎥 Recorded Classes", "📂 My Notes", "❓ Ask Doubt"])
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = "Student"
        st.rerun()

# --- ADMIN PANEL (Harish Sir) ---
if st.session_state.role == "Admin":
    st.title("👨‍🏫 Harish Sir's Control Panel")
    t1, t2, t3, t4 = st.tabs(["🚀 Live Class", "📊 Poll System", "📤 Homework", "💬 Doubts"])
    
    with t1:
        st.subheader("Start Live Class")
        topic = st.text_input("Class Topic Name")
        # TEACHER: Mode is SENDRECV so he can see student if student joins call
        webrtc_streamer(key="sir-stream", mode=WebRtcMode.SENDRECV, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        
        st.divider()
        link = st.text_input("YouTube/Drive Link to Save Permanently")
        if st.button("Save to Recorded Library"):
            if topic and link:
                st.session_state.recorded_classes.insert(0, {"title": topic, "link": link})
                st.success("Library updated!")

    with t2:
        st.subheader("Create a New Poll")
        with st.form("p_form"):
            pq = st.text_input("Question")
            pa = st.text_input("Option A")
            pb = st.text_input("Option B")
            if st.form_submit_button("Launch Poll"):
                st.session_state.active_poll = {"q": pq, "a": pa, "b": pb}
                st.session_state.poll_results = {pa: 0, pb: 0}
                st.success("Poll Live!")

    # ... (Homework and Doubts sections remain same)

# --- STUDENT PANEL ---
else:
    if menu == "🏠 Dashboard":
        st.title(f"Welcome, {st.session_state.user_name}!")
        if st.session_state.active_poll:
            st.markdown("### 📊 Live Poll from Sir")
            st.write(f"**Q: {st.session_state.active_poll['q']}**")
            vote = st.radio("Choose One", [st.session_state.active_poll['a'], st.session_state.active_poll['b']])
            if st.button("Submit Vote"):
                st.session_state.poll_results[vote] += 1
                st.success("Voted!")
        else:
            st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)

    elif menu == "🔴 Live Class":
        st.subheader("🔴 English Live Classroom")
        
        # FEATURE: Student can ONLY view by default. No camera access unless they check the box.
        st.write("Sir ki class niche dikhegi:")
        
        interact_call = st.checkbox("Ask a question on Video Call (Sir ke kehne par on karein)")
        
        if interact_call:
            # Mode SENDRECV opens student's camera for interaction
            webrtc_streamer(key="stu-interaction", mode=WebRtcMode.SENDRECV, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else:
            # Mode RECVONLY ONLY shows teacher's stream. Student's camera is NOT accessed.
            webrtc_streamer(key="stu-view-only", mode=WebRtcMode.RECVONLY, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    elif menu == "🎥 Recorded Classes":
        for vid in st.session_state.recorded_classes:
            with st.expander(f"▶️ {vid['title']}"):
                st.video(vid['link'])

    elif menu == "📂 My Notes":
        for item in st.session_state.homework_list:
            st.download_button(f"Download {item['title']}", data=item['file'])

    elif menu == "❓ Ask Doubt":
        with st.form("d_form"):
            q = st.text_area("Sawal Likhein")
            if st.form_submit_button("Bhejein"):
                if q:
                    st.session_state.doubts.append({"user": st.session_state.user_name, "id": st.session_state.user_id, "question": q, "answer": None})
                    st.success("Sent!")
        for d in reversed(st.session_state.doubts):
            if d['id'] == st.session_state.user_id:
                st.write(f"❓ {d['question']}")
                if d['answer']: st.info(f"✅ {d['answer']}")
                st.divider()