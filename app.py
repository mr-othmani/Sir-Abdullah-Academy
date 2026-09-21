import streamlit as st
import pandas as pd
from models import load_json, save_json
from utils import normalize_phone, sanitize_csv_field
from chatbot import get_bot_response
from github_store import sync_to_github

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="Sir Abdullah Academy | Online O Level & IGCSE Coaching",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MODERN ACADEMY STYLING ---
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

    .hero-banner {
        background: linear-gradient(135deg, #1e1b4b 0%, #311b92 50%, #0f172a 100%);
        border: 1px solid #3730a3;
        border-radius: 16px;
        padding: 3.5rem 2rem;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(49, 27, 146, 0.3);
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.8rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #c7d2fe;
        max-width: 750px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }

    .feature-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem 1rem;
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        border-color: #6366f1;
        transform: translateY(-4px);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
    }
    .feature-desc {
        font-size: 0.85rem;
        color: #94a3b8;
    }

    .course-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .course-badge {
        background: #312e81;
        color: #a5b4fc;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.25rem 0.6rem;
        border-radius: 20px;
        text-transform: uppercase;
    }
    .course-fee {
        color: #34d399;
        font-size: 1.2rem;
        font-weight: 800;
    }

    .stButton>button {
        background: linear-gradient(90deg, #4f46e5 0%, #6366f1 100%);
        color: white;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 0.7rem 1.5rem;
        width: 100%;
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

# --- 3. COURSES LISTING ---
O_LEVEL_COURSES = [
    {
        "title": "O Level / IGCSE Computer Science",
        "icon": "💻",
        "badge": "CAIE 2210 / 0478",
        "fee": "PKR 12,000 / mo",
        "duration": "Online Live Classes",
        "desc": "Comprehensive live interactive classes covering theory (hardware, logic gates, networking) and Paper 2 problem-solving, pseudocode, and algorithm design.",
        "highlights": ["Past Paper Practice (2015-2025)", "Pseudocode Mastery", "Paper 1 & 2 Exam Techniques"]
    },
    {
        "title": "O Level / IGCSE Mathematics",
        "icon": "📐",
        "badge": "CAIE 4024 / 0580",
        "fee": "PKR 12,000 / mo",
        "duration": "Online Live Classes",
        "desc": "In-depth online coaching in Algebra, Trigonometry, Vectors, Calculus basics, Mensuration, and Probability with live topical past paper drills.",
        "highlights": ["Topical Worksheets", "Step-by-Step Marking Schemes", "Timed Online Mocks"]
    },
    {
        "title": "O Level / IGCSE Physics",
        "icon": "⚡",
        "badge": "CAIE 5054 / 0625",
        "fee": "PKR 12,000 / mo",
        "duration": "Online Live Classes",
        "desc": "Complete online syllabus coverage: General Physics, Thermal Physics, Waves, Electricity & Magnetism, Atomic Physics, and ATP (Paper 4) preparation.",
        "highlights": ["Formula Memorization Guides", "ATP Practical Skills", "MCQ Solving Strategies"]
    },
    {
        "title": "O Level / IGCSE Chemistry",
        "icon": "🧪",
        "badge": "CAIE 5070 / 0620",
        "fee": "PKR 12,000 / mo",
        "duration": "Online Live Classes",
        "desc": "Master Stoichiometry, Organic Chemistry, Chemical Energetics, Electrochemistry, and Alternative to Practical (ATP) exam preparation via live interactive sessions.",
        "highlights": ["Stoichiometry Problem Drills", "Organic Chem Roadmap", "ATP Exam Prep"]
    },
    {
        "title": "O Level / IGCSE Biology",
        "icon": "🧬",
        "badge": "CAIE 5090 / 0610",
        "fee": "PKR 12,000 / mo",
        "duration": "Online Live Classes",
        "desc": "Cell Biology, Plant & Human Physiology, Genetics, Biotechnology, and Ecological concepts tailored precisely to Cambridge standards with digital notes.",
        "highlights": ["Diagram & Key Phrase Drills", "Marking Scheme Keyword Focus", "Past Papers"]
    },
    {
        "title": "O Level / IGCSE Islamiat",
        "icon": "🕌",
        "badge": "CAIE 2058 / 0493",
        "fee": "PKR 10,000 / mo",
        "duration": "Online Live Classes",
        "desc": "Paper 1 & Paper 2 breakdown: Quranic Passages, Life of Prophet (PBUH), Rightly Guided Caliphs, Hadiths, and Articles of Faith with digital study packs.",
        "highlights": ["Structured References & Quotes", "14-mark & 4-mark Answer Formatting", "Topical Mocks"]
    },
    {
        "title": "O Level / IGCSE Pakistan Studies (PST)",
        "icon": "🇵🇰",
        "badge": "CAIE 2059 / 0448",
        "fee": "PKR 10,000 / mo",
        "duration": "Online Live Classes",
        "desc": "History of Pakistan (Paper 1) and Environment / Geography of Pakistan (Paper 2) with detailed focus on high-scoring answer structures.",
        "highlights": ["Chronological History Timelines", "Map Skills for Geography", "High-Scoring Answer Structures"]
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
    <div style="background: #1e293b; padding: 1rem; border-radius: 10px; border: 1px solid #334155;">
        <p style="color: #ffffff; font-weight: 700; margin-bottom: 0.3rem;">💻 Class Format</p>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">100% Online Live Classes (Zoom / Google Meet)</p>
        <hr style="border-color: #334155; margin: 0.6rem 0;">
        <p style="color: #ffffff; font-weight: 700; margin-bottom: 0.3rem;">📞 Contact & Enquiries</p>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">WhatsApp: +92 332 1234567</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. PAGE ROUTING ---

# === PAGE 1: ACADEMY HOME ===
if menu == "🏠 Academy Home":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Sir Abdullah Academy</div>
        <div class="hero-subtitle">Premier 100% Online O Level & IGCSE Coaching. Live interactive sessions, topical past paper practice, and dedicated Cambridge exam preparation worldwide.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <div class="feature-title">Live Interactive Classes</div>
            <div class="feature-desc">Learn from home via live interactive online sessions.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">Topical Past Papers</div>
            <div class="feature-desc">10+ years of solved past papers & marking schemes.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">A* Exam Techniques</div>
            <div class="feature-desc">Learn Cambridge examiner keywords & answer structuring.</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Regular Online Mocks</div>
            <div class="feature-desc">Weekly assessments and realistic mock examination series.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><h2 style='text-align: center; color: white;'>O Level & IGCSE Online Courses Offered</h2><br>", unsafe_allow_html=True)

    for course in O_LEVEL_COURSES:
        col_main, col_side = st.columns([3, 1])
        with col_main:
            st.markdown(f"""
            <div class="course-card">
                <span class="course-badge">{course['badge']}</span>
                <h3 style="color: white; margin-top: 0.5rem; margin-bottom: 0.5rem;">{course['icon']} {course['title']}</h3>
                <p style="color: #94a3b8; font-size: 0.95rem;">{course['desc']}</p>
                <p style="color: #cbd5e1; font-size: 0.85rem; font-weight: 600;">Focus Points: {', '.join(course['highlights'])}</p>
            </div>
            """, unsafe_allow_html=True)
        with col_side:
            st.markdown(f"""
            <div class="course-card" style="text-align: center;">
                <p style="color: #94a3b8; margin: 0; font-size: 0.85rem;">Monthly Fee</p>
                <p class="course-fee">{course['fee']}</p>
                <p style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0;">⏱️ {course['duration']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("💡 **Ready to enroll?** Select **Course Admission** from the sidebar to register!")

# === PAGE 2: COURSE ADMISSION ===
elif menu == "📝 Course Admission":
    st.title("📝 Online Admission Application")
    st.caption("Select your subject(s) to reserve your seat for the upcoming online batch.")

    courses = load_json("courses.json", [])
    active_courses = [c["title"] for c in courses if c.get("active", True)]

    if not active_courses:
        # Fallback list if json is empty
        active_courses = [c["title"] for c in O_LEVEL_COURSES]

    with st.form("admission_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Student Full Name *")
            email = st.text_input("Email Address *")
        with col_b:
            phone = st.text_input("WhatsApp / Mobile Number * (e.g. +923321234567)")
            selected_course = st.selectbox("Select Subject / Course *", active_courses)
        
        submitted = st.form_submit_button("Submit Online Application")

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
                st.success(f"Application submitted! Thank you, {name}. We will contact you on WhatsApp with class access links shortly.")

# === PAGE 3: CHAT ASSISTANT ===
elif menu == "🤖 Chat Assistant":
    st.title("🤖 Academy Assistant")
    st.caption("Ask questions about online live classes, O Level / IGCSE subjects, fees, past paper practice, or class timings.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask about online classes, subjects, fees, past papers..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

# === PAGE 4: ADMIN DASHBOARD ===
elif menu == "🔒 Admin Dashboard":
    st.title("🔒 Admin Dashboard")
    pwd = st.sidebar.text_input("Admin Password", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.success("Authenticated")
        tab1, tab2 = st.tabs(["Enrollments Log", "Course Catalog"])
        
        with tab1:
            st.subheader("Submitted Enrollments")
            enrollments = load_json("enrollments.json", [])
            if enrollments:
                df = pd.DataFrame(enrollments)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No enrollments submitted yet.")
                
        with tab2:
            st.subheader("O Level Subject List")
            courses = load_json("courses.json", [])
            st.json(courses)
    else:
        st.warning("Enter valid password in the sidebar to access admin logs.")
