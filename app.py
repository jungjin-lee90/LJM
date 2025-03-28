import streamlit as st
import base64
from crawler.saramin import get_saramin_jobs
from crawler.jobkorea import get_jobkorea_jobs

# PNG 파일을 Base64로 인코딩
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

jobkorea_base64 = get_base64_image("/home/leejungjin/job_filter_project/icon/jobkorea.png")

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
        height: 180px;
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
        background-position: bottom center;
        background-size: 60px;
    }}
    </style>
""", unsafe_allow_html=True)

# 타이틀 중앙 정렬
st.markdown("""
    <div style="text-align: center;">
        <h1>📌 맞춤형 채용공고 필터링 봇</h1>
        <p>직무 키워드를 입력해 채용공고를 확인하세요.</p>
    </div>
""", unsafe_allow_html=True)

# 검색바 및 버튼 중앙 정렬
st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
        <div style="margin-bottom: 10px; font-weight: bold; font-size: 18px;">
            🔍 직무 검색
        </div>
    </div>
""", unsafe_allow_html=True)

job_keyword = st.text_input("", value="DevOps", label_visibility="collapsed")

run_search = st.button("채용공고 검색", type="primary")

if run_search:
    with st.spinner("채용공고를 수집 중입니다..."):
        saramin_jobs = get_saramin_jobs(keyword=job_keyword)
        jobkorea_jobs = get_jobkorea_jobs(keyword=job_keyword)
        all_jobs = saramin_jobs + jobkorea_jobs

    st.success(f"총 {len(all_jobs)}개의 공고가 수집되었습니다.")

    # 한 줄에 3개씩 카드 형태로 출력
    cols = st.columns(3)
    for idx, job in enumerate(all_jobs):
        with cols[idx % 3]:
            card_class = "job-card"
            if job.get("source") == "jobkorea":
                card_class += " jobkorea"

            st.markdown(f"""
                <a href="{job['link']}" target="_blank" style="text-decoration: none; color: inherit;">
                    <div class="{card_class}">
                        <strong>{job['title']}</strong><br>
                        {job['company']}<br>
                    </div>
                </a>
            """, unsafe_allow_html=True)

