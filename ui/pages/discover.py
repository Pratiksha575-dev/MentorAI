# ui/pages/discover.py

import html
import streamlit as st

from ml.compatibility import calculate_compatibility
from config.constants import CLUSTER_INFO
from ui.components import page_header


# =========================================================
# SMALL UI HELPERS
# =========================================================

def _initial(name):
    name = str(name or "").strip()

    if not name:
        return "?"

    return html.escape(name[0].upper())


def _safe_name(name):
    return html.escape(str(name or "Unknown"))


def _metric_bar(label, value):
    """
    Render one compatibility metric with a visible gradient bar.
    """

    value = max(0.0, min(100.0, float(value)))

    return f"""
    <div style="margin-top:1rem;">

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            color:#85859a;
            font-size:.72rem;
            font-weight:600;
        ">
            <span>{label}</span>

            <span style="
                color:#d9d4e8;
                font-weight:700;
            ">
                {value:.1f}%
            </span>
        </div>

        <div style="
            width:100%;
            height:6px;
            background:rgba(255,255,255,.055);
            border-radius:999px;
            overflow:hidden;
            margin-top:.45rem;
        ">

            <div style="
                width:{value}%;
                height:100%;
                background:linear-gradient(
                    90deg,
                    #8b5cf6,
                    #ec4899
                );
                border-radius:999px;
                box-shadow:
                    0 0 10px rgba(168,85,247,.25);
            "></div>

        </div>

    </div>
    """


def _connection_chip(icon, text):
    return f"""
    <span style="
        display:inline-flex;
        align-items:center;
        gap:.4rem;
        padding:.42rem .72rem;
        border-radius:999px;
        background:rgba(255,255,255,.055);
        border:1px solid rgba(255,255,255,.08);
        color:#cfc9df;
        font-size:.69rem;
        white-space:nowrap;
    ">
        <span>{icon}</span>
        <span>{text}</span>
    </span>
    """


# =========================================================
# DISCOVER PAGE
# =========================================================

def render_discover(profiles):

    page_header(
        "DISCOVERY ENGINE",
        "Find your people.",
        "ConnectAI compares personality, interests and social energy to discover your strongest connections."
    )

    # =====================================================
    # NOT ENOUGH PROFILES
    # =====================================================

    if len(profiles) < 2:

        st.markdown("""
        <div class="hero">

            <div class="hero-content">

                <div class="ai-badge">
                    ✦ MATCHING ENGINE
                </div>

                <div class="hero-title">
                    Your network needs more people.
                </div>

                <div class="hero-text">
                    Create another profile to unlock compatibility
                    matching and discover meaningful connections.
                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Create Another Profile →",
            type="primary",
            width="stretch"
        ):

            st.session_state.current_page = "Create Profile"
            st.rerun()

        return

    # =====================================================
    # ACTIVE PROFILE
    # =====================================================

    current_id = st.session_state.get(
        "current_profile_id"
    )

    current = next(
        (
            profile
            for profile in profiles
            if profile.get("id") == current_id
        ),
        profiles[0]
    )

    # =====================================================
    # DISCOVERY FILTER
    # =====================================================

    st.markdown("""
    <div class="glass-card" style="
        padding:1.15rem 1.35rem;
        margin-top:.4rem;
        margin-bottom:.2rem;
    ">

        <div style="
            display:flex;
            align-items:center;
            gap:1rem;
        ">

            <div style="
                width:46px;
                height:46px;
                display:flex;
                align-items:center;
                justify-content:center;
                border-radius:14px;
                background:linear-gradient(
                    135deg,
                    rgba(139,92,246,.22),
                    rgba(236,72,153,.16)
                );
                border:1px solid rgba(167,139,250,.22);
                font-size:1.25rem;
                flex-shrink:0;
            ">
                ☷
            </div>

            <div style="
                flex:1;
                min-width:0;
            ">

                <div style="
                    color:#f2eff8;
                    font-size:.86rem;
                    font-weight:800;
                    margin-bottom:.25rem;
                ">
                    What kind of connection are you looking for?
                </div>

                <div style="
                    color:#77778d;
                    font-size:.7rem;
                ">
                    Choose a discovery mode to explore your network.
                </div>

            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

    mode_options = {
        "Overall compatibility": "overall_match",
        "Travel partner": "travel_partner",
        "Study buddy": "study_buddy",
        "Project teammate": "project_partner",
        "Friendship": "friendship",
        "Intellectual connection": "intellectual_match"
    }

    mode = st.selectbox(
        "Connection type",
        list(mode_options.keys()),
        label_visibility="collapsed",
        key="discover_mode"
    )

    purpose = mode_options[mode]

    # Keep the purpose available for future UI / scoring extensions.
    # The current calculate_compatibility() function remains the
    # source of truth for these discovery scores.
    _ = purpose

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # CALCULATE MATCHES
    # =====================================================

    results = []

    for person in profiles:

        if person["id"] == current["id"]:
            continue

        score = calculate_compatibility(
            current["traits"],
            person["traits"],
            current.get("interests", []),
            person.get("interests", [])
        )

        results.append(
            (person, score)
        )

    results.sort(
        key=lambda item: item[1]["overall"],
        reverse=True
    )

    if not results:
        return

    # =====================================================
    # TOP CONNECTION
    # =====================================================

    top_person, top_score = results[0]

    top_cluster = CLUSTER_INFO.get(
        int(top_person.get("cluster", 0)),
        {
            "name": "Unknown",
            "emoji": "✦"
        }
    )

    top_name = _safe_name(top_person["name"])

    # Determine useful labels from the actual scores.
    personality_text = (
        "Aligned Personality"
        if top_score["personality"] >= 75
        else "Compatible Personality"
    )

    interests_text = (
        "Similar Interests"
        if top_score["interests"] >= 50
        else "Different Interests"
    )

    energy_text = (
        "Balanced Energy"
        if top_score["social_energy"] >= 70
        else "Different Social Energy"
    )

    st.markdown(
        '<div class="eyebrow">✦ TOP CONNECTION</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div style="
        position:relative;
        overflow:hidden;
        border-radius:24px;
        padding:1.55rem;
        margin-top:.65rem;
        border:1px solid rgba(167,139,250,.42);
        background:
            radial-gradient(
                circle at 8% 50%,
                rgba(139,92,246,.22),
                transparent 35%
            ),
            radial-gradient(
                circle at 85% 70%,
                rgba(236,72,153,.16),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                rgba(91,33,182,.18),
                rgba(236,72,153,.08)
            );
        box-shadow:
            0 0 35px rgba(139,92,246,.08),
            inset 0 1px 0 rgba(255,255,255,.04);
    ">

        <div style="
            position:relative;
            z-index:2;
            display:grid;
            grid-template-columns:110px 1fr 225px;
            gap:1.5rem;
            align-items:center;
        ">

            <!-- AVATAR WITH CROWN -->

                <div style="
                    display:flex;
                    justify-content:center;
                    align-items:center;
                ">

                    <div style="
                        position:relative;
                        width:105px;
                        height:112px;
                        display:flex;
                        justify-content:center;
                        align-items:flex-end;
                    ">

                        <!-- FLOATING CROWN -->

                        <div style="
                            position:absolute;
                            top:-4px;
                            left:50%;
                            transform:translateX(-50%);
                            z-index:5;
                            font-size:1.65rem;
                            filter:
                                drop-shadow(0 0 8px rgba(250,204,21,.55))
                                drop-shadow(0 0 16px rgba(236,72,153,.25));
                        ">
                            👑
                        </div>

                        <!-- AVATAR -->

                        <div style="
                            width:92px;
                            height:92px;
                            border-radius:50%;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            font-size:2.25rem;
                            font-weight:850;
                            color:white;
                            background:
                                linear-gradient(
                                    135deg,
                                    #8b5cf6,
                                    #ec4899
                                );
                            border:5px solid rgba(255,255,255,.08);
                            box-shadow:
                                0 0 0 8px rgba(139,92,246,.08),
                                0 0 30px rgba(236,72,153,.25);
                        ">
                            {_initial(top_person["name"])}
                        </div>

                    </div>

                </div>

            <!-- PROFILE INFORMATION -->

            <div>

                <div class="ai-badge">
                    #1 MATCH · {html.escape(mode.upper())}
                </div>

                <div style="
                    font-size:2rem;
                    line-height:1.05;
                    font-weight:850;
                    margin-top:.65rem;
                    letter-spacing:-.03em;
                ">
                    {top_name}
                </div>

                <div style="
                    color:#aaaabc;
                    font-size:.82rem;
                    margin-top:.45rem;
                ">
                    {top_cluster["emoji"]} {html.escape(top_cluster["name"])}
                </div>

                <div style="
                    color:#85859a;
                    font-size:.75rem;
                    margin-top:.65rem;
                ">
                    Your strongest connection in the current network.
                </div>

                <div style="
                    display:flex;
                    flex-wrap:wrap;
                    gap:.5rem;
                    margin-top:1rem;
                ">

                    {_connection_chip("◉", personality_text)}

                    {_connection_chip("♥", interests_text)}

                    {_connection_chip("ϟ", energy_text)}

                </div>

            </div>

            <!-- SCORE -->

            <div style="
                text-align:center;
                padding:1.15rem 1rem;
                border-radius:18px;
                background:rgba(255,255,255,.045);
                border:1px solid rgba(255,255,255,.07);
            ">

                <div class="match-score">
                    {top_score["overall"]:.1f}%
                </div>

                <div class="match-label">
                    OVERALL COMPATIBILITY
                </div>

                <div style="
                    height:1px;
                    background:rgba(255,255,255,.08);
                    margin:1rem 0 .8rem;
                "></div>

                <div style="
                    color:#85859a;
                    font-size:.68rem;
                    line-height:1.5;
                ">
                    Personality · Interests · Social Energy
                </div>

                <div style="
                    color:#d7cce9;
                    font-size:.7rem;
                    font-style:italic;
                    margin-top:.65rem;
                ">
                    Great potential for a meaningful connection
                </div>

            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # MATCH RANKING
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)

    page_header(
        "MATCH RANKING",
        "Your compatibility landscape.",
        "Higher scores indicate stronger overall compatibility."
    )

    # =====================================================
    # MATCH CARDS
    # =====================================================

    cols = st.columns(2)

    for index, (person, score) in enumerate(results):

        with cols[index % 2]:

            cluster = CLUSTER_INFO.get(
                int(person.get("cluster", 0)),
                {
                    "name": "Unknown",
                    "emoji": "✦"
                }
            )

            person_name = _safe_name(
                person.get("name", "Unknown")
            )

            # -------------------------------------------------
            # CARD
            # -------------------------------------------------

            st.markdown(f"""
            <div style="
                min-height:395px;
                box-sizing:border-box;
                display:flex;
                flex-direction:column;
                padding:1.35rem;
                margin-bottom:.35rem;
                border-radius:20px;
                border:1px solid rgba(255,255,255,.085);
                background:
                    linear-gradient(
                        145deg,
                        rgba(255,255,255,.045),
                        rgba(255,255,255,.018)
                    );
                box-shadow:
                    inset 0 1px 0 rgba(255,255,255,.025),
                    0 12px 35px rgba(0,0,0,.14);
            ">

                <!-- HEADER -->

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:flex-start;
                    gap:1rem;
                ">

                    <div style="
                        display:flex;
                        align-items:center;
                        gap:.8rem;
                    ">

                        <div style="
                            width:46px;
                            height:46px;
                            flex-shrink:0;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            border-radius:14px;
                            background:
                                linear-gradient(
                                    135deg,
                                    rgba(139,92,246,.25),
                                    rgba(236,72,153,.18)
                                );
                            border:1px solid rgba(167,139,250,.18);
                            color:#e9ddff;
                            font-size:1.2rem;
                            font-weight:850;
                        ">
                            {_initial(person.get("name"))}
                        </div>

                        <div>

                            <div style="
                                color:#77778d;
                                font-size:.68rem;
                                font-weight:700;
                                letter-spacing:.04em;
                            ">
                                #{index + 1}
                            </div>

                            <div style="
                                font-size:1.15rem;
                                font-weight:850;
                                margin-top:.18rem;
                            ">
                                {person_name}
                            </div>

                            <div style="
                                color:#85859a;
                                font-size:.72rem;
                                margin-top:.2rem;
                            ">
                                {cluster["emoji"]} {html.escape(cluster["name"])}
                            </div>

                        </div>

                    </div>

                    <div style="
                        text-align:right;
                        flex-shrink:0;
                    ">

                        <div class="match-score">
                            {score["overall"]:.1f}%
                        </div>

                        <div class="match-label">
                            COMPATIBILITY
                        </div>

                    </div>

                </div>

                <!-- METRICS -->

                <div style="
                    margin-top:1.15rem;
                    padding-top:.25rem;
                ">

                    {_metric_bar(
                        "PERSONALITY",
                        score["personality"]
                    )}

                    {_metric_bar(
                        "INTERESTS",
                        score["interests"]
                    )}

                    {_metric_bar(
                        "SOCIAL ENERGY",
                        score["social_energy"]
                    )}

                </div>

                <!-- BOTTOM NOTE -->

                <div style="
                    margin-top:auto;
                    padding-top:1.1rem;
                    color:#66667a;
                    font-size:.67rem;
                ">
                    Personality · Interests · Social Energy
                </div>

            </div>
            """, unsafe_allow_html=True)

            # -------------------------------------------------
            # COMPARE BUTTON
            # -------------------------------------------------

            if st.button(
                "Compare →",
                key=f"discover_compare_{person['id']}",
                type="primary",
                width="stretch"
            ):

                st.session_state.compare_profile_id = person["id"]

                st.session_state.current_page = "Compare"

                st.rerun()

            st.markdown(
                "<div style='height:1rem'></div>",
                unsafe_allow_html=True
            )