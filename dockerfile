# Use the official Python image
FROM python:3.9-slim

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code
COPY . .

# Expose port 8000 (default for FastAPI)
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "myapp:app", "--host", "0.0.0.0", "--port", "8000"]
