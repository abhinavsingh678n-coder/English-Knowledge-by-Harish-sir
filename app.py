import streamlit as st

# 1. Page Config
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'current_live_link' not in st.session_state: st.session_state.current_live_link = ""
if 'role' not in st.session_state: st.session_state.role = "Student"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📖 English Knowledge</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>By Harish Sir</p>", unsafe_allow_html=True)
    st.divider()
    
    menu = st.radio("Student Menu", ["🏠 Dashboard", "🔴 Join Live Class", "🎥 Recorded Classes", "📂 My Notes"])
    
    st.write("---")
    with st.expander("👨‍🏫 Staff Login"):
        admin_pwd = st.text_input("Security Key", type="password")
        if admin_pwd == "harish_sir_pro":
            st.session_state.role = "Admin"
            st.success("Admin Mode Active!")

# --- ADMIN LOGIC ---
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Control Center")
    
    tab1, tab2 = st.tabs(["🚀 Start Live & Auto-Record", "📤 Homework Upload"])
    
    with tab1:
        st.subheader("Live Class Setup")
        st.info("Sir, YouTube Live shuru karke uska link yahan dalein. Wo apne aap Recorded mein save ho jayega.")
        with st.form("live_form"):
            v_title = st.text_input("Today's Topic Name", placeholder="e.g. Passive Voice Part 1")
            v_link = st.text_input("YouTube Live/Video Link")
            submit_live = st.form_submit_button("Start Class & Save")
            
            if submit_live and v_link:
                st.session_state.current_live_link = v_link
                # Auto-add to recorded list
                st.session_state.recorded_classes.append({"title": v_title, "link": v_link})
                st.success(f"Class shuru ho gayi aur Recorded mein add ho gayi!")

    with tab2:
        # (Homework upload code remains same as previous)
        st.subheader("Upload Notes")
        h_title = st.text_input("Notes Topic")
        h_file = st.file_uploader("Select File")
        if st.button("Upload"):
            if h_title and h_file:
                st.session_state.homework_list.append({"title": h_title, "file": h_file})
                st.success("Notes Bhej diye gaye!")

# --- STUDENT LOGIC ---
else:
    if menu == "🏠 Dashboard":
        st.title("English Knowledge by Harish Sir")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)

    elif menu == "🔴 Join Live Class":
        st.subheader("🔴 Current Live Session")
        if st.session_state.current_live_link:
            st.video(st.session_state.current_live_link)
            st.write("Sir abhi padha rahe hain...")
        else:
            st.warning("Abhi koi live class nahi chal rahi hai.")

    elif menu == "🎥 Recorded Classes":
        st.subheader("🎥 All Recorded Lectures")
        if not st.session_state.recorded_classes:
            st.info("No recorded classes yet.")
        for vid in reversed(st.session_state.recorded_classes): # Newest first
            with st.expander(f"▶️ {vid['title']}"):
                st.video(vid['link'])

    elif menu == "📂 My Notes":
        st.subheader("📚 Study Material")
        for item in st.session_state.homework_list:
            st.download_button(f"Download {item['title']}", data=item['file'])