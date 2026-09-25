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

# MODERN GLASSMORPHISM & HIGH-CONTRAST DESIGN SYSTEM
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background: #080914 !important;
        color: #f1f5f9 !important;
    }

    /* FIX SIDEBAR TEXT VISIBILITY */
    section[data-testid="stSidebar"] {
        background-color: #0f1123 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        padding: 6px 10px !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.05) !important;
    }

    /* PREMIUM HERO BANNER */
    .hero-banner {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 20px;
        padding: 3.5rem 2rem;
        text-align: center;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        margin-bottom: 2.5rem;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2));
        border: 1px solid rgba(129, 140, 248, 0.4);
        color: #c7d2fe !important;
        padding: 6px 18px;
        border-radius: 30px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }
    .hero-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.8rem !important;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: #94a3b8 !important;
        max-width: 680px;
        margin: 0 auto;
        font-size: 1.05rem;
        line-height: 1.6;
        font-weight: 400;
    }

    /* INPUT FIELDS FIX */
    .stTextInput input, .stSelectbox select {
        background-color: #13162b !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }
    .stTextInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
    }

    /* CARD STYLING & GRID FIX */
    div[data-testid="stForm"], div[data-testid="stVerticalBlock"] > div[style*="flex"] {
        border-radius: 16px;
    }
    .course-card-box {
        background: #111328;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.25rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .course-card-box:hover {
        border-color: rgba(99, 102, 241, 0.5);
        transform: translateY(-3px);
    }

    /* METRICS CARDS */
    .metric-card {
        background: linear-gradient(180deg, #13162d 0%, #0d0f22 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
    }
    .metric-card h3 {
        color: #64748b !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem !important;
    }
    .metric-card h2 {
        color: #f8fafc !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }

    /* RECEIPT BOX */
    .receipt-card {
        background: #0f1226;
        border: 1px dashed #6366f1;
        border-radius: 14px;
        padding: 1.8rem;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def load_logs():
    if os.path.exists("query_log.csv"):
        return pd.read_csv("query_log.csv")
    return pd.DataFrame(columns=["Date", "Time", "Query", "Category"])

def get_whatsapp_link(phone_number, message):
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{phone_number}?text={encoded_message}"

# SIDEBAR NAVIGATION & PROFILE
with st.sidebar:
    if os.path.exists("assets/core_combo_logo.png"):
        st.image("assets/core_combo_logo.png", width=70)
    st.markdown("### **Sir Abdullah Academy**")
    st.markdown("<p style='font-size: 0.85rem; color: #94a3b8 !important; margin-top: -12px;'>O Level & IGCSE Specialist</p>", unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio("NAVIGATION", [
        "🏡 Home & Courses", 
        "💬 AI Support Assistant", 
        "📝 Enroll & Get Receipt", 
        "📊 Admin Dashboard"
    ])

    st.markdown("---")
    st.markdown("#### **Instant Support**")
    wa_url = get_whatsapp_link("923001234567", "Hi Sir Abdullah, I would like to inquire about course admissions.")
    st.markdown(f'''
        <a href="{wa_url}" target="_blank" style="text-decoration:none;">
            <div style="background: #22c55e; color: white; text-align: center; padding: 10px; border-radius: 10px; font-weight: 700; font-size: 0.9rem; box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);">
                💬 Chat on WhatsApp
            </div>
        </a>
    ''', unsafe_allow_html=True)

# COURSE CATALOG DATA
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
    <div class="hero-banner">
        <div class="hero-badge">✨ ADMISSIONS OPEN FOR O LEVEL & IGCSE</div>
        <div class="hero-title">Sir Abdullah Academy</div>
        <p class="hero-subtitle">
            Premier 100% Online Cambridge Coaching. Empowering students with conceptual understanding, 
            exam techniques, and rigorous topical past paper practice to secure top A* grades.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### **Course Offerings & Bundles**")
    search_query = st.text_input("", placeholder="🔍 Search by course name or subject code (e.g. Physics, 5054)...")

    filtered = [c for c in COURSES if search_query.lower() in c["name"].lower() or search_query.lower() in c["code"].lower()]

    cols = st.columns(3)
    for idx, course in enumerate(filtered):
        with cols[idx % 3]:
            with st.container():
                st.markdown('<div class="course-card-box">', unsafe_allow_html=True)
                if os.path.exists(course["img"]):
                    st.image(course["img"], use_container_width=True)
                st.markdown(f"#### **{course['name']}**")
                st.markdown(f"<p style='color:#64748b; font-size:0.85rem; margin-top:-8px;'>Code: {course['code']} | {course['rating']}</p>", unsafe_allow_html=True)
                st.markdown(f"**Monthly Fee:** `{course['fee']}`")
                
                course_wa = get_whatsapp_link("923001234567", f"Hi Sir Abdullah, I want to inquire about {course['name']}.")
                st.markdown(f'''
                    <a href="{course_wa}" target="_blank" style="text-decoration:none;">
                        <div style="background:#4f46e5; color:white; text-align:center; padding:8px; border-radius:8px; font-weight:600; font-size:0.85rem; margin-top:10px;">
                            Inquire Course
                        </div>
                    </a>
                ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 2: AI SUPPORT ASSISTANT
# ---------------------------------------------------------
elif page == "💬 AI Support Assistant":
    st.markdown("### **Academy AI Support Assistant**")
    st.markdown("<p style='color:#94a3b8;'>Ask questions regarding batch schedules, syllabus details, or admission requirements.</p>", unsafe_allow_html=True)

    st.markdown("**Quick Topics:**")
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

    user_query = st.text_input("", value=quick_input if quick_input else "", placeholder="Type your query here...")

    if user_query:
        try:
            response = handle_query(user_query)
        except Exception:
            response = "For custom timetable requests or specific queries, feel free to contact us on WhatsApp."
        st.info(f"**Answer:** {response}")

# ---------------------------------------------------------
# PAGE 3: ENROLL & GET RECEIPT
# ---------------------------------------------------------
elif page == "📝 Enroll & Get Receipt":
    st.markdown("### **Student Registration & Voucher Generator**")
    st.markdown("<p style='color:#94a3b8;'>Fill in the details below to generate an official registration receipt.</p>", unsafe_allow_html=True)

    with st.form("enrollment_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            student_name = st.text_input("Student Full Name*")
            guardian_email = st.text_input("Email Address")
        with col_b:
            guardian_phone = st.text_input("WhatsApp / Contact Number*")
            grade_level = st.selectbox("Grade / Board", ["O Level (O2)", "O Level (O3)", "IGCSE", "Other"])

        selected_course = st.selectbox("Select Course / Package", [c["name"] for c in COURSES])
        submitted = st.form_submit_button("Generate Registration Receipt")

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

                st.markdown(f"""
                <div class="receipt-card">
                    <h3 style="margin-top:0; color:#818cf8;">🧾 Digital Registration Card</h3>
                    <p><b>Registration ID:</b> <code>{reg_id}</code></p>
                    <p><b>Student Name:</b> {student_name}</p>
                    <p><b>Enrolled Course:</b> {selected_course}</p>
                    <p><b>Status:</b> <span style="color:#f59e0b; font-weight:600;">Pending Verification</span></p>
                </div>
                """, unsafe_allow_html=True)

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
    st.markdown("### **Academy Management Dashboard**")
    st.markdown("<p style='color:#94a3b8;'>Live metrics and customer inquiry query logs.</p>", unsafe_allow_html=True)

    df_logs = load_logs()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><h3>Total Queries</h3><h2>{len(df_logs)}</h2></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><h3>Active Courses</h3><h2>{len(COURSES)}</h2></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-card"><h3>System Status</h3><h2 style="color:#22c55e !important;">Live</h2></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### **Recorded Query Log (`query_log.csv`)**")
    if not df_logs.empty:
        st.dataframe(df_logs, use_container_width=True)
        if "Category" in df_logs.columns:
            st.markdown("#### **Query Distribution by Topic**")
            st.bar_chart(df_logs["Category"].value_counts())
    else:
        st.info("No queries logged yet. Incoming queries from the AI Support Assistant will automatically record here.")
