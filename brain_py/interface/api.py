"""
api.py
------
API interface for Tanya.
"""

class API:
    def __init__(self):
        pass

    def receive_request(self, request: dict) -> dict:
        return {"status": "ok"}
