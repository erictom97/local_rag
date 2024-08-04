# Use the official Ollama image as the base
FROM ollama/ollama:latest as ollama

# Use the official Python image for the final stage
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y \
    libasound2-dev \
    libespeak1\
    curl \
    && pip install --no-cache-dir -r requirements.txt

# Install Ollama CLI
COPY --from=ollama /usr/bin/ollama /usr/bin/ollama

# Copy the rest of the application code into the container
COPY . .

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Give execute permission to the entrypoint script
RUN chmod +x /app/entrypoint.sh

# Expose the ports the app and Ollama run on
EXPOSE 8000 11434

# Set the entrypoint to the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]