from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity  
from skills import skills_list
from transformers import pipeline

feedback_generator = pipeline(
    "text-generation",
    model="gpt2",
    max_length=150
)

model = SentenceTransformer('all-MiniLM-L6-v2')

def detect_skills(resume_text):
    detected = []

    resume_text = resume_text.lower()

    for skill in skills_list:
        if skill in resume_text:
            detected.append(skill)

    return detected



def semantic_match(resume_skills, job_skills):

    resume_embeddings = model.encode(resume_skills)
    job_embeddings = model.encode(job_skills)

    similarity_matrix = cosine_similarity(resume_embeddings, job_embeddings)

    matched = []
    missing = []

    for i, job_skill in enumerate(job_skills):
        similarity_scores = similarity_matrix[:, i]
        max_score = max(similarity_scores)

        if max_score > 0.6:
            matched.append(job_skill)
        else:
            missing.append(job_skill)

    return matched, missing


def generate_resume_feedback(resume_text, job_description):

    prompt = f"""
    Analyze the following resume and job description.
    Provide suggestions to improve the resume.

    Resume:
    {resume_text[:800]}

    Job Description:
    {job_description}

    Suggestions:
    """

    result = feedback_generator(
        prompt,
        max_new_tokens=120,
        temperature=0.7
    )

    generated_text = result[0]["generated_text"]

    feedback = generated_text.replace(prompt, "")

    return feedback