from services.emailer import send_job_application_email
from utils.scheduler import schedule_follow_up
from services.calendar import add_interview_event
from services.cover_genie import generate_cover_letter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
import os
import datetime
import csv
from datetime import datetime

def cover_letter_from_rag():
    print("📄 Generating RAG-based personalized cover letter...")

    # Load resume
    resume_path = "vault/resumes/sample_resume.txt"
    with open(resume_path, "r", encoding="utf-8") as f:
        resume_text = f.read()

    # Load Job Descriptions (JDs)
    jd_folder = "vault/jds"
    documents = []
    for file in os.listdir(jd_folder):
        if file.endswith(".txt"):
            with open(os.path.join(jd_folder, file), "r", encoding="utf-8") as f:
                content = f.read()
                documents.append(Document(page_content=content, metadata={"filename": file}))

    # Vector similarity using FAISS
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = splitter.split_documents(documents)
    db = FAISS.from_documents(texts, OpenAIEmbeddings())
    results = db.similarity_search(resume_text, k=1)

    if not results:
        print("❌ No matching job descriptions found.")
        return

    # Top match JD
    top_jd = results[0].page_content

    # Generate personalized letter
    cover_letter = generate_cover_letter(resume_text, top_jd)

    # Save to disk
    output_path = "vault/letters/generated_letter.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cover_letter)

    print("✅ Cover letter saved:", output_path)


def start_job_application_flow(to_email="recruiter@example.com", resume_file="sample_resume.txt", jd_file="sample_job1.txt"):
    print("🚀 Starting full job application flow...")

    resume_path = f"vault/resumes/{resume_file}"
    jd_path = f"vault/jds/{jd_file}"

    # === Step 1: Read files ===
    with open(resume_path, "r", encoding="utf-8") as f:
        resume_text = f.read()
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    # === Step 2: Generate personalized letter ===
    from services.cover_genie import generate_cover_letter
    cover_letter = generate_cover_letter(resume_text, jd_text)

    # Save cover letter
    cover_letter_path = "vault/letters/generated_letter.txt"
    with open(cover_letter_path, "w", encoding="utf-8") as f:
        f.write(cover_letter)

    # === Step 3: Compose Email ===
    subject = "Application for Software Engineer Role"
    body_text = (
        "Dear Hiring Manager,\n\n"
        "I hope you're doing well. Please find attached my resume and cover letter "
        "for the Software Engineer position.\n\n"
        "Best regards,\nSumit Adikari"
    )

    # === Step 4: Send Email ===
    from services.emailer import send_job_application_email
    send_job_application_email(
        to_email=to_email,
        subject=subject,
        body_text=body_text,
        resume_path=resume_path,
        cover_letter_path=cover_letter_path
    )

    # === Step 5: Schedule Follow-Up ===
    from utils.scheduler import schedule_follow_up
    schedule_follow_up(to_email, resume_path, cover_letter_path)

    # === Step 6: Calendar Event (Mock) ===
    import datetime
    from services.calendar import add_interview_event
    interview_datetime = datetime.datetime.now() + datetime.timedelta(days=2, hours=2)
    add_interview_event(interview_datetime, 30, summary="Interview with Google")

     # === Step 7: Save application log ===
    log_path = "vault/logs/applications.csv"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    log_entry = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        subject,
        to_email,
        resume_file,
        jd_file,
        "✅ Sent and Follow-up Scheduled"
    ]

    file_exists = os.path.isfile(log_path)
    with open(log_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Timestamp", "Job Title", "Email", "Resume", "JD", "Status"])
        writer.writerow(log_entry)

    print("✅ All done: Email, follow-up, and calendar.")
