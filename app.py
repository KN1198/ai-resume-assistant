import streamlit as st
from pypdf import PdfReader

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
# UPLOAD RESUME
# =========================
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

if uploaded_file:

    reader = PdfReader(uploaded_file)
    resume_text = ""

    for page in reader.pages:
        resume_text += page.extract_text() or ""

    # =========================
    # RESUME PREVIEW
    # =========================
    st.markdown("## 📌 Resume Preview")
    st.text_area("Full Resume", resume_text, height=300)

    # =========================
    # JOB DESCRIPTION INPUT
    # =========================
    st.markdown("## 💼 Job Description")
    job_desc = st.text_area("Paste Job Description Here")

    # =========================
    # ANALYSIS BUTTON
    # =========================
    if st.button("🔍 Analyze Resume for this Job"):

        text = resume_text.lower()
        job_text = job_desc.lower()

        resume_words = set(text.split())
        job_words = set(job_text.split())

        # =========================
        # MATCH SCORE
        # =========================
        match_words = resume_words.intersection(job_words)
        match_score = int(len(match_words) / len(job_words) * 100)

        st.subheader("📊 Job Match Score")
        st.success(f"{match_score}% match with job description")

        # =========================
        # MISSING KEYWORDS
        # =========================
        missing_keywords = job_words - resume_words

        st.subheader("❌ Missing Keywords from Resume")
        st.write(", ".join(list(missing_keywords)[:20]))

        # =========================
        # IMPROVEMENT SUGGESTIONS
        # =========================
        st.subheader("💡 How to Improve Your Resume for This Job")

        suggestions = []

        if match_score < 50:
            suggestions.append("⚠️ Your resume is not aligned with this job. Consider major updates.")

        if match_score < 70:
            suggestions.append("⚠️ Add more relevant skills and experience from the job description.")

        if missing_keywords:
            suggestions.append(f"👉 Add these keywords naturally: {', '.join(list(missing_keywords)[:10])}")

        if "experience" not in text:
            suggestions.append("👉 Add relevant work experience matching this job.")

        if "skills" not in text:
            suggestions.append("👉 Add a skills section tailored to this job.")

        # =========================
        # REWRITE HELP
        # =========================
        st.subheader("✍️ Suggested Resume Improvements")

        st.write("❌ Generic: Worked on data analysis")
        st.write("✅ Better: Analyzed business data using Python and SQL to improve decision-making")

        st.write("❌ Generic: Responsible for dashboard")
        st.write("✅ Better: Built interactive dashboards using Power BI to track KPIs")

        # =========================
        # DISPLAY SUGGESTIONS
        # =========================
        if suggestions:
            for s in suggestions:
                st.write(s)
        else:
            st.success("🔥 Your resume is well aligned with this job!")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("Made with | AI Resume Assistant")
