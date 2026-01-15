import streamlit as st
from streamlit_webrtc import webrtc_streamer

# 1. Page Config
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide")

# 2. Professional Style CSS
st.markdown("""
    <style>
    .stButton>button { border-radius: 8px; font-weight: bold; }
    .chat-box { background-color: #f1f3f4; padding: 10px; border-radius: 10px; height: 200px; overflow-y: auto; margin-bottom: 10px; border: 1px solid #ddd;}
    .student-msg { background-color: white; padding: 5px 10px; border-radius: 5px; margin-bottom: 5px; border-left: 4px solid #1a73e8; }
    </style>
    """, unsafe_allow_html=True)

# Session State for Chat and Navigation
if 'messages' not in st.session_state: st.session_state.messages = []
if 'page' not in st.session_state: st.session_state.page = "Dashboard"

# --- SIDEBAR ---
with st.sidebar:
    st.title("Selection Way 🎓")
    st.write(f"Teacher: **Harish Sir**")
    st.write(f"Active Students: **10**")
    st.divider()
    if st.button("🏠 Home"): st.session_state.page = "Dashboard"
    if st.button("🔴 Live Class"): st.session_state.page = "Live"
    if st.button("👨‍🏫 Admin"): st.session_state.page = "Admin"

# --- LIVE CLASS PAGE (Teachmint Style) ---
if st.session_state.page == "Live":
    st.title("🔴 Live Classroom")
    
    col_video, col_chat = st.columns([2, 1])
    
    with col_video:
        st.subheader("Video Feed")
        # In-App Video Streamer
        webrtc_streamer(key="live-stream", 
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        st.caption("Tip: Sir, apna camera aur mic yahan se allow karein.")

    with col_chat:
        st.subheader("💬 Live Chat")
        # Chat Display area
        chat_placeholder = st.empty()
        with chat_placeholder.container():
            st.markdown('<div class="chat-box">', unsafe_allow_html=True)
            for msg in st.session_state.messages:
                st.markdown(f'<div class="student-msg"><b>{msg["user"]}:</b> {msg["text"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat Input
        with st.form("chat_form", clear_on_submit=True):
            user_msg = st.text_input("Sawal puchein...", placeholder="Sir, ye repeat kar dijiye")
            if st.form_submit_button("Send"):
                if user_msg:
                    st.session_state.messages.append({"user": "Student", "text": user_msg})
                    st.rerun()

# --- OTHER PAGES ---
elif st.session_state.page == "Dashboard":
    st.header("Welcome to your Academy")
    st.image("https://img.freepik.com/free-vector/digital-learning-abstract-concept-vector-illustration_335657-2417.jpg", width=400)
    st.info("Aapki live class 'Live Class' tab mein shuru hoti hai.")
    
elif st.session_state.page == "Admin":
    st.header("Teacher Controls")
    st.write("Sir, yahan se aap bacho ke messages dekh sakte hain aur content upload kar sakte hain.")