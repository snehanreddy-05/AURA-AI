import streamlit as st
import requests


# ---------------- CONFIG ---------------- #
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# ---------------- AI FUNCTION ---------------- #
def get_ai_response(prompt, context=""):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "messages": [
            {
                "role": "system",
                "content": """
You are a Study Assistant.

Use the provided notes (if any) to answer questions.

If notes are not enough, use general knowledge.
"""
            },
            {
                "role": "user",
                "content": f"""
Context (PDF Notes):
{context}

Question:
{prompt}
"""
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return response.text
    result = response.json()

    if "choices" in result:
       return result["choices"][0]["message"]["content"]

    elif "error" in result:
       return f"Error: {result['error']}"

    else:
       return str(result)