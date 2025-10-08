FROM python:3.14-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir uvicorn fastapi pydantic email-validator && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]