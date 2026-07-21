import requests
import logging

logger = logging.getLogger(__name__)


class OllamaService:
    def __init__(
            self,
            base_url: str = "http://localhost:11434",
            model: str = "qwen2.5:1.5b"
    ):
        self.base_url = base_url
        self.model = model

    def generate(
            self,
            prompt: str
    ) -> dict:
        """
        Generate response from Ollama AI model.
        
        Args:
            prompt: The prompt to send to Ollama
            
        Returns:
            dict with response, model, and done status
            
        Raises:
            Exception: If Ollama is not running or request fails
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            print("Base URL:", self.base_url)
            print("Endpoint:", f"{self.base_url}/api/generate")
            print("Payload:", payload)

            logger.info(f"Sending prompt to Ollama (model: {self.model})")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=300  # Increased timeout to 5 minutes
            )
            
            response.raise_for_status()

            data = response.json()

            logger.info("Ollama response received successfully")
            
            return {
                "response": data.get("response", ""),
                "model": data.get("model"),
                "done": data.get("done", False)
            }
            print("Status:", response.status_code)
            print("Body:", response.text)
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Cannot connect to Ollama at {self.base_url}. Make sure Ollama is running.")
            raise Exception(
                f"Failed to connect to Ollama. Is it running at {self.base_url}? Error: {str(e)}"
            )
        except requests.exceptions.Timeout as e:
            logger.error(f"Ollama request timeout. Model might be too large or system is slow.")
            raise Exception(
                f"Ollama request timed out. Try a smaller model or increase timeout. Error: {str(e)}"
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama request failed: {str(e)}")
            raise Exception(f"Ollama request failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in Ollama service: {str(e)}")
            raise Exception(f"Unexpected Ollama error: {str(e)}")

    def list_models(self) -> list:
        """Get list of available models on Ollama."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get("models", [])
        except Exception as e:
            logger.error(f"Failed to list Ollama models: {str(e)}")
            return []

    def health_check(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get(
                f"{self.base_url}",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {str(e)}")
            return False