from app.bot.payload_parser import PayloadParser
from app.bot.prompt_builder import PromptBuilder
from app.bot.ollama_service import OllamaService
from app.bot.response_parser import ResponseParser
from app.bot.conversation_context import ConversationContext

from app.evolution.evolution_service import EvolutionService

from app.repository.tenant_repo import Tenant_repo
from app.repository.contact_repo import Contact_repo
from app.repository.session_repo import Session_repo
from app.repository.service_repo import Service_repo
from app.repository.knowledgebase_repo import KnowledgeBase_repo
from app.repository.message_repo import Message_Repo

from app.config import Config

import logging

logger = logging.getLogger(__name__)


class BotEngine:

    def __init__(self):

        self.payload_parser = PayloadParser()
        self.prompt_builder = PromptBuilder()
        self.ollama_service = OllamaService(
            base_url=Config.OLLAMA_BASE_URL,
            model=Config.OLLAMA_MODEL
        )
        self.response_parser = ResponseParser()
        self.evolution_service = EvolutionService(
            api_url=Config.EVOLUTION_API_URL,
            api_key=Config.EVOLUTION_API_KEY
        )

        self.tenant_repo = Tenant_repo()
        self.contact_repo = Contact_repo()
        self.session_repo = Session_repo()
        self.service_repo = Service_repo()
        self.knowledgebase_repo = KnowledgeBase_repo()
        self.message_repo = Message_Repo()

    def process(
        self,
        payload: dict
    ):

        # -----------------------------------
        # Parse incoming webhook payload
        # -----------------------------------

        data = self.payload_parser.parse(payload)

        # ===================================
        # NEW: DEBUG INFORMATION
        # ===================================
        print("\n" + "=" * 70)
        print("BOT ENGINE PROCESS CALLED")
        print("=" * 70)
        print("=" * 60)
        print("MESSAGE ID :", data["message_id"])
        print("FROM ME    :", data["from_me"])
        print("PHONE      :", data["phone"])
        print("MESSAGE    :", data["message"])
        print("TYPE       :", data["message_type"])
        print("=" * 60)

        # ===================================
        # NEW: Ignore our own messages
        # ===================================

        if data["from_me"]:
            logger.info("Ignoring outgoing message.")
            return None

        # ===================================
        # NEW: Ignore empty messages
        # ===================================

        if not data["message"]:
            logger.info("Ignoring empty message.")
            return None

        # -----------------------------------
        # Load Tenant
        # -----------------------------------

        print("PARSED DATA:", data)
        print("INSTANCE NAME:", data.get("instance_name"))

        tenant = self.tenant_repo.get_by_instance(
            data["instance_name"]
        )

        if tenant is None:
            print("NO TENANT FOUND")
            return {
                "reply": "Tenant not Configured"
            }

        # -----------------------------------
        # Load Contact
        # -----------------------------------

        contact = self.contact_repo.get_or_create(
            instance_name=data["instance_name"],
            phone=data["phone"],
            name=data["name"]
        )

        # -----------------------------------
        # Load Session
        # -----------------------------------

        session = self.session_repo.get_or_create(
            contact_id=contact.id,
        )

        # -----------------------------------
        # Load Business Services
        # -----------------------------------

        services = self.service_repo.get_all(
            instance_name=data["instance_name"]
        )

        # -----------------------------------
        # Load Knowledge Base
        # -----------------------------------

        knowledge = self.knowledgebase_repo.get_all(
            data["instance_name"]
        )

        # -----------------------------------
        # Load Conversation History
        # -----------------------------------

        history = self.message_repo.get_history(
            session.id
        )

        # -----------------------------------
        # Build Conversation Context
        # -----------------------------------

        context = ConversationContext(
            tenant=tenant,
            contact=contact,
            session=session,
            services=services,
            knowledge=knowledge,
            history=history,
            customer_message=data["message"],
            instance_name=data["instance_name"],
            phone=data["phone"]
        )

        # -----------------------------------
        # Save Customer Message
        # -----------------------------------

        self.message_repo.create(
            session_id=session.id,
            sender="customer",
            message_type=data["message_type"],
            content=context.customer_message
        )

        # -----------------------------------
        # Build AI Prompt
        # -----------------------------------

        prompt = self.prompt_builder.build(context)

        # -----------------------------------
        # Ask Ollama
        # -----------------------------------

        try:
            ai_response = self.ollama_service.generate(prompt)

        except Exception as e:

            logger.error(f"Ollama generation failed: {str(e)}")

            ai_response = {
                "response": '{"reply":"I apologize, but I am temporarily unavailable. Please try again later.","media":[],"follow_up":""}'
            }

        # -----------------------------------
        # Parse AI Response
        # -----------------------------------

        response = self.response_parser.parse(ai_response)

        print("AI RESPONSE:", response)

        # -----------------------------------
        # Save Bot Response
        # -----------------------------------

        self.message_repo.create(
            session_id=session.id,
            sender="bot",
            message_type="text",
            content=response["reply"]
        )

        # ===================================
        # NEW: Debug send
        # ===================================

        print("=" * 60)
        print("SENDING MESSAGE")
        print("INSTANCE :", context.instance_name)
        print("PHONE    :", context.phone)
        print("TEXT     :", response["reply"])
        print("=" * 60)

        # -----------------------------------
        # Send Reply to WhatsApp
        # -----------------------------------

        self.evolution_service.send_text(
            instance_name=context.instance_name,
            phone=context.phone,
            message=response["reply"]
        )

        return response