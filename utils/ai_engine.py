"""
utils/ai_engine.py
AURA AI — OpenRouter API engine
Bug-fix: API key was stored as a list; corrected to string.
"""

import os
import streamlit as st

# Load .env locally if dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Not available on Streamlit Cloud — that's fine

# Reads from Streamlit Secrets on Cloud, from .env locally
OPENROUTER_API_KEY = (
    st.secrets.get("OPENROUTER_API_KEY", None)
    or os.getenv("OPENROUTER_API_KEY", "")
)
OPENROUTER_URL     = "https://openrouter.ai/api/v1/chat/completions"
MODEL              = "nvidia/nemotron-3-ultra-550b-a55b:free"

# ── System prompts ────────────────────────────────────────────────────────────
_CAREER_PROMPT = """You are AURA, an advanced AI Career and Learning Assistant.

Your areas of expertise:
• Career guidance & professional development
• Coding concepts, Data Structures & Algorithms (DSA)
• Technical & HR interview preparation
• Resume review and optimization
• Skill-development roadmaps (beginner → advanced)
• AI/ML concepts and industry trends
• Placement strategies for college students
• Project ideas and portfolio building

Response guidelines:
• Be concise, accurate, and actionable
• Use structured formatting (headers, bullet points) where it aids clarity
• Include working code examples for technical questions
• Be encouraging and realistic — never give vague platitudes
• Always respond in English unless the user writes in another language
"""

_STUDY_PROMPT = """You are AURA, a Smart Study Assistant.

Use the provided Document Context to answer questions accurately and precisely.
If the context is insufficient, supplement with your general knowledge — but say so.
Format answers clearly: bullet points, numbered steps, or prose depending on the question.
Be concise; avoid padding.
"""

# ── Main function ─────────────────────────────────────────────────────────────

def get_ai_response(prompt: str,
                    context: str = "",
                    mode: str = "career",
                    history: list | None = None) -> str:
    """
    Fetch a response from OpenRouter.

    Args:
        prompt  : User's question / input text.
        context : Optional document text (PDF Assistant).
        mode    : "career" | "study"
        history : Optional list of prior messages for multi-turn context.
                  Each item: {"role": "user"|"assistant", "content": str}

    Returns:
        Response string (may contain basic markdown).
    """
    system_prompt = _CAREER_PROMPT if mode == "career" else _STUDY_PROMPT

    # Build user content
    if context:
        user_content = (
            f"Document Context (excerpt):\n{context[:3500]}\n\n"
            f"Question:\n{prompt}"
        )
    else:
        user_content = prompt

    # Build message list
    messages: list[dict] = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history[-10:])          # keep last 10 turns for brevity
    messages.append({"role": "user", "content": user_content})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "https://aura-ai.streamlit.app",
        "X-Title":       "AURA AI",
    }

    payload = {
        "model":       MODEL,
        "messages":    messages,
        "temperature": 0.70,
        "max_tokens":  1200,
    }

    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=40)

        if resp.status_code == 200:
            data = resp.json()
            if "choices" in data and data["choices"]:
                return data["choices"][0]["message"]["content"].strip()
            if "error" in data:
                return f"⚠️ API Error: {data['error'].get('message', 'Unknown error')}"
            return "⚠️ Unexpected response format from the API."

        if resp.status_code == 401:
            return "⚠️ Invalid API key. Please check your OpenRouter key in `utils/ai_engine.py`."
        if resp.status_code == 429:
            return "⚠️ Rate limit hit. Please wait a moment and try again."
        return f"⚠️ API request failed (HTTP {resp.status_code}). Details: {resp.text[:200]}"

    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. The model may be busy — please try again."
    except requests.exceptions.ConnectionError:
        return "⚠️ Connection error. Please check your internet connection."
    except Exception as exc:
        return f"⚠️ Unexpected error: {exc}"
