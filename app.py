import streamlit as st
from pypdf import PdfReader

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Resume Assistant", layout="centered")

# =========================
# HEADER
# =========================
st.markdown("""
# 🚀 AI Resume Analyzer  
### Improve your resume & match with jobs instantly
""")

st.markdown("---")

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:

    reader = PdfReader(uploaded_file)
    resume_text = ""

    for page in reader.pages:
        resume_text += page.extract_text() or ""

    # =========================
    # PREVIEW
    # =========================
    st.markdown("## 📌 Resume Preview")
    st.info(resume_text[:500])

    # =========================
    # RESUME ANALYSIS
    # =========================
    st.markdown("## ✨ Resume Analysis")

    if st.button("Analyze Resume"):

        suggestions = []
        score = 100
        text = resume_text.lower()

        if "summary" not in text and "objective" not in text:
            suggestions.append("❌ Add a professional summary")
            score -= 10

        if "experience" not in text:
            suggestions.append("❌ Add work experience section")
            score -= 15

        if "skills" not in text:
            suggestions.append("❌ Add skills section")
            score -= 15

        if len(resume_text) < 800:
            suggestions.append("⚠️ Resume too short")
            score -= 10

        keywords = ["python", "sql", "data", "analysis"]
        missing_keywords = [kw for kw in keywords if kw not in text]

        if missing_keywords:
            suggestions.append(f"⚠️ Missing keywords: {', '.join(missing_keywords)}")
            score -= 10

        st.success(f"📊 Resume Score: {score}/100")

        if suggestions:
            for s in suggestions:
                st.write(s)
        else:
            st.success("🔥 Excellent Resume!")

    # =========================
    # JOB MATCHING
    # =========================
    st.markdown("---")
    st.markdown("## 🎯 Job Match Analysis")

    job_desc = st.text_area("Paste Job Description")

    if st.button("Check Match"):

        if job_desc:
            resume_words = set(resume_text.lower().split())
            job_words = set(job_desc.lower().split())

            match = resume_words.intersection(job_words)
            score = int(len(match) / len(job_words) * 100)

            st.success(f"✅ Match Score: {score}%")

            missing = job_words - resume_words

            if missing:
                st.warning("Missing Keywords:")
                st.write(", ".join(list(missing)[:20]))
        else:
            st.error("Please paste a job description")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("Made with ❤️ by Krunal | AI Resume Assistant")
