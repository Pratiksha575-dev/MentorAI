import streamlit as st
from database import get_all_mentors, get_all_groups, get_students_by_group
from ui.components import page_header, trait_card

def render_directory():
    page_header("Directory", "View all registered faculty and student groups.", "📁")
    
    tab1, tab2 = st.tabs(["Mentors", "Student Groups"])
    
    with tab1:
        for m in get_all_mentors():
            with st.expander(f"🧑‍🏫 {m['name']}"):
                st.write(f"**Domains:** {', '.join(m['domains'])}")
                
                # Draw traits
                st.markdown("##### Advising Traits")
                cols = st.columns(5)
                traits = ['Extraversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']
                for i, trait in enumerate(traits):
                    with cols[i]:
                        trait_card(trait, m.get(trait.lower(), 0))
                
                st.markdown("##### AI Summary")
                st.write(m['ai_summary'])
                
    with tab2:
        for g in get_all_groups():
            with st.expander(f"👥 {g['name']} - {g['project_topic']}"):
                
                # Draw traits
                st.markdown("##### Group Average Traits")
                cols = st.columns(5)
                traits = ['Extraversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']
                for i, trait in enumerate(traits):
                    with cols[i]:
                        trait_card(trait, g.get(trait.lower(), 0))
                        
                st.markdown("##### AI Group Dynamic Analysis")
                st.write(g['ai_group_dynamic'])
                
                st.markdown("##### Team Members")
                students = get_students_by_group(g['id'])
                
                if students:
                    # Markdown table for students
                    table = "| Name | Ext | Neu | Agr | Con | Opn |\n|---|---|---|---|---|---|\n"
                    for s in students:
                        table += f"| {s['name']} | {s['extraversion']:.1f} | {s['neuroticism']:.1f} | {s['agreeableness']:.1f} | {s['conscientiousness']:.1f} | {s['openness']:.1f} |\n"
                    st.markdown(table)
