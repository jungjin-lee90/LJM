from saramin_selenium import get_saramin_jobs

results = get_saramin_jobs("DevOps")

for job in results:
    print(job["title"], "-", job["company"], job["link"])

