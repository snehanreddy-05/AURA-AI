"""
utils/resume_utils.py
AURA AI — Resume analysis functions powered by ai_engine.
"""

from utils.ai_engine import get_ai_response


def analyze_resume(resume_text: str) -> str:
    prompt = f"""Perform a comprehensive analysis of the resume below.

Structure your response exactly as follows:

## 🔧 Skills Identified
List all technical and soft skills detected.

## ✅ Key Strengths
What the candidate excels at (3–5 specific points).

## ⚠️ Areas for Improvement
Specific weaknesses or gaps with brief explanations.

## 📚 Missing Skills
Important skills absent from the profile that employers expect.

## 💡 Project Suggestions
2–3 targeted project ideas that would strengthen the candidate's profile.

## 🗺️ 6-Month Career Roadmap
Month-by-month milestones with concrete actions.

## 🎯 Interview Readiness Score
Score /10 with a one-paragraph justification.

Resume:
{resume_text}"""
    return get_ai_response(prompt)


def generate_interview_questions(resume_text: str) -> str:
    prompt = f"""You are a senior interviewer at a top product-based company.

Generate a tailored interview question set for this candidate.

## 💻 Technical Questions (6–8 questions)
Based on their exact tech stack and projects.

## 🚀 Project Deep-Dive Questions (4–5 questions)
Probe specific design decisions in their projects.

## 🧑‍💼 Behavioral / HR Questions (4–5 questions)
STAR-format scenarios testing teamwork, leadership, conflict resolution.

## 🔄 Follow-Up & Curveball Questions (3–4 questions)
Harder follow-ups that reveal depth of understanding.

## 📖 Must-Revise Topics Before Interview
Top 5–7 topics the candidate should brush up on, in priority order.

Resume:
{resume_text}"""
    return get_ai_response(prompt)


def skill_gap_analysis(resume_text: str, target_role: str) -> str:
    prompt = f"""You are a senior career mentor and hiring manager.

Analyse this candidate's resume against the target role and produce a structured report.

## 🛠️ Relevant Current Skills
Skills already possessed that are valuable for {target_role}.

## ❌ Critical Missing Skills
Skills that would disqualify the candidate today, ranked by importance.

## 📚 Recommended Learning Resources
For each missing skill: course name, platform, estimated hours.

## 🔨 Project Ideas to Fill the Gap
2–3 portfolio projects that directly demonstrate the missing skills.

## 🗺️ 12-Week Learning Roadmap
Week-by-week plan: topic → resource → deliverable.

## 📊 Readiness Score for {target_role}
Score /10 with gap summary.

Target Role: {target_role}

Resume:
{resume_text}"""
    return get_ai_response(prompt)


def ats_resume_score(resume_text: str) -> str:
    prompt = f"""You are an enterprise ATS (Applicant Tracking System) evaluator.

Analyse the resume and return a structured ATS report in this exact format:

## 📊 ATS Compatibility Report

**Overall Score: XX / 100**

| Category               | Score  | Comments                        |
|------------------------|--------|---------------------------------|
| Keyword Density        | XX/20  | ...                             |
| Technical Skills Match | XX/20  | ...                             |
| Work Experience        | XX/20  | ...                             |
| Education & Certs      | XX/15  | ...                             |
| Projects & Impact      | XX/15  | ...                             |
| Format & Readability   | XX/10  | ...                             |

## ✅ ATS Strengths
- What the resume does well for automated parsing

## ⚠️ ATS Failures / Risks
- Elements that hurt ATS parsing or ranking

## 🚀 Quick-Win Improvements (top 5)
Specific, actionable fixes ranked by impact.

Resume:
{resume_text}"""
    return get_ai_response(prompt)
