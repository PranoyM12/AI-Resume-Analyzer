from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import pdfplumber
from analyzer import generate_resume_feedback
from analyzer import detect_skills

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume", type="pdf")

job_description = st.text_area("Enter Job Description")


if uploaded_file is not None:

    resume_text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                resume_text += text


    resume_skills = list(dict.fromkeys(detect_skills(resume_text)))
    job_skills = list(dict.fromkeys(detect_skills(job_description)))

    from analyzer import semantic_match
    matched_skills, missing_skills = semantic_match(resume_skills, job_skills)

    if len(job_skills) > 0:
        score = int((len(matched_skills) / len(job_skills)) * 100)
    else:
        score = 0


    #Score Section
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Resume Match Score", f"{score}%")
        st.progress(score/100)

    with col2:
        st.metric("Skills Found", len(resume_skills))
        st.metric("Skills Required", len(job_skills))


    #Skill Statistics
    st.subheader("Skill Statistics")

    total_resume_skills = len(resume_skills)
    total_job_skills = len(job_skills)
    matched_count = len(matched_skills)

    st.write("Total Resume Skills:", total_resume_skills)
    st.write("Total Job Skills:", total_job_skills)
    st.write("Matched Skills:", matched_count)
    


    #Bar Chart for Matched vs Missing Skills
    import pandas as pd

    data = {
        "Category": ["Matched Skills", "Missing Skills"],
        "Count": [len(matched_skills), len(missing_skills)]
    }

    df = pd.DataFrame(data)

    st.bar_chart(df.set_index("Category"))


    #Matched Skill Section
    st.subheader("Matched Skills")
    for skill in matched_skills:
        st.write(skill)


    #Missing Skill Section
    st.subheader("Skills Missing From Resume")

    if missing_skills:
        for skill in missing_skills:
            st.write("❌", skill)
    else:
        st.write("No missing skills. Your resume matches the job description well.")


    #Skill Visualization Section
    st.subheader("Skill Match Visualization")

    matched_count = len(matched_skills)
    missing_count = len(missing_skills)

    labels = ['Matched Skills', 'Missing Skills']
    sizes = [matched_count, missing_count]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    st.pyplot(fig)

    st.subheader("Top Skills Found in Resume")

    for skill in resume_skills[:10]:
        st.write("✔", skill)


    #AI Suggestions Section
    st.subheader("AI Resume Feedback")

    if score >= 80:
        st.success("Your resume is a strong match for this job.")

    elif score >= 50:
        st.warning("Your resume partially matches the job description. Consider improving some skills.")

    else:
        st.error("Your resume has low compatibility with this job description.")
    
    if missing_skills:
        st.write("### Skills you should consider adding:")

        for skill in missing_skills:
            st.write("•", skill)


    #Overall Feedback
    st.subheader("Resume Improvement Tips")

    st.write("• Add measurable achievements in your projects")
    st.write("• Mention tools and frameworks clearly")
    st.write("• Include cloud platforms if relevant")
    st.write("• Highlight ML projects with real datasets")


    #Detected Skills Section
    st.subheader("Detected Skills")
    if resume_skills:
        for skill in resume_skills:
            st.write(skill)
    else:
        st.write("No skills detected")

    # Word Cloud Visualization
    st.subheader("Resume Skill Word Cloud")

    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    text = " ".join(resume_skills)

    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")

    st.pyplot(fig)


    #Generate AI Feedback
    st.subheader("AI Resume Suggestions")

    if job_description:

        feedback = generate_resume_feedback(resume_text, job_description)

        st.write(feedback)





    report = f"""
    AI Resume Analysis Report

    Match Score: {score}%

    Matched Skills:
    {matched_skills}

    Missing Skills:
    {missing_skills}

    AI Suggestions:
    {feedback}
    """

    st.download_button(
        label="Download Resume Analysis Report",
        data=report,
        file_name="resume_analysis.txt",
    )


    #Debug Section
    with st.expander("View Extracted Resume Text (Debug)"):
        st.write(resume_text)
