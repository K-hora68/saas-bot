from dataclasses import dataclass
from typing import Any


@dataclass
class ConversationContext:

    tenant: Any
    contact: Any
    session: Any

    services: list[Any]
    knowledge: list[Any]
    history: list[Any]

    customer_message: str
    instance_name: str
    phone: str