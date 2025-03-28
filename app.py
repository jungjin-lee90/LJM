
# app.py (웹 UI 실행용)
import streamlit as st
import pandas as pd
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from twilio.rest import Client
from crawler.saramin import get_saramin_jobs
from crawler.jobkorea import get_jobkorea_jobs
from filter.gpt_filter import filter_jobs_with_gpt

# DB 초기화
conn = sqlite3.connect("search_conditions.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_conditions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_keyword TEXT,
    required_tech TEXT,
    min_salary INTEGER,
    email TEXT,
    phone TEXT
)
''')
conn.commit()

st.title("📌 맞춤형 채용공고 필터링 봇")
st.markdown("원하는 조건을 입력해 필터링된 채용공고를 확인하세요.")

# 🔍 사용자 입력 조건
job_keyword = st.text_input("직무 키워드", value="DevOps")
required_tech = st.text_input("기술 스택 (쉼표로 구분)", value="Kubernetes")
min_salary = st.number_input("최소 연봉 (만원)", value=5000, step=100)
email = st.text_input("📧 결과를 받을 이메일 주소 (선택)", value="")
send_email = st.checkbox("📬 이메일로 결과 받기")
phone = st.text_input("📱 결과를 받을 핸드폰 번호 (선택, 국제형식 +82...)", value="")
send_sms = st.checkbox("📲 문자(SMS)로 결과 받기")

# 조건 저장
if st.button("🔐 검색 조건 저장하기"):
    cursor.execute('''
        INSERT INTO user_conditions (job_keyword, required_tech, min_salary, email, phone)
        VALUES (?, ?, ?, ?, ?)
    ''', (job_keyword, required_tech, min_salary, email, phone))
    conn.commit()
    st.success("조건이 저장되었습니다. 하루에 한 번 자동 알림이 전송됩니다!")

run_filter = st.button("채용공고 필터링 시작")

if run_filter:
    with st.spinner("채용공고를 수집 중입니다..."):
        saramin_jobs = get_saramin_jobs(keyword=job_keyword)
        jobkorea_jobs = get_jobkorea_jobs(keyword=job_keyword)
        raw_jobs = saramin_jobs + jobkorea_jobs

        filtered_jobs = filter_jobs_with_gpt(
            raw_jobs,
            target_job=job_keyword,
            target_tech=[t.strip() for t in required_tech.split(",")],
            target_salary=min_salary
        )

    st.success(f"총 {len(filtered_jobs)}개의 공고가 필터링되었습니다.")

    for job in filtered_jobs:
        with st.expander(f"{job['title']} ({job['company']}) / {job['salary']}만원"):
            st.markdown(f"**기술스택**: {', '.join(job['tech'])}")
            st.markdown(f"**고용형태**: {job['type']}")
            st.markdown(f"**설명**: {job['description']}")

    df = pd.DataFrame(filtered_jobs)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 CSV로 다운로드",
        data=csv,
        file_name="filtered_jobs.csv",
        mime="text/csv"
    )

    if send_email and email:
        try:
            sender_email = "your_email@gmail.com"
            sender_password = "your_app_password"

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = "[맞춤형 채용공고 결과 안내]"
            msg.attach(MIMEText(f"총 {len(filtered_jobs)}개의 채용공고가 필터링되었습니다.", 'plain'))

            part = MIMEBase('application', 'octet-stream')
            part.set_payload(csv)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename=filtered_jobs.csv")
            msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            st.success("이메일 전송이 완료되었습니다! 📩")
        except Exception as e:
            st.error(f"이메일 전송 실패: {e}")

    if send_sms and phone:
        try:
            account_sid = "your_twilio_account_sid"
            auth_token = "your_twilio_auth_token"
            from_number = "your_twilio_phone_number"

            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f"[맞춤형 채용공고] 총 {len(filtered_jobs)}건이 도착했습니다!",
                from_=from_number,
                to=phone
            )
            st.success("문자(SMS) 전송이 완료되었습니다! 📲")
        except Exception as e:
            st.error(f"SMS 전송 실패: {e}")
