import streamlit as st
from pypdf import PdfReader

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Resume Assistant", layout="centered")

# =========================
# CUSTOM STYLING
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
st.markdown("### 🎯 Land your dream job faster")
st.markdown("Get instant resume feedback, improve your CV, and match with job descriptions in seconds.")

st.markdown("---")

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:

    # Extract text
    reader = PdfReader(uploaded_file)
    resume_text = ""

    for page in reader.pages:
        resume_text += page.extract_text() or ""

    # =========================
    # FULL PREVIEW
    # =========================
    st.markdown("## 📌 Resume Preview")
    st.text_area("Full Resume Content", resume_text, height=300)

    # =========================
    # RESUME ANALYSIS
    # =========================
    st.markdown("## ✨ Resume Analysis")

    if st.button("Analyze Resume"):

        st.subheader("📊 Professional Resume Review")
        st.info("📌 This analysis is based on ATS (Applicant Tracking System) best practices.")

        score = 100
        feedback = []
        text = resume_text.lower()

        # Structure
        if "summary" not in text and "objective" not in text:
            feedback.append("💡 Add a strong professional summary highlighting your key skills and experience.")
            score -= 10

        if "experience" not in text:
            feedback.append("💡 Include a detailed work experience section with roles, responsibilities, and achievements.")
            score -= 15

        if "education" not in text:
            feedback.append("💡 Add your educational background with relevant details.")
            score -= 10

        if "skills" not in text:
            feedback.append("💡 Include a dedicated skills section with technical and soft skills.")
            score -= 15

        # Content quality
        if len(resume_text) < 800:
            feedback.append("💡 Your resume seems short. Add projects, measurable achievements, and impact.")
            score -= 10

        # Action verbs
        action_words = ["developed", "built", "analyzed", "led", "designed", "implemented"]
        if not any(word in text for word in action_words):
            feedback.append("💡 Use strong action verbs like 'developed', 'led', or 'implemented' to describe your work.")
            score -= 10

        # Achievements
        if "%" not in resume_text and "increase" not in text:
            feedback.append("💡 Add measurable achievements (e.g., increased revenue by 20%, reduced costs by 15%).")
            score -= 10

        # Keywords
        keywords = ["python", "sql", "data", "analysis", "dashboard"]
        missing_keywords = [kw for kw in keywords if kw not in text]

        if missing_keywords:
            feedback.append(f"💡 Missing important industry keywords: {', '.join(missing_keywords)}")
            score -= 10

        # Formatting
        if len(resume_text.split("\n")) < 10:
            feedback.append("💡 Improve formatting with clear sections and bullet points.")
            score -= 5

        # Final Score
        st.success(f"📈 Resume Score: {score}/100")

        if feedback:
            for f in feedback:
                st.write(f)
        else:
            st.success("🔥 Excellent resume! Well-structured and impactful.")

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
st.markdown("## ⚙️ How it works")
st.markdown("""
1. Upload your resume  
2. Get instant feedback  
3. Match with job descriptions  
4. Improve and apply confidently 🚀
""")

st.markdown("⭐ Used by job seekers to improve resumes instantly")
st.markdown("---")
st.markdown("Made with ❤️ | AI Resume Assistant")
