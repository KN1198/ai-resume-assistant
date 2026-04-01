import streamlit as st
from PyPDF2 import PdfReader

# ✅ Page config (must be first Streamlit command)
st.set_page_config(page_title="AI Resume Assistant", layout="centered")

# ✅ Header UI
st.markdown("## 🚀 AI Resume Analyzer")
st.markdown("Upload your resume and get instant feedback + job match score")

# Upload file
uploaded_file = st.file_uploader("📄 Upload your CV (PDF)", type=["pdf"])

if uploaded_file:

    # Extract text from PDF
    reader = PdfReader(uploaded_file)
    resume_text = ""

    for page in reader.pages:
        resume_text += page.extract_text() or ""

    # Preview
    st.subheader("📌 Resume Preview")
    st.write(resume_text[:500])

    # ===============================
    # 🔥 RESUME ANALYSIS
    # ===============================
    if st.button("✨ Improve Resume"):
        st.subheader("✅ Resume Feedback")

        suggestions = []
        score = 100
        text = resume_text.lower()

        # Section checks
        if "summary" not in text and "objective" not in text:
            suggestions.append("❌ Add a professional summary at the top.")
            score -= 10

        if "experience" not in text:
            suggestions.append("❌ Work experience section is missing.")
            score -= 15

        if "education" not in text:
            suggestions.append("❌ Education section is missing.")
            score -= 10

        if "skills" not in text:
            suggestions.append("❌ Skills section is missing.")
            score -= 15

        # Length checks
        if len(resume_text) < 800:
            suggestions.append("⚠️ Resume is too short. Add more projects and achievements.")
            score -= 10

        if len(resume_text) > 3000:
            suggestions.append("⚠️ Resume is too long. Keep it concise (1–2 pages).")
            score -= 5

        # Keyword check
        keywords = ["python", "sql", "data", "analysis", "project"]
        missing_keywords = [kw for kw in keywords if kw not in text]

        if missing_keywords:
            suggestions.append(f"⚠️ Missing important keywords: {', '.join(missing_keywords)}")
            score -= 10

        # Action words check
        action_words = ["developed", "built", "analyzed", "created", "improved"]
        if not any(word in text for word in action_words):
            suggestions.append("⚠️ Use strong action verbs like 'developed', 'analyzed', etc.")
            score -= 10

        # Score display
        st.subheader(f"📊 Resume Score: {score}/100")

        if not suggestions:
            st.success("🔥 Excellent resume! You're job-ready.")
        else:
            for s in suggestions:
                st.write(s)

    # ===============================
    # 🎯 JOB MATCHING FEATURE
    # ===============================
    st.markdown("---")
    job_desc = st.text_area("📌 Paste Job Description")

    if st.button("📊 Match Resume with Job"):
        if job_desc:
            st.subheader("📊 Job Match Analysis")

            resume_words = set(resume_text.lower().split())
            job_words = set(job_desc.lower().split())

            match = resume_words.intersection(job_words)
            score = int(len(match) / len(job_words) * 100)

            st.success(f"✅ Match Score: {score}%")

            missing = job_words - resume_words

            if missing:
                st.write("❌ Missing Keywords:")
                st.write(", ".join(list(missing)[:20]))
        else:
            st.warning("Please paste a job description")

else:
    st.info("📌 Upload a resume to get started")