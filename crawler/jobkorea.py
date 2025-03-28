import requests
from bs4 import BeautifulSoup
import json

def get_jobkorea_jobs(keyword):
    url = f"https://www.jobkorea.co.kr/Search/?stext={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []
    for article in soup.select("article.list-item"):
        try:
            link = article.get("data-gavirturl")               
            raw_data = article.get("data-gainfo")

            job_info = json.loads(raw_data) if raw_data else {}

            title = job_info.get("dimension45", "")  # 타이틀명
            company = job_info.get("dimension48", "")  # 회사명

            if not (title and company and link):
                continue

            clean_link = link.replace("/virtual", "", 1)
            print(clean_link)
            jobs.append({
                "title": title,
                "company": company,
                "link": clean_link,
                "source": "jobkorea"
            })
        except Exception as e:
            print("[에러]", e)
            continue

    return jobs
