import requests
from bs4 import BeautifulSoup

def get_company_logo_saramin(detail_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(detail_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        logo_tag = soup.select_one("div.company_logo img")
        if logo_tag:
            logo_url = logo_tag.get("src")
            if logo_url.startswith("//"):
                logo_url = "https:" + logo_url
            elif logo_url.startswith("/"):
                logo_url = "https://www.saramin.co.kr" + logo_url
            return logo_url
    except Exception as e:
        print("[로고 추출 에러 - 사람인]", e)

    return "/static/default_logo.png"


def get_company_type(company_info_url):
    try:
        res = requests.get(company_info_url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")

        for li in soup.select("li.company_summary_item"):
            label = li.select_one("p.company_summary_desc")
            value = li.select_one("strong.company_summary_tit")
            if label and "기업형태" in label.text:
                return value.text.strip()
    except Exception as e:
        print("[기업형태 에러]", e)
    return ""

def get_saramin_jobs(keyword, max_pages=None):
    base_url = "https://www.saramin.co.kr/zf_user/search?searchword={keyword}&recruitPage={page}"
    headers = {"User-Agent": "Mozilla/5.0"}

    jobs = []

    # 첫 페이지 → 최대 페이지 감지
    first_url = base_url.format(keyword=keyword, page=1)
    res = requests.get(first_url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser", from_encoding="utf-8")

    if not max_pages:
        page_numbers = soup.select("div.pagination a.btn_page")
        max_pages = max([int(a.text) for a in page_numbers if a.text.isdigit()] or [1])

    for page in range(1, max_pages + 1):
        url = base_url.format(keyword=keyword, page=page)
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser", from_encoding="utf-8")

        for item in soup.select("div.item_recruit"):
            try:
                title_tag = item.select_one("h2.job_tit > a")
                company_tag = item.select_one("div.area_corp strong.corp_name")
                company_info_tag = item.select_one("div.area_corp_info a")

                if not (title_tag and title_tag.get("title") and company_tag):
                    continue

                title = title_tag.get("title").strip()
                link = title_tag.get("href", "").strip()
                company = company_tag.get_text(strip=True)

                if link.startswith("/zf_user"):
                    link = f"https://www.saramin.co.kr{link}"

                company_info_link = ""
                if company_info_tag:
                    raw_href = company_info_tag.get("href", "")
                    if raw_href.startswith("/zf_user"):
                        company_info_link = f"https://www.saramin.co.kr{raw_href}"

                company_type = get_company_type(company_info_link)

                jobs.append({
                    "title": title,
                    "company": company,
                    "link": link,
                    "source": "saramin",
                    "company_type": company_type
                })
            except Exception as e:
                print("[에러]", e)
                continue

    return jobs

