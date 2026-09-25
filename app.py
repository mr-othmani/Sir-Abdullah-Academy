import streamlit as st
import pandas as pd
import os
from chatbot import handle_query
from models import AcademyModel

# Page configuration
st.set_page_config(
    page_title="Sir Abdullah Academy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark-mode styling and legibility
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0b0c10;
        color: #c5c6c7;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1f2833;
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Custom Hero Header */
    .hero-banner {
        background: linear-gradient(135deg, #1f2833 0%, #0b0c10 100%);
        border: 1px solid #45a29e;
        padding: 2.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero-title {
        color: #66fcf1;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #c5c6c7;
        font-size: 1.1rem;
    }

    /* Course Cards */
    .course-card {
        background-color: #1f2833;
        border: 1px solid #45a29e;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #45a29e;
        color: #0b0c10;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #66fcf1;
        color: #0b0c10;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Header & Navigation
with st.sidebar:
    if os.path.exists("assets/core_combo_logo.png"):
        st.image("assets/core_combo_logo.png", width=100)
    st.title("Sir Abdullah Academy")
    st.caption("O Level & IGCSE Specialist")
    st.markdown("---")
    
    page = st.radio("Navigation", ["Home", "AI Assistant", "Enrollment", "Admin Dashboard"])

# PAGE 1: HOME
if page == "Home":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Sir Abdullah Academy</div>
        <div class="hero-subtitle">
            Premier 100% Online Cambridge Coaching. Empowering students with conceptual understanding, 
            exam techniques, and topical past paper practice to secure top A* grades.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📚 Offered Courses")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="course-card">', unsafe_allow_html=True)
        if os.path.exists("assets/biology_logo.png"):
            st.image("assets/biology_logo.png", use_container_width=True)
        st.markdown("### O Level Biology")
        st.write("Subject Code: 5090 / 0610")
        st.write("**Fee:** PKR 5,000/month")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="course-card">', unsafe_allow_html=True)
        if os.path.exists("assets/physics_logo.png"):
            st.image("assets/physics_logo.png", use_container_width=True)
        st.markdown("### O Level Physics")
        st.write("Subject Code: 5054 / 0625")
        st.write("**Fee:** PKR 5,000/month")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="course-card">', unsafe_allow_html=True)
        if os.path.exists("assets/chemistry_logo.png"):
            st.image("assets/chemistry_logo.png", use_container_width=True)
        st.markdown("### O Level Chemistry")
        st.write("Subject Code: 5070 / 0620")
        st.write("**Fee:** PKR 5,000/month")
        st.markdown('</div>', unsafe_allow_html=True)

# PAGE 2: AI ASSISTANT
elif page == "AI Assistant":
    st.title("💬 Academy AI Assistant")
    st.write("Ask any question regarding admissions, subject offerings, fees, or class schedules.")
    
    user_query = st.text_input("Enter your query:")
    if st.button("Submit") and user_query:
        response = handle_query(user_query)
        st.info(f"**Bot:** {response}")

# PAGE 3: ENROLLMENT
elif page == "Enrollment":
    st.title("📝 Student Enrollment")
    
    with st.form("enrollment_form"):
        name = st.text_input("Student Name")
        phone = st.text_input("WhatsApp Number")
        course = st.selectbox("Select Subject", ["Biology", "Physics", "Chemistry", "Mathematics", "Computer Science"])
        submit = st.form_submit_button("Submit Enrollment")
        
        if submit:
            if name and phone:
                st.success(f"Enrollment request submitted for {name} ({course}). Contacting you shortly via WhatsApp!")
            else:
                st.error("Please fill in all required fields.")

# PAGE 4: ADMIN DASHBOARD
elif page == "Admin Dashboard":
    st.title("📊 Admin Query Log")
    
    if os.path.exists("query_log.csv"):
        df = pd.read_csv("query_log.csv")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No query log data found yet.")
