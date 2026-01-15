import streamlit as st

# 1. Page Config (Mobile friendly)
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide", page_icon="🎓")

# 2. PW Style CSS for Dashboard
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    header {visibility: hidden;}
    
    /* Top Banner / Hero Section */
    .hero-section {
        background: linear-gradient(90deg, #1a2a6c, #b21f1f, #fdbb2d);
        padding: 40px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* Batch Card (PW Style) */
    .batch-card {
        background-color: white;
        padding: 0px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        overflow: hidden;
        margin-bottom: 20px;
        border: 1px solid #eee;
    }
    .batch-image {
        width: 100%;
        height: 150px;
        background-color: #008080;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
    }
    .batch-details { padding: 15px; }
    
    /* Bottom Navigation for Mobile Look */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Navigation) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🎓 Selection Way</h2>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("Go to", ["🏠 Home", "📚 My Batches", "🔴 Live Classes", "📖 Free Resources", "👨‍🏫 Teacher Panel"])
    st.write("---")
    st.info("Study hard, Abhinav!")

# --- HOME PAGE ---
if menu == "🏠 Home":
    st.markdown("""
        <div class="hero-section">
            <h1>English Knowledge by Harish Sir</h1>
            <p>Ab Selection Hoga Pakka! 🚀</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🔥 Popular Batches")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="batch-card">
                <div class="batch-image">SSC English 2026</div>
                <div class="batch-details">
                    <h4>Target SSC CGL/CHSL</h4>
                    <p>Complete Grammar + Vocab</p>
                    <p style='color: green;'><b>Enroll Now</b></p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Batch", key="b1"): pass
        
    with col2:
        st.markdown("""
            <div class="batch-card">
                <div class="batch-image" style='background-color: #1a2a6c;'>Spoken English Pro</div>
                <div class="batch-details">
                    <h4>Zero to Hero Spoken</h4>
                    <p>Daily Live Practice Sessions</p>
                    <p style='color: green;'><b>Enroll Now</b></p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Batch", key="b2"): pass

# --- MY BATCHES (Proper Class View) ---
elif menu == "📚 My Batches":
    st.title("My Enrolled Batches")
    tab1, tab2, tab3 = st.tabs(["Lecures", "Notes", "Test Series"])
    
    with tab1:
        st.write("### Today's Lectures")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Dummy link
        st.markdown("---")
        st.write("### Previous Lectures")
        st.button("Lesson 1: Introduction to Tenses")
        st.button("Lesson 2: Present Indefinite")

    with tab2:
        st.write("### Download PDF Notes")
        st.download_button("Download Tense Chart", "PDF Data", "tenses.pdf")

# --- LIVE CLASSES ---
elif menu == "🔴 Live Classes":
    st.title("Ongoing Live Classes")
    st.error("No Live Class at this moment. Next class at 8:00 PM.")
    if st.button("Enter Live Room"):
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=https://meet.jit.si/EnglishKnowledge_Harish">', unsafe_allow_html=True)

# --- TEACHER PANEL ---
elif menu == "👨‍🏫 Teacher Panel":
    pwd = st.text_input("Admin Password", type="password")
    if pwd == "harish_sir_pro":
        st.success("Welcome Harish Sir!")
        # Sir yahan se video link aur PDF upload kar sakte hain