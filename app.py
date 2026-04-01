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
        st.info("📌 Detailed feedback based on recruiter & ATS best practices")

        score = 100
        text = resume_text.lower()

        sections = {
            "summary": "summary" in text or "objective" in text,
            "experience": "experience" in text,
            "education": "education" in text,
            "skills": "skills" in text
        }

        feedback = []

        # Summary
        if not sections["summary"]:
            feedback.append("❌ Missing Professional Summary\n👉 Add 2–3 lines highlighting your experience, skills, and career focus.\n💡 Example: 'Data Analyst with 4+ years of experience in Python, SQL, and dashboarding.'")
            score -= 10

        # Experience
        if not sections["experience"]:
            feedback.append("❌ Missing Work Experience Section\n👉 Clearly mention your roles with responsibilities and achievements.")
            score -= 15
        else:
            if "responsible for" in text:
                feedback.append("⚠️ Weak phrasing in experience\n👉 Replace 'Responsible for' with strong action verbs like 'Led', 'Developed', 'Optimized'.")
                score -= 5

        # Education
        if not sections["education"]:
            feedback.append("❌ Missing Education Section\n👉 Add your academic background clearly.")
            score -= 10

        # Skills
        if not sections["skills"]:
            feedback.append("❌ Missing Skills Section\n👉 Add technical skills like Python, SQL, Power BI, Excel.")
            score -= 15

        # Achievements
        if "%" not in resume_text and "increase" not in text:
            feedback.append("⚠️ No measurable achievements\n👉 Add impact like 'Improved efficiency by 20%' or 'Reduced cost by 15%'")
            score -= 10

        # Length
        if len(resume_text) < 800:
            feedback.append("⚠️ Resume too short\n👉 Add more projects, tools, and achievements.")
            score -= 10

        # Keywords
        keywords = ["python", "sql", "data", "analysis", "dashboard", "excel"]
        missing_keywords = [kw for kw in keywords if kw not in text]

        if missing_keywords:
            feedback.append(f"⚠️ Missing important keywords: {', '.join(missing_keywords)}\n👉 Add these to improve ATS ranking.")
            score -= 10

        # =========================
        # REWRITE SUGGESTIONS
        # =========================
        st.markdown("## ✍️ Suggested Improvements")

        if "responsible for" in text:
            st.write("❌ Responsible for managing data")
            st.write("✅ Managed and analyzed data to improve decision-making by 25%")

        if "worked on" in text:
            st.write("❌ Worked on dashboard")
            st.write("✅ Designed and developed interactive dashboards using Power BI")

        # =========================
        # SCORE
        # =========================
        st.markdown("## 📈 Resume Score")
        st.success(f"{score}/100")

        # =========================
        # FEEDBACK
        # =========================
        st.markdown("## 📌 Detailed Feedback")

        if feedback:
            for f in feedback:
                st.write(f)
        else:
            st.success("🔥 Excellent resume! Ready for job applications.")

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
st.markdown("Made with ❤️ by Krunal | AI Resume Assistant")
