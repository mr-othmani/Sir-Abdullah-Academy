import streamlit as st
import pandas as pd
from models import load_json, save_json
from utils import normalize_phone, sanitize_csv_field
from chatbot import get_bot_response
from github_store import sync_to_github

st.set_page_config(page_title="Sir Abdullah Academy", page_icon="🎓", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #f3f4f6; }
    .stButton>button { background-color: #4f46e5; color: white; border-radius: 8px; border: none; }
</style>
""", unsafe_allow_html=True)

ADMIN_PASSWORD = "osmanibhai112233"

st.sidebar.title("🎓 Navigation")
menu = st.sidebar.radio("Go to", ["Chat Assistant", "Course Admission", "Admin Dashboard"])

if menu == "Chat Assistant":
    st.title("🤖 Academy Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask about courses, fees, timings..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

elif menu == "Course Admission":
    st.title("📝 Admission Form")
    courses = load_json("courses.json", [])
    active_courses = [c["title"] for c in courses if c.get("active", True)]

    with st.form("admission_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number (e.g. 03321234567)")
        selected_course = st.selectbox("Select Course", active_courses)
        submitted = st.form_submit_button("Submit Application")

        if submitted:
            if not name or not phone:
                st.error("Please fill in required fields.")
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
                st.success("Application submitted successfully!")

elif menu == "Admin Dashboard":
    st.title("🔒 Admin Control Center")
    pwd = st.sidebar.text_input("Admin Password", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.success("Authenticated")
        tab1, tab2 = st.tabs(["Enrollments Log", "Course Catalog"])
        
        with tab1:
            st.subheader("Submitted Enrollments")
            enrollments = load_json("enrollments.json", [])
            if enrollments:
                df = pd.DataFrame(enrollments)
                st.dataframe(df)
            else:
                st.info("No enrollments yet.")
                
        with tab2:
            st.subheader("Manage Courses")
            courses = load_json("courses.json", [])
            st.json(courses)
    else:
                st.warning("Enter valid password to access admin logs.")
