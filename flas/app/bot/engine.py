from bot.context_loader import load_context
from bot.prompt_builder import build_prompt
from bot.intent_detector import detect_intent
from bot.message_router import route_message

def process_message(message_data):

    context = load_context(message_data)
    prompt  = build_prompt(message_data, context)
    ai_result = detect_intent(prompt)
    reply = route_message(ai_result, context)


    return reply