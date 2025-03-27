#!/bin/bash

echo "Starting Ollama server..."
ollama serve &  # Start Ollama in the background

echo "Ollama is ready, creating the model..."
ollama pull mistral

# ollama create finetuned_mistral -f model_files/Modelfile
ollama run mistral