import streamlit as st
import pandas as pd
from models import load_json, save_json
from utils import normalize_phone, sanitize_csv_field
from chatbot import get_bot_response
from github_store import sync_to_github

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="Sir Abdullah Academy | Premier Online O Level & IGCSE Coaching",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PROFESSIONAL ACADEMY STYLING ---
st.markdown("""
<style>
    .stApp {
        background: #090d16;
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }

    /* Hero Section */
    .hero-banner {
        background: linear-gradient(135deg, #1e1b4b 0%, #311b92 50%, #0f172a 100%);
        border: 1px solid #3730a3;
        border-radius: 16px;
        padding: 4rem 2rem;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(49, 27, 146, 0.35);
    }
    .hero-badge {
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        border: 1px solid #6366f1;
        font-size: 0.85rem;
        font-weight: 700;
        padding: 0.35rem 1rem;
        border-radius: 50px;
        display: inline-block;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.8rem;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: #c7d2fe;
        max-width: 800px;
        margin: 0 auto 1.8rem auto;
        line-height: 1.6;
    }

    /* Trust Stats Grid */
    .stat-box {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 800;
        color: #38bdf8;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 600;
    }

    /* Feature Cards */
    .feature-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1.8rem 1.2rem;
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        border-color: #6366f1;
        transform: translateY(-4px);
    }
    .feature-icon {
        font-size: 2.2rem;
        margin-bottom: 0.6rem;
    }
    .feature-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.4rem;
    }
    .feature-desc {
        font-size: 0.88rem;
        color: #94a3b8;
        line-height: 1.5;
    }

    /* Course Cards */
    .course-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1.8rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .combo-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #1e293b 100%);
        border: 2px solid #6366f1;
        border-radius: 14px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.25);
    }
    .course-badge {
        background: #312e81;
        color: #a5b4fc;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.3rem 0.7rem;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .combo-badge {
        background: #4f46e5;
        color: #ffffff;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .course-fee {
        color: #34d399;
        font-size: 1.3rem;
        font-weight: 800;
    }

    /* Streamlit Image Formatting for Course Cards */
    [data-testid="stImage"] img {
        border-radius: 12px;
        border: 1px solid #334155;
    }

    .sidebar-head {
        font-size: 1.3rem;
        font-weight: 800;
        color: #ffffff;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #312e81;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. COURSES & PACKAGES LISTING WITH IMAGE LOGOS ---
SPECIAL_COMBOS = [
    {
        "title": "The Pre-Medical Combo (Bio, Physics, Chem, Math)",
        "image_url": "assets/pre_medical_combo_logo.png",
        "badge": "PRE-MEDICAL SPECIAL BUNDLE",
        "fee": "PKR 16,000 / mo",
        "duration": "Online Live Classes",
        "desc": "Complete 4-subject package for aspiring medical students covering Biology, Physics, Chemistry, and Mathematics. Includes intensive syllabus coverage, topical past papers, and ATP exam preparation.",
        "highlights": ["Save PKR 4,000/mo vs individual enrolment", "Full coverage of Bio, Physics, Chemistry & Math", "Weekly Mocks & Topical Past Paper Drills"]
    },
    {
        "title": "The Computer Science Combo (CS, Physics, Chem, Math)",
        "image_url": "assets/cs_combo_logo.png",
        "badge": "PRE-ENGINEERING & CS BUNDLE",
        "fee": "PKR 16,000 / mo",
        "duration": "Online Live Classes",
        "desc": "Complete 4-subject package designed for future Engineers & Tech students: Computer Science, Physics, Chemistry, and Mathematics. Focuses on Pseudocode, Logic Gates, Calculations & ATPs.",
        "highlights": ["Save PKR 4,000/mo vs individual enrolment", "Full coverage of CS, Physics, Chem & Math", "Logic Drills, Code Practice & Marking Scheme Mastery"]
    },
    {
        "title": "O1 / O2 Core Appearing Combo (Islamiat + PST)",
        "image_url": "assets/core_combo_logo.png",
        "badge": "CORE SUBJECTS BUNDLE",
        "fee": "PKR 4,500 / mo",
        "duration": "Online Live Classes",
        "desc": "Complete dual-subject bundle for early appearing O Level / IGCSE subjects (Islamiat 2058 / PST 2059). Covers full Paper 1 & Paper 2 syllabus for both subjects with structured exam notes and past paper practice.",
        "highlights": ["Save PKR 500/mo vs individual enrolment", "Full coverage of Islamiat, History & Geography modules", "Topical Past Paper Revision & Mock Exam Assessments"]
    }
]

O_LEVEL_COURSES = [
    {
        "title": "O Level / IGCSE Computer Science",
        "image_url": "assets/cs_logo.png",
        "badge": "CAIE 2210 / 0478",
        "fee": "PKR 5,000 / mo",
        "duration": "Online Live Classes",
        "desc": "Master Theory (Hardware, Logic Gates, Data Transmission) & Paper 2 Problem Solving. Comprehensive practice in Pseudocode, Flowcharts, and Algorithm Design.",
        "highlights": ["10+ Years Past Paper Practice", "Pseudocode & Logic Drills", "Paper 1 & 2 Marking Scheme Mastery"]
    },
    {
        "title": "O Level / IGCSE Mathematics",
        "image_url": "assets/math_logo.png",
        "badge": "CAIE 4024 / 0580",
        "fee": "PKR 5,000 / mo",
        "duration": "Online Live Classes",
        "desc": "Clear step-by-step conceptual learning across Algebra, Trigonometry, Vectors, Mensuration, and Probability with intensive exam-style problem solving.",
        "highlights": ["Topical Worksheets & Solutions", "Exam Speed & Accuracy Drills", "Regular Assessment Tests"]
    },
    {
        "title": "O Level / IGCSE Physics",
        "image_url": "assets/physics_logo.png",
        "badge": "CAIE 5054 / 0625",
        "fee": "PKR 5,000 / mo",
        "duration": "Online Live Classes",
        "desc": "In-depth physics coverage: Mechanics, Thermal Physics, Waves, Electricity & Magnetism, Space Physics, and ATP (Paper 4) exam techniques.",
        "highlights": ["Formula Memorization Sheets", "Alternative to Practical (ATP) Focus", "MCQ Paper 1 Strategies"]
    },
    {
        "title": "O Level / IGCSE Chemistry",
        "image_url": "assets/chemistry_logo.png",
        "badge": "CAIE 5070 / 0620",
        "fee": "PKR 5,000 / mo",
        "duration": "Online Live Classes",
        "desc": "Build deep clarity in Stoichiometry, Organic Chemistry, Chemical Energetics, and Electrochemistry combined with dedicated ATP Paper preparation.",
        "highlights": ["Stoichiometry Problem Drills", "Organic Chemistry Flowcharts", "ATP Practical Exam Prep"]
    },
    {
        "title": "O Level / IGCSE Biology",
        "image_url": "assets/biology_logo.png",
        "badge": "CAIE 5090 / 0610",
        "fee": "PKR 5,000 / mo",
        "duration": "Online Live Classes",
        "desc": "Cell Biology, Plant Physiology, Genetics, Biotechnology, and Human Systems taught with precise examiner keywords to ensure maximum marks.",
        "highlights": ["Cambridge Marking Scheme Keywords", "Diagram & Function Practice", "Past Paper Revision Packs"]
    },
    {
        "title": "O Level / IGCSE Islamiat",
        "image_url": "assets/islamiat_logo.png",
        "badge": "CAIE 2058 / 0493",
        "fee": "PKR 2,500 / mo",
        "duration": "Online Live Classes",
        "desc": "Structured preparation for Paper 1 & Paper 2: Quranic Passages, Life of Prophet (PBUH), Caliphates, Hadiths, and Articles of Faith with ready-to-learn notes.",
        "highlights": ["14-Mark & 4-Mark Structured Outlines", "Quranic & Hadith References", "Topical Exam Practice"]
    },
    {
        "title": "O Level / IGCSE PST (Pakistan Studies)",
        "image_url": "assets/pst_logo.png",
        "badge": "CAIE 2059 / 0448",
        "fee": "PKR 2,500 / mo",
        "duration": "Online Live Classes",
        "desc": "Complete coverage of Paper 1 (History & Culture of Pakistan) and Paper 2 (Environment of Pakistan). Features level-of-response answer templates, maps, and case studies.",
        "highlights": ["Chronological Timelines & Answer Templates", "Geography Map Skills & Case Studies", "Topical Source-Based Questions"]
    }
]

ADMIN_PASSWORD = "osmanibhai112233"

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown('<div class="sidebar-head">🎓 Main Menu</div>', unsafe_allow_html=True)
    menu = st.radio(
        "Navigate",
        ["🏠 Academy Home", "📝 Course Admission", "🤖 Chat Assistant", "🔒 Admin Dashboard"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="background: #1e293b; padding: 1.2rem; border-radius: 12px; border: 1px solid #334155;">
        <p style="color: #ffffff; font-weight: 700; margin-bottom: 0.4rem; font-size: 0.95rem;">💻 Class Mode</p>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0; line-height: 1.4;">100% Online Live Classes<br>(Interactive via Zoom / Google Meet)</p>
        <hr style="border-color: #334155; margin: 0.8rem 0;">
        <p style="color: #ffffff; font-weight: 700; margin-bottom: 0.4rem; font-size: 0.95rem;">📞 Contact & WhatsApp</p>
        <p style="color: #38bdf8; font-size: 0.88rem; font-weight: 600; margin: 0;">+92 332 1234567</p>
        <p style="color: #94a3b8; font-size: 0.78rem; margin-top: 0.2rem;">Admissions open for upcoming session.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. PAGE ROUTING ---

# === PAGE 1: ACADEMY HOME ===
if menu == "🏠 Academy Home":
    st.markdown("""
    <div class="hero-banner">
        <span class="hero-badge">✨ ADMISSIONS OPEN FOR O LEVEL & IGCSE</span>
        <div class="hero-title">Sir Abdullah Academy</div>
        <div class="hero-subtitle">Premier 100% Online Cambridge Coaching. Empowering students with conceptual understanding, exam techniques, and rigorous topical past paper practice to secure top A* grades.</div>
    </div>
    """, unsafe_allow_html=True)

    # Trust Metrics for Parents
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="stat-box"><div class="stat-number">100%</div><div class="stat-label">Online Interactive Live Classes</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="stat-box"><div class="stat-number">10+ Yrs</div><div class="stat-label">Topical Past Paper Coverage</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="stat-box"><div class="stat-number">A* Focused</div><div class="stat-label">Cambridge Examiner Techniques</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="stat-box"><div class="stat-number">Small Batches</div><div class="stat-label">Personal Attention & Weekly Mocks</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Key Features
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💻</div>
            <div class="feature-title">Live & Interactive</div>
            <div class="feature-desc">Real-time live classes with instant doubt solving, whiteboards, and class recordings.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Topical Past Papers</div>
            <div class="feature-desc">Rigorous practice with official marking schemes to master examiner expectations.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Keyword Mastery</div>
            <div class="feature-desc">Learn key phrases and exact terminology required for top marks in CAIE assessments.</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Parent Progress Updates</div>
            <div class="feature-desc">Regular testing, homework feedback, and attendance reporting for complete peace of mind.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><h2 style='text-align: center; color: white;'>O Level & IGCSE Special Combo Packages</h2><p style='text-align: center; color: #94a3b8; margin-bottom: 2rem;'>Discounted bundle offerings for Science, Computer, and Core subjects.</p>", unsafe_allow_html=True)

    # Render Combos
    for combo in SPECIAL_COMBOS:
        col_img, col_main, col_side = st.columns([1.2, 2.5, 1])
        with col_img:
            # Displays graphic banner image logo
            st.image(combo['image_url'], use_container_width=True)
        with col_main:
            st.markdown(f"""
            <div class="combo-card">
                <span class="combo-badge">{combo['badge']}</span>
                <h3 style="color: white; margin-top: 0.6rem; margin-bottom: 0.5rem;">{combo['title']}</h3>
                <p style="color: #c7d2fe; font-size: 0.95rem; line-height: 1.5;">{combo['desc']}</p>
                <p style="color: #38bdf8; font-size: 0.85rem; font-weight: 700;">Package Features: {', '.join(combo['highlights'])}</p>
            </div>
            """, unsafe_allow_html=True)
        with col_side:
            st.markdown(f"""
            <div class="combo-card" style="text-align: center;">
                <p style="color: #a5b4fc; margin: 0; font-size: 0.85rem; font-weight: 700;">Bundle Fee</p>
                <p class="course-fee">{combo['fee']}</p>
                <p style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0;">⏱️ {combo['duration']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: white; margin-top: 2rem;'>Individual Subject Courses</h2><p style='text-align: center; color: #94a3b8; margin-bottom: 2rem;'>Select single subjects based on student requirement.</p>", unsafe_allow_html=True)

    # Render Individual Subjects
    for course in O_LEVEL_COURSES:
        col_img, col_main, col_side = st.columns([1.2, 2.5, 1])
        with col_img:
            # Displays graphic banner image logo
            st.image(course['image_url'], use_container_width=True)
        with col_main:
            st.markdown(f"""
            <div class="course-card">
                <span class="course-badge">{course['badge']}</span>
                <h3 style="color: white; margin-top: 0.6rem; margin-bottom: 0.5rem;">{course['title']}</h3>
                <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5;">{course['desc']}</p>
                <p style="color: #cbd5e1; font-size: 0.85rem; font-weight: 600;">Key Focus: {', '.join(course['highlights'])}</p>
            </div>
            """, unsafe_allow_html=True)
        with col_side:
            st.markdown(f"""
            <div class="course-card" style="text-align: center;">
                <p style="color: #94a3b8; margin: 0; font-size: 0.85rem; font-weight: 600;">Monthly Fee</p>
                <p class="course-fee">{course['fee']}</p>
                <p style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0;">⏱️ {course['duration']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("💡 **Parents & Students:** To enroll or reserve a seat in an upcoming batch, select **Course Admission** from the sidebar menu.")

# === PAGE 2: COURSE ADMISSION ===
elif menu == "📝 Course Admission":
    st.title("📝 Student Admission Form")
    st.caption("Please complete the form below to enroll for online live classes. Our team will contact you shortly via WhatsApp.")

    all_options = [c["title"] for c in SPECIAL_COMBOS] + [c["title"] for c in O_LEVEL_COURSES]

    with st.form("admission_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Student's Full Name *", placeholder="e.g. Ali Ahmed")
            email = st.text_input("Parent / Student Email Address *", placeholder="e.g. parent@example.com")
        with col_b:
            phone = st.text_input("WhatsApp Number (for class updates) *", placeholder="e.g. +92 332 1234567")
            selected_course = st.selectbox("Select Target Course / Combo *", all_options)
        
        submitted = st.form_submit_button("Submit Online Enrollment")

        if submitted:
            if not name or not phone or not email:
                st.error("Please fill in all required fields.")
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
                st.success(f"Thank you, {name}! Your admission request for {selected_course} has been received. We will send class joining details to {norm_phone} via WhatsApp shortly.")

# === PAGE 3: CHAT ASSISTANT ===
elif menu == "🤖 Chat Assistant":
    st.title("🤖 Online Academy Assistant")
    st.caption("Have questions about subject syllabus, online schedules, combo fee packages, or exam preparation strategies? Ask our assistant below!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask about online live classes, combo fees, subjects, or past paper practice..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

# === PAGE 4: ADMIN DASHBOARD ===
elif menu == "🔒 Admin Dashboard":
    st.title("🔒 Administration Portal")
    pwd = st.sidebar.text_input("Admin Security Password", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.success("Authorized Access Granted")
        tab1, tab2 = st.tabs(["Student Registrations", "Subject Catalog"])
        
        with tab1:
            st.subheader("Submitted Admission Requests")
            enrollments = load_json("enrollments.json", [])
            if enrollments:
                df = pd.DataFrame(enrollments)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No enrollment submissions found.")
                
        with tab2:
            st.subheader("Active O Level / IGCSE Subjects & Combos")
            courses = load_json("courses.json", [])
            st.json(courses)
    else:
        st.warning("Please enter your admin credentials to access registered student records.")
