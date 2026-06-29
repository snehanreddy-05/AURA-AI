"""
pages/2_📄_Resume_Studio.py
AURA AI — Resume Studio
Four tabs: ATS Score | Resume Review | Skill Gap | Interview Prep
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.theme import (
    apply_theme, sidebar_brand, sidebar_nav, sidebar_footer,
    page_title, gold_divider, aura_card,
)
from utils.pdf_utils import extract_pdf_text
from utils.resume_utils import (
    analyze_resume, generate_interview_questions,
    skill_gap_analysis, ats_resume_score,
)

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AURA AI – Resume Studio",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    sidebar_brand()
    sidebar_nav("Resume Studio")
    sidebar_footer()

# ── Page heading ──────────────────────────────────────────────────────────────
page_title(
    icon="📄",
    title_white="Resume",
    title_gold="Studio",
    subtitle="ATS Analysis · Resume Review · Skill Gap Detection · Interview Preparation",
)
gold_divider()


# ── Shared helper ─────────────────────────────────────────────────────────────
def _get_resume_input(tab_key: str) -> str:
    """
    Two-column upload + paste widget.
    Returns the resume text from whichever source has content.
    """
    c1, c2 = st.columns([1, 1], gap="medium")
    resume_text = ""

    with c1:
        st.markdown("**📎 Upload Resume (PDF)**")
        uploaded = st.file_uploader(
            "Drop your PDF here",
            type=["pdf"],
            key=f"upload_{tab_key}",
            label_visibility="collapsed",
        )
        if uploaded:
            text = extract_pdf_text(uploaded)
            if text.strip():
                resume_text = text
                st.success(f"✅ Loaded — {len(text):,} characters across {text.count(chr(12))+1} pages")
            else:
                st.warning("⚠️ Could not extract text. Try pasting below.")

    with c2:
        st.markdown("**📝 Or paste resume text**")
        pasted = st.text_area(
            "Paste resume text here",
            height=180,
            key=f"paste_{tab_key}",
            placeholder="Copy and paste your resume content here…",
            label_visibility="collapsed",
        )
        if pasted.strip():
            resume_text = pasted  # paste overrides upload if both present

    return resume_text


def _result_card(result: str):
    """Render AI result in a styled card using st.markdown (full markdown)."""
    st.markdown(
        f'<div class="aura-card-gold" style="margin-top:1rem;">'
        f'</div>',
        unsafe_allow_html=True,
    )
    # st.markdown handles headers, bullets, tables properly
    with st.container():
        st.markdown(result)


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  ATS Score",
    "🔍  Resume Review",
    "🎯  Skill Gap",
    "🎤  Interview Prep",
])

# ── Tab 1 — ATS Score ─────────────────────────────────────────────────────────
with tab1:
    st.markdown("### 📊 ATS Compatibility Score")
    st.markdown(
        "Instantly see how well your resume passes automated ATS screening — "
        "with a category breakdown and quick-fix suggestions."
    )
    resume_text = _get_resume_input("ats")

    if st.button("🚀 Run ATS Analysis", type="primary", use_container_width=True, key="btn_ats"):
        if not resume_text.strip():
            st.error("⚠️ Please upload a PDF or paste resume text first.")
        else:
            with st.spinner("Running ATS analysis…"):
                result = ats_resume_score(resume_text)
            _result_card(result)

# ── Tab 2 — Resume Review ─────────────────────────────────────────────────────
with tab2:
    st.markdown("### 🔍 Comprehensive Resume Review")
    st.markdown(
        "Get an in-depth critique covering skills, strengths, weaknesses, "
        "project suggestions, and a 6-month career roadmap."
    )
    resume_text = _get_resume_input("review")

    if st.button("🔍 Review My Resume", type="primary", use_container_width=True, key="btn_review"):
        if not resume_text.strip():
            st.error("⚠️ Please upload a PDF or paste resume text first.")
        else:
            with st.spinner("Analysing your resume…"):
                result = analyze_resume(resume_text)
            _result_card(result)

# ── Tab 3 — Skill Gap Analysis ────────────────────────────────────────────────
with tab3:
    st.markdown("### 🎯 Skill Gap Analysis")
    st.markdown(
        "Compare your current skills against your target role and receive "
        "a structured 12-week learning roadmap."
    )
    resume_text = _get_resume_input("gap")

    target_role = st.text_input(
        "🎯 Target Role",
        placeholder="e.g.  Senior Data Scientist · Full Stack Developer · ML Engineer",
        key="target_role",
    )

    if st.button("🎯 Analyse Skill Gap", type="primary", use_container_width=True, key="btn_gap"):
        if not resume_text.strip():
            st.error("⚠️ Please upload a PDF or paste resume text first.")
        elif not target_role.strip():
            st.error("⚠️ Please enter your target role.")
        else:
            with st.spinner(f"Comparing against '{target_role}'…"):
                result = skill_gap_analysis(resume_text, target_role.strip())
            _result_card(result)

# ── Tab 4 — Interview Prep ────────────────────────────────────────────────────
with tab4:
    st.markdown("### 🎤 Interview Preparation")
    st.markdown(
        "Generate a bespoke question set — technical, project deep-dives, "
        "behavioral, and must-revise topics — tailored to YOUR resume."
    )
    resume_text = _get_resume_input("interview")

    if st.button("🎤 Generate Question Set", type="primary", use_container_width=True, key="btn_interview"):
        if not resume_text.strip():
            st.error("⚠️ Please upload a PDF or paste resume text first.")
        else:
            with st.spinner("Generating personalised questions…"):
                result = generate_interview_questions(resume_text)
            _result_card(result)
