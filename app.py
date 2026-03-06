import streamlit as st
from resume_parser import extract_text_from_pdf
from ai_analysis import analyze_resume, generate_questions, evaluate_answer

st.set_page_config(page_title="AI Resume Coach", layout="wide")

st.title("AI Resume Analyzer & Interview Coach")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=300)

    if st.button("Analyze Resume"):
        analysis = analyze_resume(resume_text)
        st.subheader("Resume Feedback")
        st.write(analysis)

    if st.button("Generate Interview Questions"):
        questions = generate_questions(resume_text)
        st.subheader("Interview Questions")
        st.write(questions)

    st.subheader("Practice Interview")

    question = st.text_input("Enter a question")
    answer = st.text_area("Your Answer")

    if st.button("Evaluate Answer"):
        feedback = evaluate_answer(question, answer)
        st.write(feedback)
        