import streamlit as st
from streamlit_webrtc import webrtc_streamer

# 1. Page Config
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide")

# Session State for Content Storage
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'page' not in st.session_state: st.session_state.page = "Dashboard"

# --- SIDEBAR ---
with st.sidebar:
    st.title("Selection Way 🎓")
    st.write("Teacher: **Harish Sir**")
    st.divider()
    if st.button("🏠 Home Dashboard"): st.session_state.page = "Dashboard"
    if st.button("🔴 Live Class"): st.session_state.page = "Live"
    if st.button("📂 My Homework/Notes"): st.session_state.page = "Notes"
    if st.button("👨‍🏫 Teacher Admin"): st.session_state.page = "Admin"

# --- 1. ADMIN PANEL (Homework Upload Kaise Karein) ---
if st.session_state.page == "Admin":
    st.header("👨‍🏫 Teacher Control Center")
    pwd = st.text_input("Security Password", type="password")
    
    if pwd == "harish_sir_pro":
        st.subheader("📤 Upload New Homework/Notes")
        with st.form("upload_form", clear_on_submit=True):
            h_title = st.text_input("Homework Ka Topic (e.g. Tenses Sheet 1)")
            h_file = st.file_uploader("Choose PDF or Image", type=['pdf', 'jpg', 'png'])
            submit = st.form_submit_button("App Par Bhejein 🚀")
            
            if submit and h_title and h_file:
                # Adding to list
                st.session_state.homework_list.append({"title": h_title, "file": h_file})
                st.success(f"'{h_title}' successfully bacho ke liye upload ho gaya!")

# --- 2. NOTES SECTION (Bacho ko kaise dikhega) ---
elif st.session_state.page == "Notes":
    st.header("📚 Your Study Material")
    if not st.session_state.homework_list:
        st.info("Abhi sir ne koi homework nahi dala hai.")
    else:
        for item in st.session_state.homework_list:
            with st.container():
                col1, col2 = st.columns([3, 1])
                col1.write(f"📖 **{item['title']}**")
                col2.download_button("Download PDF", data=item['file'], file_name=f"{item['title']}.pdf")
                st.divider()

# --- 3. DASHBOARD ---
elif st.session_state.page == "Dashboard":
    st.title("Welcome to Harish Sir's Academy")
    st.image("https://img.freepik.com/free-vector/digital-learning-abstract-concept-vector-illustration_335657-2417.jpg", width=400)
    st.success("Aaj ki Live Class 8:00 PM par hogi. 'Live Class' tab check karein.")

# --- 4. LIVE CLASS ---
elif st.session_state.page == "Live":
    st.title("🔴 Live Classroom")
    webrtc_streamer(key="live-stream", 
                    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})