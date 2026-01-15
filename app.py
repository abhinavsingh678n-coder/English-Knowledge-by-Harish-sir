import streamlit as st
from streamlit_webrtc import webrtc_streamer
import time

# 1. Page Config
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage initialization
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- LOGIN SECURITY (10 Digit Check) ---
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    with st.form("login_form"):
        u_name = st.text_input("Apna Naam")
        u_mobile = st.text_input("Mobile Number (10 Digits)")
        if st.form_submit_button("Enter Classroom"):
            # Mobile number validation
            if u_name and u_mobile.isdigit() and len(u_mobile) == 10:
                st.session_state.logged_in = True
                st.session_state.user_name = u_name
                st.session_state.user_id = u_mobile
                st.rerun()
            else:
                st.error("❌ Galat Number! Kripya 10 digits ka sahi mobile number dalein.")
    st.stop()

# --- SIDEBAR BRANDING ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📖 English Knowledge</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>By Harish Sir</p>", unsafe_allow_html=True)
    st.divider()
    
    menu = st.radio("Menu", ["🏠 Dashboard", "🔴 Live Class", "🎥 Recorded Classes", "📂 My Notes", "❓ Ask Doubt"])
    
    st.write("---")
    with st.expander("👨‍🏫 Staff Login"):
        admin_pwd = st.text_input("Security Key", type="password")
        if admin_pwd == "harish_sir_pro":
            st.session_state.role = "Admin"
            st.success("Admin Mode Active!")
        if st.button("Logout"):
            st.session_state.role = "Student"
            st.session_state.logged_in = False
            st.rerun()

# --- ADMIN PANEL (Harish Sir) ---
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Control Center")
    tab1, tab2, tab3 = st.tabs(["🚀 Go Live", "📤 Homework", "❓ Doubt Panel"])
    
    with tab1:
        st.subheader("Direct Live Class")
        live_topic = st.text_input("Aaj ki Class ka Topic", value="General English")
        # In-app video streamer for Sir
        webrtc_streamer(key="teacher-live", rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        
        if st.button("End Class & Save to Recorded"):
            # Auto-save logic
            timestamp = time.strftime("%d-%m-%Y %H:%M")
            st.session_state.recorded_classes.insert(0, {"title": f"{live_topic} ({timestamp})", "type": "Live Record"})
            st.success("Class khatam ho gayi aur Recorded list mein add ho gayi!")

    with tab2:
        # Homework upload logic
        h_title = st.text_input("Notes Title")
        h_file = st.file_uploader("Select PDF/Image")
        if st.button("Upload"):
            if h_title and h_file:
                st.session_state.homework_list.insert(0, {"title": h_title, "file": h_file})
                st.success("Homework uploaded!")

    with tab3:
        # Doubt handling with ID
        for i, d in enumerate(st.session_state.doubts):
            with st.expander(f"Doubt from {d['user']} (ID: {d['id']})"):
                st.write(f"Q: {d['question']}")
                if d['answer']: st.info(f"Ans: {d['answer']}")
                else:
                    ans = st.text_area("Jawab Likhein", key=f"admin_ans_{i}")
                    if st.button("Send Reply", key=f"admin_btn_{i}"):
                        st.session_state.doubts[i]['answer'] = ans
                        st.rerun()

# --- STUDENT PANEL ---
else:
    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.user_name}!")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)

    elif menu == "🔴 Live Class":
        st.subheader("🔴 Joining Live Session...")
        # Student views Sir's camera directly
        webrtc_streamer(key="student-view", rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    elif menu == "🎥 Recorded Classes":
        st.subheader("🎥 Purani Classes")
        if not st.session_state.recorded_classes:
            st.info("Abhi koi recorded class nahi hai.")
        for vid in st.session_state.recorded_classes:
            st.warning(f"📺 {vid['title']} - (Video processing logic active)")

    elif menu == "📂 My Notes":
        # Notes download for students
        for item in st.session_state.homework_list:
            st.download_button(f"Download {item['title']}", data=item['file'])

    elif menu == "❓ Ask Doubt":
        # Doubt asking with mobile validation
        with st.form