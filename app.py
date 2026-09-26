import streamlit as st
import pandas as pd
import re
from models import load_json, save_json
from utils import normalize_phone, sanitize_csv_field
from chatbot import get_bot_response
from github_store import sync_to_github

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="Sir Abdullah Academy | Premier Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED COMMERCIAL STYLING ---
st.markdown("""
<style>
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* App Base Background */
    .stApp {
        background: #070a12;
        color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Sidebar Refinements */
    [data-testid="stSidebar"] {
        background-color: #0b1120 !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        color: #e2e8f0 !important;
        font-weight: 500;
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: #1e293b;
    }

    /* Modern Top App Header */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1.5rem;
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid #1e293b;
        border-radius: 16px;
        margin-bottom: 2rem;
    }
    .brand-title {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Hero Banner with Glass Effect */
    .hero-banner {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(49, 27, 146, 0.5) 50%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }
    .hero-badge {
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        border: 1px solid #6366f1;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 0.4rem 1.2rem;
        border-radius: 9999px;
        display: inline-block;
        margin-bottom: 1.2rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        max-width: 750px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }

    /* Stat Cards */
    .stat-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .stat-card:hover {
        border-color: #38bdf8;
        transform: translateY(-2px);
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 800;
        color: #38bdf8;
    }
    .stat-label {
        font-size: 0.82rem;
        color: #94a3b8;
        font-weight: 600;
    }

    /* Feature Cards */
    .feature-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 1.5rem 1rem;
        text-align: center;
        height: 100%;
        transition: border-color 0.2s ease;
    }
    .feature-card:hover {
        border-color: #6366f1;
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.4rem;
    }
    .feature-desc {
        font-size: 0.82rem;
        color: #94a3b8;
        line-height: 1.4;
    }

    /* Course Cards */
    .course-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .combo-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 1.5px solid #6366f1;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.2);
    }
    .course-badge {
        background: #312e81;
        color: #a5b4fc;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        text-transform: uppercase;
    }
    .combo-badge {
        background: #4f46e5;
        color: #ffffff;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        text-transform: uppercase;
    }
    .course-fee {
        color: #34d399;
        font-size: 1.3rem;
        font-weight: 800;
    }

    [data-testid="stImage"] img {
        border-radius: 12px;
        border: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIG & DATA ---
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "osmanibhai112233")

SPECIAL_COMBOS = [
    {
        "id": "combo_med",
        "title": "The Pre-Medical Combo (Bio, Physics, Chem, Math)",
        "image_url": "assets/pre_medical_combo_logo.png",
        "badge": "PRE-MEDICAL SPECIAL BUNDLE",
        "fee": "PKR 16,000 / mo",
        "category": "Combos",
        "duration": "Online Live Classes",
        "desc": "Complete 4-subject package covering Biology, Physics, Chemistry, and Mathematics. Includes intensive syllabus coverage, topical past papers, and ATP exam preparation.",
        "highlights": ["Save PKR 4,000/mo vs individual enrolment", "Full coverage of Bio, Physics, Chemistry & Math", "Weekly Mocks & Topical Past Paper Drills"]
    },
    {
        "id": "combo_cs",
        "title": "The Computer Science Combo (CS, Physics, Chem, Math)",
        "image_url": "assets/cs_combo_logo.png",
        "badge": "PRE-ENGINEERING & CS BUNDLE",
        "fee": "PKR 16,000 / mo",
        "category": "Combos",
        "duration": "Online Live Classes",
        "desc": "Complete 4-subject package designed for future Engineers & Tech students: Computer Science, Physics, Chemistry, and Mathematics. Focuses on Pseudocode, Logic Gates & ATPs.",
        "highlights": ["Save PKR 4,000/mo vs individual enrolment", "Full coverage of CS, Physics, Chem & Math", "Logic Drills, Code Practice & Marking Scheme Mastery"]
    },
    {
        "id": "combo_core",
        "title": "O1 / O2 Core Appearing Combo (Islamiat + PST)",
        "image_url": "assets/core_combo_logo.png",
        "badge": "CORE SUBJECTS BUNDLE",
        "fee": "PKR 4,500 / mo",
        "category": "Combos",
        "duration": "Online Live Classes",
        "desc": "Complete dual-subject bundle for early appearing O Level / IGCSE subjects (Islamiat 2058 / PST 2059). Covers full Paper 1 & Paper 2 syllabus with structured exam notes.",
        "highlights": ["Save PKR 500/mo vs individual enrolment", "Full coverage of Islamiat, History & Geography", "Topical Past Paper Revision & Mock Exams"]
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
        "desc": "Master Theory (Hardware, Logic Gates, Data Transmission) & Paper 2 Problem Solving. Comprehensive practice in Pseudocode, Flowcharts, and Algorithm Design.",
        "highlights": ["10+ Years Past Paper Practice", "Pseudocode & Logic Drills", "Marking Scheme Mastery"]
    },
    {
        "id": "math",
        "title": "O Level / IGCSE Mathematics",
        "image_url": "assets/math_logo.png",
        "badge": "CAIE 4024 / 0580",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "desc": "Clear step-by-step conceptual learning across Algebra, Trigonometry, Vectors, Mensuration, and Probability with intensive exam-style problem solving.",
        "highlights": ["Topical Worksheets & Solutions", "Exam Speed & Accuracy Drills", "Regular Assessment Tests"]
    },
    {
        "id": "phy",
        "title": "O Level / IGCSE Physics",
        "image_url": "assets/physics_logo.png",
        "badge": "CAIE 5054 / 0625",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "desc": "In-depth physics coverage: Mechanics, Thermal Physics, Waves, Electricity & Magnetism, Space Physics, and ATP (Paper 4) exam techniques.",
        "highlights": ["Formula Memorization Sheets", "ATP Practical Exam Prep", "MCQ Paper 1 Strategies"]
    },
    {
        "id": "chem",
        "title": "O Level / IGCSE Chemistry",
        "image_url": "assets/chemistry_logo.png",
        "badge": "CAIE 5070 / 0620",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "desc": "Build deep clarity in Stoichiometry, Organic Chemistry, Chemical Energetics, and Electrochemistry combined with dedicated ATP Paper preparation.",
        "highlights": ["Stoichiometry Problem Drills", "Organic Chemistry Flowcharts", "ATP Practical Exam Prep"]
    },
    {
        "id": "bio",
        "title": "O Level / IGCSE Biology",
        "image_url": "assets/biology_logo.png",
        "badge": "CAIE 5090 / 0610",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "desc": "Cell Biology, Plant Physiology, Genetics, Biotechnology, and Human Systems taught with precise examiner keywords to ensure maximum marks.",
        "highlights": ["Examiner Keywords Focus", "Diagram & Function Practice", "Past Paper Revision Packs"]
    },
    {
        "id": "isl",
        "title": "O Level / IGCSE Islamiat",
        "image_url": "assets/islamiat_logo.png",
        "badge": "CAIE 2058 / 0493",
        "fee": "PKR 2,500 / mo",
        "category": "Humanities",
        "duration": "Online Live Classes",
        "desc": "Structured preparation for Paper 1 & Paper 2: Quranic Passages, Life of Prophet (PBUH), Caliphates, Hadiths, and Articles of Faith with ready-to-learn notes.",
        "highlights": ["14-Mark & 4-Mark Structured Outlines", "Quranic & Hadith References", "Topical Exam Practice"]
    },
    {
        "id": "pst",
        "title": "O Level / IGCSE PST (Pakistan Studies)",
        "image_url": "assets/pst_logo.png",
        "badge": "CAIE 2059 / 0448",
        "fee": "PKR 2,500 / mo",
        "category": "Humanities",
        "duration": "Online Live Classes",
        "desc": "Complete coverage of Paper 1 (History & Culture) and Paper 2 (Environment of Pakistan). Features level-of-response answer templates, maps, and case studies.",
        "highlights": ["Chronological Timelines & Templates", "Geography Map Skills & Case Studies", "Topical Source-Based Questions"]
    }
]

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

if "selected_course_for_enrollment" not in st.session_state:
    st.session_state.selected_course_for_enrollment = SPECIAL_COMBOS[0]["title"]

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🎓 Sir Abdullah Academy")
    st.caption("Cambridge O Level & IGCSE Platform")
    st.markdown("---")
    
    menu = st.radio(
        "Navigation",
        ["🏠 Academy Portal", "📝 Instant Admission", "🤖 AI Tutor Assistant", "🔒 Admin Control"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style="background: #0f172a; padding: 1rem; border-radius: 12px; border: 1px solid #1e293b;">
        <p style="color: #38bdf8; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.3rem;">⚡ Next Session Starting</p>
        <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Live Interactive Batches via Zoom / Meet.</p>
        <hr style="border-color: #1e293b; margin: 0.6rem 0;">
        <p style="color: #ffffff; font-size: 0.8rem; font-weight: 600; margin: 0;">💬 WhatsApp Inquiry</p>
        <p style="color: #38bdf8; font-size: 0.85rem; font-weight: 700; margin: 0;">+92 332 1234567</p>
    </div>
    """, unsafe_allow_html=True)

# Top Application Bar
st.markdown("""
<div class="app-header">
    <div class="brand-title">🎓 Sir Abdullah Academy</div>
    <div style="color: #94a3b8; font-size: 0.85rem; font-weight: 500;">O Level & IGCSE Live Coaching</div>
</div>
""", unsafe_allow_html=True)

# --- 5. ROUTE CONTROLLERS ---

# PAGE 1: ACADEMY PORTAL
if menu == "🏠 Academy Portal":
    st.markdown("""
    <div class="hero-banner">
        <span class="hero-badge">✨ ADMISSIONS OPEN • SESSION 2026</span>
        <div class="hero-title">Premier Cambridge O Level & IGCSE Coaching</div>
        <div class="hero-subtitle">Master core concepts, master past paper marking schemes, and learn proven examiner techniques to secure top A* grades.</div>
    </div>
    """, unsafe_allow_html=True)

    # Key Metrics
    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        ("100%", "Interactive Live Classes"),
        ("10+ Yrs", "Topical Past Paper Practice"),
        ("A* Focused", "Cambridge Examiner Methods"),
        ("Small Groups", "Personalized Attention & Mocks")
    ]
    for col, (num, label) in zip([m1, m2, m3, m4], metrics):
        with col:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{num}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Features
    c1, c2, c3, c4 = st.columns(4)
    features = [
        ("💻", "Live & Interactive", "Real-time doubt resolution, digital whiteboards & recorded sessions."),
        ("📄", "Topical Past Papers", "Rigorous practice aligned directly with official CAIE marking schemes."),
        ("🎯", "Keyword Mastery", "Learn subject-specific terminology required for top marks."),
        ("📊", "Parent Reporting", "Regular testing, homework feedback, and performance monitoring.")
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><h2 style='text-align: center; color: white;'>Course Catalog & Special Bundles</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 1.5rem;'>Filter by subject category or search for specific subjects below.</p>", unsafe_allow_html=True)

    # Interactive Filter Bar
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        category_tab = st.radio("Category Filter", ["All", "Combos", "Sciences", "Humanities"], horizontal=True, label_visibility="collapsed")
    with filter_col2:
        search_query = st.text_input("Search courses...", placeholder="e.g. Physics or Combo", label_visibility="collapsed")

    # Filter Data Logic
    all_courses_combined = []
    for c in SPECIAL_COMBOS:
        all_courses_combined.append({**c, "is_combo": True})
    for c in O_LEVEL_COURSES:
        all_courses_combined.append({**c, "is_combo": False})

    filtered_list = all_courses_combined
    if category_tab != "All":
        filtered_list = [c for c in filtered_list if c["category"] == category_tab]
    if search_query:
        filtered_list = [c for c in filtered_list if search_query.lower() in c["title"].lower() or search_query.lower() in c["desc"].lower()]

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Filtered List
    if not filtered_list:
        st.info("No courses match your current search/filter criteria.")
    else:
        for item in filtered_list:
            col_img, col_main, col_side = st.columns([1.2, 2.5, 1.1])
            card_class = "combo-card" if item["is_combo"] else "course-card"
            badge_class = "combo-badge" if item["is_combo"] else "course-badge"

            with col_img:
                st.image(item['image_url'], use_container_width=True)
            with col_main:
                st.markdown(f"""
                <div class="{card_class}">
                    <span class="{badge_class}">{item['badge']}</span>
                    <h3 style="color: white; margin-top: 0.6rem; margin-bottom: 0.5rem;">{item['title']}</h3>
                    <p style="color: #c7d2fe if item['is_combo'] else #94a3b8; font-size: 0.9rem; line-height: 1.5;">{item['desc']}</p>
                    <p style="color: #38bdf8; font-size: 0.82rem; font-weight: 700;">Key Features: {', '.join(item['highlights'])}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_side:
                st.markdown(f"""
                <div class="{card_class}" style="text-align: center;">
                    <p style="color: #a5b4fc; margin: 0; font-size: 0.8rem; font-weight: 700;">Tution Fee</p>
                    <p class="course-fee">{item['fee']}</p>
                    <p style="color: #cbd5e1; font-size: 0.8rem; margin-bottom: 1rem;">⏱️ {item['duration']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Immediate CTA Action
                if st.button(f"Enroll in {item['id']}", key=f"btn_{item['id']}", use_container_width=True):
                    st.session_state.selected_course_for_enrollment = item['title']
                    st.info(f"Selected **{item['title']}**. Please open 'Instant Admission' from the sidebar menu to submit your details!")

# PAGE 2: INSTANT ADMISSION
elif menu == "📝 Instant Admission":
    st.title("📝 Student Admission Portal")
    st.caption("Complete the form below to reserve a seat for online live classes.")

    all_options = [c["title"] for c in SPECIAL_COMBOS] + [c["title"] for c in O_LEVEL_COURSES]
    
    # Pre-select course from home page CTA
    default_index = 0
    if st.session_state.selected_course_for_enrollment in all_options:
        default_index = all_options.index(st.session_state.selected_course_for_enrollment)

    with st.form("admission_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Student's Full Name *", placeholder="e.g. Ali Ahmed")
            email = st.text_input("Parent / Student Email *", placeholder="e.g. parent@example.com")
        with col_b:
            phone = st.text_input("WhatsApp Phone *", placeholder="e.g. +92 332 1234567")
            selected_course = st.selectbox("Selected Course / Combo *", all_options, index=default_index)
        
        submitted = st.form_submit_button("Submit Application")

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
                st.success(f"Application submitted successfully for **{name}** ({selected_course})! Class details will be sent to {norm_phone} via WhatsApp.")

# PAGE 3: CHAT ASSISTANT
elif menu == "🤖 AI Tutor Assistant":
    st.title("🤖 Online AI Learning Assistant")
    st.caption("Ask questions about course syllabi, class schedules, or exam preparation tips.")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you with O Level / IGCSE prep or course details today?"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask about classes, fee structures, or past paper practice..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

# PAGE 4: ADMIN CONTROL
elif menu == "🔒 Admin Control":
    st.title("🔒 Administration Portal")
    pwd = st.sidebar.text_input("Admin Password", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.success("Authenticated Successfully")
        tab1, tab2 = st.tabs(["Student Applications", "Course Catalog JSON"])
        
        with tab1:
            enrollments = load_json("enrollments.json", [])
            if enrollments:
                df = pd.DataFrame(enrollments)
                st.subheader(f"Total Applications Received: {len(df)}")
                st.dataframe(df, use_container_width=True)
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Registrations (CSV)",
                    data=csv,
                    file_name="enrollments_export.csv",
                    mime="text/csv"
                )
            else:
                st.info("No enrollment submissions found.")
                
        with tab2:
            courses = load_json("courses.json", [])
            st.json(courses)
    elif pwd:
        st.error("Invalid credentials provided.")
    else:
        st.warning("Please enter your admin credentials in the sidebar.")
