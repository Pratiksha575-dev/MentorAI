# ui/pages/profiles.py

import streamlit as st

from config.constants import CLUSTER_INFO
from ui.components import page_header


def render_profiles(profiles):

    page_header(
        "YOUR PEOPLE",
        "Profiles in the network.",
        "Explore the personalities that have joined your ConnectAI network."
    )

    if not profiles:

        st.markdown("""
        <div class="hero">
            <div class="hero-content">

                <div class="ai-badge">
                    ✦ NETWORK EMPTY
                </div>

                <div class="hero-title">
                    Your network starts here.
                </div>

                <div class="hero-text">
                    Create the first personality profile and start
                    building your ConnectAI network.
                </div>

            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Create First Profile  →",
            type="primary",
            width="stretch"
        ):
            st.session_state.current_page = "Create Profile"
            st.rerun()

        return

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    search = st.text_input(
        "Search profiles",
        placeholder="Search by name..."
    )

    filtered = profiles

    if search.strip():

        filtered = [
            p for p in profiles
            if search.lower() in p.get("name", "").lower()
        ]

    st.markdown(
        f"""
        <div style="
            color:#77778d;
            font-size:.78rem;
            margin:1rem 0 1.2rem;
        ">
            {len(filtered)} profile(s) found
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # PROFILE GRID
    # --------------------------------------------------

    # Larger gap gives the cards more breathing room.
    cols = st.columns(
        3,
        gap="large"
    )

    for index, profile in enumerate(filtered):

        with cols[index % 3]:

            name = profile.get("name", "Unknown")
            cluster = profile.get("cluster", 0)

            info = CLUSTER_INFO.get(
                int(cluster),
                {
                    "name": f"Cluster {cluster}",
                    "emoji": "✦",
                    "description": ""
                }
            )

            initial = (
                name.strip()[0].upper()
                if name.strip()
                else "?"
            )

            interests = profile.get("interests", [])

            if isinstance(interests, str):
                interests = []

            interest_text = ", ".join(
                interests[:4]
            )

            # --------------------------------------------------
            # PROFILE CARD
            # --------------------------------------------------

            st.markdown(
                f"""
                <div class="profile-card">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                    ">

                        <div class="profile-avatar">
                            {initial}
                        </div>

                        <div style="
                            color:#a78bfa;
                            font-size:.7rem;
                            font-weight:700;
                        ">
                            ID #{profile.get("id", "")}
                        </div>

                    </div>

                    <div style="
                        font-size:1.15rem;
                        font-weight:800;
                        margin-top:1rem;
                    ">
                        {name}
                    </div>

                    <div style="
                        color:#aaaabc;
                        font-size:.78rem;
                        margin-top:.35rem;
                    ">
                        {info["emoji"]} {info["name"]}
                    </div>

                    <div style="
                        color:#707087;
                        font-size:.75rem;
                        line-height:1.6;
                        margin-top:.8rem;
                        min-height:48px;
                    ">
                        {info["description"]}
                    </div>

                    <div style="
                        margin-top:1rem;
                        color:#89899d;
                        font-size:.72rem;
                    ">
                        {interest_text
                        if interest_text
                        else "No interests added"}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            # --------------------------------------------------
            # SPACE BETWEEN CARD AND BUTTON
            # --------------------------------------------------

            st.markdown(
                "<div style='height:14px;'></div>",
                unsafe_allow_html=True
            )

            # --------------------------------------------------
            # VIEW PROFILE BUTTON
            # --------------------------------------------------

            if st.button(
                "View Profile  →",
                key=f"profile_view_{profile['id']}",
                width="stretch"
            ):

                st.session_state.current_profile_id = profile["id"]
                st.session_state.current_page = "My Personality"

                st.rerun()

            # --------------------------------------------------
            # SPACE BEFORE NEXT ROW
            # --------------------------------------------------

            st.markdown(
                "<div style='height:28px;'></div>",
                unsafe_allow_html=True
            )