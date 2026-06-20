from utils.ai_engine import *
from utils.ai_engine import get_ai_response
from utils.pdf_utils import extract_pdf_text
from utils.ocr_utils import extract_text_from_scanned_pdf
from utils.resume_utils import (
    analyze_resume,
    generate_interview_questions,
    skill_gap_analysis,
    ats_resume_score,
)
# ---------------- UI CONFIG ---------------- #
st.set_page_config(
    page_title="AI Study & Career Assistant",
    page_icon="🤖",
    layout="wide"
)

st.sidebar.title("🤖 AI Study & Career Assistant")

st.sidebar.markdown("---")

st.sidebar.subheader("📚 PDF Tools")

st.sidebar.subheader("📄 Resume Tools")

st.sidebar.markdown("---")

st.sidebar.info(
    """
    Features:
    • Chatbot
    • PDF Q&A
    • OCR
    • Resume Analyzer
    • Interview Questions
    • Skill Gap Analysis
    • ATS Score
    """
)
st.title("🤖 AI Study & Career Assistant")

st.markdown(
    "Your personal AI mentor for learning, resumes, interviews, and career growth."
)

# ---------------- SESSION MEMORY ---------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
st.sidebar.title("📄 Upload Study Material")

pdf_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

pdf_text = ""

if pdf_file:

    pdf_text = extract_pdf_text(pdf_file)

    if len(pdf_text.strip()) < 100:

        pdf_file.seek(0)

        pdf_text = extract_text_from_scanned_pdf(pdf_file)

        st.sidebar.info(
            "📸 Scanned PDF detected. OCR used."
        )

    st.sidebar.success(
        f"Loaded {len(pdf_text)} characters"
    )
    st.write("PDF Characters:", len(pdf_text))
st.sidebar.markdown("---")
st.sidebar.subheader("📄 Resume Analyzer")

resume_file = st.sidebar.file_uploader(
    "Upload Resume",
    type=["pdf"],
    key="resume_upload"
) 
resume_text = extract_pdf_text(resume_file)
st.write("Resume Characters:", len(resume_text))
st.text_area(
    "Resume Preview",
    resume_text[:1000],
    height=200
)
if resume_file:

    if st.sidebar.button("🚀 Analyze Resume"):

        with st.spinner("Analyzing Resume..."):

            report = analyze_resume(
                resume_text
            )

        st.subheader("📊 Resume Analysis")

        st.write(report)
if resume_file:

    resume_text = extract_pdf_text(resume_file)

    if len(resume_text.strip()) < 100:

        resume_file.seek(0)

        resume_text = extract_text_from_scanned_pdf(
            resume_file
        )

    st.sidebar.success(
        "Resume Loaded Successfully ✅"
    ) 
target_role = st.sidebar.text_input(
    "🎯 Target Role",
    placeholder="Example: Data Scientist"
)   
if st.sidebar.button(
    "📊 Skill Gap Analysis",
    key="skill_gap_btn"
):

    if target_role:

        with st.spinner(
            "Analyzing Skill Gap..."
        ):

            report = skill_gap_analysis(
                resume_text,
                target_role
            )

        st.subheader(
            f"📊 Skill Gap Analysis: {target_role}"
        )

        st.markdown(report)

    else:

        st.warning(
            "Please enter a target role."
        )
if st.sidebar.button(
    "📈 ATS Resume Score",
    key="ats_score_btn"
):

    with st.spinner("Calculating ATS Score..."):

        ats_report = ats_resume_score(resume_text)

    import re

    ats = re.search(
        r"ATS Score:\s*(\d+)",
        ats_report
    )

    tech = re.search(
        r"Technical Skills:\s*(\d+)",
        ats_report
    )

    projects = re.search(
        r"Projects:\s*(\d+)",
        ats_report
    )

    comm = re.search(
        r"Communication:\s*(\d+)",
        ats_report
    )

    format_score = re.search(
        r"Resume Format:\s*(\d+)",
        ats_report
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ATS Score", ats.group(1)+"/100")

    with col2:
        st.metric("Technical Skills", tech.group(1)+"/10")

    with col3:
        st.metric("Projects", projects.group(1)+"/10")

    col4, col5 = st.columns(2)

    with col4:
        st.metric("Communication", comm.group(1)+"/10")

    with col5:
        st.metric("Resume Format", format_score.group(1)+"/10")

    st.markdown(ats_report)
if st.sidebar.button("🎤 Generate Interview Questions"):

    with st.spinner("Generating Questions..."):

        questions = generate_interview_questions(
            resume_text
        )

    st.subheader("🎤 Interview Questions")

    st.markdown(questions)

# ---------------- USER INPUT ---------------- #
prompt = st.chat_input("Ask me anything about coding, DSA, AI, or careers...")

if prompt:

    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # AI response
    try:
        with st.spinner("Thinking... 🤔"):
           reply = get_ai_response(prompt, pdf_text)

    except Exception as e:
        reply = f"⚠️ Error: {e}"

    # Save + display assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

# ---------------- CLEAR CHAT ---------------- #
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()