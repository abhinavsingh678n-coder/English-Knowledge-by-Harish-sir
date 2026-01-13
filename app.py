import streamlit as st
import datetime

# Page Settings
st.set_page_config(page_title="Selection Way Pro", layout="wide", page_icon="🎓")

# Sidebar - Branding & Role
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=100)
st.sidebar.title("Selection Way")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.title("🔐 Secure Classroom Login")
    col1, col2 = st.columns(2)
    
    with col1:
        role = st.selectbox("Aapka Role", ["Student", "Teacher"])
        password = st.text_input("Security Password", type="password")
        
        if st.button("Secure Login"):
            if password == "1234":
                st.session_state.logged_in = True
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Ghalat Password! Kripya sahi password dalein.")
    
    with col2:
        st.info("### Legal Disclaimer\nYe app 'Selection Way' educational services ke liye banaya gaya hai. Iska misuse karna mana hai.")

# --- DASHBOARD ---
else:
    st.sidebar.success(f"Log-in as: {st.session_state.role}")
    menu = st.sidebar.radio("Navigation", ["Classroom", "Attendance", "Study Material", "Homework/Test", "Settings"])

    if menu == "Classroom":
        st.header("🔴 Live Teaching Hub")
        st.markdown("---")
        col_info, col_btn = st.columns([2, 1])
        with col_info:
            st.subheader("Today's Topic: English Grammar")
            st.write("Teacher is ready. Please join the room for live discussion.")
        with col_btn:
            if st.button("JOIN LIVE CLASS NOW", use_container_width=True):
                # Professional Jitsi Room
                room_link = "https://meet.jit.si/SelectionWay_Pro_Class"
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={room_link}">', unsafe_allow_html=True)

    elif menu == "Attendance":
        st.header("📅 Attendance Record")
        today = datetime.date.today()
        st.write(f"Aaj ki Date: {today}")
        if st.button("Mark My Attendance"):
            st.balloons()
            st.success("Aapki attendance record ho gayi hai!")

    elif menu == "Study Material":
        st.header("📑 Library & Notes")
        tab1, tab2 = st.tabs(["PDF Notes", "Video Lectures"])
        with tab1:
            st.button("Download: Chapter 1.pdf")
            st.button("Download: Syllabus.pdf")
        with tab2:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Yahan apna video link dalein

    elif menu == "Homework/Test":
        st.header("📝 Homework & Assignments")
        if st.session_state.role == "Teacher":
            st.text_area("Write Homework for Students")
            st.file_uploader("Upload Assignment Paper")
            st.button("Assign to Class")
        else:
            st.warning("No pending homework for today.")

    elif menu == "Settings":
        st.header("⚙️ App Settings")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()