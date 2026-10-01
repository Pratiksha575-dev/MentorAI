# ui/pages/ask_connectai.py

import json
import html
import re
import streamlit as st

from llm import ask_ollama
from ml.compatibility import calculate_query_compatibility
from ui.components import page_header, ai_card


# =========================================================
# CONNECTAI AI PAGE
# =========================================================

def render_ask_connectai(profiles):

    page_header(
        "CONNECTAI AI",
        "Ask your network anything.",
        "Describe what you're looking for naturally. ConnectAI interprets your request and searches the compatibility network."
    )

    # -----------------------------------------------------
    # NO PROFILES
    # -----------------------------------------------------

    if not profiles:

        st.markdown("""
        <div class="hero">

            <div class="hero-content">

                <div class="ai-badge">
                    ✦ CONNECTAI INTELLIGENCE
                </div>

                <div class="hero-title">
                    Your AI network is waiting.
                </div>

                <div class="hero-text">
                    Create your first personality profile before
                    asking ConnectAI to discover connections.
                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Create My Profile →",
            type="primary",
            use_container_width=True
        ):

            st.session_state.current_page = "Create Profile"
            st.rerun()

        return

    # -----------------------------------------------------
    # ACTIVE PROFILE
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # AI INTRO
    # -----------------------------------------------------

    st.markdown(f"""
    <div class="hero">

        <div class="hero-content">

            <div class="ai-badge">
                ✦ AI NETWORK ASSISTANT
            </div>

            <div style="
                font-size:1.9rem;
                font-weight:800;
                margin-top:1rem;
            ">
                Hey {html.escape(current["name"])} 👋
            </div>

            <div class="hero-text">
                Tell me what kind of person you're looking for.
                I'll translate your request into personality priorities,
                calculate real compatibility scores and explain the results.
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # EXAMPLE PROMPTS
    # -----------------------------------------------------

    st.markdown("""
    <div class="glass-card">

        <div style="
            font-weight:800;
            font-size:1rem;
        ">
            ✦ Try asking
        </div>

        <div style="
            color:#77778d;
            font-size:.76rem;
            line-height:1.7;
            margin-top:.45rem;
        ">
            Natural language works — you don't need to know
            anything about personality models.
        </div>

        <div style="
            display:flex;
            flex-wrap:wrap;
            gap:.55rem;
            margin-top:1rem;
        ">

            <span class="ai-badge">
                Best travel partner?
            </span>

            <span class="ai-badge">
                Good study buddy?
            </span>

            <span class="ai-badge">
                Best project teammate?
            </span>

            <span class="ai-badge">
                Who complements me?
            </span>

            <span class="ai-badge">
                Who would challenge me intellectually?
            </span>

            <span class="ai-badge">
                Who would make a great friend?
            </span>

        </div>

    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # QUERY INPUT
    # -----------------------------------------------------

    query = st.text_area(
        "Ask ConnectAI",
        placeholder=(
            "Example: Who would be the best partner for travelling?"
        ),
        height=130,
        key="connectai_query"
    )

    ask_button = st.button(
        "Ask ConnectAI  ✦",
        type="primary",
        use_container_width=True,
        key="ask_connectai_button"
    )

    if not ask_button:
        return

    if not query.strip():

        st.warning(
            "Enter a question first."
        )

        return

    # -----------------------------------------------------
    # AI PROCESSING
    # -----------------------------------------------------

    with st.spinner(
        "ConnectAI is analyzing your question..."
    ):

        # =================================================
        # STEP 1 — OLLAMA INTENT PARSING
        # =================================================

        prompt = f"""
You are the intent parser for ConnectAI,
an AI personality compatibility application.

The user is asking:

"{query}"

Your job is to convert this request into structured JSON.

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations.

Use exactly this structure:

{{
    "purpose": "overall_match",
    "important_traits": {{
        "Extraversion": 0.20,
        "Neuroticism": 0.15,
        "Agreeableness": 0.25,
        "Conscientiousness": 0.20,
        "Openness": 0.20
    }},
    "important_factors": [
        "shared_interests",
        "social_energy"
    ]
}}

Allowed purpose values:

- overall_match
- travel_partner
- study_buddy
- project_partner
- friendship
- intellectual_match
- adventure_partner
- team_member

Interpret the user's intention carefully.

Examples:

Travel questions should usually favor:
- Openness
- Extraversion
- Agreeableness
- shared interests
- social energy

Study questions should usually favor:
- Conscientiousness
- Openness
- intellectual curiosity

Project/team questions should usually favor:
- Conscientiousness
- Agreeableness
- Extraversion
- shared interests

Friendship questions should usually favor:
- Agreeableness
- Extraversion
- shared interests

Intellectual questions should usually favor:
- Openness
- Conscientiousness
- intellectual curiosity

The five trait weights must add up approximately to 1.0.
"""

        raw = ask_ollama(
            prompt,
            model="llama3.2:latest",
            num_predict=180,
            temperature=0.1,
            timeout=45
        )

        # =================================================
        # STEP 2 — PARSE OLLAMA JSON
        # =================================================

        intent = None

        try:

            start = raw.find("{")
            end = raw.rfind("}") + 1

            if start != -1 and end > start:

                intent = json.loads(
                    raw[start:end]
                )

        except Exception:

            intent = None

        # =================================================
        # STEP 3 — SAFE FALLBACK
        # =================================================

        if not isinstance(intent, dict):

            intent = {
                "purpose": "overall_match",

                "important_traits": {
                    "Extraversion": 0.20,
                    "Neuroticism": 0.15,
                    "Agreeableness": 0.25,
                    "Conscientiousness": 0.20,
                    "Openness": 0.20
                },

                "important_factors": [
                    "shared_interests",
                    "social_energy"
                ]
            }

        # -------------------------------------------------
        # NORMALIZE PURPOSE
        # -------------------------------------------------

        purpose = str(
            intent.get(
                "purpose",
                "overall_match"
            )
        ).strip().lower()

        allowed_purposes = {
            "overall_match",
            "travel_partner",
            "study_buddy",
            "project_partner",
            "friendship",
            "intellectual_match",
            "adventure_partner",
            "team_member"
        }

        if purpose not in allowed_purposes:
            purpose = "overall_match"

        intent["purpose"] = purpose

        # =================================================
        # STEP 4 — CALCULATE REAL COMPATIBILITY
        # =================================================

        matches = []

        for person in profiles:

            if person["id"] == current["id"]:
                continue

            try:

                score = calculate_query_compatibility(
                    current["traits"],
                    person["traits"],
                    current.get("interests", []),
                    person.get("interests", []),
                    intent
                )

                matches.append(
                    (
                        person,
                        score
                    )
                )

            except Exception:
                continue

        # =================================================
        # STEP 5 — SORT
        # =================================================

        matches.sort(
            key=lambda item: item[1].get(
                "overall",
                0
            ),
            reverse=True
        )

    # -----------------------------------------------------
    # NO MATCHES
    # -----------------------------------------------------

    if not matches:

        st.warning(
            "There are no other profiles available to compare yet."
        )

        return

    top_matches = matches[:3]

    # =====================================================
    # AI RESULT
    # =====================================================

    result_text = ""

    for rank, (person, score) in enumerate(
        top_matches,
        start=1
    ):

        result_text += f"""
#{rank} — {person["name"]}

Overall compatibility: {score["overall"]}%
Personality compatibility: {score["personality"]}%
Interest compatibility: {score["interests"]}%
Social energy compatibility: {score["social_energy"]}%
"""

    # -----------------------------------------------------
    # OLLAMA EXPLANATION
    # -----------------------------------------------------

    explanation_prompt = f"""
You are ConnectAI,
an AI personality compatibility assistant.

Current user:
{current["name"]}

User's question:
{query}

Interpreted purpose:
{purpose}

Calculated results:

{result_text}

Explain the result in a friendly and intelligent way.

Rules:

1. Never invent scores.
2. Never change the ranking.
3. Never claim scientific certainty.
4. Use the calculated scores as the source of truth.
5. Explain why the top person fits the user's request.
6. Mention one useful trade-off if appropriate.
7. Keep the explanation concise.
8. Do not mention internal JSON or programming.
"""

    with st.spinner(
        "Generating your ConnectAI insight..."
    ):

        explanation = ask_ollama(
            explanation_prompt,
            model="llama3.1:8b",
            num_predict=420,
            temperature=0.45,
            timeout=90
        )

    # =====================================================
    # DISPLAY AI ANSWER
    # =====================================================

    # Clean any markdown artifacts Ollama may still return.
    clean_lines = []
    for line in str(explanation or "").splitlines():
        line = line.strip()
        line = line.replace("**", "").replace("__", "")
        while line.startswith("#"):
            line = line[1:].lstrip()
        line = re.sub(r"^[•*+\-]\s+", "", line)
        line = re.sub(r"^\d+[.)]\s+", "", line)
        if line:
            clean_lines.append(line)

    cleaned_explanation = "\n\n".join(clean_lines)
    explanation_html = html.escape(cleaned_explanation).replace(
        "\n\n", "</p><p>"
    ).replace("\n", "<br>")

    st.markdown(f"""
    <div style="
        margin-top:.25rem;
        margin-bottom:1.8rem;
        padding:1.9rem 2rem 2.05rem;
        border-radius:24px;
        background:linear-gradient(135deg,rgba(139,92,246,.12),rgba(236,72,153,.055));
        border:1px solid rgba(167,110,255,.20);
        box-shadow:0 18px 55px rgba(0,0,0,.22), inset 0 1px 0 rgba(255,255,255,.035);
    ">
        <div class="ai-badge">✦ CONNECTAI INTELLIGENCE</div>
        <div style="font-size:1.65rem;font-weight:800;margin-top:1.15rem;margin-bottom:1rem;">
            ConnectAI's answer
        </div>
        <div style="color:#c1b9cf;font-size:.95rem;line-height:1.9;overflow-wrap:anywhere;">
            <p style="margin:0;">{explanation_html}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # INTERPRETED INTENT
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="glass-card">

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">

            <div>

                <div style="
                    color:#77778d;
                    font-size:.7rem;
                    text-transform:uppercase;
                    letter-spacing:.08em;
                ">
                    CONNECTAI UNDERSTOOD
                </div>

                <div style="
                    font-size:1.15rem;
                    font-weight:800;
                    margin-top:.4rem;
                ">
                    {purpose.replace("_", " ").title()}
                </div>

            </div>

            <div class="ai-badge">
                AI INTERPRETED
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # MATCH RESULTS
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)

    page_header(
        "MATCH RESULTS",
        "People ConnectAI found.",
        f"Top matches for your {purpose.replace('_', ' ')} request."
    )

    for rank, (person, score) in enumerate(
        top_matches,
        start=1
    ):

        initial = (
            person["name"].strip()[0].upper()
            if person["name"].strip()
            else "?"
        )

        st.markdown(f"""
        <div class="profile-card">

            <div style="
                display:flex;
                align-items:center;
                justify-content:space-between;
                gap:1rem;
            ">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:1rem;
                ">

                    <div style="
                        color:#77778d;
                        font-size:.75rem;
                        font-weight:700;
                    ">
                        #{rank}
                    </div>

                    <div class="profile-avatar">
                        {initial}
                    </div>

                    <div>

                        <div style="
                            font-size:1.1rem;
                            font-weight:800;
                        ">
                            {html.escape(person["name"])}
                        </div>

                        <div style="
                            color:#77778d;
                            font-size:.72rem;
                            margin-top:.25rem;
                        ">
                            Personality · Interests · Social Energy
                        </div>

                    </div>

                </div>

                <div style="
                    text-align:right;
                ">

                    <div class="match-score">
                        {score["overall"]:.1f}%
                    </div>

                    <div class="match-label">
                        compatibility
                    </div>

                </div>

            </div>

            <div style="
                display:grid;
                grid-template-columns:repeat(3,1fr);
                gap:.8rem;
                margin-top:1.2rem;
            ">

                <div>
                    <div style="
                        color:#66667a;
                        font-size:.67rem;
                    ">
                        PERSONALITY
                    </div>

                    <div style="
                        font-weight:700;
                        margin-top:.2rem;
                    ">
                        {score["personality"]:.1f}%
                    </div>
                </div>

                <div>
                    <div style="
                        color:#66667a;
                        font-size:.67rem;
                    ">
                        INTERESTS
                    </div>

                    <div style="
                        font-weight:700;
                        margin-top:.2rem;
                    ">
                        {score["interests"]:.1f}%
                    </div>
                </div>

                <div>
                    <div style="
                        color:#66667a;
                        font-size:.67rem;
                    ">
                        SOCIAL ENERGY
                    </div>

                    <div style="
                        font-weight:700;
                        margin-top:.2rem;
                    ">
                        {score["social_energy"]:.1f}%
                    </div>
                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)

        # Clear breathing room between the profile card and its action.
        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        if st.button(
            f"Compare with {person['name']} →",
            key=f"ai_compare_{person['id']}",
            use_container_width=True
        ):

            st.session_state.compare_profile_id = person["id"]
            st.session_state.current_page = "Compare"
            st.rerun()

        # Larger separation before the next result card.
        if rank < len(top_matches):
            st.markdown("<div style='height:1.35rem;'></div>", unsafe_allow_html=True)