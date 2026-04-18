import streamlit as st
import plotly.graph_objects as go
import re
from resume_parser import extract_text_from_pdf
from ai_analysis import analyze_resume_for_job, evaluate_answer
from fpdf import FPDF

# Custom CSS for responsive design
CUSTOM_CSS = """
<style>
    /* Mobile-first approach */
    * {
        box-sizing: border-box;
    }
    
    /* Overall page styling */
    .main {
        padding: 1rem;
    }
    
    /* Responsive container */
    @media (max-width: 640px) {
        .main {
            padding: 0.5rem;
        }
        .stTitle h1 {
            font-size: 1.5rem !important;
        }
    }
    
    @media (min-width: 641px) and (max-width: 1024px) {
        .main {
            padding: 1rem;
        }
        .stTitle h1 {
            font-size: 2rem !important;
        }
    }
    
    @media (min-width: 1025px) {
        .main {
            padding: 2rem;
        }
        .stTitle h1 {
            font-size: 2.5rem !important;
        }
    }
    
    /* Responsive buttons */
    .stButton > button {
        width: 100%;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
    }
    
    @media (max-width: 640px) {
        .stButton > button {
            padding: 0.6rem 1rem;
            font-size: 0.9rem;
        }
    }
    
    /* Responsive text areas and inputs */
    .stTextInput input, .stTextArea textarea {
        width: 100% !important;
        padding: 0.75rem;
        font-size: 1rem;
        border-radius: 0.5rem;
    }
    
    @media (max-width: 640px) {
        .stTextInput input, .stTextArea textarea {
            padding: 0.6rem;
            font-size: 0.95rem;
        }
    }
    
    /* Responsive tabs */
    .stTabs {
        width: 100%;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    @media (max-width: 640px) {
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.25rem;
        }
        .stTabs [role="tab"] {
            font-size: 0.85rem;
            padding: 0.5rem 0.75rem;
        }
    }
    
    /* Responsive metrics/cards */
    .metric-card {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        width: 100%;
    }
    
    @media (max-width: 640px) {
        .metric-card {
            padding: 0.75rem;
            margin: 0.35rem 0;
        }
    }
    
    /* Responsive file uploader */
    .stFileUploader {
        width: 100%;
    }
    
    /* Responsive charts */
    .plotly-graph-div {
        width: 100% !important;
        height: auto !important;
    }
    
    /* Responsive text content */
    .stMarkdown, .stText {
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    @media (max-width: 640px) {
        .stMarkdown, .stText {
            font-size: 0.95rem;
            line-height: 1.4;
        }
    }
    
    /* Download button responsive */
    .stDownloadButton > button {
        width: 100%;
    }
    
    /* Info/warning/success messages */
    .stAlert {
        width: 100%;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    @media (max-width: 640px) {
        .stAlert {
            padding: 0.75rem;
            margin: 0.75rem 0;
        }
    }
    
    /* Spinner responsive */
    .stSpinner {
        text-align: center;
    }
    
    /* Two-column layout for larger screens */
    @media (min-width: 1025px) {
        .content-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }
    }
    
    @media (max-width: 1024px) {
        .content-row {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }
</style>
"""

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =============================
# PDF GENERATION
# =============================
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


# =============================
# STREAMLIT PAGE CONFIGURATION
# =============================
st.set_page_config(
    page_title="AI Resume Coach",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Vamshi-2404/AI-Resume-Analyzer-Interview-Coach',
        'Report a bug': "https://github.com/Vamshi-2404/AI-Resume-Analyzer-Interview-Coach/issues",
        'About': "AI Resume Analyzer & Interview Coach"
    }
)

# Initialize session state
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = ""

# Title
st.title("🚀 AI Resume Analyzer & Interview Coach")
st.markdown("---")

# Create responsive layout using columns
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")

with col2:
    st.subheader("💼 Job Description")
    job_description = st.text_area(
        "Paste Job Description",
        placeholder="Paste the job description here for better analysis...",
        height=150,
        label_visibility="collapsed"
    )

st.markdown("---")

# =============================
# RUN APP WHEN RESUME PROVIDED
# =============================
if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    
    # Create tabs with responsive design
    tab1, tab2, tab3 = st.tabs(
        ["📊 ATS Analysis", "🧠 Interview Questions", "🎤 Mock Interview"]
    )
    
    # =============================
    # TAB 1 — ATS ANALYSIS
    # =============================
    with tab1:
        st.subheader("Resume Analysis")
        
        if st.button("🔍 Analyze Resume", key="analyze_btn", use_container_width=True):
            with st.spinner("🔄 Analyzing your resume..."):
                if job_description.strip() != "":
                    st.session_state.analysis_result = analyze_resume_for_job(
                        resume_text, job_description
                    )
                else:
                    st.session_state.analysis_result = analyze_resume_for_job(
                        resume_text,
                        "Analyze the resume and give general feedback without ATS scoring."
                    )
        
        # Show result if available
        result = st.session_state.get("analysis_result", "")
        
        if result:
            st.subheader("📋 ATS Analysis Result")
            
            # Display main result
            st.write(result)
            
            # Extract ATS score safely
            match = re.search(r'ATS Match Score:\s*(\d+)', result)
            
            if match:
                ats_score = int(match.group(1))
            else:
                ats_score = 0
            
            ats_score = min(max(ats_score, 0), 100)
            
            # ATS Gauge Meter (responsive)
            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=ats_score,
                    title={"text": "ATS Match Score"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "green"},
                        "steps": [
                            {"range": [0, 50], "color": "rgba(255, 0, 0, 0.5)"},
                            {"range": [50, 75], "color": "rgba(255, 165, 0, 0.5)"},
                            {"range": [75, 100], "color": "rgba(144, 238, 144, 0.5)"},
                        ],
                    },
                )
            )
            
            fig.update_layout(
                margin=dict(l=20, r=20, t=40, b=20),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Download PDF Report
            pdf_file = generate_pdf(result)
            
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_file,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.info("👆 Click 'Analyze Resume' to get started!", icon="ℹ️")
    
    # =============================
    # TAB 2 — INTERVIEW QUESTIONS
    # =============================
    with tab2:
        st.subheader("📝 Expected Interview Questions")
        
        result = st.session_state.get("analysis_result", "")
        
        if result:
            st.write(result)
        else:
            st.info("Run the ATS analysis first to generate interview questions.", icon="ℹ️")
    
    # =============================
    # TAB 3 — MOCK INTERVIEW
    # =============================
    with tab3:
        st.subheader("🎤 AI Mock Interview")
        
        # Create responsive columns for interview input
        question = st.text_input(
            "Enter Interview Question",
            placeholder="e.g., Tell me about yourself...",
            label_visibility="collapsed"
        )
        
        answer = st.text_area(
            "Your Answer",
            placeholder="Type your answer here...",
            height=200,
            label_visibility="collapsed"
        )
        
        if st.button("✅ Evaluate Answer", key="evaluate_btn", use_container_width=True):
            if question and answer:
                feedback = evaluate_answer(question, answer)
                
                st.subheader("💬 Interview Feedback")
                st.write(feedback)
            else:
                st.warning("Please enter both a question and an answer!", icon="⚠️")

else:
    st.info("👆 Please upload a resume (PDF) to get started!", icon="ℹ️")