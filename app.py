import streamlit as st

# 1. Page Config
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# Data Storage
if 'homework_list' not in st.session_state: st.session_state.homework_list = []
if 'recorded_classes' not in st.session_state: st.session_state.recorded_classes = []
if 'doubts' not in st.session_state: st.session_state.doubts = []
if 'role' not in st.session_state: st.session_state.role = "Student"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .error-text { color: red; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR BRANDING ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📖 English Knowledge</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>By Harish Sir</p>", unsafe_allow_html=True)
    st.divider()
    
    if st.session_state.logged_in or st.session_state.role == "Admin":
        menu = st.radio("Student Menu", ["🏠 Dashboard", "🔴 Join Live Class", "🎥 Recorded Classes", "📂 My Notes", "❓ Ask Doubt"])
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = "Student"
            st.rerun()
    
    st.write("---")
    with st.expander("👨‍🏫 Staff Login"):
        admin_pwd = st.text_input("Security Key", type="password")
        if admin_pwd == "harish_sir_pro":
            st.session_state.role = "Admin"
            st.success("Admin Mode Active!")

# --- LOGIN LOGIC (Mobile Number Check) ---
if not st.session_state.logged_in and st.session_state.role != "Admin":
    st.title("🎓 English Knowledge Login")
    with st.form("login_form"):
        u_name = st.text_input("Apna Naam")
        u_mobile = st.text_input("Mobile Number (10 Digits)")
        if st.form_submit_button("Enter Classroom"):
            if u_name and u_mobile.isdigit() and len(u_mobile) == 10:
                st.session_state.logged_in = True
                st.session_state.user_name = u_name
                st.session_state.user_id = u_mobile
                st.rerun()
            else:
                st.error("❌ Galat Number! Kripya 10 digits ka sahi mobile number dalein.")

# --- ADMIN PANEL LOGIC ---
elif st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Control Center")
    tab1, tab2, tab3 = st.tabs(["🚀 Classes", "📤 Homework", "❓ Doubt Panel"])
    
    with tab1:
        v_title = st.text_input("Topic Name")
        v_link = st.text_input("YouTube Link")
        if st.button("Add Class"):
            if v_title and v_link:
                st.session_state.recorded_classes.insert(0, {"title": v_title, "link": v_link})
                st.success("Class add ho gayi!")

    with tab2:
        h_title = st.text_input("Notes Title")
        h_file = st.file_uploader("Select File")
        if st.button("Upload"):
            if h_title and h_file:
                st.session_state.homework_list.insert(0, {"title": h_title, "file": h_file})
                st.success("Notes upload ho gaye!")

    with tab3:
        st.subheader("💬 Bachon ke Sawal")
        for i, d in enumerate(st.session_state.doubts):
            with st.expander(f"From: {d['user']} (ID: {d['id']})"):
                st.write(f"**Q:** {d['question']}")
                if d['answer']: st.info(f"Answer: {d['answer']}")
                else:
                    ans = st.text_area("Reply", key=f"ans_{i}")
                    if st.button("Send", key=f"btn_{i}"):
                        st.session_state.doubts[i]['answer'] = ans
                        st.rerun()

# --- STUDENT PAGES ---
else:
    if menu == "🏠 Dashboard":
        st.title(f"Welcome, {st.session_state.user_name}!")
        st.image("https://img.freepik.com/free-vector/online-education-concept_52683-37453.jpg", use_container_width=True)

    elif menu == "❓ Ask Doubt":
        st.header("❓ Puchein Apna Sawal")
        with st.form("s_doubt", clear_on_submit=True):
            q = st.text_area("Sawal Likhein")
            if st.form_submit_button("Sir ko Bhejein"):
                # Double Check: Only if ID is valid (which is already checked at login)
                if q:
                    st.session_state.doubts.append({
                        "user": st.session_state.user_name, 
                        "id": st.session_state.user_id, 
                        "question": q, 
                        "answer": None
                    })
                    st.success("Doubt bhej diya gaya!")
        
        st.divider()
        for d in reversed(st.session_state.doubts):
            if d['id'] == st.session_state.user_id:
                st.write(f"❓ **Q:** {d['question']}")
                if d['answer']: st.info(f"✅ **Ans:** {d['answer']}")
                else: st.warning("⏳ Pending...")
                st.write("---")