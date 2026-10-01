# ui/components.py

import streamlit as st
from textwrap import dedent

from config.constants import TRAIT_META, CLUSTER_INFO


def render_html(html):
    """
    Render HTML safely without allowing Python indentation
    to turn the HTML into a Markdown code block.
    """
    st.markdown(
        dedent(html).strip(),
        unsafe_allow_html=True
    )


def page_header(eyebrow, title, subtitle=""):

    render_html(
        f"""
        <div class="eyebrow">{eyebrow}</div>
        <div class="page-title">{title}</div>
        <div class="page-subtitle">{subtitle}</div>
        """
    )


def glass_card(title, content):

    render_html(
        f"""
        <div class="glass-card">

            <div style="
                font-size:1.1rem;
                font-weight:700;
                margin-bottom:0.6rem;
            ">
                {title}
            </div>

            <div style="
                color:#9696aa;
                line-height:1.7;
            ">
                {content}
            </div>

        </div>
        """
    )


def stat_card(label, value, description=""):

    render_html(
        f"""
        <div class="stat-card">

            <div class="stat-label">
                {label}
            </div>

            <div class="stat-value">
                {value}
            </div>

            <div class="stat-description">
                {description}
            </div>

        </div>
        """
    )


def trait_card(trait, score):

    meta = TRAIT_META.get(
        trait,
        {
            "icon": "✦",
            "description": ""
        }
    )

    percentage = max(
        0,
        min(
            100,
            ((float(score) - 1) / 4) * 100
        )
    )

    render_html(
        f"""
        <div class="trait-card">

            <div class="trait-icon">
                {meta["icon"]}
            </div>

            <div class="trait-name">
                {trait}
            </div>

            <div class="trait-score">
                {float(score):.2f}

                <span style="
                    font-size:0.75rem;
                    color:#66667a;
                    font-weight:500;
                ">
                    / 5
                </span>
            </div>

            <div class="trait-bar">

                <div
                    class="trait-fill"
                    style="width:{percentage}%"
                ></div>

            </div>

        </div>
        """
    )


def profile_avatar(name):

    letter = (
        name.strip()[0].upper()
        if name and name.strip()
        else "?"
    )

    return dedent(
        f"""
        <div class="profile-avatar">
            {letter}
        </div>
        """
    ).strip()


def cluster_badge(cluster):

    info = CLUSTER_INFO.get(
        int(cluster),
        {
            "name": f"Cluster {cluster}",
            "emoji": "✦"
        }
    )

    return f'{info["emoji"]} {info["name"]}'


def match_score(score):

    render_html(
        f"""
        <div>

            <div class="match-score">
                {float(score):.1f}%
            </div>

            <div class="match-label">
                compatibility
            </div>

        </div>
        """
    )


def ai_card(title, content):

    render_html(
        f"""
        <div class="ai-card">

            <span class="ai-badge">
                ✦ ConnectAI Intelligence
            </span>

            <h3 style="margin-top:0.9rem;">
                {title}
            </h3>

            <div style="
                color:#b0b0c1;
                line-height:1.75;
            ">
                {content}
            </div>

        </div>
        """
    )