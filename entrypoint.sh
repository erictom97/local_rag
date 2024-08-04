#!/bin/bash

# Start Ollama service in the background
ollama serve &

# Wait for Ollama service to start
echo "Waiting for Ollama service to start..."
until curl -s http://localhost:11434/api/version > /dev/null; do
    sleep 1
done
echo "Ollama service is up and running."

# Pull the required models
echo "Pulling llama2 model..."
ollama pull llama2
echo "Pulling mxbai-embed-large model..."
ollama pull mxbai-embed-large

# Start the Flask application
echo "Starting Flask application..."
exec python app.py