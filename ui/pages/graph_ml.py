import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
import math
import os
from database import get_all_mentors, get_all_groups, get_students_by_group
from ui.components import page_header

def calculate_distance(t1, t2):
    return math.sqrt(
        (t1.get('extraversion',0) - t2.get('extraversion',0))**2 +
        (t1.get('neuroticism',0) - t2.get('neuroticism',0))**2 +
        (t1.get('agreeableness',0) - t2.get('agreeableness',0))**2 +
        (t1.get('conscientiousness',0) - t2.get('conscientiousness',0))**2 +
        (t1.get('openness',0) - t2.get('openness',0))**2
    )

def render_graph_ml():
    page_header("University Neural Web", "Graph ML & Community Detection simulation.", "🕸️")
    
    st.markdown("This physics-based network graph visualizes the hidden social fabric of the university. Nodes represent individuals, and edges are drawn based on high personality compatibility. The physics engine automatically pulls highly compatible 'Super-Teams' together into distinct clusters.")
    
    with st.spinner("Generating Neural Web..."):
        # 1. Fetch data
        mentors = get_all_mentors()
        groups = get_all_groups()
        
        students = []
        for g in groups:
            students.extend(get_students_by_group(g['id']))
            
        nodes = []
        for m in mentors:
            nodes.append({"id": f"M_{m['id']}", "label": f"Dr. {m['name'].split()[-1]}", "type": "Mentor", "traits": m})
        for s in students:
            nodes.append({"id": f"S_{s['id']}", "label": s['name'], "type": "Student", "traits": s})
            
        # 2. Build NetworkX Graph
        G = nx.Graph()
        
        for n in nodes:
            if n["type"] == "Mentor":
                G.add_node(n["id"], label=n["label"], color="#8b5cf6", size=30, title="Mentor")
            else:
                G.add_node(n["id"], label=n["label"], color="#3b82f6", size=15, title="Student")
                
        # Calculate edges based on compatibility (distance)
        # Max distance in 5D space (0-5 scale) is approx 11.18
        threshold = st.slider("Compatibility Threshold (Lower = stricter matching)", 1.0, 6.0, 1.5)
        
        edge_count = 0
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                dist = calculate_distance(nodes[i]["traits"], nodes[j]["traits"])
                if dist < threshold:
                    # Weight is inverse of distance (closer = stronger pull)
                    weight = (threshold - dist) * 2 
                    G.add_edge(nodes[i]["id"], nodes[j]["id"], value=weight, color="#4b5563")
                    edge_count += 1
                    
        st.caption(f"Generated {len(nodes)} nodes and {edge_count} compatibility edges.")
        
        # 3. Create PyVis Network
        net = Network(height='800px', width='100%', bgcolor='#0e1117', font_color='white')
        net.from_nx(G)
        
        # Physics settings for the cool gravity effect
        net.set_options('''
        var options = {
          "physics": {
            "forceAtlas2Based": {
              "gravitationalConstant": -50,
              "centralGravity": 0.01,
              "springLength": 100,
              "springConstant": 0.08
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }
        }
        ''')
        
        # Save and read HTML
        path = "graph.html"
        net.save_graph(path)
        
        with open(path, 'r', encoding='utf-8') as f:
            html_data = f.read()
            
        # Display in Streamlit
        components.html(html_data, height=620)
        
        # Cleanup
        if os.path.exists(path):
            os.remove(path)
