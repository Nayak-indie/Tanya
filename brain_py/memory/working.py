"""
working.py
----------
Short-term (working) memory for Tanya.
Resets on shutdown.
"""

class WorkingMemory:
    def __init__(self):
        self._data = {}

    def set(self, key: str, value):
        self._data[key] = value

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def clear(self):
        self._data.clear()

    def snapshot(self):
        return dict(self._data)
