import requests

def get_wanted_jobs(keyword: str, page: int = 1, limit: int = 20):
    jobs = []
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    url = f"https://www.wanted.co.kr/api/v4/jobs?query={keyword}&limit={limit}&offset={(page - 1) * limit}"

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        for item in data.get("data", []):
            jobs.append({
                "title": item.get("position"),
                "company": item.get("company", {}).get("name"),
                "link": f"https://www.wanted.co.kr/wd/{item.get('id')}",
                "location": item.get("address", {}).get("location"),
                "company_type": "원티드",
                "logo_url": item.get("company", {}).get("logo_url", ""),
                "source": "wanted"
            })
    except Exception as e:
        print("[원티드 API 오류]", e)

    return jobs
