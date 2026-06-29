"""
pages/3_📚_PDF_Assistant.py
AURA AI — PDF Assistant
Upload → auto-summary → persistent chat Q&A session
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.theme import (
    apply_theme, sidebar_brand, sidebar_nav, sidebar_footer,
    page_title, gold_divider, chat_disclaimer, render_message, now_time,
)
from utils.pdf_utils import extract_pdf_text, get_pdf_page_count
from utils.ai_engine import get_ai_response

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AURA AI – PDF Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    sidebar_brand()
    sidebar_nav("PDF Assistant")
    sidebar_footer()

# ── Page heading ──────────────────────────────────────────────────────────────
page_title(
    icon="📚",
    title_white="PDF",
    title_gold="Assistant",
    subtitle="Upload study material, research papers, or notes — then ask anything.",
)
gold_divider()

# ── Session state initialisation ─────────────────────────────────────────────
if "pdf_messages"  not in st.session_state: st.session_state.pdf_messages  = []
if "pdf_context"   not in st.session_state: st.session_state.pdf_context   = ""
if "pdf_doc_name"  not in st.session_state: st.session_state.pdf_doc_name  = ""
if "pdf_pages"     not in st.session_state: st.session_state.pdf_pages     = 0


# ── Upload panel ──────────────────────────────────────────────────────────────
with st.expander(
    "📎 Upload Document" + (f"  ·  **{st.session_state.pdf_doc_name}**" if st.session_state.pdf_doc_name else ""),
    expanded=not st.session_state.pdf_context,
):
    uploaded = st.file_uploader(
        "Drop a PDF here (max 200 MB)",
        type=["pdf"],
        key="pdf_uploader",
        help="Supports text-based PDFs. For scanned documents, OCR support may be limited.",
    )

    col_upload, col_clear = st.columns([4, 1])

    with col_upload:
        if uploaded and uploaded.name != st.session_state.pdf_doc_name:
            with st.spinner("📖 Reading PDF…"):
                text = extract_pdf_text(uploaded)

            if text.strip():
                pages = get_pdf_page_count(uploaded)
                st.session_state.pdf_context  = text
                st.session_state.pdf_doc_name = uploaded.name
                st.session_state.pdf_pages    = pages
                st.session_state.pdf_messages = []

                # Auto-generate document summary
                with st.spinner("🤖 Generating summary…"):
                    summary = get_ai_response(
                        "Provide a concise 4–5 sentence summary of this document. "
                        "Then list the 5 main topics covered as bullet points.",
                        context=text,
                        mode="study",
                    )

                ts = now_time()
                welcome = (
                    f"📄 **{uploaded.name}** loaded successfully "
                    f"({pages} pages, {len(text):,} characters)!\n\n"
                    f"**Summary:**\n{summary}\n\n"
                    "---\n*Ask me anything about this document!*"
                )
                st.session_state.pdf_messages.append(
                    {"role": "assistant", "content": welcome, "time": ts}
                )
                st.success(f"✅ '{uploaded.name}' ready — {pages} pages")
                st.rerun()
            else:
                st.error(
                    "⚠️ Could not extract text from this PDF. "
                    "It may be scanned or image-based. "
                    "Ensure Tesseract OCR is installed for scanned documents."
                )

    with col_clear:
        if st.session_state.pdf_doc_name:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.pdf_context  = ""
                st.session_state.pdf_doc_name = ""
                st.session_state.pdf_pages    = 0
                st.session_state.pdf_messages = []
                st.rerun()


# ── Active document status bar ────────────────────────────────────────────────
if st.session_state.pdf_doc_name:
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:8px;'
        f'padding:0.45rem 0.85rem;margin-bottom:0.8rem;'
        f'background:rgba(240,165,0,0.07);'
        f'border:1px solid rgba(240,165,0,0.22);border-radius:10px;'
        f'font-size:13px;color:#F0A500;">'
        f'📄 <strong>{st.session_state.pdf_doc_name}</strong>'
        f'<span style="color:#4A5180;margin-left:auto;">'
        f'{st.session_state.pdf_pages} pages · '
        f'{len(st.session_state.pdf_context):,} chars</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.pdf_messages:
    render_message(msg["role"], msg["content"], msg.get("time", ""))


# ── Chat input ────────────────────────────────────────────────────────────────
if st.session_state.pdf_context:
    placeholder_text = "Ask a question about your document…"
else:
    placeholder_text = "Upload a PDF above to start asking questions…"

if prompt := st.chat_input(placeholder_text):
    if not st.session_state.pdf_context:
        st.warning("⚠️ Please upload a PDF document first.")
        st.stop()

    ts_user = now_time()
    st.session_state.pdf_messages.append(
        {"role": "user", "content": prompt, "time": ts_user}
    )
    render_message("user", prompt, ts_user)

    # Typing indicator
    typing_ph = st.empty()
    typing_ph.markdown("""
    <div class="aura-msg-ai-wrap">
        <div class="aura-ai-avatar">✦</div>
        <div class="aura-typing-dots">
            <span></span><span></span><span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Multi-turn history for context
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.pdf_messages[:-1]
    ]
    response = get_ai_response(
        prompt,
        context=st.session_state.pdf_context,
        mode="study",
        history=history,
    )

    typing_ph.empty()
    ts_ai = now_time()
    st.session_state.pdf_messages.append(
        {"role": "assistant", "content": response, "time": ts_ai}
    )
    render_message("assistant", response, ts_ai)


# ── Disclaimer ────────────────────────────────────────────────────────────────
chat_disclaimer()
