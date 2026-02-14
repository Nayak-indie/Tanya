"""
short_term.py
-------------
Handles working memory (volatile, resettable).
"""

class ShortTermMemory:
    def __init__(self):
        self.memory = {}

    def remember(self, key: str, value):
        self.memory[key] = value

    def recall(self, key: str):
        return self.memory.get(key, None)
