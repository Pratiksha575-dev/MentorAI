# ui/pages/network.py

import math
import streamlit as st
import networkx as nx
import plotly.graph_objects as go

from ml.compatibility import calculate_compatibility
from config.constants import CLUSTER_INFO
from ui.components import page_header


# =========================================================
# NETWORK PAGE
# =========================================================

def render_network(profiles):

    page_header(
        "SOCIAL GRAPH",
        "See your network.",
        "Every person becomes a node. Stronger compatibility creates stronger connections."
    )

    # -----------------------------------------------------
    # EMPTY NETWORK
    # -----------------------------------------------------

    if not profiles:

        st.markdown("""
        <div class="hero">

            <div class="hero-content">

                <div class="ai-badge">
                    ✦ NETWORK VISUALIZATION
                </div>

                <div class="hero-title">
                    Your graph is waiting.
                </div>

                <div class="hero-text">
                    Create personality profiles to begin building
                    your compatibility network.
                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Create Profile →",
            type="primary",
            use_container_width=True
        ):

            st.session_state.current_page = "Create Profile"
            st.rerun()

        return

    # -----------------------------------------------------
    # NETWORK EXPLANATION
    # -----------------------------------------------------

    st.markdown("""
    <div class="glass-card">

        <div style="
            display:flex;
            align-items:center;
            gap:.8rem;
        ">

            <div style="
                font-size:1.4rem;
            ">
                ⌘
            </div>

            <div>

                <div style="
                    font-size:1rem;
                    font-weight:800;
                ">
                    ConnectAI Social Graph
                </div>

                <div style="
                    color:#77778d;
                    font-size:.75rem;
                    margin-top:.25rem;
                ">
                    Nodes represent people. Lines represent
                    meaningful compatibility relationships.
                </div>

            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # COMPATIBILITY THRESHOLD
    # -----------------------------------------------------

    threshold = st.slider(
        "Connection threshold",
        min_value=20,
        max_value=90,
        value=40,
        step=5,
        help=(
            "Only connections at or above this compatibility "
            "score are shown."
        )
    )

    # -----------------------------------------------------
    # BUILD GRAPH
    # -----------------------------------------------------

    graph = nx.Graph()

    for profile in profiles:

        graph.add_node(
            profile["id"],
            name=profile["name"],
            cluster=profile.get("cluster", 0)
        )

    # Calculate every pair
    for i, person_a in enumerate(profiles):

        for person_b in profiles[i + 1:]:

            try:

                score = calculate_compatibility(
                    person_a["traits"],
                    person_b["traits"],
                    person_a.get("interests", []),
                    person_b.get("interests", [])
                )

                overall = float(
                    score["overall"]
                )

                if overall >= threshold:

                    graph.add_edge(
                        person_a["id"],
                        person_b["id"],
                        weight=overall
                    )

            except Exception:

                continue

    # -----------------------------------------------------
    # NETWORK STATISTICS
    # -----------------------------------------------------

    total_people = len(profiles)
    total_connections = graph.number_of_edges()

    possible_connections = (
        total_people * (total_people - 1) / 2
    )

    if possible_connections > 0:

        density = (
            total_connections /
            possible_connections
        )

    else:

        density = 0

    connected_people = len(
        [
            node
            for node in graph.nodes()
            if graph.degree(node) > 0
        ]
    )

    # -----------------------------------------------------
    # STAT CARDS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""
        <div class="stat-card">

            <div class="stat-label">
                PEOPLE
            </div>

            <div class="stat-value">
                {total_people}
            </div>

            <div class="stat-description">
                Profiles in network
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="stat-card">

            <div class="stat-label">
                CONNECTIONS
            </div>

            <div class="stat-value">
                {total_connections}
            </div>

            <div class="stat-description">
                Above threshold
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="stat-card">

            <div class="stat-label">
                CONNECTED
            </div>

            <div class="stat-value">
                {connected_people}
            </div>

            <div class="stat-description">
                People with matches
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""
        <div class="stat-card">

            <div class="stat-label">
                DENSITY
            </div>

            <div class="stat-value">
                {density * 100:.1f}%
            </div>

            <div class="stat-description">
                Network density
            </div>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # SINGLE PERSON CASE
    # -----------------------------------------------------

    if len(profiles) == 1:

        st.info(
            "Add another profile to create your first connection."
        )

        return

    # -----------------------------------------------------
    # GRAPH LAYOUT
    # -----------------------------------------------------

    if len(graph.nodes()) > 1:

        positions = nx.spring_layout(
            graph,
            seed=42,
            k=1.5,
            iterations=80
        )

    else:

        positions = {
            node: (0, 0)
            for node in graph.nodes()
        }

    # -----------------------------------------------------
    # EDGES
    # -----------------------------------------------------

    edge_traces = []

    for person_a, person_b, data in graph.edges(
        data=True
    ):

        x0, y0 = positions[person_a]
        x1, y1 = positions[person_b]

        score = data["weight"]

        edge_traces.append(
            go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode="lines",
                line=dict(
                    width=max(
                        1,
                        min(5, score / 25)
                    )
                ),
                hoverinfo="text",
                text=[
                    f"{score:.1f}% compatibility"
                ]
            )
        )

    # -----------------------------------------------------
    # NODES
    # -----------------------------------------------------

    node_x = []
    node_y = []
    node_names = []
    node_hover = []
    node_sizes = []

    current_id = st.session_state.get(
        "current_profile_id"
    )

    for node in graph.nodes():

        x, y = positions[node]

        node_x.append(x)
        node_y.append(y)

        name = graph.nodes[node]["name"]

        node_names.append(name)

        degree = graph.degree(node)

        node_sizes.append(
            28 + degree * 4
        )

        node_hover.append(
            f"{name}<br>"
            f"Connections: {degree}"
        )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_names,
        textposition="bottom center",
        hovertext=node_hover,
        hoverinfo="text",
        marker=dict(
            size=node_sizes,
            line=dict(
                width=2
            )
        )
    )

    # -----------------------------------------------------
    # FIGURE
    # -----------------------------------------------------

    fig = go.Figure()

    for trace in edge_traces:

        fig.add_trace(trace)

    fig.add_trace(node_trace)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=650,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        xaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False
        ),

        hoverlabel=dict(
            bgcolor="#151522",
            bordercolor="#7c3aed",
            font=dict(
                color="white"
            )
        )
    )

    st.markdown("""
    <div class="eyebrow">
        NETWORK VISUALIZATION
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    # -----------------------------------------------------
    # STRONGEST CONNECTIONS
    # -----------------------------------------------------

    connections = []

    for person_a, person_b, data in graph.edges(
        data=True
    ):

        connections.append(
            (
                data["weight"],
                graph.nodes[person_a]["name"],
                graph.nodes[person_b]["name"]
            )
        )

    connections.sort(
        reverse=True
    )

    if connections:

        st.markdown("<br>", unsafe_allow_html=True)

        page_header(
            "STRONGEST LINKS",
            "Your closest connections.",
            "The strongest compatibility relationships currently visible in your network."
        )

        cols = st.columns(
            min(3, len(connections))
        )

        for index, (
            score,
            name_a,
            name_b
        ) in enumerate(
            connections[:3]
        ):

            with cols[index]:

                st.markdown(f"""
                <div class="profile-card">

                    <div style="
                        color:#77778d;
                        font-size:.7rem;
                        text-transform:uppercase;
                        letter-spacing:.08em;
                    ">
                        CONNECTION #{index + 1}
                    </div>

                    <div style="
                        font-size:1rem;
                        font-weight:800;
                        margin-top:.6rem;
                    ">
                        {name_a}
                        <span style="
                            color:#a78bfa;
                        ">
                            ×
                        </span>
                        {name_b}
                    </div>

                    <div style="
                        margin-top:.8rem;
                    ">

                        <span class="match-score">
                            {score:.1f}%
                        </span>

                    </div>

                    <div class="match-label">
                        compatibility
                    </div>

                </div>
                """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="glass-card"
             style="text-align:center;">

            <div style="
                font-size:1.4rem;
            ">
                ◌
            </div>

            <div style="
                font-weight:800;
                margin-top:.5rem;
            ">
                No connections at this threshold
            </div>

            <div style="
                color:#77778d;
                font-size:.78rem;
                margin-top:.4rem;
            ">
                Lower the connection threshold to reveal
                more relationships.
            </div>

        </div>
        """, unsafe_allow_html=True)