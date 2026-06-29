"""
pages/4_ℹ️_About.py
AURA AI — About Page
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.theme import (
    apply_theme, sidebar_brand, sidebar_nav, sidebar_footer,
    page_title, gold_divider,
)

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AURA AI – About",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    sidebar_brand()
    sidebar_nav("About AURA")
    sidebar_footer()

# ── Heading ───────────────────────────────────────────────────────────────────
page_title(
    icon="ℹ️",
    title_white="About",
    title_gold="AURA",
    subtitle="Your Intelligent Career & Learning Companion",
)
gold_divider()

# ── Main two-column layout ────────────────────────────────────────────────────
left, right = st.columns([3, 2], gap="large")

with left:
    # What is AURA
    st.markdown("""
    <div class="aura-card">
        <h2 style="color:#F0A500;margin-top:0;">🚀 What is AURA AI?</h2>
        <p style="color:#CBD5E1;line-height:1.85;margin-bottom:0;">
            AURA AI is an intelligent career and learning companion built to help
            students and professionals accelerate their career journey. Powered by
            cutting-edge large language models via the OpenRouter API, AURA provides
            personalised guidance across career development, technical skills, resume
            optimisation, and academic learning — all in a single, beautiful platform.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Features
    st.markdown("""
    <div class="aura-card">
        <h2 style="color:#F0A500;margin-top:0;">✨ Core Features</h2>
        <ul style="color:#CBD5E1;line-height:2.3;margin-bottom:0;">
            <li>💬 <strong style="color:#E8ECF8;">Career Chat</strong>
                — AI mentor for coding, placement, DSA, and career Q&amp;A</li>
            <li>📄 <strong style="color:#E8ECF8;">Resume Studio</strong>
                — ATS scoring, skill gap, and personalised interview questions</li>
            <li>📚 <strong style="color:#E8ECF8;">PDF Assistant</strong>
                — smart Q&amp;A over any uploaded document with auto-summary</li>
            <li>🎯 <strong style="color:#E8ECF8;">Skill Gap Analysis</strong>
                — 12-week roadmap to your target role</li>
            <li>🎤 <strong style="color:#E8ECF8;">Interview Prep</strong>
                — technical, behavioral, and deep-dive questions from your resume</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Future roadmap
    st.markdown("""
    <div class="aura-card">
        <h2 style="color:#F0A500;margin-top:0;">🔭 Future Roadmap</h2>
        <ul style="color:#CBD5E1;line-height:2.2;margin-bottom:0;">
            <li>🎙️ Voice assistant integration</li>
            <li>🌍 Multi-language support</li>
            <li>💼 AI-powered job recommendation engine</li>
            <li>📈 Learning progress tracker &amp; streaks</li>
            <li>🔗 LinkedIn profile optimiser</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with right:
    # Tech stack
    st.markdown("""
    <div class="aura-card-gold">
        <h2 style="color:#F0A500;margin-top:0;">🛠️ Tech Stack</h2>
        <ul style="color:#CBD5E1;line-height:2.3;margin-bottom:0;">
            <li>🐍 Python 3.10+</li>
            <li>⚡ Streamlit (multi-page)</li>
            <li>🤖 OpenRouter API (LLM backend)</li>
            <li>📄 pdfplumber + PyPDF2</li>
            <li>🔍 Tesseract OCR + pdf2image</li>
            <li>🎨 Custom CSS (Space Theme)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Developer card
    st.markdown("""
    <div class="aura-card">
        <h2 style="color:#F0A500;margin-top:0;">👨‍💻 Developer</h2>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
            <div style="
                width:48px;height:48px;min-width:48px;
                border-radius:50%;
                background:radial-gradient(circle at 38% 35%,#4A90E2,#7B6FF0);
                display:flex;align-items:center;justify-content:center;
                font-size:20px;
                box-shadow:0 0 14px rgba(123,111,240,0.5);
            ">S</div>
            <div>
                <p style="margin:0;font-size:17px;font-weight:600;color:#E8ECF8;">
                    Snehan Reddy
                </p>
                <p style="margin:0;font-size:12px;color:#7A82A8;">
                    AI &amp; Career Tools Developer
                </p>
            </div>
        </div>
        <p style="color:#CBD5E1;font-size:13px;line-height:1.7;margin-bottom:0;">
            Building intelligent tools for the next generation of engineers and
            helping students land their dream roles through AI-powered guidance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Model info
    st.markdown("""
    <div class="aura-card">
        <h2 style="color:#F0A500;margin-top:0;">🤖 AI Model</h2>
        <p style="color:#CBD5E1;font-size:13px;line-height:1.7;margin-bottom:0;">
            Powered by <strong style="color:#E8ECF8;">NVIDIA Nemotron</strong>
            via the OpenRouter API — one of the most capable free-tier models
            for reasoning, coding, and career analysis tasks.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="aura-card" style="text-align:center;padding:1rem;">
    <span style="font-size:22px;">♾️</span>
    <p style="color:#7A82A8;font-size:13px;margin:6px 0 0;">
        AURA AI v2.0 — Where Ambition Meets Intelligence
    </p>
</div>
""", unsafe_allow_html=True)
