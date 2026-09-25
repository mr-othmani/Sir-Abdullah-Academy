import streamlit as st
import pandas as pd
import os
import json
import urllib.parse
from datetime import datetime

# Import modular project files
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

# Helper Functions
def load_logs():
    if os.path.exists("query_log.csv"):
        return pd.read_csv("query_log.csv")
    return pd.DataFrame(columns=["Date", "Time", "Query", "Category"])

def get_whatsapp_link(phone_number, message):
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{phone_number}?text={encoded_message}"

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    if os.path.exists("assets/core_combo_logo.png"):
        st.image("assets/core_combo_logo.png", width=80)
    
    st.title("Sir Abdullah Academy")
    st.caption("O Level & IGCSE Specialist")
    st.divider()

    page = st.radio("Navigation", [
        "🏡 Home & Courses", 
        "💬 AI Support Assistant", 
        "📝 Enroll & Get Receipt", 
        "📊 Admin Dashboard"
    ])

    st.divider()
    st.caption("Instant WhatsApp Support")
    wa_url = get_whatsapp_link("923001234567", "Hi Sir Abdullah, I want to inquire about course admissions.")
    st.link_button("💬 Chat on WhatsApp", wa_url, use_container_width=True, type="primary")

# ---------------------------------------------------------
# COURSE DATASET
# ---------------------------------------------------------
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
    # Clean Hero Container
    with st.container(border=True):
        st.badge("✨ ADMISSIONS OPEN FOR O LEVEL & IGCSE")
        st.title("Sir Abdullah Academy")
        st.markdown(
            "Premier 100% Online Cambridge Coaching. Empowering students with conceptual understanding, "
            "exam techniques, and rigorous topical past paper practice to secure top A* grades."
        )

    st.write("")
    st.subheader("📚 Available Courses & Bundles")
    
    # Native Search Input
    search_query = st.text_input("Search Courses", placeholder="Type subject or code e.g. Physics, 5054...")

    filtered = [c for c in COURSES if search_query.lower() in c["name"].lower() or search_query.lower() in c["code"].lower()]

    # Course Grid Layout
    cols = st.columns(3)
    for idx, course in enumerate(filtered):
        with cols[idx % 3]:
            with st.container(border=True):
                if os.path.exists(course["img"]):
                    st.image(course["img"], use_container_width=True)
                
                st.subheader(course["name"])
                st.caption(f"Code: {course['code']} | Rating: {course['rating']}")
                st.write(f"**Monthly Fee:** `{course['fee']}`")
                
                course_wa = get_whatsapp_link("923001234567", f"Hi Sir Abdullah, I want to inquire about {course['name']}.")
                st.link_button("Inquire Course", course_wa, use_container_width=True)

# ---------------------------------------------------------
# PAGE 2: AI SUPPORT ASSISTANT
# ---------------------------------------------------------
elif page == "💬 AI Support Assistant":
    st.title("💬 Academy AI Support Assistant")
    st.caption("Ask questions regarding batch schedules, syllabus details, or admission requirements.")

    st.write("**Quick Suggestion Topics:**")
    c1, c2, c3, c4 = st.columns(4)
    quick_input = ""
    if c1.button("⏰ Business Hours", use_container_width=True):
        quick_input = "What are your business hours?"
    if c2.button("💳 Payment Methods", use_container_width=True):
        quick_input = "What payment methods do you accept?"
    if c3.button("📞 Contact Info", use_container_width=True):
        quick_input = "What is your contact number?"
    if c4.button("📖 Course List", use_container_width=True):
        quick_input = "What courses do you offer?"

    user_query = st.text_input("Type your question:", value=quick_input if quick_input else "", placeholder="Ask a question...")

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
    st.title("📝 Student Registration & Voucher Generator")
    st.caption("Fill in the details below to generate an official registration receipt.")

    with st.form("enrollment_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            student_name = st.text_input("Student Full Name*")
            guardian_email = st.text_input("Email Address")
        with col_b:
            guardian_phone = st.text_input("WhatsApp / Contact Number*")
            grade_level = st.selectbox("Grade / Board", ["O Level (O2)", "O Level (O3)", "IGCSE", "Other"])

        selected_course = st.selectbox("Select Course / Package", [c["name"] for c in COURSES])
        submitted = st.form_submit_button("Generate Registration Receipt", type="primary")

        if submitted:
            if student_name and guardian_phone:
                reg_id = f"SAA-{datetime.now().strftime('%Y%m%d%H%M')}"
                st.success("✅ Registration Processed Successfully!")
                st.balloons()

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
Present this Registration ID on WhatsApp to 
confirm your class schedule.
==========================================
"""

                with st.container(border=True):
                    st.subheader("🧾 Digital Registration Card")
                    st.write(f"**Registration ID:** `{reg_id}`")
                    st.write(f"**Student Name:** {student_name}")
                    st.write(f"**Enrolled Course:** {selected_course}")
                    st.write("**Status:** 🟡 Pending Verification")

                st.download_button(
                    label="📥 Download Official Receipt (.txt)",
                    data=receipt_text,
                    file_name=f"Receipt_{student_name.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            else:
                st.error("Please fill in all required fields (Student Name and Contact Number).")

# ---------------------------------------------------------
# PAGE 4: ADMIN DASHBOARD
# ---------------------------------------------------------
elif page == "📊 Admin Dashboard":
    st.title("📊 Academy Management Dashboard")
    st.caption("Live monitoring of query logs and platform status.")

    df_logs = load_logs()

    m1, m2, m3 = st.columns(3)
    m1.metric(label="Logged Queries", value=len(df_logs))
    m2.metric(label="Active Courses", value=len(COURSES))
    m3.metric(label="System Status", value="Live 🟢")

    st.divider()
    st.subheader("📋 Query Analytics (`query_log.csv`)")
    if not df_logs.empty:
        st.dataframe(df_logs, use_container_width=True)
        if "Category" in df_logs.columns:
            st.subheader("📈 Query Distribution by Topic")
            st.bar_chart(df_logs["Category"].value_counts())
    else:
        st.info("No queries logged yet. Incoming queries from the AI Support Assistant will automatically record here.")
