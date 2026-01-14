import streamlit as st

# Password Settings
ADMIN_PASSWORD = "harish_sir_pro" # Aap ise badal sakte hain

st.set_page_config(page_title="Selection Way Pro", layout="centered")

# CSS for PW Look
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #1a73e8; color: white; font-weight: bold;}
    .card { padding: 20px; border-radius: 15px; background-color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px; color: black; border-left: 5px solid #1a73e8;}
    </style>
    """, unsafe_allow_html=True)

if 'user_type' not in st.session_state:
    st.session_state.user_type = None

# --- LOGIN PAGE ---
if st.session_state.user_type is None:
    st.markdown("<h1 style='text-align: center;'>🎓 Selection Way</h1>", unsafe_allow_html=True)
    st.write("Apna role chunein aur padhai shuru karein:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👨‍🏫 Teacher Login"):
            st.session_state.user_type = 'Teacher'
            st.rerun()
    with col2:
        if st.button("👨‍🎓 Student Login"):
            st.session_state.user_type = 'Student'
            st.rerun()

# --- TEACHER DASHBOARD (With Password) ---
elif st.session_state.user_type == 'Teacher':
    st.title("👨‍🏫 Teacher Admin Panel")
    pwd = st.text_input("Admin Password Dalein", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.success("Welcome Harish Sir!")
        tab1, tab2 = st.tabs(["🎥 Live Class", "📂 Upload Notes"])
        
        with tab1:
            st.subheader("Live Class Control")
            if st.button("🚀 START LIVE CLASS NOW"):
                st.markdown(f'<meta http-equiv="refresh" content="0;URL=https://meet.jit.si/SelectionWay_HarishSir_Live">', unsafe_allow_html=True)

        with tab2:
            st.subheader("Upload Study Material")
            uploaded_file = st.file_uploader("PDF ya Image select karein", type=['pdf', 'png', 'jpg'])
            note_title = st.text_input("Title (e.g. Noun Notes)")
            if st.button("✅ Publish to Students"):
                st.success("Notes bacho ke portal par upload ho gaye!")
    
    if st.button("🔙 Back to Home"):
        st.session_state.user_type = None
        st.rerun()

# --- STUDENT DASHBOARD ---
elif st.session_state.user_type == 'Student':
    st.title("👨‍🎓 Student Dashboard")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔴 Live Class")
    st.write("Join Harish Sir's live session.")
    if st.button("JOIN NOW"):
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=https://meet.jit.si/SelectionWay_HarishSir_Live">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("📂 My Study Notes")
    st.info("Sir dwara upload kiye gaye notes yahan dikhenge.")

    if st.button("🔙 Back to Home"):
        st.session_state.user_type = None
        st.rerun()