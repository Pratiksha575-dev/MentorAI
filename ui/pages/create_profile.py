 
import streamlit as st

from config.questions import (
    QUESTIONS,
    SECTIONS,
    SCALE_OPTIONS,
    SCALE_LABELS
)

from config.constants import (
    INTEREST_OPTIONS,
    CLUSTER_INFO
)

from ml.personality_model import analyze_personality
from database import save_profile
from llm import generate_personality_summary

from ui.components import page_header

# =========================================================
# CONNECTAI ASSESSMENT PROGRESS UI
# =========================================================

st.markdown(
    """
    <style>

    .ca-progress-card {
        margin-top: 1.15rem;
        margin-bottom: 1.35rem;
        padding: 1rem 1.15rem 1.05rem;
        border-radius: 16px;
        border: 1px solid rgba(167, 139, 250, 0.16);
        background:
            linear-gradient(
                135deg,
                rgba(24, 20, 42, 0.88),
                rgba(12, 12, 25, 0.92)
            );
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.035),
            0 10px 28px rgba(0,0,0,0.12);
    }

    .ca-progress-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: .65rem;
    }

    .ca-progress-label {
        color: #aaa3b9;
        font-size: .68rem;
        font-weight: 750;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    .ca-progress-value {
        color: #e5cfff;
        font-size: .72rem;
        font-weight: 850;
        white-space: nowrap;
    }

    .ca-progress-value span {
        color: #777184;
        font-weight: 600;
    }

    .ca-progress-track {
        position: relative;
        width: 100%;
        height: 9px;
        overflow: hidden;
        border-radius: 999px;
        background: rgba(255,255,255,.055);
        box-shadow: inset 0 1px 3px rgba(0,0,0,.35);
    }

    .ca-progress-fill {
        position: relative;
        height: 100%;
        min-width: 0;
        border-radius: 999px;
        background:
            linear-gradient(
                90deg,
                #8b5cf6 0%,
                #c65af1 48%,
                #ec4899 100%
            );
        box-shadow:
            0 0 14px rgba(217,70,239,.32),
            0 0 28px rgba(139,92,246,.14);
        transition: width .35s ease;
    }

    .ca-progress-fill::after {
        content: "";
        position: absolute;
        top: 1px;
        right: 2px;
        width: 22px;
        height: 7px;
        border-radius: 999px;
        background: rgba(255,255,255,.42);
        filter: blur(3px);
        opacity: .65;
    }

    .ca-progress-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-top: .58rem;
        color: #625e6d;
        font-size: .61rem;
    }

    .ca-progress-footer strong {
        color: #a995c5;
        font-weight: 750;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# =========================================================
# HELPERS
# =========================================================

def get_saved_answer(index):
    """
    Return an existing answer if the user has already answered
    this question.
    """
    
    if not isinstance(st.session_state.get('assessment_answers'), dict):
        st.session_state.assessment_answers = {}

    key = f"question_{index}"

    if key in st.session_state:
        st.session_state.assessment_answers[index] = st.session_state[key]
        return st.session_state[key]
        
    if index in st.session_state.assessment_answers:
        return st.session_state.assessment_answers[index]

    return None


def save_current_answers():
    """
    Answers are already stored by Streamlit widgets in
    session_state. This helper exists to keep the flow explicit.
    """

    answers = []
    missing = []

    for index in range(50):
        answer = get_saved_answer(index)

        if answer is None:
            missing.append(index)
        else:
            answers.append(answer)

    if missing:
        print(f"Missing answers for indices: {missing}")
        print(f"Current assessment_answers: {st.session_state.get('assessment_answers')}")
        return None

    return answers


# =========================================================
# MAIN PAGE
# =========================================================

def render_create_profile():

    page_header(
        "PERSONALITY ASSESSMENT",
        "Create your profile.",
        "Answer honestly. There are no right or wrong answers — your responses help ConnectAI understand your personality."
    )

    # =====================================================
    # INTRO
    # =====================================================

    st.markdown("""
    <div class="hero">

        <div class="hero-content">

            <div class="ai-badge">
                ✦ 50 QUESTION PERSONALITY ENGINE
            </div>

            <div style="
                font-size:1.8rem;
                font-weight:800;
                margin-top:1rem;
            ">
                Let's discover what makes you, you.
            </div>

            <div style="
                color:#aaaabc;
                line-height:1.7;
                margin-top:.7rem;
                max-width:720px;
            ">
                Your answers are analyzed using a Big Five personality
                model and machine learning. ConnectAI then uses local AI
                to generate a personalized interpretation.
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    st.markdown(
        '<div class="eyebrow">01 · BASIC INFORMATION</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:

        name = st.text_input(
            "Your name",
            placeholder="Enter your name",
            key="profile_name"
        )
        
    with col2:
        role = st.selectbox(
            "Role",
            options=["mentee", "mentor"],
            format_func=lambda x: "Student Group" if x == "mentee" else "Faculty Mentor",
            key="profile_role"
        )

    with col3:

        interests = st.multiselect(
            "Your interests",
            INTEREST_OPTIONS,
            placeholder="Choose things you enjoy..."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # PERSONALITY ASSESSMENT
    # =====================================================

    st.markdown(
        '<div class="eyebrow">02 · PERSONALITY QUESTIONS</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div style="
        color:#88889d;
        font-size:.82rem;
        margin-bottom:1rem;
    ">
        Five dimensions. Ten questions each. Choose the answer
        that feels most like you.
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # CURRENT SECTION
    # -----------------------------------------------------

    if "assessment_section" not in st.session_state:
        st.session_state.assessment_section = 0

    current_section = st.session_state.assessment_section

    current_section = max(
        0,
        min(current_section, len(SECTIONS) - 1)
    )

    st.session_state.assessment_section = current_section

    section = SECTIONS[current_section]

    start = section["start"]
    end = section["end"]

    # =====================================================
    # CONNECTAI CUSTOM PROGRESS
    # =====================================================

    answered_in_section = 0

    for question_index in range(start, end):
        if get_saved_answer(question_index) is not None:
            answered_in_section += 1

    completed_questions = start + answered_in_section

    progress_percent = int(
        (completed_questions / 50) * 100
    )

    st.markdown(
        f"""
        <div style="
            margin:1.15rem 0 1.25rem;
            padding:1rem 1.15rem 1.05rem;
            border-radius:16px;
            border:1px solid rgba(167,139,250,.16);
            background:
                linear-gradient(
                    135deg,
                    rgba(24,20,42,.92),
                    rgba(12,12,25,.96)
                );
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,.035),
                0 10px 28px rgba(0,0,0,.14);
        ">

            <div style="
                display:flex;
                align-items:center;
                justify-content:space-between;
                gap:1rem;
                margin-bottom:.7rem;
            ">

                <div style="
                    color:#aaa3b9;
                    font-size:.68rem;
                    font-weight:750;
                    letter-spacing:.08em;
                    text-transform:uppercase;
                ">
                    Assessment progress
                </div>

                <div style="
                    color:#e5cfff;
                    font-size:.72rem;
                    font-weight:850;
                    white-space:nowrap;
                ">
                    {completed_questions}
                    <span style="
                        color:#777184;
                        font-weight:600;
                    ">
                        / 50 questions
                    </span>
                </div>

            </div>

            <div style="
                width:100%;
                height:9px;
                overflow:hidden;
                border-radius:999px;
                background:rgba(255,255,255,.065);
                box-shadow:inset 0 1px 3px rgba(0,0,0,.38);
            ">

                <div style="
                    width:{progress_percent}%;
                    height:9px;
                    border-radius:999px;
                    background:
                        linear-gradient(
                            90deg,
                            #8b5cf6 0%,
                            #c65af1 50%,
                            #ec4899 100%
                        );
                    box-shadow:
                        0 0 12px rgba(217,70,239,.38),
                        0 0 25px rgba(139,92,246,.16);
                "></div>

            </div>

            <div style="
                display:flex;
                align-items:center;
                justify-content:space-between;
                gap:1rem;
                margin-top:.6rem;
                color:#625e6d;
                font-size:.61rem;
            ">

                <div>
                    Section
                    <span style="
                        color:#a995c5;
                        font-weight:750;
                    ">
                        {current_section + 1} of 5
                    </span>
                </div>

                <div>
                    <span style="
                        color:#a995c5;
                        font-weight:750;
                    ">
                        {progress_percent}%
                    </span>
                    complete
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # SECTION CARD
    # =====================================================

    st.markdown(f"""
    <div class="glass-card">

        <div style="
            color:#77778d;
            font-size:.78rem;
            line-height:1.6;
        ">
            {section["name"]} explores one part of your personality.
            There are no correct answers — go with your first instinct.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # QUESTIONS
    # =====================================================

    for question_index in range(start, end):

        code, question = QUESTIONS[question_index]

        saved = get_saved_answer(question_index)
        default_index = SCALE_OPTIONS.index(saved) if saved in SCALE_OPTIONS else 0

        st.radio(
            f"{question_index + 1}. {question}",
            SCALE_OPTIONS,
            format_func=lambda x: SCALE_LABELS[x],
            horizontal=True,
            key=f"question_{question_index}",
            index=default_index
        )

        if question_index < end - 1:

            st.markdown(
                "<div style='height:10px'></div>",
                unsafe_allow_html=True
            )

    # =====================================================
    # NAVIGATION
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)

    nav_left, nav_mid, nav_right = st.columns(
        [1, 2, 1]
    )

    # -----------------------------------------------------
    # BACK
    # -----------------------------------------------------

    with nav_left:

        if current_section > 0:

            if st.button(
                "← Previous",
                width="stretch",
                key=f"previous_section_{current_section}"
            ):

                st.session_state.assessment_section -= 1
                st.rerun()

    # -----------------------------------------------------
    # SECTION STATUS
    # -----------------------------------------------------

    with nav_mid:

        st.markdown(
            f"""
            <div style="
                text-align:center;
                color:#77778d;
                font-size:.78rem;
                padding-top:.6rem;
            ">
                Section {current_section + 1} of 5
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # NEXT / ANALYZE
    # -----------------------------------------------------

    with nav_right:

        if current_section < len(SECTIONS) - 1:

            if st.button(
                "Next →",
                type="primary",
                width="stretch",
                key=f"next_section_{current_section}"
            ):

                missing = []

                for question_index in range(start, end):

                    if get_saved_answer(question_index) is None:
                        missing.append(question_index + 1)

                if missing:

                    st.warning(
                        f"Please answer all questions in this section first."
                    )

                else:

                    st.session_state.assessment_section += 1
                    st.rerun()

        else:

            if st.button(
                "Analyze My Working Style ✦",
                type="primary",
                width="stretch",
                key="analyze_personality_button"
            ):

                # -----------------------------------------
                # BASIC VALIDATION
                # -----------------------------------------

                if not name.strip():

                    st.error(
                        "Please enter your name first."
                    )

                    st.stop()

                # -----------------------------------------
                # COLLECT ALL ANSWERS
                # -----------------------------------------

                answers = save_current_answers()

                if answers is None:

                    st.error(
                        "Please answer all 50 personality questions."
                    )

                    st.stop()

                # -----------------------------------------
                # ML ANALYSIS
                # -----------------------------------------

                with st.spinner(
                    "ConnectAI is analyzing your personality..."
                ):

                    try:

                        result = analyze_personality(
                            answers
                        )

                        traits = result["traits"]
                        cluster = result["cluster"]

                        cluster_info = CLUSTER_INFO.get(
                            int(cluster),
                            {
                                "name": f"Cluster {cluster}",
                                "emoji": "✦"
                            }
                        )

                        # ---------------------------------
                        # FAST AI SUMMARY
                        # ---------------------------------

                        summary = generate_personality_summary(
                            name=name.strip(),
                            traits=traits,
                            cluster_name=cluster_info["name"],
                            interests=interests
                        )

                        # ---------------------------------
                        # SAVE PROFILE
                        # ---------------------------------

                        profile_id = save_profile(
                            name=name.strip(),
                            role=role,
                            interests=interests,
                            traits=traits,
                            cluster=cluster,
                            core_answers=answers,
                            scenario_answers=[],
                            ai_summary=summary,
                            ai_insights={}
                        )

                        # ---------------------------------
                        # SESSION STATE
                        # ---------------------------------

                        st.session_state.current_profile_id = profile_id

                        # Reset form state for next time
                        st.session_state.assessment_answers = {}
                        st.session_state.assessment_section = 0

                        st.session_state.assessment_result = result

                        st.session_state.current_page = "My Personality"

                        # Reset questionnaire section
                        st.session_state.assessment_section = 0

                        st.success(
                            "Your ConnectAI personality profile has been created!"
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Something went wrong while creating your profile: {e}"
                        )
