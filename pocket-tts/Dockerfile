FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install pocket-tts flask scipy huggingface_hub

# Copy the server
COPY app.py .

# HuggingFace token for accessing voice files
ENV HF_TOKEN=""

EXPOSE 8000

CMD ["python", "app.py"]