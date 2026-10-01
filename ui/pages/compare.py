# ui/pages/compare.py

import html
import streamlit as st
import plotly.graph_objects as go

from ml.compatibility import calculate_compatibility, explain_match
from config.constants import TRAITS, TRAIT_META, CLUSTER_INFO
from ui.components import page_header


# =========================================================
# HTML HELPER
# =========================================================

def render_html(content):
    """
    Use the same rendering mechanism as the rest of the ConnectAI app.
    Do NOT use st.html here because the current project already has a
    markdown HTML-rendering setup in app.py/components.py.
    """
    if not isinstance(content, str):
        content = str(content)

    st.markdown(content, unsafe_allow_html=True)


# =========================================================
# SMALL HELPERS
# =========================================================

def safe_text(value):
    return html.escape(str(value or ""))


def profile_id(profile):
    return profile.get("id")


def profile_name(profile):
    return str(profile.get("name") or "Unknown")


def initial(name):
    value = profile_name({"name": name}).strip()
    return safe_text(value[0].upper() if value else "?")


def trait_value(profile, trait):
    try:
        value = profile.get("traits", {}).get(trait, 0)
        return max(0.0, min(5.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def cluster_info_for(profile):
    try:
        cluster = int(profile.get("cluster", 0))
    except (TypeError, ValueError):
        cluster = 0

    return CLUSTER_INFO.get(
        cluster,
        {
            "name": "Unknown",
            "emoji": "✦",
            "description": "Personality profile"
        }
    )


def similarity_label(score):
    score = float(score)

    if score >= 85:
        return "Strong Alignment"
    if score >= 70:
        return "Good Compatibility"
    if score >= 55:
        return "Moderate Compatibility"
    return "Interesting Differences"


def interest_visual_value(score):
    score = max(0.0, min(100.0, float(score)))
    return 1.0 + (score / 100.0) * 4.0


def shared_interests(person_a, person_b):
    a = {
        str(item).strip()
        for item in person_a.get("interests", [])
        if str(item).strip()
    }
    b = {
        str(item).strip()
        for item in person_b.get("interests", [])
        if str(item).strip()
    }

    return sorted(a.intersection(b))


def strongest_trait(profile):
    values = {
        trait: trait_value(profile, trait)
        for trait in TRAITS
    }
    return max(values, key=values.get) if values else "Openness"


def weakest_trait(profile):
    values = {
        trait: trait_value(profile, trait)
        for trait in TRAITS
    }
    return min(values, key=values.get) if values else "Neuroticism"


def profile_tags(profile):
    """
    Generate three simple product-friendly tags from the actual
    personality scores rather than hard-coding labels.
    """
    tags = []

    openness = trait_value(profile, "Openness")
    conscientiousness = trait_value(profile, "Conscientiousness")
    extraversion = trait_value(profile, "Extraversion")
    agreeableness = trait_value(profile, "Agreeableness")

    if openness >= 3.7:
        tags.append(("✦", "Open-minded"))
    elif openness >= 3.0:
        tags.append(("✦", "Curious"))
    else:
        tags.append(("◉", "Grounded"))

    if conscientiousness >= 3.7:
        tags.append(("◈", "Organized"))
    elif conscientiousness >= 3.0:
        tags.append(("✓", "Reliable"))
    else:
        tags.append(("○", "Flexible"))

    if extraversion >= 3.7:
        tags.append(("ϟ", "Social"))
    elif agreeableness >= 3.7:
        tags.append(("♥", "Supportive"))
    else:
        tags.append(("◉", "Thoughtful"))

    return tags


def chip(icon, text):
    return f"""
    <span style="
        display:inline-flex;
        align-items:center;
        gap:.38rem;
        padding:.42rem .68rem;
        border-radius:999px;
        background:rgba(255,255,255,.045);
        border:1px solid rgba(255,255,255,.08);
        color:#cbc4dc;
        font-size:.68rem;
        white-space:nowrap;
    ">
        <span>{safe_text(icon)}</span>
        <span>{safe_text(text)}</span>
    </span>
    """


def metric_bar(person_a_name, value_a, person_b_name, value_b):
    value_a = max(0.0, min(5.0, float(value_a)))
    value_b = max(0.0, min(5.0, float(value_b)))

    width_a = value_a / 5.0 * 100.0
    width_b = value_b / 5.0 * 100.0

    return f"""
    <div style="margin-top:.9rem;">
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            color:#85859a;
            font-size:.68rem;
        ">
            <span>{safe_text(person_a_name)}</span>
            <span style="color:#ddd6e9;font-weight:700;">{value_a:.1f} / 5</span>
        </div>

        <div style="
            height:6px;
            margin-top:.35rem;
            border-radius:999px;
            overflow:hidden;
            background:rgba(255,255,255,.055);
        ">
            <div style="
                width:{width_a:.1f}%;
                height:100%;
                border-radius:999px;
                background:linear-gradient(90deg,#c026d3,#ec4899);
                box-shadow:0 0 10px rgba(236,72,153,.22);
            "></div>
        </div>

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            color:#85859a;
            font-size:.68rem;
            margin-top:.65rem;
        ">
            <span>{safe_text(person_b_name)}</span>
            <span style="color:#ddd6e9;font-weight:700;">{value_b:.1f} / 5</span>
        </div>

        <div style="
            height:6px;
            margin-top:.35rem;
            border-radius:999px;
            overflow:hidden;
            background:rgba(255,255,255,.055);
        ">
            <div style="
                width:{width_b:.1f}%;
                height:100%;
                border-radius:999px;
                background:linear-gradient(90deg,#22a7f0,#6366f1);
                box-shadow:0 0 10px rgba(59,130,246,.18);
            "></div>
        </div>
    </div>
    """


def metric_card(icon, title, score, person_a, value_a, person_b, value_b):
    return f"""
    <div style="
        min-height:185px;
        padding:1.15rem;
        border-radius:19px;
        background:linear-gradient(
            145deg,
            rgba(255,255,255,.045),
            rgba(255,255,255,.018)
        );
        border:1px solid rgba(255,255,255,.075);
        box-shadow:inset 0 1px 0 rgba(255,255,255,.025);
        box-sizing:border-box;
    ">
        <div style="
            display:flex;
            align-items:center;
            gap:.7rem;
        ">
            <div style="
                width:38px;
                height:38px;
                display:flex;
                align-items:center;
                justify-content:center;
                border-radius:12px;
                background:linear-gradient(
                    135deg,
                    rgba(99,102,241,.22),
                    rgba(236,72,153,.18)
                );
                font-size:1rem;
            ">
                {safe_text(icon)}
            </div>

            <div style="
                color:#a8a0b9;
                font-size:.66rem;
                font-weight:800;
                letter-spacing:.11em;
            ">
                {safe_text(title)}
            </div>
        </div>

        <div style="
            font-size:2rem;
            font-weight:850;
            margin-top:.65rem;
            color:#f3edf9;
        ">
            {float(score):.1f}%
        </div>

        {metric_bar(person_a, value_a, person_b, value_b)}
    </div>
    """


def insight_card(icon, title, text, accent):
    return f"""
    <div style="
        height:100%;
        min-height:145px;
        padding:1rem 1.1rem;
        border-radius:16px;
        background:rgba(255,255,255,.025);
        border:1px solid rgba(255,255,255,.06);
        box-sizing:border-box;
    ">
        <div style="
            display:flex;
            align-items:center;
            gap:.65rem;
        ">
            <div style="
                width:36px;
                height:36px;
                display:flex;
                align-items:center;
                justify-content:center;
                border-radius:11px;
                background:{accent};
                font-size:1.1rem;
            ">
                {safe_text(icon)}
            </div>

            <div style="
                color:#eee9f5;
                font-size:.82rem;
                font-weight:800;
            ">
                {safe_text(title)}
            </div>
        </div>

        <div style="
            color:#85859a;
            font-size:.72rem;
            line-height:1.65;
            margin-top:.8rem;
        ">
            {safe_text(text)}
        </div>
    </div>
    """


# =========================================================
# BIG FIVE CHART
# =========================================================

def create_trait_chart(person_a, person_b):
    categories = list(TRAITS)

    values_a = [trait_value(person_a, trait) for trait in categories]
    values_b = [trait_value(person_b, trait) for trait in categories]

    labels = [
        TRAIT_META.get(trait, {}).get("short", trait[:3].upper())
        for trait in categories
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name=profile_name(person_a),
            x=labels,
            y=values_a,
            marker=dict(
                color="#ec4899",
                line=dict(color="#c026d3", width=1)
            ),
            text=[f"{v:.1f}" for v in values_a],
            textposition="outside",
            textfont=dict(color="#f1eaff", size=12),
            hovertemplate=(
                f"{safe_text(profile_name(person_a))}"
                "<br>%{x}: %{y:.2f}/5"
                "<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Bar(
            name=profile_name(person_b),
            x=labels,
            y=values_b,
            marker=dict(
                color="#4f9cf9",
                line=dict(color="#6366f1", width=1)
            ),
            text=[f"{v:.1f}" for v in values_b],
            textposition="outside",
            textfont=dict(color="#f1eaff", size=12),
            hovertemplate=(
                f"{safe_text(profile_name(person_b))}"
                "<br>%{x}: %{y:.2f}/5"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        barmode="group",
        height=390,
        margin=dict(l=35, r=15, t=35, b=55),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, sans-serif",
            color="#aaaabc"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color="#aaaabc")
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=10, color="#aaaabc"),
            linecolor="rgba(255,255,255,.08)"
        ),
        yaxis=dict(
            range=[0, 5.6],
            tickvals=[1, 2, 3, 4, 5],
            gridcolor="rgba(255,255,255,.07)",
            zeroline=False,
            tickfont=dict(size=10, color="#77778d")
        ),
        bargap=.25,
        bargroupgap=.08
    )

    return fig


# =========================================================
# MAIN PAGE
# =========================================================

def render_compare(profiles):

    page_header(
        "COMPARE PROFILES",
        "Side by side, deeper insights.",
        "Compare two profiles to see how you complement each other across personality, interests and social energy."
    )

    # -----------------------------------------------------
    # NOT ENOUGH PROFILES
    # -----------------------------------------------------

    if len(profiles) < 2:
        render_html("""
        <div class="hero">
            <div class="hero-content">
                <div class="ai-badge">✦ PROFILE COMPARISON</div>
                <div class="hero-title">Two profiles make a connection.</div>
                <div class="hero-text">
                    Create at least two profiles to unlock side-by-side
                    personality and compatibility analysis.
                </div>
            </div>
        </div>
        """)
        return

    # -----------------------------------------------------
    # PROFILE OPTIONS
    #
    # IMPORTANT:
    # The selectboxes use profile IDs, never names.
    # Therefore "Samruddhi" can never cause a KeyError.
    # -----------------------------------------------------

    profile_by_id = {
        profile_id(profile): profile
        for profile in profiles
        if profile_id(profile) is not None
    }

    ids = list(profile_by_id.keys())

    def display_name(pid):
        return profile_name(profile_by_id[pid])

    current_id = st.session_state.get("current_profile_id")

    if current_id not in profile_by_id:
        current_id = ids[0]

    other_ids = [pid for pid in ids if pid != current_id]

    if not other_ids:
        return

    saved_compare_id = st.session_state.get("compare_profile_id")

    if saved_compare_id in profile_by_id and saved_compare_id != current_id:
        default_b = saved_compare_id
    else:
        default_b = other_ids[0]

    # A nonce gives the swap action a fresh widget identity.
    # This avoids modifying a widget's session state after creation.
    nonce = int(st.session_state.get("compare_widget_nonce", 0))

    default_a = current_id

    if st.session_state.get("compare_swap_pending"):
        pending_a = st.session_state.get("compare_pending_a")
        pending_b = st.session_state.get("compare_pending_b")

        if pending_a in profile_by_id and pending_b in profile_by_id:
            default_a = pending_a
            default_b = pending_b

        st.session_state.compare_swap_pending = False

    # -----------------------------------------------------
    # SELECTORS
    # -----------------------------------------------------

    selector_left, selector_swap, selector_right = st.columns([5, 1, 5])

    with selector_left:
        render_html("""
        <div style="
            color:#aaaabc;
            font-size:.72rem;
            font-weight:800;
            letter-spacing:.08em;
            margin-bottom:.45rem;
        ">
            PERSON A
        </div>
        """)

        selected_a = st.selectbox(
            "Person A",
            options=ids,
            index=ids.index(default_a),
            format_func=display_name,
            label_visibility="collapsed",
            key=f"compare_a_v3_{nonce}"
        )

    with selector_swap:
        st.markdown("<div style='height:1.35rem'></div>", unsafe_allow_html=True)

        if st.button(
            "⇄",
            key=f"compare_swap_v3_{nonce}",
            help="Swap the two profiles"
        ):
            st.session_state.compare_pending_a = selected_b if "selected_b" in locals() else default_b
            st.session_state.compare_pending_b = selected_a
            st.session_state.compare_swap_pending = True
            st.session_state.compare_widget_nonce = nonce + 1
            st.rerun()

    with selector_right:
        render_html("""
        <div style="
            color:#aaaabc;
            font-size:.72rem;
            font-weight:800;
            letter-spacing:.08em;
            margin-bottom:.45rem;
        ">
            PERSON B
        </div>
        """)

        selected_b = st.selectbox(
            "Person B",
            options=ids,
            index=ids.index(default_b),
            format_func=display_name,
            label_visibility="collapsed",
            key=f"compare_b_v3_{nonce}"
        )

    person_a = profile_by_id[selected_a]
    person_b = profile_by_id[selected_b]

    # Save B only as a non-widget state value.
    st.session_state.compare_profile_id = person_b.get("id")

    # -----------------------------------------------------
    # SAME PROFILE
    # -----------------------------------------------------

    if selected_a == selected_b:
        render_html("""
        <div style="
            margin-top:1rem;
            padding:1rem 1.1rem;
            border-radius:16px;
            background:rgba(245,158,11,.08);
            border:1px solid rgba(245,158,11,.22);
            color:#e8d9bd;
        ">
            <strong>Choose two different people.</strong><br>
            <span style="font-size:.78rem;color:#aaa09a;">
                Select another profile to compare personality and compatibility.
            </span>
        </div>
        """)
        return

    # -----------------------------------------------------
    # COMPATIBILITY
    # -----------------------------------------------------

    result = calculate_compatibility(
        person_a.get("traits", {}),
        person_b.get("traits", {}),
        person_a.get("interests", []),
        person_b.get("interests", [])
    )

    overall = float(result.get("overall", 0))
    personality_score = float(result.get("personality", 0))
    interest_score = float(result.get("interests", 0))
    social_score = float(result.get("social_energy", 0))

    cluster_a = cluster_info_for(person_a)
    cluster_b = cluster_info_for(person_b)

    tags_a = profile_tags(person_a)
    tags_b = profile_tags(person_b)

    shared = shared_interests(person_a, person_b)

    # -----------------------------------------------------
    # PROFILE SUMMARY
    # -----------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    render_html(f"""
    <div style="
        position:relative;
        overflow:hidden;
        border-radius:24px;
        padding:1.5rem;
        border:1px solid rgba(167,139,250,.4);
        background:
            radial-gradient(
                circle at 15% 50%,
                rgba(139,92,246,.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 45%,
                rgba(236,72,153,.16),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                rgba(91,33,182,.17),
                rgba(236,72,153,.08)
            );
        box-shadow:
            0 0 35px rgba(139,92,246,.08),
            inset 0 1px 0 rgba(255,255,255,.04);
    ">

        <div style="
            display:grid;
            grid-template-columns:1fr 230px 1fr;
            gap:1rem;
            align-items:center;
        ">

            <!-- PERSON A -->
            <div style="text-align:left;">
                <div style="
                    display:flex;
                    align-items:center;
                    gap:1rem;
                ">
                    <div style="
                        width:82px;
                        height:82px;
                        flex-shrink:0;
                        border-radius:50%;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-size:2rem;
                        font-weight:850;
                        color:white;
                        background:linear-gradient(135deg,#8b5cf6,#ec4899);
                        border:4px solid rgba(255,255,255,.08);
                        box-shadow:
                            0 0 0 7px rgba(139,92,246,.08),
                            0 0 25px rgba(236,72,153,.22);
                    ">
                        {initial(profile_name(person_a))}
                    </div>

                    <div>
                        <div style="
                            color:#f1edf8;
                            font-size:1.25rem;
                            font-weight:850;
                        ">
                            {safe_text(profile_name(person_a))}
                        </div>

                        <div style="
                            color:#aaaabc;
                            font-size:.76rem;
                            margin-top:.3rem;
                        ">
                            {safe_text(cluster_a.get("emoji","✦"))}
                            {safe_text(cluster_a.get("name","Unknown"))}
                        </div>
                    </div>
                </div>

                <div style="
                    display:flex;
                    flex-wrap:wrap;
                    gap:.4rem;
                    margin-top:.9rem;
                ">
                    {''.join(chip(icon, text) for icon, text in tags_a)}
                </div>
            </div>

            <!-- CENTER SCORE -->
            <div style="
                text-align:center;
                padding:.5rem;
            ">
                <div style="
                    color:#c9a5ff;
                    font-size:.68rem;
                    font-weight:800;
                    letter-spacing:.12em;
                ">
                    OVERALL COMPATIBILITY
                </div>

                <div style="
                    font-size:3rem;
                    line-height:1.1;
                    margin-top:.25rem;
                    font-weight:900;
                    background:linear-gradient(90deg,#c084fc,#f472b6);
                    -webkit-background-clip:text;
                    -webkit-text-fill-color:transparent;
                ">
                    {overall:.1f}%
                </div>

                <div style="
                    display:inline-block;
                    padding:.5rem .8rem;
                    margin-top:.35rem;
                    border-radius:13px;
                    background:linear-gradient(
                        135deg,
                        rgba(99,102,241,.18),
                        rgba(236,72,153,.12)
                    );
                    border:1px solid rgba(167,139,250,.2);
                    color:#ddd4eb;
                    font-size:.67rem;
                ">
                    {safe_text(similarity_label(overall))}
                </div>

                <div style="
                    color:#a995bb;
                    font-size:1.2rem;
                    margin-top:.35rem;
                    letter-spacing:.2rem;
                ">
                    〰〰
                </div>
            </div>

            <!-- PERSON B -->
            <div style="text-align:right;">
                <div style="
                    display:flex;
                    align-items:center;
                    justify-content:flex-end;
                    gap:1rem;
                ">
                    <div>
                        <div style="
                            color:#f1edf8;
                            font-size:1.25rem;
                            font-weight:850;
                        ">
                            {safe_text(profile_name(person_b))}
                        </div>

                        <div style="
                            color:#aaaabc;
                            font-size:.76rem;
                            margin-top:.3rem;
                        ">
                            {safe_text(cluster_b.get("emoji","✦"))}
                            {safe_text(cluster_b.get("name","Unknown"))}
                        </div>
                    </div>

                    <div style="
                        width:82px;
                        height:82px;
                        flex-shrink:0;
                        border-radius:50%;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-size:2rem;
                        font-weight:850;
                        color:white;
                        background:linear-gradient(135deg,#ec4899,#8b5cf6);
                        border:4px solid rgba(255,255,255,.08);
                        box-shadow:
                            0 0 0 7px rgba(236,72,153,.07),
                            0 0 25px rgba(139,92,246,.22);
                    ">
                        {initial(profile_name(person_b))}
                    </div>
                </div>

                <div style="
                    display:flex;
                    justify-content:flex-end;
                    flex-wrap:wrap;
                    gap:.4rem;
                    margin-top:.9rem;
                ">
                    {''.join(chip(icon, text) for icon, text in tags_b)}
                </div>
            </div>

        </div>

        <div style="
            display:flex;
            justify-content:center;
            flex-wrap:wrap;
            gap:.7rem;
            margin-top:1.3rem;
        ">
            <span style="
                padding:.5rem .85rem;
                border-radius:999px;
                background:rgba(255,255,255,.045);
                border:1px solid rgba(255,255,255,.08);
                color:#cfc6dd;
                font-size:.68rem;
            ">
                ♟ Aligned Personalities
            </span>

            <span style="
                padding:.5rem .85rem;
                border-radius:999px;
                background:rgba(255,255,255,.045);
                border:1px solid rgba(255,255,255,.08);
                color:#cfc6dd;
                font-size:.68rem;
            ">
                ♥ {len(shared)} Shared Interest{"s" if len(shared) != 1 else ""}
            </span>

            <span style="
                padding:.5rem .85rem;
                border-radius:999px;
                background:rgba(255,255,255,.045);
                border:1px solid rgba(255,255,255,.08);
                color:#cfc6dd;
                font-size:.68rem;
            ">
                ϟ Balanced Energy
            </span>
        </div>

    </div>
    """)

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    metric_columns = st.columns(3)

    metric_data = [
        (
            "◉",
            "PERSONALITY MATCH",
            personality_score,
            trait_value(person_a, "Openness"),
            trait_value(person_b, "Openness")
        ),
        (
            "♥",
            "INTEREST MATCH",
            interest_score,
            interest_visual_value(interest_score),
            interest_visual_value(interest_score)
        ),
        (
            "ϟ",
            "SOCIAL ENERGY MATCH",
            social_score,
            trait_value(person_a, "Extraversion"),
            trait_value(person_b, "Extraversion")
        )
    ]

    for column, item in zip(metric_columns, metric_data):
        icon, title, score, value_a, value_b = item

        with column:
            render_html(
                metric_card(
                    icon,
                    title,
                    score,
                    profile_name(person_a),
                    value_a,
                    profile_name(person_b),
                    value_b
                )
            )

    # -----------------------------------------------------
    # BIG FIVE
    # -----------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    render_html("""
    <div style="
        padding:1.2rem 1.25rem .25rem;
        border-radius:20px 20px 0 0;
        border:1px solid rgba(255,255,255,.065);
        border-bottom:none;
        background:rgba(255,255,255,.018);
    ">
        <div style="
            display:flex;
            align-items:center;
            gap:.7rem;
        ">
            <div style="font-size:1.15rem;">▥</div>

            <div>
                <div style="
                    color:#c9a5ff;
                    font-size:.72rem;
                    font-weight:850;
                    letter-spacing:.12em;
                ">
                    BIG FIVE TRAITS COMPARISON
                </div>

                <div style="
                    color:#77778d;
                    font-size:.68rem;
                    margin-top:.3rem;
                ">
                    How you both score on the core personality
                    dimensions (1 = Low, 5 = High)
                </div>
            </div>
        </div>
    </div>
    """)

    chart = create_trait_chart(person_a, person_b)

    st.plotly_chart(
        chart,
        width="stretch",
        config={
            "displayModeBar": False,
            "responsive": True
        }
    )

    # -----------------------------------------------------
    # KEY INSIGHTS
    # -----------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    social_difference = abs(
        trait_value(person_a, "Extraversion")
        - trait_value(person_b, "Extraversion")
    )

    conscientiousness_difference = abs(
        trait_value(person_a, "Conscientiousness")
        - trait_value(person_b, "Conscientiousness")
    )

    agreeableness_average = (
        trait_value(person_a, "Agreeableness")
        + trait_value(person_b, "Agreeableness")
    ) / 2.0

    openness_difference = abs(
        trait_value(person_a, "Openness")
        - trait_value(person_b, "Openness")
    )

    if social_difference <= 0.5:
        insight_1 = (
            "You have very similar social energy levels, suggesting "
            "a natural comfort in spending time together."
        )
    else:
        insight_1 = (
            "Your social energy levels differ, which can create a "
            "balance between outgoing and quieter interaction styles."
        )

    if conscientiousness_difference >= 0.7:
        insight_2 = (
            "Your differences in conscientiousness can be a strength — "
            "one person may bring structure while the other brings flexibility."
        )
    else:
        insight_2 = (
            "Your organization and work styles are fairly aligned, "
            "making planning and collaboration more natural."
        )

    if shared:
        shared_preview = ", ".join(shared[:3])
        if len(shared) > 3:
            shared_preview += f" + {len(shared) - 3} more"

        insight_3 = (
            f"You share {len(shared)} interest"
            f"{'s' if len(shared) != 1 else ''}"
            f" ({shared_preview}), giving you natural common ground."
        )
    elif agreeableness_average >= 3.8:
        insight_3 = (
            "You both show relatively high agreeableness, creating "
            "a strong foundation for support, trust and collaboration."
        )
    elif openness_difference >= 1.0:
        insight_3 = (
            "Your openness scores are noticeably different, which can "
            "create opportunities to introduce each other to new perspectives."
        )
    else:
        insight_3 = (
            "Your differences leave room for learning from each other's "
            "perspectives, interests and ways of approaching situations."
        )

    render_html("""
    <div style="
        padding:1.3rem;
        border-radius:21px;
        background:
            radial-gradient(
                circle at 10% 50%,
                rgba(139,92,246,.17),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 50%,
                rgba(236,72,153,.13),
                transparent 32%
            ),
            linear-gradient(
                135deg,
                rgba(91,33,182,.12),
                rgba(236,72,153,.07)
            );
        border:1px solid rgba(167,139,250,.25);
    ">
        <div style="
            display:flex;
            align-items:center;
            gap:.7rem;
        ">
            <div style="font-size:1.35rem;">💡</div>

            <div>
                <div style="
                    color:#c9a5ff;
                    font-size:.72rem;
                    font-weight:850;
                    letter-spacing:.12em;
                ">
                    KEY INSIGHTS
                </div>

                <div style="
                    color:#77778d;
                    font-size:.68rem;
                    margin-top:.25rem;
                ">
                    What makes this connection work
                </div>
            </div>
        </div>
    </div>
    """)

    insight_columns = st.columns(3)

    insight_data = [
        (
            "♥",
            "Social Dynamic",
            insight_1,
            "rgba(236,72,153,.14)"
        ),
        (
            "♟",
            "Complementary Strengths",
            insight_2,
            "rgba(99,102,241,.16)"
        ),
        (
            "★",
            "Shared Potential",
            insight_3,
            "rgba(250,204,21,.12)"
        )
    ]

    for column, data in zip(insight_columns, insight_data):
        with column:
            render_html(insight_card(*data))

    # -----------------------------------------------------
    # TECHNICAL NOTE
    # -----------------------------------------------------

    render_html(f"""
    <div style="
        text-align:center;
        color:#56566a;
        font-size:.64rem;
        margin:1.3rem 0 .5rem;
    ">
        ConnectAI compatibility: {overall:.1f}% ·
        Personality {personality_score:.1f}% ·
        Interests {interest_score:.1f}% ·
        Social Energy {social_score:.1f}%
    </div>
    """)
