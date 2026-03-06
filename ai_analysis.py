import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"


# ---------------------------------------------------
# ATS Resume Analysis + Interview Question Generator
# ---------------------------------------------------

def analyze_resume_for_job(resume_text, job_description):

    prompt = f"""
    You are an Applicant Tracking System (ATS) and senior technical recruiter.

    Analyze the resume against the job description.

    Provide the following:

    1. ATS Match Score (0-100%)
    2. Matching Skills between resume and job description
    3. Missing Skills required for the role
    4. Suggestions to improve the resume for this job

    Then generate:

    5. 8 Technical interview questions for this role
    6. 3 Behavioral interview questions
    7. 2 Python coding questions relevant to the job

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ---------------------------------------------------
# Generate Additional Interview Questions
# ---------------------------------------------------

def generate_questions(job_description):

    prompt = f"""
    Based on the following job description generate:

    - 5 technical interview questions
    - 3 behavioral interview questions
    - 2 coding questions related to Python

    Job Description:
    {job_description}
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ---------------------------------------------------
# Evaluate Interview Answer
# ---------------------------------------------------

def evaluate_answer(question, answer):

    prompt = f"""
    Evaluate the interview answer for a Python developer role.

    Question:
    {question}

    Candidate Answer:
    {answer}

    Provide:

    1. Score out of 10
    2. Feedback on the answer
    3. What the ideal answer should include
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content