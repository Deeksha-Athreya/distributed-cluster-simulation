FROM python:3.9-slim

WORKDIR /app

# Copy project files
COPY requirements.txt .
COPY src/ ./src/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Default command
CMD ["python", "-m", "src.api_server"]