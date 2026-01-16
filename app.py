import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import time

# 1. PAGE SETTINGS
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'call_active' not in st.session_state: st.session_state.call_active = False 
if 'active_poll' not in st.session_state: st.session_state.active_poll = None
if 'poll_results' not in st.session_state: st.session_state.poll_results = {}
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- LOGIN (10 Digit Check) ---
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    with st.expander("👨‍🏫 Harish Sir Login"):
        if st.text_input("Security Key", type="password") == "harish_sir_pro":
            if st.button("Admin Login"):
                st.session_state.role = "Admin"
                st.rerun()

    st.subheader("Student Login")
    u_name = st.text_input("Full Name")
    u_mobile = st.text_input("Mobile Number")
    if st.button("Login"):
        if u_name and len(u_mobile.strip()) == 10: # Strict 10-digit rule
            st.session_state.logged_in = True
            st.session_state.user_name = u_name
            st.session_state.user_id = u_mobile.strip()
            st.rerun()
    st.stop()

# --- SIDEBAR (PW Style Navigation) ---
with st.sidebar:
    st.title("📖 English Knowledge")
    st.caption("By Harish Sir")
    st.divider()
    menu = st.radio("Go to", ["🏠 Dashboard", "🔴 LIVE CLASS", "🎥 Recorded", "📚 Notes", "💬 Ask Doubts"])
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = "Student"
        st.rerun()

# --- ADMIN PANEL (Teacher Control) ---
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Teacher Dashboard")
    t1, t2, t3, t4 = st.tabs(["🚀 LIVE CONTROL", "📊 POLLS", "📤 CONTENT", "💬 DOUBTS"])
    
    with t1:
        st.subheader("1. Your Live Stream")
        webrtc_streamer(key="sir-live-main", mode=WebRtcMode.SENDRECV, 
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        
        st.divider()
        st.subheader("2. Video Call with Student")
        if not st.session_state.call_active:
            if st.button("📞 START FACE-TO-FACE CALL"):
                st.session_state.call_active = True
                st.rerun()
        else:
            if st.button("🛑 END CALL (Return to Lecture)"):
                st.session_state.call_active = False
                st.rerun()

    with t2:
        with st.form("poll"):
            q = st.text_input("Question")
            a = st.text_input("Option A"); b = st.text_input("Option B")
            if st.form_submit_button("Launch Poll"):
                st.session_state.active_poll = {"q": q, "a": a, "b": b}
                st.session_state.poll_results = {a: 0, b: 0}; st.rerun()
        if st.session_state.active_poll:
            st.bar_chart(st.session_state.poll_results)
            if st.button("Close Poll"): st.session_state.active_poll = None; st.rerun()

    # (Notes and Doubts Logic)
    with t3:
        n_t = st.text_input("Notes Title"); n_f = st.file_uploader("Select PDF")
        if st.button("Upload"):
            if n_t and n_f: st.session_state.homework_list.insert(0, {"title": n_t, "file": n_f}); st.success("Notes Shared!")

# --- STUDENT PANEL (PW Interface) ---
else:
    if menu == "🔴 LIVE CLASS":
        st.markdown("### 🔴 Watching Live Session")
        
        # Automatic Switching Logic
        if st.session_state.call_active:
            st.warning("📞 Sir is talking to you! Video Interaction Active.")
            webrtc_streamer(key="pw-interaction", mode=WebRtcMode.SENDRECV,
                            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else:
            # Direct view without any button
            webrtc_streamer(key="pw-view", mode=WebRtcMode.RECVONLY,
                            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    elif menu == "🏠 Dashboard":
        st.title(f"Hi {st.session_state.user_name}!")
        if st.session_state.active_poll:
            st.markdown("#### 📊 Current Poll")
            st.write(st.session_state.active_poll['q'])
            v = st.radio("Choose", [st.session_state.active_poll['a'], st.session_state.active_poll['b']])
            if st.button("Vote"):
                st.session_state.poll_results[v] += 1; st.success("Vote Sent!")
        else:
            st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)

    elif menu == "🎥 Recorded":
        for v in st.session_state.recorded_classes:
            st.info(f"🎥 {v['title']} - Completed")

    elif menu == "📚 Notes":
        for n in st.session_state.homework_list:
            st.download_button(f"📥 Download {n['title']}", data=n['file'])

    elif menu == "💬 Ask Doubts":
        with st.form("d"):
            dq = st.text_area("Type Doubt")
            if st.form_submit_button("Ask Sir"):
                st.session_state.doubts.append({"user": st.session_state.user_name, "id": st.session_state.user_id, "question": dq, "answer": None})
        for d in reversed(st.session_state.doubts):
            if d['id'] == st.session_state.user_id:
                st.write(f"Q: {d['question']}"); 
                if d['answer']: st.info(f"A: {d['answer']}")