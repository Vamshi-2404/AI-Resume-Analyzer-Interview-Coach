import streamlit as st
import plotly.graph_objects as go
import re
from resume_parser import extract_text_from_pdf
from ai_analysis import analyze_resume_for_job, evaluate_answer
from fpdf import FPDF

# -----------------------------
# PDF GENERATION
# -----------------------------
def generate_pdf(report_text):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AI Resume Analysis Report", ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", size=12)

    for line in report_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf_output = pdf.output(dest="S").encode("latin-1")

    return pdf_output


# -----------------------------
# STREAMLIT PAGE
# -----------------------------
st.set_page_config(page_title="AI Resume Coach", layout="wide")

st.title("🚀 AI Resume Analyzer & Interview Coach")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

job_description = st.text_area("Paste Job Description")

# -----------------------------
# RUN APP WHEN BOTH PROVIDED
# -----------------------------
if uploaded_file :

    resume_text = extract_text_from_pdf(uploaded_file)

    tab1, tab2, tab3 = st.tabs(
        ["📊 ATS Analysis", "🧠 Interview Questions", "🎤 Mock Interview"]
    )

    # =============================
    # TAB 1 — ATS ANALYSIS
    # =============================
    with tab1:

        

     if st.button("Analyze Resume", key="analyze_btn"):

        with st.spinner("Analyzing resume..."):

         if job_description.strip() != "":
                st.session_state.analysis_result = analyze_resume_for_job(
                    resume_text, job_description
                )
         else:
                st.session_state.analysis_result = analyze_resume_for_job(
                    resume_text,
                    "Analyze the resume and give general feedback without ATS scoring."
                )

    # -------------------------
    # SHOW RESULT IF AVAILABLE
    # -------------------------

    result = st.session_state.get("analysis_result", "")

    if result:

        st.subheader("ATS Analysis Result")

        st.write(result)
            
            # Extract ATS score safely
        result = st.session_state.analysis_result
        match = re.search(r'ATS Match Score:\s*(\d+)', result)

        if match:
                ats_score = int(match.group(1))
        else:
                ats_score = 0

        ats_score = min(max(ats_score, 0), 100)

            # ------------------------
            # ATS Gauge Meter
            # ------------------------
        fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=ats_score,
                    title={"text": "ATS Match Score"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "green"},
                        "steps": [
                            {"range": [0, 50], "color": "red"},
                            {"range": [50, 75], "color": "orange"},
                            {"range": [75, 100], "color": "lightgreen"},
                        ],
                    },
                )
            )

        st.plotly_chart(fig, width="stretch")

            # ------------------------
            # DOWNLOAD PDF REPORT
            # ------------------------
        pdf_file = generate_pdf(result)

        st.download_button(
                label="Download PDF Report",
                data=pdf_file,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf",
            )

    # =============================
    # TAB 2 — INTERVIEW QUESTIONS
    # =============================
    with tab2:

        result = st.session_state.get("analysis_result", "")

        if result:

            st.subheader("Expected Interview Questions")

            st.write(result)

        else:
            st.info("Run the ATS analysis first to generate questions.")

    # =============================
    # TAB 3 — MOCK INTERVIEW
    # =============================
    with tab3:

        st.subheader("AI Mock Interview")

        question = st.text_input("Enter Interview Question")

        answer = st.text_area("Your Answer")

        if st.button("Evaluate Answer"):

            feedback = evaluate_answer(question, answer)

            st.subheader("Interview Feedback")

            st.write(feedback)