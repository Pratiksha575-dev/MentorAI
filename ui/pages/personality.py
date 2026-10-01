# ui/pages/personality.py

import html
import re

import streamlit as st
import plotly.graph_objects as go

from config.constants import TRAITS, CLUSTER_INFO
from ui.components import page_header


# =========================================================
# PERSONALITY PAGE — CONNECTAI
# =========================================================
#
# Designed to closely match the supplied ConnectAI reference:
#
#   • Futuristic dark glassmorphism
#   • Compact profile hero
#   • Five dimensions in one horizontal row
#   • Fingerprint + At a Glance side by side
#   • Interests as compact horizontal pills
#   • AI reading as a compact horizontal feature card
#   • Trait breakdown as compact horizontal cards lower down
#
# Existing ML/database values are used directly.
# No personality values are hard-coded.
# =========================================================


# =========================================================
# PAGE-SCOPED CSS
# =========================================================

def inject_personality_css():
    st.markdown(
        """
        <style>


        /* =================================================
           FINAL POLISH OVERRIDES
           ================================================= */

        .ca-card-heading {
            display:flex;
            align-items:center;
            gap:.7rem;
            padding:.1rem .05rem .35rem;
        }

        .ca-card-heading .ca-panel-icon {
            flex:0 0 auto;
        }

        /* Streamlit bordered containers used for fingerprint
           and glance should look like the rest of the glass UI. */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border:1px solid rgba(167,139,250,.18) !important;
            border-radius:20px !important;
            background:
                linear-gradient(
                    145deg,
                    rgba(255,255,255,.035),
                    rgba(255,255,255,.012)
                ) !important;
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,.025),
                0 12px 35px rgba(0,0,0,.10) !important;
            overflow:hidden !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"] > div {
            border:0 !important;
        }

        .ca-ai-panel {
            min-height:158px !important;
        }

        .ca-ai-body {
            min-height:92px !important;
        }

        .ca-ai-copy {
            min-width:0;
            flex:1;
        }

        .ca-ai-action-slot {
            width:150px;
            flex:0 0 150px;
        }

        /* Style the real Streamlit full-analysis button. */
        div[data-testid="stButton"] button[kind="secondary"] {
            border-radius:999px !important;
            border:1px solid rgba(236,72,153,.42) !important;
            background:
                linear-gradient(
                    135deg,
                    rgba(139,92,246,.20),
                    rgba(236,72,153,.18)
                ) !important;
            color:#d8baff !important;
            font-size:.68rem !important;
            font-weight:800 !important;
            min-height:38px !important;
            box-shadow:0 0 22px rgba(139,92,246,.08) !important;
        }

        div[data-testid="stButton"] button[kind="secondary"]:hover {
            border-color:rgba(236,72,153,.7) !important;
            transform:translateY(-1px);
        }

        .ca-ai-full {
            margin-top:.65rem;
            padding:1.15rem 1.25rem;
            border-radius:18px;
            background:
                linear-gradient(
                    145deg,
                    rgba(139,92,246,.075),
                    rgba(236,72,153,.045)
                );
            border:1px solid rgba(167,139,250,.17);
        }

        .ca-ai-full-title {
            color:#d4b5ff;
            font-size:.78rem;
            font-weight:800;
            margin-bottom:.55rem;
        }

        .ca-ai-full-text {
            color:#b8b0c2;
            font-size:.80rem;
            line-height:1.75;
        }

        .ca-ai-full-text strong {
            color:#eee7f6;
            font-weight:800;
        }

        .ca-ai-empty {
            margin-top:.65rem;
            padding:.85rem 1rem;
            border-radius:14px;
            color:#777285;
            background:rgba(255,255,255,.018);
            border:1px solid rgba(255,255,255,.055);
            font-size:.72rem;
        }

        /* Replace the old uneven 2 + 2 + 1 trait layout. */
        .ca-insight-grid {
            display:grid;
            grid-template-columns:repeat(3, minmax(0, 1fr));
            gap:.75rem;
            margin-top:.75rem;
        }

        .ca-insight-card {
            min-height:105px;
            display:flex;
            align-items:center;
            gap:.75rem;
            padding:.85rem .9rem;
            border-radius:16px;
            background:
                linear-gradient(
                    145deg,
                    rgba(255,255,255,.035),
                    rgba(255,255,255,.012)
                );
            border:1px solid rgba(255,255,255,.065);
            box-shadow:inset 0 1px 0 rgba(255,255,255,.02);
        }

        .ca-insight-icon {
            width:38px;
            height:38px;
            flex:0 0 38px;
            display:flex;
            align-items:center;
            justify-content:center;
            border-radius:12px;
            background:
                linear-gradient(
                    135deg,
                    rgba(139,92,246,.15),
                    rgba(236,72,153,.12)
                );
            border:1px solid rgba(167,139,250,.16);
            font-size:1rem;
        }

        .ca-insight-copy {
            min-width:0;
            flex:1;
        }

        .ca-insight-label {
            color:#777285;
            font-size:.62rem;
            font-weight:700;
        }

        .ca-insight-trait {
            color:#eee9f5;
            font-size:.78rem;
            font-weight:800;
            margin-top:.15rem;
        }

        .ca-insight-description {
            color:#777285;
            font-size:.61rem;
            line-height:1.45;
            margin-top:.2rem;
        }

        .ca-insight-score {
            color:#d5b6ff;
            font-size:.72rem;
            font-weight:850;
            white-space:nowrap;
        }

        @media (max-width: 900px) {
            .ca-insight-grid {
                grid-template-columns:1fr;
            }

            .ca-ai-action-slot {
                width:100px;
                flex-basis:100px;
            }
        }

        /* =================================================
           PAGE WIDTH / SPACING
           ================================================= */

        .connectai-personality {
            width:100%;
            box-sizing:border-box;
        }

        .connectai-personality * {
            box-sizing:border-box;
        }


        /* =================================================
           HERO
           ================================================= */

        .ca-hero {
            position:relative;
            overflow:hidden;
            min-height:185px;
            padding:1.65rem 1.75rem;
            border-radius:25px;
            background:
                radial-gradient(
                    circle at 8% 50%,
                    rgba(91,33,182,.28),
                    transparent 34%
                ),
                radial-gradient(
                    circle at 92% 45%,
                    rgba(236,72,153,.19),
                    transparent 34%
                ),
                linear-gradient(
                    135deg,
                    rgba(55,28,135,.44),
                    rgba(65,20,65,.34)
                );
            border:1px solid rgba(139,92,246,.30);
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,.055),
                0 20px 55px rgba(0,0,0,.18);
        }

        .ca-hero-glow-one {
            position:absolute;
            width:250px;
            height:250px;
            right:-80px;
            top:-100px;
            border-radius:50%;
            background:rgba(236,72,153,.12);
            filter:blur(50px);
            pointer-events:none;
        }

        .ca-hero-glow-two {
            position:absolute;
            width:180px;
            height:180px;
            left:100px;
            bottom:-120px;
            border-radius:50%;
            background:rgba(139,92,246,.13);
            filter:blur(45px);
            pointer-events:none;
        }

        .ca-hero-inner {
            position:relative;
            z-index:2;
        }

        .ca-hero-profile {
            display:flex;
            align-items:center;
            gap:1.05rem;
        }

        .ca-avatar {
            width:78px;
            height:78px;
            min-width:78px;
            border-radius:50%;
            display:flex;
            align-items:center;
            justify-content:center;
            color:#fff;
            font-size:2.05rem;
            font-weight:900;
            background:
                radial-gradient(
                    circle at 32% 25%,
                    rgba(255,255,255,.32),
                    transparent 28%
                ),
                linear-gradient(
                    135deg,
                    #693cff,
                    #ef3d91
                );
            border:4px solid rgba(255,255,255,.08);
            box-shadow:
                0 0 0 7px rgba(139,92,246,.08),
                0 0 30px rgba(236,72,153,.23);
        }

        .ca-profile-name {
            color:#f8f6fb;
            font-size:2rem;
            font-weight:850;
            letter-spacing:-.035em;
            line-height:1.05;
            margin-top:.62rem;
        }

        .ca-cluster-line {
            color:#c7b9d0;
            font-size:.78rem;
            margin-top:.35rem;
        }

        .ca-cluster-description {
            color:#aaa1b3;
            font-size:.76rem;
            line-height:1.55;
            margin-top:.65rem;
            max-width:650px;
        }

        .ca-quote {
            width:275px;
            max-width:32%;
            padding-left:1.5rem;
            border-left:1px solid rgba(255,255,255,.09);
            color:#c4b7cc;
            font-size:.75rem;
            line-height:1.65;
            font-style:italic;
        }

        .ca-quote-mark {
            color:#bd7bff;
            font-size:2.6rem;
            line-height:.55;
            font-style:normal;
            margin-bottom:.4rem;
        }


        /* =================================================
           FIVE DIMENSIONS
           ================================================= */

        .ca-section-row {
            display:flex;
            align-items:flex-end;
            justify-content:space-between;
            gap:1rem;
            margin-top:1.25rem;
            margin-bottom:.65rem;
        }

        .ca-section-title {
            color:#c28cff;
            font-size:.70rem;
            font-weight:850;
            letter-spacing:.12em;
            text-transform:uppercase;
        }

        .ca-section-helper {
            color:#777489;
            font-size:.65rem;
        }

        .ca-five-grid {
            display:grid;
            grid-template-columns:
                repeat(5, minmax(0, 1fr));
            gap:.72rem;
        }

        .ca-dimension-card {
            min-width:0;
            height:142px;
            padding:1rem;
            border-radius:17px;
            background:
                linear-gradient(
                    145deg,
                    rgba(255,255,255,.037),
                    rgba(255,255,255,.012)
                );
            border:1px solid rgba(255,255,255,.075);
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,.025);
        }

        .ca-dimension-icon {
            height:27px;
            font-size:1.35rem;
            line-height:1;
        }

        .ca-dimension-name {
            color:#aaa6b9;
            font-size:.68rem;
            font-weight:650;
            margin-top:.52rem;
            white-space:nowrap;
            overflow:hidden;
            text-overflow:ellipsis;
        }

        .ca-dimension-value {
            color:#f4f1f8;
            font-size:1.18rem;
            font-weight:850;
            margin-top:.38rem;
        }

        .ca-dimension-value span {
            color:#777286;
            font-size:.62rem;
            font-weight:650;
        }

        .ca-progress {
            width:100%;
            height:5px;
            margin-top:.65rem;
            overflow:hidden;
            border-radius:999px;
            background:rgba(255,255,255,.075);
        }

        .ca-progress-fill {
            height:100%;
            border-radius:999px;
            background:
                linear-gradient(
                    90deg,
                    #8b5cf6,
                    #ec4899
                );
            box-shadow:
                0 0 10px rgba(236,72,153,.25);
        }


        /* =================================================
           TWO-COLUMN INSIGHT AREA
           ================================================= */

        .ca-two-col {
            display:grid;
            grid-template-columns:
                minmax(0, 1.08fr)
                minmax(0, .92fr);
            gap:.85rem;
            margin-top:.85rem;
        }

        .ca-panel {
            min-width:0;
            border-radius:20px;
            background:
                linear-gradient(
                    145deg,
                    rgba(255,255,255,.034),
                    rgba(255,255,255,.012)
                );
            border:1px solid rgba(255,255,255,.065);
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,.025);
        }

        .ca-panel-header {
            display:flex;
            align-items:center;
            gap:.55rem;
            padding:1rem 1.05rem .3rem;
        }

        .ca-panel-icon {
            color:#c084fc;
            font-size:1rem;
        }

        .ca-panel-label {
            color:#c084fc;
            font-size:.69rem;
            font-weight:850;
            letter-spacing:.105em;
        }

        .ca-panel-subtitle {
            color:#686779;
            font-size:.62rem;
            margin-top:.18rem;
        }

        .ca-radar-wrap {
            height:345px;
            padding:0 .25rem .15rem;
        }


        /* =================================================
           AT A GLANCE
           ================================================= */

        .ca-glance-content {
            padding:.35rem 1rem 1rem;
        }

        .ca-glance-card {
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:.8rem;
            padding:.68rem .75rem;
            margin-top:.52rem;
            border-radius:13px;
            background:rgba(255,255,255,.025);
            border:1px solid rgba(255,255,255,.06);
        }

        .ca-glance-left {
            display:flex;
            align-items:center;
            gap:.65rem;
            min-width:0;
        }

        .ca-glance-icon {
            width:34px;
            height:34px;
            min-width:34px;
            display:flex;
            align-items:center;
            justify-content:center;
            border-radius:10px;
            background:rgba(139,92,246,.10);
            border:1px solid rgba(139,92,246,.15);
            font-size:.95rem;
        }

        .ca-glance-label {
            color:#777489;
            font-size:.59rem;
        }

        .ca-glance-trait {
            color:#e4deea;
            font-size:.73rem;
            font-weight:750;
            margin-top:.12rem;
        }

        .ca-glance-score {
            color:#eee9f4;
            font-size:.78rem;
            font-weight:850;
            white-space:nowrap;
        }

        .ca-glance-score span {
            color:#666374;
            font-size:.57rem;
        }

        .ca-glance-note {
            margin-top:.65rem;
            padding:.68rem .75rem;
            border-radius:12px;
            background:
                linear-gradient(
                    135deg,
                    rgba(139,92,246,.075),
                    rgba(236,72,153,.045)
                );
            border:1px solid rgba(139,92,246,.14);
            color:#9d95a9;
            font-size:.65rem;
            line-height:1.5;
        }


        /* =================================================
           INTERESTS
           ================================================= */

        .ca-interest-panel {
            margin-top:.85rem;
            padding:.78rem .82rem;
            border-radius:18px;
            background:
                linear-gradient(
                    135deg,
                    rgba(255,255,255,.026),
                    rgba(139,92,246,.035)
                );
            border:1px solid rgba(255,255,255,.065);
        }

        .ca-interest-header {
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:1rem;
            margin-bottom:.58rem;
        }

        .ca-interest-heading {
            display:flex;
            align-items:center;
            gap:.52rem;
            color:#c084fc;
            font-size:.68rem;
            font-weight:850;
            letter-spacing:.10em;
        }

        .ca-interest-helper {
            color:#777386;
            font-size:.61rem;
        }

        .ca-interest-track {
            display:flex;
            align-items:center;
            gap:.42rem;
            overflow:hidden;
            white-space:nowrap;
            min-width:0;
        }

        .ca-interest-chip {
            display:inline-flex;
            align-items:center;
            justify-content:center;
            gap:.4rem;
            height:37px;
            padding:0 .78rem;
            border-radius:999px;
            flex:0 0 auto;
            color:#c7a8ed;
            font-size:.68rem;
            font-weight:650;
            background:
                linear-gradient(
                    135deg,
                    rgba(139,92,246,.08),
                    rgba(236,72,153,.045)
                );
            border:1px solid rgba(139,92,246,.28);
        }

        .ca-interest-arrow {
            width:35px;
            height:35px;
            min-width:35px;
            display:flex;
            align-items:center;
            justify-content:center;
            border-radius:50%;
            color:#d1b4f4;
            background:rgba(91,33,182,.17);
            border:1px solid rgba(139,92,246,.32);
            font-size:1rem;
            margin-left:auto;
        }


        /* =================================================
           AI READING
           ================================================= */

        .ca-ai-panel {
            position:relative;
            overflow:hidden;
            margin-top:.85rem;
            padding:.85rem 1rem;
            border-radius:19px;
            background:
                radial-gradient(
                    circle at 5% 50%,
                    rgba(139,92,246,.13),
                    transparent 35%
                ),
                radial-gradient(
                    circle at 95% 50%,
                    rgba(236,72,153,.10),
                    transparent 35%
                ),
                linear-gradient(
                    135deg,
                    rgba(91,33,182,.12),
                    rgba(236,72,153,.055)
                );
            border:1px solid rgba(167,139,250,.22);
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,.035);
        }

        .ca-ai-top {
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:1rem;
            margin-bottom:.72rem;
        }

        .ca-ai-label {
            display:flex;
            align-items:center;
            gap:.52rem;
            color:#c084fc;
            font-size:.68rem;
            font-weight:850;
            letter-spacing:.10em;
        }

        .ca-ai-helper {
            color:#777386;
            font-size:.61rem;
        }

        .ca-ai-body {
            display:grid;
            grid-template-columns:66px minmax(0, 1fr) auto;
            align-items:center;
            gap:1rem;
        }

        .ca-robot {
            width:66px;
            height:66px;
            min-width:66px;
            display:flex;
            align-items:center;
            justify-content:center;
            border-radius:18px;
            background:
                radial-gradient(
                    circle at 50% 35%,
                    rgba(255,255,255,.20),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    rgba(139,92,246,.42),
                    rgba(236,72,153,.30)
                );
            border:1px solid rgba(255,255,255,.10);
            box-shadow:
                0 0 24px rgba(139,92,246,.17);
            font-size:2rem;
        }

        .ca-ai-title {
            color:#f2edf7;
            font-size:1.18rem;
            font-weight:850;
            line-height:1.15;
        }

        .ca-ai-title span {
            color:#d982ed;
        }

        .ca-ai-preview {
            color:#aaa4b4;
            font-size:.70rem;
            line-height:1.6;
            margin-top:.3rem;
            max-width:760px;
        }

        .ca-ai-button {
            padding:.65rem .88rem;
            border-radius:999px;
            color:#e4caff;
            font-size:.66rem;
            font-weight:750;
            white-space:nowrap;
            background:
                linear-gradient(
                    135deg,
                    rgba(139,92,246,.18),
                    rgba(236,72,153,.16)
                );
            border:1px solid rgba(167,139,250,.27);
        }


        /* =================================================
           LOWER TRAIT BREAKDOWN
           ================================================= */

        .ca-breakdown-grid {
            display:grid;
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
            gap:.72rem;
            margin-top:.75rem;
        }

        .ca-breakdown-card {
            min-width:0;
            min-height:112px;
            padding:.9rem 1rem;
            border-radius:17px;
            background:
                linear-gradient(
                    145deg,
                    rgba(255,255,255,.035),
                    rgba(255,255,255,.012)
                );
            border:1px solid rgba(255,255,255,.065);
        }

        .ca-breakdown-top {
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:1rem;
        }

        .ca-breakdown-name {
            color:#eeeaf4;
            font-size:.78rem;
            font-weight:800;
        }

        .ca-breakdown-score {
            color:#eeeaf4;
            font-size:.86rem;
            font-weight:850;
            white-space:nowrap;
        }

        .ca-breakdown-score span {
            color:#666374;
            font-size:.56rem;
        }

        .ca-breakdown-description {
            color:#6e6b7d;
            font-size:.61rem;
            margin-top:.22rem;
            white-space:nowrap;
            overflow:hidden;
            text-overflow:ellipsis;
        }

        .ca-breakdown-meta {
            display:flex;
            align-items:center;
            justify-content:space-between;
            margin-top:.62rem;
            color:#777286;
            font-size:.58rem;
        }


        /* =================================================
           FOOTER
           ================================================= */

        .ca-footer {
            display:flex;
            align-items:center;
            justify-content:center;
            gap:.75rem;
            margin:1.3rem 0 .5rem;
            color:#656174;
            font-size:.65rem;
            font-style:italic;
        }

        .ca-footer-line {
            width:42px;
            height:1px;
            background:rgba(255,255,255,.09);
        }


        /* =================================================
           RESPONSIVE
           ================================================= */

        @media (max-width: 1050px) {

            .ca-five-grid {
                grid-template-columns:
                    repeat(3, minmax(0, 1fr));
            }

            .ca-two-col {
                grid-template-columns:1fr;
            }

            .ca-quote {
                display:none;
            }
        }

        @media (max-width: 700px) {

            .ca-five-grid {
                grid-template-columns:
                    repeat(2, minmax(0, 1fr));
            }

            .ca-breakdown-grid {
                grid-template-columns:1fr;
            }

            .ca-ai-body {
                grid-template-columns:52px minmax(0, 1fr);
            }

            .ca-robot {
                width:52px;
                height:52px;
                min-width:52px;
                font-size:1.5rem;
            }

            .ca-ai-button {
                display:none;
            }

            .ca-interest-helper {
                display:none;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DATA HELPERS
# =========================================================

def get_traits(profile):
    raw = profile.get("traits", {})

    traits = {}

    for trait in TRAITS:
        try:
            value = float(raw.get(trait, 0) or 0)
        except (TypeError, ValueError):
            value = 0.0

        traits[trait] = max(1.0, min(5.0, value))

    return traits


def get_cluster(profile):
    try:
        return int(profile.get("cluster", 0))
    except (TypeError, ValueError):
        return 0


def get_interests(profile):
    interests = profile.get("interests", [])

    if isinstance(interests, str):
        return []

    return [
        str(item).strip()
        for item in interests
        if str(item).strip()
    ]


def trait_level(score):
    if score >= 4:
        return "High expression"
    if score >= 3:
        return "Moderate expression"
    return "Lower expression"


def percentage(score):
    return max(
        0,
        min(
            100,
            ((score - 1) / 4) * 100
        )
    )


def escape(value):
    return html.escape(str(value))


# =========================================================
# AI TEXT HELPERS
# =========================================================

def clean_ai_text(text):
    """
    Safely clean Ollama output.

    Handles:
        **bold**
        markdown headings
        numbered paragraphs
        unnecessary whitespace

    Returns HTML-safe text.
    """

    if not text:
        return ""

    text = str(text).strip()

    # Remove markdown headings.
    text = re.sub(
        r"^\s*#{1,6}\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    # Escape before adding our own HTML.
    text = html.escape(text)

    # Convert markdown bold.
    text = re.sub(
        r"\*\*(.+?)\*\*",
        r"<strong>\1</strong>",
        text
    )

    # Collapse excessive whitespace.
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    return text.strip()


def extract_ai_title(summary, fallback="Creative Empath"):
    """
    Extract a short title from an Ollama response.

    Example:
        **Samruddhi: Creative Empath**

    becomes:
        Creative Empath
    """

    if not summary:
        return fallback

    match = re.search(
        r"\*\*(?:[^:*]{1,40}:\s*)?([^*\n]{3,60})\*\*",
        str(summary)
    )

    if match:
        candidate = match.group(1).strip()

        if len(candidate.split()) <= 7:
            return candidate

    # Try the first line if it looks like a title.
    first_line = str(summary).strip().splitlines()[0]

    first_line = re.sub(
        r"^[#\-\*\s]+",
        "",
        first_line
    ).strip()

    first_line = re.sub(
        r"^[^:]{1,35}:\s*",
        "",
        first_line
    ).strip()

    if (
        first_line
        and len(first_line.split()) <= 6
        and len(first_line) <= 55
    ):
        return first_line

    return fallback


def make_ai_preview(summary):
    """
    Take only the useful introductory part of the AI reading.

    The full Ollama response can be long. The dashboard should
    show a short preview so it does not dominate the page.
    """

    if not summary:
        return (
            "ConnectAI's local AI interpretation will appear here "
            "after your personality profile is analyzed."
        )

    text = clean_ai_text(summary)

    # Remove a bold title if it was included at the beginning.
    text = re.sub(
        r"^\s*<strong>.*?</strong>\s*",
        "",
        text,
        count=1
    ).strip()

    # Convert line breaks into spaces for a compact preview.
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    # Keep the card compact.
    if len(text) > 300:
        text = text[:297].rsplit(" ", 1)[0] + "..."

    return text



# =========================================================
# CLUSTER-SPECIFIC PROFILE QUOTES
# =========================================================
#
# These are intentionally different for each ML cluster.
# They are UI copy, not generated personality facts.
#
CLUSTER_QUOTES = {
    0: (
        "A sensitive perspective, an open mind, "
        "and a quiet curiosity shape how you connect."
    ),
    1: (
        "A thoughtful mind, an independent streak, "
        "and curiosity guide the way you see the world."
    ),
    2: (
        "A grounded outlook, practical thinking, "
        "and steady instincts shape your approach."
    ),
    3: (
        "A confident presence, collaborative energy, "
        "and drive help you bring people together."
    ),
}

def get_cluster_quote(cluster):
    return CLUSTER_QUOTES.get(
        int(cluster),
        "A distinctive mix of traits gives you your own way of seeing and connecting."
    )

# =========================================================
# INTEREST ICONS
# =========================================================

INTEREST_ICONS = {
    "Music": "🎵",
    "Movies": "🎬",
    "Travel": "✈️",
    "Photography": "📷",
    "Art": "🎨",
    "Writing": "🖊️",
    "Reading": "📚",
    "Fashion": "◈",
    "Technology": "⌘",
    "Coding": "</>",
    "Gaming": "🎮",
    "Sports": "⚡",
    "Fitness": "ϟ",
    "Cooking": "◉",
    "Business": "◆",
    "Entrepreneurship": "↗",
    "Science": "✦",
    "Nature": "🌿",
    "Volunteering": "♥",
    "Dance": "♫",
    "History": "◫",
    "Design": "◇",
    "Social Media": "◎",
    "Movies & Series": "🎬",
}


# =========================================================
# RENDER FUNCTIONS
# =========================================================

def render_hero(profile, cluster_info):
    name = str(profile.get("name", "Unknown"))
    initial = name.strip()[0].upper() if name.strip() else "?"

    try:
        cluster_id = int(profile.get("cluster", 0))
    except (TypeError, ValueError):
        cluster_id = 0

    profile_quote = get_cluster_quote(cluster_id)

    st.markdown(
        f"""
        <div class="ca-hero">

            <div class="ca-hero-glow-one"></div>
            <div class="ca-hero-glow-two"></div>

            <div class="ca-hero-inner">

                <div style="
                    display:flex;
                    align-items:center;
                    justify-content:space-between;
                    gap:2rem;
                ">

                    <div style="
                        min-width:0;
                        flex:1;
                    ">

                        <div class="ca-hero-profile">

                            <div class="ca-avatar">
                                {escape(initial)}
                            </div>

                            <div style="min-width:0;">

                                <div class="ai-badge">
                                    ✦ PERSONALITY PROFILE
                                </div>

                                <div class="ca-profile-name">
                                    {escape(name)}
                                </div>

                                <div class="ca-cluster-line">
                                    {escape(cluster_info["emoji"])}
                                    &nbsp;
                                    {escape(cluster_info["name"])}
                                </div>

                            </div>

                        </div>

                        <div class="ca-cluster-description">
                            {escape(cluster_info["description"])}
                        </div>

                    </div>

                    <div class="ca-quote">

                        <div class="ca-quote-mark">
                            “
                        </div>

                        {escape(profile_quote)}

                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def render_dimensions(traits):
    st.markdown(
        """
        <div class="ca-section-row">

            <div class="ca-section-title">
                YOUR FIVE DIMENSIONS
            </div>

            <div class="ca-section-helper">
                Each dimension is scored from 1 to 5
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    icons = {
        "Extraversion": "⚡",
        "Neuroticism": "🌙",
        "Agreeableness": "💗",
        "Conscientiousness": "◇",
        "Openness": "✦",
    }

    cards = []

    for trait in TRAITS:

        score = traits[trait]
        pct = percentage(score)

        cards.append(
            f"""
            <div class="ca-dimension-card">

                <div class="ca-dimension-icon">
                    {icons.get(trait, "✦")}
                </div>

                <div class="ca-dimension-name">
                    {escape(trait)}
                </div>

                <div class="ca-dimension-value">
                    {score:.2f}
                    <span>/ 5</span>
                </div>

                <div class="ca-progress">
                    <div
                        class="ca-progress-fill"
                        style="width:{pct:.1f}%;">
                    </div>
                </div>

            </div>
            """
        )

    st.markdown(
        f"""
        <div class="ca-five-grid">
            {''.join(cards)}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_radar(traits, name):

    values = [
        traits[trait]
        for trait in TRAITS
    ]

    radar_values = values + [values[0]]
    radar_traits = TRAITS + [TRAITS[0]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=radar_values,
            theta=radar_traits,
            fill="toself",
            name=str(name),
            line=dict(
                color="#f04ba9",
                width=3
            ),
            fillcolor="rgba(240,75,169,.22)",
            hovertemplate=(
                "%{theta}: %{r:.2f}/5"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",

            radialaxis=dict(
                visible=True,
                range=[1, 5],
                tickvals=[1, 2, 3, 4, 5],
                tickfont=dict(
                    size=8,
                    color="#5f5c70"
                ),
                gridcolor="rgba(255,255,255,.075)",
                linecolor="rgba(255,255,255,.05)"
            ),

            angularaxis=dict(
                gridcolor="rgba(255,255,255,.065)",
                linecolor="rgba(255,255,255,.05)",
                tickfont=dict(
                    size=9,
                    color="#aaa5b5"
                )
            )
        ),

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,

        margin=dict(
            l=40,
            r=40,
            t=15,
            b=15
        ),

        height=335
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False,
            "responsive": True
        }
    )




# =========================================================
# FINAL SPACING / ALIGNMENT OVERRIDES
# =========================================================

def inject_final_layout_css():
    st.markdown("""
    <style>
    /* Give every major card a predictable separation. */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        margin-top: .85rem !important;
        margin-bottom: 0 !important;
        padding: 0 !important;
        border: 1px solid rgba(167,139,250,.22) !important;
        border-radius: 20px !important;
        background: linear-gradient(145deg, rgba(255,255,255,.035), rgba(255,255,255,.012)) !important;
        overflow: hidden !important;
    }

    /* Streamlit columns need breathing room between cards. */
    [data-testid="column"] {
        min-width: 0 !important;
    }

    .ca-panel-header {
        padding: 1.05rem 1.15rem .15rem !important;
    }

    .ca-radar-wrap {
        height: 365px !important;
    }

    /* Interest icons and labels share one flex baseline. */
    .ca-interest-track {
        display: flex !important;
        align-items: center !important;
        gap: .48rem !important;
        padding: .05rem 0 .05rem !important;
        overflow: hidden !important;
    }

    .ca-interest-chip {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        vertical-align: middle !important;
        height: 38px !important;
        padding: 0 .82rem !important;
        gap: .42rem !important;
        line-height: 1 !important;
    }

    .ca-interest-icon {
        width: 18px !important;
        min-width: 18px !important;
        height: 18px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1 !important;
        font-size: .82rem !important;
    }

    .ca-interest-name {
        display: inline-flex !important;
        align-items: center !important;
        height: 100% !important;
        line-height: 1 !important;
    }

    /* AI content and button have actual padding and aligned centers. */
    .ca-ai-top {
        padding: 1rem 1.1rem .25rem !important;
        margin: 0 !important;
    }

    .ca-ai-body-fixed {
        display: flex !important;
        align-items: center !important;
        gap: 1rem !important;
        min-width: 0 !important;
        padding: .55rem 0 1rem 1.1rem !important;
    }

    .ca-ai-copy {
        min-width: 0 !important;
    }

    .ca-ai-preview {
        max-height: 43px !important;
        overflow: hidden !important;
        padding-right: .3rem !important;
    }

    /* The button itself gets a comfortable hit area and never touches the edge. */
    .ca-ai-panel + div button,
    div[data-testid="stVerticalBlockBorderWrapper"] button {
        margin: .35rem .7rem .35rem 0 !important;
        min-height: 40px !important;
        padding: .55rem .85rem !important;
        border-radius: 999px !important;
        border: 1px solid rgba(236,72,153,.42) !important;
        background: linear-gradient(135deg, rgba(139,92,246,.20), rgba(236,72,153,.17)) !important;
        color: #dfc5fa !important;
        font-size: .66rem !important;
        font-weight: 800 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] button:hover {
        border-color: rgba(236,72,153,.72) !important;
        transform: translateY(-1px) !important;
    }

    .ca-ai-full {
        margin: .15rem 1.1rem 1rem !important;
        padding: 1rem 1.05rem !important;
        border-radius: 16px !important;
    }

    .ca-ai-empty {
        margin: .2rem 1.1rem 1rem !important;
    }

    .ca-footer {
        margin-top: 1.15rem !important;
        margin-bottom: .7rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# SPACING / OVERLAP SAFETY OVERRIDES
# =========================================================

def inject_spacing_safety_css():
    """Final spacing rules so cards never visually touch or overlap."""
    st.markdown("""
    <style>

    /* -------------------------------------------------
       GLOBAL PAGE RHYTHM
       ------------------------------------------------- */
    .connectai-personality {
        padding-bottom: 2.5rem !important;
    }

    .connectai-personality > * {
        margin-bottom: .15rem !important;
    }

    /* Give each major visual section clear breathing room. */
    .ca-five-grid {
        margin-top: .75rem !important;
        margin-bottom: 1.35rem !important;
        gap: .9rem !important;
    }

    .ca-dimension-card {
        padding: 1.15rem 1.05rem !important;
        min-height: 145px !important;
        height: auto !important;
    }

    /* -------------------------------------------------
       BORDERED STREAMLIT CARDS
       ------------------------------------------------- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        margin-top: 1.35rem !important;
        margin-bottom: 1.35rem !important;
        padding: 0 !important;
        overflow: visible !important;
    }

    /* Streamlit inserts an inner block inside the border wrapper.
       Give that block real internal breathing room. */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 1.05rem 1.15rem 1.15rem !important;
        border: 0 !important;
        box-sizing: border-box !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="column"] {
        padding-left: .25rem !important;
        padding-right: .25rem !important;
    }

    /* -------------------------------------------------
       FINGERPRINT
       ------------------------------------------------- */
    .ca-panel-header {
        padding: .15rem .05rem .55rem !important;
        margin-bottom: .2rem !important;
    }

    .ca-radar-wrap {
        height: 370px !important;
        padding: .1rem .35rem .35rem !important;
        margin-top: .1rem !important;
    }

    /* -------------------------------------------------
       INTERESTS
       ------------------------------------------------- */
    .ca-interest-panel {
        margin-top: 1.35rem !important;
        margin-bottom: 1.35rem !important;
        padding: 1rem 1.05rem 1.05rem !important;
    }

    .ca-interest-header {
        margin-bottom: .8rem !important;
        padding: 0 .1rem !important;
    }

    .ca-interest-track {
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        align-content: center !important;
        gap: .65rem !important;
        width: 100% !important;
        padding: .1rem !important;
        overflow: visible !important;
    }

    .ca-interest-chip {
        flex: 0 0 auto !important;
        min-width: 0 !important;
        height: 40px !important;
        padding: 0 .9rem !important;
        gap: .48rem !important;
        line-height: 1 !important;
        white-space: nowrap !important;
        margin: 0 !important;
    }

    .ca-interest-icon {
        width: 20px !important;
        min-width: 20px !important;
        height: 20px !important;
        line-height: 20px !important;
        text-align: center !important;
    }

    .ca-interest-name {
        line-height: 20px !important;
        height: 20px !important;
        display: inline-flex !important;
        align-items: center !important;
    }

    .ca-interest-arrow {
        width: 40px !important;
        height: 40px !important;
        flex: 0 0 40px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 50% !important;
        margin: 0 !important;
    }

    /* -------------------------------------------------
       AI CARD
       ------------------------------------------------- */
    .ca-ai-top {
        padding: 0 .05rem .75rem !important;
        margin: 0 !important;
    }

    .ca-ai-body-fixed {
        display: flex !important;
        align-items: center !important;
        gap: 1.2rem !important;
        width: 100% !important;
        min-width: 0 !important;
        min-height: 92px !important;
        padding: .65rem .15rem 1.05rem !important;
        margin: 0 !important;
    }

    .ca-ai-copy {
        min-width: 0 !important;
        overflow: hidden !important;
        padding: .1rem 0 !important;
    }

    /* Never allow the preview text to enter the action-button area. */
    .ca-ai-body-fixed,
    .ca-ai-copy,
    .ca-ai-preview {
        overflow-wrap: anywhere !important;
        word-break: normal !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="column"] {
        min-width: 0 !important;
    }

    .ca-ai-title {
        margin-bottom: .42rem !important;
        line-height: 1.2 !important;
    }

    .ca-ai-preview {
        padding-right: .5rem !important;
        line-height: 1.65 !important;
        max-height: 50px !important;
        overflow: hidden !important;
        margin-top: .45rem !important;
    }

    /* Button has its own space inside its column. */
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stButton"] {
        width: 100% !important;
        margin: 0 !important;
        padding: .25rem !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stButton"] button {
        width: 100% !important;
        min-height: 42px !important;
        padding: .65rem 1rem !important;
        margin: 0 !important;
        box-sizing: border-box !important;
        white-space: nowrap !important;
    }

    .ca-ai-full {
        clear: both !important;
        margin: 1.35rem 0 .25rem !important;
        padding: 1.35rem 1.35rem !important;
        border-radius: 17px !important;
        box-sizing: border-box !important;
    }

    .ca-ai-full-title {
        margin-bottom: .85rem !important;
        line-height: 1.35 !important;
    }

    .ca-ai-full-text {
        line-height: 1.8 !important;
    }

    /* -------------------------------------------------
       FOOTER / ACTIONS
       ------------------------------------------------- */
    .ca-footer {
        margin-top: 1.6rem !important;
        margin-bottom: 1rem !important;
    }

    /* Never let the bottom action buttons touch each other. */
    .connectai-personality .stButton {
        box-sizing: border-box !important;
    }

    /* -------------------------------------------------
       RESPONSIVE SAFETY
       ------------------------------------------------- */
    @media (max-width: 1050px) {
        .ca-five-grid {
            grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        }
    }

    @media (max-width: 760px) {
        .ca-five-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        }

        .ca-hero-profile {
            gap: .8rem !important;
        }

        .ca-quote {
            display: none !important;
        }

        .ca-interest-header {
            align-items: flex-start !important;
            flex-direction: column !important;
        }
    }

    @media (max-width: 520px) {
        .ca-five-grid {
            grid-template-columns: 1fr !important;
        }

        .ca-interest-chip {
            max-width: 100% !important;
        }

        .ca-ai-body-fixed {
            align-items: flex-start !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)

# =========================================================
# REFERENCE-STYLE LOWER SECTIONS
# =========================================================

def render_fingerprint(traits, name):
    """Single full-width fingerprint card; no repetitive glance card."""
    with st.container(border=True):
        st.markdown("""
        <div class="ca-panel-header">
            <div class="ca-panel-icon">✦</div>
            <div>
                <div class="ca-panel-label">PERSONALITY FINGERPRINT</div>
                <div class="ca-panel-subtitle">Your Big Five personality pattern</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        render_radar(traits, name)


def render_interests(interests):
    if not interests:
        return

    chips = []
    visible = interests[:9]
    for interest in visible:
        icon = INTEREST_ICONS.get(interest, "✦")
        chips.append(f"""
        <div class="ca-interest-chip">
            <span class="ca-interest-icon">{escape(icon)}</span>
            <span class="ca-interest-name">{escape(interest)}</span>
        </div>
        """)

    if len(interests) > len(visible):
        chips.append('<div class="ca-interest-arrow">›</div>')

    st.markdown(f"""
    <div class="ca-interest-panel">
        <div class="ca-interest-header">
            <div class="ca-interest-heading">
                <span>♥</span>
                <span>INTEREST SIGNATURE</span>
            </div>
            <div class="ca-interest-helper">
                Your interests add another layer to your personality.
            </div>
        </div>
        <div class="ca-interest-track">
            {''.join(chips)}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_ai_reading(profile):
    summary = str(profile.get("ai_summary", "") or "").strip()
    title = extract_ai_title(summary, fallback="Your AI Personality")
    preview = make_ai_preview(summary)
    profile_id = profile.get("id", "current")
    state_key = f"show_full_ai_{profile_id}"

    words = title.split()
    if len(words) >= 2:
        title_html = f"{escape(' '.join(words[:-1]))} <span>{escape(words[-1])}</span>"
    else:
        title_html = escape(title)

    # Header is HTML, while the actual action button is rendered by
    # Streamlit immediately inside the same bordered container. This
    # avoids the old button being visually detached from the AI card.
    with st.container(border=True):
        st.markdown("""
        <div class="ca-ai-top">
            <div class="ca-ai-label">
                <span>✦</span>
                <span>AI PERSONALITY READING</span>
            </div>
            <div class="ca-ai-helper">A more human perspective on your personality.</div>
        </div>
        """, unsafe_allow_html=True)

        body_col, action_col = st.columns([5.45, 1.5], gap="large", vertical_alignment="center")

        with body_col:
            st.markdown(f"""
            <div class="ca-ai-body-fixed">
                <div class="ca-robot">◉</div>
                <div class="ca-ai-copy">
                    <div class="ca-ai-title">{title_html}</div>
                    <div class="ca-ai-preview">{escape(preview)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with action_col:
            if summary:
                label = "Hide Analysis ↑" if st.session_state.get(state_key, False) else "Read Full Analysis →"
                if st.button(label, key=f"read_full_ai_{profile_id}", width="stretch"):
                    st.session_state[state_key] = not st.session_state.get(state_key, False)
                    st.rerun()

        if summary and st.session_state.get(state_key, False):
            st.markdown("""
            <div style="
                height:1px;
                margin:1.05rem .15rem 1.1rem;
                background:linear-gradient(
                    90deg,
                    rgba(139,92,246,.05),
                    rgba(167,139,250,.22),
                    rgba(236,72,153,.08)
                );
            "></div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="ca-ai-full">
                <div class="ca-ai-full-title">✦ Full AI personality analysis</div>
                <div class="ca-ai-full-text">{clean_ai_text(summary)}</div>
            </div>
            """, unsafe_allow_html=True)
        elif not summary:
            st.markdown("""
            <div class="ca-ai-empty">
                ✦ Your AI personality interpretation will appear here after your profile is analyzed.
            </div>
            """, unsafe_allow_html=True)


def render_personality(profiles):
    inject_personality_css()
    inject_final_layout_css()
    inject_spacing_safety_css()

    page_header(
        "PERSONALITY INTELLIGENCE",
        "Your personality, visualized.",
        "A machine-learning interpretation of your Big Five personality profile."
    )

    if not profiles:
        st.markdown("""
        <div class="ca-hero">
            <div class="ca-hero-inner">
                <div class="ai-badge">✦ PERSONALITY ENGINE</div>
                <div style="color:#f7f4fa;font-size:1.75rem;font-weight:850;margin-top:1rem;">
                    Your personality fingerprint is waiting.
                </div>
                <div style="color:#a39baa;font-size:.82rem;line-height:1.7;margin-top:.45rem;max-width:650px;">
                    Complete the ConnectAI assessment to discover your Big Five personality profile.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create My Profile →", type="primary", width="stretch", key="personality_create_empty"):
            st.session_state.current_page = "Create Profile"
            st.rerun()
        return

    current_id = st.session_state.get("current_profile_id")
    profile = next((p for p in profiles if p.get("id") == current_id), profiles[0])
    name = str(profile.get("name", "Unknown"))
    traits = get_traits(profile)
    cluster = get_cluster(profile)
    cluster_info = CLUSTER_INFO.get(cluster, {
        "name": f"Cluster {cluster}",
        "emoji": "✦",
        "description": "A unique personality pattern discovered by the ML engine."
    })
    interests = get_interests(profile)

    render_hero(profile, cluster_info)
    render_dimensions(traits)

    # Full-width fingerprint gives the radar enough breathing room and
    # removes the repetitive At a Glance panel.
    render_fingerprint(traits, name)

    # Interests are only rendered when data exists.
    render_interests(interests)

    # Compact AI card with a real working button.
    render_ai_reading(profile)

    st.markdown("""
    <div class="ca-footer">
        <span class="ca-footer-line"></span>
        “Different minds. A more connected world.”
        <span class="ca-footer-line"></span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button("Discover My Matches  ✧", type="primary", width="stretch", key="personality_discover"):
            st.session_state.current_page = "Discover Matches"
            st.rerun()
    with col2:
        if st.button("Ask ConnectAI  ✦", width="stretch", key="personality_ask"):
            st.session_state.current_page = "Ask ConnectAI"
            st.rerun()

