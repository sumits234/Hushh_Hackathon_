import os
import faiss
import openai
from dotenv import load_dotenv
from utils.parser import extract_text_from_file

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Convert text to embeddings
def get_embedding(text):
    response = openai.Embedding.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

# Load all job descriptions and embed them
def build_job_vector_store(jd_folder="vault/jds"):
    index = faiss.IndexFlatL2(1536)
    jd_texts = []
    filenames = []

    for filename in os.listdir(jd_folder):
        filepath = os.path.join(jd_folder, filename)
        jd_text = extract_text_from_file(filepath)
        if jd_text.strip():
            embedding = get_embedding(jd_text)
            index.add([embedding])
            jd_texts.append(jd_text)
            filenames.append(filename)

    return index, jd_texts, filenames

# Embed the resume and find top N matches
def find_matching_jobs(resume_path, top_n=3):
    index, jd_texts, filenames = build_job_vector_store()
    resume_text = extract_text_from_file(resume_path)
    resume_embedding = get_embedding(resume_text)
    
    D, I = index.search([resume_embedding], top_n)

    results = []
    for idx in I[0]:
        results.append((filenames[idx], jd_texts[idx]))
    
    return results
