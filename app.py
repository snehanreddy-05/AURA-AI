"""
app.py
AURA AI — Home / Landing Page
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from utils.theme import apply_theme, sidebar_brand, sidebar_nav, sidebar_footer

# ── Must be the very first Streamlit call ─────────────────────────────────────
st.set_page_config(
    page_title="AURA AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    sidebar_brand()
    sidebar_nav("Home")
    sidebar_footer()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding-top:36px;padding-bottom:8px;">
    <h1 style="
        font-size:3.6rem;font-weight:800;
        color:white;margin-bottom:10px;
        text-shadow:
            0 0 14px rgba(74,144,226,0.55),
            0 0 28px rgba(123,111,240,0.35);
    "> Welcome to AURA AI </h1>
    <h3 style="color:#FBBF24;font-weight:500;margin-bottom:20px;">
        Where Ambition Meets Intelligence
    </h3>
    <p style="font-size:1.1rem;color:#CBD5E1;max-width:780px;
              margin:auto;line-height:1.85;">
        Build Skills. Shape Careers. Unlock Opportunities.<br>
        — all in one powerful platform.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Feature Cards ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="aura-card" style="min-height:160px;">
        <h2 style="margin-top:0;">💬 Career Chat</h2>
        <p style="color:#CBD5E1;">Ask career, coding, AI, placement,
        DSA and interview questions instantly.</p>
        <p style="color:#F0A500;margin-bottom:0;">24/7 Intelligent Mentor</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="aura-card" style="min-height:160px;">
        <h2 style="margin-top:0;">📄 Resume Studio</h2>
        <p style="color:#CBD5E1;">ATS Analysis, Resume Review,
        Skill Gap Detection, Interview Preparation.</p>
        <p style="color:#F0A500;margin-bottom:0;">Career Optimization</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="aura-card" style="min-height:160px;">
        <h2 style="margin-top:0;">📚 PDF Assistant</h2>
        <p style="color:#CBD5E1;">Upload notes, research papers or study
        material and ask questions instantly.</p>
        <p style="color:#F0A500;margin-bottom:0;">Smart Learning</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Quick Actions ─────────────────────────────────────────────────────────────
st.markdown("## 🚀 Quick Actions")

q1, q2, q3 = st.columns(3, gap="medium")

with q1:
    if st.button("💬 Start Career Chat", use_container_width=True, type="primary"):
        st.switch_page("pages/1_💬_Career_Chat.py")

with q2:
    if st.button("📄 Open Resume Studio", use_container_width=True, type="primary"):
        st.switch_page("pages/2_📄_Resume_Studio.py")

with q3:
    if st.button("📚 Open PDF Assistant", use_container_width=True, type="primary"):
        st.switch_page("pages/3_📚_PDF_Assistant.py")

st.markdown("---")

# ── Why AURA ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="aura-card">
    <h2 style="color:#F0A500;margin-top:0;">🚀 Why AURA AI?</h2>
    <ul style="color:#CBD5E1;line-height:2.2;margin-bottom:0;">
        <li>🤖 <strong style="color:#E8ECF8;">AI Career Guidance</strong>
            — answers for any career or coding question</li>
        <li>📊 <strong style="color:#E8ECF8;">Resume Intelligence</strong>
            — ATS scoring, skill-gap analysis, instant review</li>
        <li>🎤 <strong style="color:#E8ECF8;">Interview Preparation</strong>
            — personalised question generation from your resume</li>
        <li>📚 <strong style="color:#E8ECF8;">PDF Learning Assistant</strong>
            — smart Q&amp;A over any document</li>
        <li>🗺️ <strong style="color:#E8ECF8;">Learning Roadmaps</strong>
            — structured week-by-week paths to your goals</li>
    </ul>
</div>
""", unsafe_allow_html=True)
