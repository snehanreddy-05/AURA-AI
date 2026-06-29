"""
pages/1_💬_Career_Chat.py
AURA AI — Career Chat
Renders messages exactly like the reference screenshot:
  User  → right-aligned bubble, "You" + timestamp above
  AURA  → left-aligned bubble with sparkle avatar, "AURA AI" + timestamp above
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.theme import (
    apply_theme, sidebar_brand, sidebar_nav, sidebar_footer,
    page_title, gold_divider, chat_disclaimer, render_message, now_time,
)
from utils.ai_engine import get_ai_response

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AURA AI – Career Chat",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    sidebar_brand()
    sidebar_nav("Career Chat")
    sidebar_footer()

# ── Page heading ──────────────────────────────────────────────────────────────
page_title(
    icon="💬",
    title_white="Career",
    title_gold="Chat",
    subtitle="Ask coding, AI, placement, interview, career and learning questions.",
)
gold_divider()

# ── Session state ─────────────────────────────────────────────────────────────
if "career_messages" not in st.session_state:
    st.session_state.career_messages: list[dict] = []

# ── Render existing history ───────────────────────────────────────────────────
for msg in st.session_state.career_messages:
    render_message(msg["role"], msg["content"], msg.get("time", ""))

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask me anything..."):
    ts_user = now_time()

    # 1 — store & render user message
    st.session_state.career_messages.append(
        {"role": "user", "content": prompt, "time": ts_user}
    )
    render_message("user", prompt, ts_user)

    # 2 — show typing indicator while waiting
    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="aura-msg-ai-wrap">
        <div class="aura-ai-avatar">✦</div>
        <div class="aura-typing-dots">
            <span></span><span></span><span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3 — call AI
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.career_messages[:-1]   # exclude the just-added user msg
    ]
    response = get_ai_response(prompt, mode="career", history=history)

    # 4 — clear typing indicator, store & render AI message
    typing_placeholder.empty()
    ts_ai = now_time()
    st.session_state.career_messages.append(
        {"role": "assistant", "content": response, "time": ts_ai}
    )
    render_message("assistant", response, ts_ai)

# ── Disclaimer ────────────────────────────────────────────────────────────────
chat_disclaimer()
