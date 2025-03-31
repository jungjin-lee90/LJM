import streamlit as st
import base64
from crawler_sources import get_all_jobs
import streamlit.components.v1 as components
import hashlib

# 1. 필터 기능 추가.
# 2. 같은 내용의 공고일 경우에 하나의 공고로 표현하고, 사람인 마크와 잡코리아 마크를 넣고 마크를 누르면 각각의 사이트로 링크되게끔
# 3. 알림 기능 추가. 사용자가 원하는 조건으로 설정해두면 해당 조건에 맞는 공고가 추가될 경우에 알림을 보내도록. 
# 카카오톡이면 괜찮을거 같음, DB 연동, cron 연동
# 4. favicon 생성 O
# 5. 타이틀을 좀더 멋있게 변경 O
# 6. 최대 공고 개수 증가, 현재는 1페이지 밖에 못가져오고 있음.
# 7. 잡코리아, 사람인 아이콘 및 크롤링에 대한 법적인 문제가 없는지도 서비스 오픈한다면 확인해봐야 함.
# 8. job-card ux 변경 O
# 9. 원티드, 로켓펀치 크롤링도 제공
# 10. 상업화 이전엔 크롤링 방식, 어느정도 트래픽이 확인되고 나면 크롤링에서 API 방식으로 변경해야 한다.
# 11. 채용 사이트 로고 사라짐, 이전, 다음 위치 조정

def get_color_from_company(company_name):
    hash_object = hashlib.md5(company_name.encode())
    hex_digest = hash_object.hexdigest()
    hue = int(hex_digest[:2], 16) * 360 // 255
    return f"hsl({hue}, 70%, 50%)"

def get_color_from_company_type(company_type):
    if "대기업" in company_type:
        return "#1A237E"
    elif "중견" in company_type:
        return "#6A1B9A"
    elif "중소" in company_type:
        return "#00897B"
    elif "스타트업" in company_type:
        return "#FB8C00"
    elif "외국계" in company_type:
        return "#C62828"
    return "#0d47a1"

def get_icon_from_source(source):
    if "jobkorea" in source:
        return jobkorea_base64
    elif "saramin" in source:
        return saramin_base64
    elif "wanted" in source:
        return wanted_base64
    elif "rocketpunch" in source:
        return rocket_base64

# PNG 파일을 Base64로 인코딩
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

jobkorea_base64 = get_base64_image("./icon/jobkorea.png")
saramin_base64 = get_base64_image("./icon/saramin.png")
favicon_base64 = get_base64_image("./icon/EmployeeLee.png")
wanted_base64 = get_base64_image("./icon/wanted.png")
rocket_base64 = get_base64_image("./icon/rocketpunch.png")

# 페이지 설정
st.set_page_config(
    page_title="이직원 - 이직을 원하는 사람들",
    page_icon=f"data:image/png;base64,{favicon_base64}",  # base64 favicon
    layout="wide"
)

# CSS 삽입 (Base64 배경 이미지 포함)
st.markdown(f"""
    <style>
    .reportview-container .main .block-container {{
        padding-left: 20% !important;
        padding-right: 20% !important;
    }}
    .job-card {{
        background-color: #f5f5f5;
        border-radius: 15px;
        padding: 15px;
        margin: 10px;
        text-align: center;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        height: 220px;
        width: 90%;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: normal;
        overflow: auto;
        transition: all 0.2s ease-in-out;
    }}
    .job-card:hover {{
        background-color: #e0f0ff;
        transform: scale(1.03);
        cursor: pointer;
    }}
    .job-card.jobkorea {{
        background-image: url("data:image/png;base64,{jobkorea_base64}");
        background-repeat: no-repeat;
        background-position: center calc(100% - 14px);
        background-size: 60px;
    }}
    .job-card.saramin {{
        background-image: url("data:image/png;base64,{saramin_base64}");
        background-repeat: no-repeat;
        background-position: bottom center;
        background-size: 85px;
    }}
    .job-title {{
        /*background-color: #e3f2fd; */  /* 연한 하늘색 */
        padding: 5px 8px;
        border-radius: 8px;
        font-weight: bold;
        color: #0d47a1;  /* 진한 파란색 텍스트 */
        display: inline-block;
        margin-bottom: 6px;
        font-size: 15px;  /* 기존보다 약간 작게 */
    }}
    .job-company {{
        /* background-color: #f1f8e9; */  /* 연한 연두색 */
        padding: 4px 8px;
        border-radius: 8px;
        font-weight: 500;
        color: #33691e;  /* 진한 초록색 텍스트 */
        display: inline-block;
        margin-bottom: 6px;
        font-size: 13px;  /* 회사명은 더 살짝 작게 */
    }}
    .job-card.large {{
        border-right: 6px solid #1A237E;  /* 대기업: 남색 */
        border-bottom: 6px solid #1A237E;  /* 대기업: 남색 */
    }}
    .job-card.medium {{
        border-right: 6px solid #6A1B9A;  /* 중견기업: 보라 */
        border-bottom: 6px solid #6A1B9A;  /* 중견기업: 보라 */
    }}
    .job-card.small {{
        border-right: 6px solid #00897B;  /* 중소기업: 청록 */
        border-bottom: 6px solid #00897B;  /* 중소기업: 청록 */
    }}
    .job-card.startup {{
        border-right: 6px solid #FB8C00;  /* 스타트업: 주황 */
        border-bottom: 6px solid #FB8C00;  /* 스타트업: 주황 */
    }}
    .job-card.foreign {{
        border-right: 6px solid #C62828;  /* 외국계: 빨강 */
        border-bottom: 6px solid #C62828;  /* 외국계: 빨강 */
    }}

    </style>
""", unsafe_allow_html=True)


# 타이틀 중앙 정렬
# ✅ 상단 타이틀 + 로고 이미지 + 애니메이션
components.html(f"""
    <div style="text-align: center;">
        <div style="display: flex; justify-content: center; align-items: center; gap: 12px;">
            <img src="data:image/png;base64,{favicon_base64}" style="height: 48px;" />
            <h1 id="title-text" style="
                transition: opacity 1s ease-in-out, color 1s ease-in-out;
                font-size: 48px;
                margin: 0;
                color: #1A237E;
            ">이직을 원하는 사람들</h1>
        </div>
        <p style="font-size: 18px;">직무 키워드를 입력해 채용공고를 확인하세요.</p>
    </div>

    <script>
        const titles = [
            {{ text: "이직을 원하는 사람들", color: "#1A237E" }},
            {{ text: "이직원", color: "#FB8C00" }}
        ];
        let i = 0;
        const titleElement = document.getElementById("title-text");

        function switchTitle() {{
            if (!titleElement) return;
            titleElement.style.opacity = 0;
            setTimeout(() => {{
                i = (i + 1) % titles.length;
                titleElement.innerText = titles[i].text;
                titleElement.style.color = titles[i].color;
                titleElement.style.opacity = 1;
            }}, 1000);
        }}

        setInterval(switchTitle, 5000);
    </script>
""", height=150)


# 🔻 1차 구분선
st.markdown("""
    <hr style="
        border: 1px solid #ccc;
        width: 33%;
        margin: 30px auto;
    ">
""", unsafe_allow_html=True)


# 검색바 및 버튼 중앙 정렬
left_col, search_col, right_col = st.columns([3, 3, 3])
with search_col:
    st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
            <div style="margin-bottom: 10px; font-weight: bold; font-size: 18px;">🔍 직무 검색</div>
        </div>
    """, unsafe_allow_html=True)
    job_keyword = st.text_input("직무 키워드 입력", value="DevOps", label_visibility="collapsed")
    run_search = st.button("채용공고 검색", type="primary")

# 기업 형태 설명
st.markdown(f"""
    <style>
    .custom-legend {{
        position: absolute;
        top: -150px;
        right: 600px;
        background-color: #fff;
        padding: 10px 15px;
        border: 1px solid #ccc;
        border-radius: 8px;
        font-size: 14px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }}
    </style>
    <div class="custom-legend">
        <ul style="list-style: none; padding-left: 0; line-height: 1.6; margin-top: 8px;">
            <li><span style="display:inline-block; width:12px; height:12px; background:#1A237E; margin-right:6px; border-radius:2px;"></span>대기업</li>
            <li><span style="display:inline-block; width:12px; height:12px; background:#6A1B9A; margin-right:6px; border-radius:2px;"></span>중견기업</li>
            <li><span style="display:inline-block; width:12px; height:12px; background:#00897B; margin-right:6px; border-radius:2px;"></span>중소기업</li>
            <li><span style="display:inline-block; width:12px; height:12px; background:#FB8C00; margin-right:6px; border-radius:2px;"></span>스타트업</li>
            <li><span style="display:inline-block; width:12px; height:12px; background:#C62828; margin-right:6px; border-radius:2px;"></span>외국계기업</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# 🔻 2차 구분선
st.markdown("""
    <hr style="
        border: 1px solid #ccc;
        width: 33%;
        margin: 30px auto;
    ">
""", unsafe_allow_html=True)


# 페이지네이션 상태
PER_PAGE = 30
if "page" not in st.session_state:
    st.session_state.page = 0

if "loading" not in st.session_state:
    st.session_state.loading = False

if "search_triggered" not in st.session_state:
    st.session_state.search_triggered = False

if run_search:
    st.session_state.loading = True
    st.session_state.search_triggered = True
    st.rerun() 

if st.session_state.loading: 
    # 애니메이션 정의
    st.markdown("""
    <style>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .spinner {
        display: inline-block;
        width: 18px;
        height: 18px;
        border: 3px solid #ccc;
        border-top: 3px solid #1A237E;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 10px;
        vertical-align: middle;
    }
    </style>
    """, unsafe_allow_html=True)

    # 로딩 UI
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <div style="display: inline-block;">
            <div class="spinner"></div>
            <span style="font-size: 18px; font-weight: bold; vertical-align: middle;">
                채용공고를 수집 중입니다...
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 검색 실행
if st.session_state.search_triggered:
    st.session_state.all_jobs = get_all_jobs(job_keyword)
    st.session_state.page = 0
    st.session_state.loading = False
    st.session_state.search_triggered = False
    st.rerun()  # 🔁 로딩 끝났으니 다시 렌더링
    
# all_jobs가 세션에 존재할 경우 결과 출력
if "all_jobs" in st.session_state:
    all_jobs = st.session_state.all_jobs
    st.markdown(f"""
        <div style="text-align: center; font-size: 16px; font-weight: bold; color: #388E3C; margin-top: 10px; margin-bottom: 10px;">
            ✅ 총 {len(all_jobs)}개의 공고가 수집되었습니다.
        </div>
    """, unsafe_allow_html=True)

    total_pages = (len(all_jobs) - 1) // PER_PAGE + 1
    current_page = st.session_state.page
    start = current_page * PER_PAGE
    end = start + PER_PAGE
    current_jobs = all_jobs[start:end]

    left_col, content_col, right_col = st.columns([2, 3, 2])

    with content_col:
        cols = st.columns(3)
        for idx, job in enumerate(current_jobs):
            with cols[idx % 3]:
                card_class = "job-card"
                company_type = job.get("company_type", "").strip()
                if "대기업" in company_type:
                    card_class += " large"
                elif "중견" in company_type:
                    card_class += " medium"
                elif "중소" in company_type:
                    card_class += " small"
                elif "스타트업" in company_type:
                    card_class += " startup"
                elif "외국계" in company_type:
                    card_class += " foreign"

                company = job.get("company", "회사명")
                title = job.get("title", "공고 제목")
                link = job.get("link", "#")
                color = get_color_from_company_type(company_type)
                source = job.get("source", "")
                icon_base64 = get_icon_from_source(source)
                icon_html = f"<img src='data:image/png;base64,{icon_base64}' style='height: 18px; margin-bottom: 4px;' />" if icon_base64 else ""

                st.markdown(f"""<a href="{link}" target="_blank" style="text-decoration: none; color: inherit;">
                    <div class="{card_class}" style="text-align: center; padding: 20px 16px; border-radius: 12px; min-height: 180px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="margin-bottom: 4px;">{icon_html}</div>
                        <div style="background-color: {color}; color: white; font-size: 18px; font-weight: bold; padding: 12px 8px; border-radius: 12px; margin-bottom: 10px; letter-spacing: 1px;">
                            {company}
                        </div>
                        <div class="job-title" style="font-size: 15px;">{title}</div>
                    </div>
                </a>""", unsafe_allow_html=True)

    # 페이지네이션
    st.markdown("""<div style='text-align: center; margin-top: 20px;'>""", unsafe_allow_html=True)
    col1, col_prev, col_next, col2 = st.columns([2, 8, 3, 2])
    with col_prev:
        if st.session_state.page > 0 and st.button("⬅ 이전", key="prev_page"):
            st.session_state.page -= 1
            st.rerun()
    with col_next:
        if st.session_state.page < total_pages - 1 and st.button("다음 ➡", key="next_page"):
            st.session_state.page += 1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)








