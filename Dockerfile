# 1️⃣ Use Python base image
FROM python:3.14-slim

# 2️⃣ Install system packages required for mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 3️⃣ Set working directory
WORKDIR /app

# 4️⃣ Copy requirements
COPY requirements.txt .

# 5️⃣ Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copy full project
COPY . .

# 7️⃣ Expose Flask port
EXPOSE 5000

# 8️⃣ Run app
CMD ["python", "app.py"]
