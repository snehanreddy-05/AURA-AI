# ✦ AURA AI — Intelligent Career Assistant

> *Where Ambition Meets Intelligence*

AURA AI is a beautifully designed, AI-powered career and learning platform built with Streamlit. It combines a cinematic deep-space visual identity with real, practical AI tools — chat mentor, resume analysis, and a PDF study assistant — all running on a free OpenRouter AI model.

---

## 🌌 What Is AURA AI?

AURA AI is not just another Streamlit dashboard. It is designed to feel like a futuristic AI operating system — dark space background, animated nebula clouds, cross-shaped twinkling stars, gold accents, glassmorphism cards, and smooth transitions. Underneath that experience live four powerful tools built for students and early-career professionals.

---

## 🚀 Features

### 💬 Career Chat
A full multi-turn AI chat interface. Ask anything related to:
- Career guidance and professional development
- Coding, Data Structures & Algorithms (DSA)
- Technical and HR interview preparation
- AI/ML concepts and industry trends
- Placement strategy for college students
- Project ideas and portfolio building
- Skill-development roadmaps

Keeps full conversation history within the session. Shows a typing indicator while AURA thinks. Each message is timestamped with styled left/right chat bubbles.

### 📄 Resume Studio
Upload a PDF resume or paste text, then run any of four analyses:

| Tab | What it does |
|-----|-------------|
| 📊 ATS Score | Scores your resume against ATS criteria with a category breakdown and quick-fix suggestions |
| 🔍 Resume Review | Full critique — skills, strengths, weaknesses, project suggestions, 6-month roadmap |
| 🎯 Skill Gap | Compare your profile against a target role, get a 12-week structured learning plan |
| 🎤 Interview Prep | Generate a bespoke question set — technical, project deep-dives, behavioural, must-revise topics |

### 📚 PDF Assistant
Upload any PDF (notes, research papers, textbooks) and chat with it:
- Auto-generates a 4–5 sentence summary + 5 key topics on upload
- Full persistent multi-turn Q&A grounded in the document
- Falls back to OCR for scanned/image-based PDFs (requires Tesseract)

### 🎨 Visual Design
- Deep space background with animated nebula (blue + purple)
- 300 twinkling background dot-stars
- 38 cross/diffraction-spike medium stars with glow halos and pulse animation
- Glassmorphism cards, gold borders, Orbitron display font
- Fully dark-themed — inputs, file uploaders, chat bar, everything

---

## 📁 Project Structure

```
aura_ai/
├── app.py                          ← Home page / landing screen
│
├── pages/
│   ├── 1_💬_Career_Chat.py        ← Chat mentor page
│   ├── 2_📄_Resume_Studio.py      ← Resume analysis (4 tabs)
│   ├── 3_📚_PDF_Assistant.py      ← PDF upload + Q&A chat
│   └── 4_ℹ️_About.py             ← About AURA page
│
├── utils/
│   ├── __init__.py
│   ├── ai_engine.py               ← OpenRouter API calls + system prompts
│   ├── pdf_utils.py               ← PDF text extraction (pdfplumber + PyPDF2 fallback)
│   ├── resume_utils.py            ← Resume analysis functions (ATS, review, gap, interview)
│   ├── ocr_utils.py               ← OCR for scanned PDFs (Tesseract + pdf2image)
│   └── theme.py                   ← All UI: apply_theme(), sidebar, chat bubbles, starfield
│
├── assets/
│   └── css/
│       └── aura_theme.css         ← Full CSS — variables, cards, chat, inputs, animations
│
└── requirements.txt
```

---

## 📦 Requirements

### Python Packages

Install everything with:

```bash
pip install -r requirements.txt
```

| Package | Version | Why it is needed |
|---------|---------|-----------------|
| `streamlit` | ≥ 1.31.0 | The entire web framework — pages, widgets, state, layout |
| `requests` | ≥ 2.31.0 | Makes HTTP calls to the OpenRouter AI API |
| `pdfplumber` | ≥ 0.10.0 | Primary PDF text extractor — handles complex layouts, tables, columns |
| `PyPDF2` | ≥ 3.0.0 | Fallback PDF reader if pdfplumber cannot extract text |
| `pytesseract` | ≥ 0.3.10 | Python wrapper for Tesseract OCR — reads scanned/image PDFs |
| `pdf2image` | ≥ 1.16.3 | Converts PDF pages into images so Tesseract can process them |
| `Pillow` | ≥ 10.0.0 | Image processing library required by pdf2image and pytesseract |

### System Dependency — Tesseract OCR

`pytesseract` is just a Python wrapper. You also need the **Tesseract binary** installed on your system:

**Windows**
```
Download and install from:
https://github.com/UB-Mannheim/tesseract/wiki
Default path: C:\Program Files\Tesseract-OCR\tesseract.exe
```

**macOS**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian)**
```bash
sudo apt install tesseract-ocr
```

> Tesseract is only needed for scanned PDFs. Text-based PDFs work without it.

### Poppler (required by pdf2image)

**Windows** — Download from https://github.com/oschwartz10612/poppler-windows/releases, extract, and add the `bin/` folder to your PATH.

**macOS**
```bash
brew install poppler
```

**Linux**
```bash
sudo apt install poppler-utils
```

---

## ⚙️ Configuration

### API Key

AURA AI uses **OpenRouter** (free tier) to call the AI model. The key is in `utils/ai_engine.py`:

```python
OPENROUTER_API_KEY = "sk-or-v1-..."   # ← your key here
MODEL              = "nvidia/nemotron-3-ultra-550b-a55b:free"
```

To get a free key:
1. Go to https://openrouter.ai
2. Sign up → Dashboard → API Keys → Create Key
3. Replace the value in `ai_engine.py`

You can also swap `MODEL` to any other model available on OpenRouter.

---

## ▶️ Running the App

```bash
# From inside the aura_ai/ directory
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## 🛠️ How Each Utility Works

### `ai_engine.py`
Central AI brain. One function — `get_ai_response()` — handles two modes:
- `"career"` — uses the Career mentor system prompt
- `"study"` — uses the Study assistant system prompt, grounded in document context

Keeps the last 10 conversation turns for multi-turn memory. Handles all error states (timeout, rate limit, invalid key) with clean user-facing messages.

### `pdf_utils.py`
PDF text extraction with a two-layer fallback:
1. **pdfplumber** — tries first, handles columns, tables, complex layouts
2. **PyPDF2** — fallback if pdfplumber returns empty
3. **OCR via `ocr_utils.py`** — last resort for scanned image-based PDFs

### `resume_utils.py`
Four AI-powered functions, each sends a structured prompt to `ai_engine.py`:
- `ats_resume_score()` — ATS compatibility check
- `analyze_resume()` — full 6-section critique
- `skill_gap_analysis()` — gap vs target role + 12-week roadmap
- `generate_interview_questions()` — personalised question bank

### `theme.py`
Everything visual lives here:
- `apply_theme()` — loads `aura_theme.css` + injects the animated starfield
- `sidebar_brand()` — AURA logo block in sidebar
- `sidebar_nav()` — navigation with active-page highlight, uses absolute paths to avoid emoji filename issues on Windows
- `render_message()` — styled chat bubbles (user right, AURA left with avatar)
- `page_title()`, `gold_divider()`, `aura_card()` — reusable UI components

---

## 🌐 Architecture Flow

```
User opens browser
        ↓
   app.py (Home)
        ↓
   apply_theme()  ──→  aura_theme.css + animated starfield
        ↓
   sidebar_nav()  ──→  switch_page() with absolute OS paths
        ↓
   Page selected  ──→  Career Chat / Resume Studio / PDF Assistant
        ↓
   User input
        ↓
   ai_engine.get_ai_response()
        ↓
   OpenRouter API  ──→  nvidia/nemotron-3-ultra-550b-a55b (free)
        ↓
   Response rendered in styled chat bubble / result card
```

---

## 🔑 Known Notes

- **Navigation paths** — `sidebar_nav()` uses `os.path.abspath()` to build page paths. This fixes emoji-in-filename issues on Windows with Python 3.12+ and Streamlit 1.36+.
- **Chat history** — stored in `st.session_state`, resets when the browser tab is closed or refreshed.
- **PDF size** — text is capped at 3,500 characters per API call to stay within token limits. For long documents, answers are based on the first ~3,500 characters of extracted text.
- **Free model limits** — the OpenRouter free tier has rate limits. If you hit them, wait a few seconds and retry.

---

## ✦ Built with AURA Design Philosophy

> Classic elegance × Modern AI. Think Apple × OpenAI × Space Observatory.

Not cyberpunk. Not neon overload. Premium, cinematic, intelligent.


## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/snehanreddy-05/AURA_AI.git
````

Move into the project directory

```bash
cd AURA_AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 🔮 Future Enhancements

* User Authentication
* Conversation History
* AI Memory
* Voice Assistant
* Resume Templates
* Mock Interview Simulator
* Job Recommendation Engine
* Streamlit Cloud Deployment
* Mobile Optimization

---

## 👨‍💻 Author

**Snehan Reddy**

Computer Science Engineering Student

Passionate about Artificial Intelligence, Machine Learning, and Building Real-World AI Applications.

GitHub:
https://github.com/snehanreddy-05

---

## 📄 License

This project is licensed under the MIT License.

```
```
