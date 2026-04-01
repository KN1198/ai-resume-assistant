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

    # SAFE PDF READING
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            resume_text += page.extract_text() or ""

        if not resume_text.strip():
            st.warning("⚠️ This PDF has no readable text. Use a proper exported PDF.")
            st.stop()

    except PdfReadError:
        st.error("❌ Cannot read this PDF. Upload a proper resume.")
        st.stop()

    # =========================
    # PREVIEW
    # =========================
    st.markdown("## 📌 Resume Preview")
    st.text_area("Resume Content", resume_text, height=300)

    # =========================
    # JOB DESCRIPTION
    # =========================
    st.markdown("## 💼 Job Description")
    job_desc = st.text_area("Paste Job Description Here")

    if st.button("🔍 Analyze & Improve Resume"):

        text = resume_text.lower()
        job_text = job_desc.lower()

        resume_words = set(text.split())
        job_words = set(job_text.split())

        match_score = int(len(resume_words & job_words) / len(job_words) * 100) if job_words else 0

        st.subheader("📊 Match Score")
        st.success(f"{match_score}% match with job")

        missing_keywords = list(job_words - resume_words)[:10]

        st.subheader("❌ Missing Keywords")
        st.write(", ".join(missing_keywords) if missing_keywords else "None")

        # =========================
        # SECTION DETECTION
        # =========================
        sections = {
            "summary": "",
            "experience": "",
            "education": "",
            "skills": ""
        }

        current_section = None
        for line in resume_text.split("\n"):
            lower = line.lower()

            if "summary" in lower or "objective" in lower:
                current_section = "summary"
            elif "experience" in lower:
                current_section = "experience"
            elif "education" in lower:
                current_section = "education"
            elif "skills" in lower:
                current_section = "skills"

            if current_section:
                sections[current_section] += line + "\n"

        # =========================
        # IMPROVE CONTENT
        # =========================
        improved_summary = f"""
Results-driven professional with strong expertise in data analysis, problem-solving, and business insights.
Skilled in Python, SQL, and tools relevant to this role.
"""

        improved_experience = """
- Developed data-driven solutions to improve business performance  
- Analyzed datasets using Python and SQL  
- Built dashboards and reports for insights  
- Improved efficiency through automation  
"""

        improved_skills = "\n".join([f"- {kw}" for kw in missing_keywords]) if missing_keywords else sections["skills"]

        # =========================
        # FINAL RESUME
        # =========================
        improved_resume = f"""
===============================
        UPDATED RESUME
===============================

🔹 SUMMARY
{improved_summary if sections["summary"] else "Add professional summary"}

🔹 EXPERIENCE
{improved_experience if sections["experience"] else "Add experience section"}

🔹 SKILLS
{improved_skills if sections["skills"] else "Add skills"}

🔹 EDUCATION
{sections["education"] if sections["education"] else "Add education"}

===============================
"""

        st.markdown("## 📄 Improved Resume")
        st.text_area("Updated Resume", improved_resume, height=300)

        # =========================
        # DOWNLOAD
        # =========================
        st.markdown("## 📥 Download Resume")

        st.download_button(
            "Download TXT",
            data=improved_resume,
            file_name="updated_resume.txt",
            mime="text/plain"
        )

        def create_docx(text):
            doc = Document()
            for line in text.split("\n"):
                doc.add_paragraph(line)

            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            return buffer

        st.download_button(
            "Download DOCX",
            data=create_docx(improved_resume),
            file_name="updated_resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("Built by Krunal 🚀")
