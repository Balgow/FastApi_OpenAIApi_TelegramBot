FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2