from utils.ai_engine import get_ai_response
def analyze_resume(resume_text):
    prompt = f"""
Analyze the following resume.

Provide:

1. Skills Identified
2. Strengths
3. Weaknesses
4. Missing Skills
5. Project Suggestions
6. Career Roadmap
7. Interview Readiness Score (out of 10)

Resume:

{resume_text}
"""

    return get_ai_response(prompt)
def generate_interview_questions(resume_text):
    prompt = f"""
You are an experienced interviewer from a product company.

Generate interview questions specifically tailored to the candidate's projects, skills, and experience.

Provide:

## Technical Questions
## Project Questions
## HR Questions
## Follow-up Questions
## Ideal Topics To Revise Before Interview

Resume:

{resume_text}
"""
    return get_ai_response(prompt) 
def skill_gap_analysis(resume_text, target_role):

    prompt = f"""
You are a career mentor.

Analyze the resume against the target role.

Provide:

## Current Skills

## Missing Skills

## Recommended Courses

## Recommended Projects

## Learning Roadmap (3 Months)

Target Role:
{target_role}

Resume:
{resume_text}
"""

    return get_ai_response(prompt)
def ats_resume_score(resume_text):

    prompt = f"""
You are an ATS (Applicant Tracking System).

Analyze this resume and return ONLY in this format:

ATS Score: XX

Technical Skills: X

Projects: X

Communication: X

Resume Format: X

Resume:

{resume_text}
"""

    return get_ai_response(prompt)