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
            if st.button("Home", key="nav_home", type="primary" if st.session_state.get("active_tab") == "Home" else "tertiary"):
                st.session_state.active_tab = "Home"
                st.rerun()
        with n2:
            if st.button("Courses", key="nav_courses", type="primary" if st.session_state.get("active_tab") == "Courses" else "tertiary"):
                st.session_state.active_tab = "Courses"
                st.rerun()
        with n3:
            if st.button("Admission", key="nav_admission", type="primary" if st.session_state.get("active_tab") == "Admission" else "tertiary"):
                st.session_state.active_tab = "Admission"
                st.rerun()
        with n4:
            if st.button("AI Tutor", key="nav_ai", type="primary" if st.session_state.get("active_tab") == "Assistant" else "tertiary"):
                st.session_state.active_tab = "Assistant"
                st.rerun()

    with col_cta:
        st.markdown('<div class="btn-gradient-purple">', unsafe_allow_html=True)
        if st.button("⚡ Enroll Now", key="nav_enroll_btn", use_container_width=True):
            st.session_state.active_tab = "Admission"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-bottom: 1px solid rgba(226, 232, 240, 0.8); margin: 0.8rem 0 2rem 0;'>", unsafe_allow_html=True)

def render_footer():
    """Renders professional footer with accreditation links and copyright details."""
    st.markdown("<br><br><hr style='border: none; border-bottom: 1px solid rgba(226, 232, 240, 0.8);'><br>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    
    with f_col1:
        st.markdown("""
        <h4 style="color: #4c1d95; font-weight: 800; margin-bottom: 0.5rem;">Sir Abdullah Academy</h4>
        <p style="color: #64748b; font-size: 0.85rem; line-height: 1.6;">
            Pakistan's premier digital institute for Cambridge O & A Level preparation. Dedicated to concept clarity, marking scheme mastery, and top grade performance.
        </p>
        """, unsafe_allow_html=True)
    
    with f_col2:
        st.markdown("""
        <h5 style="font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">Quick Links</h5>
        <p style="font-size: 0.85rem; color: #64748b; margin: 0.2rem 0;">• CAIE Examination Timetable</p>
        <p style="font-size: 0.85rem; color: #64748b; margin: 0.2rem 0;">• Past Paper Library</p>
        <p style="font-size: 0.85rem; color: #64748b; margin: 0.2rem 0;">• Verified Results</p>
        """, unsafe_allow_html=True)
        
    with f_col3:
        st.markdown("""
        <h5 style="font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">Support</h5>
        <p style="font-size: 0.85rem; color: #64748b; margin: 0.2rem 0;">💬 WhatsApp: +92 332 1234567</p>
        <p style="font-size: 0.85rem; color: #64748b; margin: 0.2rem 0;">✉️ support@sirabdullah.com</p>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 2rem; padding-bottom: 1rem;">
        © 2026 Sir Abdullah Academy. All rights reserved. Not affiliated directly with Cambridge Assessment International Education (CAIE).
    </div>
    """, unsafe_allow_html=True)
