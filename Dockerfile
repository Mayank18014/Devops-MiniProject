# Use python-slim for a lightweight container
FROM python:3.9-slim

# Set environment variables to optimize Python for Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project folders (database, models, routes, static, templates, utils)
COPY . .

# Expose the Flask port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
