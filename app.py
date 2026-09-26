import streamlit as st
import pandas as pd
import re
from models import load_json, save_json
from utils import normalize_phone, sanitize_csv_field
from chatbot import get_bot_response
from github_store import sync_to_github

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="Sir Abdullah Academy | Premier O & A Level Online Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. VIBRANT & ADVANCED MODERN STYLING WITH BACKGROUND MESH ---
st.markdown("""
<style>
    /* Hide Default Streamlit Chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

    /* Global Canvas with Mesh Radiant Animated Background */
    .stApp {
        background: 
            radial-gradient(circle at 10% 10%, rgba(147, 51, 234, 0.15) 0%, transparent 45%),
            radial-gradient(circle at 90% 15%, rgba(245, 158, 11, 0.12) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 85%, rgba(236, 72, 153, 0.12) 0%, transparent 45%),
            #f8fafc;
        color: #0f172a;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1260px;
    }

    /* Fixed Top Navbar Glassmorphic Container */
    .brand-circle {
        background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%);
        color: white;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 1.1rem;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.4);
    }
    
    .brand-title {
        font-size: 1.35rem;
        font-weight: 900;
        background: linear-gradient(135deg, #4c1d95 0%, #1e1b4b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }

    /* Navigation Button Customization */
    div[data-testid="stColumn"] button[kind="tertiary"] {
        color: #475569 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border: none !important;
        background: transparent !important;
        padding: 0.4rem 0.8rem !important;
    }
    div[data-testid="stColumn"] button[kind="tertiary"]:hover {
        color: #7c3aed !important;
    }
    div[data-testid="stColumn"] button[kind="primary"] {
        background: #f3e8ff !important;
        color: #6d28d9 !important;
        font-weight: 800 !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Vibrant Buttons */
    .btn-gradient-purple button {
        background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 0.98rem !important;
        border-radius: 50px !important;
        padding: 0.75rem 1.8rem !important;
        border: none !important;
        box-shadow: 0 10px 25px rgba(124, 58, 237, 0.35) !important;
        transition: all 0.25s ease !important;
    }
    .btn-gradient-purple button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 14px 30px rgba(124, 58, 237, 0.5) !important;
    }

    .btn-gradient-amber button {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 0.98rem !important;
        border-radius: 50px !important;
        padding: 0.75rem 1.8rem !important;
        border: none !important;
        box-shadow: 0 10px 25px rgba(217, 119, 6, 0.35) !important;
        transition: all 0.25s ease !important;
    }
    .btn-gradient-amber button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 14px 30px rgba(217, 119, 6, 0.5) !important;
    }

    /* Hero Typography */
    .floating-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #ffffff;
        color: #6d28d9;
        font-size: 0.82rem;
        font-weight: 800;
        padding: 0.45rem 1.2rem;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(109, 40, 217, 0.1);
        border: 1px solid #ede9fe;
        margin-bottom: 1.2rem;
    }

    .hero-heading {
        font-size: 3.8rem;
        font-weight: 900;
        color: #0f172a;
        line-height: 1.1;
        letter-spacing: -2px;
        margin-bottom: 1.2rem;
    }
    
    .gradient-purple {
        background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .gradient-gold {
        background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subhead {
        font-size: 1.15rem;
        color: #475569;
        line-height: 1.6;
        margin-bottom: 2.2rem;
        font-weight: 500;
        max-width: 580px;
    }

    /* Hero Frame */
    .hero-graphic-card {
        position: relative;
        padding: 10px;
    }

    .badge-result-top {
        position: absolute;
        top: -15px;
        right: 20px;
        background: #ffffff;
        color: #0f172a;
        font-size: 0.85rem;
        font-weight: 800;
        padding: 0.6rem 1.2rem;
        border-radius: 50px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
        border: 1px solid #e2e8f0;
        z-index: 10;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .device-bezel {
        background: #090d16;
        border-radius: 36px;
        padding: 12px;
        box-shadow: 0 30px 70px rgba(109, 40, 217, 0.25);
        border: 1px solid #1e293b;
    }

    .device-screen {
        background: linear-gradient(145deg, #3b0764 0%, #1e1b4b 100%);
        border-radius: 26px;
        padding: 2.8rem 1.8rem 2.2rem 1.8rem;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .pulse-dot {
        height: 8px;
        width: 8px;
        background-color: #22c55e;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #22c55e;
    }

    .screen-pill {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 16px;
        padding: 0.9rem 1.2rem;
        margin-top: 0.9rem;
        text-align: left;
        backdrop-filter: blur(12px);
        transition: transform 0.2s ease;
    }
    .screen-pill:hover {
        transform: scale(1.02);
        background: rgba(255, 255, 255, 0.12);
    }

    /* Enterprise Feature Cards */
    .vibrant-feature-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 2rem 1.4rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .vibrant-feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(109, 40, 217, 0.15);
        border-color: #c084fc;
    }

    .icon-box {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);
        color: #7c3aed;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.7rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 6px 15px rgba(124, 58, 237, 0.15);
    }

    /* Live Stat KPI Counter Bar */
    .stat-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid #ede9fe;
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.06);
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 900;
        color: #6d28d9;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 700;
    }

    /* Review Cards */
    .review-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #f1f5f9;
        box-shadow: 0 8px 20px rgba(0,0,0,0.03);
    }

    /* Course Cards */
    .course-card-wrapper {
        background: #ffffff;
        border-radius: 24px;
        padding: 1.8rem;
        border: 1px solid #f1f5f9;
        box-shadow: 0 6px 25px rgba(0,0,0,0.03);
        margin-bottom: 1.2rem;
    }
    .combo-card-wrapper {
        background: linear-gradient(135deg, #ffffff 0%, #faf5ff 100%);
        border-radius: 24px;
        padding: 1.8rem;
        border: 2px solid #c084fc;
        box-shadow: 0 12px 35px rgba(192, 132, 252, 0.18);
        margin-bottom: 1.2rem;
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
        "highlights": ["Past Papers Practice", "Pseudocode Practice", "Paper 1 & 2 Focus"]
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
col_logo, col_nav, col_cta = st.columns([2, 3, 1.3])

with col_logo:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px;">
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
    st.markdown('<div class="btn-gradient-purple">', unsafe_allow_html=True)
    if st.button("⚡ Enroll Now", key="nav_enroll_btn", use_container_width=True):
        st.session_state.active_tab = "Admission"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: none; border-bottom: 1px solid rgba(226, 232, 240, 0.8); margin: 0.8rem 0 2rem 0;'>", unsafe_allow_html=True)

# --- 5. ROUTE RENDERING ---

# PAGE: HOME HERO
if st.session_state.active_tab == "Home":
    hero_left, hero_right = st.columns([1.25, 1])

    with hero_left:
        st.markdown("""
        <div class="floating-pill">⭐ Every Lesson Counts</div>
        <div class="hero-heading">
            Pakistan's <span class="gradient-purple">#1 Online</span> Platform for <span class="gradient-gold">O & A Level</span> Success
        </div>
        <div class="hero-subhead">
            High-quality interactive live classes, topical solved past papers, examiner keyword mastery, and expert teachers — guaranteed to secure top A* grades.
        </div>
        """, unsafe_allow_html=True)

        cta1, cta2 = st.columns(2)
        with cta1:
            st.markdown('<div class="btn-gradient-purple">', unsafe_allow_html=True)
            if st.button("🚀 Explore Courses", key="hero_explore", use_container_width=True):
                st.session_state.active_tab = "Courses"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with cta2:
            st.markdown('<div class="btn-gradient-amber">', unsafe_allow_html=True)
            if st.button("📝 Apply for Admission", key="hero_apply", use_container_width=True):
                st.session_state.active_tab = "Admission"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with hero_right:
        st.markdown("""
        <div class="hero-graphic-card">
            <div class="badge-result-top">
                <span>🎗️</span> 10,000+ A* Results
            </div>
            <div class="device-bezel">
                <div class="device-screen">
                    <p style="text-transform: uppercase; font-size: 0.75rem; letter-spacing: 1.5px; font-weight: 800; color: #c084fc; margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: center; gap: 8px;">
                        <span class="pulse-dot"></span> LIVE ONLINE BATCH
                    </p>
                    <h2 style="font-weight: 900; font-size: 1.9rem; color: #facc15; margin-bottom: 0.4rem; letter-spacing: -0.5px;">NOW STUDY ONLINE</h2>
                    <p style="font-size: 0.9rem; opacity: 0.85; margin-bottom: 1.5rem;">Interactive Zoom & Meet Classes with Sir Abdullah</p>
                    <div class="screen-pill">
                        <p style="margin:0; font-size:0.88rem; font-weight:700;">💻 Digital Whiteboard & Instant Doubts</p>
                    </div>
                    <div class="screen-pill">
                        <p style="margin:0; font-size:0.88rem; font-weight:700;">📚 Comprehensive Topical Solved Papers</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- LIVE ACADEMY STATS BAR ---
    st.markdown("### 📈 Academy Impact at a Glance")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown('<div class="stat-card"><div class="stat-number">10,000+</div><div class="stat-label">A* & A Grades Secured</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="stat-card"><div class="stat-number">Expert</div><div class="stat-label">Top Tier Faculty</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="stat-card"><div class="stat-number">98.4%</div><div class="stat-label">CAIE Exam Pass Rate</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown('<div class="stat-card"><div class="stat-number">24/7</div><div class="stat-label">AI Tutor Support</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature Grid
    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("💻", "Live Interactive Classes", "Engage directly with expert faculty with immediate doubt resolution."),
        ("📝", "Topical Past Papers", "Comprehensive topical past paper practice aligned with CAIE marking schemes."),
        ("🎯", "Keyword Mastery", "Learn subject-specific keywords required for full marks in exam papers."),
        ("📊", "Parent Tracking", "Regular attendance updates, test feedback, and personal performance reports.")
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(f"""
            <div class="vibrant-feature-card">
                <div class="icon-box">{icon}</div>
                <h4 style="font-weight: 800; color: #0f172a; margin-bottom: 0.5rem; font-size: 1.05rem;">{title}</h4>
                <p style="font-size: 0.85rem; color: #64748b; line-height: 1.55; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # --- STUDENT TESTIMONIALS SECTION ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-weight: 900;'>🌟 Success Stories from Our Students</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 1.8rem;'>See how Sir Abdullah Academy helped students achieve top CAIE positions.</p>", unsafe_allow_html=True)
    
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("""
        <div class="review-card">
            <p style="color: #f59e0b; font-weight: 800; margin-bottom: 0.4rem;">⭐⭐⭐⭐⭐</p>
            <p style="font-size: 0.88rem; color: #334155; line-height: 1.5;">"Sir Abdullah's keyword mastery strategy helped me score 4 A*s in O Level CS & Sciences. The topical past paper drills made all the difference!"</p>
            <h5 style="font-weight: 800; color: #6d28d9; margin-top: 0.8rem; margin-bottom: 0;">— Hamza Malik</h5>
            <span style="font-size: 0.75rem; color: #94a3b8;">4 A*s | O Level Student</span>
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div class="review-card">
            <p style="color: #f59e0b; font-weight: 800; margin-bottom: 0.4rem;">⭐⭐⭐⭐⭐</p>
            <p style="font-size: 0.88rem; color: #334155; line-height: 1.5;">"The live classes and instant doubt solver allowed me to stay ahead of my school syllabus. Best online academy in Pakistan hands down."</p>
            <h5 style="font-weight: 800; color: #6d28d9; margin-top: 0.8rem; margin-bottom: 0;">— Ayesha Siddiqui</h5>
            <span style="font-size: 0.75rem; color: #94a3b8;">3 A*s 1 A | IGCSE Student</span>
        </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown("""
        <div class="review-card">
            <p style="color: #f59e0b; font-weight: 800; margin-bottom: 0.4rem;">⭐⭐⭐⭐⭐</p>
            <p style="font-size: 0.88rem; color: #334155; line-height: 1.5;">"As a parent, I loved the weekly performance reports and test updates. My son improved from grade C to an A* in just 4 months!"</p>
            <h5 style="font-weight: 800; color: #6d28d9; margin-top: 0.8rem; margin-bottom: 0;">— Dr. Imran Tariq</h5>
            <span style="font-size: 0.75rem; color: #94a3b8;">Parent of A Level Student</span>
        </div>
        """, unsafe_allow_html=True)

# PAGE: COURSES
elif st.session_state.active_tab == "Courses":
    st.markdown("<h2 style='text-align: center; font-weight: 900; margin-bottom: 0.3rem;'>O Level & IGCSE Courses</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 2rem;'>Select an individual subject or discount combo package below.</p>", unsafe_allow_html=True)

    f_col1, f_col2 = st.columns([2, 1])
    with f_col1:
        cat_filter = st.radio("Category Filter", ["All", "Combos", "Sciences", "Humanities"], horizontal=True, label_visibility="collapsed")
    with f_col2:
        search_txt = st.text_input("Search subject...", placeholder="e.g. Computer Science or Pre-Medical", label_visibility="collapsed")

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

    for item in filtered:
        c_img, c_main, c_side = st.columns([1, 2.5, 1])
        card_class = "combo-card-wrapper" if item["is_combo"] else "course-card-wrapper"
        badge_bg = "#fef3c7" if item["is_combo"] else "#f3e8ff"
        badge_color = "#b45309" if item["is_combo"] else "#7e22ce"

        with c_img:
            st.image(item["image_url"], use_container_width=True)
        with c_main:
            st.markdown(f"""
            <div class="{card_class}">
                <span style="background: {badge_bg}; color: {badge_color}; font-weight: 800; font-size: 0.72rem; padding: 0.3rem 0.8rem; border-radius: 50px;">{item['badge']}</span>
                <h3 style="font-weight: 800; color: #0f172a; margin-top: 0.6rem; margin-bottom: 0.4rem;">{item['title']}</h3>
                <p style="color: #475569; font-size: 0.88rem; line-height: 1.5; margin-bottom: 0.8rem;">{item['desc']}</p>
                <p style="color: #6d28d9; font-size: 0.82rem; font-weight: 700;">Key Features: {', '.join(item['highlights'])}</p>
            </div>
            """, unsafe_allow_html=True)
        with c_side:
            st.markdown(f"""
            <div class="{card_class}" style="text-align: center;">
                <p style="color: #64748b; font-size: 0.8rem; font-weight: 700; margin: 0;">Monthly Tuition Fee</p>
                <div style="font-size: 1.4rem; font-weight: 900; color: #6d28d9;">{item['fee']}</div>
                <p style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 1rem;">⏱️ {item['duration']}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="btn-gradient-purple">', unsafe_allow_html=True)
            if st.button(f"Enroll in {item['id']}", key=f"btn_enroll_{item['id']}", use_container_width=True):
                st.session_state.selected_course_for_enrollment = item['title']
                st.session_state.active_tab = "Admission"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# PAGE: ADMISSION
elif st.session_state.active_tab == "Admission":
    st.markdown("<h2 style='text-align: center; font-weight: 900; margin-bottom: 0.3rem;'>📝 Online Admission Portal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 2rem;'>Complete the details below to reserve your seat in the upcoming batch.</p>", unsafe_allow_html=True)

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

        submitted = st.form_submit_button("Submit Admission Application")

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
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 2rem;'>Ask questions about course syllabi, class schedules, or exam strategies.</p>", unsafe_allow_html=True)

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
st.markdown("<br><hr style='border: none; border-bottom: 1px solid rgba(226, 232, 240, 0.8);'><br>", unsafe_allow_html=True)
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
