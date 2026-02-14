"""
rust_bridge.py
---------------
Handles communication with Rust core.
"""

class RustBridge:
    def __init__(self):
        pass

    def send_task(self, task: dict) -> dict:
        return {"status": "pending"}
