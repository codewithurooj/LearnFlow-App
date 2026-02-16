FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/services/mcp-context/
COPY ../shared /app/shared/

EXPOSE 8008

CMD ["uvicorn", "services.mcp-context.main:app", "--host", "0.0.0.0", "--port", "8008"]
