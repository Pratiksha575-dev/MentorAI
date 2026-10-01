import streamlit as st
from config.constants import DOMAIN_OPTIONS
from config.questions import MENTOR_QUESTIONS, SCALE_OPTIONS, SCALE_LABELS
from ml.personality_model import analyze_traits
from database import save_mentor
from llm import generate_mentor_summary
from ui.components import page_header

def render_register_mentor():
    page_header("Register Mentor", "Join the faculty mentorship directory.", "🧑‍🏫")
    
    name = st.text_input("Full Name", placeholder="e.g. Dr. Jane Smith")
    domains = st.multiselect("Interested Domains", DOMAIN_OPTIONS, )
    
    st.markdown("### Advising Style Assessment")
    st.write("Please answer the following 20 questions to help us match you with the right student groups.")
    
    answers = []
    for i, (trait, text) in enumerate(MENTOR_QUESTIONS):
        ans = st.radio(
            f"{i+1}. {text}", 
            SCALE_OPTIONS, 
            format_func=lambda x: SCALE_LABELS[x],
            horizontal=True,
            key=f"m_q_{i}"
        )
        answers.append(ans)
        
    if st.button("Register as Mentor", type="primary"):
        if not name.strip():
            st.error("Please enter your name.")
            return
            
        with st.spinner("Analyzing advising style..."):
            traits = analyze_traits(answers, MENTOR_QUESTIONS)
            summary = generate_mentor_summary(name, domains, traits)
            
            m_id = save_mentor(name, domains, traits, summary)
            
            st.success("Mentor Profile Created Successfully!")
            st.write(summary)
            
            # Reset UI state (hacky way for Streamlit)
            st.session_state.current_page = "Dashboard"
            st.rerun()
