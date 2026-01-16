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

# --- LOGIN SYSTEM (10-Digit Mobile Check) ---
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    with st.expander("👨‍🏫 Harish Sir Access"):
        admin_key = st.text_input("Security Key", type="password")
        if st.button("Admin Login"):
            if admin_key == "harish_sir_pro":
                st.session_state.role = "Admin"
                st.rerun()

    st.subheader("Student Classroom Login")
    u_name = st.text_input("Apna Naam")
    u_mobile = st.text_input("Mobile Number (10 Digits Only)")
    if st.button("Login"):
        if u_name and len(u_mobile.strip()) == 10:
            st.session_state.logged_in = True
            st.session_state.user_name = u_name
            st.session_state.user_id = u_mobile.strip()
            st.rerun()
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

# --- ADMIN PANEL (Teacher Control) ---
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Master Control Panel")
    t1, t2, t3 = st.tabs(["🚀 LIVE CLASS", "📊 POLLS", "📤 CONTENT"])
    
    with t1:
        if not st.session_state.is_live:
            if st.button("🔴 START LIVE CLASS"):
                st.session_state.is_live = True
                st.rerun()
        else:
            st.success("✅ Aap Live Hain!")
            webrtc_streamer(key="sir-live-stream", mode=WebRtcMode.SENDRECV, 
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
        poll_q = st.text_input("Enter Question")
        if st.button("Launch Poll"):
            st.session_state.active_poll = poll_q
            st.success("Poll Live!")

    with t3:
        n_t = st.text_input("Notes Title"); n_f = st.file_uploader("PDF Only")
        if st.button("Upload"):
            if n_t and n_f: st.session_state.homework_list.insert(0, {"title": n_t, "file": n_f}); st.success("Uploaded!")

# --- STUDENT PANEL (PW Style) ---
else:
    if st.session_state.is_live:
        st.markdown("""
            <div style="background-color:#ff4b4b; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; margin-bottom:10px;">
                🔴 HARISH SIR IS LIVE NOW!
            </div>
            """, unsafe_allow_html=True)
        
        # PW Style: Direct Entry to Live
        if st.session_state.call_active:
            st.warning("📞 Interaction On: Sir is talking to you!")
            webrtc_streamer(key="stu-interaction-pw", mode=WebRtcMode.SENDRECV, 
                            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        else:
            webrtc_streamer(key="stu-view-pw", mode=WebRtcMode.RECVONLY, 
                            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        st.divider()

    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.user_name}")
        if not st.session_state.is_live:
            st.info("Abhi koi Live class nahi chal rahi hai. Sir ke Live aate hi yahan Join ka button aa jayega.")
        if st.session_state.active_poll:
            st.markdown(f"#### 📊 Poll: {st.session_state.active_poll}")
            if st.button("Vote"): st.success("Recorded!")
        else:
            st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)

    elif menu == "🎥 Recorded":
        st.write("Recorded lectures yahan dikhengi.")

    elif menu == "📚 Notes":
        for n in st.session_state.homework_list:
            st.download_button(f"📥 Download {n['title']}", data=n['file'])

    elif menu == "💬 Ask Doubts":
        dq = st.text_area("Type Doubt")
        if st.button("Send"):
            st.session_state.doubts.append({"id": st.session_state.user_id, "q": dq})
            st.success("Sent!")