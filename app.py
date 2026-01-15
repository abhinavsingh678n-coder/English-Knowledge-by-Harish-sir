import streamlit as st

# 1. Page Config
st.set_page_config(page_title="English Knowledge by Harish Sir", layout="wide")

# Session State Initialization
if 'role' not in st.session_state: st.session_state.role = "Student" # Default Role

# --- SIDEBAR (Clean & Simple for Students) ---
with st.sidebar:
    st.title("Selection Way 🎓")
    st.write(f"Welcome, {st.session_state.get('user_name', 'Student')}!")
    st.divider()
    
    # Ye options sabko dikhenge (Bacho ke liye)
    menu = st.radio("Menu", ["🏠 Home", "🔴 Live Class", "🎥 Recorded Classes", "📂 My Notes"])
    
    st.write("---")
    # Secret Admin Entry (Sir ke liye)
    with st.expander("👨‍🏫 Staff Only"):
        admin_pwd = st.text_input("Admin Key", type="password")
        if admin_pwd == "harish_sir_pro":
            st.session_state.role = "Admin"
            st.success("Admin Mode Active!")
        else:
            st.session_state.role = "Student"

# --- LOGIC ACCORDING TO ROLE ---

# Agar Role Admin hai toh Sir ko Control dikhao
if st.session_state.role == "Admin":
    st.header("👨‍🏫 Harish Sir's Control Center")
    st.info("Sir, yahan se aap Homework aur Videos upload kar sakte hain.")
    # Uploading logic yahan aayega...

# Padhai wala content (Bacho ke liye)
else:
    if menu == "🏠 Home":
        st.title("Welcome to Class!")
        st.image("https://img.freepik.com/free-vector/digital-learning-abstract-concept-vector-illustration_335657-2417.jpg", width=400)
    
    elif menu == "🔴 Live Class":
        st.subheader("Live Class Section")
        st.write("Sir abhi live nahi hain. Timing: 8:00 PM")
        
    elif menu == "🎥 Recorded Classes":
        st.subheader("Purani Classes")
        # Video list...