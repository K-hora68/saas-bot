from flask import Blueprint, jsonify, request
import logging
import time
from datetime import datetime

from app.extensions import db
from app.models.messages import Message
from app.bot.botEngine import BotEngine


webhook_bp = Blueprint("webhook", __name__)
logger = logging.getLogger(__name__)
bot_engine = BotEngine()


    # """
    # Webhook endpoint to receive incoming messages from Evolution API.
    # Evolution API sends messages here based on the webhook configuration.
    # """
    # try:
    #     data = request.get_json(silent=True) or {}
        
    #     if not data:
    #         return jsonify({"status": "received"}), 200
        
    #     logger.info(f"Received webhook: {data}")
        
    #     # Process the message through BotEngine
    #     # The BotEngine.process() method expects payload with specific structure
    #     response = bot_engine.process(data)
        
    #     return jsonify({
    #         "status": "processed",
    #         "response": response
    #     }), 200
        
    # except Exception as e:
    #     logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
    #     return jsonify({
    #         "status": "error",
    #         "message": str(e)
    #     }), 500
@webhook_bp.route("/webhook/messages", methods=["POST"])
def receive_message():
    print("=" * 60)
    print("WEBHOOK RECEIVED")
    print("TIME:", time.time())
    print(request.json["data"]["key"]["id"])
    print("=" * 60)
    data = request.get_json(silent=True) or {}

    message_data = data.get("data", {})

    # Ignore messages sent by your own WhatsApp account
    if message_data.get("key", {}).get("fromMe", False):
        return jsonify({
            "status": "ignored",
            "reason": "from_me"
        }), 200

    # Ignore events without a text message
    if not (
        message_data.get("message", {}).get("conversation") or
        message_data.get("message", {}).get("extendedTextMessage")
    ):
        return jsonify({
            "status": "ignored",
            "reason": "not_text"
        }), 200
    print("=" * 70)
    print("WEBHOOK RECEIVED")
    print(request.json)
    print("=" * 70)
    response = bot_engine.process(data)

    print("====================")
    print("BOT RESPONSE:", response)
    print("====================")

    return jsonify({
        "status": "processed",
        "response": response
    }), 200

@webhook_bp.route("/", methods=["POST"])
def webhook():
    print("=" * 60)
    print("WEBHOOK RECEIVED")
    print(request.json)
    print("=" * 60)
    return "", 200

@webhook_bp.route("/webhook/status", methods=["POST"])
def webhook_status():
    """
    Webhook endpoint to receive message status updates from Evolution API.
    (e.g., message sent, delivered, read, failed)
    """
    try:
        data = request.get_json(silent=True) or {}
        
        logger.info(f"Message status update: {data}")
        
        # Update message status in database if needed
        if data.get("messageId"):
            message = Message.query.filter_by(
                external_id=data.get("messageId")
            ).first()
            
            if message:
                message.status = data.get("status", "unknown")
                message.updated_at = datetime.utcnow()
                db.session.commit()
                logger.info(f"Updated message status: {data.get('messageId')} -> {data.get('status')}")
        
        return jsonify({"status": "received"}), 200
        
    except Exception as e:
        logger.error(f"Error processing status update: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@webhook_bp.route("/webhook/events", methods=["POST"])
def webhook_events():
    """
    Generic webhook endpoint for other Evolution API events.
    """
    try:
        data = request.get_json(silent=True) or {}
        
        event_type = data.get("event")
        logger.info(f"Received event: {event_type} - {data}")
        
        # Handle different event types
        if event_type == "connection.update":
            logger.info(f"Connection update: {data.get('instance')}")
        elif event_type == "instance.created":
            logger.info(f"Instance created: {data.get('instance')}")
        elif event_type == "instance.deleted":
            logger.info(f"Instance deleted: {data.get('instance')}")
        
        return jsonify({"status": "received"}), 200
        
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@webhook_bp.route("/webhook/health", methods=["GET"])
def webhook_health():
    """
    Health check endpoint for Evolution API webhooks.
    """
    return jsonify({
        "status": "healthy",
        "service": "flas-webhook",
        "timestamp": datetime.utcnow().isoformat()
    }), 200
