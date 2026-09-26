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
    initial_sidebar_state="collapsed"  # Collapsed by default for clean web layout
)

# --- 2. IVY-STYLE LIGHT THEMING & CSS ---
st.markdown("""
<style>
    /* Hide Streamlit Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Background with Soft Lavender Glow */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #f3e8ff 0%, #f8fafc 45%, #f1f5f9 100%);
        color: #0f172a;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Top Navigation Header */
    .ivy-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #ffffff;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        margin-bottom: 2.5rem;
        border: 1px solid #f1f5f9;
    }
    .ivy-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 900;
        font-size: 1.3rem;
        color: #4c1d95;
    }
    .brand-circle {
        background: #6d28d9;
        color: #ffffff;
        width: 42px;
        height: 42px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.1rem;
    }

    /* Floating Pill Badge */
    .floating-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #ffffff;
        color: #475569;
        font-size: 0.82rem;
        font-weight: 700;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.2rem;
    }

    /* Large Ivy Hero Typography */
    .ivy-hero-heading {
        font-size: 3.4rem;
        font-weight: 900;
        color: #0f172a;
        line-height: 1.15;
        letter-spacing: -1px;
        margin-bottom: 1rem;
    }
    .highlight-purple {
        color: #6d28d9;
    }
    .highlight-gold {
        color: #d97706;
    }
    .ivy-hero-subtext {
        font-size: 1.15rem;
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 1.8rem;
    }

    /* Device / App Showcase Box */
    .device-mockup-container {
        position: relative;
        background: #ffffff;
        border-radius: 28px;
        padding: 1.5rem;
        box-shadow: 0 20px 40px rgba(109, 40, 217, 0.12);
        border: 2px solid #f1f5f9;
        text-align: center;
    }
    .floating-result-tag {
        position: absolute;
        top: -15px;
        right: 15px;
        background: #ffffff;
        color: #0f172a;
        font-size: 0.8rem;
        font-weight: 800;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }

    /* Light Theme Cards */
    .ivy-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 1.8rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        border: 1px solid #f1f5f9;
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .ivy-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(109, 40, 217, 0.08);
        border-color: #ddd6fe;
    }
    .ivy-combo-card {
        background: linear-gradient(135deg, #ffffff 0%, #faf5ff 100%);
        border-radius: 20px;
        padding: 1.8rem;
        box-shadow: 0 6px 20px rgba(109, 40, 217, 0.08);
        border: 2px solid #c084fc;
        height: 100%;
    }
    .tag-purple {
        background: #f3e8ff;
        color: #7e22ce;
        font-weight: 800;
        font-size: 0.72rem;
        padding: 0.3rem 0.8rem;
        border-radius: 50px;
        text-transform: uppercase;
    }
    .tag-gold {
        background: #fef3c7;
        color: #b45309;
        font-weight: 800;
        font-size: 0.72rem;
        padding: 0.3rem 0.8rem;
        border-radius: 50px;
        text-transform: uppercase;
    }
    .price-text {
        font-size: 1.4rem;
        font-weight: 900;
        color: #6d28d9;
    }

    /* Buttons Override */
    .stButton>button {
        background: #fbbf24 !important;
        color: #0f172a !important;
        font-weight: 800 !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background: #f59e0b !important;
        transform: scale(1.02);
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
        "desc": "Complete 4-subject package for Biology, Physics, Chemistry, and Mathematics. Includes complete syllabus, topical solved papers, and ATP prep.",
        "highlights": ["Save PKR 4,000/mo", "Full 4-Subject Coverage", "Weekly Mocks & Topical Papers"]
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

# --- 4. TOP NAVIGATION BAR (IVY STYLE) ---
st.markdown("""
<div class="ivy-navbar">
    <div class="ivy-brand">
        <div class="brand-circle">SAA</div>
        <span>Sir Abdullah Academy</span>
    </div>
    <div style="color: #64748b; font-size: 0.9rem; font-weight: 600;">
        📍 Live Cambridge O & A Level Online Prep
    </div>
</div>
""", unsafe_allow_html=True)

# Main Section Switcher
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 1])
with nav_col1:
    btn_home = st.button("🏠 Home", use_container_width=True)
with nav_col2:
    btn_courses = st.button("📚 Courses & Pricing", use_container_width=True)
with nav_col3:
    btn_admission = st.button("📝 Direct Admission", use_container_width=True)
with nav_col4:
    btn_assistant = st.button("🤖 AI Assistant", use_container_width=True)

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"

if btn_home:
    st.session_state.active_tab = "Home"
elif btn_courses:
    st.session_state.active_tab = "Courses"
elif btn_admission:
    st.session_state.active_tab = "Admission"
elif btn_assistant:
    st.session_state.active_tab = "Assistant"

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. PAGE CONTROLLER ---

# PAGE: HOME & HERO
if st.session_state.active_tab == "Home":
    hero_left, hero_right = st.columns([1.3, 1])

    with hero_left:
        st.markdown("""
        <div class="floating-badge">⭐ Every Lesson Counts</div>
        <div class="ivy-hero-heading">
            Pakistan's <span class="highlight-purple">#1 Online Platform</span> for <span class="highlight-gold">O & A Level Success</span>
        </div>
        <div class="ivy-hero-subtext">
            High-quality interactive live classes, topical solved past papers, examiner keyword mastery, and expert teachers — designed to guarantee top A* grades.
        </div>
        """, unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 Explore Courses Now", use_container_width=True):
                st.session_state.active_tab = "Courses"
                st.rerun()
        with col_btn2:
            if st.button("📝 Apply for Admission", use_container_width=True):
                st.session_state.active_tab = "Admission"
                st.rerun()

    with hero_right:
        st.markdown("""
        <div class="device-mockup-container">
            <div class="floating-result-tag">🎗️ 10,000+ A* Results</div>
            <div style="background: linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%); padding: 2.5rem 1.5rem; border-radius: 20px; color: white;">
                <h2 style="font-weight: 900; margin-bottom: 0.5rem; color: #fbbf24;">NOW STUDY ONLINE</h2>
                <p style="font-size: 0.95rem; opacity: 0.9;">Join Live Zoom & Google Meet Classes with Sir Abdullah</p>
                <div style="background: rgba(255,255,255,0.15); padding: 1rem; border-radius: 12px; margin-top: 1.5rem; backdrop-filter: blur(8px);">
                    <p style="margin: 0; font-weight: 700; font-size: 0.9rem;">📚 Interactive Whiteboards</p>
                    <p style="margin: 0; font-weight: 700; font-size: 0.9rem; margin-top: 0.4rem;">📑 10+ Yrs Topical Solved Papers</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color: #e2e8f0;'><br>", unsafe_allow_html=True)

    # Feature Highlights Grid
    st.markdown("<h2 style='text-align: center; font-weight: 900; margin-bottom: 2rem;'>Why Students Choose Sir Abdullah Academy</h2>", unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("💻", "Live Interactive Classes", "Engage directly with expert faculty with immediate doubt resolution."),
        ("📝", "Topical Past Papers", "10+ years of topical past paper practice aligned with CAIE marking schemes."),
        ("🎯", "Keyword Mastery", "Learn subject-specific keywords required for full marks in exam papers."),
        ("📊", "Parent Tracking", "Regular attendance updates, test feedback, and personal performance reports.")
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(f"""
            <div class="ivy-card" style="text-align: center;">
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">{icon}</div>
                <h4 style="font-weight: 800; color: #0f172a; margin-bottom: 0.4rem;">{title}</h4>
                <p style="font-size: 0.85rem; color: #64748b; line-height: 1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# PAGE: COURSES & PRICING
elif st.session_state.active_tab == "Courses":
    st.markdown("<h2 style='text-align: center; font-weight: 900; margin-bottom: 0.5rem;'>O Level & IGCSE Course Offerings</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 2rem;'>Filter by subject category or search for your required subject.</p>", unsafe_allow_html=True)

    # Filter Bar
    f_col1, f_col2 = st.columns([2, 1])
    with f_col1:
        cat_filter = st.radio("Category Filter", ["All", "Combos", "Sciences", "Humanities"], horizontal=True, label_visibility="collapsed")
    with f_col2:
        search_txt = st.text_input("Search subject...", placeholder="e.g. Physics or Pre-Medical", label_visibility="collapsed")

    # Filter Logic
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
        card_style = "ivy-combo-card" if item["is_combo"] else "ivy-card"
        badge_style = "tag-gold" if item["is_combo"] else "tag-purple"

        with c_img:
            st.image(item["image_url"], use_container_width=True)
        with c_main:
            st.markdown(f"""
            <div class="{card_style}">
                <span class="{badge_style}">{item['badge']}</span>
                <h3 style="font-weight: 800; color: #0f172a; margin-top: 0.5rem; margin-bottom: 0.4rem;">{item['title']}</h3>
                <p style="color: #475569; font-size: 0.9rem; line-height: 1.5; margin-bottom: 0.8rem;">{item['desc']}</p>
                <p style="color: #6d28d9; font-size: 0.82rem; font-weight: 700;">Highlights: {', '.join(item['highlights'])}</p>
            </div>
            """, unsafe_allow_html=True)
        with c_side:
            st.markdown(f"""
            <div class="{card_style}" style="text-align: center;">
                <p style="color: #64748b; font-size: 0.8rem; font-weight: 700; margin: 0;">Monthly Tuition Fee</p>
                <div class="price-text">{item['fee']}</div>
                <p style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 1rem;">⏱️ {item['duration']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Enroll in {item['id']}", key=f"btn_enroll_{item['id']}", use_container_width=True):
                st.session_state.selected_course_for_enrollment = item['title']
                st.session_state.active_tab = "Admission"
                st.rerun()

# PAGE: ADMISSION
elif st.session_state.active_tab == "Admission":
    st.markdown("<h2 style='text-align: center; font-weight: 900; margin-bottom: 0.5rem;'>📝 Online Admission Form</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 2rem;'>Fill out your details to reserve your seat in the upcoming online batch.</p>", unsafe_allow_html=True)

    all_options = [c["title"] for c in SPECIAL_COMBOS] + [c["title"] for c in O_LEVEL_COURSES]
    default_idx = 0
    if st.session_state.selected_course_for_enrollment in all_options:
        default_idx = all_options.index(st.session_state.selected_course_for_enrollment)

    with st.form("ivy_admission_form", clear_on_submit=True):
        a1, a2 = st.columns(2)
        with a1:
            name = st.text_input("Student's Full Name *", placeholder="e.g. Ali Ahmed")
            email = st.text_input("Parent / Student Email *", placeholder="e.g. parent@example.com")
        with a2:
            phone = st.text_input("WhatsApp Number *", placeholder="e.g. +92 332 1234567")
            selected_course = st.selectbox("Select Target Course / Combo *", all_options, index=default_idx)

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
                st.success(f"Application submitted successfully for **{name}**! Class details will be sent to **{norm_phone}** via WhatsApp.")

# PAGE: AI ASSISTANT
elif st.session_state.active_tab == "Assistant":
    st.markdown("<h2 style='text-align: center; font-weight: 900; margin-bottom: 0.5rem;'>🤖 AI Learning Assistant</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 2rem;'>Ask questions about course syllabi, fee structures, or past paper strategy.</p>", unsafe_allow_html=True)

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

# ADMIN PANEL FOOTER TRIGGER
st.markdown("<br><hr style='border-color: #e2e8f0;'><br>", unsafe_allow_html=True)
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
