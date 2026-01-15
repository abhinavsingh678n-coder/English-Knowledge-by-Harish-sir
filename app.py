import streamlit as st
from streamlit_webrtc import webrtc_streamer
import time

# 1. PAGE SETTINGS
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage Initialization
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# 2. LOGIN SYSTEM (Security Check)
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    with st.form("login_form"):
        u_name = st.text_input("Apna Naam")
        u_mobile = st.text_input("Mobile Number (10 Digits Only)")
        if st.form_submit_button("Enter Classroom"):
            # Check for exactly 10 digits
            if u_name and u_mobile.isdigit() and len(u_mobile) == 10:
                st.session_state.logged_in = True
                st.session_state.user_name = u_name
                st.session_state.user_id = u_mobile
                st.rerun()
            else:
                st.error("❌ Galat Number! Kripya 10 digits ka sahi number dalein.")
    st.stop()

# 3. SIDEBAR BRANDING
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📖 English Knowledge</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>By Harish Sir</p>", unsafe_allow_html=True)
    st.divider()
    
    # Selection Menu
    menu = st.radio("Menu", ["🏠 Dashboard", "🔴 Live Class", "🎥 Recorded Classes", "📂 My Notes", "❓ Ask Doubt"])
    
    st.write("---")
    with st.expander("👨‍🏫 Teacher Access"):
        admin_pwd = st.text_input("Security Key", type="password")
        if admin_pwd == "harish_sir_pro":
            st.session_state.role = "Admin"
            st.success("Admin Mode Active!")
    
    if st.button("Logout Account"):
        st.session_state.logged_in = False
        st.session_state.role = "Student"
        st.rerun()

# 4. ADMIN PANEL (Harish Sir's View)
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Control Center")
    tab1, tab2, tab3 = st.tabs(["🚀 Go Live", "📤 Homework", "❓ Doubt Panel"])
    
    with tab1:
        st.subheader("Direct Live Class (App Se)")
        topic = st.text_input("Class Topic Name", "Grammar Lesson")
        # Direct Camera Access
        webrtc_streamer(key="teacher-live", rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        
        if st.button("End Class & Add to Recorded"):
            timestamp = time.strftime("%d-%b %H:%M")
            st.session_state.recorded_classes.insert(0, {"title": f"{topic} ({timestamp})"})
            st.success("Class khatam! Recorded section mein naam add ho gaya.")

    with tab2:
        st.subheader("Upload Study Material")
        with st.form("hw_form", clear_on_submit=True):
            h_title = st.text_input("Title")
            h_file = st.file_uploader("Choose PDF/Image")
            if st.form_submit_button("Upload"):
                if h_title and h_file:
                    st.session_state.homework_list.insert(0, {"title": h_title, "file": h_file})
                    st.success("Bacho ko bhej diya gaya!")

    with tab3:
        st.subheader("💬 Doubts from Students")
        if not st.session_state.doubts:
            st.info("Abhi koi sawal nahi hai.")
        else:
            for i, d in enumerate(st.session_state.doubts):
                with st.expander(f"Doubt from {d['user']} (ID: {d['id']})"):
                    st.write(f"**Q:** {d['question']}")
                    if d['answer']: st.success(f"**Ans:** {d['answer']}")
                    else:
                        ans = st.text_area("Jawab Likhein", key=f"ans_{i}")
                        if st.button("Send", key=f"btn_{i}"):
                            st.session_state.doubts[i]['answer'] = ans
                            st.rerun()

# 5. STUDENT PANEL (Bacho ka View)
else:
    if menu == "🏠 Dashboard":
        st.title(f"Namaste, {st.session_state.user_name}!")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)

    elif menu == "🔴 Live Class":
        st.subheader("🔴 Live Class Screen")
        # Student sees Sir's stream directly
        webrtc_streamer(key="student-view", rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    elif menu == "🎥 Recorded Classes":
        st.subheader("🎥 Purani Recorded Classes")
        if not st.session_state.recorded_classes:
            st.info("Abhi koi recorded class available nahi hai.")
        for vid in st.session_state.recorded_classes:
            st.warning(f"📺 {vid['title']} (Ready for playback)")

    elif menu == "📂 My Notes":
        st.subheader("📚 Notes & Homework")
        for item in st.session_state.homework_list:
            st.download_button(f"Download {item['title']}", data=item['file'])

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
                    st.success("Sawal bhej diya gaya!")
        
        st.divider()
        for d in reversed(st.session_state.doubts):
            if d['id'] == st.session_state.user_id:
                st.write(f"❓ Q: {d['question']}")
                if d['answer']: st.info(f"✅ Ans: {d['answer']}")
                else: st.warning("⏳ Sir reply karenge...")
                st.write("---")