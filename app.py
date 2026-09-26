import streamlit as st
import pandas as pd
import re
from models import load_json, save_json
from utils import normalize_phone, sanitize_csv_field
from chatbot import get_bot_response
from github_store import sync_to_github

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="Sir Abdullah Academy | Premier O & A Level Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ULTRA-PROFESSIONAL & VIBRANT STYLING ---
st.markdown("""
<style>
    /* Hide Default Streamlit Elements */
    #MainMenu, footer, header { visibility: hidden; }

    /* Modern Typography Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

    /* Global Canvas */
    .stApp {
        background: 
            radial-gradient(circle at 0% 0%, rgba(99, 102, 241, 0.18) 0%, transparent 35%),
            radial-gradient(circle at 100% 20%, rgba(236, 72, 153, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 50% 80%, rgba(139, 92, 246, 0.2) 0%, transparent 45%),
            radial-gradient(circle at 90% 90%, rgba(245, 158, 11, 0.15) 0%, transparent 35%),
            #0a0e1a;
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px;
    }

    /* Keyframe Animations */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 15px rgba(124, 58, 237, 0.4); }
        50% { box-shadow: 0 0 30px rgba(124, 58, 237, 0.7); }
        100% { box-shadow: 0 0 15px rgba(124, 58, 237, 0.4); }
    }

    /* Header Styling */
    .brand-circle {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        color: white;
        width: 48px;
        height: 48px;
        border-radius: 14px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 1.15rem;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .brand-title {
        font-size: 1.45rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }

    /* Streamlit Button Overrides */
    div.stButton > button {
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.6rem !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        border: 1px solid transparent !important;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 35px rgba(139, 92, 246, 0.6) !important;
    }

    div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 10px 25px rgba(245, 158, 11, 0.35) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 35px rgba(245, 158, 11, 0.55) !important;
    }

    div[data-testid="stColumn"] button[kind="tertiary"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        background: transparent !important;
        padding: 0.5rem 1rem !important;
    }
    div[data-testid="stColumn"] button[kind="tertiary"]:hover {
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }

    /* Hero Section UI */
    .floating-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(139, 92, 246, 0.15);
        backdrop-filter: blur(12px);
        color: #a78bfa;
        font-size: 0.85rem;
        font-weight: 700;
        padding: 0.5rem 1.2rem;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(167, 139, 250, 0.3);
        margin-bottom: 1.5rem;
    }

    .hero-heading {
        font-size: 3.8rem;
        font-weight: 900;
        color: #ffffff;
        line-height: 1.1;
        letter-spacing: -2px;
        margin-bottom: 1.2rem;
    }
    
    .gradient-purple {
        background: linear-gradient(135deg, #a78bfa 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .gradient-gold {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subhead {
        font-size: 1.15rem;
        color: #94a3b8;
        line-height: 1.6;
        margin-bottom: 2.2rem;
        font-weight: 400;
        max-width: 580px;
    }

    /* Hero Graphics */
    .hero-graphic-card {
        position: relative;
        padding: 10px;
    }

    .badge-result-top {
        position: absolute;
        top: -12px;
        right: 15px;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(12px);
        color: #ffffff;
        font-size: 0.85rem;
        font-weight: 800;
        padding: 0.65rem 1.3rem;
        border-radius: 50px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.15);
        z-index: 10;
        animation: float 4s ease-in-out infinite;
    }

    .device-bezel {
        background: #0f172a;
        border-radius: 32px;
        padding: 14px;
        box-shadow: 0 30px 70px rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: pulseGlow 5s infinite;
    }

    .device-screen {
        background: linear-gradient(160deg, #1e1b4b 0%, #0f172a 100%);
        border-radius: 22px;
        padding: 2.5rem 1.8rem 2.2rem 1.8rem;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .pulse-dot {
        height: 10px;
        width: 10px;
        background-color: #10b981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 12px #10b981;
    }

    .screen-pill {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
        text-align: left;
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    .screen-pill:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(167, 139, 250, 0.4);
    }

    /* Features Grid Cards */
    .vibrant-feature-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        border-radius: 24px;
        padding: 2.2rem 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        height: 100%;
    }
    .vibrant-feature-card:hover {
        transform: translateY(-8px);
        background: rgba(15, 23, 42, 0.85);
        border-color: rgba(139, 92, 246, 0.5);
        box-shadow: 0 20px 45px rgba(139, 92, 246, 0.25);
    }

    .icon-box {
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        color: #a78bfa;
        border-radius: 18px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        margin-bottom: 1.2rem;
        border: 1px solid rgba(167, 139, 250, 0.3);
    }

    /* Stat Cards */
    .stat-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 22px;
        padding: 1.6rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transition: transform 0.25s ease;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        border-color: rgba(167, 139, 250, 0.4);
    }
    .stat-number {
        font-size: 2.4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #94a3b8;
        font-weight: 600;
        margin-top: 0.2rem;
    }

    /* --- FIXES FOR COURSES SECTION --- */
    
    /* 1. Radio Button Visibility Fix */
    div[data-testid="stRadio"] label p {
        color: #f8fafc !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }

    /* 2. Text Input / Search Bar Customization */
    div[data-testid="stTextInput"] input {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
        padding: 0.6rem 1rem !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 12px rgba(139, 92, 246, 0.4) !important;
    }

    /* 3. High Quality Uniform Course Card Containers */
    .course-card-wrapper {
        background: rgba(15, 23, 42, 0.75);
        border-radius: 24px;
        padding: 1.8rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 12px 35px rgba(0,0,0,0.35);
        margin-bottom: 1.5rem;
        backdrop-filter: blur(16px);
        transition: all 0.3s ease;
    }
    .course-card-wrapper:hover {
        border-color: rgba(167, 139, 250, 0.4);
        transform: translateY(-3px);
    }

    .combo-card-wrapper {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border-radius: 24px;
        padding: 1.8rem;
        border: 1px solid rgba(245, 158, 11, 0.4);
        box-shadow: 0 15px 40px rgba(245, 158, 11, 0.15);
        margin-bottom: 1.5rem;
        backdrop-filter: blur(16px);
        transition: all 0.3s ease;
    }
    .combo-card-wrapper:hover {
        border-color: rgba(245, 158, 11, 0.7);
        transform: translateY(-3px);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIG & DATA ---
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "osmanibhai112233")

SPECIAL_COMBOS = [
    {
        "id": "combo_med",
        "title": "Pre-Medical Master Bundle",
        "image_url": "assets/pre_medical_combo_logo.png",
        "badge": "SPECIAL BUNDLE",
        "fee": "PKR 16,000 / mo",
        "category": "Combos",
        "duration": "Online Live Classes",
        "desc": "Complete 4-subject package for Biology, Physics, Chemistry, and Mathematics. Includes full syllabus coverage, topical solved past papers, and ATP practical preparation.",
        "highlights": ["Save PKR 4,000/mo", "Full 4-Subject Coverage", "Weekly Mocks & Past Papers"]
    },
    {
        "id": "combo_cs",
        "title": "Pre-Engineering & CS Bundle",
        "image_url": "assets/cs_combo_logo.png",
        "badge": "SPECIAL BUNDLE",
        "fee": "PKR 16,000 / mo",
        "category": "Combos",
        "duration": "Online Live Classes",
        "desc": "Complete 4-subject package: Computer Science, Physics, Chemistry, and Math. Practice pseudocode, logic gates, and calculation strategies.",
        "highlights": ["Save PKR 4,000/mo", "Full CS & Engineering Prep", "Marking Scheme Drills"]
    },
    {
        "id": "combo_core",
        "title": "O1 / O2 Core Subjects Combo",
        "image_url": "assets/core_combo_logo.png",
        "badge": "CORE BUNDLE",
        "fee": "PKR 4,500 / mo",
        "category": "Combos",
        "duration": "Online Live Classes",
        "desc": "Dual-subject bundle for Islamiat (2058) and Pakistan Studies (2059). Complete Paper 1 & Paper 2 coverage with structured exam notes.",
        "highlights": ["Save PKR 500/mo", "Islamiat & PST Dual Prep", "Topical Past Paper Revision"]
    }
]

O_LEVEL_COURSES = [
    {
        "id": "cs",
        "title": "O Level / IGCSE Computer Science",
        "image_url": "assets/cs_logo.png",
        "badge": "CAIE 2210 / 0478",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "desc": "Master Theory & Paper 2 Problem Solving. Extensive practice with pseudocode, algorithms, flowcharts, and hardware theory.",
        "highlights": ["10+ Yrs Past Papers", "Pseudocode Practice", "Paper 1 & 2 Focus"]
    },
    {
        "id": "math",
        "title": "O Level / IGCSE Mathematics",
        "image_url": "assets/math_logo.png",
        "badge": "CAIE 4024 / 0580",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "desc": "Step-by-step conceptual clarity across Algebra, Trigonometry, Vectors, and Statistics with exam speed drills.",
        "highlights": ["Topical Worksheets", "Speed & Accuracy Drills", "Weekly Assessments"]
    },
    {
        "id": "phy",
        "title": "O Level / IGCSE Physics",
        "image_url": "assets/physics_logo.png",
        "badge": "CAIE 5054 / 0625",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "desc": "In-depth Physics coverage: Mechanics, Electricity, Magnetism, Waves, Space Physics, and ATP Paper 4 techniques.",
        "highlights": ["Formula Memorization Sheets", "ATP Exam Preparation", "MCQ Paper Strategies"]
    },
    {
        "id": "chem",
        "title": "O Level / IGCSE Chemistry",
        "image_url": "assets/chemistry_logo.png",
        "badge": "CAIE 5070 / 0620",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "desc": "Build deep clarity in Stoichiometry, Organic Chemistry, Chemical Energetics, and Electrochemistry with ATP practice.",
        "highlights": ["Stoichiometry Drills", "Organic Chemistry Maps", "ATP Practical Prep"]
    },
    {
        "id": "bio",
        "title": "O Level / IGCSE Biology",
        "image_url": "assets/biology_logo.png",
        "badge": "CAIE 5090 / 0610",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "desc": "Cell Biology, Plant Physiology, Genetics, and Human Systems with exact examiner keywords to ensure full marks.",
        "highlights": ["Examiner Keyword Mastery", "Diagram Drills", "Past Paper Packs"]
    },
    {
        "id": "isl",
        "title": "O Level / IGCSE Islamiat",
        "image_url": "assets/islamiat_logo.png",
        "badge": "CAIE 2058 / 0493",
        "fee": "PKR 2,500 / mo",
        "category": "Humanities",
        "duration": "Online Live Classes",
        "desc": "Structured preparation for Paper 1 & Paper 2: Quranic Passages, Seerah, Caliphates, and Hadith references with complete notes.",
        "highlights": ["14 & 4-Mark Outlines", "Quranic References", "Topical Answer Practice"]
    },
    {
        "id": "pst",
        "title": "O Level / IGCSE Pakistan Studies",
        "image_url": "assets/pst_logo.png",
        "badge": "CAIE 2059 / 0448",
        "fee": "PKR 2,500 / mo",
        "category": "Humanities",
        "duration": "Online Live Classes",
        "desc": "Complete history timelines & geography case studies with level-of-response answer templates and map skills.",
        "highlights": ["Chronological Timelines", "Map Skills & Case Studies", "Source-Based Questions"]
    }
]

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

if "selected_course_for_enrollment" not in st.session_state:
    st.session_state.selected_course_for_enrollment = SPECIAL_COMBOS[0]["title"]

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"

# --- 4. TOP FLOATING NAVBAR ---
col_logo, col_nav, col_cta = st.columns([2.2, 3, 1.3])

with col_logo:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 14px;">
        <div class="brand-circle">SAA</div>
        <span class="brand-title">Sir Abdullah Academy</span>
    </div>
    """, unsafe_allow_html=True)

with col_nav:
    n1, n2, n3, n4 = st.columns(4)
    with n1:
        if st.button("Home", key="nav_home", type="primary" if st.session_state.active_tab == "Home" else "tertiary"):
            st.session_state.active_tab = "Home"
            st.rerun()
    with n2:
        if st.button("Courses", key="nav_courses", type="primary" if st.session_state.active_tab == "Courses" else "tertiary"):
            st.session_state.active_tab = "Courses"
            st.rerun()
    with n3:
        if st.button("Admission", key="nav_admission", type="primary" if st.session_state.active_tab == "Admission" else "tertiary"):
            st.session_state.active_tab = "Admission"
            st.rerun()
    with n4:
        if st.button("AI Tutor", key="nav_ai", type="primary" if st.session_state.active_tab == "Assistant" else "tertiary"):
            st.session_state.active_tab = "Assistant"
            st.rerun()

with col_cta:
    if st.button("⚡ Enroll Now", key="nav_enroll_btn", type="secondary", use_container_width=True):
        st.session_state.active_tab = "Admission"
        st.rerun()

st.markdown("<hr style='border: none; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin: 1rem 0 2.5rem 0;'>", unsafe_allow_html=True)

# --- 5. ROUTE RENDERING ---

# PAGE: HOME HERO
if st.session_state.active_tab == "Home":
    hero_left, hero_right = st.columns([1.25, 1])

    with hero_left:
        st.markdown("""
        <div class="floating-pill">✨ Premium Online Learning Platform</div>
        <div class="hero-heading">
            Pakistan's <span class="gradient-purple">#1 Online</span> Academy for <span class="gradient-gold">O & A Level</span>
        </div>
        <div class="hero-subhead">
            Unlock your full academic potential with interactive live classes, topical solved past papers, examiner keyword mastery, and personalized 1-on-1 mentorship.
        </div>
        """, unsafe_allow_html=True)

        cta1, cta2 = st.columns(2)
        with cta1:
            if st.button("🚀 Explore Courses", key="hero_explore", type="primary", use_container_width=True):
                st.session_state.active_tab = "Courses"
                st.rerun()

        with cta2:
            if st.button("📝 Apply for Admission", key="hero_apply", type="secondary", use_container_width=True):
                st.session_state.active_tab = "Admission"
                st.rerun()

    with hero_right:
        st.markdown("""
        <div class="hero-graphic-card">
            <div class="badge-result-top">
                <span>🏆</span> 10,000+ A* Grades
            </div>
            <div class="device-bezel">
                <div class="device-screen">
                    <p style="text-transform: uppercase; font-size: 0.75rem; letter-spacing: 2px; font-weight: 800; color: #a78bfa; margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: center; gap: 8px;">
                        <span class="pulse-dot"></span> LIVE ACADEMY PORTAL
                    </p>
                    <h2 style="font-weight: 900; font-size: 2rem; color: #fbbf24; margin-bottom: 0.4rem; letter-spacing: -0.5px;">NOW STUDY ONLINE</h2>
                    <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 1.5rem;">Interactive Zoom & Meet Classes with Sir Abdullah</p>
                    <div class="screen-pill">
                        <p style="margin:0; font-size:0.88rem; font-weight:700; color: #f8fafc;">💻 Interactive Whiteboard & Instant Doubt Resolution</p>
                    </div>
                    <div class="screen-pill">
                        <p style="margin:0; font-size:0.88rem; font-weight:700; color: #f8fafc;">📚 10+ Years Topical Solved Past Papers</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- LIVE ACADEMY STATS BAR ---
    st.markdown("<h3 style='font-weight: 800; font-size: 1.4rem; margin-bottom: 1rem;'>📈 Academy Impact at a Glance</h3>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown('<div class="stat-card"><div class="stat-number">10,000+</div><div class="stat-label">A* & A Grades Secured</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="stat-card"><div class="stat-number">98.4%</div><div class="stat-label">CAIE Exam Pass Rate</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="stat-card"><div class="stat-number">24/7</div><div class="stat-label">AI Learning Support</div></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Feature Grid
    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("💻", "Live Interactive Classes", "Engage directly with expert faculty with immediate doubt resolution during live sessions."),
        ("📝", "Topical Past Papers", "10+ years of topical past paper practice fully aligned with CAIE marking schemes."),
        ("🎯", "Keyword Mastery", "Learn exact subject-specific examiner keywords required for top grade boundaries."),
        ("📊", "Parent Tracking", "Regular attendance updates, test feedback, and personal student performance reports.")
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(f"""
            <div class="vibrant-feature-card">
                <div class="icon-box">{icon}</div>
                <h4 style="font-weight: 800; color: #ffffff; margin-bottom: 0.6rem; font-size: 1.1rem;">{title}</h4>
                <p style="font-size: 0.88rem; color: #94a3b8; line-height: 1.6; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# PAGE: COURSES (FIXED AREA)
elif st.session_state.active_tab == "Courses":
    st.markdown("<h2 style='text-align: center; font-weight: 900; margin-bottom: 0.3rem;'>O Level & IGCSE Courses</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 2.2rem;'>Select an individual subject or discount combo package below.</p>", unsafe_allow_html=True)

    # Filter Bar
    f_col1, f_col2 = st.columns([2.5, 1.2])
    with f_col1:
        cat_filter = st.radio("Category Filter", ["All", "Combos", "Sciences", "Humanities"], horizontal=True, label_visibility="collapsed")
    with f_col2:
        search_txt = st.text_input("Search subject...", placeholder="Search subject or bundle...", label_visibility="collapsed")

    combined_courses = []
    for c in SPECIAL_COMBOS:
        combined_courses.append({**c, "is_combo": True})
    for c in O_LEVEL_COURSES:
        combined_courses.append({**c, "is_combo": False})

    filtered = combined_courses
    if cat_filter != "All":
        filtered = [c for c in filtered if c["category"] == cat_filter]
    if search_txt:
        filtered = [c for c in filtered if search_txt.lower() in c["title"].lower() or search_txt.lower() in c["desc"].lower()]

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Course List
    for item in filtered:
        c_img, c_main, c_side = st.columns([1, 2.5, 1])
        card_class = "combo-card-wrapper" if item["is_combo"] else "course-card-wrapper"
        badge_bg = "rgba(245, 158, 11, 0.18)" if item["is_combo"] else "rgba(139, 92, 246, 0.18)"
        badge_color = "#fbbf24" if item["is_combo"] else "#c084fc"

        with c_img:
            st.image(item["image_url"], use_container_width=True)
        with c_main:
            st.markdown(f"""
            <div class="{card_class}">
                <span style="background: {badge_bg}; color: {badge_color}; font-weight: 800; font-size: 0.75rem; padding: 0.35rem 0.9rem; border-radius: 50px; border: 1px solid {badge_color};">{item['badge']}</span>
                <h3 style="font-weight: 800; color: #ffffff; margin-top: 0.8rem; margin-bottom: 0.5rem; font-size: 1.35rem;">{item['title']}</h3>
                <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6; margin-bottom: 1rem;">{item['desc']}</p>
                <p style="color: #a78bfa; font-size: 0.85rem; font-weight: 700; margin: 0;">Key Features: {', '.join(item['highlights'])}</p>
            </div>
            """, unsafe_allow_html=True)
        with c_side:
            st.markdown(f"""
            <div class="{card_class}" style="text-align: center;">
                <p style="color: #94a3b8; font-size: 0.8rem; font-weight: 700; margin: 0;">Monthly Tuition Fee</p>
                <div style="font-size: 1.55rem; font-weight: 900; color: #fbbf24; margin: 0.4rem 0;">{item['fee']}</div>
                <p style="color: #64748b; font-size: 0.82rem; margin-bottom: 1.2rem;">⏱️ {item['duration']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Properly Labeled Enroll Button
            if st.button("⚡ Enroll Now", key=f"btn_enroll_{item['id']}", type="primary", use_container_width=True):
                st.session_state.selected_course_for_enrollment = item['title']
                st.session_state.active_tab = "Admission"
                st.rerun()

# PAGE: ADMISSION
elif st.session_state.active_tab == "Admission":
    st.markdown("<h2 style='text-align: center; font-weight: 900; margin-bottom: 0.3rem;'>📝 Online Admission Portal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 2rem;'>Complete the details below to reserve your seat in the upcoming batch.</p>", unsafe_allow_html=True)

    all_options = [c["title"] for c in SPECIAL_COMBOS] + [c["title"] for c in O_LEVEL_COURSES]
    default_idx = 0
    if st.session_state.selected_course_for_enrollment in all_options:
        default_idx = all_options.index(st.session_state.selected_course_for_enrollment)

    with st.form("admission_form_ivy", clear_on_submit=True):
        a1, a2 = st.columns(2)
        with a1:
            name = st.text_input("Student's Full Name *", placeholder="e.g. Ali Ahmed")
            email = st.text_input("Parent / Student Email *", placeholder="e.g. parent@example.com")
        with a2:
            phone = st.text_input("WhatsApp Number *", placeholder="e.g. +92 332 1234567")
            selected_course = st.selectbox("Target Course / Combo *", all_options, index=default_idx)

        submitted = st.form_submit_button("Submit Admission Application", type="primary")

        if submitted:
            if not name.strip():
                st.error("Please enter the student's full name.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address.")
            elif len(phone.strip()) < 8:
                st.error("Please enter a valid WhatsApp phone number.")
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
                st.success(f"Application submitted successfully for **{name}**! Details will be sent to **{norm_phone}** via WhatsApp.")

# PAGE: AI TUTOR
elif st.session_state.active_tab == "Assistant":
    st.markdown("<h2 style='text-align: center; font-weight: 900; margin-bottom: 0.3rem;'>🤖 AI Learning Assistant</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 2rem;'>Ask questions about course syllabi, class schedules, or exam strategies.</p>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you with Cambridge O Level / IGCSE subjects today?"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask a question about classes, fees, or subjects..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

# ADMIN PANEL FOOTER
st.markdown("<br><hr style='border: none; border-bottom: 1px solid rgba(255, 255, 255, 0.08);'><br>", unsafe_allow_html=True)
with st.expander("🔒 Admin Portal Access"):
    admin_pwd = st.text_input("Enter Admin Password", type="password")
    if admin_pwd == ADMIN_PASSWORD:
        st.success("Authorized Access Granted")
        enrollments = load_json("enrollments.json", [])
        if enrollments:
            df = pd.DataFrame(enrollments)
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Registrations CSV", data=csv, file_name="enrollments_export.csv", mime="text/csv")
        else:
            st.info("No enrollment submissions found.")
    elif admin_pwd:
        st.error("Incorrect password.")
