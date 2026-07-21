import requests
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class EvolutionService:
    """
    Client service for interacting with Evolution API.
    Handles sending and receiving messages through WhatsApp via Evolution API.
    """

    def __init__(self, api_url: str = None, api_key: str = None):

        self.api_url = api_url or "http://localhost:8080"
        self.api_key = api_key
        self.timeout = 10


    def _get_headers(self) -> Dict[str, str]:

        headers = {
            "Content-Type": "application/json"
        }

        if self.api_key:
            headers["apikey"] = self.api_key

        return headers


    def send_text(
        self,
        instance_name: str,
        phone: str,
        message: str
    ) -> Dict[str, Any]:

        try:
            url = f"{self.api_url}/message/sendText/{instance_name}"

            payload = {
                "number": phone,
                "text": message,
            }

            print("\n" + "=" * 70)
            print("SEND_TEXT CALLED")
            print("Instance:", instance_name)
            print("Phone:", phone)
            print("Message:", message)
            print("=" * 70)
            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout,
            )


            print("========== EVOLUTION SEND ==========")
            print("URL:", url)
            print("PAYLOAD:", payload)
            print("HEADERS:", self._get_headers())
            print("STATUS:", response.status_code)
            print("BODY:", response.text)
            print("====================================")
            print("API KEY:", self.api_key)

            response.raise_for_status()


            logger.info(
                f"Message sent successfully to {phone} via instance {instance_name}"
            )

            return response.json()


        except requests.exceptions.RequestException as e:

            logger.error(
                f"Error sending message: {str(e)}"
            )


            if e.response:
                print("========== EVOLUTION ERROR ==========")
                print(e.response.text)
                print("====================================")


            raise Exception(
                f"Failed to send message via Evolution API: {str(e)}"
            )



    def send_media(
        self,
        instance_name: str,
        phone: str,
        media_url: str,
        caption: str = None
    ) -> Dict[str, Any]:

        try:
            url = f"{self.api_url}/message/sendMedia/{instance_name}"

            payload = {
                "number": phone,
                "mediaUrl": media_url,
            }

            if caption:
                payload["caption"] = caption


            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout,
            )

            response.raise_for_status()


            return response.json()


        except requests.exceptions.RequestException as e:

            logger.error(
                f"Error sending media: {str(e)}"
            )

            raise Exception(
                f"Failed to send media via Evolution API: {str(e)}"
            )



    def get_instance_status(
        self,
        instance_name: str
    ) -> Dict[str, Any]:

        try:
            url = f"{self.api_url}/instance/info/{instance_name}"

            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()


        except requests.exceptions.RequestException as e:

            logger.error(
                f"Error getting instance status: {str(e)}"
            )

            raise Exception(
                f"Failed to get instance status: {str(e)}"
            )



    def create_instance(
        self,
        instance_name: str
    ) -> Dict[str, Any]:

        try:
            url = f"{self.api_url}/instance/create"

            payload = {
                "instanceName": instance_name
            }


            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()


        except requests.exceptions.RequestException as e:

            logger.error(
                f"Error creating instance: {str(e)}"
            )

            raise Exception(
                f"Failed to create instance: {str(e)}"
            )



    def set_webhook(
        self,
        instance_name: str,
        webhook_url: str,
        events: list = None
    ) -> Dict[str, Any]:

        try:
            url = f"{self.api_url}/webhook/set/{instance_name}"


            payload = {
                "webhook": {
                    "enabled": True,
                    "url": webhook_url,
                    "webhookByEvents": True,
                    "events": events or [
                        "MESSAGES_UPSERT"
                    ]
                }
            }


            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()


        except requests.exceptions.RequestException as e:

            logger.error(
                f"Error setting webhook: {str(e)}"
            )

            raise Exception(
                f"Failed to set webhook: {str(e)}"
            )



    def get_webhook(
        self,
        instance_name: str
    ) -> Dict[str, Any]:

        try:
            url = f"{self.api_url}/webhook/find/{instance_name}"


            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=self.timeout,
            )


            response.raise_for_status()

            return response.json()


        except requests.exceptions.RequestException as e:

            logger.error(
                f"Error getting webhook: {str(e)}"
            )

            raise Exception(
                f"Failed to get webhook: {str(e)}"
            )