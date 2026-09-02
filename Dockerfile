FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY backend/ ./backend/

# Copy frontend code
COPY frontend/ ./frontend/

# Build frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# Set working directory back to app root
WORKDIR /app

# Expose port
EXPOSE 8000

# Run backend with frontend serving
CMD ["python", "-u", "backend/main.py"]
