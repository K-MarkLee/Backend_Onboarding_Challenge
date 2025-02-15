FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY=your-secret-key-here \
    DEBUG=True \
    DB_NAME=postgres \
    DB_USER=postgres \
    DB_PASSWORD=postgres \
    DB_HOST=db \
    DB_PORT=5432

# 8000번 포트 노출
EXPOSE 8000

# 헬스체크를 위한 스크립트 추가
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# 실행 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
