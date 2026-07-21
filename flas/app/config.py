import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///user.db"
    JWT_SECRET_KEY = "Kahora@2006"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Evolution API Configuration
    EVOLUTION_API_URL = os.getenv(
        "EVOLUTION_API_URL",
        "http://localhost:8080"
    )

    EVOLUTION_API_KEY = os.getenv(
        "EVOLUTION_API_KEY",
        None
    )
    print("Evolution URL:", EVOLUTION_API_URL)
    print("Evolution key loaded:", EVOLUTION_API_KEY)
    
    # Webhook Configuration
    WEBHOOK_URL = os.getenv(
        "WEBHOOK_URL",
        "http://localhost:5000/webhook"
    )

    WEBHOOK_EVENTS = os.getenv(
        "WEBHOOK_EVENTS",
        "messages,message_status,connection_update"
    )
    
    # Ollama AI Configuration
    OLLAMA_BASE_URL = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    OLLAMA_MODEL = os.getenv(
        "OLLAMA_MODEL",
        "qwen2.5:1.5b"
    )