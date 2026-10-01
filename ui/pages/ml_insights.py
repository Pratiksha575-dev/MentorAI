import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go
from database import get_all_mentors, get_all_groups, get_students_by_group
from ui.components import page_header

def render_ml_insights():
    page_header("ML Insights & Archetypes", "Dynamic K-Means Clustering on live user data.", "🤖")
    
    st.markdown("We use Unsupervised Machine Learning (K-Means Clustering) to automatically discover distinct personality archetypes in the university population. The algorithm groups students and mentors into clusters based entirely on the 5-dimensional distance between their Extraversion, Neuroticism, Agreeableness, Conscientiousness, and Openness scores.")
    
    mentors = get_all_mentors()
    groups = get_all_groups()
    
    data = []
    
    for m in mentors:
        data.append({
            "Name": m['name'],
            "Type": "Mentor",
            "Extraversion": m.get('extraversion', 0),
            "Neuroticism": m.get('neuroticism', 0),
            "Agreeableness": m.get('agreeableness', 0),
            "Conscientiousness": m.get('conscientiousness', 0),
            "Openness": m.get('openness', 0)
        })
        
    for g in groups:
        students = get_students_by_group(g['id'])
        for s in students:
            data.append({
                "Name": s['name'] + f" ({g['name']})",
                "Type": "Student",
                "Extraversion": s.get('extraversion', 0),
                "Neuroticism": s.get('neuroticism', 0),
                "Agreeableness": s.get('agreeableness', 0),
                "Conscientiousness": s.get('conscientiousness', 0),
                "Openness": s.get('openness', 0)
            })
            
    if len(data) < 5:
        st.warning("Not enough data to run Machine Learning.")
        return
        
    df = pd.DataFrame(data)
    features = ['Extraversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']
    X = df[features]
    
    k = st.slider("Select number of clusters (K)", min_value=2, max_value=6, value=3)
    
    with st.spinner("Training K-Means model..."):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        df['Cluster'] = kmeans.fit_predict(X)
        df['Cluster'] = df['Cluster'].astype(str)
        
    st.markdown("### Personality Clusters (3D Projection)")
    fig = px.scatter_3d(
        df, 
        x='Extraversion', 
        y='Conscientiousness', 
        z='Neuroticism',
        color='Cluster',
        symbol='Type',
        hover_name='Name',
    )
    
    # Make background transparent and bigger
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=700,
        scene=dict(
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)")
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Cluster Archetypes (Centers)")
    centers = pd.DataFrame(kmeans.cluster_centers_, columns=features)
    
    radar_fig = go.Figure()
    for i, row in centers.iterrows():
        radar_fig.add_trace(go.Scatterpolar(
            r=row.values.tolist() + [row.values[0]],
            theta=features + [features[0]],
            fill='toself',
            name=f'Cluster {i}'
        ))
        
    radar_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5], gridcolor="rgba(255,255,255,0.1)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")
        ),
        font=dict(color="white")
    )
    st.plotly_chart(radar_fig, use_container_width=True)
    
