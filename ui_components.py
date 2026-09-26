# Save this in: ui_components.py
import streamlit as st

def render_top_navbar():
    """Renders floating top navigation header with active tab state tracking."""
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
            if st.button("Home", key="top_nav_home_btn", type="primary" if st.session_state.get("active_tab") == "Home" else "tertiary"):
                st.session_state.active_tab = "Home"
                st.rerun()
        with n2:
            if st.button("Courses", key="top_nav_courses_btn", type="primary" if st.session_state.get("active_tab") == "Courses" else "tertiary"):
                st.session_state.active_tab = "Courses"
                st.rerun()
        with n3:
            if st.button("Admission", key="top_nav_admission_btn", type="primary" if st.session_state.get("active_tab") == "Admission" else "tertiary"):
                st.session_state.active_tab = "Admission"
                st.rerun()
        with n4:
            if st.button("AI Tutor", key="top_nav_ai_btn", type="primary" if st.session_state.get("active_tab") == "Assistant" else "tertiary"):
                st.session_state.active_tab = "Assistant"
                st.rerun()

    with col_cta:
        st.markdown('<div class="btn-gradient-purple">', unsafe_allow_html=True)
        if st.button("⚡ Enroll Now", key="top_nav_enroll_btn", use_container_width=True):
            st.session_state.active_tab = "Admission"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-bottom: 1px solid rgba(226, 232, 240, 0.8); margin: 0.8rem 0 2rem 0;'>", unsafe_allow_html=True)
