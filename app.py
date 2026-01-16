import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

# 1. PAGE SETTINGS
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage Initialization
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'is_live' not in st.session_state: st.session_state.is_live = False 
if 'call_active' not in st.session_state: st.session_state.call_active = False 
if 'active_poll' not in st.session_state: st.session_state.active_poll = None
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- LOGIN SYSTEM ---
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    with st.expander("👨‍🏫 Harish Sir Access"):
        admin_key = st.text_input("Security Key", type="password")
        if st.button("Admin Login"):
            if admin_key == "harish_sir_pro":
                st.session_state.role = "Admin"
                st.rerun()

    st.subheader("Student Classroom Entry")
    u_name = st.text_input("Apna Naam")
    u_mobile = st.text_input("Mobile Number (10 Digits)")
    if st.button("Login"):
        if u_name and len(u_mobile.strip()) == 10:
            st.session_state.logged_in = True
            st.session_state.user_name = u_name
            st.session_state.user_id = u_mobile.strip()
            st.rerun()
        else:
            st.error("❌ Sahi 10-digit number dalein.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("📖 English Knowledge")
    st.caption("By Harish Sir")
    st.divider()
    menu = st.radio("Navigation", ["🏠 Dashboard", "🎥 Recorded", "📚 Notes", "💬 Ask Doubts"])
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = "Student"
        st.rerun()

# --- ADMIN PANEL (Teacher) ---
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Master Control Panel")
    t1, t2, t3 = st.tabs(["🚀 LIVE CLASS", "📊 POLLS", "📤 CONTENT"])
    
    with t1:
        if not st.session_state.is_live:
            if st.button("🔴 START LIVE CLASS"):
                st.session_state.is_live = True
                st.rerun()
        else:
            st.success("✅ Aap Live Hain! Bache ab jud sakte hain.")
            webrtc_streamer(key="teacher-live", mode=WebRtcMode.SENDRECV, 
                            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            st.divider()
            if not st.session_state.call_active:
                if st.button("📞 Start Interaction (Video Call)"):
                    st.session_state.call_active = True
                    st.rerun()
            else:
                if st.button("🛑 Stop Interaction"):
                    st.session_state.call_active = False
                    st.rerun()
            if st.button("🏁 END FULL CLASS"):
                st.session_state.is_live = False
                st.session_state.call_active = False
                st.rerun()

    with t2:
        poll_q = st.text_input("Poll Question")
        if st.button("Launch"): st.session_state.active_poll = poll_q

    with t3:
        n_t = st.text_input("Notes Title"); n_f = st.file_uploader("PDF")
        if st.button("Upload"):
            if n_t and n_f: st.session_state.homework_list.insert(0, {"title": n_t, "file": n_f}); st.success("Uploaded!")

# --- STUDENT PANEL (PW Style) ---
else:
    # PW Logic: Agar Sir Live hain, toh Dashboard par sabse upar Join button aayega
    if st.session_state.is_live:
        st.markdown("""
            <style>
            .live-box { background-color: #ff4b4b; color: white; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold; margin-bottom: 20px; animation: blinker 1.5s linear infinite; }
            @keyframes blinker { 50% { opacity: 0.6; } }
            </style>
            <div class="live-box">🔴 HARISH SIR IS LIVE NOW!</div>
            """, unsafe_allow_html=True)
        
        if st.button("▶️ JOIN LIVE CLASS NOW"):
            st.session_state.show_live = True
        
        if st.session_state.get('show_live', False):
            if st.session_state.call_active:
                st.warning("📞 Interaction Mode: Sir is talking to you!")
                webrtc_streamer(key="stu-interaction-v2", mode=WebRtcMode.SENDRECV, 
                                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            else:
                st.info("📺 Watching Harish Sir Live...")
                webrtc_streamer(key="stu-view-v2", mode=WebRtcMode.RECVONLY, 
                                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            if st.button("Leave Class"):
                st.session_state.show_live = False
                st.rerun()
        st.divider()

    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.user_name}")
        if not st.session_state.is_live:
            st.info("Abhi koi Live class nahi chal rahi hai. Sir ke Live aate hi Join ka button aa jayega.")
        if st.session_state.active_poll:
            st.markdown(f"#### 📊 Poll: {st.session_state.active_poll}")
            if st.button("Done"): st.success("Voted!")

    elif menu == "🎥 Recorded":
        st.write("Lectures appear here.")

    elif menu == "📚 Notes":
        for n in st.session_state.homework_list:
            st.download_button(f"Download {n['title']}", data=n['file'])

    elif menu == "💬 Ask Doubts":
        dq = st.text_area("Type Doubt")
        if st.button("Send"):
            st.session_state.doubts.append({"id": st.session_state.user_id, "q": dq})
            st.success("Sent to Sir!")