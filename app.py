import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import time

# 1. PAGE SETTINGS
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage Initialization
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'call_active' not in st.session_state: st.session_state.call_active = False # Sir's Video Call Toggle
if 'active_poll' not in st.session_state: st.session_state.active_poll = None
if 'poll_results' not in st.session_state: st.session_state.poll_results = {}
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- LOGIN SYSTEM (Strict 10-Digit Mobile Check) ---
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    with st.expander("👨‍🏫 Staff Access (Harish Sir)"):
        admin_key = st.text_input("Security Key", type="password")
        if st.button("Admin Login"):
            if admin_key == "harish_sir_pro":
                st.session_state.role = "Admin"
                st.rerun()

    st.subheader("Student Entry")
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
            st.error("❌ Galat Detail! 10-digit number dalein.")
    st.stop()

# --- SIDEBAR BRANDING ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📖 English Knowledge</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>By Harish Sir</p>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("Menu", ["🏠 Dashboard", "🔴 Live Class", "🎥 Recorded Classes", "📂 My Notes", "❓ Ask Doubt"])
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = "Student"
        st.rerun()

# --- ADMIN PANEL (Harish Sir's View) ---
if st.session_state.role == "Admin":
    st.title("👨‍🏫 Harish Sir's Control Center")
    t1, t2, t3, t4 = st.tabs(["🚀 Live Control", "📊 Poll", "📤 Homework", "💬 Doubts"])
    
    with t1:
        st.subheader("1. Live Lecture Control")
        topic = st.text_input("Today's Topic Name")
        # TEACHER STREAM
        webrtc_streamer(key="sir-live", mode=WebRtcMode.SENDRECV, 
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        
        st.divider()
        st.subheader("2. Student Video Call Control")
        if not st.session_state.call_active:
            if st.button("📞 Start Video Call with Students"):
                st.session_state.call_active = True
                st.rerun()
        else:
            if st.button("🛑 End Video Call (Resume Lecture)"):
                st.session_state.call_active = False
                st.rerun()
        
        st.divider()
        if st.button("🎬 End Full Class & Save"):
            if topic:
                st.session_state.recorded_classes.insert(0, {"title": topic, "link": "Class Ended Successfully"})
                st.success("Class Record ho gayi!")

    with t2:
        st.subheader("Create Poll")
        with st.form("p_form"):
            pq = st.text_input("Question")
            pa = st.text_input("Option A"); pb = st.text_input("Option B")
            if st.form_submit_button("Launch Poll"):
                st.session_state.active_poll = {"q": pq, "a": pa, "b": pb}
                st.session_state.poll_results = {pa: 0, pb: 0}
                st.success("Poll Live!")
        if st.session_state.active_poll:
            st.bar_chart(st.session_state.poll_results)
            if st.button("Clear Poll"): st.session_state.active_poll = None; st.rerun()

    with t3:
        h_t = st.text_input("Notes Title"); h_f = st.file_uploader("Upload")
        if st.button("Send Notes"):
            if h_t and h_f: st.session_state.homework_list.insert(0, {"title": h_t, "file": h_f}); st.success("Uploaded!")

    with t4:
        for i, d in enumerate(st.session_state.doubts):
            with st.expander(f"From {d['user']} (ID: {d['id']})"):
                st.write(f"Q: {d['question']}")
                if d['answer']: st.info(f"Ans: {d['answer']}")
                else:
                    ans = st.text_area("Reply", key=f"ans_{i}")
                    if st.button("Send", key=f"btn_{i}"):
                        st.session_state.doubts[i]['answer'] = ans; st.rerun()

# --- STUDENT PANEL (Bachon ka View) ---
else:
    if menu == "🏠 Dashboard":
        st.title(f"Welcome, {st.session_state.user_name}!")
        if st.session_state.active_poll:
            st.markdown("### 📊 Live Poll from Sir")
            st.write(f"**Q: {st.session_state.active_poll['q']}**")
            vote = st.radio("Choose One", [st.session_state.active_poll['a'], st.session_state.active_poll['b']])
            if st.button("Submit Vote"):
                st.session_state.poll_results[vote] += 1; st.success("Voted!")
        else:
            st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)

    elif menu == "🔴 Live Class":
        st.subheader("🔴 English Live Classroom")
        # LOGIC: Sir's Call Active? Then Student Cam Opens, else View Only
        if st.session_state.call_active:
            st.warning("⚠️ Sir is calling you! Camera/Mic is now ON.")
            webrtc_streamer(key="stu-call", mode=WebRtcMode.SENDRECV,
                            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else:
            st.info("📺 Sir is teaching. (Your Cam/Mic is OFF)")
            webrtc_streamer(key="stu-view", mode=WebRtcMode.RECVONLY,
                            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    elif menu == "🎥 Recorded Classes":
        for vid in st.session_state.recorded_classes:
            st.warning(f"📺 {vid['title']} - Class Finished")

    elif menu == "📂 My Notes":
        for item in st.session_state.homework_list:
            st.download_button(f"Download {item['title']}", data=item['file'])

    elif menu == "❓ Ask Doubt":
        with st.form("d_form"):
            q = st.text_area("Sawal Likhein")
            if st.form_submit_button("Bhejein"):
                if q: st.session_state.doubts.append({"user": st.session_state.user_name, "id": st.session_state.user_id, "question": q, "answer": None}); st.success("Sent!")
        for d in reversed(st.session_state.doubts):
            if d['id'] == st.session_state.user_id:
                st.write(f"❓ {d['question']}")
                if d['answer']: st.info(f"✅ {d['answer']}")
                st.divider()