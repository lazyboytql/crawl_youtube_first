FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/

RUN chmod +x /app/entrypoint.sh

RUN adduser --disabled-password --gecos '' appuser
USER appuser

ENTRYPOINT ["sh", "/app/entrypoint.sh"]