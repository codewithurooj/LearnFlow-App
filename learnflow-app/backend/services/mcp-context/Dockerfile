FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY shared/ /app/shared/
COPY services/mcp-context/ /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8008}/health || exit 1

EXPOSE 8008
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8008}"]
