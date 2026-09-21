import streamlit as st
import pandas as pd
from models import load_json, save_json
from utils import normalize_phone, sanitize_csv_field
from chatbot import get_bot_response
from github_store import sync_to_github

# --- 1. PREMIUM PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sir Abdullah Academy | Premier IT Education",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed" # Starts collapsed for cleaner home view
)

# --- 2. ADVANCED PROFESSIONAL STYLING (CSS) ---
# Midnight Navy, Crimson Accent, and Charcoal Palette
st.markdown("""
<style>
    /* Main App Background */
    .stApp { background-color: #0d1117; color: #e6edf3; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom Main Container Padding */
    .main .block-container { padding-top: 1rem; padding-bottom: 3rem; }

    /* Professional Header/Nav Sim */
    .academy-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid #30363d;
    }
    .logo-text { font-size: 1.8rem; font-weight: 700; color: #f0f6fc; }
    .contact-cta { background-color: transparent; border: 1px solid #4f46e5; color: #4f46e5; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-size: 0.9rem;}
    .contact-cta:hover { background-color: #4f46e5; color: white; }

    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 4rem 2rem;
        background: radial-gradient(circle, rgba(31,38,105,1) 0%, rgba(13,17,23,1) 100%);
        border-radius: 12px;
        margin-bottom: 3rem;
        border: 1px solid #1e293b;
    }
    .hero-title { font-size: 3.2rem; font-weight: 800; color: white; margin-bottom: 0.5rem; letter-spacing: -1px; }
    .hero-subtitle { font-size: 1.3rem; color: #94a3b8; max-width: 700px; margin: 0 auto 2rem auto; line-height: 1.6; }

    /* Feature/Highlight Cards */
    .highlight-card {
        background-color: #161b22;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #30363d;
        height: 100%;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .highlight-card:hover { transform: translateY(-3px); border-color: #4f46e5; }
    .icon-box { font-size: 2rem; color: #4f46e5; margin-bottom: 1rem; }
    .card-title { font-size: 1.25rem; font-weight: 600; color: #f0f6fc; margin-bottom: 0.5rem; }
    .card-text { font-size: 0.95rem; color: #8b949e; line-height: 1.5; }

    /* Course Cards */
    .course-card {
        background-color: #161b22;
        border-radius: 8px;
        border: 1px solid #30363d;
        margin-bottom: 1rem;
        overflow: hidden;
    }
    .course-header {
        background-color: #1f2937;
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #30363d;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .course-title { font-size: 1.3rem; font-weight: 700; color: white; margin: 0; }
    .course-price { font-size: 1.1rem; font-weight: 600; color: #10b981; }
    .course-body { padding: 1.5rem; }
    .course-meta { font-size: 0.85rem; color: #8b949e; margin-bottom: 1rem; display: flex; gap: 1rem;}

    /* Premium Buttons */
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: background-color 0.2s;
        width: 100%;
    }
    .stButton>button:hover { background-color: #4338ca; }
    .stButton>button:active { background-color: #3730a3; }

    /* Chat Styling */
    .stChatMessage { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; margin-bottom: 0.5rem; }
    .stChatInputContainer { background-color: #161b22 !important; border: 1px solid #30363d !important; border-radius: 8px !important; }

    /* Contact Sidebar styling */
    .contact-box { background-color: #161b22; padding: 1rem; border-radius: 8px; border: 1px solid #30363d; margin-top: 1rem;}
</style>
""", unsafe_allow_html=True)

# --- 3. HELPER DATA ( Hardcoded for premium homepage display) ---
HOMEPAGE_COURSES = [
    {
        "title": "Python for Beginners",
        "icon": "🐍",
        "desc": "Master the fundamentals of Python programming, the world's most popular language for AI, Data Science, and Web Development. Ideal for absolute beginners.",
        "duration": "8 Weeks",
        "level": "Beginner",
        "fee": "PKR 15,000"
    },
    {
        "title": "Full-Stack Web Development",
        "icon": "🌐",
        "desc": "Become a modern web developer. Learn HTML5, CSS3, JavaScript (ES6+), React.js, Node.js, and MongoDB. Build and deploy real-world applications.",
        "duration": "12 Weeks",
        "level": "Intermediate",
        "fee": "PKR 25,000"
    },
    {
        "title": "Data Science Fundamentals",
        "icon": "📊",
        "desc": "Learn to analyze data, extract insights, and build predictive models using Python, Pandas, NumPy, and Scikit-Learn. A structured path to AI.",
        "duration": "10 Weeks",
        "level": "Beginner-Friendly",
        "fee": "PKR 30,000"
    }
]

# --- 4. APPLICATION LOGIC ---
ADMIN_PASSWORD = "osmanibhai112233"

# - Professional Navigation Bar Sim -
st.markdown(f"""
<div class="academy-header">
    <div class="logo-text">Sir Abdullah Academy</div>
    <a href="https://wa.me/923321234567" class="contact-cta" target="_blank">Contact on WhatsApp</a>
</div>
""", unsafe_allow_html=True)

# - Sidebar (Simplified) -
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:white;'>Menu</h2>", unsafe_allow_html=True)
    menu = st.radio("Navigate", ["🏛️ Academy Home", "📝 Start Admission", "🤖 Chat Assistant", "🔒 Admin Panel"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""
    <div class="contact-box">
        <p style='color:white; font-weight:600; margin-bottom:0.2rem;'>Campus Location:</p>
        <p style='color:#8b949e; font-size:0.9rem; margin:0;'>Gulshan-e-Iqbal, Karachi, Pakistan</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. PAGE ROUTING ---

# --- PAGE A: ACADEMY HOME (The new premium landing page) ---
if menu == "🏛️ Academy Home":
    # 1. Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Premier IT Education in Karachi</div>
        <div class="hero-subtitle">Empowering the next generation of tech leaders with practical, industry-focused skills in programming, web development, and data science.</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Academy Highlights Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="highlight-card">
            <div class="icon-box">👨‍🏫</div>
            <div class="card-title">Expert Faculty</div>
            <div class="card-text">Learn from seasoned industry professionals with real-world experience.</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="highlight-card">
            <div class="icon-box">💻</div>
            <div class="card-title">Project-Based Learning</div>
            <div class="card-text">Build a portfolio of completed projects to showcase your skills.</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="highlight-card">
            <div class="icon-box">🏆</div>
            <div class="card-title">Career Support</div>
            <div class="card-text">Gain interview preparation and job placement assistance.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. Featured Courses Section
    st.markdown("<h2 style='text-align:center; color:white; margin-bottom:2rem;'>Explore Our Programs</h2>", unsafe_allow_html=True)

    # Display hardcoded courses professionally
    for course in HOMEPAGE_COURSES:
        with st.container():
            st.markdown(f"""
            <div class="course-card">
                <div class="course-header">
                    <h3 class="course-title">{course['icon']} {course['title']}</h3>
                    <span class="course-price">{course['fee']}</span>
                </div>
                <div class="course-body">
                    <div class="course-meta">
                        <span>⏱️ {course['duration']}</span>
                        <span>📈 {course['level']}</span>
                    </div>
                    <p class="course-text" style="color:#8b949e; margin-bottom:1rem;">{course['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 4. Final Call to Action
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<h3 style='text-align:center; color:white;'>Ready to kickstart your career?</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#8b949e; margin-bottom:1rem;'>Apply today or chat with our automated assistant for instant answers.</p>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Start Admission Form"):
                # Programmatically switch menu state
                st.session_state['menu_state'] = "📝 Start Admission"
                st.rerun() # Requires Streamlit >= 1.27
        with col_btn2:
             if st.button("Open Chat Assistant"):
                st.session_state['menu_state'] = "🤖 Chat Assistant"
                st.rerun()

    # Footer
    st.markdown("""
    <div style="text-align:center; padding-top:3rem; border-top: 1px solid #30363d; margin-top:2rem; color:#8b949e; font-size:0.85rem;">
        © 2024 Sir Abdullah Academy. All rights reserved. <br>
        Gulshan-e-Iqbal, Karachi | +92 332 1234567 | info@sirabdullah.edu.pk
    </div>
    """, unsafe_allow_html=True)

# --- PAGE B: ADMISSION FORM (Standard Form, Professional Styling) ---
elif menu == "📝 Start Admission":
    st.markdown("<h1 style='color:white; margin-bottom:2rem;'>📝 Admission Application</h1>", unsafe_allow_html=True)
    
    courses_data = load_json("courses.json", [])
    active_courses = [c["title"] for c in courses_data if c.get("active", True)]

    if not active_courses:
         st.warning("No courses are currently open for enrollment.")
    else:
        with st.form("admission_form"):
            st.markdown("<p style='color:#8b949e;'>Fill in your details accurately. Our team will contact you shortly after submission.</p>", unsafe_allow_html=True)
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                name = st.text_input("Full Name (as per CNIC/B-Form)*")
                email = st.text_input("Email Address (for correspondence)*")
            with col_f2:
                phone = st.text_input("WhatsApp/Phone Number (e.g. 03321234567)*")
                selected_course = st.selectbox("Select Your Desired Course*", active_courses)
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_sb1, col_sb2, col_sb3 = st.columns([1,1,1])
            with col_sb2:
                submitted = st.form_submit_button("Submit Application")

            if submitted:
                if not name or not phone or not email:
                    st.error("Please fill in all required fields (*) before submitting.")
                else:
                    norm_phone = normalize_phone(phone)
                    enrollments = load_json("enrollments.json", [])
                    new_entry = {
                        "name": sanitize_csv_field(name),
                        "email": sanitize_csv_field(email),
                        "phone": norm_phone,
                        "course": selected_course
                    }
                    enrollments.append(new_entry)
                    save_json("enrollments.json", enrollments)
                    sync_to_github("enrollments.json", enrollments)
                    st.success(f"Thank you {name}. Your application for '{selected_course}' has been submitted. Check your email for confirmation.")

# --- PAGE C: CHAT ASSISTANT (Dedicated Chat Interface) ---
elif menu == "🤖 Chat Assistant":
    st.markdown("<h1 style='color:white; margin-bottom:1rem;'>🤖 Academy Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8b949e; margin-bottom:2rem;'>Our automated bot can answer questions about admissions, fees, timings, and campus locations. Just type your query below.</p>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask about courses, fees, timings..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

# --- PAGE D: ADMIN PANEL (Requires Authentication) ---
elif menu == "🔒 Admin Panel":
    st.markdown("<h1 style='color:white; margin-bottom:2rem;'>🔒 Admin Dashboard</h1>", unsafe_allow_html=True)
    
    # Simple Authentication
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        st.markdown("<div style='background-color:#161b22; padding:2rem; border-radius:8px; border:1px solid #30363d; max-width:400px; margin:0 auto;'>", unsafe_allow_html=True)
        st.subheader("Authentication Required")
        pwd_input = st.text_input("Enter Admin Password", type="password")
        if st.button("Access Dashboard"):
            if pwd_input == ADMIN_PASSWORD:
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Invalid password. Access denied.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Display Admin Content if authenticated
    else:
        st.success("Authenticated Successfully")
        tab_log, tab_course = st.tabs(["Enrollment Logs", "Course Management"])
        
        with tab_log:
            st.subheader("Submitted Enrollments")
            enrollments = load_json("enrollments.json", [])
            if enrollments:
                df = pd.DataFrame(enrollments)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No enrollments have been submitted yet.")
                
        with tab_course:
            st.subheader("Manage Active Courses")
            courses_data = load_json("courses.json", [])
            st.json(courses_data)
            st.markdown("<p style='font-size:0.9rem; color:#8b949e;'>Edit 'courses.json' on GitHub to modify available courses.</p>", unsafe_allow_html=True)
        
        # Logout button
        if st.sidebar.button("Log Out"):
            st.session_state['authenticated'] = False
            st.rerun()
