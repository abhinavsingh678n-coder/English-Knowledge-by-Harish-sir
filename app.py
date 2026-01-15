import streamlit as st
from streamlit_webrtc import webrtc_streamer

# 1. Page Config - Browser tab mein bhi yahi naam dikhega
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Session State for Data Storage
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'role' not in st.session_state: st.session_state.role = "Student"

# --- SIDEBAR (Updated Branding) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📖 English Knowledge</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>By Harish Sir</p>", unsafe_allow_html=True)
    st.divider()
    
    # Menu for Students
    menu = st.radio("Student Menu", ["🏠 Home Dashboard", "🔴 Live Class", "🎥 Recorded Classes", "📂 My Notes"])
    
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
    st.info("Sir, yahan se aap apni classes aur homework manage kar sakte hain.")
    
    tab1, tab2, tab3 = st.tabs(["🚀 Start Live Class", "📤 Upload Homework", "🎬 Add Recorded Video"])
    
    with tab1:
        st.subheader("Bacho ko Live Padhayein")
        st.write("Niche 'Start' button dabayein aur camera allow karein.")
        # Isse Sir app ke andar hi live ho jayenge
        webrtc_streamer(key="admin-live", 
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    with tab2:
        st.subheader("Homework Bhejein")
        with st.form("hw_form", clear_on_submit=True):
            title = st.text_input("Homework Ka Topic (e.g. Tenses Sheet 1)")
            file = st.file_uploader("Select PDF or Image", type=['pdf', 'jpg', 'png'])
            if st.form_submit_button("App Par Bhejein 🚀"):
                if title and file:
                    st.session_state.homework_list.append({"title": title, "file": file})
                    st.success(f"'{title}' bacho ko bhej diya gaya!")

    with tab3:
        st.subheader("Purani Recorded Class Add Karein")
        with st.form("vid_form", clear_on_submit=True):
            v_title = st.text_input("Video Ka Topic")
            v_link = st.text_input("YouTube Link Copy-Paste Karein")
            if st.form_submit_button("Library Mein Add Karein"):
                if v_title and v_link:
                    st.session_state.recorded_classes.append({"title": v_title, "link": v_link})
                    st.success("Video recorded section mein add ho gaya!")

# 2. STUDENT PAGES
else:
    if menu == "🏠 Home Dashboard":
        st.title("English Knowledge by Harish Sir")
        st.markdown("### 🎓 Ab Selection Hoga Pakka!")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)
        st.info("Aaj ki Live Class ki timing ke liye apne WhatsApp group ko check karein.")

    elif menu == "🔴 Live Class":
        st.subheader("🔴 Live Classroom")
        st.write("Sir Live aayenge toh aapko yahan dikhenge. Niche 'Start' dabayein.")
        webrtc_streamer(key="student-view", 
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    elif menu == "🎥 Recorded Classes":
        st.subheader("🎥 Purani Recorded Classes")
        if not st.session_state.recorded_classes:
            st.info("Abhi koi recorded class available nahi hai.")
        for vid in st.session_state.recorded_classes:
            with st.expander(f"▶️ {vid['title']}"):
                st.video(vid['link'])

    elif menu == "📂 My Notes":
        st.subheader("📚 Homework & Study Material")
        if not st.session_state.homework_list:
            st.info("Harish Sir ne abhi koi naye notes nahi dale hain.")
        for item in st.session_state.homework_list:
            with st.container():
                col1, col2 = st.columns([3, 1])
                col1.write(f"📖 **{item['title']}**")
                col2.download_button(f"Download", data=item['file'], file_name=f"{item['title']}.pdf")
                st.divider()