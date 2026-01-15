import streamlit as st

# 1. Page Config
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'role' not in st.session_state: st.session_state.role = "Student"

# --- SIDEBAR BRANDING ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📖 English Knowledge</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>By Harish Sir</p>", unsafe_allow_html=True)
    st.divider()
    
    menu = st.radio("Student Menu", ["🏠 Dashboard", "🔴 Join Live Class", "🎥 Recorded Classes", "📂 My Notes", "❓ Ask Doubt"])
    
    st.write("---")
    with st.expander("👨‍🏫 Staff Login"):
        admin_pwd = st.text_input("Security Key", type="password")
        if admin_pwd == "harish_sir_pro":
            st.session_state.role = "Admin"
            st.success("Admin Mode Active!")
        else:
            st.session_state.role = "Student"

# --- ADMIN PANEL LOGIC ---
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Control Center")
    tab1, tab2, tab3 = st.tabs(["🚀 Classes", "📤 Homework", "❓ Doubt Panel"])
    
    with tab1:
        st.subheader("Add Live/Recorded Class")
        with st.form("class_form", clear_on_submit=True):
            v_title = st.text_input("Topic Name")
            v_link = st.text_input("YouTube Link")
            if st.form_submit_button("Add to App"):
                if v_title and v_link:
                    st.session_state.recorded_classes.insert(0, {"title": v_title, "link": v_link})
                    st.success("Class add ho gayi!")

    with tab2:
        st.subheader("Upload Notes")
        with st.form("hw_form", clear_on_submit=True):
            h_title = st.text_input("Notes Title")
            h_file = st.file_uploader("Select PDF/Image")
            if st.form_submit_button("Upload Now"):
                if h_title and h_file:
                    st.session_state.homework_list.insert(0, {"title": h_title, "file": h_file})
                    st.success("Notes upload ho gaye!")

    with tab3:
        st.subheader("💬 Bachon ke Doubts (With ID)")
        if not st.session_state.doubts:
            st.info("Abhi koi doubt nahi aaya hai.")
        else:
            for i, d in enumerate(st.session_state.doubts):
                with st.container():
                    st.write(f"**From:** {d['user']} (ID: {d['id']})")
                    st.write(f"**Q:** {d['question']}")
                    if d['answer']:
                        st.info(f"✅ Your Answer: {d['answer']}")
                    else:
                        reply = st.text_area("Answer Likhein", key=f"ans_{i}")
                        if st.button("Reply", key=f"btn_{i}"):
                            st.session_state.doubts[i]['answer'] = reply
                            st.rerun()

# --- STUDENT PAGES ---
else:
    if menu == "🏠 Dashboard":
        st.title("English Knowledge by Harish Sir")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)

    elif menu == "🔴 Join Live Class":
        st.subheader("🔴 Live Classroom")
        st.info("Sir Live aayenge toh yahan video dikhegi.")
        # Dummy live stream viewer
        st.write("Checking for Live Stream...")

    elif menu == "🎥 Recorded Classes":
        st.subheader("🎥 All Classes")
        for vid in st.session_state.recorded_classes:
            with st.expander(f"▶️ {vid['title']}"):
                st.video(vid['link'])

    elif menu == "📂 My Notes":
        st.subheader("📚 Study Material")
        for item in st.session_state.homework_list:
            st.download_button(f"Download {item['title']}", data=item['file'])

    elif menu == "❓ Ask Doubt":
        st.header("❓ Puchein Apna Sawal")
        with st.form("s_doubt", clear_on_submit=True):
            name = st.text_input("Apna Naam")
            s_id = st.text_input("Apna Mobile (ID)")
            q = st.text_area("Sawal Likhein")
            if st.form_submit_button("Sir ko Bhejein"):
                if name and s_id and q:
                    st.session_state.doubts.append({"user": name, "id": s_id, "question": q, "answer": None})
                    st.success("Sawal bhej diya gaya!")