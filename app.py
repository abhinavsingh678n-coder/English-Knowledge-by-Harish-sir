import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

# 1. PAGE SETTINGS
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Global Variable Simulation (Bacho aur Sir ko sync karne ke liye)
if 'is_live' not in st.session_state: st.session_state.is_live = False 
if 'call_active' not in st.session_state: st.session_state.call_active = False 

# Data Storage Initialization
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
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

# --- ADMIN PANEL (Harish Sir) ---
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Master Control Panel")
    t1, t2, t3 = st.tabs(["🚀 LIVE CLASS", "📊 POLLS", "📤 CONTENT"])
    
    with t1:
        # Sir ka Live Status Control
        live_status = st.toggle("🔴 START / STOP LIVE CLASS", value=st.session_state.is_live)
        st.session_state.is_live = live_status
        
        if st.session_state.is_live:
            st.success("✅ Aap Live Hain! Bache ab jud sakte hain.")
            webrtc_streamer(key="sir-live-v3", mode=WebRtcMode.SENDRECV, 
                            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            
            st.divider()
            call_status = st.toggle("📞 Start Interaction (Video Call)", value=st.session_state.call_active)
            st.session_state.call_active = call_status
        else:
            st.info("Class band hai. Live jaane ke liye upar wala button dabayein.")

# --- STUDENT PANEL (PW Style Logic) ---
else:
    # PW Style Notification Box
    if st.session_state.is_live:
        st.markdown("""
            <div style="background-color:#ff4b4b; color:white; padding:20px; border-radius:15px; text-align:center; font-weight:bold; margin-bottom:20px; border: 2px solid white;">
                <h2 style="color:white; margin:0;">🔴 HARISH SIR IS LIVE NOW!</h2>
                <p style="margin:5px 0 0 0;">Niche join button par click karein</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("▶️ JOIN LIVE CLASS NOW", use_container_width=True):
            st.session_state.show_live_screen = True

        if st.session_state.get('show_live_screen', False):
            if st.session_state.call_active:
                st.warning("📞 Interaction Mode: Sir is talking to you face-to-face!")
                webrtc_streamer(key="stu-interaction-v3", mode=WebRtcMode.SENDRECV, 
                                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            else:
                st.info("📺 Watching Harish Sir Live...")
                webrtc_streamer(key="stu-view-v3", mode=WebRtcMode.RECVONLY, 
                                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            
            if st.button("Leave Class"):
                st.session_state.show_live_screen = False
                st.rerun()
    
    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.user_name}")
        if not st.session_state.is_live:
            st.info("Abhi koi Live class nahi chal rahi hai. Sir ke Live aate hi yahan Join ka button aa jayega.")
        else:
            st.success("Class chalu hai! Upar 'Join Live' par click karein.")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)

    elif menu == "🎥 Recorded":
        st.write("Purane lectures yahan dikhengi.")

    elif menu == "📚 Notes":
        for n in st.session_state.homework_list:
            st.download_button(f"📥 Download {n['title']}", data=n['file'])

    elif menu == "💬 Ask Doubts":
        dq = st.text_area("Type Doubt")
        if st.button("Send Doubt"):
            st.session_state.doubts.append({"id": st.session_state.user_id, "q": dq})
            st.success("Sent to Sir!")