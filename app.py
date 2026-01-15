import streamlit as st

# 1. Page Config
st.set_page_config(page_title="English Knowledge - Free Batch", layout="wide", page_icon="📖")

# 2. Custom CSS for PW Blue Theme & Professional Look
st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    header {visibility: hidden;}
    
    /* Profile Section */
    .profile-box {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        margin-bottom: 20px;
    }
    
    /* Batch Card Styling */
    .free-batch-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        overflow: hidden;
        border: 1px solid #e0e0e0;
        margin-bottom: 25px;
    }
    .batch-header {
        background: linear-gradient(135deg, #0052D4, #4364F7, #6FB1FC);
        color: white;
        padding: 20px;
        text-align: center;
        font-weight: bold;
    }
    .batch-tag {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 2px 8px;
        border-radius: 5px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initializing Session State ---
if 'user_name' not in st.session_state: st.session_state.user_name = "Abhinav" # Default for testing

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown(f"### 👋 Hello, {st.session_state.user_name}")
    st.write("Student ID: #EK2026")
    st.write("---")
    menu = st.radio("Navigation", ["🏠 Dashboard", "📂 My Free Batches", "🎥 Live Library", "📑 Homework/Notes", "👨‍🏫 Admin"])
    st.write("---")
    st.success("App for Harish Sir's Students")

# --- DASHBOARD ---
if menu == "🏠 Dashboard":
    st.markdown("<h2 style='color: #1a73e8;'>My Learning Dashboard</h2>", unsafe_allow_html=True)
    
    # Hero Banner
    st.image("https://img.freepik.com/free-vector/students-watching-webinar-computer-screen-online-education-concept_74855-10584.jpg", use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="free-batch-card">
                <div class="batch-header">UP Board Special (English)</div>
                <div style="padding: 15px;">
                    <span class="batch-tag">FREE BATCH</span>
                    <h4>Class 10th & 12th</h4>
                    <p>Complete Grammar Coverage</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Start Learning Now", key="btn1"):
            st.info("Directing to Class 10th-12th Section...")

    with col2:
        st.markdown("""
            <div class="free-batch-card">
                <div class="batch-header" style="background: linear-gradient(135deg, #FF512F, #DD2476);">Spoken English Master</div>
                <div style="padding: 15px;">
                    <span class="batch-tag">FREE BATCH</span>
                    <h4>Speaking & Vocabulary</h4>
                    <p>Learn to speak in 60 Days</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Join Spoken Class", key="btn2"):
            st.info("Directing to Spoken Section...")

# --- MY BATCHES (Classroom View) ---
elif menu == "📂 My Free Batches":
    st.title("📚 Classroom")
    tab1, tab2 = st.tabs(["📺 Lectures", "📖 Study Material"])
    
    with tab1:
        st.subheader("Latest Video Classes")
        # Harish sir yahan apne YouTube video ka link dal sakte hain
        st.video("https://www.youtube.com/watch?v=Xp0N1f8w6bU") # Example video
        st.markdown("**Topic:** Introduction to Passive Voice")
        
    with tab2:
        st.subheader("Handwritten Notes")
        st.info("Harish Sir's special PDF notes will appear here.")
        st.button("📄 Download Tenses Chart (PDF)")

# --- ADMIN PANEL ---
elif menu == "👨‍🏫 Admin":
    st.subheader("Harish Sir's Login")
    pwd = st.text_input("Security Key", type="password")
    if pwd == "harish_sir_pro":
        st.success("Access Granted!")
        st.write("Yahan se aap naye videos aur PDF bacho ke liye free mein add kar sakte hain.")