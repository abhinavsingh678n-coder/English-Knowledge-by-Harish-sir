import streamlit as st
from streamlit_webrtc import webrtc_streamer
import time

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage Initialization (Ye info server chalne tak save rahegi)
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- UI STYLE ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #007bff; color: white; }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN SYSTEM (Mobile Number Validation)
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    st.info("Kripya apna sahi naam aur 10-digit mobile number dalein.")
    with st.container():
        u_name = st.text_input("Apna Pura Naam")
        u_mobile = st.text_input("Mobile Number (ID)")
        if st.button("Enter Classroom"):
            if u_name and u_mobile.isdigit() and len(u_mobile) == 10:
                st.session_state.logged_in = True
                st.session_state.user_name = u_name
                st.session_state.user_id = u_mobile
                st.success(f"Swagat hai, {u_name}!")
                st.rerun()
            else:
                st.error("❌ Galat Detail! Naam bharein aur Mobile Number sahi 10 digits ka hona chahiye.")
    
    # Staff access during login screen
    with st.expander("👨‍🏫 Harish Sir Login"):
        admin_key = st.text_input("Enter Admin Key", type="password")
        if st.button("Admin Login"):
            if admin_key == "harish_sir_pro":
                st.session_state.role = "Admin"
                st.rerun()
    st.stop()

# 3. SIDEBAR (Navigation & Branding)
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>📖 English Knowledge</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>By Harish Sir</p>", unsafe_allow_html=True)
    st.divider()
    
    # Tabs for navigation
    menu = st.radio("Navigation", ["🏠 Dashboard", "🔴 Live Class", "🎥 Recorded Classes", "📂 My Notes", "❓ Ask Doubt"])
    
    st.divider()
    if st.button("🚪 Logout App"):
        st.session_state.logged_in = False
        st.session_state.role = "Student"
        st.rerun()

# 4. ADMIN PANEL (Harish Sir's View)
if st.session_state.role == "Admin":
    st.title("👨‍🏫 Harish Sir's Dashboard")
    adm_tab1, adm_tab2, adm_tab3 = st.tabs(["🚀 Live & Record", "📤 Upload Notes", "💬 Doubt Panel"])
    
    with adm_tab1:
        st.subheader("Start Direct Live Class")
        live_topic = st.text_input("Class Topic", "English Grammar Part 1")
        webrtc_streamer(key="teacher-live", rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        if st.button("End Class & Save Recording"):
            t_stamp = time.strftime("%d-%m %I:%M %p")
            st.session_state.recorded_classes.insert(0, {"title": f"{live_topic} ({t_stamp})"})
            st.success("Class Record ho gayi aur list mein add ho gayi!")

    with adm_tab2:
        st.subheader("Upload Notes for Students")
        n_title = st.text_input("Notes Title (e.g. Tense Chart)")
        n_file = st.file_uploader("Upload PDF/Image")
        if st.button("Send to Students"):
            if n_title and n_file:
                st.session_state.homework_list.insert(0, {"title": n_title, "file": n_file})
                st.success("Notes Upload Successfully!")

    with adm_tab3:
        st.subheader("Bachon ke Doubts")
        if not st.session_state.doubts:
            st.info("Abhi koi naya sawal nahi hai.")
        else:
            for i, d in enumerate(st.session_state.doubts):
                with st.expander(f"Doubt from: {d['user']} (ID: {d['id']})"):
                    st.write(f"**Q:** {d['question']}")
                    if d['answer']:
                        st.success(f"✅ Your Answer: {d['answer']}")
                    else:
                        reply = st.text_area("Answer Likhein", key=f"ans_{i}")
                        if st.button("Reply Now", key=f"btn_{i}"):
                            st.session_state.doubts[i]['answer'] = reply
                            st.rerun()

# 5. STUDENT PANEL (Bacho ka View)
else:
    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.user_name}!")
        st.markdown(f"**User ID:** {st.session_state.user_id}")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)
        st.info("Side menu se apni class join karein ya notes download karein.")

    elif menu == "🔴 Live Class":
        st.subheader("🔴 Live Class Screen")
        st.write("Sir live aayenge toh yahan video dikhegi.")
        webrtc_streamer(key="student-view", rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    elif menu == "🎥 Recorded Classes":
        st.subheader("🎥 Purani Recorded Classes")
        if not st.session_state.recorded_classes:
            st.info("Abhi koi video available nahi hai.")
        else:
            for vid in st.session_state.recorded_classes:
                st.warning(f"📺 {vid['title']} - (Video Processing...)")

    elif menu == "📂 My Notes":
        st.subheader("📚 Notes & Homework")
        if not st.session_state.homework_list:
            st.info("Abhi koi notes nahi hain.")
        else:
            for item in st.session_state.homework_list:
                st.download_button(f"📥 Download: {item['title']}", data=item['file'])

    elif menu == "❓ Ask Doubt":
        st.header("❓ Doubt Box")
        with st.form("doubt_f"):
            q = st.text_area("Apna Sawal Puchein")
            if st.form_submit_button("Sir ko Bhejein"):
                if q:
                    st.session_state.doubts.append({
                        "user": st.session_state.user_name, 
                        "id": st.session_state.user_id, 
                        "question": q, 
                        "answer": None
                    })
                    st.success("Sawal bhej diya gaya! Niche jawab check karein.")
        
        st.divider()
        st.subheader("📝 Mere Purane Sawal")
        for d in reversed(st.session_state.doubts):
            # Student ko sirf apna hi doubt dikhega
            if d['id'] == st.session_state.user_id:
                with st.container():
                    st.write(f"❓ **Q:** {d['question']}")
                    if d['answer']:
                        st.info(f"👨‍🏫 **Sir ka Jawab:** {d['answer']}")
                    else:
                        st.warning("⏳ Sir ka jawab aana baaki hai...")
                    st.write("---")