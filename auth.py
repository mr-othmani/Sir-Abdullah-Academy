import bcrypt
import streamlit as st
from database import SessionLocal, UserAccount

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def authenticate_user(username_or_email: str, password: str):
    db = SessionLocal()
    try:
        user = db.query(UserAccount).filter(
            (UserAccount.username == username_or_email) | (UserAccount.email == username_or_email)
        ).first()
        if user and verify_password(password, user.password_hash):
            return user
        return None
    finally:
        db.close()

def render_login_component():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        st.sidebar.markdown(f"👤 Logged in as **{st.session_state.user['username']}** ({st.session_state.user['role'].capitalize()})")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()
        return st.session_state.user

    with st.expander("🔒 Portal Authentication Login", expanded=False):
        login_id = st.text_input("Username or Email", key="login_id")
        password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Sign In", key="btn_signin"):
            user = authenticate_user(login_id, password)
            if user:
                st.session_state.user = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
                st.success(f"Welcome back, {user.username}!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
    return st.session_state.user
