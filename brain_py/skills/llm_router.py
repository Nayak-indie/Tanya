
from brain_py.skills.mixtral_client import send_message as mixtral_send

def llm_router(messages, model="mixtral"):
    """
    Route chat messages to local Mixtral (Ollama).
    Args:
        messages: list of dicts, e.g. [{"role": "user", "content": "Hi"}]
        model: "mixtral" (ignored)
    Returns:
        str: model response text
    """
    return mixtral_send(messages)
