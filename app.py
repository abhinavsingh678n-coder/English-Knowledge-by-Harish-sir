 import streamlit as st

# Admin Settings
ADMIN_PASSWORD = "harish_sir_pro"

st.set_page_config(page_title="Selection Way Pro", layout="centered")

# Professional UI CSS
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #1a73e8; color: white; font-weight: bold;}
    .login-box { padding: 30px; border-radius: 20px; background-color: white; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center; }
    </style>
    """, unsafe_allow_html=True)

if 'login_state' not in st.session_state:
    st.session_state.login_state = "selection"
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# --- 1. SELECTION PAGE ---
if st.session_state.login_state == "selection":
    st.markdown("<h1 style='text-align: center;'>🎓 Selection Way</h1>", unsafe_allow_html=True)
    st.write("Welcome! Please choose your role:")
    if st.button("👨‍🏫 Teacher Login"):
        st.session_state.login_state = "teacher_login"
        st.rerun()
    if st.button("👨‍🎓 Student Login"):
        st.session_state.login_state = "student_login"
        st.rerun()

# --- 2. TEACHER LOGIN (Password Protected) ---
elif st.session_state.login_state == "teacher_login":
    st.subheader("Teacher Admin Access")
    pwd = st.text_input("Admin Password Dalein", type="password")
    if st.button("Login as Admin"):
        if pwd == ADMIN_PASSWORD:
            st.session_state.login_state = "teacher_dashboard"
            st.rerun()
        else:
            st.error("Wrong Password!")
    if st.button("🔙 Back"):
        st.session_state.login_state = "selection"
        st.rerun()

# --- 3. STUDENT LOGIN (Mobile Number System) ---
elif st.session_state.login_state == "student_login":
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.subheader("Student Login")
    mobile = st.text_input("📞 Apna Mobile Number Dalein", placeholder="9876543210")
    name = st.text_input("👤 Apna Naam Dalein", placeholder="Full Name")
    
    if st.button("START LEARNING NOW 🚀"):
        if len(mobile) == 10 and name:
            st.session_state.user_name = name
            st.session_state.login_state = "student_dashboard"
            st.rerun()
        else:
            st.warning("Please enter a valid 10-digit number and your name.")
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("🔙 Back"):
        st.session_state.login_state = "selection"
        st.rerun()

# --- 4. TEACHER DASHBOARD ---
elif st.session_state.login_state == "teacher_dashboard":
    st.title("👨‍🏫 Harish Sir's Panel")
    if st.button("🚀 START LIVE CLASS"):
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=https://meet.jit.si/SelectionWay_Harish_Live">', unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.login_state = "selection"
        st.rerun()

# --- 5. STUDENT DASHBOARD ---
elif st.session_state.login_state == "student_dashboard":
    st.title(f"👋 Welcome, {st.session_state.user_name}!")
    st.info("Aap Selection Way Academy se jud chuke hain.")
    if st.button("🔴 Join Live Class"):
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=https://meet.jit.si/SelectionWay_Harish_Live">', unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.login_state = "selection"
        st.rerun()