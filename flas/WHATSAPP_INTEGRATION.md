# WhatsApp Evolution API Integration Guide

## Overview

Your Flas project is now fully integrated with **Evolution API** for WhatsApp messaging. This enables your bot to both **send and receive** messages through WhatsApp.

## Architecture

```
WhatsApp User ↔ Evolution API ↔ Flask App (Flas)
                    ↓
              Webhooks to Flask
                    ↓
              BotEngine processes message
                    ↓
              LLM/Ollama generates response
                    ↓
              Evolution API sends reply
```

## Setup Instructions

### 1. **Configure Environment Variables**

Create a `.env` file from `.env.example`:

```bash
# Evolution API Configuration
EVOLUTION_API_URL=http://localhost:3333
EVOLUTION_API_KEY=your_api_key_here

# Webhook Configuration (URL where Evolution API sends messages)
WEBHOOK_URL=http://localhost:5000/webhook
WEBHOOK_EVENTS=messages,message_status,connection_update

# Database Configuration
SQLALCHEMY_DATABASE_URI=sqlite:///user.db

# JWT Configuration
JWT_SECRET_KEY=Kahora@2006
```

### 2. **Start Evolution API**

If running Evolution API locally:

```bash
# Using Docker Compose (from evolution-api folder)
docker-compose up -d

# Or using the official setup
# Follow: https://docs.evolutionfoundation.com.br
```

### 3. **Configure Evolution API Webhook**

Set up the webhook in your Evolution API instance to point to your Flask app:

```bash
curl -X POST http://localhost:3333/webhook/set/<instance_name> \
  -H "Content-Type: application/json" \
  -d '{
    "webhook": "http://your-flask-app:5000/webhook/messages",
    "events": ["messages", "message_status"]
  }'
```

Or use the `EvolutionService.set_webhook()` method:

```python
from app.evolution import EvolutionService
from app.config import Config

service = EvolutionService(
    api_url=Config.EVOLUTION_API_URL,
    api_key=Config.EVOLUTION_API_KEY
)

service.set_webhook(
    instance_name="my_instance",
    webhook_url="http://your-flask-app:5000/webhook/messages",
    events=["messages", "message_status"]
)
```

### 4. **Start Flas Application**

```bash
cd flas
source .venv/Scripts/activate  # On Windows, or .venv/Scripts/activate
python Run.py
```

The Flask app will start on `http://localhost:5000`

## Available Endpoints

### Receiving Messages (Webhooks)

#### 1. **Message Webhook** - Receives incoming WhatsApp messages

```
POST /webhook/messages
```

Evolution API sends incoming messages here. The BotEngine processes them and generates responses.

#### 2. **Status Webhook** - Receives message status updates

```
POST /webhook/status
```

Receives updates like: message_sent, message_delivered, message_read, message_failed

#### 3. **Events Webhook** - Receives general events

```
POST /webhook/events
```

Connection updates, instance created/deleted, etc.

#### 4. **Health Check**

```
GET /webhook/health
```

Check if webhook endpoint is running.

## EvolutionService API Reference

### Sending Messages

```python
from app.evolution import EvolutionService

service = EvolutionService(
    api_url="http://localhost:3333",
    api_key="your_key"  # optional
)

# Send text message
response = service.send_text(
    instance_name="my_instance",
    phone="+5511999999999",
    message="Hello from bot!"
)

# Send media (image, video, audio)
response = service.send_media(
    instance_name="my_instance",
    phone="+5511999999999",
    media_url="https://example.com/image.jpg",
    caption="Check this out!"
)
```

### Instance Management

```python
# Create new instance
response = service.create_instance(instance_name="new_instance")

# Get instance status
status = service.get_instance_status(instance_name="my_instance")

# Set webhook
response = service.set_webhook(
    instance_name="my_instance",
    webhook_url="http://your-app:5000/webhook/messages",
    events=["messages", "message_status"]
)

# Get webhook config
webhook = service.get_webhook(instance_name="my_instance")
```

### Message Management

```python
# Get messages
messages = service.get_messages(
    instance_name="my_instance",
    limit=10,
    offset=0
)

# Mark message as read
response = service.mark_as_read(
    instance_name="my_instance",
    message_id="msg_id_123"
)
```

## Message Flow

### Incoming Message Flow

1. **User sends WhatsApp message** → Evolution API
2. **Evolution API sends webhook** → `/webhook/messages`
3. **BotEngine processes message**:
   - Parse payload
   - Load tenant/contact/session
   - Get conversation history
   - Build context
   - Generate LLM response via Ollama
   - Parse response
4. **Save to database**
5. **Send reply via EvolutionService** → WhatsApp user

### Outgoing Message Flow

```python
# In your code
from app.evolution import EvolutionService

service = EvolutionService()
service.send_text(
    instance_name="my_instance",
    phone=user_phone,
    message="Your bot response"
)
```

## Database Models

The integration uses these models:

- **Tenant**: Business/Organization account
- **Contact**: WhatsApp user/contact
- **Session**: Conversation session
- **Message**: Individual messages sent/received
- **Service**: Business services offered
- **KnowledgeBase**: Information the bot uses

## Error Handling

All methods include proper error logging and exception handling:

```python
from app.evolution import EvolutionService

service = EvolutionService()

try:
    response = service.send_text(
        instance_name="instance",
        phone="+5511999999999",
        message="Hello"
    )
except Exception as e:
    print(f"Error: {e}")
    # Handle error
```

## Testing

### Test Sending a Message

```bash
curl -X POST http://localhost:5000/webhook/health
# Should return: {"status": "healthy", "service": "flas-webhook", ...}
```

### Test Webhook

```bash
curl -X POST http://localhost:5000/webhook/messages \
  -H "Content-Type: application/json" \
  -d '{
    "instance_name": "test_instance",
    "phone": "+5511999999999",
    "message": "Test message"
  }'
```

## Troubleshooting

### Webhooks not receiving messages

1. Check Evolution API URL is correct
2. Verify webhook URL is publicly accessible (if Evolution API is external)
3. Confirm webhook is set on the Evolution API instance
4. Check Flask app is running: `GET http://localhost:5000/webhook/health`

### Messages not being processed

1. Check BotEngine logs in Flask console
2. Verify database connection
3. Check Ollama service is running (for LLM responses)
4. Review incoming payload structure

### Connection errors

1. Verify Evolution API is running
2. Check API URL and key configuration
3. Test connectivity: `curl http://your-evolution-api:3333`

## Next Steps

1. Configure your Evolution API instance with webhook
2. Test message sending with the endpoints
3. Set up environment variables properly
4. Deploy to production (update WEBHOOK_URL to public URL)

## Resources

- [Evolution API Docs](https://docs.evolutionfoundation.com.br)
- [Evolution API GitHub](https://github.com/evolution-foundation/evolution-api)
- [Flask Documentation](https://flask.palletsprojects.com)
