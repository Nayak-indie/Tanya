import json
import time
from typing import Dict, Any

class MemoryCore:
    def __init__(self, file_path="tanya_memory.json"):
        self.file_path = file_path
        try:
            with open(file_path, "r") as f:
                self.memory: Dict[str, Any] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.memory = {}

    def remember(self, key: str, value: Any):
        self.memory[key] = {"value": value, "timestamp": time.time()}
        self._save()

    def recall(self, key: str, default=None):
        return self.memory.get(key, {}).get("value", default)

    def forget(self, key: str):
        if key in self.memory:
            del self.memory[key]
            self._save()

    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.memory, f, indent=2)
