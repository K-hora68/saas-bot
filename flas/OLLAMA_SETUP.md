# Ollama AI Setup Guide

## Overview

Your Flas chatbot uses **Ollama** as the AI engine to generate intelligent responses. Ollama is a lightweight LLM platform that runs locally.

## Prerequisites

- **Ollama installed** on your system
- **At least 4GB RAM** (8GB+ recommended)
- **Internet connection** (only for initial model download)

## Installation

### 1. **Download and Install Ollama**

- **Windows/Mac/Linux**: Download from [ollama.ai](https://ollama.ai)
- Follow the installation instructions for your OS

### 2. **Verify Installation**

Open terminal and run:

```bash
ollama --version
```

## Running Ollama

### Start Ollama Server

```bash
ollama serve
```

The server will start on `http://localhost:11434` (default port)

### Pull a Model

In a new terminal, pull the recommended model:

```bash
# Recommended: Qwen 2.5 (5.5B) - Fast and accurate
ollama pull qwen2.5:5.5b

# Or other options:
ollama pull llama2              # Llama2 7B
ollama pull mistral             # Mistral 7B
ollama pull neural-chat         # Neural Chat 7B
ollama pull dolphin-mixtral     # Dolphin Mixtral 8x7B
```

The first pull will download the model (~3-5GB depending on model).

## Configuration

### 1. **Create `.env` file**

```bash
cd flas
cp .env.example .env
```

### 2. **Edit `.env` with your Ollama settings**

```env
# Ollama AI Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:5.5b
```

### Model Selection

Choose based on your hardware:

| Model               | Size | Speed  | Accuracy  | RAM Required |
| ------------------- | ---- | ------ | --------- | ------------ |
| **qwen2.5:5.5b** ⭐ | 5.5B | Fast   | Good      | 4GB          |
| **mistral**         | 7B   | Medium | Excellent | 8GB          |
| **neural-chat**     | 7B   | Medium | Good      | 8GB          |
| **llama2**          | 7B   | Medium | Good      | 8GB          |
| **dolphin-mixtral** | 8x7B | Slow   | Excellent | 16GB+        |

## Verify Setup

### 1. **Start all services**

Terminal 1 - Start Ollama:

```bash
ollama serve
```

Terminal 2 - Start Flask:

```bash
cd flas
python Run.py
```

### 2. **Test Ollama connection**

```bash
curl http://localhost:11434/api/tags
```

Should return available models in JSON format.

### 3. **Test the bot**

Using the Flask app:

```bash
curl -X POST http://localhost:5000/webhook/health
```

Should return:

```json
{ "status": "healthy", "service": "flas-webhook", "timestamp": "..." }
```

## How It Works

### Message Flow

1. **User sends WhatsApp message**
2. **Webhook receives message** → `/webhook/messages`
3. **BotEngine processes**:
   - Parses message payload
   - Loads conversation history
   - Builds detailed prompt with context
   - **Sends to Ollama** via `http://localhost:11434/api/generate`
   - Ollama generates AI response
   - Parses response as JSON
4. **Saves to database**
5. **Sends reply via WhatsApp** (Evolution API)

### Prompt Structure

The prompt sent to Ollama includes:

- Business information
- Available services
- Knowledge base
- Customer information
- Conversation history
- Customer message
- Response format requirements

Example prompt:

```
You are the official WhatsApp assistant for [Business Name].

==========================
BUSINESS INFORMATION
==========================

Business Name: MyBusiness
Description: We provide services...

==========================
AVAILABLE SERVICES
==========================

Name: Service 1
Description: ...
Price: $50

==========================
KNOWLEDGE BASE
==========================

Q: How do I book?
A: You can book through WhatsApp...

==========================
CUSTOMER MESSAGE
==========================

Hello, I want to know about your services

==========================
RESPONSE FORMAT
==========================

Return ONLY valid JSON.
{
    "reply": "...",
    "media": [],
    "follow_up": ""
}
```

## Troubleshooting

### Ollama Connection Error

**Error**: `Failed to connect to Ollama at http://localhost:11434`

**Solution**:

1. Check Ollama is running: `ollama serve`
2. Verify URL is correct in `.env`
3. Check firewall/network permissions

### Model Not Found

**Error**: `Model 'qwen2.5:5.5b' not found`

**Solution**:

```bash
# Pull the model
ollama pull qwen2.5:5.5b

# List available models
ollama list
```

### Response Timeout

**Error**: `Ollama request timed out`

**Solution**:

1. Model might be too large for your hardware
2. Try a smaller model (e.g., `mistral` instead of `dolphin-mixtral`)
3. Increase timeout in code (currently 300 seconds / 5 minutes)

### Slow Responses

**Issue**: Responses take >30 seconds

**Solutions**:

- Use a smaller model
- Allocate more RAM to your system
- Run Ollama on GPU if available:
  ```bash
  # Install NVIDIA CUDA support
  # Then Ollama will automatically use GPU
  ```

### Out of Memory

**Error**: `CUDA out of memory` or system freezes

**Solution**:

1. Use a smaller model
2. Close other applications
3. Increase system swap/virtual memory
4. Upgrade RAM

## Hardware Recommendations

### Minimum (Functional)

- CPU: Modern dual-core
- RAM: 4GB
- Storage: 10GB SSD

### Recommended (Good Performance)

- CPU: 4-core or better
- RAM: 8-16GB
- Storage: 20GB SSD
- GPU: NVIDIA with CUDA (optional but faster)

### Optimal (Fast Responses)

- CPU: 8+ core
- RAM: 16GB+
- Storage: Fast SSD 50GB+
- GPU: NVIDIA RTX 3060+ or equivalent

## Advanced Configuration

### Use GPU (NVIDIA)

1. Install NVIDIA CUDA
2. Install cuDNN
3. Ollama will auto-detect and use GPU

### Use Different Ollama Port

```env
OLLAMA_BASE_URL=http://localhost:9999
```

Then run:

```bash
ollama serve --port 9999
```

### Use Remote Ollama

```env
OLLAMA_BASE_URL=http://remote-server:11434
```

## Available Models

Visit [Ollama Model Library](https://ollama.ai/library) for full list. Popular choices:

- **qwen2.5:5.5b** - Fast, good for business use
- **mistral** - Fast, good reasoning
- **llama2** - Popular, well-tuned
- **neural-chat** - Good for conversations
- **dolphin-mixtral** - Best quality (slow, requires 16GB+ RAM)

## Uninstall/Reset

### Stop Ollama

```bash
# Kill the process or close the application
```

### Remove Models

```bash
rm -rf ~/.ollama  # Linux/Mac
rmdir %USERPROFILE%\.ollama  # Windows
```

### Reinstall

1. Uninstall Ollama application
2. Remove models folder
3. Reinstall from [ollama.ai](https://ollama.ai)

## Production Deployment

### Using Docker

```yaml
# docker-compose.yml
version: "3"
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0:11434

  flas:
    build: ./flas
    ports:
      - "5000:5000"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama

volumes:
  ollama_data:
```

Run with:

```bash
docker-compose up -d
```

## Monitoring

### Check Ollama Status

```bash
# List models
ollama list

# Show model info
ollama show qwen2.5:5.5b
```

### View Logs

Logs are printed to console when running `ollama serve`.

## Resources

- [Ollama Official Docs](https://github.com/ollama/ollama)
- [Model Library](https://ollama.ai/library)
- [Community](https://github.com/ollama/ollama/discussions)
