FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Render HTTP port
EXPOSE 8080

# Start FastAPI with Gunicorn (also runs bot via startup event)
CMD ["gunicorn", "main:web_app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080"]
