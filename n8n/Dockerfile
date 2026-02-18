FROM docker.n8n.io/n8nio/n8n:latest

USER root

# Install curl to download Ollama
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy workflow
COPY workflow.json /workflow.json

# Startup script: run Ollama in background, pull model, then start n8n
CMD ["sh", "-c", "\
  ollama serve & \
  sleep 5 && \
  ollama pull llama3.2:3b  && \
  n8n import:workflow --input=/workflow.json && \
  n8n start \
"]

EXPOSE 5678 11434