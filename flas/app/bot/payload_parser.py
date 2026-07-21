from typing import Any

class PayloadParser:

    def parse(
            self,
            payload: dict[str, Any]
    ) -> dict [str, Any]:
        data = payload.get(
            "data",
            {}
        )

        key = data.get(
            "key",
            {}
        )
        message = data.get("message", {})

        return {
            "instance_name": payload.get(
                "instance"
            ),
            "phone":key.get(
                "remoteJid",
                ""
            ),
            "message_id":key.get(
                "id"
            ),
            "from_me":key.get(
                "fromMe",
                False
            ),
            "message_type": self.get_message_type(
                message
            ),
            "message": self.get_message_text(
               message 
            ),
            
            "name": data.get(
            "pushName",
            ""
            )
        }
    
    def get_message_type(
            self,
            message: dict
    ) -> str:
        if"conversation" in message:
            return "text"
        
        if "extendedTextMessage" in message:
            return "text"
        
        if "imageMessage" in message:
            return "image"
        
        if "videoMessage" in message:
            return "video"
        
        if "documentMessage" in message:
            return "document"
        
        if "audioMessage" in message:
            return "audio"
        
        return "unknown"
    
    def get_message_text(
            self,
            message: dict
    )-> str:

       if "conversation" in message:
           return message["conversation"]

       if(
           "extendedTextMessage"
           in message
       ):
           return message["extendedTextMessage"].get("text", "")
       
       if(
           "imageMessage"
           in message
       ):
           return message["imageMessage"].get("caption", "")
       
       return ""