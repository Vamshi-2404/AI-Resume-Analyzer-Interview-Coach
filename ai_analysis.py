import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_resume(resume_text):

    prompt = f"""
    Analyze this resume and provide:

    1. Strengths
    2. Weaknesses
    3. Missing skills for Software Engineer roles
    4. Suggestions to improve

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def generate_questions(resume_text):

    prompt = f"""
    Based on this resume generate:

    - 5 technical interview questions
    - 3 behavioral questions

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def evaluate_answer(question, answer):

    prompt = f"""
    Evaluate this interview answer.

    Question:
    {question}

    Answer:
    {answer}

    Provide:
    - Score out of 10
    - Feedback
    - Improved answer
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content