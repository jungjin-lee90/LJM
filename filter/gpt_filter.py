import openai

openai.api_key = "your-api-key-here"

def filter_jobs_with_gpt(jobs, target_job, target_tech, target_salary):
    return [job for job in jobs if job['salary'] >= target_salary and any(t in job['tech'] for t in target_tech)]
