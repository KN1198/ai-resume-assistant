import streamlit as st
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from docx import Document
from io import BytesIO

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Resume Assistant", layout="centered")

# =========================
# STYLING
# =========================
st.markdown("""
<style>
    .stButton>button {
        background-color: #6366F1;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("# 🚀 AI Resume Analyzer")
st.markdown("### 🎯 Optimize your resume for any job")
st.markdown("---")

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

if uploaded_file:

    resume_text = ""

    # =========================
    # SAFE PDF READING
    # =========================
    try:
        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            resume_text += page.extract_text() or ""

        if not resume_text.strip():
            st.warning("⚠️ This PDF seems to be scanned or has no readable text.")
            st.info("💡 Tip: Export your resume as a proper PDF from Word or Google Docs.")

    except PdfReadError:
        st.error("❌ Unable to read this PDF. Please upload a valid text-based resume.")
        st.stop()

    # =========================
    # RESUME PREVIEW
    # =========================
    st.markdown("## 📌 Resume Preview")
    st.text_area("Full Resume", resume_text, height=300)

    # =========================
    # JOB DESCRIPTION
    # =========================
    st.markdown("## 💼 Job Description")
    job_desc = st.text_area("Paste Job Description Here")

    # =========================
    # ANALYSIS
    # =========================
    if st.button("🔍 Analyze Resume for this Job"):

        text = resume_text.lower()
        job_text = job_desc.lower()

        resume_words = set(text.split())
        job_words = set(job_text.split())

        # MATCH SCORE
        match_words = resume_words.intersection(job_words)
        match_score = int(len(match_words) / len(job_words) * 100) if job_words else 0

        st.subheader("📊 Job Match Score")
        st.success(f"{match_score}% match with job description")

        # MISSING KEYWORDS
        missing_keywords = job_words - resume_words

        st.subheader("❌ Missing Keywords")
        if missing_keywords:
            st.write(", ".join(list(missing_keywords)[:20]))
        else:
            st.success("No major keywords missing!")

        # =========================
        # IMPROVEMENT SUGGESTIONS
        # =========================
        st.subheader("💡 Resume Improvements for This Job")

        suggestions = []

        if match_score < 50:
            suggestions.append("⚠️ Resume is not aligned with this job. Major updates needed.")

        if match_score < 70:
            suggestions.append("⚠️ Add more relevant skills and experience from the job description.")

        if missing_keywords:
            suggestions.append(f"👉 Add keywords: {', '.join(list(missing_keywords)[:10])}")

        if "experience" not in text:
            suggestions.append("👉 Add relevant work experience.")

        if "skills" not in text:
            suggestions.append("👉 Add a skills section tailored to this job.")

        for s in suggestions:
            st.write(s)

        # =========================
        # REWRITE EXAMPLES
        # =========================
        st.subheader("✍️ Resume Rewrite Examples")

        st.write("❌ Worked on data analysis")
        st.write("✅ Analyzed business data using Python and SQL to improve decision-making")

        st.write("❌ Responsible for dashboard")
        st.write("✅ Built interactive dashboards using Power BI to track KPIs")

        # =========================
        # IMPROVED RESUME GENERATION
        # =========================
        improved_resume = f"""
PROFESSIONAL SUMMARY:
Data-driven professional with expertise in Python, SQL, and analytics.

SKILLS:
Python, SQL, Data Analysis, Dashboarding

EXPERIENCE:
- Improved processes using data-driven insights
- Built dashboards and reports for decision-making

TAILORED KEYWORDS:
{', '.join(list(missing_keywords)[:10])}
"""

        st.markdown("## 📄 Improved Resume")
        st.text_area("Generated Resume", improved_resume, height=300)

        # =========================
        # DOWNLOAD OPTIONS
        # =========================
        st.markdown("## 📥 Download Resume")

        # TXT
        st.download_button(
            label="Download as TXT",
            data=improved_resume,
            file_name="improved_resume.txt",
            mime="text/plain"
        )

        # DOCX FUNCTION
        def create_docx(text):
            doc = Document()
            for line in text.split("\n"):
                doc.add_paragraph(line)

            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            return buffer

        docx_file = create_docx(improved_resume)

        st.download_button(
            label="Download as Word (.docx)",
            data=docx_file,
            file_name="improved_resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("## ⚙️ How it works")
st.markdown("""
1. Upload your resume  
2. Paste job description  
3. Get match score  
4. Improve and download your resume 🚀
""")

st.markdown("⭐ Built by Krunal | AI Resume Assistant")
