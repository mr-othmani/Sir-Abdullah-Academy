import streamlit as st
import pandas as pd
import plotly.express as px
from database import SessionLocal, StudentEnrollment

def render_analytics_dashboard():
    st.markdown("### 📊 Enrollment Analytics & Platform Performance")
    
    db = SessionLocal()
    try:
        enrollments = db.query(StudentEnrollment).all()
        if not enrollments:
            st.info("No enrollment data available for analytics yet.")
            return

        data = [{
            "Name": e.full_name,
            "Course": e.course,
            "Status": e.status,
            "Date": e.created_at
        } for e in enrollments]
        
        df = pd.DataFrame(data)

        # Top Metric Cards
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Applicants", len(df))
        col2.metric("Most Popular Course", df["Course"].mode()[0] if not df.empty else "N/A")
        col3.metric("Pending Confirmations", len(df[df["Status"] == "Pending"]))

        st.markdown("<br>", unsafe_allow_html=True)
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            fig_courses = px.pie(
                df, names="Course", title="Enrollment Share by Course",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                hole=0.4
            )
            st.plotly_chart(fig_courses, use_container_width=True)

        with chart_col2:
            df["Date_Only"] = pd.to_datetime(df["Date"]).dt.date
            timeline = df.groupby("Date_Only").size().reset_index(name="Signups")
            fig_line = px.line(
                timeline, x="Date_Only", y="Signups", title="Daily Application Growth",
                markers=True, color_discrete_sequence=["#7c3aed"]
            )
            st.plotly_chart(fig_line, use_container_width=True)

    finally:
        db.close()
