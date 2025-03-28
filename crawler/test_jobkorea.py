from jobkorea import get_jobkorea_jobs

results = get_jobkorea_jobs("DevOps")
for job in results:
    print(job["title"], job["company"], job["link"])

