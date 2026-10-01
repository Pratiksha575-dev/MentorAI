import streamlit as st
from database import get_all_mentors, get_all_groups
from ui.components import page_header

def render_home():
    page_header("Overview 🏠", "MentorAI Dashboard", "Command center for the mentorship program.")
    
    mentors = get_all_mentors()
    groups = get_all_groups()
    
    total_students = 0
    from database import get_students_by_group
    for g in groups:
        total_students += len(get_students_by_group(g['id']))
        
    c1, c2, c3 = st.columns(3)
    c1.metric("Registered Mentors 🧑‍🏫", len(mentors), delta="Active")
    c2.metric("Student Groups 👥", len(groups), delta="Ready")
    c3.metric("Total Students 🎓", total_students, delta="Enrolled")
    
    st.markdown("### Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
        <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(0,0,0,0)); padding:20px; border-radius:12px; border:1px solid rgba(139, 92, 246, 0.3); height: 140px; margin-bottom: 10px;">
            <h4 style="margin-top:0;">🤖 ML Insights</h4>
            <p style="color:#94a3b8; font-size:14px; margin-bottom:0;">View 3D K-Means clustering of all users based on Big Five traits.</p>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("View ML Insights", use_container_width=True):
            st.session_state.current_page = "ML Insights"
            st.rerun()
            
    with col2:
        st.markdown('''
        <div style="background: linear-gradient(135deg, rgba(217, 70, 239, 0.1), rgba(0,0,0,0)); padding:20px; border-radius:12px; border:1px solid rgba(217, 70, 239, 0.3); height: 140px; margin-bottom: 10px;">
            <h4 style="margin-top:0;">🕸️ Neural Web</h4>
            <p style="color:#94a3b8; font-size:14px; margin-bottom:0;">Explore the interactive physics-based Graph ML simulation of super-teams.</p>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("Open Neural Web", use_container_width=True):
            st.session_state.current_page = "Neural Web"
            st.rerun()
            
    with col3:
        st.markdown('''
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(0,0,0,0)); padding:20px; border-radius:12px; border:1px solid rgba(16, 185, 129, 0.3); height: 140px; margin-bottom: 10px;">
            <h4 style="margin-top:0;">⚙️ Allocation</h4>
            <p style="color:#94a3b8; font-size:14px; margin-bottom:0;">Run the matching engine to pair mentees with their perfect faculty mentor.</p>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("Run Allocation", use_container_width=True):
            st.session_state.current_page = "Run Allocation"
            st.rerun()
