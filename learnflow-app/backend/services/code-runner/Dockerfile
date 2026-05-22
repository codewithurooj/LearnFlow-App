FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY shared/ /app/shared/
COPY services/code-runner/ /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run as non-root for security
RUN useradd -m -u 1000 runner
USER runner

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8003/health || exit 1

EXPOSE 8003
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8003}"]
