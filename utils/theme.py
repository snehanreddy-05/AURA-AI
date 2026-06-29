"""
utils/theme.py
AURA AI — Theme utilities v2.0
Provides: apply_theme, sidebar_brand, sidebar_nav, sidebar_footer,
          page_title, gold_divider, chat_disclaimer,
          render_message, now_time, aura_card
"""

import os
import re
import html
import streamlit as st
from datetime import datetime



# ── Internal helpers ──────────────────────────────────────────────────────────

def _css_path() -> str:
    base = os.path.dirname(__file__)
    return os.path.join(base, "..", "assets", "css", "aura_theme.css")


def _md_to_html(text: str) -> str:
    """Convert basic markdown to safe HTML for chat bubbles."""
    # Escape HTML entities
    text = html.escape(text)
    # Fenced code blocks  ``` ... ```
    text = re.sub(
        r'```(\w*)\n(.*?)```',
        lambda m: f'<pre style="background:rgba(0,0,0,0.35);border:1px solid rgba(255,255,255,0.07);'
                  f'border-radius:8px;padding:10px 14px;overflow-x:auto;font-size:12.5px;margin:8px 0;">'
                  f'<code>{m.group(2)}</code></pre>',
        text, flags=re.DOTALL
    )
    # Inline code
    text = re.sub(
        r'`([^`]+)`',
        r'<code style="background:rgba(123,111,240,0.18);border:1px solid rgba(123,111,240,0.22);'
        r'border-radius:4px;padding:1px 6px;font-size:12.5px;color:#FFD166;">\1</code>',
        text
    )
    # Bold + italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.+?)\*\*',     r'<strong>\1</strong>',          text)
    text = re.sub(r'\*(.+?)\*',          r'<em>\1</em>',                  text)
    # Headers (## and ###)
    text = re.sub(r'^### (.+)$',
                  r'<h3 style="color:#E8ECF8;font-size:14.5px;font-weight:600;margin:10px 0 4px;">\1</h3>',
                  text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$',
                  r'<h2 style="color:#E8ECF8;font-size:15.5px;font-weight:600;margin:10px 0 4px;">\1</h2>',
                  text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$',
                  r'<h1 style="color:#E8ECF8;font-size:17px;font-weight:700;margin:10px 0 5px;">\1</h1>',
                  text, flags=re.MULTILINE)
    # Unordered list items
    text = re.sub(r'^[-*] (.+)$',
                  r'<li style="margin:3px 0;">\1</li>',
                  text, flags=re.MULTILINE)
    # Numbered list items
    text = re.sub(r'^\d+\. (.+)$',
                  r'<li style="margin:3px 0;">\1</li>',
                  text, flags=re.MULTILINE)
    # Wrap consecutive <li> in <ul>
    text = re.sub(
        r'(<li[^>]*>.*?</li>\n?)+',
        lambda m: f'<ul style="margin:6px 0;padding-left:20px;">{m.group(0)}</ul>',
        text, flags=re.DOTALL
    )
    # Paragraph breaks
    text = re.sub(r'\n{2,}', '</p><p style="margin:5px 0;">', text)
    # Single line breaks
    text = text.replace('\n', '<br>')
    return f'<p style="margin:0;">{text}</p>'


# ── Public API ────────────────────────────────────────────────────────────────

def apply_theme():
    """Inject AURA CSS + twinkling star background into any page."""
    with open(_css_path(), "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    # Twinkling stars (runs once per page load)
    st.markdown("""
    <script>
    (function() {
        if (document.querySelectorAll('.star-dot').length) return;
        for (let i = 0; i < 60; i++) {
            const s = document.createElement('div');
            s.className = 'star-dot';
            s.style.left              = (Math.random() * 100) + 'vw';
            s.style.top               = (Math.random() * 100) + 'vh';
            s.style.opacity           = (Math.random() * 0.6 + 0.1).toFixed(2);
            s.style.animationDuration = (Math.random() * 4 + 2).toFixed(1) + 's';
            s.style.animationDelay    = (Math.random() * 4).toFixed(1)     + 's';
            document.body.appendChild(s);
        }
    })();
    </script>
    """, unsafe_allow_html=True)


def sidebar_brand():
    """Render the space/Earth hero section at the top of the sidebar."""
    st.sidebar.markdown("""
    <div class="aura-sidebar-hero">
        <div class="aura-earth-bg"></div>
        <div class="aura-brand-overlay">
            <div class="aura-logo">✦</div>
            <p class="aura-brand-name">AURA AI</p>
            <p class="aura-brand-tagline">Your Intelligent Career &amp; Learning Companion</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def sidebar_nav(current_page: str = ""):
    """
    Render styled navigation items.
    Active page renders as a highlighted HTML div (no click needed).
    Inactive pages render as styled Streamlit buttons that call switch_page().

    Paths are resolved to absolute OS paths from the project root so that
    emoji filenames work correctly on Windows with any Streamlit version.
    """
    # theme.py lives at  <project_root>/utils/theme.py
    # so the project root is one level up from here.
    _root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def _p(*parts: str) -> str:
        """Join parts relative to project root and return an absolute path."""
        return os.path.join(_root, *parts)

    pages = [
        ("🏠", "Home",           _p("app.py")),
        ("💬", "Career Chat",    _p("pages", "1_💬_Career_Chat.py")),
        ("📄", "Resume Studio",  _p("pages", "2_📄_Resume_Studio.py")),
        ("📚", "PDF Assistant",  _p("pages", "3_PDF_Assistant.py")),
        ("ℹ️", "About AURA",     _p("pages", "4_ℹ️_About.py")),
    ]
    st.sidebar.markdown('<div style="padding:0.5rem 0.5rem 0;">', unsafe_allow_html=True)

    for icon, label, path in pages:
        is_active = (label == current_page)
        if is_active:
            st.sidebar.markdown(f"""
            <div style="
                display:flex;align-items:center;gap:12px;
                padding:0.62rem 1rem;border-radius:10px;
                background:rgba(240,165,0,0.10);
                border-left:3px solid #F0A500;
                color:#E8ECF8;font-size:14px;font-weight:500;
                margin-bottom:2px;font-family:'Inter',sans-serif;
                cursor:default;
            ">
                <span style="font-size:15px;width:20px;text-align:center;">{icon}</span>
                <span>{label}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.sidebar.button(f"{icon}  {label}",
                                 key=f"nav_{label}",
                                 use_container_width=True):
                st.switch_page(path)

    st.sidebar.markdown('</div>', unsafe_allow_html=True)


def sidebar_footer():
    """Render the AURA AI info card at the bottom of the sidebar."""
    st.sidebar.markdown("""
    <div style="padding:1rem 0.75rem 0.75rem;">
        <div style="
            display:flex;align-items:center;gap:10px;
            padding:0.75rem 1rem;
            background:rgba(255,255,255,0.03);
            border-radius:12px;
            border:1px solid rgba(255,255,255,0.07);
        ">
            <div style="
                width:34px;height:34px;min-width:34px;flex-shrink:0;
                border-radius:50%;
                background:radial-gradient(circle at 40% 35%,#4A90E2,#7B6FF0);
                display:flex;align-items:center;justify-content:center;
                font-size:14px;
                box-shadow:0 0 12px rgba(123,111,240,0.5);
            ">✦</div>
            <div>
                <p style="margin:0;font-size:13px;font-weight:500;color:#E8ECF8;">AURA AI</p>
                <p style="margin:0;font-size:11px;color:#7A82A8;line-height:1.4;">
                    Empowering Your Future<br>with Intelligence
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def page_title(icon: str, title_white: str, title_gold: str, subtitle: str = ""):
    """Render the styled two-tone page heading."""
    st.markdown(f"""
    <div class="aura-page-title">
        <span style="font-size:28px;">{icon}</span>
        <h1>{title_white} <span>{title_gold}</span></h1>
    </div>
    {"<p class='aura-page-subtitle'>" + subtitle + "</p>" if subtitle else ""}
    """, unsafe_allow_html=True)


def gold_divider():
    """Thin gold-to-transparent gradient rule."""
    st.markdown("""
    <div style="height:1px;
         background:linear-gradient(to right,#F0A500,transparent);
         margin-bottom:1.25rem;opacity:0.5;"></div>
    """, unsafe_allow_html=True)


def chat_disclaimer():
    """Render the footer disclaimer on chat pages."""
    st.markdown("""
    <div class="aura-disclaimer">
        🛡️ &nbsp;AURA AI can make mistakes. Please verify important information.
    </div>
    """, unsafe_allow_html=True)


def render_message(role: str, content: str, timestamp: str):
    """
    Render a single chat bubble exactly matching the screenshot:
      • user  → right-aligned, 'You' + timestamp above bubble
      • ai    → left-aligned,  avatar + 'AURA AI' + timestamp, then bubble
    """
    content_html = _md_to_html(content)

    if role == "user":
        st.markdown(f"""
        <div class="aura-msg-user-wrap">
            <div class="aura-msg-user-header">
                <span class="aura-sender-you">You</span>
                <span class="aura-msg-time">{timestamp}</span>
            </div>
            <div class="aura-bubble-user">{content_html}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="aura-msg-ai-wrap">
            <div class="aura-ai-avatar">✦</div>
            <div class="aura-msg-ai-body">
                <div class="aura-msg-ai-header">
                    <span class="aura-sender-ai">AURA AI</span>
                    <span class="aura-msg-time">{timestamp}</span>
                </div>
                <div class="aura-bubble-ai">{content_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def now_time() -> str:
    """Current wall-clock time formatted for chat timestamps."""
    return datetime.now().strftime("%I:%M %p").lstrip("0")


def aura_card(content_html: str, gold_border: bool = False):
    """Wrap arbitrary HTML in an AURA-styled card."""
    cls = "aura-card-gold" if gold_border else "aura-card"
    st.markdown(f'<div class="{cls}">{content_html}</div>', unsafe_allow_html=True)
