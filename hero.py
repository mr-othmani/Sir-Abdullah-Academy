import streamlit as st

def render_hero_section():
    """Renders the top vibrant hero banner and right-side interactive frame."""
    hero_left, hero_right = st.columns([1.25, 1])

    with hero_left:
        st.markdown("""
        <div class="floating-pill">⭐ Every Lesson Counts</div>
        <div class="hero-heading">
            Pakistan's <span class="gradient-purple">#1 Online</span> Platform for <span class="gradient-gold">O & A Level</span> Success
        </div>
        <div class="hero-subhead">
            High-quality interactive live classes, topical solved past papers, examiner keyword mastery, and expert faculty — guaranteed to secure top A* grades.
        </div>
        """, unsafe_allow_html=True)

        cta1, cta2 = st.columns(2)
        with cta1:
            st.markdown('<div class="btn-gradient-purple">', unsafe_allow_html=True)
            if st.button("🚀 Explore Courses", key="hero_explore_btn", use_container_width=True):
                st.session_state.active_tab = "Courses"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with cta2:
            st.markdown('<div class="btn-gradient-amber">', unsafe_allow_html=True)
            if st.button("📝 Apply for Admission", key="hero_apply_btn", use_container_width=True):
                st.session_state.active_tab = "Admission"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with hero_right:
        st.markdown("""
        <div class="hero-graphic-card">
            <div class="badge-result-top">
                <span>🎗️</span> 10,000+ A* Results
            </div>
            <div class="device-bezel">
                <div class="device-screen">
                    <p style="text-transform: uppercase; font-size: 0.75rem; letter-spacing: 1.5px; font-weight: 800; color: #c084fc; margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: center; gap: 8px;">
                        <span class="pulse-dot"></span> LIVE ONLINE BATCH
                    </p>
                    <h2 style="font-weight: 900; font-size: 1.9rem; color: #facc15; margin-bottom: 0.4rem; letter-spacing: -0.5px;">NOW STUDY ONLINE</h2>
                    <p style="font-size: 0.9rem; opacity: 0.85; margin-bottom: 1.5rem;">Interactive Zoom & Meet Classes with Sir Abdullah</p>
                    <div class="screen-pill">
                        <p style="margin:0; font-size:0.88rem; font-weight:700;">💻 Digital Whiteboard & Instant Doubts</p>
                    </div>
                    <div class="screen-pill">
                        <p style="margin:0; font-size:0.88rem; font-weight:700;">📚 10+ Yrs Topical Solved Papers</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_value_grid():
    """Renders the 4-column feature grid below the hero header."""
    st.markdown("<br><br>", unsafe_allow_html=True)
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
            <div class="vibrant-feature-card">
                <div class="icon-box">{icon}</div>
                <h4 style="font-weight: 800; color: #0f172a; margin-bottom: 0.5rem; font-size: 1.05rem;">{title}</h4>
                <p style="font-size: 0.85rem; color: #64748b; line-height: 1.55; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
