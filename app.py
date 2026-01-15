import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import time

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage Initialization
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- UI STYLE ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; background-color: #007bff; color: white; }
    .doubt-card { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #007bff; margin-bottom: 10px; box-shadow: 0px 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN SYSTEM (Mobile Validation)
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    
    # Harish Sir Hidden Access
    with st.expander("👨‍🏫 Staff Login"):
        admin_pwd = st.text_input("Security Key", type="password")
        if st.button("Admin Login"):
            if admin_pwd == "harish_sir_pro":
                st.session_state.role = "Admin"
                st.rerun()

    st.write("---")
    # Student Login Form
    st.subheader("Student Classroom Entry")
    u_name = st.text_input("Apna Pura Naam")
    u_mobile = st.text_input("Mobile Number (10 Digits Only)")
    
    if st.button("Enter Classroom"):
        clean_num = u_mobile.strip()
        if u_name and clean_num.isdigit() and len(clean_num) == 10:
            st.session_state.logged_in = True
            st.session_state.user_name = u_name
            st.session_state.user_id = clean_num
            st.rerun()
        else:
            st.error("❌ Galat Entry! Naam aur 10-digit mobile number zaruri hai.")
    st.stop()

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📖 English Knowledge</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>By Harish Sir</p>", unsafe_allow_html=True)
    st.divider()
    
    menu = st.radio("Navigation", ["🏠 Dashboard", "🔴 Live Class & Video Call", "🎥 Recorded Classes", "📂 My Notes", "❓ Ask Doubt"])
    
    st.divider()
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = "Student"
        st.rerun()

# 4. ADMIN PANEL (Harish Sir's View)
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Interaction Panel")
    tab1, tab2, tab3 = st.tabs(["🚀 Live & Video Call", "📤 Upload Homework", "💬 Doubt Panel"])
    
    with tab1:
        st.subheader("Start Live Class / Student Interaction")
        topic = st.text_input("Class Topic Name")
        # Direct Video Call/Live System
        webrtc_streamer(key="sir-interaction", mode=WebRtcMode.SENDRECV,
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        
        st.divider()
        st.subheader("Save as Recorded (Permanent)")
        rec_link = st.text_input("Paste YouTube/Drive Video Link")
        if st.button("Add to Recorded Library"):
            if topic and rec_link:
                st.session_state.recorded_classes.insert(0, {"title": topic, "link": rec_link})
                st.success("Bacho ki library mein add ho gaya!")

    with tab2:
        st.subheader("Upload Notes/PDF")
        h_t = st.text_input("Notes Title")
        h_f = st.file_uploader("Select File")
        if st.button("Upload & Send"):
            if h_t and h_f:
                st.session_state.homework_list.insert(0, {"title": h_t, "file": h_f})
                st.success("Uploaded successfully!")

    with tab3:
        st.subheader("💬 Bachon ke Doubts (With ID)")
        if not st.session_state.doubts:
            st.info("Abhi koi naya doubt nahi aaya hai.")
        else:
            for i, d in enumerate(st.session_state.doubts):
                with st.expander(f"From: {d['user']} (ID: {d['id']})"):
                    st.write(f"**Q:** {d['question']}")
                    if d['answer']: st.success(f"**Ans:** {d['answer']}")
                    else:
                        ans = st.text_area("Reply", key=f"ans_{i}")
                        if st.button("Send Reply", key=f"btn_{i}"):
                            st.session_state.doubts[i]['answer'] = ans
                            st.rerun()

# 5. STUDENT PANEL (Bachon ka View)
else:
    if menu == "🏠 Dashboard":
        st.title(f"Welcome, {st.session_state.user_name}!")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)

    elif menu == "🔴 Live Class & Video Call":
        st.subheader("🔴 Joining Video Interaction")
        st.info("Sir Live aayenge toh yahan video dikhegi. Sir ke kehne par hi 'Start' karein.")
        # Students can receive Sir's video and send their own for interaction
        webrtc_streamer(key="student-call", mode=WebRtcMode.SENDRECV,
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    elif menu == "🎥 Recorded Classes":
        st.subheader("🎥 Purani Recorded Classes")
        for vid in st.session_state.recorded_classes:
            with st.expander(f"▶️ {vid['title']}"):
                st.video(vid['link'])

    elif menu == "📂 My Notes":
        st.subheader("📚 Study Material")
        for item in st.session_state.homework_list:
            st.download_button(f"📥 Download {item['title']}", data=item['file'])

    elif menu == "❓ Ask Doubt":
        st.header("❓ Doubt Box")
        with st.form("doubt_f", clear_on_submit=True):
            q = st.text_area("Apna Sawal Likhein")
            if st.form_submit_button("Sir se Puchein"):
                if q:
                    st.session_state.doubts.append({
                        "user": st.session_state.user_name, 
                        "id": st.session_state.user_id, 
                        "question": q, 
                        "answer": None
                    })
                    st.success("Doubt bhej diya gaya!")
        
        st.divider()
        st.subheader("📝 Mere Purane Doubt ke Jawab")
        for d in reversed(st.session_state.doubts):
            if d['id'] == st.session_state.user_id:
                st.markdown(f"""<div class='doubt-card'><strong>Q:</strong> {d['question']}</div>""", unsafe_allow_html=True)
                if d['answer']: st.info(f"✅ **Ans:** {d['answer']}")
                else: st.warning("⏳ Sir reply karenge...")
                st.write("---")