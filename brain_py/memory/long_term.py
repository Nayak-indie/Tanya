"""
long_term.py
------------
Handles persistent memory (SQLite, Redis, etc.).
"""

class LongTermMemory:
    def __init__(self):
        self.storage_path = "data/long_term.db"

    def save(self, key: str, value):
        pass

    def load(self, key: str):
        return None
