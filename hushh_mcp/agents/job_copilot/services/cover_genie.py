import openai
from string import Template
import os

# Load from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cover_letter(job_title, company_name, job_description, user_resume):
    prompt_template = open("hushh_mcp/agents/job_copilot/prompts/cover_letter.tpl").read()
    filled_prompt = Template(prompt_template).substitute(
        job_title=job_title,
        company_name=company_name,
        job_description=job_description,
        user_resume=user_resume
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": filled_prompt}],
        temperature=0.7,
        max_tokens=600
    )

    return response['choices'][0]['message']['content']
