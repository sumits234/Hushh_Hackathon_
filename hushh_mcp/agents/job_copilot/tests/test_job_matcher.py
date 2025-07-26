import os
import sys
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from dotenv import load_dotenv

load_dotenv()

# Setup paths
RESUME_PATH = "vault/resumes/sample_resume.txt"
JDS_FOLDER = "vault/jds"

def load_documents():
    docs = []
    for filename in os.listdir(JDS_FOLDER):
        if filename.endswith(".txt"):
            with open(os.path.join(JDS_FOLDER, filename), "r", encoding="utf-8") as f:
                content = f.read()
                docs.append(Document(page_content=content, metadata={"filename": filename}))
    return docs

def main():
    # 1. Load resume
    with open(RESUME_PATH, "r", encoding="utf-8") as f:
        resume_text = f.read()

    # 2. Load job docs
    docs = load_documents()
    if not docs:
        print("❌ No job descriptions found in vault/jds/")
        return

    # 3. Create vector store
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)

    # 4. Query with resume
    print("🔍 Matching jobs based on your resume...\n")
    results = db.similarity_search(resume_text, k=3)

    for i, result in enumerate(results, 1):
        print(f"🔹 Match #{i}: {result.metadata['filename']}")
        print(result.page_content[:300], "...\n")

if __name__ == "__main__":
    main()
