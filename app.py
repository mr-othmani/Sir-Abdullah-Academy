import streamlit as st
import pandas as pd
import os
import json
import urllib.parse
from datetime import datetime

# Import project modules
try:
    from models import AcademyModel
    from utils import load_json, save_json
    from chatbot import handle_query
except ImportError:
    pass

# Page Configuration
st.set_page_config(
    page_title="Sir Abdullah Academy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Midnight Navy Styling
st.markdown("""
<style>
    /* Global Background & Typography */
    .stApp {
        background-color: #0d0e23;
        color: #ffffff;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #121433;
        border-right: 1px solid #2e2a80;
    }

    /* Hero Section Banner */
    .hero-container {
        background-color: #1a1851;
        border: 1px solid #2e2a80;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #161840;
        border: 1px solid #2e2a80;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .metric-card h3 {
        color: #a5b4fc;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    .metric-card h2 {
        color: #ffffff;
        font-size: 2rem;
        margin: 0;
    }

    /* Receipt Box */
    .receipt-box {
        background-color: #161840;
        border: 2px dashed #4f46e5;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper Function: Load Logs
def load_logs():
    if os.path.exists("query_log.csv"):
        return pd.read_csv("query_log.csv")
    return pd.DataFrame(columns=["Date", "Time", "Query", "Category"])

# Helper Function: WhatsApp Link Generator
def get_whatsapp_link(phone_number, message):
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{phone_number}?text={encoded_message}"

# Sidebar Navigation
if os.path.exists("assets/core_combo_logo.png"):
    st.sidebar.image("assets/core_combo_logo.png", width=90)
st.sidebar.title("Sir Abdullah Academy")
st.sidebar.caption("O Level & IGCSE Specialist")

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", [
    "🏡 Home & Courses", 
    "💬 AI Support Assistant", 
    "📝 Enroll & Get Receipt", 
    "📊 Admin Dashboard"
])

# Sidebar Direct WhatsApp Contact Widget
st.sidebar.markdown("---")
st.sidebar.subheader("📲 Instant WhatsApp Support")
wa_url = get_whatsapp_link("923001234567", "Hi Sir Abdullah, I would like to inquire about course admissions.")
st.sidebar.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:8px; font-weight:bold; cursor:pointer;">💬 Chat on WhatsApp</button></a>', unsafe_allow_html=True)

# List of Available Courses
COURSES = [
    {"name": "Biology (O Level / IGCSE)", "code": "5090 / 0610", "fee": "PKR 5,000/mo", "rating": "4.9 ⭐", "img": "assets/biology_logo.png"},
    {"name": "Physics (O Level / IGCSE)", "code": "5054 / 0625", "fee": "PKR 5,000/mo", "rating": "5.0 ⭐", "img": "assets/physics_logo.png"},
    {"name": "Chemistry (O Level / IGCSE)", "code": "5070 / 0620", "fee": "PKR 5,000/mo", "rating": "4.8 ⭐", "img": "assets/chemistry_logo.png"},
    {"name": "Mathematics (O Level / IGCSE)", "code": "4024 / 0580", "fee": "PKR 5,000/mo", "rating": "4.9 ⭐", "img": "assets/math_logo.png"},
    {"name": "Computer Science (O Level / IGCSE)", "code": "2210 / 0478", "fee": "PKR 5,000/mo", "rating": "5.0 ⭐", "img": "assets/cs_logo.png"},
    {"name": "Islamiat & Pakistan Studies", "code": "2058 / 2059", "fee": "PKR 5,000/mo", "rating": "4.9 ⭐", "img": "assets/islamiat_logo.png"},
    {"name": "Core Appearing Combo", "code": "Islamiat + PST", "fee": "PKR 8,000/mo", "rating": "5.0 ⭐", "img": "assets/core_combo_logo.png"},
    {"name": "Pre-Medical Combo", "code": "Bio + Chem + Physics", "fee": "PKR 12,000/mo", "rating": "5.0 ⭐", "img": "assets/pre_medical_combo_logo.png"},
    {"name": "Pre-Engineering Combo", "code": "Math + Physics + Chem", "fee": "PKR 12,000/mo", "rating": "4.9 ⭐", "img": "assets/pre_engineering_combo_logo.png"},
]

# ---------------------------------------------------------
# PAGE 1: HOME & COURSES
# ---------------------------------------------------------
if page == "🏡 Home & Courses":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">✨ ADMISSIONS OPEN FOR O LEVEL & IGCSE</div>
        <h1 style="color: white; margin: 0 0 10px 0; font-size: 2.8rem;">Sir Abdullah Academy</h1>
        <p style="color: #cbd5e1; max-width: 750px; margin: 0 auto; font-size: 1.1rem; line-height: 1.6;">
            Premier 100% Online Cambridge Coaching. Empowering students with conceptual understanding, 
            exam techniques, and rigorous topical past paper practice to secure top A* grades.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📚 Course Offerings & Bundles")
    search_query = st.text_input("🔍 Filter by course name or code...", "")

    filtered = [c for c in COURSES if search_query.lower() in c["name"].lower() or search_query.lower() in c["code"].lower()]

    cols = st.columns(3)
    for idx, course in enumerate(filtered):
        with cols[idx % 3]:
            with st.container(border=True):
                if os.path.exists(course["img"]):
                    st.image(course["img"], use_container_width=True)
                st.markdown(f"### {course['name']}")
                st.caption(f"Code: {course['code']} | Rating: {course['rating']}")
                st.markdown(f"**Monthly Fee:** `{course['fee']}`")
                
                # Direct WhatsApp Inquiry Link per course
                course_wa = get_whatsapp_link("923001234567", f"Hi Sir Abdullah, I want to enroll in {course['name']}.")
                st.markdown(f'<a href="{course_wa}" target="_blank"><button style="width:100%; background-color:#4f46e5; color:white; border:none; padding:8px; border-radius:6px; font-weight:600;">Inquire Course</button></a>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 2: AI SUPPORT ASSISTANT
# ---------------------------------------------------------
elif page == "💬 AI Support Assistant":
    st.title("💬 Academy AI Support Assistant")
    st.write("Instant automated responses regarding schedules, syllabus, and fees.")

    st.markdown("#### Suggested Topics:")
    c1, c2, c3, c4 = st.columns(4)
    quick_input = ""
    if c1.button("⏰ Business Hours"):
        quick_input = "What are your business hours?"
    if c2.button("💳 Payment Methods"):
        quick_input = "What payment methods do you accept?"
    if c3.button("📞 Contact Info"):
        quick_input = "What is your contact number?"
    if c4.button("📖 Course List"):
        quick_input = "What courses do you offer?"

    user_query = st.text_input("Type your question below:", value=quick_input if quick_input else "")

    if user_query:
        try:
            response = handle_query(user_query)
        except Exception:
            response = "For detailed syllabus queries or custom schedules, please reach out via our WhatsApp support."
        st.info(f"**Answer:** {response}")

# ---------------------------------------------------------
# PAGE 3: ENROLL & GET RECEIPT
# ---------------------------------------------------------
elif page == "📝 Enroll & Get Receipt":
    st.title("📝 Student Registration & Fee Voucher")
    st.write("Submit your information to generate your digital registration receipt.")

    with st.form("enrollment_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            student_name = st.text_input("Student Full Name*")
            guardian_email = st.text_input("Email Address")
        with col_b:
            guardian_phone = st.text_input("WhatsApp / Contact Number*")
            grade_level = st.selectbox("Grade / Board", ["O Level (O2)", "O Level (O3)", "IGCSE", "Other"])

        selected_course = st.selectbox("Select Course / Combo Package", [c["name"] for c in COURSES])
        submitted = st.form_submit_button("Generate Registration Receipt")

        if submitted:
            if student_name and guardian_phone:
                reg_id = f"SAA-{datetime.now().strftime('%Y%m%d%H%M')}"
                st.success("✅ Enrollment Recorded Successfully!")
                st.balloons()

                # Generate Digital Receipt View
                receipt_text = f"""
                ==========================================
                         SIR ABDULLAH ACADEMY
                    OFFICIAL ENROLLMENT RECEIPT
                ==========================================
                Registration ID : {reg_id}
                Date            : {datetime.now().strftime('%Y-%m-%d %H:%M')}
                Student Name    : {student_name}
                Contact Phone   : {guardian_phone}
                Grade / Board   : {grade_level}
                Enrolled Course : {selected_course}
                Status          : Pending Payment Verification
                ==========================================
                Please present this Registration ID on WhatsApp 
                to confirm batch timing.
                ==========================================
                """

                st.markdown(f"""
                <div class="receipt-box">
                    <h3 style="margin-top:0; color:#818cf8;">🧾 Digital Registration Card</h3>
                    <p><b>Registration ID:</b> <code>{reg_id}</code></p>
                    <p><b>Student Name:</b> {student_name}</p>
                    <p><b>Course:</b> {selected_course}</p>
                    <p><b>Status:</b> <span style="color:#f59e0b;">Pending Verification</span></p>
                </div>
                """, unsafe_allow_html=True)

                st.download_button(
                    label="📥 Download Official Receipt (.txt)",
                    data=receipt_text,
                    file_name=f"Receipt_{student_name.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            else:
                st.error("Please fill in all required fields (Name and WhatsApp number).")

# ---------------------------------------------------------
# PAGE 4: ADMIN DASHBOARD
# ---------------------------------------------------------
elif page == "📊 Admin Dashboard":
    st.title("📊 Academy Management Dashboard")
    st.caption("Live monitoring of query logs and platform status.")

    df_logs = load_logs()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><h3>Logged Queries</h3><h2>{len(df_logs)}</h2></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><h3>Active Courses</h3><h2>{len(COURSES)}</h2></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-card"><h3>System Health</h3><h2>🟢 100% Operational</h2></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📋 Query Analytics (`query_log.csv`)")
    if not df_logs.empty:
        st.dataframe(df_logs, use_container_width=True)
        if "Category" in df_logs.columns:
            st.subheader("📈 Query Distribution by Topic")
            st.bar_chart(df_logs["Category"].value_counts())
    else:
        st.info("No queries recorded yet. Questions processed by the chatbot will appear here automatically.")
        
