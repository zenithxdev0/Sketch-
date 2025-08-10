FROM python:3.11-slim

WORKDIR /app

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY . .

EXPOSE 8080

CMD ["gunicorn", "main:web_app", "-b", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker"]

