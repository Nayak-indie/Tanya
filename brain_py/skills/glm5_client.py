"""
glm5_client.py
--------------
GLM-5 model client for advanced reasoning.
Uses Ollama-compatible API for GLM-style models.
"""

from typing import List, Dict, Optional
import requests
import os


class GLMClient:
    """
    Client for GLM-style models via Ollama.
    Falls back to local Ollama if no external API.
    """
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
    
    def send_message(self, messages: List[Dict], **kwargs) -> Dict:
        """
        Send message to GLM model.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: temperature, max_tokens, etc.
        
        Returns:
            Response dict with 'content' and metadata
        """
        try:
            # Use any available GLM-style model
            model = kwargs.get("model", "glm4:latest")
            
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.7),
                    "num_predict": kwargs.get("max_tokens", 2048),
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=kwargs.get("timeout", 120)
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "content": data.get("message", {}).get("content", ""),
                    "model": model,
                    "done": data.get("done", True)
                }
            else:
                return {
                    "status": "error",
                    "result": f"API error: {response.status_code}"
                }
                
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "result": "Cannot connect to Ollama. Is it running?"
            }
        except Exception as e:
            return {
                "status": "error",
                "result": str(e)
            }
    
    def generate(self, prompt: str, **kwargs) -> Dict:
        """Generate completion from prompt."""
        messages = [{"role": "user", "content": prompt}]
        return self.send_message(messages, **kwargs)


# Global instance
_glm_client = GLMClient()


def send_message(messages: List[Dict], **kwargs):
    """Convenience function."""
    return _glm_client.send_message(messages, **kwargs)


def generate(prompt: str, **kwargs):
    """Convenience function for completion."""
    return _glm_client.generate(prompt, **kwargs)
