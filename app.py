"""
app.py
Streamlit application for Sir Abdullah Academy - Online Tuition Chatbot.

Pages:
    - Home             : Introduction to the academy
    - Chatbot          : Customer Support Bot (FAQ chatbot)
    - Course Manager     : Admin panel demonstrating OOP CRUD (Course/CourseManager)
    - Query Log        : View logged customer queries

Run with:
    streamlit run app.py
"""

import os
import csv
import base64
import json
from datetime import datetime
import pandas as pd
import streamlit as st

# ===========================================================================
# BACKWARD COMPATIBLE & RESILIENT IMPORTS WITH FALLBACK BLUEPRINTS
# ===========================================================================

# --- 1. OOP Blueprint Requirement ---
class Course:
    def __init__(self, course_id, name, category, status="Active"):
        self.course_id = course_id
        self.name = name
        self.category = category
        self.status = status

    def to_dict(self):
        return {
            "Course ID": self.course_id,
            "Name": self.name,
            "Category": self.category,
            "Status": self.status
        }


class CourseManagerFallback:
    def __init__(self, filepath="courses.json"):
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            self._save([])

    def _load(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save(self, data):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def add(self, name, course_id, category, status="Active"):
        courses = self._load()
        if any(c.get("Course ID") == course_id for c in courses):
            return False, f"Course ID '{course_id}' already exists."
        
        new_course = Course(course_id, name, category, status)
        courses.append(new_course.to_dict())
        self._save(courses)
        return True, f"Course '{name}' added successfully!"

    def search(self, course_id):
        courses = self._load()
        for c in courses:
            if c.get("Course ID") == course_id:
                return Course(c["Course ID"], c["Name"], c["Category"], c["Status"])
        return None

    def update(self, course_id, name=None, category=None, status=None):
        courses = self._load()
        found = False
        for c in courses:
            if c.get("Course ID") == course_id:
                if name:
                    c["Name"] = name
                if category:
                    c["Category"] = category
                if status:
                    c["Status"] = status
                found = True
                break
        if found:
            self._save(courses)
            return True, f"Course ID '{course_id}' updated successfully!"
        return False, f"Course ID '{course_id}' not found."

    def delete(self, course_id):
        courses = self._load()
        filtered = [c for c in courses if c.get("Course ID") != course_id]
        if len(filtered) < len(courses):
            self._save(filtered)
            return True, f"Course ID '{course_id}' deleted successfully."
        return False, f"Course ID '{course_id}' not found."

    def display(self):
        return self._load()


# --- 2. Chatbot & Query Classifier Implementation ---
GREETINGS = ["hi", "hello", "hey", "good morning", "good evening", "thanks", "thank you", "bye"]

class SirAbdullahChatbotFallback:
    def classify_query(self, query):
        q = query.lower()
        if any(k in q for k in ["fee", "price", "cost", "payment", "pkr"]):
            return "Payment & Fees"
        elif any(k in q for k in ["phone", "whatsapp", "contact", "email", "location"]):
            return "Contact Information"
        elif any(k in q for k in ["time", "hour", "schedule", "timing", "batch"]):
            return "Business Hours"
        elif any(k in q for k in ["course", "subject", "matric", "o level", "a level", "python"]):
            return "Product / Course Information"
        elif any(k in q for k in ["online", "zoom", "meet", "class", "demo"]):
            return "Services & Delivery"
        else:
            return "Other"

    def log_query(self, query, category):
        # Exclude casual greetings from being saved to the CSV log
        if query.lower().strip() in GREETINGS:
            return False
        
        log_file = "query_log.csv"
        file_exists = os.path.exists(log_file)
        
        with open(log_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Date", "Time", "Query", "Category"])
            now = datetime.now()
            writer.writerow([
                now.strftime("%Y-%m-%d"),
                now.strftime("%I:%M %p"),
                query.replace(",", " ").strip(),
                category
            ])
        return True

    def get_response(self, query):
        q = query.lower().strip()
        
        # Friendly response for simple greetings
        if q in ["hi", "hello", "hey", "good morning", "good evening"]:
            return "Hello! Welcome to Sir Abdullah Academy. How can I assist you with your studies today?", "Greeting", False
        if q in ["thanks", "thank you", "bye"]:
            return "You're welcome! Feel free to reach out anytime.", "Greeting", False

        category = self.classify_query(query)
        
        if category == "Payment & Fees":
            res = "Our fee structure varies by course level: Matric/O Levels start at PKR 5,000/mo, and A Level/Programming packages start at PKR 6,500/mo."
        elif category == "Contact Information":
            res = "You can contact Sir Abdullah Academy on WhatsApp at +92 332 1234567 or email us at support@sirabdullah.edu.pk."
        elif category == "Business Hours":
            res = "Live interactive online classes take place Monday through Saturday in flexible morning and evening batches."
        elif category == "Product / Course Information":
            res = "We offer complete tuition for Matric, O Level, A Level, Python Programming, and Web Development."
        else:
            res = "Thank you for reaching out! A student counselor will guide you further. For immediate support, please contact us on WhatsApp."

        logged = self.log_query(query, category)
        return res, category, logged


# Attempt imports from local modules; fall back to embedded classes if unavailable
try:
    from models import CourseManager
except ImportError:
    CourseManager = CourseManagerFallback

try:
    from chatbot import SirAbdullahChatbot
except ImportError:
    try:
        from chatbot import SirOsmaniChatbot as SirAbdullahChatbot
    except ImportError:
        SirAbdullahChatbot = SirAbdullahChatbotFallback

try:
    from utils import read_csv_rows, validate_input
except ImportError:
    def validate_input(text):
        return bool(text and text.strip())

    def read_csv_rows(filepath):
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                return df.to_dict(orient="records")
            except Exception:
                return []
        return []


# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Sir Abdullah Academy",
    page_icon="🎓",
    layout="wide",
)

LOGO_PATH = os.path.join("assets", "logo.png")
BACKGROUND_PATH = "background.png"

def set_background(image_path):
    """
    Sets a full-page background image using custom CSS.
    A dark, semi-transparent overlay is added on top so text stays readable.
    If the image file doesn't exist, this does nothing (no crash).
    """
    if not os.path.exists(image_path):
        return

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    ext = image_path.split(".")[-1]

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(0,0,0,0.35), rgba(0,0,0,0.35)),
                url("data:image/{ext};base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


set_background(BACKGROUND_PATH)


# ---------------------------------------------------------------------------
# CACHED RESOURCES
# ---------------------------------------------------------------------------

@st.cache_resource
def get_chatbot():
    return SirAbdullahChatbot()


@st.cache_resource
def get_course_manager():
    return CourseManager()


chatbot = get_chatbot()
course_manager = get_course_manager()

# Chat history lives in session state so it persists across reruns
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False


# ---------------------------------------------------------------------------
# ADMIN PASSWORD
# ---------------------------------------------------------------------------
ADMIN_PASSWORD = "osmanibhai112233"


# ---------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------------------------

with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=120)
    st.title("🎓 Sir Abdullah Academy")
    st.caption("Online Tuition Platform")

    available_pages = ["🏠 Home", "💬 Chatbot"]

    if st.session_state.is_admin:
        available_pages += ["📚 Course Manager", "📄 Query Log"]

    page = st.radio("Navigate", available_pages)

    st.divider()

    if st.session_state.is_admin:
        st.success("🔓 Admin mode is ON")
        if st.button("Log out of Admin"):
            st.session_state.is_admin = False
            st.rerun()
    else:
        with st.expander("🔒 Admin Login"):
            entered_password = st.text_input("Password", type="password", key="admin_password_input")
            if st.button("Unlock Admin Pages"):
                if entered_password == ADMIN_PASSWORD:
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")

    st.divider()
    st.caption("Python & AI Mastery — Final Project")


# ---------------------------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------------------------

if page == "🏠 Home":
    st.title("Welcome to Sir Abdullah Academy 🎓")
    st.subheader("Quality Online Tuition, Anywhere, Anytime")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            **Sir Abdullah Academy** offers online tuition for:
            - Matric (Science & Arts)
            - O Level & A Level
            - Python Programming & Web Development

            Ask our chatbot anything about courses, fees, timings,
            teachers, or how to enroll!
            """
        )
        if st.button("💬 Start chatting with our Support Bot"):
            st.session_state["_redirect_hint"] = True
            st.info("Select '💬 Chatbot' from the sidebar to begin.")

    with col2:
        st.markdown("#### Why choose us?")
        st.success("✅ Qualified & experienced teachers")
        st.success("✅ Free demo class before enrollment")
        st.success("✅ Flexible weekday & weekend batches")
        st.success("✅ Recorded lectures & progress reports")

    st.divider()
    st.markdown("#### Our Courses")
    courses = course_manager.display()
    if courses:
        df = pd.DataFrame(courses)
        st.table(df)
    else:
        st.warning("No courses have been added yet. Add some in the Course Manager page.")


# ---------------------------------------------------------------------------
# CHATBOT PAGE
# ---------------------------------------------------------------------------

elif page == "💬 Chatbot":
    st.title("💬 Sir Abdullah Academy — Support Chatbot")
    st.caption("Ask about courses, fees, timings, teachers, location, or enrollment.")

    example_cols = st.columns(4)
    examples = [
        "What courses do you offer?",
        "What are your fees?",
        "What are the class timings?",
        "How can I enroll?",
    ]
    clicked_example = None
    for col, ex in zip(example_cols, examples):
        with col:
            if st.button(ex):
                clicked_example = ex

    for sender, message in st.session_state.chat_history:
        with st.chat_message(sender):
            st.write(message)

    user_input = st.chat_input("Type your question here...")
    final_input = clicked_example or user_input

    if final_input:
        if not validate_input(final_input):
            st.error("Please enter a valid question.")
        else:
            st.session_state.chat_history.append(("user", final_input))
            with st.chat_message("user"):
                st.write(final_input)

            response, category, logged = chatbot.get_response(final_input)

            st.session_state.chat_history.append(("assistant", response))
            with st.chat_message("assistant"):
                st.write(response)
                if logged:
                    st.caption(f"📁 Logged under category: **{category}**")

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()


# ---------------------------------------------------------------------------
# COURSE MANAGER PAGE (OOP CRUD DEMO)
# ---------------------------------------------------------------------------

elif page == "📚 Course Manager":
    st.title("📚 Course Manager")
    st.caption("Admin panel demonstrating the Course / CourseManager class (OOP Blueprint).")

    tab_add, tab_search, tab_update, tab_delete, tab_display = st.tabs(
        ["➕ Add", "🔍 Search", "✏️ Update", "🗑️ Delete", "📋 Display All"]
    )

    with tab_add:
        with st.form("add_course_form"):
            name = st.text_input("Course Name")
            course_id = st.text_input("Course ID")
            category = st.selectbox(
                "Category",
                ["Matric", "O Level", "A Level", "AI and Programming", "Other"],
            )
            status = st.selectbox("Status", ["Active", "Inactive"])
            submitted = st.form_submit_button("Add Course")

        if submitted:
            if not validate_input(name) or not validate_input(course_id):
                st.error("Course Name and Course ID are required.")
            else:
                success, msg = course_manager.add(name, course_id, category, status)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

    with tab_search:
        search_id = st.text_input("Enter Course ID to search", key="search_id")
        if st.button("Search"):
            result = course_manager.search(search_id)
            if result:
                st.success("Course found:")
                st.json(result.to_dict() if hasattr(result, "to_dict") else result)
            else:
                st.error(f"No course found with ID '{search_id}'.")

    with tab_update:
        update_id = st.text_input("Course ID to update", key="update_id")
        new_name = st.text_input("New Name (optional)", key="update_name")
        new_category = st.selectbox(
            "New Category (optional)",
            ["", "Matric", "O Level", "A Level", "AI and Programming", "Other"],
            key="update_category",
        )
        new_status = st.selectbox("New Status (optional)", ["", "Active", "Inactive"], key="update_status")
        if st.button("Update Course"):
            success, msg = course_manager.update(
                update_id,
                name=new_name or None,
                category=new_category or None,
                status=new_status or None,
            )
            if success:
                st.success(msg)
            else:
                st.error(msg)

    with tab_delete:
        delete_id = st.text_input("Course ID to delete", key="delete_id")
        if st.button("Delete Course"):
            success, msg = course_manager.delete(delete_id)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    with tab_display:
        courses = course_manager.display()
        if courses:
            st.dataframe(pd.DataFrame(courses), use_container_width=True)
        else:
            st.info("No courses added yet.")


# ---------------------------------------------------------------------------
# QUERY LOG PAGE
# ---------------------------------------------------------------------------

elif page == "📄 Query Log":
    st.title("📄 Customer Query Log")
    st.caption("Meaningful customer queries logged by the chatbot (greetings are excluded).")

    rows = read_csv_rows("query_log.csv")
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.markdown("#### Queries by Category")
        if "Category" in df.columns:
            st.bar_chart(df["Category"].value_counts())
    else:
        st.info("No queries have been logged yet. Try the chatbot!")
