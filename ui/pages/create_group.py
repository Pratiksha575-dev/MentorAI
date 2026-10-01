import streamlit as st
from config.questions import STUDENT_QUESTIONS, SCALE_OPTIONS, SCALE_LABELS
from ml.personality_model import analyze_traits
from database import save_student_group, save_student
from llm import generate_group_dynamic
from ui.components import page_header

def render_create_group():
    page_header("Create Student Group", "Form a project team and analyze your dynamic.", "👥")
    
    if "group_members" not in st.session_state:
        st.session_state.group_members = []
        
    g_name = st.text_input("Group Name", placeholder="e.g. The Innovators")
    g_topic = st.text_input("Project Topic", placeholder="e.g. AI-powered Chatbot")
    
    st.markdown("### Current Members")
    if not st.session_state.group_members:
        st.info("No members added yet. Please add at least 1 member.")
    else:
        for idx, m in enumerate(st.session_state.group_members):
            st.success(f"Member {idx+1}: {m['name']}")
            
    st.divider()
    
    st.markdown("### Add New Member")
    m_name = st.text_input("Member Name", key="new_member_name")
    
    answers = []
    for i, (trait, text) in enumerate(STUDENT_QUESTIONS):
        ans = st.radio(
            f"{i+1}. {text}", 
            SCALE_OPTIONS, 
            format_func=lambda x: SCALE_LABELS[x],
            horizontal=True,
            key=f"s_q_{i}"
        )
        answers.append(ans)
        
    if st.button("Add Member to Group"):
        if not m_name.strip():
            st.error("Please enter a member name.")
        else:
            traits = analyze_traits(answers, STUDENT_QUESTIONS)
            st.session_state.group_members.append({"name": m_name, "traits": traits})
            st.success(f"Added {m_name}!")
            st.rerun()
            
    st.divider()
    
    if len(st.session_state.group_members) > 0:
        if st.button("Finalize Group & Analyze Dynamic", type="primary", use_container_width=True):
            if not g_name.strip() or not g_topic.strip():
                st.error("Please provide a Group Name and Project Topic.")
                return
                
            with st.spinner("Analyzing group dynamic..."):
                members = st.session_state.group_members
                
                # Aggregate traits
                avg_traits = {
                    "Extraversion": sum(m["traits"]["Extraversion"] for m in members) / len(members),
                    "Neuroticism": sum(m["traits"]["Neuroticism"] for m in members) / len(members),
                    "Agreeableness": sum(m["traits"]["Agreeableness"] for m in members) / len(members),
                    "Conscientiousness": sum(m["traits"]["Conscientiousness"] for m in members) / len(members),
                    "Openness": sum(m["traits"]["Openness"] for m in members) / len(members),
                }
                
                dynamic = generate_group_dynamic(g_name, g_topic, members)
                
                g_id = save_student_group(g_name, g_topic, avg_traits, dynamic)
                
                for m in members:
                    save_student(g_id, m["name"], m["traits"], "")
                    
                st.success("Group created!")
                st.write(dynamic)
                
                st.session_state.group_members = [] # reset
