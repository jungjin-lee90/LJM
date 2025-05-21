FROM python:3.10-slim

WORKDIR /app

# 시스템 패키지 설치 (필요 시 cron 등 추가 가능)
RUN apt-get update && apt-get install -y \
    curl \
 && rm -rf /var/lib/apt/lists/*

# 파이썬 패키지 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 앱 소스 복사
COPY . .

# 포트 설정 (Streamlit 기본 포트)
EXPOSE 8501

# 실행 명령
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

