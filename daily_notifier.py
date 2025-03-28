
import sqlite3
import pandas as pd
from crawler.saramin import get_saramin_jobs
from crawler.jobkorea import get_jobkorea_jobs
from filter.gpt_filter import filter_jobs_with_gpt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from twilio.rest import Client

EMAIL_ADDRESS = "dlwjdwls90@gmail.com"
EMAIL_PASSWORD = "zdsz117871!"
TWILIO_SID = "your_twilio_sid"
TWILIO_TOKEN = "your_twilio_token"
TWILIO_NUMBER = "your_twilio_number"

conn = sqlite3.connect("search_conditions.db")
cursor = conn.cursor()
cursor.execute("SELECT job_keyword, required_tech, min_salary, email, phone FROM user_conditions")
users = cursor.fetchall()

for job_keyword, required_tech, min_salary, email, phone in users:
    tech_list = [t.strip() for t in required_tech.split(",")]
    saramin_jobs = get_saramin_jobs(job_keyword)
    jobkorea_jobs = get_jobkorea_jobs(job_keyword)
    raw_jobs = saramin_jobs + jobkorea_jobs
    filtered = filter_jobs_with_gpt(raw_jobs, job_keyword, tech_list, min_salary)

    if not filtered:
        continue

    df = pd.DataFrame(filtered)
    csv_data = df.to_csv(index=False).encode("utf-8-sig")

    if email:
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = email
            msg["Subject"] = f"[맞춤형 채용공고] {job_keyword} 관련 {len(filtered)}건"

            body = f"총 {len(filtered)}개의 공고가 필터링되었습니다. 첨부파일을 확인해주세요."
            msg.attach(MIMEText(body, "plain"))

            part = MIMEBase("application", "octet-stream")
            part.set_payload(csv_data)
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment; filename=filtered_jobs.csv")
            msg.attach(part)

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()

            print(f"✅ 이메일 전송 완료: {email}")
        except Exception as e:
            print(f"❌ 이메일 전송 실패 ({email}): {e}")

    if phone:
        try:
            client = Client(TWILIO_SID, TWILIO_TOKEN)
            message = client.messages.create(
                body=f"[맞춤형 채용공고] {job_keyword} 관련 {len(filtered)}건의 공고가 도착했습니다.",
                from_=TWILIO_NUMBER,
                to=phone
            )
            print(f"📲 문자 전송 완료: {phone}")
        except Exception as e:
            print(f"❌ 문자 전송 실패 ({phone}): {e}")
