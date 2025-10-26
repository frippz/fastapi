FROM python:3.12-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache curl

# Install uv
RUN pip install --no-cache-dir uv

# Copy requirements and install dependencies
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Copy application code
COPY app/ ./app/

# Create data directory with proper permissions
RUN mkdir -p /app/data && chmod 755 /app/data

EXPOSE 80

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
