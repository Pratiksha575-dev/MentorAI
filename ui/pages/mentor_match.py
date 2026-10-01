import streamlit as st
from database import get_all_mentors, get_all_groups
from ml.mentor_matcher import match_mentors_and_mentees
from llm import generate_mentor_briefing
from ui.components import page_header

def render_mentor_match():
    page_header("Mentor-Mentee Alignment Engine", "Allocate groups optimally.", "⚙️")
    
    mentors = get_all_mentors()
    groups = get_all_groups()
    
    if not mentors or not groups:
        st.warning("Need at least 1 mentor and 1 group.")
        return
        
    if st.button("Run Allocation Algorithm ✨", type="primary", use_container_width=True):
        st.session_state.mentor_assignments = match_mentors_and_mentees(mentors, groups, max_groups_per_mentor=4)
        st.rerun()

    if "mentor_assignments" in st.session_state:
        st.markdown("<br><h3>Allocation Results</h3>", unsafe_allow_html=True)
        assignments = st.session_state.mentor_assignments
        
        for mentor_id, data in assignments.items():
            mentor = data["mentor"]
            assigned_groups = data["mentees"]
            
            with st.expander(f"🧑‍🏫 Mentor: {mentor['name']} ({len(assigned_groups)} Groups)"):
                if not assigned_groups:
                    st.info("No groups assigned.")
                    continue
                    
                for m_data in assigned_groups:
                    group = m_data["mentee"]
                    score = m_data["score"]
                    
                    st.markdown(f"#### 👥 {group['name']}")
                    st.caption(f"**Topic:** {group['project_topic']}")
                    
                    # Normalize score to max out at 100 for display
                    display_score = min(score, 100.0)
                    
                    # Beautiful UI pill for compatibility
                    st.markdown(f'''
                    <div style="display:flex; align-items:center; margin-bottom:1rem;">
                        <div style="background:#a78bfa; color:#1e1e2e; padding:4px 12px; border-radius:20px; font-weight:bold; font-size:0.9rem;">
                            Compatibility Score: {display_score:.0f} / 100
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    advice_key = f"advice_{mentor['id']}_{group['id']}"
                    
                    if advice_key in st.session_state:
                        st.markdown(f'''
                        <div style="background:rgba(139,92,246,0.1); padding:1rem; border-radius:10px; border:1px solid rgba(139,92,246,0.2); margin-top:10px;">
                            <strong style="color:#c084fc">🤖 AI Mentor Briefing:</strong><br>
                            {st.session_state[advice_key]}
                        </div>
                        ''', unsafe_allow_html=True)
                    else:
                        if st.button(f"Generate Briefing for {group['name']}", key=f"btn_{mentor['id']}_{group['id']}"):
                            with st.spinner("Analyzing match..."):
                                advice = generate_mentor_briefing(mentor, group)
                                st.session_state[advice_key] = advice
                                st.rerun()
                    st.divider()
