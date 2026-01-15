import streamlit as st
from streamlit_webrtc import webrtc_streamer

# 1. Page Config
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide")

# Session State for Data Storage (Taki refresh par data turant na ude)
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'role' not in st.session_state: st.session_state.role = "Student"

# --- SIDEBAR ---
with st.sidebar:
    st.title("Selection Way 🎓")
    st.write(f"Teacher: **Harish Sir**")
    st.divider()
    
    # Menu for Students
    menu = st.radio("Student Menu", ["🏠 Home", "🔴 Live Class", "🎥 Recorded Classes", "📂 My Notes"])
    
    st.write("---")
    # Secret Teacher Entry
    with st.expander("👨‍🏫 Staff Login (Harish Sir)"):
        admin_pwd = st.text_input("Security Key", type="password")
        if admin_pwd == "harish_sir_pro":
            st.session_state.role = "Admin"
            st.success("Admin Mode Active!")
        else:
            st.session_state.role = "Student"

# --- LOGIC START ---

# 1. HARISH SIR'S ADMIN PANEL (Live Class & Homework)
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Control Center")
    
    tab1, tab2, tab3 = st.tabs(["🚀 Start Live Class", "📤 Upload Homework", "🎬 Add Recorded Video"])
    
    with tab1:
        st.subheader("Bacho ko Live Padhayein")
        st.write("Niche 'Start' button dabayein aur camera allow karein.")
        webrtc_streamer(key="admin-live", 
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    with tab2:
        st.subheader("Homework Bhejein")
        with st.form("hw_form", clear_on_submit=True):
            title = st.text_input("Topic Name")
            file = st.file_uploader("Select PDF/Image", type=['pdf', 'jpg', 'png'])
            if st.form_submit_button("Upload to App"):
                if title and file:
                    st.session_state.homework_list.append({"title": title, "file": file})
                    st.success(f"'{title}' bacho ko bhej diya gaya!")

    with tab3:
        st.subheader("Purani Class Add Karein")
        with st.form("vid_form", clear_on_submit=True):
            v_title = st.text_input("Video Topic")
            v_link = st.text_input("YouTube Link")
            if st.form_submit_button("Add Video"):
                if v_title and v_link:
                    st.session_state.recorded_classes.append({"title": v_title, "link": v_link})
                    st.success("Video Library mein add ho gaya!")

# 2. STUDENT PAGES (Sir ke logout hone par ya bacho ke liye)
else:
    if menu == "🏠 Home":
        st.title("Welcome to Selection Way")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)
        st.info("Sir Live aayenge toh 'Live Class' tab mein join karein.")

    elif menu == "🔴 Live Class":
        st.subheader("🔴 Harish Sir ki Live Class")
        # Bachon ke liye viewer
        webrtc_streamer(key="student-view", 
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    elif menu == "🎥 Recorded Classes":
        st.subheader("🎥 Purani Recorded Classes")
        if not st.session_state.recorded_classes:
            st.write("Abhi koi recorded class nahi hai.")
        for vid in st.session_state.recorded_classes:
            with st.expander(f"▶️ {vid['title']}"):
                st.video(vid['link'])

    elif menu == "📂 My Notes":
        st.subheader("📚 Homework & Notes")
        if not st.session_state.homework_list:
            st.write("Sir ne abhi koi notes nahi dale hain.")
        for item in st.session_state.homework_list:
            st.download_button(f"Download {item['title']}", data=item['file'], file_name=f"{item['title']}.pdf")