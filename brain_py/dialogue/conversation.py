# brain_py/dialogue/conversation.py

from brain_py.memory.memory_core import MemoryCore

class ConversationState:
    def __init__(self, memory: MemoryCore):
        self.memory = memory
        self.topic = None

    def add_user(self, text: str):
        history = self.memory.recall("conversation", [])
        history.append({"speaker": "user", "text": text})
        self.memory.remember("conversation", history)
        self._infer_topic(text)

    def add_tanya(self, text: str):
        history = self.memory.recall("conversation", [])
        history.append({"speaker": "tanya", "text": text})
        self.memory.remember("conversation", history)

    def _infer_topic(self, text: str):
        self.topic = "discussion" if len(text.split()) > 6 else "command"
