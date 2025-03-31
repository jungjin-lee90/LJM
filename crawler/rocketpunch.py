import requests
from bs4 import BeautifulSoup

def get_rocketpunch_jobs(keyword: str, page: int = 1):
    jobs = []
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://www.rocketpunch.com/jobs?query={keyword}&page={page}"

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        for item in soup.select("div.company.item"):
            title_tag = item.select_one("div.job-title a")
            company_tag = item.select_one("div.name a")

            if title_tag and company_tag:
                job_link = "https://www.rocketpunch.com" + title_tag.get("href")
                jobs.append({
                    "title": title_tag.text.strip(),
                    "company": company_tag.text.strip(),
                    "link": job_link,
                    "company_type": "로켓펀치",
                    "source": "rocketpunch",
                    "logo_url": "",  # 필요 시 후처리
                })
    except Exception as e:
        print("[로켓펀치 크롤링 오류]", e)

    return jobs
