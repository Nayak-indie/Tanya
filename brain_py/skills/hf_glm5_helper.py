"""
hf_glm5_helper.py
-----------------
HuggingFace model helper for running local models.
Supports various LLMs via HuggingFace transformers.
"""

from typing import List, Dict, Optional
import os


class HFModelHelper:
    """
    Helper for running local models via HuggingFace.
    Supports GGUF, GPTQ, AWQ formats.
    """
    
    def __init__(self, model_name: str = "microsoft/phi-2"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
    
    def load_model(self, quant_method: str = "gptq"):
        """
        Load model from HuggingFace.
        
        Args:
            model_name: Model ID from HuggingFace
            quant_method: Quantization method (gptq, awq, gguf)
        """
        try:
            # Check if we have required dependencies
            try:
                from transformers import AutoModelForCausalLM, AutoTokenizer
            except ImportError:
                return {
                    "status": "error",
                    "result": "transformers not installed. Run: pip install transformers torch"
                }
            
            # For now, return info about loading
            return {
                "status": "info",
                "model": self.model_name,
                "message": f"Model loading not fully implemented. Use Ollama for local inference.",
                "suggestion": "Run 'ollama pull " + self.model_name.split('/')[-1] + "' instead"
            }
            
        except Exception as e:
            return {"status": "error", "result": str(e)}
    
    def generate(self, prompt: str, **kwargs):
        """Generate response from model."""
        if not self.model:
            return {
                "status": "error",
                "result": "Model not loaded. Call load_model() first."
            }
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(**inputs, **kwargs)
            return {
                "status": "success",
                "result": self.tokenizer.decode(outputs[0])
            }
        except Exception as e:
            return {"status": "error", "result": str(e)}
    
    def list_available_models(self):
        """List models that can be loaded."""
        return [
            "microsoft/phi-2",
            "meta-llama/Llama-2-7b-chat-hf",
            "tiiuae/falcon-7b-instruct",
            "EleutherAI/gpt-neo-2.7B",
            "bigscience/bloom-560m",
        ]


# Global instance
_hf_helper = HFModelHelper()


def get_helper(model_name: str = None) -> HFModelHelper:
    """Get HF model helper instance."""
    if model_name:
        return HFModelHelper(model_name)
    return _hf_helper
