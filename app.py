import streamlit as st
import pandas as pd
import re
from models import load_json, save_json
from utils import normalize_phone, sanitize_csv_field
from chatbot import get_bot_response
from github_store import sync_to_github

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sir Abdullah Academy | Premier O Level & IGCSE Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. COMMERCIAL UI STYLING ---
st.markdown("""
<style>
    /* Dark Modern Commercial Theme */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }

    /* Hero Section */
    .hero-banner {
        background: linear-gradient(135deg, #1e1b4b 0%, #311b92 50%, #0f172a 100%);
        border: 1px solid #4338ca;
        border-radius: 20px;
        padding: 3.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
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
        font-size: 1.15rem;
        color: #94a3b8;
        max-width: 750px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }

    /* Stat Cards */
    .stat-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }
    .stat-number {
        font-size: 1.75rem;
        font-weight: 800;
        color: #38bdf8;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 600;
    }

    /* Course Cards Grid */
    .card-container {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .card-container:hover {
        border-color: #6366f1;
        transform: translateY(-2px);
    }
    .card-combo {
        background: linear-gradient(180deg, #1e1b4b 0%, #1e293b 100%);
        border: 1.5px solid #6366f1;
    }
    .badge-tag {
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        text-transform: uppercase;
        width: fit-content;
        margin-bottom: 0.75rem;
    }
    .badge-primary { background: #312e81; color: #a5b4fc; }
    .badge-featured { background: #4f46e5; color: #ffffff; }

    .price-tag {
        font-size: 1.25rem;
        font-weight: 800;
        color: #34d399;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SECURE AUTH CONFIGURATION ---
# Retrieve from st.secrets if deployed, fallback for local dev
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "osmanibhai112233")

# --- 4. DATA SOURCES ---
SPECIAL_COMBOS = [
    {
        "id": "combo_med",
        "title": "The Pre-Medical Combo",
        "badge": "PRE-MEDICAL SPECIAL BUNDLE",
        "fee": "PKR 16,000 / mo",
        "desc": "Biology, Physics, Chemistry, and Mathematics. Includes intensive syllabus coverage, topical past papers, and ATP exam preparation.",
        "highlights": ["Save PKR 4,000/mo", "Bio, Physics, Chem & Math", "Weekly Mocks & Past Papers"]
    },
    {
        "id": "combo_cs",
        "title": "The Computer Science Combo",
        "badge": "PRE-ENGINEERING & CS BUNDLE",
        "fee": "PKR 16,000 / mo",
        "desc": "Computer Science, Physics, Chemistry, and Mathematics. Focuses on Pseudocode, Logic Gates, Calculations & ATPs.",
        "highlights": ["Save PKR 4,000/mo", "CS, Physics, Chem & Math", "Logic & Marking Scheme Mastery"]
    },
    {
        "id": "combo_core",
        "title": "O1 / O2 Core Appearing Combo",
        "badge": "CORE SUBJECTS BUNDLE",
        "fee": "PKR 4,500 / mo",
        "desc": "Islamiat 2058 / PST 2059 bundle covering full Paper 1 & Paper 2 syllabus with structured exam notes and past paper practice.",
        "highlights": ["Save PKR 500/mo", "Islamiat, History & Geography", "Topical Past Paper Revision"]
    }
]

O_LEVEL_COURSES = [
    {"id": "cs", "title": "O Level / IGCSE Computer Science", "code": "CAIE 2210 / 0478", "fee": "PKR 5,000 / mo"},
    {"id": "math", "title": "O Level / IGCSE Mathematics", "code": "CAIE 4024 / 0580", "fee": "PKR 5,000 / mo"},
    {"id": "phy", "title": "O Level / IGCSE Physics", "code": "CAIE 5054 / 0625", "fee": "PKR 5,000 / mo"},
    {"id": "chem", "title": "O Level / IGCSE Chemistry", "code": "CAIE 5070 / 0620", "fee": "PKR 5,000 / mo"},
    {"id": "bio", "title": "O Level / IGCSE Biology", "code": "CAIE 5090 / 0610", "fee": "PKR 5,000 / mo"},
    {"id": "isl", "title": "O Level / IGCSE Islamiat", "code": "CAIE 2058 / 0493", "fee": "PKR 2,500 / mo"},
    {"id": "pst", "title": "O Level / IGCSE Pakistan Studies", "code": "CAIE 2059 / 0448", "fee": "PKR 2,500 / mo"}
]

# --- 5. HELPER FUNCTIONS ---
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

# --- 6. SIDEBAR ROUTING ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/graduation-cap.png", width=60)
    st.title("Sir Abdullah Academy")
    
    menu = st.radio(
        "Navigation",
        ["🏠 Academy Home", "📝 Course Admission", "🤖 AI Assistant", "🔒 Admin Dashboard"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    **📞 Direct Support**  
    WhatsApp: [+92 332 1234567](https://wa.me/923321234567)  
    Email: support@sirabdullah.com  
    """)

# --- 7. ROUTE CONTROLLERS ---

# PAGE 1: HOME
if menu == "🏠 Academy Home":
    st.markdown("""
    <div class="hero-banner">
        <span class="hero-badge">🎓 Admissions Open • Session 2026</span>
        <div class="hero-title">Master Your O Level & IGCSE Exams</div>
        <div class="hero-subtitle">Interactive online coaching tailored for top grades. Learn concepts, solve past papers, and master examiner techniques.</div>
    </div>
    """, unsafe_allow_html=True)

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("100%", "Live Online Batches"),
        ("10+ Yrs", "Topical Past Papers"),
        ("A* Target", "Examiner Techniques"),
        ("1-on-1", "Doubt Resolution")
    ]
    for col, (num, label) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{num}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("### Featured Combo Bundles")
    c1, c2, c3 = st.columns(3)
    for col, combo in zip([c1, c2, c3], SPECIAL_COMBOS):
        with col:
            st.markdown(f"""
            <div class="card-container card-combo">
                <div>
                    <span class="badge-tag badge-featured">{combo['badge']}</span>
                    <h4>{combo['title']}</h4>
                    <p style="color: #94a3b8; font-size: 0.88rem;">{combo['desc']}</p>
                </div>
                <div>
                    <hr style="border-color: #334155; margin: 0.8rem 0;">
                    <div class="price-tag">{combo['fee']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Single Subject Modules")
    sc1, sc2 = st.columns(2)
    for idx, course in enumerate(O_LEVEL_COURSES):
        target_col = sc1 if idx % 2 == 0 else sc2
        with target_col:
            st.markdown(f"""
            <div class="card-container" style="margin-bottom: 1rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span class="badge-tag badge-primary">{course['code']}</span>
                        <h4 style="margin:0;">{course['title']}</h4>
                    </div>
                    <div class="price-tag">{course['fee']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# PAGE 2: ADMISSION
elif menu == "📝 Course Admission":
    st.title("📝 Student Enrollment Portal")
    st.write("Fill out the application below to register for live classes.")

    all_options = [c["title"] for c in SPECIAL_COMBOS] + [c["title"] for c in O_LEVEL_COURSES]

    with st.form("enrollment_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Student Name *")
            email = st.text_input("Email Address *")
        with col2:
            phone = st.text_input("WhatsApp Phone *", placeholder="+92 300 1234567")
            course_choice = st.selectbox("Select Course/Bundle *", all_options)

        submitted = st.form_submit_button("Submit Application")

        if submitted:
            if not full_name.strip():
                st.error("Please provide a valid name.")
            elif not is_valid_email(email):
                st.error("Please provide a valid email address.")
            elif len(phone.strip()) < 8:
                st.error("Please provide a valid WhatsApp contact number.")
            else:
                norm_phone = normalize_phone(phone)
                enrollments = load_json("enrollments.json", [])
                
                new_record = {
                    "name": sanitize_csv_field(full_name),
                    "email": sanitize_csv_field(email),
                    "phone": norm_phone,
                    "course": course_choice
                }
                
                enrollments.append(new_record)
                save_json("enrollments.json", enrollments)
                sync_to_github("enrollments.json", enrollments)

                st.success(f"Application received for **{full_name}**! Our team will reach out via WhatsApp at {norm_phone}.")

# PAGE 3: CHAT ASSISTANT
elif menu == "🤖 AI Assistant":
    st.title("🤖 Academy Virtual Assistant")
    st.caption("Ask questions regarding schedules, course topics, or bundle details.")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you regarding admissions or course details today?"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Type your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

# PAGE 4: ADMIN DASHBOARD
elif menu == "🔒 Admin Dashboard":
    st.title("🔒 Admin Portal")
    
    pwd = st.text_input("Enter Admin Credentials", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.success("Authenticated")
        
        enrollments = load_json("enrollments.json", [])
        if enrollments:
            df = pd.DataFrame(enrollments)
            
            st.subheader(f"Registered Students ({len(df)})")
            st.dataframe(df, use_container_width=True)
            
            # Export function
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Registrations to CSV",
                data=csv,
                file_name="enrollments_export.csv",
                mime="text/csv"
            )
        else:
            st.info("No enrollment records currently available.")
    elif pwd:
        st.error("Invalid Admin Key")
