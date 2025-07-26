import argparse
from flows import start_job_application_flow

def main():
    parser = argparse.ArgumentParser(description="🤖 AI Job Application Agent CLI")
    parser.add_argument("--email", required=True, help="Recruiter email to send application to")
    parser.add_argument("--jd", required=False, help="Job description filename in vault/jds/")

    args = parser.parse_args()

    print("🎯 Starting job application process with:")
    print(f"📧 Recruiter Email: {args.email}")
    if args.jd:
        print(f"📄 JD File: {args.jd}")

    start_job_application_flow(to_email=args.email, jd_file=args.jd)

if __name__ == "__main__":
    main()
