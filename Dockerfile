FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

ENV RENDER_API=1
CMD ["sh", "-c", "uvicorn api:api --host 0.0.0.0 --port ${PORT:-10000}"]