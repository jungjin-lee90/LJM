import requests
from bs4 import BeautifulSoup
import json

def get_company_logo_jobkorea(detail_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(detail_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # 상세 페이지 내 기업 로고 img 태그 찾기
        logo_tag = soup.select_one("div.coLogo img")
        if logo_tag:
            logo_url = logo_tag.get("src")
            if logo_url.startswith("//"):
                logo_url = "https:" + logo_url
            elif logo_url.startswith("/"):
                logo_url = "https://www.jobkorea.co.kr" + logo_url
            return logo_url
    except Exception as e:
        print("[로고 추출 에러]", e)

    # 실패 시 기본 로고 이미지
    return "/static/default_logo.png"


def get_company_type_jobkorea(detail_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(detail_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # '기업형태' 텍스트가 포함된 dt 찾기
        for dt in soup.find_all("dt"):
            if "기업형태" in dt.get_text(strip=True):
                dd = dt.find_next_sibling("dd")
                return dd.get_text(strip=True) if dd else ""
    except Exception as e:
        print("[기업형태 추출 에러]", e)
    return ""

def get_jobkorea_jobs(keyword, max_pages=None):
    base_url = "https://www.jobkorea.co.kr/Search/?stext={keyword}&tabType=recruit"
    headers = {"User-Agent": "Mozilla/5.0"}

    jobs = []

    # 먼저 첫 페이지 요청 → 최대 페이지 확인
    first_url = base_url.format(keyword=keyword)
    res = requests.get(first_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 페이지 번호 중 가장 큰 것 찾기
    if not max_pages:
        page_numbers = soup.select("div.tplPagination a.tplBtn.tplBtn-num")
        max_pages = max([int(a.text) for a in page_numbers if a.text.isdigit()] or [1])

    for page in range(1, max_pages + 1):
        url = base_url.format(keyword=keyword) + f"&Page_No={page}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        for article in soup.select("article.list-item"):
            try:
                link = article.get("data-gavirturl")
                raw_data = article.get("data-gainfo")

                job_info = json.loads(raw_data) if raw_data else {}

                title = job_info.get("dimension45", "")
                company = job_info.get("dimension48", "")

                if not (title and company and link):
                    continue

                clean_link = link.replace("/virtual", "", 1)

                company_type = get_company_type_jobkorea(clean_link)
                jobs.append({
                    "title": title,
                    "company": company,
                    "link": clean_link,
                    "source": "jobkorea",
                    "company_type": company_type
                })
            except Exception as e:
                print("[에러]", e)
                continue

    return jobs

